#! /usr/bin/python
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
#    interfaces
#
# Purpose
#    Define utlilities used by roundup
#
#--
#

import calendar
import time
import os
import re
import locale
from roundup.cgi.TranslationService import get_translation
from roundup.cgi.templating         import HTMLClass
from roundup.date                   import Date, Interval
from roundup.hyperdb                import Database as hyperdb_database
from copy                           import copy
from xml.sax.saxutils               import escape

import common
import freeze
import user_dynamic
import vacation

def localecollate (s) :
    old = locale.getlocale (locale.LC_COLLATE)
    locale.setlocale (locale.LC_COLLATE, '')
    s = locale.strxfrm (str (s))
    locale.setlocale (locale.LC_COLLATE, old)
    return s
# end def localecollate

def correct_midnight_date_string (db) :
    """returns GMT's "today.midnight" in localtime format.
    suitable for passing in to forms that need this date.
    """
    d   = Date ('00:00', -db._db.getUserTimezone ())
    return d.pretty ('%Y-%m-%d.%H:%M:%S')
# end def correct_midnight_date_string

def rough_date_diff (left, right, format = "%Y-%m-%d") :
    """returns the interval between the two dates left - right.
    format is used for the granularity when interpreting the two values.

    left and right need to be Date values.
    format needs to be a Date parseable format.
    """
    l_d = Date (left.pretty (format))
    r_d = Date (right.pretty (format))
    return l_d - r_d
# end def rough_date_diff

def start_timer (utils) :
    """starts an internal timer for profiling the templates
    """
    utils.timer = time.time ()
    return utils.timer
# end def start_timer

def time_stamp (utils) :
    """return a timestamp in seconds elapsed from last `start_timer` call
    """
    return time.time () - utils.timer
# end def time_stamp

def date_help \
    ( request
    , item
    , width    = 300
    , height   = 200
    , label    = ''"(cal)"
    , form     = "itemSynopsis"
    ) :
    """dump out the link to a calendar pop-up window

    item: HTMLProperty e.g.: context.deadline
    """
    if item.isset () :
        # Hack: rup seems to have a bug where sometimes item._value is a
        # string and not a Date class... in this case __str__ fails.
        # Looks like this happens when an error is raised.
        x = item
        if type ("") == type (item._value) : x = item._value
        date = "&date=%s" % x
    else :
        date = ""
    if item.is_edit_ok () :
        return ( """<a class="classhelp" """
                 """href="javascript:help_window """
               """('%s?@template=calendar"""
                 """&property=%s"""
                 """&form=%s%s', %d, %d)">%s</a>"""
                 % ( request.classname
                   , item._name
                   , form
                   , date
                   , width
                   , height
                   , label
                   )
               )
    return ''
# end def date_help

def html_calendar (request) :
    """returns a html calendar.

    `request`  the roundup.request object
               - @template : name of the template
               - form      : name of the form to store back the date
               - property  : name of the property of the form to store
                             back the date
               - date      : current date
               - display   : when browsing, specifies year and month

    html will simply be a table.
    """
    #print request.form
    date_str  = request.form.getfirst ("date", ".")
    display   = request.form.getfirst ("display", date_str)
    template  = request.form.getfirst ("@template", "calendar")
    form      = request.form.getfirst ("form")
    property  = request.form.getfirst ("property")
    curr_date = Date (date_str) # to highlight
    display   = Date (display)  # to show
    year      = display.year
    month     = display.month
    day       = display.day

    # for navigation
    date_prev_month = display + Interval ("-1m")
    date_next_month = display + Interval ("+1m")
    date_prev_year  = display + Interval ("-1y")
    date_next_year  = display + Interval ("+1y")

    res      = []
    res.append ("""<table class="calendar">""")

    base_link = "%s?@template=%s&property=%s&form=%s&date=%s" % \
                (request.classname, template, property, form, curr_date)

    # navigation
    # month
    res.append (""" <tr>""")
    res.append ("""  <td>""")
    res.append ("""   <table width="100%" class="calendar_nav">""")
    res.append ("""    <tr>""")
    link = base_link + "&display=%s" % date_prev_month
    res.append ("""     <td><a href="%s">&lt;</a></td>""" % link)
    res.append ("""     <td>%s</td>""" % calendar.month_name [month])
    link = base_link + "&display=%s" % date_next_month
    res.append ("""     <td><a href="%s">&gt;</a></td>""" % link)
    # spacer
    res.append ("""     <td width="100%"></td>""")
    # year
    link = base_link + "&display=%s" % date_prev_year
    res.append ("""     <td><a href="%s">&lt;</a></td>""" % link)
    res.append ("""     <td>%s</td>""" % year)
    link = base_link + "&display=%s" % date_next_year
    res.append ("""     <td><a href="%s">&gt;</a></td>""" % link)
    res.append ("""    </tr>""")
    res.append ("""   </table>""")
    res.append ("""  </td>""")
    res.append (""" </tr>""")

    # the calendar
    res.append (""" <tr>""")
    res.append ("""  <td>""")
    res.append ("""   <table class="calendar_display">""")
    res.append ("""    <tr class="weekdays">""")
    for day_ in calendar.weekheader (3).split () :
        res.append \
               ("""     <td>%s</td>""" % day_)
    res.append ("""    </tr>""")

    for week_ in calendar.monthcalendar (year, month) :
        res.append \
               ("""    <tr>""")
        for day_ in week_ :
            link = "javascript:form[field].value = '%d-%02d-%02d'; " \
                              "window.close ();" % (year, month, day_)
            #print curr_date, day_, month, year
            if day_  == curr_date.day   and \
               month == curr_date.month and \
               year  == curr_date.year :
                # highlight
                style = "today"
            else :
                style = ""
            if day_ :
                res.append \
               ("""     <td class="%s"><a href="%s">%s</a></td>""" %
                          (style, link, day_))
            else :
                res.append \
               ("""     <td></td>""")
        res.append \
               ("""    </tr>""")
    res.append ("""   </table>""")
    res.append ("""  </tb>""")
    res.append (""" </tr>""")
    res.append ("""</table>""")
    return "\n".join (res)
