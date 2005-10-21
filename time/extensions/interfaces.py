# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004,2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@mexx.mobile
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
#
#++
# Name
#    interfaces
#
# Purpose
#    Define utlilities used by roundup
#
# Revision Dates
#    11-Oct-2004 (MPH) Creation - from default tracker's interfaces.py
#     2-Nov-2004 (MPH) Added `calendar`
#     1-Dec-2004 (MPH) Added `start_timer` and `time_stamp` for profiling
#     6-Jun-2005 (RSC) Moved to extensions and reworked for new 0.8 framework
#     8-Jun-2005 (RSC) Removed "self" (was reference to utils in old framework)
#                      Note that the timer now needs some explicit object
#     8-Jun-2005 (RSC) Missing import of time and calendar added.
#    ««revision-date»»···
#--
#

import calendar
import time
import os
from roundup.cgi.TranslationService import get_translation
from roundup                        import date as r_date
from copy                           import copy
from xml.sax.saxutils               import escape

_      = lambda x : x
common = None

def correct_midnight_date_string (db) :
    """returns GMT's "today.midnight" in localtime format.
    suitable for passing in to forms that need this date.
    """
    d   = date.Date ('00:00', -db._db.getUserTimezone ())
    return d.pretty ('%Y-%m-%d.%H:%M:%S')
# end def correct_midnight_date_string

def rough_date_diff (left, right, format = "%Y-%m-%d") :
    """returns the interval between the two dates left - right.
    format is used for the granularity when interpreting the two values.

    left and right need to be date.Date values.
    format needs to be a date.Date parseable format.
    """
    l_d = date.Date (left.pretty (format))
    r_d = date.Date (right.pretty (format))
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
    , label    = "(cal)"
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
    curr_date = r_date.Date (date_str) # to highlight
    display   = r_date.Date (display)  # to show
    year      = display.year
    month     = display.month
    day       = display.day

    # for navigation
    date_prev_month = display + r_date.Interval ("-1m")
    date_next_month = display + r_date.Interval ("+1m")
    date_prev_year  = display + r_date.Interval ("-1y")
    date_next_year  = display + r_date.Interval ("+1y")

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

def button_submit_to (db, user, date) :
    """ Create the submit_to button for time tracking submissions. We
        get the supervisor of the user and check if clearance is
        delegated.
    """
    db = db._db
    supervisor = db.user.get (user,       'supervisor')
    clearance  = db.user.get (supervisor, 'clearance_by') or supervisor
    nickname   = db.user.get (clearance,  'nickname').upper ()
    return \
        '''<input type="button" value="%s"
            onClick="
                document.forms.edit_daily_record ['@action'].value =
                    'daily_record_submit';
                document.forms.edit_daily_record ['date'].value = '%s'
                document.edit_daily_record.submit ();
            ">
        ''' % (_ ("Submit to %(nickname)s" % locals ()), date)
# end def button_submit_to

def button_action (date, action, value) :
    """ Create a button for time-tracking actions """
    ''"approve", ''"deny", ''"edit again"
    #print action, value
    return \
        '''<input type="button" value="%s"
            onClick="
                document.forms.edit_daily_record ['@action'].value =
                    'daily_record_%s';
                document.forms.edit_daily_record ['date'].value = '%s'
                document.edit_daily_record.submit ();
            ">
        ''' % (value, action, date)
# end def button_action

def batch_has_status (batch, status) :
    b = copy (batch)
    for i in batch :
        if str (i.status) == status :
            return True
    return False
# end def batch_open

def work_packages (db, daily_record) :
    """ Compute allowed work packages for this date and user of the
        given daily_record. Needs a HTML db and a HTML daily_record.
    """
    date       = daily_record.date
    filterspec = \
        { 'bookers'    : daily_record.user.id
        , 'time_start' : ';%s' % date
        }
    x1 = db.time_wp.filter (filterspec = filterspec)
    filterspec ['bookers'] = '-1'
    x2 = db.time_wp.filter (filterspec = filterspec)
    x = [wp for wp in x1 + x2 if not wp.time_end or wp.time_end >= date]
    return x
# end def work_packages

def sorted (vals, keys, fun = str) :
    """ Sort given values by given keys. Should be optimized to use key
        sorting (available in python 2.4) and fuction "sorted".
        The function "fun" is tricky. If you want to sort numerically,
        use "int" here, but i18n.gettext is also nice for sorting by
        translated values...
    """
    keyfun = lambda x, y : \
        cmp ([fun (x [k]) for k in keys], [fun (y [k]) for k in keys])
    vals   = [v for v in vals]
    vals.sort (keyfun)
    return vals
# end def sorted

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
    clearer_for = db.user.find (clearance_by = uid)
    if not db.user.get (uid, 'clearance_by') :
        clearer_for.append (uid)
    approve_for = []
    for u in clearer_for :
        approve_for.extend (db.user.find (supervisor = u))
    return dict ([(a, 1) for a in approve_for])
# end def approval_for

def welcome (db) :
    fname = os.path.join \
        ( '/tttech/company/operations/org-handbook/info'
        , 'Welcome-info-Startseite-Time2005.txt'
        )
    try :
        text = file (fname, 'rU').read ()
        return escape (text).replace ('\n\n', '<br>\n')
    except IOError :
        pass
    return "".join ((_ ("Welcome to the "), db.config.TRACKER_NAME, '.'))
# end def welcome

def init (instance) :
    import sys, os
    global _, get_user_dynamic
    sys.path.insert (0, os.path.join (instance.config.HOME, 'lib'))
    from user_dynamic import get_user_dynamic
    from common       import clearance_by
    from common       import user_has_role
    del (sys.path [0])
    _   = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.config.TRACKER_HOME).gettext
    reg = instance.registerUtil
    reg ("correct_midnight_date_string", correct_midnight_date_string)
    reg ("rough_date_diff",              rough_date_diff)
    reg ("start_timer",                  start_timer)
    reg ("time_stamp",                   time_stamp)
    reg ("date_help",                    date_help)
    reg ("html_calendar",                html_calendar)
    reg ("button_submit_to",             button_submit_to)
    reg ("button_action",                button_action)
    reg ("batch_has_status",             batch_has_status)
    reg ("work_packages",                work_packages)
    reg ("sorted",                       sorted)
    reg ("weekend_allowed",              weekend_allowed)
    reg ("approval_for",                 approval_for)
    reg ("clearance_by",                 clearance_by)
    reg ("user_has_role",                user_has_role)
    reg ("welcome",                      welcome)
