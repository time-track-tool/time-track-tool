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
#    release
#
# Purpose
#    Detectors for the 'release' class
#
# Revision Dates
#    11-Oct-2004 (MPH) Creation
#    ««revision-date»»···
#--
#

from roundup import mailgw, date
from roundup.cgi import client, templating

class Client(client.Client):
    ''' derives basic CGI implementation from the standard module,
        with any specific extensions
    '''
    pass

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

class MailGW(mailgw.MailGW):
    ''' derives basic mail gateway implementation from the standard module,
        with any specific extensions
    '''
    pass

# vim: set filetype=python ts=4 sw=4 et si