# end def html_calendar

def daily_record_check_batch (db, request) :
    if 'user' not in request.filterspec or 'date' not in request.filterspec :
        return []
    batch = request.batch ()
    if batch.sequence_length > 31 :
        return []
    return batch
# end def daily_record_check_batch

def batch_has_status (batch, status) :
    b = copy (batch)
    for i in batch :
        if str (i.status) == status :
            return True
    return False
# end def batch_open

def work_packages (db, daily_record, editable = True) :
    """ Compute allowed work packages for this date and user of the
        given daily_record. Needs a HTML db and a HTML daily_record.
    """
    if not editable :
        return []
    date = daily_record.date._value # is a html prop
    user = daily_record.user.id
    filt = {'project.approval_required' : False}
    srt  = [('+', 'project.name'), ('+', 'name')]
    wps  = vacation.valid_wps \
        (db._db, filter = filt, date = date, user = user, srt = srt)
    wps  = (db.time_wp.getItem (k) for k in wps)
    srt  = lambda z: (localecollate (z.project), localecollate (z.name))
    return sorted (wps, key = srt)
# end def work_packages

def work_packages_selector (wps) :
    """ Generate all options for wps inside a selector. Return html and
        a dict containing id to option number mapping
    """
    d    = { -1 : 0 }
    html = [' <option value="-1">- no selection -</option>']
    for n, wp in enumerate (wps) :
        d [wp.id] = n + 1
        html.append \
            ( ' <option value="%s">%s %s %s</option>'
            % tuple ([escape (str (s)) for s in
                      (wp.id, wp.project, wp.wp_no, wp.name)]
                    )
            )
    return '\n'.join (html), d
# end def work_packages_selector

def work_packages_javascript (name, wpsdict, id) :
    idx = wpsdict.get (id, 0)
    return ("<script> document.edit_daily_record ['%(name)s'].options "
            "[%(idx)s].selected = true;</script>"
           % locals ()
           )
# end def work_packages_javascript

def u_sorted (vals, keys, fun = str) :
    """ Sort given values by given keys.
        The function "fun" is tricky. If you want to sort numerically,
        use "int" here, but i18n.gettext is also nice for sorting by
        translated values...
    """
    key    = lambda x : [fun (x [k]) for k in keys]
    return sorted (vals, key = key)
# end def u_sorted

def weekend_allowed (db, daily_record) :
    user, date = [str (daily_record [i]) for i in 'user', 'date']
    user = db.user.lookup (user)
    dyn = user_dynamic.get_user_dynamic (db, user, date)
    return dyn and dyn.weekend_allowed
# end def weekend_allowed

