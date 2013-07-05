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
import locale
from roundup.cgi.TranslationService import get_translation
from roundup.date                   import Date, Interval
from copy                           import copy
from xml.sax.saxutils               import escape

from user_dynamic                   import get_user_dynamic
from user_dynamic                   import act_or_latest_user_dynamic
from user_dynamic                   import next_user_dynamic, prev_user_dynamic
from user_dynamic                   import update_tr_duration
from common                         import clearance_by, ymd, persons_for_adr
from common                         import user_has_role, monthstart_twoweeksago
from common                         import Size_Limit

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
    from time import time
    date       = daily_record.date
    filterspec = \
        { 'bookers'    : daily_record.user.id
        , 'time_start' : ';%s' % date
        }
    x1 = db._db.time_wp.filter (None, filterspec)
    #print "1st query", time () - timestamp, daily_record.user.id, date
    filterspec ['bookers'] = '-1'
    x2 = db._db.time_wp.filter (None, filterspec)
    #print "2nd query", time () - timestamp
    wps = (db.time_wp.getItem (k) for k in x1 + x2)
    x = [wp for wp in wps if not wp.time_end or wp.time_end >= date]
    #print "filtering", time () - timestamp
    srt = lambda z: (localecollate (z.project), localecollate (z.name))
    return sorted (x, key = srt)
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
    dyn = get_user_dynamic (db, user, date)
    return dyn and dyn.weekend_allowed
# end def weekend_allowed

def approval_for (db) :
    """ Return a hash of all user-ids for which the current db.getuid()
        user may approve time records
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
    if not db.user.get (uid, 'clearance_by') :
        clearer_for.append (uid)
    approve_for = []
    for u in clearer_for :
        approve_for.extend (db.user.find (supervisor = u))
    aprv = dict ([(a, 1) for a in approve_for])
    if uid in aprv : del aprv [uid]
    return aprv
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
            update_tr_duration (db, db.daily_record.getnode (id))
            db.commit()
        return 'travel'
    return ''
# end def color_duration

def now () :
    return Date ('.')
# end def now

def until_now () :
    return now ().pretty (';%Y-%-m-%d')
# end def until_now

def get_from_form (request, name) :
    for key in ('@' + name, ':' + name):
        if request.form.has_key (key):
            return request.form [key].value.strip()
    return ''
# end def get_from_form

def user_classhelp (db, property='responsible', inputtype = 'radio') :
    status = ','.join \
        (db._db.user_status.filter (None, dict (is_nosy = True)))
    if status :
        status = ';status=' + status
    return db.user.classhelp \
        ( ','.join (n for n in
                    'username,nickname,firstname,lastname'.split(',')
                    if n in db._db.user.properties
                   )
        , property  = property
        , filter    = 'roles=Nosy' + status
        , inputtype = inputtype
        , width     = '600'
        , pagesize  = 500
        )
# end def user_classhelp

def nickname (db, user) :
    if 'nickname' in db._db.user.properties and user.nickname.is_view_ok () :
        return user.nickname.plain ()
    return user.username.plain ()
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

def init (instance) :
    reg = instance.registerUtil
    reg ("correct_midnight_date_string", correct_midnight_date_string)
    reg ("rough_date_diff",              rough_date_diff)
    reg ("start_timer",                  start_timer)
    reg ("time_stamp",                   time_stamp)
    reg ("date_help",                    date_help)
    reg ("html_calendar",                html_calendar)
    reg ("batch_has_status",             batch_has_status)
    reg ("work_packages",                work_packages)
    reg ("work_packages_selector",       work_packages_selector)
    reg ("work_packages_javascript",     work_packages_javascript)
    reg ("sorted",                       u_sorted)
    reg ("weekend_allowed",              weekend_allowed)
    reg ("approval_for",                 approval_for)
    reg ("clearance_by",                 clearance_by)
    reg ("user_has_role",                user_has_role)
    reg ("welcome",                      welcome)
    reg ("monthstart_twoweeksago",       monthstart_twoweeksago)
    reg ("get_user_dynamic",             get_user_dynamic)
    reg ("next_user_dynamic",            next_user_dynamic)
    reg ("prev_user_dynamic",            prev_user_dynamic)
    reg ("act_or_latest_user_dynamic",   act_or_latest_user_dynamic)
    reg ("ymd",                          ymd)
    reg ("color_duration",               color_duration)
    reg ("now",                          now)
    reg ("until_now",                    until_now)
    reg ("get_from_form",                get_from_form)
    reg ("user_classhelp",               user_classhelp)
    reg ("nickname",                     nickname)
    reg ("persons_for_adr",              persons_for_adr)
    reg ("indexargs_dict",               indexargs_dict)
    reg ("may_search",                   may_search)
    reg ("Size_Limit",                   Size_Limit)
