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
#    time_record
#
# Purpose
#    Detectors for the 'time_record'
#
# Revision Dates
#     8-Jun-2005 (RSC) Creation
#    ««revision-date»»···
#--
#

from roundup            import roundupdb, hyperdb
from roundup.exceptions import Reject
from roundup.date       import Date

def check_timestamps (start, end, date) :
    start.year  = end.year  = date.year
    start.month = end.month = date.month
    start.day   = end.day   = date.day
    if start < end :
        raise Reject, "start and end must be on same day and start < end."
    if start.timestamp () % 900 or end.timestamp () % 900 :
        raise Reject, "Times must be given in quarters of an hour"
# end def check_timestamp

def check_duration (d) :
    if duration.as_seconds () % 900 :
        raise Reject, "Times must be given in quarters of an hour"
# end def check_duration

def new_time_record (db, cl, nodeid, new_values) :
    """ auditor on time_record
        set default for date of today if not given
        either duration or both start/end must be set but not both
        -- correct start/end to 'date' if wrong day
        set duration from start/end if duration empty
    """
    if 'date' not in new_values :
        now = Date ('.')
        now.hour = now.minute = now.second = 0
        new_values ['date'] = now
    if 'start' in new_values :
        if not 'end' in new_values :
            raise Reject, "end time must be given"
        if 'duration' in new_values :
            raise Reject, "Either specify duration or start/end"
        start = new_values ['start']
        end   = new_values ['end']
        check_timestamps (start, end, date)
        new_values ['duration'] = start - end
    else :
        if 'start' in new_values or 'end' in new_values :
            raise Reject, "Either specify duration or start/end"
        duration = new_values ['duration']
        check_duration (duration)
# end def new_time_record

def check_time_record (db, cl, nodeid, new_values) :
    date     = new_values.get ('date',       cl.get (nodeid, 'date'))
    start    = new_values.get ('start',      cl.get (nodeid, 'start'))
    end      = new_values.get ('end',        cl.get (nodeid, 'end'))
    duration = new_values.get ('duration',   cl.get (nodeid, 'duration'))
    if start :
        if 'duration' in new_values :
            raise Reject, "Either specify duration or start/end"
        check_timestamps (start, end, date)
        new_values ['duration'] = start - end
    else :
        check_duration (duration)
# end def check_time_record

def init (db) :
    db.time_record.audit ("create" , new_time_record)
    db.time_record.audit ("set"    , check_time_record)
# end def init

### __END__ time_record
