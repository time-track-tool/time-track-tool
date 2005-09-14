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
from operator                       import add
from time                           import gmtime

get_user_dynamic = None
user_has_role    = None
_                = lambda x : x

def check_timestamps (start, end, date) :
    start.year  = end.year  = date.year
    start.month = end.month = date.month
    start.day   = end.day   = date.day
    if start > end :
        raise Reject, _ ("start and end must be on same day and start <= end.")
    if start.timestamp () % 900 or end.timestamp () % 900 :
        raise Reject, _ ("Times must be given in quarters of an hour")
# end def check_timestamp

def check_duration (d) :
    if (d * 3600) % 900 :
        raise Reject, _ ("Times must be given in quarters of an hour")
# end def check_duration

hour_format = '%H:%M'

def pretty_time_record (tr, sdate, user) :
    tr_pr = ["%(user)s, %(sdate)s" % locals ()]
    if tr.start :
        tr_pr.append ("%s-%s" % (tr.start, tr.end))
    else :
        tr_pr.append ("%sh" % tr.duration)
    return ' '.join (tr_pr)
# end def pretty_time_record

def time_records_consistent (db, cl, nodeid) :
    """ Check if all time records for this daily record are consistent

        + check that each record contains a wp
        + check that a start_time exists unless durations_allowed
        + check that there are no overlapping work hours
          - get all records with a start time
          - sort by start time
          - check pairwise for overlap
        + check that sum of work-time does not exceed 10 hours -- if user
          may not work more than 10 hours
        + check that there is a lunch break of at least .5 hours if user
          worked for more than 6 hours and durations_allowed is not
          specified
    """
    date  = cl.get (nodeid, 'date')
    sdate = date.pretty ('%Y-%m-%d')
    uid   = cl.get (nodeid, 'user')
    uname = db.user.get (uid, 'username')
    msgs  = []
    dynamic = get_user_dynamic (db, uid, date)
    if not dynamic :
        raise Reject, "No dynamic user data for %(uname)s, %(date)s" % locals ()
    trec = \
        [db.time_record.getnode (i) for i in db.time_record.filter
         (None, dict (daily_record = nodeid), sort = ('+', 'start'))
        ]
    nonempty = []
    for tr in trec :
        tr_pr = pretty_time_record (tr, date, uname)
        if not tr.wp :
            msgs.append ("%(tr_pr)s: No work package" % locals ())
            durations_allowed = dynamic.durations_allowed
        else :
            durations_allowed = \
                (  dynamic.durations_allowed
                or db.time_wp.get (tr.wp, 'durations_allowed')
                )
        if not durations_allowed and not tr.start :
            msgs.append ("%(tr_pr)s: No durations allowed" % locals ())
        if tr.start :
            nonempty.append (tr)
    for i in range (len (nonempty) - 1) :
        tr    = (nonempty [i], nonempty [i + 1])
        start = [t.start for t in tr]
        end   = [t.end   for t in tr]
        tr_pr = ', '.join ([pretty_time_record (t, date, uname) for t in tr])
        if not (start [0] >= end [1] or start [1] >= end [0]) :
            msgs.append ("%(tr_pr)s overlap" % locals ())
    tr_pr = "%s, %s:" % (uname, sdate)
    if not dynamic.long_worktime :
        work = reduce (add, [t.duration for t in trec], 0)
        if work > 10 :
            msgs.append \
                ("%(tr_pr)s Overall work-time more than 10 hours: %s" % work)
    if not dynamic.durations_allowed :
        nobreak  = 0
        last_end = None
        for tr in nonempty :
            start   = Date (tr.start, offset = 0)
            if last_end and (start - last_end).as_seconds () >= 30 * 60 :
                nobreak  = tr.duration
            else :
                nobreak += tr.duration
            last_end = Date (tr.end,  offset = 0)
            if nobreak > 6 :
                msgs.append \
                    ("%(tr_pr)s More than 6 hours "
                     "without a break of at least half an hour"
                    % locals ()
                    )
                break

    if msgs :
        msgs.sort ()
        raise Reject, '\n'.join ([_ (i) for i in msgs])
    return True
# end def time_records_consistent