def approval_for (db, valid_only = False) :
    """ Return a hash of all user-ids for which the current db.getuid()
        user may approve time records. If valid_only is specified we
        return only users with status 'valid' or a user_dyn record with
        a frozen date below the validity span.
    """
    try :
        db  = db._db
    except AttributeError :
        pass
    uid = db.getuid ()
    clearer_for = db.user.find   (clearance_by = uid)
    subst       = db.user.filter \
        (None, {'substitute' : uid, 'subst_active' : True})
    clearer_for.extend (subst)
    # clearance_by may be inherited once via subst:
    if subst :
        clearer_for.extend (db.user.find (clearance_by = subst))
    if not db.user.get (uid, 'clearance_by') :
        clearer_for.append (uid)
    # if clearer_for is empty return empty dict
    if not clearer_for :
        return {}
    d   = dict (supervisor = clearer_for)
    d_a = dict (d)
    if valid_only :
        d_a ['status'] = db.user_status.lookup ('valid')
    approve_for = dict.fromkeys (db.user.filter (None, d_a), 1)
    if valid_only :
        d ['status'] = list \
            (x for x in db.user_status.getnodeids (retired = False)
             if x != d_a ['status']
            )
        invalid = dict.fromkeys (db.user.filter (None, d), 1)
        for u in invalid.keys () :
            if u in approve_for :
                del invalid [u]
                continue
            dyn = user_dynamic.act_or_latest_user_dynamic (db, u)
            if not dyn :
                del invalid [u]
                continue
            # User invalid but dyn user valid?!
            if dyn.valid_to is None :
                continue
            if freeze.frozen (db, u, dyn.valid_to - common.day) :
                del invalid [u]
        approve_for.update (invalid)
    if uid in approve_for :
        del approve_for [uid]
    return approve_for
# end def approval_for

def welcome (db) :
    fname = os.path.join (db.config.TRACKER_HOME, 'Welcome-Info.txt')
    try :
        text = file (fname, 'rU').read ()
        return escape (text).replace ('\n\n', '<br>\n')
    except IOError :
        pass
    return "".join ((db._ (''"Welcome to the "), db.config.TRACKER_NAME, '.'))
# end def welcome

def color_duration (tr) :
    """Compute the css class for a duration or tr_duration. Note that we
       also compute the cached value of tr_duration if not yet computed.
    """
    db         = tr._db
    travel_act = db.time_activity.filter (None, {'travel' : True})
    travel_act = dict ((a, 1) for a in travel_act)
    if tr.time_activity and tr.time_activity.id in travel_act:
        if not tr.tr_duration or tr.activity < tr.daily_record.activity :
            id = tr.daily_record.id
            user_dynamic.update_tr_duration (db, db.daily_record.getnode (id))
        return 'travel'
    return ''
# end def color_duration

def now () :
    return Date ('.')
# end def now

def until_now () :
    return now ().pretty (';%Y-%m-%d')
# end def until_now

def get_from_form (request, name) :
    try :
        for key in ('@' + name, ':' + name):
            if request.form.has_key (key):
                return request.form [key].value.strip()
    except TypeError:
        pass
    return ''
# end def get_from_form

def user_props (db) :
    try :
        db = db._db
    except AttributeError :
        pass
    props = dict (username = 0, firstname = 2, lastname = 3, address = 6)
    props = dict \
        ((k, v) for k, v in props.iteritems () if k in db.user.properties)
    if 'firstname' not in props :
        props ['realname'] = 5
    return ','.join \
        (x [0] for x in sorted (props.iteritems (), key = lambda x : x [1]))
# end def user_props

def user_classhelp \
    ( db
    , property='responsible'
    , inputtype      = 'radio'
    , user_status    = None
    , ids            = None
    , form           = 'itemSynopsis'
    , internal_only  = False
    , exclude_system = False
    , client         = None
    ) :
    try :
        hdb = db._db
    except AttributeError :
        hdb = db
    if user_status :
        status = user_status
    else :
        udict = dict (is_nosy = True)
        if exclude_system :
            udict ['is_system'] = False
        if internal_only :
            udict ['is_internal'] = True
        status = ','.join (hdb.user_status.filter (None, udict))
    if status :
        status = ';status=' + status
    idfilter = ''
    if ids :
        if isinstance (ids, type ([])) :
            ids = ','.join (ids)
        idfilter = ';id=' + ids
    if isinstance (db, hyperdb_database) :
        classhelp = HTMLClass (client, 'user').classhelp
    else :
        classhelp = db.user.classhelp
    return classhelp \
        ( user_props (db)
        , property  = property
        , filter    = 'roles=Nosy' + status + idfilter
        , inputtype = inputtype
        , width     = '1200'
        , pagesize  = 2000
        , form      = form
        )
