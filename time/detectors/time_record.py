#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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

import common
from user_dynamic                   import get_user_dynamic, day_work_hours
from freeze                         import frozen

def check_timestamps (start, end, date) :
    start.year  = end.year  = date.year
    start.month = end.month = date.month
    start.day   = end.day   = date.day
    if start > end :
        raise Reject, _ ("start and end must be on same day and start <= end.")
    if start.timestamp () % 900 or end.timestamp () % 900 :
        raise Reject, _ ("Times must be given in quarters of an hour")
# end def check_timestamp

def check_duration (d, max = 0) :
    if d < 0 :
        raise Reject, _ ("No negative times are allowed")
    if (d * 3600) % 900 :
        raise Reject, _ ("Times must be given in quarters of an hour")
    if max and d > max :
        raise Reject, _ ("Duration must not exceed %s hours" % max)
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
        + Travel times (either wp has travel flag or time_activity has
          travel flag) are excempt from work-time and lunch break checks
        + no_overtime flag in time_project: check if really no overtime
          booked
    """
    date     = cl.get (nodeid, 'date')
    sdate    = date.pretty (common.ymd)
    uid      = cl.get (nodeid, 'user')
    uname    = db.user.get (uid, 'username')
    msgs     = []
    dynamic  = get_user_dynamic (db, uid, date)
    if not dynamic :
        raise Reject, "No dynamic user data for %(uname)s, %(date)s" % locals ()
    if not dynamic.booking_allowed :
        raise Reject, "Booking not allowed for %(uname)s, %(date)s" % locals ()
    trec     = \
        [db.time_record.getnode (i) for i in db.time_record.filter
         (None, dict (daily_record = nodeid), sort = ('+', 'start'))
        ]
    trec_notravel   = []
    need_break_recs = []
    noover_sum      = 0
    daily_hours     = day_work_hours (dynamic, date)
    for tr in trec :
        tr_pr  = pretty_time_record (tr, date, uname)
        act    = tr.time_activity
        wp     = tr.wp
        travel = \
            (  act and db.time_activity.get (act, 'travel')
            or wp  and db.time_wp.get       (wp,  'travel')
            )
        if not travel :
            trec_notravel.append (tr)
        if not tr.wp :
            msgs.append ("%(tr_pr)s: No work package" % locals ())
            durations_allowed = dynamic.durations_allowed
        else :
            durations_allowed = \
                (  dynamic.durations_allowed
                or db.time_wp.get (tr.wp, 'durations_allowed')
                )
            pr        = db.time_wp.get      (tr.wp, 'project')
            max_hours = db.time_project.get (pr,    'max_hours')
            no_over   = db.time_project.get (pr,    'no_overtime')
            if max_hours is not None :
                if tr.duration > max_hours :
                    msgs.append \
                        ( "%(tr_pr)s: Duration must not exceed %(max_hours)s"
                        % locals ()
                        )
            if no_over :
                noover_sum += tr.duration
                if tr.duration > daily_hours :
                    msgs.append \
                        ( "%(tr_pr)s: Duration must not exceed %(daily_hours)s"
                        % locals ()
                        )
        if not durations_allowed and not tr.start :
            msgs.append ("%(tr_pr)s: No durations allowed" % locals ())
        if tr.start and not travel :
            need_break_recs.append (tr)
    for i in range (len (need_break_recs) - 1) :
        tr    = (need_break_recs [i], need_break_recs [i + 1])
        start = [t.start for t in tr]
        end   = [t.end   for t in tr]
        tr_pr = ', '.join ([pretty_time_record (t, date, uname) for t in tr])
        if not (start [0] >= end [1] or start [1] >= end [0]) :
            msgs.append ("%(tr_pr)s overlap" % locals ())
    tr_pr = "%s, %s:" % (uname, sdate)
    if noover_sum > daily_hours :
        msgs.append \
            ( "%(tr_pr)s Sum of no-overtime WPs must not exceed %(daily_hours)s"
            % locals ()
            )
    if dynamic.daily_worktime :
        work = reduce (add, [t.duration for t in trec_notravel], 0)
        if work > dynamic.daily_worktime :
            dwt = dynamic.daily_worktime
            msgs.append \
                ( "%(tr_pr)s Work-time more than %(dwt)s hours: %(work)s"
                % locals ()
                )
    if not dynamic.durations_allowed :
        nobreak  = 0
        last_end = None
        for tr in need_break_recs :
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
           but don't allow accepting own records
         - From submitted to open     by supervisor or by HR or by user
         - From accepted  to open     by HR
    """
    for i in 'user', 'date' :
        if i in new_values and db.getuid () != '1' :
            raise Reject, _ ("%(attr)s may not be changed") % {'attr' : _ (i)}
    if i in ('status',) :
        if i in new_values and not new_values [i] :
            raise Reject, _ ("%(attr)s must be set") % {'attr' : _ (i)}
    user       = cl.get (nodeid, 'user')
    date       = cl.get (nodeid, 'date')
    if frozen (db, user, date) and new_values.keys () != ['tr_duration_ok'] :
        uname = db.user.get (user, 'username')
        raise Reject, _ ("Frozen: %(uname)s, %(date)s") % locals ()
    uid        = db.getuid ()
    is_hr      = common.user_has_role (db, uid, 'hr')
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
                  and user != uid
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
        db.daily_record.set (drec_id, tr_duration_ok = 0)
        db.daily_record.set \
            ( drec_id
            , time_record    = [str (i) for i in trecs]
            , tr_duration_ok = None
            )
        dr = db.daily_record.getnode (drec_id)
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
    common.require_attributes (_, cl, nodeid, new_values, 'user', 'date')
    user  = new_values ['user']
    uname = db.user.get (user, 'username')
    if  (   uid != user
        and not common.user_has_role (db, uid, 'controlling')
        and not common.user_has_role (db, uid, 'admin')
        ) :
        raise Reject, _ ("Only user and Controlling may create daily records")
    common.reject_attributes (_, new_values, 'time_record')
    # the following is allowed for the admin (import!)
    if uid != '1' :
        common.reject_attributes (_, new_values, 'status')
    date = new_values ['date']
    date.hour = date.minute = date.second = 0
    new_values ['date'] = date
    dyn  = get_user_dynamic (db, user, date)
    if not dyn and uid != '1' :
        raise Reject, \
            _ ("No dynamic user data for %(uname)s, %(date)s") % locals ()
    if uid != '1' and not dyn.booking_allowed :
        raise Reject, _ \
            ("Booking not allowed for %(uname)s, %(date)s") % locals ()
    if frozen (db, user, date) :
        raise Reject, _ ("Frozen: %(uname)s, %(date)s") % locals ()
    if db.daily_record.filter \
        (None, {'date' : date.pretty ('%Y-%m-%d'), 'user' : user}) :
        raise Reject, _ ("Duplicate record: date = %(date)s, user = %(user)s") \
            % new_values
    new_values ['time_record'] = []
    if 'status' not in new_values :
        new_values ['status']  = db.daily_record_status.lookup ('open')
    new_values ['tr_duration_ok'] = None