def check_daily_record (db, cl, nodeid, new_values) :
    """ Check that status changes are OK. Allowed changes:

         - From open to submitted by user or by HR
         - From submitted to accepted by supervisor or by HR
         - From submitted to open     by supervisor or by HR
         - From accepted  to open     by HR
    """
    for i in 'user', 'date' :
        if i in new_values :
            raise Reject, _ ("%(attr)s may not be changed") % {'attr' : _ (i)}
    if i in ('status',) :
        if i in new_values and not new_values [i] :
            raise Reject, _ ("%(attr)s must be set") % {'attr' : _ (i)}
    user       = cl.get (nodeid, 'user')
    uid        = db.getuid ()
    is_hr      = user_has_role (db, uid, 'hr')
    old_status = cl.get (nodeid, 'status')
    status     = new_values.get ('status', old_status)
    supervisor = db.user.get (user, 'supervisor')
    if supervisor : # if no supervisor nobody can do it
        clearance  = db.user.get (supervisor, 'clearance_by') or supervisor
        clearers   = [db.user.get (clearance, 'substitute')]
        if not db.user.get (clearance, 'subst_active') :
            clearers = []
        clearers.append (clearance)
        may_give_clearance = uid in clearers
    else :
        may_give_clearance = False

    old_status, status = \
        [db.daily_record_status.get (i, 'name') for i in [old_status, status]]
    if status != old_status :
        if not (  (   status == 'submitted' and old_status == 'open'
                  and (is_hr or user == uid)
                  and time_records_consistent (db, cl, nodeid)
                  )
               or (   status == 'accepted'  and old_status == 'submitted'
                  and (is_hr or may_give_clearance)
                  )
               or (   status == 'open'      and old_status == 'submitted'
                  and (is_hr or user == uid or may_give_clearance)
                  )
               or (   status == 'open'      and old_status == 'accepted'
                  and is_hr
                  )
               ) :
            raise Reject, \
                ( _ ("Denied state change: %(old_status)s->%(status)s")
                % locals ()
                )
# end def check_daily_record

def update_timerecs (db, time_record_id, set_it) :
    """ Update list of time_records with the given time_record_id
        if do_reset is specified, we *remove* the given id from the
        list, otherwise we *add* it.
    """
    id      = int (time_record_id)
    drec_id = db.time_record.get (time_record_id, 'daily_record')
    trecs_o = [int (i) for i in db.daily_record.get (drec_id, 'time_record')]
    trecs   = dict ([(i, 1) for i in trecs_o])
    if set_it :
        trecs [id] = 1
    else :
        del trecs [id]
    trecs   = trecs.keys ()
    trecs.sort ()
    if trecs != trecs_o :
        db.daily_record.set (drec_id, time_record = [str (i) for i in trecs])
# end def update_timerecs

def update_time_record_in_daily_record (db, cl, nodeid, old_values) :
    update_timerecs (db, nodeid, True)
# end def update_time_record_in_daily_record

def new_daily_record (db, cl, nodeid, new_values) :
    """
        Only create a daily_record if a user_dynamic record exists for
        the user.
        If a new daily_record is created, we check the date provided:
        If hours, minutes, seconds are all zero we think the time was
        entered in UTC and do no conversion. If one is non-zero, we get
        the timezone from the user information and re-encode the date as
        UTC -- this effectively makes the date a 'naive' date. Then we
        nullify hour, minute, second of the date.
        After that, we check that there is no duplicate daily_record
        with the same date for this user.
    """
    uid = db.getuid ()
    for i in 'user', 'date' :
        if i not in new_values :
            raise Reject, _ ("%(attr)s must be specified") % {'attr' : _ (i)}
    user = new_values ['user']
    if  (   uid != user
        and not user_has_role (db, uid, 'controlling')
        and not user_has_role (db, uid, 'admin')
        ) :
        raise Reject, _ ("Only user and Controlling may create daily records")
    for i in 'time_record', :
        if i in new_values :
            raise Reject, _ ("%(attr)s must not be specified") % {'attr': _ (i)}
    # the following is allowed for the admin (import!)
    for i in 'status', :
        if i in new_values and uid != '1' :
            raise Reject, _ ("%(attr)s must not be specified") % {'attr': _ (i)}
    date = new_values ['date']
    date.hour = date.minute = date.second = 0
    new_values ['date'] = date
    if not get_user_dynamic (db, user, date) and uid != '1' :
        raise Reject, \
            _ ("No dynamic user data for %(user)s, %(date)s") % locals ()
    if db.daily_record.filter \
        (None, {'date' : str (date.local (0)), 'user' : user}) :
        raise Reject, _ ("Duplicate record: date = %(date)s, user = %(user)s") \
            % new_values
    new_values ['time_record'] = []
    if 'status' not in new_values :
        new_values ['status']  = db.daily_record_status.lookup ('open')
