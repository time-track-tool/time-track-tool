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
#     1-Dec-2004 (MPH) Added `start_timer` and `time_stamp` for profiling
#    ««revision-date»»···
#--
#

from roundup import mailgw, date
from roundup.cgi import client, templating
import calendar
import time

MultilinkHTMLProperty = templating.MultilinkHTMLProperty

r_date = date

class SearchAttribute :
    """
        util:  instance of TemplatingUtils
        name:  name of the attribute of the item to be displayed in the
               search.
        label: label of the field in html.
        lnkcls, lnkattr: applies to Link and Multilink properties
        only and give the class to which the link points and the
        attribute to display for this class.

        SearchAttribute items will come from the index page for
        a class (an entry in "props" for the search_display macro).
    """
    def __init__ \
        ( self
        , util
        , prop
        , item        = None
        , selname     = None
        , label       = None
        , lnkcls      = None
        , lnkattr     = None
        , multiselect = None
        , is_label    = None
        , editable    = None
        ) :
        self.util        = util
        self.prop        = prop
        self.item        = item
        self.classname   = prop._classname
        self.klass       = prop._db.getclass (self.classname)
        self.name        = prop._name
        self.selname     = selname
        self.label       = label
        self.lnkname     = None
        self.lnkattr     = lnkattr
        self.multiselect = multiselect
        self.is_label    = is_label
        self.editable    = editable
        self.key         = None
        if hasattr (prop._prop, 'classname') :
            self.lnkname = prop._prop.classname
            self.lnkcls  = prop._db.getclass (self.lnkname)
            self.key     = self.lnkcls.getkey ()
        if not self.selname :
            self.selname = self.name
            if self.lnkattr :
                l = self.lnkattr.split ('.')
                if len (l) > 1 :
                    self.selname = l [-2]
        if not self.label :
            self.label = self.util.pretty (self.selname)

        if self.lnkname and not self.lnkattr :
            self.lnkattr = self.lnkcls.labelprop ()
        if (   self.is_label is None
           and (  self.name == 'id'
               or self.klass.labelprop () == self.classname
               )
           ) :
            self.is_label = 1
        if self.item :
            self.hprop = item [self.name]
    # end def __init__

    def as_listentry (self, item) :
        self.item  = item
        self.hprop = item [self.name]
        if self.editable :
            return self.editfield ()
        if self.is_label :
            return self.formatlink ()
        elif self.lnkname :
            if isinstance (self.hprop, MultilinkHTMLProperty) :
                return ", ".join \
                    ([ self.deref (i).formatlink ()
                       for i in range (len (self.hprop))
                    ])
            else :
                return self.deref ().formatlink ()
        return str (self.hprop)
    # end def as_listentry

    def deref (self, index = None) :
        """
            from an item get the property prop. This does some recursive
            magic: If prop consists of a path across several other Link
            properties, we dereference the whole prop list.
            Returns the new SearchAttribute.
        """
        p = self.hprop
        if index is not None : p = self.hprop [index]
        for i in self.lnkattr.split ('.') :
            last_p = p
            p      = p [i]
        return self.util.SearchAttribute (self.util, p, item = last_p)
    # end def deref

    def sortable (self) :
        return self.key == self.lnkattr
    # def sortable

    def formatlink (self) :
        """
            Render my property of an item as a link to this item. We get
            the item. The name of the item and its id are computed.
        """
        i = self.item
        return """<a class="%s" href="%s%s">%s</a>""" \
            % (self.util.linkclass (i), self.classname, i.id, self.hprop)
    # end def formatlink

    def editfield (self) :
        return "<span style='white-space:nowrap'>%s</span>" \
            % self.item [self.name].field ()
    # end def editfield

# end class SearchAttribute


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

    SearchAttribute = SearchAttribute

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

    def start_timer (self) :
        """starts an internal timer for profiling the templates
        """
        self.timer = time.time ()
        return self.timer
    # end def start_timer

    def time_stamp (self) :
        """return a timestamp in seconds elapsed from last `start_timer` call
        """
        return time.time () - self.timer
    # end def time_stamp

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
