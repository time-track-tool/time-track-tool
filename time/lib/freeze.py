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
from   common             import next_search_date, day

def frozen (db, user, date) :
    """ Get frozen freeze-records >= date. If some are found, the date
        is frozen.
    """
    f = db.daily_record_freeze.filter \
        ( None
        , dict (user = user, date = date.pretty ('%Y-%m-%d;'), frozen = True)
        , group = [('+', 'date')]
        )
    return f
# end def frozen

def range_frozen (db, user, range) :
    """Check if a given range of dates is completely frozen
    """
    if not range or not user :
        return False
    if ';' not in range :
        db.get_logger ().error ("RANGE: %s" % range)
    date = Date (range.split (';')[1])
    return frozen (db, user, date)
# end def range_frozen

def find_next_dr_freeze (db, user, date, direction = '+', frozen = True) :
    """ Search for next daily_record_freeze in direction *after* date.
        By default searches for frozen records only. Setting frozen to
        None will find *all* records, setting it to False will find only
        thawed records.
    """
    try :
        db = db._db
    except AttributeError :
        pass
    date  = next_search_date (date, direction)
    sdict = dict (user = user, date = date)
    if frozen is not None :
        sdict ['frozen'] = frozen
    recs  = db.daily_record_freeze.filter \
        (None, sdict, group = [(direction, 'date')])
    if recs :
        return db.daily_record_freeze.getnode (recs [0])
    return None
# end def find_next_dr_freeze

def find_prev_dr_freeze (db, user, date, frozen = True) :
    return find_next_dr_freeze \
        (db, user, date, direction = '-', frozen = frozen)
# end def find_prev_dr_freeze

def _find_next (db, daily_record_freeze, direction = '+', frozen = None) :
    user = daily_record_freeze.user.id
    return find_next_dr_freeze \
        (db, user, daily_record_freeze.date, direction, frozen = frozen)
# end def _find_next

def next_dr_freeze (db, daily_record_freeze, frozen = None) :
    return _find_next (db, daily_record_freeze, frozen = frozen)
# end def next_dr_freeze

def prev_dr_freeze (db, daily_record_freeze, frozen = None) :
    return _find_next (db, daily_record_freeze, '-', frozen = frozen)
# end def prev_dr_freeze

### __END__