# end def new_daily_record

def check_start_end_duration \
    (date, start, end, duration, new_values, dist = 0) :
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
    if dist :
        check_duration (dist)
    if start and ":" not in start :
        start = start + ":00"
    if end   and ":" not in end :
        end   = end   + ":00"
    if 'end' in new_values :
        if not start :
            attr = _ ('start')
            raise Reject, _ (''"%(attr)s must be specified") % locals ()
        if 'duration' in new_values :
            raise Reject, _ (''"Either specify duration or start/end")
        dstart = Date (start, offset = 0)
        dend   = Date (end,   offset = 0)
        check_timestamps (dstart, dend, date)
        duration                = (dend - dstart).as_seconds () / 3600.
        new_values ['duration'] = duration
        new_values ['start']    = dstart.pretty (hour_format)
        new_values ['end']      = dend.pretty   (hour_format)
    else :
        if not duration and duration != 0 :
            raise Reject, \
                ( _ ("%(date)s: You specified new values "
                     "for %(attr)s but no duration"
                    )
                % dict ( date = date.pretty (common.ymd)
                       , attr = ", ".join ([_ (i) for i in new_values.keys ()])
                       )
                )
        check_duration (duration, 24)
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
    if dist and dist < duration :
        duration -= dist
        if start :
            hours   = int (dist)
            minutes = (dist - hours) * 60
            dstart  = dstart + Interval ('%d:%d' % (hours, minutes))
            new_values ['start'] = dstart.pretty (hour_format)
        new_values ['duration']  = duration
    return dstart, dend