# end def new_daily_record

def check_start_end_duration \
    (date, start, end, duration, new_values, split = 0) :
    """
        either duration or both start/end must be set but not both
        of duration/end
        set duration from start/end if duration empty
        set end from start/duration if end empty
        Note: We are using naive times (with timezone 0) here, this
        means we can safely use date.pretty for converting back to
        string.
    """
    dstart = dend = None
    if split :
        check_duration (split)
    if 'end' in new_values :
        if not start :
            raise Reject, _ ("%(attr)s must be specified") % {'attr' : 'start'}
        if 'duration' in new_values :
            raise Reject, _ ("Either specify duration or start/end")
        dstart = Date (start, offset = 0)
        dend   = Date (end,   offset = 0)
        check_timestamps (dstart, dend, date)
        duration                = (dend - dstart).as_seconds () / 3600.
        new_values ['duration'] = duration
        new_values ['start']    = dstart.pretty (hour_format)
        new_values ['end']      = dend.pretty   (hour_format)
    else :
        if not duration and duration != 0 :
            raise Reject, _ ("Either specify duration or start/end")
        check_duration (duration)
        if 'duration' in new_values :
            new_values ['duration'] = duration
        if start :
            dstart  = Date (start, offset = 0)
            if 'start' in new_values or 'duration' in new_values :
                minutes = duration * 60
                hours   = int (duration % 60)
                minutes = minutes - hours * 60
                dend    = dstart + Interval ('%d:%d' % (hours, minutes))
                check_timestamps (dstart, dend, date)
                new_values ['start'] = dstart.pretty (hour_format)
                new_values ['end']   = dend.pretty   (hour_format)
    if split :
        if duration <= split :
            raise Reject, _ ("Split must be < duration")
        duration -= split
        if start :
            hours   = int (split)
            minutes = (split - hours) * 60
            dstart  = dstart + Interval ('%d:%d' % (hours, minutes))
            new_values ['start'] = dstart.pretty (hour_format)
        del new_values ['split']
        new_values ['duration']  = duration
    return dstart, dend
# end def check_start_end_duration

def correct_work_location (db, wp, new_values) :
    project_id    = db.time_wp.get      (wp,         'project')
    work_location = db.time_project.get (project_id, 'work_location')
    if work_location :
        new_values ['work_location'] = work_location
# end def correct_work_location

def new_time_record (db, cl, nodeid, new_values) :
    """ auditor on time_record
    """
    uid = db.getuid ()
    for i in 'daily_record', :
        if i not in new_values :
            raise Reject, _ ("%(attr)s must be specified") % {'attr' : _ (i)}
    for i in 'split', :
        if i in new_values :
            raise Reject, _ ("%(attr)s must not be specified") % {'attr': _ (i)}
    dr       = db.daily_record.getnode (new_values ['daily_record'])
    if dr.status != db.daily_record_status.lookup ('open') and uid != '1' :
        raise Reject, _ ('Editing of time records only for status "open"')
    if  (   uid != dr.user
        and not user_has_role (db, uid, 'controlling')
        and not user_has_role (db, uid, 'admin')
        ) :
        raise Reject, _ ("Only user and Controlling may create time records")
    dynamic  = get_user_dynamic (db, dr.user, dr.date)
    if not dynamic :
        if uid != '1' :
            raise Reject, \
                _ ("No dynamic user data for %(user)s, %(date)s") % locals ()
    else :
        if not dynamic.weekend_allowed and uid != '1' :
            wday = gmtime (dr.date.timestamp ())[6]
            if wday in (5, 6) :
                raise Reject, _ ('No weekend booking allowed')
    start    = new_values.get ('start',    None)
    end      = new_values.get ('end',      None)
    duration = new_values.get ('duration', None)
    dstart, dend = check_start_end_duration \
        (dr.date, start, end, duration, new_values)
    if 'duration' in new_values and new_values ['duration'] == 0 :
        raise Reject, _ ('Duration must be non-zero for new time record')
    if 'work_location' not in new_values :
        new_values ['work_location'] = '1'
    if 'wp' in new_values :
        correct_work_location (db, new_values ['wp'], new_values)
    duration = new_values.get ('duration', None)
    ls       = Date (db.user.get (dr.user, 'lunch_start'))
    ls.year  = dr.date.year
    ls.month = dr.date.month
    ls.day   = dr.date.day
    ld       = db.user.get (dr.user, 'lunch_duration')
    hours    = int (ld)
    minutes  = (ld - hours) * 60
    le       = ls + Interval ('%d:%d' % (hours, minutes))
    print duration, ls, ld, hours, minutes, le, start, dstart, dend
    if duration > 6 and start and dstart < ls and dend > ls :
        newrec  = { 'daily_record' : new_values ['daily_record']
                  , 'start'        : le.pretty (hour_format) 
                  }
        
        dur1    = (ls - dstart).as_seconds () / 3600.
        dur2    = duration - dur1
        if end :
            dur2 -= ld
        newrec ['duration']     = dur2
        new_values ['end']      = ls.pretty (hour_format)
        new_values ['duration'] = dur1
        if dur2 > 0 :
            db.time_record.create (** newrec)
