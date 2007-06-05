#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
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
#
#++
# Name
#    summary
#
# Purpose
#    Time-tracking summary reports
#

import csv
import cgi
import time
try :
    from cStringIO import StringIO
except ImportError :
    from StringIO  import StringIO

from roundup.date                   import Date, Interval
from roundup.cgi                    import templating
from roundup.cgi.TranslationService import get_translation
from roundup.cgi.actions            import Action
from rsclib.autosuper               import autosuper
from rsclib.PM_Value                import PM_Value

from common                         import pretty_range, week_from_date, ymd
from common                         import user_has_role, date_range
from common                         import weekno_year_from_day, end_of_period
from sum_common                     import time_wp_viewable
from sum_common                     import daily_record_viewable
from user_dynamic                   import update_tr_duration, get_user_dynamic
from user_dynamic                   import compute_balance, durations

day = Interval ('1d')

class Extended_Node (autosuper) :
    def __getattr__ (self, name) :
        """ Delegate everything to our node """
        if not name.startswith ('__') :
            result = getattr (self.node, name)
            setattr (self, name, result)
            return result
        raise AttributeError, name
    # end def __getattr__

    def __repr__ (self) :
        return "%s (%s)" % (self.__class__.__name__, repr (self.name))
    # end def __repr__

    __str__ = __repr__

# end class Extended_Node

class Extended_Daily_Record (Extended_Node) :
    """ Keeps information about the username *and* about the status of
        the daily_records: own records (is_own = True) are records wich
        may be unconditionally viewed by the user. For details about
        permissions, see lib/summary.py daily_record_viewable.
    """

    def __init__ (self, db, drid) :
        self.node     = db.daily_record.getnode (drid)
        self.username = db.user.get (self.user, 'username')
        self.name     = self.username
        self.is_own   = daily_record_viewable (db, db.getuid (), drid)
    # end def __init__

    def __cmp__ (self, other) :
        return \
            cmp (self.date, other.date) or cmp (self.username, other.username)
    # end def __cmp__
# end class Extended_Daily_Record

class Extended_WP (Extended_Node) :
    """ Keeps information about the username *and* about the status of
        the work package.
        
        For permissions, see time_wp_viewable in lib/summary.py
    """
    def __init__ (self, db, wpid) :
        self.node          = db.time_wp.getnode  (wpid)
        self.project_name  = db.time_project.get (self.project, 'name')
        self.is_own        = time_wp_viewable (db, db.getuid (), wpid)
        self.effort_perday = PM_Value (0, 1)
        if  (   self.time_start and self.time_end
            and self.planned_effort is not None
            ) :
            self.start = s = Date (str (self.time_start))
            self.end   = e = Date (str (self.time_end))
            days           = (e - s).get_tuple () [3]
            if days :
                self.effort_perday = PM_Value (self.planned_effort / days)
    # end def __init__

    def effort (self, date) :
        if not self.effort_perday.missing :
            if self.start <= date <= self.end :
                return self.effort_perday
            return PM_Value (0)
        return self.effort_perday
    # end def effort

    def __cmp__ (self, other) :
        return \
            (  cmp (self.project_name, other.project_name)
            or cmp (self.name,         other.name)
            )
    # end def __cmp__
# end class Extended_WP

class Extended_Time_Record (Extended_Node) :
    """ Keeps information about the username *and* about the status of
        the time record: own records (is_own = True) are records wich
        may be unconditionally viewed by the user. This is the case if
        the user owns the wp or owns the daily_record of the time
        record.
    """
    def __init__ (self, db, trid, dr, wp) :
        self.node         = db.time_record.getnode  (trid)
        self.dr           = dr [self.node.daily_record]
        self.wp           = wp [self.node.wp]
        self.is_own       = self.dr.is_own or self.wp.is_own
    # end def __init__

    def __getattr__ (self, name) :
        """ Delegate everything to first the daily_record, then the wp,
            then our node.
        """
        if not name.startswith ('__') :
            for x in self.dr, self.wp :
                try :
                    result = getattr (x, name)
                    setattr (self, name, result)
                    return result
                except AttributeError :
                    return self.__super.__getattr__ (name)
        raise AttributeError, name
    # end def __getattr__

    def __cmp__ (self, other) :
        return (cmp (self.dr, other.dr) or cmp (self.wp, other.wp))
    # end def __cmp__
# end class Extended_Time_Record

