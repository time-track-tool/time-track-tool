#! /usr/bin/python
# Copyright (C) 2014-22 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************

from   math   import ceil
from   time   import gmtime
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import re
import common
import user_dynamic
import vacation
import o_permission
from   roundup.date           import Date, Interval
from   roundup.cgi.actions    import NewItemAction
from   roundup.cgi.exceptions import Redirect
from   roundup.cgi.templating import HTMLItem
from   roundup.rest           import _data_decorator, Routing, RestfulInstance


def user_leave_submissions (db, context):
    dt  = '%s;' % Date ('. - 14m').pretty (common.ymd)
    uid = db._db.getuid ()
    d   = dict (user = uid, first_day = dt)
    s   = [('+', 'first_day')]
    ls = db.leave_submission.filter (None, d, s)
    return ls
# end def user_leave_submissions

def approval_stati (db):
    st  = ('submitted', 'cancel requested')
    st  = [db._db.leave_status.lookup (x) for x in st]
    return dict (status = st)
# end def approval_stati

def approve_leave_submissions (db, utils, context):
    uid = db._db.getuid ()
    d   = approval_stati (db)
    d ['user'] = list (utils.approval_for (db, True))
    ls  = db.leave_submission.filter (None, d)
    return ls
# end def approve_leave_submissions

def approve_leave_submissions_hr (db, context, request):
    uid = db._db.getuid ()
    if not common.user_has_role \
        (db._db, uid, 'HR-leave-approval', 'HR-vacation'):
        return []
    fs  = request.filterspec
    d   = {}
    for n in ('status', 'user', 'time_wp.project', 'first_day', 'last_day'):
        if n in fs:
            d [n] = fs [n]
    ls  = db.leave_submission.filter (None, d)
    if 'approval_hr' in fs:
        new_ls = []
        for l in ls:
            tp  = l.time_wp.project
            fd  = l.first_day._value
            ld  = l.last_day._value
            u   = l.user.id
            dyn = user_dynamic.get_user_dynamic (db._db, u, fd)
            ctp = dyn.contract_type
            hr  = vacation.need_hr_approval \
                (db._db, tp, u, ctp, fd, ld, str (l.status.name), False)
            ah  = fs ['approval_hr'].lower () == 'yes'
            if hr == ah:
                new_ls.append (l)
        ls = new_ls
    return ls
# end def approve_leave_submissions_hr

class Leave_Buttons (object):
    user_buttons = dict \
        (( ('open',             ( ('submitted',        ""'Submit')
                                , ('cancelled',        ""'Cancel')
                                )
           )                   
         , ('submitted',        (('open',              ""'Edit again'), ))
         , ('accepted',         (('cancel requested',  ""'Request Cancel'), ))
        ))

    approve_buttons = dict \
        (( ('submitted',        ( ('accepted',         ""'Accept')
                                , ('declined',         ""'Decline')
                                )
           )
         , ('cancel requested', ( ('cancelled',        ""'Allow cancel')
                                , ('accepted',         ""'Decline cancel')
                                )
           )
        ))

    def __init__ (self, db):
        self.htmldb    = db
        self.db        = db._db
        self.st_open   = self.db.leave_status.lookup ('open')
        self.st_subm   = self.db.leave_status.lookup ('submitted')
        self.st_accp   = self.db.leave_status.lookup ('accepted')
        self.st_cncr   = self.db.leave_status.lookup ('cancel requested')
        self.uid       = self.db.getuid ()
    # end def __init__

    def button (self, newstate, msg):
        msg = msg % self.__dict__
        designator = self.ep_status.item.designator ()
        return \
            '''<input type="button" value="%(msg)s" onClick="
               if (submit_once ()) {
                   document.forms.edit_leave_submission
                       ['%(designator)s@status'].value = '%(newstate)s';
                   document.forms.edit_leave_submission.submit ();
               }">
            ''' % locals ()
    # end def button

    def generate (self, ep_status):
        """ Buttons in leave submission forms (edit or approval)
        """
        ret            = []
        self.ep_status = ep_status
        self.user      = ep_status.item.user.id
        self.sunick    = str (ep_status.item.user.supervisor.nickname).upper ()
        stname         = str (ep_status.prop.name)
        db             = ep_status.item._db
        if (self.uid == self.user and stname in self.user_buttons):
            for b in self.user_buttons [stname]:
                ret.append (self.button (*b))
        elif stname in self.approve_buttons and self.uid != self.user:
            if common.user_has_role (self.db, self.uid, 'HR-leave-approval'):
                for b in self.approve_buttons [stname]:
                    ret.append (self.button (*b))
            else:
                tp        = ep_status.item.time_wp.project.id
                tp        = db.time_project.getnode (tp)
                first_day = ep_status.item.first_day._value
                last_day  = ep_status.item.last_day._value
                dyn       = user_dynamic.get_user_dynamic \
                    (db, self.user, last_day)
                ctype     = dyn.contract_type
                need_hr   = vacation.need_hr_approval \
                    (db, tp, self.user, ctype, first_day, last_day, stname)
                if  (   self.uid in common.tt_clearance_by (self.db, self.user)
                    and not need_hr
                    ):
                    for b in self.approve_buttons [stname]:
                        ret.append (self.button (*b))
        if ret:
            ret.append \
                ( '<input type="hidden" name="%s@status" value="%s">'
                % (ep_status.item.designator (), stname)
                )
        return ''.join (ret)
    # end def generate