# end def user_classhelp

def nickname (db, user) :
    if 'nickname' in db._db.user.properties and user.nickname.is_view_ok () :
        return user.nickname.plain (escape = 1)
    return user.username.plain (escape = 1)
# end def nickname

def indexargs_dict (nav, form) :
    d = {}
    if nav :
        d = {':startwith' : nav.first, ':pagesize' : nav.size}
    if form.has_key (':nosearch') :
        d [':nosearch'] = 1
    return d
# end def indexargs_dict

def may_search (db, uid, classname, property) :
    check = getattr (db.security, 'hasSearchPermission', None)
    if check :
        return check (uid, classname, property)
    return True
# end def may_search

def artefact_link_match (db, field) :
    """ Match given field content against configurable regex.
        Return True if matching.
    """
    try :
        db = db._db
    except AttributeError :
        pass
    if not field :
        return None
    rgx = re.compile (getattr (db.config.ext, 'MATCH_ARTEFACT', 'http'))
    return rgx.search (field)
# end def artefact_link_match

def pr_agents (db) :
    try :
        db = db._db
    except AttributeError :
        pass
    vroles = set ()
    for ptid in db.purchase_type.getnodeids (retired = False) :
        pt = db.purchase_type.getnode (ptid)
        vroles.update (pt.pr_view_roles)
    users = set ()
    for rid in vroles :
        vr = db.pr_approval_order.getnode (rid)
        users.update (vr.users)
    return ','.join (users)
# end def pr_agents

def valid_activities (db, date) :
    try :
        db = db._db
    except AttributeError :
        pass
    date = date._value
    all_activities = db.time_activity.getnodeids (retired = False)
    if 'reduced_activity_list' not in db.user.properties :
        return all_activities
    ts = db.user.get (db.getuid (), 'reduced_activity_list')
    if ts and ts <= date :
        return list (set (all_activities).intersection (['10', '11']))
    return all_activities
# end def valid_activities

def valid_item (now) :
    """ Return parameters for querying valid items of a class that has
        valid_from and valid_to properties.
    """
    pr = common.pretty_range
    d  = dict \
        ( valid_from = ','.join ((pr (None, now), '-'))
        , valid_to   = ','.join ((pr (now),       '-'))
        )
    return d
# end def valid_item

def init (instance) :
    reg = instance.registerUtil
    reg ("correct_midnight_date_string", correct_midnight_date_string)
    reg ("rough_date_diff",              rough_date_diff)
    reg ("start_timer",                  start_timer)
    reg ("time_stamp",                   time_stamp)
    reg ("date_help",                    date_help)
    reg ("html_calendar",                html_calendar)
    reg ("batch_has_status",             batch_has_status)
    reg ("daily_record_check_batch",     daily_record_check_batch)
    reg ("work_packages",                work_packages)
    reg ("work_packages_selector",       work_packages_selector)
    reg ("work_packages_javascript",     work_packages_javascript)
    reg ("sorted",                       u_sorted)
    reg ("weekend_allowed",              weekend_allowed)
    reg ("approval_for",                 approval_for)
    reg ("user_has_role",                common.user_has_role)
    reg ("welcome",                      welcome)
    reg ("monthstart_twoweeksago",       common.monthstart_twoweeksago)
    reg ("get_user_dynamic",             user_dynamic.get_user_dynamic)
    reg ("next_user_dynamic",            user_dynamic.next_user_dynamic)
    reg ("prev_user_dynamic",            user_dynamic.prev_user_dynamic)
    reg ("act_or_latest_user_dynamic",  user_dynamic.act_or_latest_user_dynamic)
    reg ("ymd",                          common.ymd)
    reg ("color_duration",               color_duration)
    reg ("now",                          now)
    reg ("until_now",                    until_now)
    reg ("get_from_form",                get_from_form)
    reg ("user_classhelp",               user_classhelp)
    reg ("nickname",                     nickname)
    reg ("persons_for_adr",              common.persons_for_adr)
    reg ("indexargs_dict",               indexargs_dict)
    reg ("may_search",                   may_search)
    reg ("Size_Limit",                   common.Size_Limit)
    reg ("user_props",                   user_props)
    reg ("artefact_link_match",          artefact_link_match)
    reg ("pr_agents",                    pr_agents)
    reg ("valid_activities",             valid_activities)
    reg ("valid_item",                   valid_item)