# end def new_time_record

def check_time_record (db, cl, nodeid, new_values) :
    for i in 'daily_record', :
        if i in new_values :
            raise Reject, _ ("%(attr)s may not be changed") % {'attr' : _ (i)}
    status   = db.daily_record.get (cl.get (nodeid, 'daily_record'), 'status')
    if status != db.daily_record_status.lookup ('open') :
        raise Reject, _ ('Editing of time records only for status "open"')
    drec     = new_values.get ('daily_record', cl.get (nodeid, 'daily_record'))
    start    = new_values.get ('start',        cl.get (nodeid, 'start'))
    end      = new_values.get ('end',          cl.get (nodeid, 'end'))
    duration = new_values.get ('duration',     cl.get (nodeid, 'duration'))
    split    = new_values.get ('split',        cl.get (nodeid, 'split'))
    wp       = new_values.get ('wp',           cl.get (nodeid, 'wp'))
    date     = db.daily_record.get (drec, 'date')
    wl       = 'work_location'
    ta       = 'time_activity'
    location = new_values.get (wl,             cl.get (nodeid, wl))
    activity = new_values.get (ta,             cl.get (nodeid, ta))
    check_start_end_duration \
        (date, start, end, duration, new_values, split = split)
    if not location :
        new_values ['work_location'] = '1'
    if split :
        if 'wp' in new_values :
            del new_values ['wp']
            wp = cl.get (nodeid, 'wp')
        newrec = dict \
            ( daily_record  = cl.get (nodeid, 'daily_record')
            , duration      = split
            , wp            = wp
            , time_activity = activity
            , work_location = location
            )
        if (start) :
            newrec ['start'] = start
        cl.create (** newrec)
    if wp :
        correct_work_location (db, wp, new_values)
# end def check_time_record

def check_for_retire (db, cl, nodeid, old_values) :
    if cl.get (nodeid, 'duration') == 0 :
        cl.retire (nodeid)
# end def check_for_retire

def check_retire (db, cl, nodeid, dummy) :
    """ remove ourselves from the daily record """
    update_timerecs (db, nodeid, False)
# end def check_retire

def init (db) :
    import sys, os
    global _, get_user_dynamic, user_has_role
    sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
    user_dynamic     = __import__ ('user_dynamic', globals (), locals ())
    get_user_dynamic = user_dynamic.get_user_dynamic
    common           = __import__ ('common', globals (), locals ())
    user_has_role    = common.user_has_role
    del (sys.path [0])
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.time_record.audit  ("create", new_time_record)
    db.time_record.audit  ("set",    check_time_record)
    db.time_record.react  ("create", update_time_record_in_daily_record)
    db.time_record.react  ("set",    check_for_retire)
    db.time_record.react  ("retire", check_retire)
    db.daily_record.audit ("create", new_daily_record)
    db.daily_record.audit ("set",    check_daily_record)
# end def init

### __END__ time_record