# end class Leave_Buttons

def remaining_until (db, uid = None, now = None):
    try:
        db  = db._db
    except AttributeError:
        pass
    if now is None:
        now = Date ('.')
    if uid is None:
        uid = db.getuid ()
    dyn = user_dynamic.get_user_dynamic (db, uid, now)
    if dyn is None:
        return None
    return vacation.next_yearly_vacation_date \
        (db, uid, dyn.contract_type, now) - common.day
# end def remaining_until

def remaining_vacation (db, user, ctype = -1, date = None):
    remain = vacation.remaining_vacation
    c = ceil (remain (db, user, ctype = ctype, date = date))
    if c == 0:
        return 0.0
    return float (c)
# end def remaining_vacation

def consolidated_vacation (db, user, date):
    return ceil (vacation.consolidated_vacation (db, user, date = date))
# end def remaining_vacation

def _get_ctype (db, user, start, end):
    now = Date ('.')
    if start <= now <= end:
        dyn = user_dynamic.get_user_dynamic (db, user, now)
    else:
        dyn = user_dynamic.get_user_dynamic (db, user, start)
    return dyn.contract_type
# end def _get_ctype

def _get_stati (db, statusname):
    st  = [db.leave_status.lookup (statusname)]
    if statusname == 'accepted':
        st.append (db.leave_status.lookup ('cancel requested'))
    return st
# end def _get_stati

def vacation_with_status (db, user, start, end, statusname):
    stati = _get_stati (db, statusname)
    ctype = _get_ctype (db, user, start, end)
    return vacation.vacation_submission_days \
        (db, user, ctype, start, end, * stati)
# end def vacation_with_status

def flexitime_with_status (db, user, start, end, statusname):
    stati = _get_stati (db, statusname)
    ctype = _get_ctype (db, user, start, end)
    return vacation.flexitime_submission_days \
        (db, user, ctype, start, end, * stati)
# end def flexitime_with_status

class New_Leave_Action (NewItemAction):

    fixurl = re.compile (r'[0-9]*$')
    def handle (self):
        url = None
        try:
            NewItemAction.handle (self)
        except Redirect as exc:
            try:
                url = exc.message
            except AttributeError:
                url = exc.args [0]
        if url:
            up     = url.split  ('?', 1)
            up [0] = self.fixurl.sub ('', up [0])
            url    = '?'.join (up)
            raise Redirect (url)
    # end def handle

# end class New_Leave_Action

def leave_days (db, user, first_day, last_day):
    if first_day is None or last_day is None:
        return 0
    if not isinstance (first_day, Date):
        try:
            first_day = Date (first_day._value)
        except AttributeError:
            first_day = Date (first_day)
    if not isinstance (last_day, Date):
        try:
            last_day = Date (last_day._value)
        except AttributeError:
            last_day = Date (last_day)
    try:
        return vacation.leave_days (db, user, first_day, last_day)
    except AssertionError:
        return 'Invalid data'