# end def check_start_end_duration

def correct_work_location (db, wp, new_values) :
    project_id    = db.time_wp.get      (wp,         'project')
    work_location = db.time_project.get (project_id, 'work_location')
    if work_location :
        new_values ['work_location'] = work_location
# end def correct_work_location

def check_generated (new_values) :
    if 'start' in new_values and 'start_generated' not in new_values :
        new_values ['start_generated'] = False
    if (   (  'start'    in new_values
           or 'end'      in new_values
           or 'duration' in new_values
           )
       and 'end_generated' not in new_values
       ) :
        new_values   ['end_generated'] = False
# end def check_generated

def new_time_record (db, cl, nodeid, new_values) :
    """ auditor on time_record
    """
    uid    = db.getuid ()
    travel = False
    common.require_attributes (_, cl, nodeid, new_values, 'daily_record')
    common.reject_attributes  (_, new_values, 'dist', 'tr_duration')
    check_generated (new_values)
    dr       = db.daily_record.getnode (new_values ['daily_record'])
    uname    = db.user.get (dr.user, 'username')
    if (dr.status != db.daily_record_status.lookup ('open') and uid != '1') :
        raise Reject, _ ('Editing of time records only for status "open"')
    if frozen (db, dr.user, dr.date) :
        date = dr.date
        raise Reject, _ ("Frozen: %(uname)s, %(date)s") % locals ()
    if  (   uid != dr.user
        and not common.user_has_role (db, uid, 'controlling')
        and not common.user_has_role (db, uid, 'admin')
        ) :
        raise Reject, _ \
            ( ("Only %(uname)s and Controlling may create time records")
            % locals ()
            )
    dynamic  = get_user_dynamic (db, dr.user, dr.date)
    date     = dr.date.pretty (common.ymd)
    if not dynamic :
        if uid != '1' :
            raise Reject, _ \
                ("No dynamic user data for %(uname)s, %(date)s") % locals ()
    else :
        if not dynamic.booking_allowed and uid != '1' :
            raise Reject, _ \
                ("Booking not allowed for %(uname)s, %(date)s") % locals ()
        if not (dr.weekend_allowed or dynamic.weekend_allowed) and uid != '1' :
            wday = gmtime (dr.date.timestamp ())[6]
            if wday in (5, 6) :
                raise Reject, _ ('No weekend booking allowed')
    start    = new_values.get ('start',    None)
    end      = new_values.get ('end',      None)
    duration = new_values.get ('duration', None)
    dstart, dend = check_start_end_duration \
        (dr.date, start, end, duration, new_values)
    if 'work_location' not in new_values :
        new_values ['work_location'] = '1'
    if 'wp' in new_values and new_values ['wp'] :
        wp = new_values ['wp']
        correct_work_location (db, wp, new_values)
        travel = travel or db.time_wp.get (wp, 'travel')
    if 'time_activity' in new_values and new_values ['time_activity'] :
        act    = new_values ['time_activity']
        travel = travel or db.time_activity.get (act, 'travel')
    duration = new_values.get ('duration', None)
    ls       = Date (db.user.get (dr.user, 'lunch_start') or '12:00')
    ls.year  = dr.date.year
    ls.month = dr.date.month
    ls.day   = dr.date.day
    ld       = db.user.get (dr.user, 'lunch_duration') or 1
    hours    = int (ld)
    minutes  = (ld - hours) * 60
    le       = ls + Interval ('%d:%d' % (hours, minutes))
    if not travel and duration > 6 and start and dstart < ls and dend > ls :
        newrec  = { 'daily_record' : new_values ['daily_record']
                  , 'start'        : le.pretty (hour_format)
                  }

        dur1    = (ls - dstart).as_seconds () / 3600.
        dur2    = duration - dur1
        if end :
            dur2 -= ld
        newrec ['duration']     = dur2
        for attr in 'wp', 'time_activity', 'work_location' :
            if attr in new_values and new_values [attr] :
                newrec [attr] = new_values [attr]
        new_values ['end']      = ls.pretty (hour_format)
        new_values ['duration'] = dur1
        if dur2 > 0 :
            db.time_record.create (** newrec)