class Container (autosuper) :
    def __init__ (self, * args, ** kw) :
        self.sums  = {}
        self.plans = {}
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def add_sum (self, other_container, tr) :
        self.add_user_sum \
            (other_container, tr.username, tr.tr_duration or tr.duration)
    # end def add_sum

    def add_user_sum (self, other_container, username, sum) :
        for key in other_container, (other_container, username) :
            if key not in self.sums :
                self.sums [key] = PM_Value (0)
            self.sums [key] += sum
    # end def add_user_sum

    def add_plan (self, other_container, duration) :
        if other_container not in self.plans :
            self.plans [other_container] = PM_Value (0)
        self.plans [other_container] += PM_Value (duration, not duration)
    # end def add_plan

    def get_sum (self, other_container, username = None, default = None) :
        key = other_container
        if username :
            key = (other_container, username)
        if key in self.sums :
            return self.sums [key]
        return default
    # end def get_sum

    def get_plan (self, other_container, default = None) :
        if other_container in self.plans :
            return self.plans [other_container]
        return default
    # end def get_plan

    def as_html (self) :
        return cgi.escape (str (self))
    # end def as_html
# end class Container

class Time_Container (Container) :
    """ Container for time-ranges: has a start and end date and a hash
        of WP_Container to sum objects.
    """
    def __init__ (self, start, end) :
        self.__super.__init__ ()
        self.start    = start
        self.end      = end
        self.sort_end = end
        self.dict     = {}
    # end def __init__

    def __repr__ (self) :
        return "%s (%s, %s)" % (self.__class__.__name__, self.start, self.end)
    # end def __repr__

    __str__ = __repr__

    def __hash__ (self) :
        return hash (repr (self))
    # end def __hash__

    def __setitem__ (self, name, value) :
        self.dict [name] = value
    # end def __setitem__

    def __getitem__ (self, name) :
        return self.dict [name]
    # end def __getitem__

    def __delitem__ (self, name) :
        del self.dict [name]
    # end def __delitem__

    def __iter__ (self) :
        return self.dict.iterkeys ()
    # end def __iter__
    iterkeys = __iter__

    def iteritems (self) :
        return self.dict.iteritems ()
    # end def iteritems

    def __contains__ (self, name) :
        return name in self.dict
    # end def __contains__

# end class Time_Container

class Day_Container (Time_Container) :
    def __init__ (self, day) :
        date = Date (day.pretty (ymd))
        self.__super.__init__ (date, date + Interval ('1d'))
    # end def __init__

    def __str__ (self) :
        return self.start.pretty (ymd)
    # end def __str__
# end class Day_Container

class Week_Container (Time_Container) :
    def __init__ (self, day) :
        start, end = week_from_date  (day)
        self.__super.__init__ (start, end + Interval ('1d'))
    # end def __init__

    def __str__ (self) :
        return "WW %s/%s" % weekno_year_from_day (self.start)
    # end def __str__
# end class Week_Container

class Month_Container (Time_Container) :
    def __init__ (self, day) :
        year   = day.year
        month  = day.month
        nmonth = day.month + 1
        nyear  = year
        if nmonth > 12 :
            nmonth = 1
            nyear = year + 1
        fmt = '%4s-%s-01'
        self.__super.__init__ \
            (Date (fmt % (year, month)), Date (fmt % (nyear, nmonth)))
    # end def __init__

    def __str__ (self) :
        return self.start.pretty ("%B %Y")
    # end def __str__
# end class Month_Container

class Range_Container (Time_Container) :
    """ Contains the whole selected time-range """
    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.sort_end = self.end + Interval ('1m')
    # end def __init__

    def __str__ (self) :
        return "%s;%s" % (self.start.pretty (ymd), self.end.pretty (ymd))
    # end def __str__
# end class Range_Container

time_container_classes = \
    { 'day'   : Day_Container
    , 'week'  : Week_Container
    , 'month' : Month_Container
    , 'range' : Range_Container
    }

class Comparable_Container (Container, dict) :
    sortkey = 50
    def __str__ (self) :
        return self.name
    # end def __str__

    def __cmp__ (self, other) :
        return \
            (  cmp (self.sortkey, other.sortkey) 
            or cmp (_ (self.classname), _ (other.classname))
            or cmp (self.name, other.name)
            )
    # end def __cmp__

# end class Comparable_Container