# end def leave_days

def eoy_vacation (db, user, date, ctype = -1):
    eoy = Date (date.pretty ('%Y-12-31'))
    vc  = vacation.get_vacation_correction (db, user, ctype, date)
    assert vc
    yday, pd, carry, ltot = vacation.vacation_params (db, user, eoy, vc)
    cons  = vacation.consolidated_vacation (db, user, vc.contract_type, eoy)
    return float (ceil (cons - ltot + carry))
# end def eoy_vacation

def month_name (date):
    d = Date (date)
    return d.pretty ('%B')
# end def month_name

class Leave_Display (object):

    def __init__ \
        ( self, db, user, supervisor, dt
        , types             = None
        , lim_dt            = True
        , all_user_fallback = True
        , absence_type      = None
        ):
        self.db = db
        try:
            self.db = db = db._db
        except AttributeError:
            pass
        if types is None:
            types = 'absence holiday homeoffice inoffice weekend'.split ()
        self.types = set (types)
        now        = self.now = Date ('.')
        if not dt:
            som = common.start_of_month (now)
            eom = common.end_of_month (now)
            dt  = common.pretty_range (som, eom)
        try:
            fd, ld = dt.split (';')
        except ValueError:
            fd = ld = dt
        self.fdd   = fdd = Date (fd)
        self.ldd   = ldd = Date (ld)
        self.month = month_name (self.fdd)
        if lim_dt:
            if common.start_of_month (fdd) != common.start_of_month (ldd):
                self.ldd = ldd = common.end_of_month (fdd)
                dt = common.pretty_range (fdd, ldd)
        srt        = [('+', a) for a in ('lastname', 'firstname')]
        self.users = users = []
        valid = db.user_status.filter (None, dict (name = 'valid'))
        vstatus = dict (status = valid)
        if user:
            self.users = users = db.user.filter (user, vstatus, sort = srt)
        if supervisor:
            d = dict (vstatus)
            d.update (supervisor = supervisor)
            u = db.user.filter (None, d, sort = srt)
            users.extend (u)
        use_all_users = \
            not self.users and (not (user or supervisor) or all_user_fallback)
        if use_all_users:
            self.users = users = db.user.filter (None, vstatus, sort = srt)
        else:
            self.users = users = db.user.filter (users, vstatus, sort = srt)
        acc = db.leave_status.lookup ('accepted')
        flt = dict \
            ( first_day = ';%s' % fd
            , last_day  = '%s;' % ld
            , user      = users
            , status    = acc
            )
        sp  = ('user.lastname', 'user.firstname', 'first_day')
        srt = [('+', a) for a in sp]
        lvfirst  = db.leave_submission.filter \
            (None, dict (first_day = dt, user = users, status = acc))
        lvlast   = db.leave_submission.filter \
            (None, dict (last_day = dt, user = users, status = acc))
        lvperiod = db.leave_submission.filter (None, flt)
        lvs = list (set (lvfirst + lvlast + lvperiod))
        # Put them in a dict by user-id
        self.lvdict = {}
        for id in lvs:
            lv = db.leave_submission.getnode (id)
            if lv.user not in self.lvdict:
                self.lvdict [lv.user] = []
            self.lvdict [lv.user].append (lv)

        # Get all absence records in the given time range, same algo as for
        if 'status' in flt:
            del flt ['status']
        fifi = dict (first_day = dt, user = users)
        lafi = dict (last_day  = dt, user = users)
        if absence_type:
            fifi.update (absence_type = absence_type)
            lafi.update (absence_type = absence_type)
            flt.update  (absence_type = absence_type)
        abfirst  = db.absence.filter (None, fifi)
        ablast   = db.absence.filter (None, lafi)
        abperiod = db.absence.filter (None, flt)
        abs = list (set (abfirst + ablast + abperiod))
        # Put them in a dict by user-id
        self.abdict = {}
        for id in abs:
            ab = db.absence.getnode (id)
            if ab.user not in self.abdict:
                self.abdict [ab.user] = []
            self.abdict [ab.user].append (ab)

        # Get public holidays
        srt = [('+', 'date')]
        ph  = db.public_holiday.filter (None, dict (date = dt), sort = srt)
        # Index by location/org_location and sort by date
        self.by_location = {}
        self.by_olo = {}
        for id in ph:
            holiday = db.public_holiday.getnode (id)
            for loc in holiday.locations:
                if loc not in self.by_location:
                    self.by_location [loc] = []
                self.by_location [loc].append (holiday)
            for olo in holiday.org_location:
                if olo not in self.by_olo:
                    self.by_olo [olo] = []
                self.by_olo [olo].append (holiday)

        self.abs_v = db.absence_type.getnode (db.absence_type.lookup ('V'))
        self.abs_a = db.absence_type.getnode (db.absence_type.lookup ('A'))
    # end def __init__

    @classmethod
    def from_request (cls, db, request):
        user = supervisor = dt = None
        if request.filterspec:
            if 'date' in request.filterspec:
                dt = request.filterspec ['date']
            if 'first_day' in request.filterspec:
                dt = request.filterspec ['first_day']
            if 'user' in request.filterspec:
                user = request.filterspec ['user']
            if 'supervisor' in request.filterspec:
                supervisor = request.filterspec ['supervisor']
        obj = cls (db, user, supervisor, dt)
        # Needed by month_link method which is only used by html form
        obj.request = request
        return obj
    # end def from_request

    def as_dict_entry (self, typ = None, abs = None, **kw):
        """ Return a dictionary for use with the REST API
            The typ is an absence_type
        """
        d = {}
        if abs:
            if abs.absence_type:
                typ = self.db.absence_type.getnode (abs.absence_type)
            else:
                d.update (type = 'absence')
        if typ:
            t = dict \
                ( id          = typ.id
                , link        = self.data_path + 'absence_type/' + typ.id
                , description = typ.description
                , code        = typ.code
                , cssclass    = typ.cssclass
                )
            d.update (absence_type = t, type = 'absence')
            if typ.cssclass == 'inoffice':
                d.update (type = 'inoffice')
            if typ.cssclass == 'homeoffice':
                d.update (type = 'homeoffice')
        if 'holiday' in kw:
            h  = kw ['holiday']
            hd = dict \
                ( description = h.description
                , name        = h.name
                , id          = h.id
                , link        = self.data_path + 'public_holiday/' + h.id
                )
            d.update (holiday = hd, type = 'holiday')
        if 'lolo' in kw:
            lolo = kw ['lolo']
            cn   = lolo.cl.classname
            lid  = dict \
                ( id   = lolo.id
                , name = lolo.name
                , link = self.data_path + cn + '/' + lolo.id
                )
            d [cn] = lid
        return d
    # end def as_dict_entry

    def as_dict (self, rest_instance, path):
        """ GET request for timesheet
        """

        self.data_path = path
        uid = self.db.getuid ()
        if not self.db.security.hasPermission ('View', uid, 'timesheet'):
            raise Unauthorised ('Permission to view timesheet denied')
        result = []
        for u in self.users:
            user = self.db.user.getnode (u)
            rec = {}
            rec ['user'] = dict \
                ( id        = user.id
                , link      = self.data_path + 'user/' + user.id
                , lastname  = user.lastname
                , firstname = user.firstname
                , username  = user.username
                )
            rec ['date'] = {}
            lolo_d, holidays = self.get_holidays (u)
            fmt = self.as_dict_entry
            d   = self.fdd
            while d <= self.ldd:
                dt = d.pretty (common.ymd)
                if gmtime (d.timestamp ()) [6] in [5, 6]:
                    r = dict (type = 'weekend')
                else:
                    r = (  self.get_holiday_entry
                               (d, holidays, lolo_d, fmt = fmt)
                        or self.get_absence_entry (user, d, fmt = fmt)
                        or self.get_leave_entry   (user, d, fmt = fmt)
                        )
                if r and r ['type'] in self.types:
                    rec ['date'][dt] = r
                d += common.day
            result.append (rec)
        retval = {}
        retval ['@total_size'] = len (result)
        retval ['collection'] = result

        rest_instance.client.setHeader ('X-Count-Total', str (len (result)))
        rest_instance.client.setHeader ("Allow", "OPTIONS, GET")

        return 200, retval
    # end def as_dict

    def format_leaves (self):
        """ HTML-Format of leave requests and holidays
            We first get leaves and absence records by user and date-range.
            We search for all starting in the range *and* ending in the
            range. In addition we search for all that start *before* the
            range and end *after* the range. In the next step we get all the
            public holidays in the range and index them by location.
        """
        db    = self.db

        ret = []
        ret.append ('<table class="timesheet">')
        for n, u in enumerate (self.users):
            user = db.user.getnode (u)
            if n % 20 == 0:
                ret.extend (self.header_line ())
            ret.append (' <tr>')
            ret.append ('  <td class="name">%s</td>' % user.lastname)
            ret.append ('  <td class="name">%s</td>' % user.firstname)
            ret.append ('  <td class="name">%s</td>' % user.username)
            lolo_d, holidays = self.get_holidays (u)
            d = self.fdd
            while d <= self.ldd:
                if gmtime (d.timestamp ()) [6] in [5, 6]:
                    ret.append ('  <td class="holiday"/>')
                else:
                    r = (  self.get_holiday_entry (d, holidays, lolo_d)
                        or self.get_absence_entry (user, d)
                        or self.get_leave_entry   (user, d)
                        )
                    if r:
                        ret.append (r)
                    else:
                        ret.append (self.formatlink (date = d, user = u))
                d += common.day
            ret.append (' </tr>')
        ret.extend (self.header_line ())
        ret.append ('<tr/><tr/><tr/><tr/>')
        ret.append ('</table>')
        return '\n'.join (ret)
    # end def format_leaves

    def get_holidays (self, user):
        lolo_d = {}
        dyn = user_dynamic.get_user_dynamic (self.db, user, self.now)
        if dyn and dyn.org_location:
            loc = self.db.org_location.get (dyn.org_location, 'location')
            olo = dyn.org_location
            holidays = {}
            for h in self.by_location.get (loc, []):
                key = h.date.pretty (common.ymd)
                holidays [key] = h
                lolo_d   [key] = self.db.location.getnode (loc)
            for h in self.by_olo.get (olo, []):
                key = h.date.pretty (common.ymd)
                holidays [key] = h
                lolo_d   [key] = self.db.org_location.getnode (olo)
        else:
            holidays = {}
        return lolo_d, holidays
    # end def get_holidays

    def _helpwin (self, url):
        return "javascript:abswin('%s', '600', '300')" % url
    # end def _helpwin

    def has_permission (self, perm='Create'):
        """ Permission to create/edit absence
        """
        return self.db.security.hasPermission \
            (perm, self.db.getuid (), 'absence')
    # end def has_permission

    def header_line (self):
        ret = []
        ret.append (' <tr>')
        ret.append ('  <th class="name">Last name</th>'
                    '  <th class="name">First Name</th>'
                    '  <th class="name">Username</th>'
                    )
        d = self.fdd
        while d <= self.ldd:
            ret.append ('  <th>%s</th>' % d.day)
            d += common.day
        ret.append (' </tr>')
        return ret
    # end def header_line

    def formatlink (self, typ = None, date = None, user = None, abs = None):
        code = cls = title = a = href = ''
        if self.has_permission ():
            href = 'href="%s"' % self._helpwin ('absence?%s')
        urlp = {'@template' : 'item'}
        if typ:
            urlp ['absence_type'] = typ.id
        if user:
            urlp ['user'] = user
        if date:
            urlp ['first_day'] = date
            urlp ['last_day']  = date
        if urlp and self.has_permission ():
            href = href % urlencode (urlp)
        if abs:
            if abs.absence_type:
                typ = self.db.absence_type.getnode (abs.absence_type)
            if self.has_permission ('Edit'):
                href  = 'href="%s"' % self._helpwin ('absence%s' % abs.id)
            urlp  = ''
        if typ:
            cls   = 'class="%s"' % typ.cssclass
            code  = typ.code
            title = 'title="%s"' % typ.description
            a     = '<a %s %s>%s</a>' % (title, href, code)
        if not a and href:
            a = '<a %s>&nbsp;</a>' % href
        return '  <td %s>%s</td>' % (cls, a)
    # end def formatlink

    def get_absence_entry (self, user, d, fmt = None):
        if fmt is None:
            fmt = self.formatlink
        if user.id not in self.abdict:
            return None
        for ab in self.abdict [user.id]:
            if ab.first_day <= d <= ab.last_day:
                return fmt (abs = ab)
        return None
    # end def get_absence_entry

    def format_holiday (self, d, lolo, holiday):
        pd = d.pretty (common.ymd)
        t  = "%s: %s" % (lolo.name, str (holiday.name))
        if holiday.description:
            t = '%s (%s)' % (t, holiday.description)
        ret = []
        ret.append ('  <td class="holiday">')
        ret.append ('   <a title="%s">&nbsp;</a>' % t)
        ret.append ('  </td>')
        return '\n'.join (ret)
    # end def format_holiday

    def get_holiday_entry (self, d, holidays, lolo_d, fmt = None):
        if fmt is None:
            fmt = self.format_holiday
        ret = []
        pd = d.pretty (common.ymd)
        if pd in holidays:
            lolo = lolo_d [pd]
            return fmt (d = d, lolo = lolo, holiday = holidays [pd])
    # end def get_holiday_entry

    def get_leave_entry (self, user, d, fmt = None):
        if fmt is None:
            fmt = self.formatlink
        if user.id not in self.lvdict:
            return None
        for lv in self.lvdict [user.id]:
            if lv.first_day <= d <= lv.last_day:
                wp  = self.db.time_wp.getnode (lv.time_wp)
                tp  = self.db.time_project.getnode (wp.project)
                uid = user.id
                if tp.is_vacation:
                    return fmt (self.abs_v, date = d, user = uid)
                else:
                    assert tp.is_special_leave or tp.max_hours == 0
                    return fmt (self.abs_a, date = d, user = uid)
    # end def get_leave_entry

    def month_link (self, s, e, symbol):
        if 'first_day' not in self.request.filter:
            self.request.filter.append ('first_day')
        url = self.request.indexargs_url \
            ('timesheet', dict (first_day = common.pretty_range (s, e)))
        return '<a href="%s">%s</a>' % (url, symbol)
    # end def month_link

    def month_links (self):
        """ Return month name with links to prev/next month
        """
        pms = self.fdd - Interval ('1m')
        nms = self.fdd + Interval ('1m')
        pme = common.end_of_month (pms)
        nme = common.end_of_month (nms)
        return '&nbsp'.join \
            (( self.month_link (pms, pme, '&lt;&lt;')
             , self.month
             , str (self.fdd.year)
             , self.month_link (nms, nme, '&gt;&gt;')
            ))
    # end def month_links

