# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
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
#    ««revision-date»»···
#--
#

from roundup import mailgw, date
from roundup.cgi import client, templating
import calendar

r_date = date

class Client(client.Client):
    ''' derives basic CGI implementation from the standard module,
        with any specific extensions
    '''
    pass
# end class Client

class TemplatingUtils:
    ''' Methods implemented on this class will be available to HTML templates
        through the 'utils' variable.
    '''
    def correct_midnight_date_string (self, db) :
        """returns GMT's "today.midnight" in localtime format.
        suitable for passing in to forms that need this date.
        """
        d   = date.Date ('00:00', -db._db.getUserTimezone ())
        return d.pretty ('%Y-%m-%d.%H:%M:%S')
    # end def correct_midnight_date_string

    def rough_date_diff (self, left, right, format = "%Y-%m-%d") :
        """returns the interval between the two dates left - right.
        format is used for the granularity when interpreting the two values.

        left and right need to be date.Date values.
        format needs to be a date.Date parseable format.
        """
        l_d = date.Date (left.pretty (format))
        r_d = date.Date (right.pretty (format))
        return l_d - r_d
    # end def rough_date_diff

    def date_help ( self
                  , request
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
            date = "&date=%s" % item
        else :
            date = ""
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
    # end def date_help

    def html_calendar (self, request) :
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
        print request.form
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
                print curr_date, day_, month, year
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
# end class TemplatingUtils

class MailGW(mailgw.MailGW):
    ''' derives basic mail gateway implementation from the standard module,
        with any specific extensions
    '''
    pass
# end class MailGW

### __END__ task
# vim: set filetype=python ts=4 sw=4 et si
