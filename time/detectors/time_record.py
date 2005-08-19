#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
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
#    Detectors for the 'time_record' and 'daily_record'
#
# Revision Dates
#     8-Jun-2005 (RSC) Creation
#    ««revision-date»»···
#--
#

from roundup                        import roundupdb, hyperdb
from roundup.exceptions             import Reject
from roundup.date                   import Date, Interval
from roundup.cgi.TranslationService import get_translation

_ = lambda x : x

def check_timestamps (start, end, date) :
    start.year  = end.year  = date.year
    start.month = end.month = date.month
    start.day   = end.day   = date.day
    if start >= end :
        raise Reject, "start and end must be on same day and start < end."
    if start.timestamp () % 900 or end.timestamp () % 900 :
        raise Reject, "Times must be given in quarters of an hour"
# end def check_timestamp

def check_duration (d) :
    if (d * 3600) % 900 :
        raise Reject, "Times must be given in quarters of an hour"
# end def check_duration

hour_format = '%H:%M'

def check_daily_record (db, cl, nodeid, new_values) :
    for i in 'user', 'date' :
        if i in new_values :
            raise Reject, "%(attr)s may not be changed" % {'attr' : _ (i)}
    if i in ('status',) :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s must be set" % {'attr' : _ (i)}
# end def check_daily_record

def update_time_record_in_daily_record (db, cl, nodeid, old_values) :
    drec_id = cl.get (nodeid, 'daily_record')
    trecs_o = [int (i) for i in db.daily_record.get (drec_id, 'time_record')]
    trecs   = dict ([(i, 1) for i in trecs_o])
    trecs [int (nodeid)] = 1
    trecs   = trecs.keys ()
    trecs.sort ()
    if trecs != trecs_o :
        db.daily_record.set (drec_id, time_record = [str (i) for i in trecs])
# end def update_time_record_in_daily_record

def new_daily_record (db, cl, nodeid, new_values) :
    """
        If a new daily_record is created, we check the date provided:
        If hours, minutes, seconds are all zero we think the time was
        entered in UTC and do no conversion. If one is non-zero, we get
        the timezone from the user information and re-encode the date as
        UTC -- this effectively makes the date a 'naive' date. Then we
        nullify hour, minute, second of the date.
        After that, we check that there is no duplicate daily_record
        with the same date for this user.
    """
    for i in 'user', 'date' :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
    for i in 'status', 'time_record' :
        if i in new_values :
            raise Reject, "%(attr)s must not be specified" % {'attr' : _ (i)}
    date = new_values ['date']
    date.hour = date.minute = date.second = 0
    new_values ['date'] = date
    user = new_values ['user']
    if db.daily_record.filter \
        (None, {'date' : str (date.local (0)), 'user' : user}) :
        raise Reject, "Duplicate record: date = %(date)s, user = %(user)s" \
            % new_values
    new_values ['time_record'] = []
    new_values ['status']      = db.daily_record_status.lookup ('open')
# end def new_daily_record

def check_start_end_duration (date, start, end, duration, new_values) :
    """
        either duration or both start/end must be set but not both
        of duration/end
        set duration from start/end if duration empty
        set end from start/duration if end empty
        Note: We are using naive times (with timezone 0) here, this
        means we can safely use date.pretty for converting back to
        string.
        FIXME: if start not provided, check if allowed to record
               durations only
    """
    if 'end' in new_values :
        if not start :
            raise Reject, "%(attr)s must be specified" % {'attr' : 'start'}
        if 'duration' in new_values :
            raise Reject, "Either specify duration or start/end"
        dstart = Date (start, offset = 0)
        dend   = Date (end,   offset = 0)
        check_timestamps (dstart, dend, date)
        new_values ['duration'] = (dend - dstart).as_seconds () / 3600.
        new_values ['start']    = dstart.pretty (hour_format)
        new_values ['end']      = dend.pretty   (hour_format)
    else :
        if not duration :
            raise Reject, "Either specify duration or start/end"
        check_duration (duration)
        if 'duration' in new_values :
            new_values ['duration'] = duration
        if start and ('start' in new_values or 'duration' in new_values) :
            dstart  = Date (start, offset = 0)
            minutes = duration * 60
            hours   = duration % 60
            minutes = minutes - hours * 60
            dend    = dstart + Interval ('%d:%d' % (hours, minutes))
            check_timestamps (dstart, dend, date)
            new_values ['start'] = dstart.pretty (hour_format)
            new_values ['end']   = dend.pretty   (hour_format)
# end def check_start_end_duration

def new_time_record (db, cl, nodeid, new_values) :
    """ auditor on time_record
    """
    for i in 'daily_record', :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
    date     = db.daily_record.get (new_values ['daily_record'], 'date')
    start    = new_values.get ('start',    None)
    end      = new_values.get ('end',      None)
    duration = new_values.get ('duration', None)
    check_start_end_duration (date, start, end, duration, new_values)
# end def new_time_record

def check_time_record (db, cl, nodeid, new_values) :
    for i in 'daily_record', :
        if i in new_values :
            raise Reject, "%(attr)s may not be changed" % {'attr' : _ (i)}
    drec     = new_values.get ('daily_record', cl.get (nodeid, 'daily_record'))
    start    = new_values.get ('start',        cl.get (nodeid, 'start'))
    end      = new_values.get ('end',          cl.get (nodeid, 'end'))
    duration = new_values.get ('duration',     cl.get (nodeid, 'duration'))
    date     = db.daily_record.get (drec, 'date')
    check_start_end_duration (date, start, end, duration, new_values)
# end def check_time_record

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.time_record.audit  ("create", new_time_record)
    db.time_record.audit  ("set",    check_time_record)
    db.time_record.react  ("create", update_time_record_in_daily_record)
    db.daily_record.audit ("create", new_daily_record)
    db.daily_record.audit ("set",    check_daily_record)
# end def init

### __END__ time_record