# end def new_time_record

def check_time_record (db, cl, nodeid, new_values) :
    for i in 'daily_record', :
        if i in new_values :
            raise Reject, _ ("%(attr)s may not be changed") % {'attr' : _ (i)}
    drec     = new_values.get ('daily_record', cl.get (nodeid, 'daily_record'))
    dr       = db.daily_record.getnode (drec)
    date     = dr.date
    user     = dr.user
    if  (   frozen (db, user, date)
        and new_values.keys () != ['tr_duration']
        ) :
        uname = db.user.get (user, 'username')
        raise Reject, _ ("Frozen: %(uname)s, %(date)s") % locals ()
    status   = db.daily_record.get (cl.get (nodeid, 'daily_record'), 'status')
    if  (   status != db.daily_record_status.lookup ('open')
        and new_values.keys () != ['tr_duration']
        and db.getuid () != '1'
        ) :
        raise Reject, _ ('Editing of time records only for status "open"')
    # allow empty duration to delete record
    if 'duration' in new_values and new_values ['duration'] is None :
        return
    check_generated (new_values)
    start    = new_values.get ('start',        cl.get (nodeid, 'start'))
    end      = new_values.get ('end',          cl.get (nodeid, 'end'))
    duration = new_values.get ('duration',     cl.get (nodeid, 'duration'))
    dist     = new_values.get ('dist',         cl.get (nodeid, 'dist'))
    wp       = new_values.get ('wp',           cl.get (nodeid, 'wp'))
    wl       = 'work_location'
    ta       = 'time_activity'
    location = new_values.get (wl,             cl.get (nodeid, wl))
    activity = new_values.get (ta,             cl.get (nodeid, ta))
    comment  = new_values.get ('comment',      cl.get (nodeid, 'comment'))
    check_start_end_duration \
        (date, start, end, duration, new_values, dist = dist)
    if not location :
        new_values ['work_location'] = '1'
    if dist and not wp :
        raise Reject, _ ("Distribution: WP must be given")
    if dist :
        if dist < duration :
            newrec = dict \
                ( daily_record  = drec
                , duration      = dist
                , wp            = wp
                , time_activity = activity
                , work_location = location
                )
            if comment :
                newrec ['comment'] = comment
            start_generated = new_values.get \
                ('start_generated', cl.get (nodeid, 'start_generated'))
            if (start) :
                newrec     ['start']           = start
                newrec     ['end_generated']   = True
                newrec     ['start_generated'] = start_generated
                new_values ['start_generated'] = True
            cl.create (** newrec)
            for attr in 'wp', 'time_activity', 'work_location', 'comment' :
                if attr in new_values :
                    del new_values [attr]
            wp = cl.get (nodeid, 'wp')
        elif dist == duration :
            # Nothing to do -- just set new wp
            pass
        else :
            dist -= duration
            wstart, wend = common.week_from_date (date)
            dsearch = common.pretty_range (date, wend)
            drs = db.daily_record.filter \
                (None, dict (user = user, date = dsearch))
            trs = db.time_record.filter  \
                (None, {'daily_record' : drs})
            trs = [db.time_record.getnode (t) for t in trs]
            trs = [t for t in trs
                   if  (   not t.wp
                       and t.id != nodeid
                       and (   t.daily_record != drec
                           or (  start and t.start > start
                              or not start
                              )
                           )
                       )
                  ]
            trs = [(db.daily_record.get (tr.daily_record, 'date'), tr.start, tr)
                   for tr in trs
                  ]
            trs.sort ()
            trs = [tr [2] for tr in trs]
            sum = reduce (add, [t.duration for t in trs], 0)
            if sum < dist :
                raise Reject, _ \
                    ("dist must not exceed sum of unassigned times in week")
            for tr in trs :
                if tr.duration <= dist :
                    dist -= tr.duration
                    db.time_record.set \
                        ( tr.id
                        , wp            = wp
                        , time_activity = activity
                        , work_location = location
                        )
                else :
                    param = dict (duration = tr.duration - dist)
                    newrec = dict \
                        ( daily_record  = tr.daily_record
                        , duration      = dist
                        , wp            = wp
                        , time_activity = activity
                        , work_location = location
                        )
                    if tr.start :
                        param ['start_generated'] = True
                        dstart  = Date (tr.start)
                        hours   = int (dist)
                        minutes = (dist - hours) * 60
                        dstart += Interval ('%d:%d' % (hours, minutes))
                        param ['start'] = dstart.pretty (hour_format)
                        newrec ['start']           = tr.start
                        newrec ['end_generated']   = True
                    cl.create          (** newrec)
                    # warning side-effect, calling set will change
                    # values in current tr!
                    db.time_record.set (tr.id, **param)
                    dist = 0
                if not dist :
                    break
            assert (dist == 0)
        del new_values ['dist']
    if wp :
        correct_work_location (db, wp, new_values)
    if 'tr_duration' not in new_values :
        new_values ['tr_duration'] = None