# end class Leave_Display


def avg_hours (db, user, dy):
    try:
        db = db._db
    except AttributeError:
        pass
    if not isinstance (dy, Date):
        return "00.00"
    return "%2.2f" % vacation.avg_hours_per_week_this_year (db, user, dy)
# end def avg_hours

def current_user_dynamic (context, user = None):
    db = context._db
    client = context._client
    now = Date ('.')
    uid = user or db.getuid ()
    dyn = user_dynamic.get_user_dynamic (db, uid, now)
    allowed = o_permission.dynamic_user_allowed_by_olo
    if dyn and allowed (db, db.getuid (), dyn.id):
        dyn = HTMLItem (client, 'user_dynamic', dyn.id)
        return dyn
    return None
# end def current_user_dynamic

def flexi_alliquot_html (db, user, date_in_year, ctype):
    if date_in_year is None:
        return 0.0
    if not isinstance (date_in_year, Date):
        try:
            date_in_year = Date (date_in_year)
        except ValueError:
            return 0.0
    return vacation.flexi_alliquot (db, user, date_in_year, ctype)
# end def flexi_alliquot_html

def flexi_remain_html (db, user, date_in_year, ctype):
    if date_in_year is None:
        return 0.0
    if not isinstance (date_in_year, Date):
        try:
            date_in_year = Date (date_in_year)
        except ValueError:
            return 0.0
    return vacation.flexi_remain (db, user, date_in_year, ctype)
