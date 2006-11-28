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
#    freeze
#
# Purpose
#    Freezing of daily records
#
#--
#
from   roundup import roundupdb, hyperdb
from   roundup.exceptions import Reject
from   roundup.date       import Date, Interval, Range
from   time               import gmtime
from   roundup.hyperdb    import String, Link, Multilink
from   common             import next_search_date

def frozen (db, user, date) :
    """ Get freeze-records >= date. If some are found, check if date is
        frozen.
    """
    f = db.daily_record_freeze.filter \
        ( None
        , dict (user = user, date = date.pretty ('%Y-%m-%d;'), frozen = True)
        )
    return f
# end def frozen

def range_frozen (db, user, range) :
    """Check if a given range of dates is completely frozen
    """
    if not range or not user :
        return False
    date = Date (range.split (';')[1])
    return frozen (db, user, date)
# end def range_frozen

def _find_next (db, daily_record_freeze, direction = '+') :
    user = daily_record_freeze.user.id
    date = next_search_date (daily_record_freeze.date, direction)
    recs = db._db.daily_record_freeze.filter \
        (None, dict (user = user, date = date), group = [(direction, 'date')])
    if recs :
        return recs [0]
    return None
# end def _find_next

def next_dr_freeze (db, daily_record_freeze) :
    return _find_next (db, daily_record_freeze)
# end def next_dr_freeze

def prev_dr_freeze (db, daily_record_freeze) :
    return _find_next (db, daily_record_freeze, '-')
# end def prev_dr_freeze

### __END__