# end def check_time_record

def check_for_retire_and_duration (db, cl, nodeid, old_values) :
    if cl.get (nodeid, 'duration') is None :
        cl.retire (nodeid)
    elif common.changed_values (old_values, cl, nodeid) != ['tr_duration'] :
        drid = cl.get (nodeid, 'daily_record')
        db.daily_record.set (drid, tr_duration_ok = 0)
        db.daily_record.set (drid, tr_duration_ok = None)
# end def check_for_retire_and_duration

def check_retire (db, cl, nodeid, dummy) :
    """ remove ourselves from the daily record """
    update_timerecs (db, nodeid, False)
# end def check_retire

def send_mail_on_deny (db, cl, nodeid, old_values) :
    """If daily record is denied, send message to user."""

    my_uid    = db.getuid ()
    other_uid = cl.get (nodeid, "user")
    if my_uid == other_uid :
        return ### user reopened himself

    dr_status     = db.getclass ("daily_record_status")
    old_status    = old_values ["status"]
    new_status    = cl.get (nodeid, "status")
    s_sub, s_open = [dr_status.lookup (s) for s in ("submitted", "open")]

    if (old_status, new_status) == (s_sub, s_open) :
        mailer  = roundupdb.Mailer (db.config)
        date    = cl.get (nodeid, "date").pretty (common.ymd)
        superv  = db.user.get (my_uid, "username")
        email   = db.user.get (other_uid, "address")
        subject = "Daily record denied for %(date)s by %(superv)s" % locals ()
        content = \
            ( "Your daily record for %(date)s has been denied.\n"
              "Please contact %(superv)s for details, then submit again.\n"
            % locals ()
            )
        try :
            mailer.standard_message ((email,), subject, content)
        except roundupdb.MessageSendError, message :
            raise roundupdb.DetectorError, message
# end def send_mail_on_deny


def init (db) :
    if 'time_record' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.time_record.audit  ("create", new_time_record)
    db.time_record.audit  ("set",    check_time_record)
    db.time_record.react  ("create", update_time_record_in_daily_record)
    db.time_record.react  ("set",    check_for_retire_and_duration)
    db.time_record.react  ("retire", check_retire)
    db.daily_record.audit ("create", new_daily_record)
    db.daily_record.audit ("set",    check_daily_record)
    db.daily_record.react ("set",    send_mail_on_deny)
# end def init

### __END__ time_record