# end def flexi_remain_html

def lookup_users (db, userstring):
    r = []
    for u in userstring.split (','):
        u = u.strip ()
        if u.isdigit ():
            r.append (u)
        try:
            uid = db.user.lookup (u)
            r.append (uid)
        except KeyError:
            pass
    return r
# end def lookup_users

def ct_for_year (db, user, now = None):
    ct = set ()
    if now is None:
        now = Date ('.')
    jan = Date ('%s-01-01' % now.year)
    dec = Date ('%s-12-31' % now.year)
    dyn = user_dynamic.first_user_dynamic (db, user, date = jan)
    while dyn:
        ct.add (dyn.contract_type)
        dyn = user_dynamic.next_user_dynamic (db, dyn)
        if not dyn or dyn.valid_from > dec:
            break
    ct = [db.contract_type.getnode (x) if x else None for x in ct]
    ct.sort (key = lambda x : (x and x.name or ''))
    return ct
# end def ct_for_year

class Rest_Request (RestfulInstance):

    @Routing.route ("/aux/timesheet", 'GET')
    @_data_decorator
    def timesheet (self, input, *args, **kw):
        supervisor = user = date = types = abstypes = None
        if 'supervisor' in input:
            supervisor = lookup_users (self.db, input ['supervisor'].value)
        if 'user' in input:
            user = lookup_users (self.db, input ['user'].value)
        if 'date' in input:
            date = input ['date'].value
        if 'type' in input:
            types = [x.strip () for x in input ['type'].value.split (',')]
        if 'absence_type' in input:
            abt = input ['absence_type']
            abstypes = [x.strip () for x in abt.value.split (',')]
        ld = Leave_Display \
            ( self.db, user, supervisor, date
            , types = types
            , lim_dt = False
            , all_user_fallback = False
            , absence_type = abstypes
            )
        path = '%s/' % (self.data_path)
        return ld.as_dict (self, path = path)
    # end def timesheet