class Sum_Container (Comparable_Container, dict) :
    sortkey = 100
    def __init__ (self, name = "Sum", visible = True, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.name      = name
        self.visible   = visible
        self.classname = ''
    # end def __init__

    def __repr__ (self) :
        classname = self.__class__.__name__
        return "%s (%s, %s, %s)" % \
            (classname, self.name, self.visible, self.__super.__repr__ ())
    # end def __repr__

    def __hash__ (self) :
        return hash ((self.__class__, self.name))
    # end def __hash__
# end class Sum_Container

class WP_Container (Comparable_Container, dict) :
    def __init__ \
        (self, klass, id, visible = True, verbname = '', * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.klass     = klass
        self.classname = klass.classname
        self.id        = id
        self.visible   = visible
        self.name      = klass.get (id, 'name')
        self.verbname  = verbname

        if klass.classname == 'time_wp' :
            self.sortkey = 30
            p = klass.db.time_project.get (klass.get (id, 'project'), 'name')
            self.name  = '/'.join ((p, self.name))
    # end def __init__
    
    def __repr__ (self) :
        name = self.__class__.__name__
        return "%s (%s, %s, %s)" % \
            (name, self.classname, self.id, self.__super.__repr__ ())
    # end def __repr__

    def __str__ (self) :
        return "%s %s %s" % (_ (self.classname), self.name, self.verbname)
    # end def __str__

    def as_html (self) :
        return "%s %s %s" % \
            ( cgi.escape (_ (self.classname)).replace (' ', '&nbsp;')
            , cgi.escape (self.name).replace          (' ', '&nbsp;')
            , cgi.escape (self.verbname).replace      (' ', '&nbsp;')
            )

    def __hash__ (self) :
        return hash ((self.__class__, self.classname, self.id))
    # end def __hash__
# end class WP_Container

class _Report (autosuper) :
    def html_item (self, item) :
        if not item and not isinstance (item, dict) and not item == 0 :
            return "   <td/>"
        if isinstance (item, PM_Value) :
            if item.missing and not item :
                return ('  <td class="missing"/>')
            return \
                ('  <td %sstyle="text-align:right;">%2.02f</td>'
                % (['class="missing" ', ''][not item.missing], item)
                )
        if isinstance (item, type (0.0)) or isinstance (item, type (0)) :
            return ('  <td style="text-align:right;">%2.02f</td>' % item)
        if isinstance (item, str) :
            return ('  <td>%s</td>' % item)
        return ('  <td>%s</td>' % item.as_html ())
    # end def html_item

    def html_header_item (self, item) :
        return ('  <th>%s</th>' % str (item))
    # end def html_header_item

    def html_line (self, items) :
        items.insert (0, " <tr>")
        items.append (" </tr>")
        self.html_output.extend (items)
    # end def html_line

    def csv_item (self, item) :
        if not item and not isinstance (item, dict) and not item == 0 :
            return ''
        if isinstance (item, PM_Value) :
            if item.missing and not item :
                return "-"
            return '%2.02f' % item
        if isinstance (item, type (0.0)) :
            return '%2.02f' % item
        return str (item)
    # end def csv_item

    def csv_line (self, items) :
        self.csvwriter.writerow (items)
    # end def csv_line

    def as_html (self) :
        s = self.html_output = ['']
        s.append ('<table class="list" border="1">')
        self.html_line (self.header_line (self.html_header_item))
        self._output   (self.html_line, self.html_item)
        s.append ("</table>")
        return '\n'.join (s)
    # end def as_html

    def as_csv (self) :
        io             = StringIO ()
        self.csvwriter = csv.writer (io, dialect = 'excel', delimiter = ',')
        self.csv_line (self.header_line (self.csv_item))
        self._output  (self.csv_line, self.csv_item)
        return io.getvalue ()
    # end def as_csv
# end class _Report

class Summary_Report (_Report) :
    """ TODO:
        - special colors for 
          - daily record not yet accepted
          - no daily record found -- involves checking dynamic user data
        FIXME: Check where we need naive dates...
    """
    def __init__ (self, db, request, utils, is_csv = False) :
        try :
            db = db._db
        except AttributeError :
            pass
        filterspec      = request.filterspec
        sort_by         = request.sort
        group_by        = request.group
        columns         = request.columns
        now             = Date ('.')
        assert (request.classname == 'summary_report')
        wp_containers   = []
        if not columns :
            columns     = db.summary_report.getprops ().keys ()
        self.columns    = dict ((c, True) for c in columns)
        status          = filterspec.get \
            ('status', db.daily_record_status.getnodeids ())
        timestamp       = time.time ()
        show_empty      = filterspec.get ('show_empty',     'no')
        show_all_users  = filterspec.get ('show_all_users', 'no')
        show_missing    = filterspec.get ('show_missing',   'no')
        self.show_empty = show_empty == 'yes'
        show_all_users  = self.show_all_users = show_all_users == 'yes'
        show_missing    = show_missing == 'yes' and not is_csv
        travel_act      = db.time_activity.filter (None, {'travel' : True})
        travel_act      = dict ((a, 1) for a in travel_act)
        self.show_plan  = 'planned_effort' in self.columns

        #print "time", timestamp
        #print filterspec
        #print self.columns, self.show_plan
        start, end  = date_range (db, filterspec)
        users       = filterspec.get ('user', [])
        sv          = dict ((i, 1) for i in filterspec.get ('supervisor', []))
        svu         = []
        if sv :
            svu     = db.user.find (supervisor = sv)
        users       = dict ((u, 1) for u in users + svu).keys ()
        olo_or_dept = False
        drecs       = {}
        org_dep_usr = {}
        for cl in 'department', 'org_location' :
            spec = dict ((s, 1) for s in filterspec.get (cl, []))
            if spec :
                olo_or_dept = True
                udrs        = []
                for i in db.user_dynamic.find (** {cl : spec}) :
                    ud = db.user_dynamic.getnode (i)
                    if  (   ud.valid_from <= end
                        and (not ud.valid_to or ud.valid_to > start)
                        ) :
                        udrs.append (ud)
                        org_dep_usr [ud.user] = 1
                for ud in udrs :
                    udstart = max (ud.valid_from, start)
                    if ud.valid_to :
                        udend = min (ud.valid_to - Interval ('1d'), end)
                    else :
                        udend = end
                    assert (udstart <= udend)
                    drs = db.daily_record.filter \
                        ( None, dict 
                            ( user   = ud.user
                            , date   = pretty_range (udstart, udend)
                            , status = status
                            )
                        )
                    edr = Extended_Daily_Record
                    drs = [edr (db, d) for d in drs]
                    drecs.update (dict ((d.id, d) for d in drs))

        #print "after departments:", time.time () - timestamp
        if not users and not olo_or_dept :
            users   = db.user.getnodeids () # also invalid users!
        #print users, start, end, status
        dr          = []
        if users :
            dr = db.daily_record.filter \
                ( None, dict 
                    ( user   = users
                    , date   = pretty_range (start, end)
                    , status = status
                    )
                )
        #print "n_dr:", len (dr), time.time () - timestamp
        dr          = dict \
            ((d, Extended_Daily_Record (db, d)) for d in dr)
        #print "after users:", time.time () - timestamp
        dr.update (drecs)
        #print "after dr.update:", time.time () - timestamp
        self.dr_by_user_date = dict \
            (((str (v.username), v.date.pretty (ymd)), v)
             for v in dr.itervalues ()
            )
        #print "after dr_dat_usr:", time.time () - timestamp

        trvl_tr     = {}
        for d in dr.itervalues () :
            update_tr_duration (db, d)
        db.commit ()
        #print "trv daily_recs", len (trvl_dr), time.time () - timestamp

        wp          = dict ((w, 1) for w in filterspec.get ('time_wp', []))
        #print "native wp", len (wp), time.time () - timestamp

        wpgs        = filterspec.get ('time_wp_group',     [])
        for wpg in wpgs :
            wp_containers.append \
                ( WP_Container
                    ( db.time_wp_group, wpg
                    , 'time_wp_group' in self.columns
                    , ''
                    , [(w, 1) for w in db.time_wp_group.get (wpg, 'wps')]
                    )
                )
            wp.update (wp_containers [-1])
        #print "wpgs", len (wp), time.time () - timestamp
        projects    = filterspec.get ('time_project',      [])
        #print projects
        for p in projects :
            #print p, db.time_wp.find (project = p)
            wp_containers.append \
                ( WP_Container
                    ( db.time_project, p
                    , 'time_project' in self.columns
                    , ''
                    , [(w, 1) for w in db.time_wp.find (project = p)]
                    )
                )
            #print wp_containers [-1]
            wp.update (wp_containers [-1])
        #print "projects", len (wp), time.time () - timestamp
        ccs         = filterspec.get ('cost_center',       [])
        for cc in ccs :
            wp_containers.append \
                ( WP_Container
                    ( db.cost_center, cc
                    , 'cost_center' in self.columns
                    , ''
                    , [(w, 1) for w in db.time_wp.find (cost_center = cc)]
                    )
                )
            wp.update (wp_containers [-1])
        #print "ccs", len (wp), time.time () - timestamp
        ccgs        = filterspec.get ('cost_center_group', [])
        for ccg in ccgs :
            ccs     = db.cost_center.find (cost_center_group = ccg)
            ccs     = dict ((c, 1) for c in ccs)
            wp_containers.append \
                ( WP_Container 
                    ( db.cost_center_group, ccg
                    , 'cost_center_group' in self.columns
                    )
                )
            for cc in ccs :
                wps = dict ((w,1) for w in db.time_wp.find (cost_center = cc))
                wp_containers [-1].update (wps)
            wp.update (wp_containers [-1])
        #print "ccgs", len (wp), time.time () - timestamp
        if  (    not wp
            and 'time_wp'           not in filterspec
            and 'time_wp_group'     not in filterspec
            and 'time_project'      not in filterspec
            and 'cost_center'       not in filterspec
            and 'cost_center_group' not in filterspec
            ) :
            wp = dict ((w, 1) for w in db.time_wp.getnodeids ())
        #print "wp-default", len (wp), time.time () - timestamp
        #print "n_wp:", len (wp)
        work_pkg    = dict ((w, Extended_WP (db, w)) for w in wp.iterkeys ())
        #print "ext wp", time.time () - timestamp
        time_recs   = []
        # 276 sec: (4.6 min) (for Decos: ~ 250 sec)
        if dr and wp :
            time_recs = []
            for d in dr.itervalues () :
                for t in d.time_record :
                    if db.time_record.get (t, 'wp') in work_pkg :
                        tr = Extended_Time_Record (db, t, dr, work_pkg)
                        time_recs.append (tr)
        #print "ext time_recs", len (time_recs), time.time () - timestamp
        time_recs   = [t for t in time_recs if t.is_own]
        #print "own time_recs", len (time_recs), time.time () - timestamp
        time_recs.sort ()
        #print "srt time_recs", len (time_recs), time.time () - timestamp
        if self.show_empty :
            usrs         = users + org_dep_usr.keys ()
            uids_by_name = dict ((db.user.get (u, 'username'), u) for u in usrs)
            # filter out users without a dyn user record in our date range
            # Except for those who have booked in the range
            if not self.show_all_users :
                users = {}
                for u, uid in uids_by_name.iteritems () :
                    d   = start
                    while d <= end :
                        if get_user_dynamic (db, uid, d) :
                            users [u] = uid
                            break
                        d = d + Interval ('1d')
                for tr in time_recs :
                    u = tr.username
                    users [u] = uids_by_name [u]
                uids_by_name = users
            usernames    = uids_by_name.keys ()
        else :
            usernames    = dict ((tr.username, 1) for tr in time_recs).keys ()
            uids_by_name = dict ((u, db.user.lookup (u)) for u in usernames)
        #print "         usernames", time.time () - timestamp

        #print "filtered usernames", time.time () - timestamp
        usernames.sort ()
        #print "sorted   usernames", time.time () - timestamp
        #print usernames
        
        # append only wps where somebody actually booked on
        wps         = dict ((tr.wp.id, 1) for tr in time_recs)
        for w in wps.iterkeys () :
            wp_containers.append \
                ( WP_Container 
                    ( db.time_wp, w
                    , 'time_wp' in self.columns
                    , [''
                      , ( '%s %s'
                        % ( _ ('cost_center')
                          , db.cost_center.get
                            (db.time_wp.get (w, 'cost_center'), 'name')
                          )
                        )
                      ]['cost_center' in self.columns]
                    , ((w, 1),)
                    )
                )
        #print "filtered wps", time.time () - timestamp
        wp_containers.append \
            (Sum_Container (_ ('Sum'), 'summary' in self.columns, wps))

        # Build time containers
        rep_types  = filterspec.get \
            ('summary_type', [db.summary_type.lookup ('range')])
        rep_types  = [db.summary_type.get (i, 'name') for i in rep_types]
        time_containers = dict ((t, []) for t in rep_types)
        d = start
        while d <= end :
            for t, cont in time_containers.iteritems () :
                if not cont or cont [-1].end <= d :
                    try :
                        cont.append (time_container_classes [t] (d))
                    except TypeError :
                        cont.append (time_container_classes [t] (start, end))
            d = d + Interval ('1d')
        #print "time containers", time.time () - timestamp
        wp_containers = [w for w in wp_containers if w.visible]
        wp_containers.sort ()
        #print "sorted wp containers", time.time () - timestamp
        # invert wp_containers
        containers_by_wp = {}
        for wc in wp_containers :
            for w in wc :
                if w in containers_by_wp :
                    containers_by_wp [w].append (wc)
                else :
                    containers_by_wp [w]      = [wc]
        #print "inverted wp containers", time.time () - timestamp
        tc_pointers = dict ((i, 0) for i in time_containers.iterkeys ())
        #print "after tc_pointers", time.time () - timestamp

        d        = start
        tidx     = 0
        invalid  = PM_Value (0, 1)
        # wp may not be viewable due to permissions
        valid_wp = \
            [w for w in work_pkg.itervalues () if w.id in containers_by_wp]
        while d <= end :
            if show_missing :
                no_daily_record = \
                    [u for u in usernames
                     if (   (u, d.pretty (ymd)) not in self.dr_by_user_date
                        and (  self.show_all_users
                            or get_user_dynamic (db, uids_by_name [u], d)
                            )
                        )
                    ]
                #print "user", len (no_daily_record), time.time () - timestamp
            for tcp in tc_pointers.iterkeys () :
                while (d >= time_containers [tcp][tc_pointers [tcp]].sort_end) :
                    tc_pointers [tcp] += 1
                tc = time_containers [tcp][tc_pointers [tcp]]
                if self.show_plan or show_missing :
                    for w in valid_wp :
                        for wc in containers_by_wp [w.id] :
                            if self.show_plan :
                                wc.add_plan (tc, w.effort (d))
                                tc.add_plan (wc, w.effort (d))
                            if show_missing :
                                for u in no_daily_record :
                                    wc.add_user_sum (tc, u, invalid)
                                    tc.add_user_sum (wc, u, invalid)
                #print "plan", time.time () - timestamp
            while tidx < len (time_recs) and time_recs [tidx].date == d :
                t  = time_recs [tidx]
                for tcp in tc_pointers.iterkeys () :
                    tc = time_containers [tcp][tc_pointers [tcp]]
                    for wpc in containers_by_wp [t.wp.id] :
                        tc. add_sum (wpc, t)
                        wpc.add_sum (tc,  t)
                tidx += 1
            d = d + Interval ('1d')
            #print "1d", time.time () - timestamp
        #print "SUMs built", time.time () - timestamp
        self.wps             = wps
        self.usernames       = usernames
        self.start           = start
        self.end             = end
        self.time_containers = time_containers
        self.wp_containers   = wp_containers
    # end def __init__

    def header_line (self, formatter) :
        line = []
        line.append (formatter (_ ('Container')))
        line.append (formatter (_ ('time')))
        if 'user' in self.columns :
            for u in self.usernames :
                line.append (formatter (u))
        line.append (formatter (_ ('Sum')))
        if self.show_plan :
            for i in 'planned_effort', '%', 'remaining' :
                line.append (formatter (_ (i)))
        return line
    # end def header_line

    def _output_line (self, wpc, type, idx, formatter) :
        line = []
        tc   = self.time_containers [type][idx]
        line.append (formatter (wpc))
        line.append (formatter (tc))
        if 'user' in self.columns :
            for u in self.usernames :
                line.append (formatter (tc.get_sum (wpc, u, '')))
        sum = tc.get_sum (wpc, default = PM_Value (0.0))
        line.append (formatter (sum))
        if self.show_plan :
            plan = tc.get_plan (wpc)
            line.append (formatter (plan))
            if plan :
                line.append (formatter (sum * 100. / plan))
                line.append (formatter (plan - sum))
            else :
                missing = plan is None or plan.missing
                line.append (formatter (PM_Value (0, missing)))
                line.append (formatter (PM_Value (0, missing)))
        return line
    # end def _output_line

    def _output (self, line_formatter, item_formatter) :
        start = self.start + Interval ('1d')
        end   = max \
            ([self.time_containers [i][-1].sort_end
              for i in self.time_containers.keys ()
            ])
        for wpc in self.wp_containers :
            tc_pointers = dict \
                ([(i, 0) for i in self.time_containers.iterkeys ()])
            d = start
            containertypes = 'day', 'week', 'month', 'range' # order matters.
            while d <= end :
                for tcp in [i for i in containertypes if i in tc_pointers] :
                    try :
                        tc = self.time_containers [tcp][tc_pointers [tcp]]
                    except IndexError :
                        continue
                    if d >= tc.sort_end :
                        if  (   wpc.visible
                            and (self.show_empty or tc.get_sum (wpc))
                            ) :
                            line_formatter \
                                ( self._output_line
                                  (wpc, tcp, tc_pointers [tcp], item_formatter)
                                )
                        tc_pointers [tcp] += 1
                d = d + Interval ('1d')
    # end def _output
# end class Summary_Report

class Overtime_Corrections :
    def __init__ (self) :
        self.items = []
    # end def __init__

    def append (self, item) :
        self.items.append (item)
    # end def append

    def as_html (self) :
        return ' + '.join (i.as_html () for i in self.items)
    # end def as_html

    def __repr__ (self) :
        return ' + '.join (str (i) for i in self.items)
    # end def __repr__
# end class Overtime_Corrections

class Staff_Report (_Report) :
    fields = \
        ( ""'balance_week_start'
        , ""'actual_open'
        , ""'actual_submitted'
        , ""'actual_accepted'
        , ""'actual_all'
        , ""'required'
        , ""'supp_weekly_hours'
        , ""'overtime_correction'
        , ""'balance_week_end'
        )
    period_fields = \
        ( ""'overtime_period'
        , ""'balance_period_start'
        , ""'additional_hours'
        , ""'supp_per_period'
        , ""'balance_period_end'
        )

    def __init__ (self, db, request, utils, is_csv = False) :
        self.htmldb  = db
        try :
            db = db._db
        except AttributeError :
            pass
        self.db      = db
        self.uid     = db.getuid ()
        stati        = (db.daily_record_status.getnode (i)
                        for i in db.daily_record_status.getnodeids ()
                       )
        self.stati   = dict ((i.id, i.name) for i in stati)
        self.request = request
        self.utils   = utils
        filterspec   = request.filterspec
        status       = filterspec.get \
            ('status', db.daily_record_status.getnodeids ())
        users        = filterspec.get ('user', [])
        sv           = dict ((i, 1) for i in filterspec.get ('supervisor', []))
        svu          = []
        if sv :
            svu      = db.user.find (supervisor = sv)
        users        = dict ((u, 1) for u in users + svu)
        start, end   = date_range (db, filterspec)
        self.start   = start
        self.end     = end
        found_users  = bool (users)
        st           = filterspec.get \
            ('summary_type', [db.summary_type.lookup ('range')])
        sum_types    = dict ((db.summary_type.get (i, 'name'), 1) for i in st)
        for cl in 'department', 'org_location' :
            spec = filterspec.get (cl, [])
            if spec :
                found_users = True
                for i in db.user_dynamic.filter \
                    ( None
                    , {cl : spec, 'valid_from' : end.pretty (';%Y-%m-%d')}
                    ) :
                    ud = db.user_dynamic.getnode (i)
                    if  (   ud.valid_from <= end
                        and (not ud.valid_to or ud.valid_to > end)
                        ) :
                        users [ud.user] = 1
        if not found_users :
            users = dict ((i, 1) for i in db.user.getnodeids ())
        all_in = filterspec.get ('all_in')
        if all_in is not None :
            all_in = all_in == 'yes'
        for u in users.keys () :
            dyn = get_user_dynamic (db, u, end)
            if  (  not dyn
                or all_in is not None and all_in != bool (dyn.all_in)
                or not self.permission_ok (u)
                ) :
                del users [u]
        self.users = sorted \
            ( users.keys ()
            , key = lambda x : db.user.get (x, 'username')
            )
        self.values      = values = {}
        self.need_period = False
        for u in self.users :
            dyn        = get_user_dynamic (db, u, end)
            values [u] = []
            for period in 'week', 'month', 'range' :
                if period not in sum_types :
                    continue
                if period == 'range' :
                    container = time_container_classes [period] (start, end)
                    values [u].append   (container)
                    self.fill_container (container, u, dyn, start, end)
                else :
                    date = start
                    while date < end :
                        eop       = end_of_period (date, period)
                        container = time_container_classes [period] (date)
                        values [u].append   (container)
                        self.fill_container (container, u, dyn, date, eop)
                        date      = eop + day
        db.commit () # commit cached daily_record values
    # end def __init__

    def fill_container (self, container, user, dyn, start, end) :
        db = self.db
        u  = user
        container ['balance_week_start'] = compute_balance \
            (db, u, start - day, 'week', True)
        container ['balance_week_end']   = compute_balance \
            (db, u, end,         'week', True)
        container ['overtime_period'] = ''
        if dyn.overtime_period :
            period = db.overtime_period.get (dyn.overtime_period, 'name')
            container ['overtime_period'] = period
            self.need_period = True
            container ['balance_period_start'] = compute_balance \
                (db, u, start - day, period, True)
            container ['balance_period_end']   = compute_balance \
                (db, u, end,         period, True)
        else :
            container ['balance_period_start'] = ''
            container ['balance_period_end']   = ''
        ov = db.overtime_correction.filter \
            (None, dict (user = u, date = pretty_range (start, end)))
        try :
            ovs = Overtime_Corrections ()
            for x in ov :
                item  = self.htmldb.overtime_correction.getItem (x)
                value = item.value
                ep    = self.utils.ExtProperty
                ovs.append \
                    ( ep
                        ( self.utils, value
                        , item         = item
                        , is_labelprop = True
                        )
                    )
            container ['overtime_correction'] = ovs
        except AttributeError :
            container ['overtime_correction'] = ' + '.join \
                (str (db.overtime_correction.get (i, 'value')) for i in ov)
        d = start
        container ['supp_per_period']        = dyn.supp_per_period
        container ['actual_all']             = 0
        container ['actual_open']            = 0
        container ['actual_submitted']       = 0
        container ['actual_accepted']        = 0
        container ['required']               = 0
        container ['supp_weekly_hours']      = 0
        container ['additional_hours']       = 0
        while d <= end :
            act, req, sup, add, do_week, do_perd, st, ovr, op = \
                durations (db, u, d)
            assert (not act or st)
            container ['actual_all'] += act
            if st :
                f = 'actual_' + self.stati [st]
                container [f] += act
            container ['required']          += req * (do_week or do_perd)
            container ['additional_hours']  += add * do_perd
            container ['supp_weekly_hours'] += sup * do_week
            d = d + day
    # end def fill_container

    def permission_ok (self, user) :
        if user == self.uid :
            return True
        if user_has_role (self.db, self.uid, 'HR') :
            return True
        if self.db.user.get (user, 'supervisor') == self.uid :
            return True
        return False
    # end def permission_ok

    def header_line (self, formatter) :
        line = []
        line.append (formatter (_ ('user')))
        line.append (formatter (_ ('time')))
        for f in self.fields :
            line.append (formatter (_ (f)))
        if self.need_period :
            for f in self.period_fields :
                line.append (formatter (_ (f)))
        return line
    # end def header_line

    def _output (self, line_formatter, item_formatter) :
        for u in self.users :
            try :
                item  = self.htmldb.user.getItem (u)
                uname = item.username
                user  = self.utils.ExtProperty (self.utils, uname, item = item)
            except AttributeError :
                user  = self.db.user.get (u, 'username')
            for container in self.values [u] :
                line  = []
                line.append (item_formatter (user))
                line.append (item_formatter (container))
                for f in self.fields :
                    line.append (item_formatter (container [f]))
                if self.need_period :
                    for f in self.period_fields :
                        line.append (item_formatter (container [f]))
                line_formatter (line)
    # end def _output

# end class Staff_Report

class CSV_Report (Action, autosuper) :
    def handle (self) :
        request                   = templating.HTMLRequest     (self.client)
        self.utils                = templating.TemplatingUtils (self.client)
        h                         = self.client.additional_headers
        h ['Content-Type']        = 'text/csv'
        h ['Content-Disposition'] = 'inline; filename=summary.csv'
        self.client.header    ()
        if self.client.env ['REQUEST_METHOD'] == 'HEAD' :
            # all done, return a dummy string
            return 'dummy'
        report = self.report_class (self.db, request, self.utils, is_csv = True)
        return report.as_csv ()
    # end def handle
# end class CSV_Report

class CSV_Summary_Report (CSV_Report) :
    report_class = Summary_Report
# end class CSV_Summary_Report

class CSV_Staff_Report (CSV_Report) :
    report_class = Staff_Report
# end class CSV_Staff_Report

def init (instance) :
    global _
    _   = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.config.TRACKER_HOME).gettext
    util   = instance.registerUtil
    util   ('Summary_Report',     Summary_Report)
    util   ('Staff_Report',       Staff_Report)
    action = instance.registerAction
    action ('csv_summary_report', CSV_Summary_Report)
    action ('csv_staff_report',   CSV_Staff_Report)
# end def init