# end class Rest_Request


def init (instance):
    reg = instance.registerUtil
    reg ('valid_wps',                    vacation.valid_wps)
    reg ('valid_leave_wps',              vacation.valid_leave_wps)
    reg ('valid_leave_projects',         vacation.valid_leave_projects)
    reg ('leave_days',                   leave_days)
    reg ('user_leave_submissions',       user_leave_submissions)
    reg ('approve_leave_submissions',    approve_leave_submissions)
    reg ('approve_leave_submissions_hr', approve_leave_submissions_hr)
    reg ('Leave_Buttons',                Leave_Buttons)
    reg ('remaining_until',              remaining_until)
    reg ('remaining_vacation',           remaining_vacation)
    reg ('consolidated_vacation',        consolidated_vacation)
    reg ('vacation_with_status',         vacation_with_status)
    reg ('flexitime_with_status',        flexitime_with_status)
    reg ('vacation_time_sum',            vacation.vacation_time_sum)
    reg ('get_vacation_correction',      vacation.get_vacation_correction)
    reg ('year',                         Interval ('1y'))
    reg ('day',                          common.day)
    reg ('eoy_vacation',                 eoy_vacation)
    reg ('Leave_Display',                Leave_Display)
    reg ('month_name',                   month_name)
    reg ('flexi_alliquot',               flexi_alliquot_html)
    reg ('flexi_remain',                 flexi_remain_html)
    reg ('avg_hours_per_week_this_year', avg_hours)
    reg ('get_current_ctype',            vacation.get_current_ctype)
    reg ('current_user_dynamic',         current_user_dynamic)
    reg ('ct_for_year',                  ct_for_year)
    action = instance.registerAction
    action ('new_leave',                 New_Leave_Action)
# end def init
