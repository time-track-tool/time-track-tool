#! /usr/bin/python
# Copyright (C) 2006-22 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#--
#

from roundup                        import roundupdb, hyperdb
from roundup.exceptions             import Reject
from roundup.date                   import Date, Interval
from operator                       import add
from time                           import gmtime

from freeze                         import frozen

import json
import common
import user_dynamic
import vacation

hour_format = '%H:%M'

def check_timestamps (_, start, end, date) :
    t = end
    if end == '24:00' :
        t = '00:00'
    dstart = Date (start, offset = 0)
    dend   = Date (t,     offset = 0)
    dstart.year  = dend.year  = date.year
    dstart.month = dend.month = date.month
    dstart.day   = dend.day   = date.day
    if end == '24:00' :
        dend += common.day
        dend.hours = dend.seconds = dend.minutes = 0
    if dstart > dend :
        raise Reject (_ ("start and end must be on same day and start <= end."))
    if dstart.timestamp () % 900 or dend.timestamp () % 900 :
        raise Reject (_ ("Times must be given in quarters of an hour"))
    dur = (dend - dstart).as_seconds () / 3600.
    ep  = dend.pretty (hour_format)
    if end == '24:00' :
        assert ep == '00:00'
        ep = end
    return dstart, dend, dstart.pretty (hour_format), ep, dur
# end def check_timestamps

def check_duration (_, d, max = 0) :
    if d is None :
        raise Reject (_ ("Duration (or Start/End) must be given"))
    if d < 0 :
        raise Reject (_ ("No negative times are allowed"))
    if (d * 3600) % 900 :
        raise Reject (_ ("Times must be given in quarters of an hour"))
    if max and d > max :
        raise Reject (_ ("Duration must not exceed %s hours" % max))
# end def check_duration

def pretty_att_record (db, dr, ar) :
    _     = db.i18n.gettext
    sdate = dr.date.pretty (common.ymd)
    user  = db.user.get (dr.user, 'username')
    ar_pr = ["%(user)s, %(sdate)s" % locals ()]
    if ar.start :
        ar_pr.append ("%s-%s" % (ar.start, ar.end))
    else :
        wl = db.work_location.getnode (ar.work_location)
        ar_pr.append ("%s: %s" % (_ ('work_location'), wl.code))
    return ' '.join (ar_pr)
# end def pretty_att_record

def pretty_time_record (db, dr, tr) :
    sdate = dr.date.pretty (common.ymd)
    user  = db.user.get (dr.user, 'username')
    tr_pr = ["%(user)s, %(sdate)s" % locals ()]
    tr_pr.append ("%sh" % tr.duration)
    return ' '.join (tr_pr)
# end def pretty_time_record

def get_and_check_dyn (db, dr) :
    dynamic = user_dynamic.get_user_dynamic (db, dr.user, dr.date)
    uname   = db.user.get (dr.user, 'username')
    date    = dr.date
    if not dynamic :
        raise Reject \
            ("No dynamic user data for %(uname)s, %(date)s" % locals ())
    if not dynamic.booking_allowed :
        raise Reject ("Booking not allowed for %(uname)s, %(date)s" % locals ())
    return dynamic
# end def get_and_check_dyn

def att_records_consistent (db, dr) :
    """ Check if all attendance records for this daily record are consistent
        Performed when dr.status changes open->submitted
        + check that each record contains a work_location
        + check that a start_time exists unless durations_allowed
          -> only done if there is a time_record link?
        + check that there are no overlapping work hours
          - get all records with a start time
          - sort by start time
          - check pairwise for overlap
        + check that there is a lunch break of at least .5 hours if user
          worked for more than 6 hours and durations_allowed is not
          specified
        + Travel times (if time_activity has travel flag) are excempt
          from lunch break checks
    """
    _        = db.i18n.gettext
    msgs     = []
    uname    = db.user.get (dr.user, 'username')
    dyn      = get_and_check_dyn (db, dr)
    arec     = [db.attendance_record.getnode (i) for i in dr.attendance_record]
    last_ar  = None
    need_break_recs = []
    for ar in sorted (arec, key = lambda a: a.start) :
        ar_pr  = pretty_att_record (db, dr, ar)
        wl     = None
        if ar.work_location :
            wl = db.work_location.getnode (ar.work_location)
        if not ar.work_location :
            msgs.append ("%(ar_pr)s: No work location" % locals ())
        durations_allowed = dyn.durations_allowed
        if wl and wl.durations_allowed :
            durations_allowed = True
        if not durations_allowed and not ar.start :
            msgs.append ("%(ar_pr)s: Need Start/End" % locals ())
        if ar.start and wl and not wl.travel :
            need_break_recs.append (ar)
        if last_ar and last_ar.start :
            ars = [last_ar, ar]
            start = [a.start for a in ars]
            end   = [a.end   for a in ars]
            ar_pr = ', '.join ([pretty_att_record (db, dr, a) for a in ars])
            if not (start [0] >= end [1] or start [1] >= end [0]) :
                msgs.append ("%(tr_pr)s overlap" % locals ())
        last_ar = ar
    if not dyn.durations_allowed :
        nobreak  = 0.0
        last_end = None
        for ar in need_break_recs :
            start   = Date (ar.start, offset = 0)
            s, e, ds, de, duration = check_timestamps \
                (_, ar.start, ar.end, dr.date)
            if last_end and (start - last_end).as_seconds () >= 30 * 60 :
                nobreak  = duration
            else :
                nobreak += duration
            last_end = Date (ar.end,  offset = 0)
            if nobreak > 6 :
                msgs.append \
                    ("%(ar_pr)s More than 6 hours "
                     "without a break of at least half an hour"
                    % locals ()
                    )
                break
    if msgs :
        msgs.sort ()
        raise Reject ('\n'.join ([_ (i) for i in msgs]))
    return True
# end def att_records_consistent

def time_records_consistent (db, dr) :
    """ Check if all time records for this daily record are consistent
        Performed when dr.status changes open->submitted
        + check that each record contains a wp
        + check that sum of work-time does not exceed 10 hours -- if user
          may not work more than 10 hours
        + Travel times (if time_activity has travel flag) are excempt
          from work-time checks
        + no_overtime flag in time_project: check if really no overtime
          booked
        + Check that all WP are bookable
          + User is on bookers list
          + WP is valid
    """
    _        = db.i18n.gettext
    dtp      = dr.date.pretty (common.ymd)
    uname    = db.user.get (dr.user, 'username')
    msgs     = []
    dyn      = get_and_check_dyn (db, dr)
    trec     = [db.time_record.getnode (i) for i in dr.time_record]
    trec_notravel   = []
    noover_sum      = 0
    noover_sum_day  = 0
    no_over_wp      = None
    daily_hours     = user_dynamic.day_work_hours (dyn, dr.date)
    for tr in trec :
        tr_pr  = pretty_time_record (db, dr, tr)
        act    = tr.time_activity
        wp     = tr.wp
        travel = act and db.time_activity.get (act, 'travel')
        if not travel :
            trec_notravel.append (tr)
        if not tr.wp :
            msgs.append ("%(tr_pr)s: No work package" % locals ())
        else :
            wp        = db.time_wp.getnode  (tr.wp)
            pr        = db.time_project.getnode (wp.project)
            prname    = pr.name
            wpname    = wp.name
            max_hours = pr.max_hours
            no_over   = pr.no_overtime
            if pr.no_overtime_day :
                no_over_wp = "%s.%s" % (pr.name, wp.name)
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
            noover_sum_day += tr.duration
            if not wp.is_public and dr.user not in wp.bookers :
                msgs.append \
                    ( "User %(uname)s may not book on work package "
                      "%(prname)s.%(wpname)s"
                    % locals ()
                    )
            if dr.date < wp.time_start :
                msgs.append \
                    ( "Work package %(prname)s.%(wpname)s not yet valid "
                      "for date %(dtp)s"
                    % locals ()
                    )
            if wp.has_expiration_date and dr.date > wp.time_end :
                msgs.append \
                    ( "Work package %(prname)s.%(wpname)s no longer valid "
                      "for date %(dtp)s"
                    % locals ()
                    )
    tr_pr = "%s, %s:" % (uname, dtp)
    if noover_sum > daily_hours :
        msgs.append \
            ( "%(tr_pr)s: Sum of no-overtime WPs "
              "must not exceed %(daily_hours)s"
            % locals ()
            )
    if no_over_wp and noover_sum_day > daily_hours :
        msgs.append \
            ( "%(tr_pr)s No-overtime WP %(no_over_wp)s: "
              "time must not exceed %(daily_hours)s"
            % locals ()
            )
    if dyn.daily_worktime :
        work = sum (t.duration for t in trec_notravel)
        if work > dyn.daily_worktime :
            dwt = dyn.daily_worktime
            msgs.append \
                ( "%(tr_pr)s Work-time more than %(dwt)s hours: %(work)s"
                % locals ()
                )
    if msgs :
        msgs.sort ()
        raise Reject ('\n'.join ([_ (i) for i in msgs]))
    return True
# end def time_records_consistent

def check_daily_record (db, cl, nodeid, new_values) :
    """ Check that status changes are OK. Allowed changes:
         - From open to submitted by user or by HR
           But only if no leave submission in state 'submitted',
           'approved', 'cancel requested' exists
         - From submitted to accepted by supervisor or by HR
           but don't allow accepting own records
         - From submitted to open     by supervisor or by HR or by user
         - From accepted  to open     by HR
         - From open to leave if an accepted leave_submission exists
         - From leave to open if leave_submissions exist which are *all*
           in state cancel
    """
    _ = db.i18n.gettext
    for i in 'user', 'date' :
        if i in new_values and db.getuid () != '1' :
            raise Reject (_ ("%(attr)s may not be changed") % {'attr' : _ (i)})
    if i in ('status',) :
        if i in new_values and not new_values [i] :
            raise Reject (_ ("%(attr)s must be set") % {'attr' : _ (i)})
    user       = cl.get (nodeid, 'user')
    date       = cl.get (nodeid, 'date')
    if  (  frozen (db, user, date)
        and list (new_values) != ['tr_duration_ok']
        ) :
        uname = db.user.get (user, 'username')
        raise Reject (_ ("Frozen: %(uname)s, %(date)s") % locals ())
    uid        = db.getuid ()
    is_hr      = common.user_has_role (db, uid, 'hr')
    old_status = cl.get (nodeid, 'status')
    status     = new_values.get ('status', old_status)
    may_give_clearance = uid in common.tt_clearance_by (db, user)

    vs_exists = False
    st_accp = db.leave_status.lookup ('accepted')
    vs = vacation.leave_submissions_on_date (db, user, date)
    # All leave submissions in state cancelled (or declined)?
    # Check if at least one is cancelled
    cn = db.leave_status.lookup ('cancelled')
    dc = db.leave_status.lookup ('declined')
    op = db.leave_status.lookup ('open')
    vs_cancelled = True
    if not vs :
        vs_cancelled = False
    if vs_cancelled :
        for v in vs :
            if v.status == dc :
                continue
            if v.status == cn :
                vs_cancelled = True
            else :
                vs_cancelled = False
                break
    vs_has_valid  = False
    vs_has_open   = False
    for v in vs :
        if v.status == op :
            vs_has_open = True
        if v.status == op or v.status == cn or v.status == dc :
            continue
        vs_has_valid = True
        break
    vs = [v for v in vs if v.status == st_accp]
    if vs :
        assert len (vs) == 1
        vs_accepted = True

    old_status, status = \
        [db.daily_record_status.get (i, 'name') for i in [old_status, status]]
    ttby = db.user.get (user, 'timetracking_by')
    dr = cl.getnode (nodeid)
    if status != old_status :
        if not (  (   status == 'submitted' and old_status == 'open'
                  and (is_hr or user == uid or ttby == uid)
                  and time_records_consistent (db, dr)
                  and att_records_consistent (db, dr)
                  and not vs_has_valid
                  # FIXME: We may want to check vs_has_open
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
               or (   status == 'leave'     and old_status == 'open'
                  and vs_accepted
                  )
               or (   status == 'open'      and old_status == 'leave'
                  and vs_cancelled
                  )
               ) :
            msg = "Invalid Transition"
            if old_status == 'open' :
                if 'status' == 'submitted' :
                    if not is_hr and user != uid :
                        msg = _ ("Permission denied")
                    elif not time_records_consistent (db, dr) :
                        msg = _ ("Inkonsistent time records")
                    elif not att_records_consistent (db, dr) :
                        msg = _ ("Inkonsistent attendance records")
                    elif vs_has_valid or vs_has_open :
                        msg = _ ("Leave submission exists")
                elif 'status' == 'leave' :
                    msg = _ ("No accepted leave submission")
            elif old_status == 'leave' :
                msg = _ ("Leave submission not cancelled")
            elif old_status == 'accepted' :
                msg = _ ("Re-open only by HR")
            elif old_status == 'submitted' :
                if status == 'accepted' :
                    if not is_hr and not may_give_clearance :
                        msg = _ ("Permission denied")
                    elif user == uid :
                        msg = _ ("May not self-approve")
                elif status == 'open' :
                    if not is_hr and user != uid and not may_give_clearance :
                        msg = _ ("Permission denied")
            raise Reject \
                ( _ ("Denied state change: %(old_status)s->%(status)s: %(msg)s")
                % locals ()
                )
# end def check_daily_record

def invalidate_tr_duration_in_dr (db, time_record_id) :
    """ Invalidate tr duration, this used to also set the list of
        time_records in the daily record which is now an automatic
        backlink.
    """
    drec_id = db.time_record.get (time_record_id, 'daily_record')
    dr      = db.daily_record.getnode (drec_id)
    user_dynamic.invalidate_tr_duration (db, dr.user, dr.date, dr.date)
# end def invalidate_tr_duration_in_dr

def compute_tr_duration (db, cl, nodeid, old_values) :
    invalidate_tr_duration_in_dr (db, nodeid)
# end def compute_tr_duration

def new_daily_record (db, cl, nodeid, new_values) :
    """ Only create a daily_record if a user_dynamic record exists for
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
    _   = db.i18n.gettext
    uid = db.getuid ()
    common.require_attributes (_, cl, nodeid, new_values, 'user', 'date')
    user  = new_values ['user']
    ttby  = db.user.get (user, 'timetracking_by')
    uname = db.user.get (user, 'username')
    if  (   uid != user
        and uid != ttby
        and not common.user_has_role (db, uid, 'controlling', 'admin')
        ) :
        raise Reject \
            ( _ ("Only user, Timetracking by user, "
                "and Controlling may create daily records"
                )
            )
    # the following is allowed for the admin (import!)
    if uid != '1' :
        common.reject_attributes (_, new_values, 'status')
    date = new_values ['date']
    date.hour = date.minute = date.second = 0
    new_values ['date'] = date
    dyn  = user_dynamic.get_user_dynamic (db, user, date)
    if not dyn and uid != '1' :
        raise Reject \
            (_ ("No dynamic user data for %(uname)s, %(date)s") % locals ())
    if uid != '1' and not dyn.booking_allowed :
        raise Reject \
            (_ ("Booking not allowed for %(uname)s, %(date)s") % locals ())
    if frozen (db, user, date) :
        raise Reject (_ ("Frozen: %(uname)s, %(date)s") % locals ())
    if db.daily_record.filter \
        (None, {'date' : date.pretty ('%Y-%m-%d'), 'user' : user}) :
        raise Reject \
            ( _ ("Duplicate record: date = %(date)s, user = %(user)s")
            % new_values
            )
    if 'status' not in new_values :
        new_values ['status']  = db.daily_record_status.lookup ('open')
    new_values ['tr_duration_ok'] = None
# end def new_daily_record

def compute_endtime (start, duration) :
    minutes = duration * 60
    hours   = int (duration % 60)
    minutes = minutes - hours * 60
    ds      = Date (start, offset = 0)
    t = (ds + Interval ('%d:%d' % (hours, minutes))).pretty (hour_format)
    if duration > 0 and t == '00:00' :
        t = '24:00'
    return t
# end def compute_endtime

def check_start_end_duration (_, date, start, end, duration, new_values) :
    """ Either duration or both start/end must be set but not both
        of duration/end, if both are set, duration wins, but only in
        case of *creation*, not modification.
        Set end from start/duration if end empty
        Note: We are using naive times (with timezone 0) here, this
        means we can safely use date.pretty for converting back to
        string.
        Note2: This only works (and is only called) for legacy-interface
        where time_record and attendance_record are linked.
    """
    dstart = dend = None
    if start and ":" not in start :
        start = start + ":00"
    if end   and ":" not in end :
        end   = end   + ":00"
    if 'end' in new_values :
        if not start :
            attr = _ ('start')
            raise Reject (_ (''"%(attr)s must be specified") % locals ())
        dstart, dend, sp, ep, dur = check_timestamps (_, start, end, date)
        duration                = dur
        new_values ['start']    = sp
        new_values ['end']      = ep
    else :
        if duration is not None :
            check_duration (_, duration, 24)
        if start and 'start' in new_values :
            if duration is None :
                t = end
            else :
                t = compute_endtime (start, duration)
            dstart, dend, sp, ep, dur = check_timestamps (_, start, t, date)
            new_values ['start'] = sp
            new_values ['end']   = ep
    return dstart, dend
# end def check_start_end_duration

def leave_wp (db, dr, wp, start, end, duration) :
    if not wp :
        return False
    if start is not None or end is not None or duration is None :
        return False
    tp = db.time_project.getnode (db.time_wp.get (wp, 'project'))
    if not tp.approval_required :
        return False
    # Only search for non-cancelled non-retired non-declined
    st  = []
    unwanted = ('cancelled', 'retired', 'declined')
    for stid in db.leave_status.getnodeids (retired = False) :
        if db.leave_status.get (stid, 'name') in unwanted :
            continue
        st.append (stid)
    vs = vacation.leave_submissions_on_date \
        (db, dr.user, dr.date, filter = dict (status = st))
    if not vs :
        return False
    assert len (vs) == 1
    vs = vs [0]
    if vs.status != db.leave_status.lookup ('accepted') :
        return False
    clearer = common.tt_clearance_by (db, dr.user)
    uid     = db.getuid ()
    ld      = vacation.leave_duration (db, dr.user, dr.date)
    if tp.max_hours is not None :
        ld = min (ld, tp.max_hours)
    if not ld and tp.max_hours != 0 :
        return False
    if ld != duration :
        return False
    if  (  (uid in clearer and not tp.approval_hr)
        or (   common.user_has_role (db, uid, 'HR-leave-approval')
           and tp.approval_hr
           )
        ) :
        return True
    return False
# end def leave_wp

def vacation_wp (db, wpid) :
    """ Allow creation of vacation wp for other user
    """
    wp = db.time_wp.getnode (wpid)
    tp = db.time_project.getnode (wp.project)
    if tp.is_public_holiday :
        return True
    return False
# end def vacation_wp

def check_open_not_frozen (db, dr, uname) :
    _ = db.i18n.gettext
    if dr.status != db.daily_record_status.lookup ('open') and uid != '1' :
        raise Reject (_ ('Editing of time records only for status "open"'))
    if frozen (db, dr.user, dr.date) :
        date = dr.date
        raise Reject (_ ("Frozen: %(uname)s, %(date)s") % locals ())
# end def check_open_not_frozen

def new_attendance_record (db, cl, nodeid, new_values) :
    _      = db.i18n.gettext
    uid    = db.getuid ()
    common.require_attributes (_, cl, nodeid, new_values, 'daily_record')
    dr     = db.daily_record.getnode (new_values ['daily_record'])
    uname  = db.user.get (dr.user, 'username')
    trid   = new_values.get ('time_record', None)
    check_open_not_frozen (db, dr, uname)
    duration = None
    if trid :
        tr = db.time_record.getnode (trid)
        # Allow only one attendance_record link to a tr
        if tr.attendance_record :
            raise Reject (_ ("Only one link to a time record allowed"))
        duration = tr.duration
    start = new_values.get ('start')
    end   = new_values.get ('end')
    check_start_end_duration (_, dr.date, start, end, duration, new_values)
# end def new_attendance_record

def new_time_record (db, cl, nodeid, new_values) :
    """ auditor on time_record
    """
    _      = db.i18n.gettext
    uid    = db.getuid ()
    travel = False
    common.require_attributes \
        (_, cl, nodeid, new_values, 'daily_record', 'duration')
    common.reject_attributes  (_, new_values, 'tr_duration')
    dr       = db.daily_record.getnode (new_values ['daily_record'])
    uname    = db.user.get (dr.user, 'username')
    check_open_not_frozen (db, dr, uname)
    duration = new_values.get ('duration', None)
    check_duration (_, duration, 24)
    wpid     = new_values.get ('wp')
    ttby     = db.user.get (dr.user, 'timetracking_by')
    if  (   uid != dr.user
        and uid != ttby
        and not common.user_has_role (db, uid, 'controlling', 'admin')
        and not leave_wp (db, dr, wpid, None, None, duration)
        and not vacation_wp (db, wpid)
        ) :
        raise Reject \
            (_ ("Only %(uname)s, Timetracking by, and Controlling "
                "may create time records"
               )
            % locals ()
            )
    dynamic  = user_dynamic.get_user_dynamic (db, dr.user, dr.date)
    date     = dr.date.pretty (common.ymd)
    if not dynamic :
        if uid != '1' :
            raise Reject \
                (_ ("No dynamic user data for %(uname)s, %(date)s") % locals ())
    else :
        if not dynamic.booking_allowed and uid != '1' :
            raise Reject \
                (_ ("Booking not allowed for %(uname)s, %(date)s") % locals ())
        if not (dr.weekend_allowed or dynamic.weekend_allowed) and uid != '1' :
            wday = gmtime (dr.date.timestamp ())[6]
            if wday in (5, 6) :
                raise Reject (_ ('No weekend booking allowed'))
# end def new_time_record

def check_att_record (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    for i in 'daily_record', :
        if i in new_values :
            raise Reject (_ ("%(attr)s may not be changed") % {'attr' : _ (i)})
    # time_record may not be changed to *another* time_record
    # But *may* become empty if new interface is used
    if new_values.get ('time_record', None) :
        attr = _ ('time_record')
        raise Reject (_ ("%(attr)s may not be changed") % locals ())
    tr       = None
    duration = None
    ar       = cl.getnode (nodeid)
    trid     = new_values.get ('time_record',  ar.time_record)
    if trid :
        tr = db.time_record.getnode (trid)
        duration = tr.duration
    drec     = new_values.get ('daily_record', ar.daily_record)
    dr       = db.daily_record.getnode (drec)
    date     = dr.date
    user     = dr.user
    uname    = db.user.get (user, 'username')
    start    = new_values.get ('start', ar.start)
    end      = new_values.get ('end',   ar.end)
    uid      = db.getuid ()
    ttby     = db.user.get (dr.user, 'timetracking_by')
    location = new_values.get ('work_location', ar.work_location)
    dur      = duration
    # Allow change of end independent of existing duration in tr
    if ar.end :
        dur = None
    check_start_end_duration (_, date, start, end, dur, new_values)
    if  (   uid != dr.user
        and uid != ttby
        and not common.user_has_role (db, uid, 'controlling', 'admin', 'hr')
        ) :
        raise Reject \
            ( _ ( "Only %(uname)s, Timetracking by, and Controlling "
                  "may create/change attendance records"
                )
            % locals ()
            )
    dynamic  = user_dynamic.get_user_dynamic (db, dr.user, dr.date)
    date     = dr.date.pretty (common.ymd)
    if not dynamic :
        if uid != '1' :
            raise Reject \
                (_ ("No dynamic user data for %(uname)s, %(date)s") % locals ())
    else :
        if not dynamic.booking_allowed and uid != '1' :
            raise Reject \
                (_ ("Booking not allowed for %(uname)s, %(date)s") % locals ())
        if not (dr.weekend_allowed or dynamic.weekend_allowed) and uid != '1' :
            wday = gmtime (dr.date.timestamp ())[6]
            if wday in (5, 6) :
                raise Reject (_ ('No weekend booking allowed'))
    if 'start' in new_values and 'start_generated' not in new_values :
        new_values ['start_generated'] = False
    if 'end' in new_values and 'end_generated' not in new_values :
        new_values ['end_generated'] = False
# end def check_att_record

def check_time_record (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    for i in 'daily_record', :
        if i in new_values :
            raise Reject (_ ("%(attr)s may not be changed") % {'attr' : _ (i)})
    drec     = new_values.get ('daily_record', cl.get (nodeid, 'daily_record'))
    dr       = db.daily_record.getnode (drec)
    date     = dr.date
    user     = dr.user
    wpid     = new_values.get ('wp', cl.get (nodeid, 'wp'))
    wp       = None
    tp       = None
    is_ph    = False
    if (wpid) :
        wp = db.time_wp.getnode (wpid)
        tp = db.time_project.getnode (wp.project)
        is_ph = tp.is_public_holiday
    if  (   frozen (db, user, date)
        and list (new_values) != ['tr_duration']
        ) :
        uname = db.user.get (user, 'username')
        raise Reject (_ ("Frozen: %(uname)s, %(date)s") % locals ())
    status   = db.daily_record.get (cl.get (nodeid, 'daily_record'), 'status')
    leave    = db.daily_record_status.lookup ('leave')
    subm     = db.daily_record_status.lookup ('submitted')
    accpt    = db.daily_record_status.lookup ('accepted')
    allow    = False
    if dr.status == leave :
        du = vacation.leave_duration (db, user, date, is_ph)
        if  (   list (new_values) == ['duration']
            and new_values ['duration'] == du
            and cl.get (nodeid, 'duration') != du
            ) :
            allow = True
    elif dr.status in (subm, accpt) and is_ph :
        du = vacation.leave_duration (db, user, date, is_ph)
        if (   new_values.keys () == ['duration']
           and new_values ['duration'] == du
           and cl.get (nodeid, 'duration') != du
           ) :
           allow = True
    allow = allow or db.getuid () == '1'
    if  (   status != db.daily_record_status.lookup ('open')
        and list (new_values) != ['tr_duration']
        and not allow
        ) :
        raise Reject (_ ('Editing of time records only for status "open"'))
    # allow empty duration to delete record
    if 'duration' in new_values and new_values ['duration'] is None :
        keys = dict.fromkeys (new_values)
        del keys ['duration']
        if len (keys) > 0 :
            raise Reject \
                ( _ ('%(date)s: No duration means "delete record" but '
                     'you entered new value for %(attr)s'
                    )
                % dict ( date = date.pretty (common.ymd)
                       , attr = ", ".join (['"' + _ (i) + '"' for i in keys])
                       )
                )
        return
    duration = new_values.get ('duration',     cl.get (nodeid, 'duration'))
    wp       = new_values.get ('wp',           cl.get (nodeid, 'wp'))
    ta       = 'time_activity'
    activity = new_values.get (ta,             cl.get (nodeid, ta))
    comment  = new_values.get ('comment',      cl.get (nodeid, 'comment'))
    if 'tr_duration' not in new_values :
        new_values ['tr_duration'] = None
# end def check_time_record

def check_for_retire_and_duration (db, cl, nodeid, old_values) :
    dur = cl.get (nodeid, 'duration')
    if dur is None :
        cl.retire (nodeid)
    elif (common.changed_values (old_values, cl, nodeid)
         not in (['tr_duration'], [])
         ) :
        drid = cl.get (nodeid, 'daily_record')
        dr = db.daily_record.getnode (drid)
        user_dynamic.invalidate_tr_duration (db, dr.user, dr.date, dr.date)
# end def check_for_retire_and_duration

def fix_daily_recs_after_retire (db, cl, nodeid, dummy) :
    """ Update the tr_duration in daily record """
    invalidate_tr_duration_in_dr (db, nodeid)
# end def fix_daily_recs_after_retire

def check_retire (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    assert not new_values
    uid      = db.getuid ()
    st_open  = db.daily_record_status.lookup ('open')
    st_leave = db.daily_record_status.lookup ('leave')
    tr = cl.getnode (nodeid)
    dr = db.daily_record.getnode (tr.daily_record)
    if frozen (db, dr.user, dr.date) :
        raise Reject (_ ("Can't retire frozen time record"))
    tt_by = db.user.get (dr.user, 'timetracking_by')
    allowed = True
    if dr.status == st_open :
        if  (   uid != dr.user
            and uid != tt_by
            and not common.user_has_role (db, uid, 'controlling', 'admin')
            ) :
            # Must have a leave submission in status accepted, then we
            # can retire existing records
            ac = db.leave_status.lookup ('accepted')
            vs = vacation.leave_submissions_on_date \
                (db, dr.user, dr.date, filter = dict (status = ac))
            if not vs :
                allowed = False
    else :
        if dr.status == st_leave :
            # All leave submissions must be in state cancelled or declined
            # At least one must be cancelled
            cn = db.leave_status.lookup ('cancelled')
            dc = db.leave_status.lookup ('declined')
            vs = vacation.leave_submissions_on_date (db, dr.user, dr.date)
            if not vs :
                allowed = False
            if allowed :
                allowed = False
                for v in vs :
                    if v.status == dc :
                        continue
                    if v.status == cn :
                        allowed = True
                    if v.status != cn :
                        allowed = False
                        break
        else :
            allowed = False
    # Allow admin to retire any time_record (!)
    if not allowed and db.getuid () != '1' :
        raise Reject (_ ("Permission denied"))
# end def check_retire

def send_mail_on_deny (db, cl, nodeid, old_values) :
    """If daily record is denied, send message to user."""

    changer   = db.getuid ()
    other_uid = cl.get (nodeid, "user")
    if changer == other_uid :
        return ### user reopened himself

    dr_status     = db.getclass ("daily_record_status")
    old_status    = old_values ["status"]
    new_status    = cl.get (nodeid, "status")
    s_sub, s_open = [dr_status.lookup (s) for s in ("submitted", "open")]

    if (old_status, new_status) == (s_sub, s_open) :
        mailer  = roundupdb.Mailer (db.config)
        date    = cl.get (nodeid, "date").pretty (common.ymd)
        sup     = db.user.getnode (changer)
        superv  = sup.username
        email   = db.user.get (other_uid, "address")
        sender  = (sup.realname, sup.address)
        subject = "Daily record denied for %(date)s by %(superv)s" % locals ()
        content = \
            ( "Your daily record for %(date)s has been denied.\n"
              "Please contact %(superv)s for details, then submit again.\n"
            % locals ()
            )
        try :
            mailer.standard_message ((email,), subject, content, sender)
        except roundupdb.MessageSendError as message :
            raise roundupdb.DetectorError (message)
# end def send_mail_on_deny

def check_metadata (db, cl, nodeid, new_values) :
    """ The metadata field should be in json.
        This field should have the following format:
        { 'system_name' : 'jira'
        , 'levels'      : [ { 'level' : 1
                            , 'level_name' : 'Project'
                            , 'name' : 'Project-Name'
                            , 'id' : '4711'
                          , ...
                          ]
        }
        Note that both, the top-level system_name and levels are
        required. In the levels array at least one member is required.
        The level is an integer value and levels must start with 1 and
        be tightly numbered (without jumps of the counter). The
        level_name and name of the respective item on that level depends
        on the remote system. The id is a string because some systems
        may use non-numeric ids here. The fields shown are all required,
        additional fields may be present.
    """
    _ = db.i18n.gettext
    if 'metadata' not in new_values :
        return
    metadata = new_values ['metadata']
    # Allow empty
    if not metadata :
        return
    obj = json.loads (metadata)
    if not isinstance (obj, type ({})) :
        raise Reject (_ ("Invalid metadata, object not a dict"))
    if 'system_name' not in obj or 'levels' not in obj :
        raise Reject (_ ("Invalid metadata, required fields missing"))
    if not isinstance (obj ['levels'], type ([])) :
        raise Reject (_ ("Invalid metadata, levels must be array"))
    for n, lvl in enumerate (obj ['levels']) :
        if not isinstance (lvl, type ({})) :
            raise Reject (_ ("Invalid metadata, level not a dict"))
        for k in 'level', 'level_name', 'name', 'id' :
            if k not in lvl :
                raise Reject \
                    (_ ('Invalid metadata, required field "%s" '
                        'in level missing'
                       )
                    % k
                    )
                if k != 'level' :
                    if not isinstance (lvl ['k'], type (u'')) :
                        raise Reject \
                            (_ ('Invalid metadata: %s: String expected') % k)
            if int (lvl ['level']) != n + 1 :
                raise Reject (_ ('Invalid metadata, level: expect: %d' % (n+1)))
# end def check_metadata

def fix_tr_duration (db, cl, nodeid, old_values) :
    """ If the tr_duration_ok was set to None we recompute the
        tr_duration here.
    """
    dr = cl.getnode (nodeid)
    if dr.tr_duration_ok is None :
        user_dynamic.update_tr_duration (db, dr)
# end def fix_tr_duration

def check_obsolete_props (db, cl, nodeid, new_values) :
    """ Check no-longer-valid properties of time-record
        We cannot get rid of these properties yet (because we need to
        copy things to attendance records) but we make sure here that
        they are no longer used (at least not changed).
    """
    _ = db.i18n.gettext
    v = 'end end_generated start start_generated work_location'
    for k in v.split () :
        if k in new_values :
            raise Reject (_ ('Trying to change obsolete property "%s"') % k)
# end def check_obsolete_props

def update_arec (db, cl, nodeid, old_values) :
    """ If attendance record is changed *and* has a corresponding
        time_record link, we update the duration if necessary
    """
    ar = cl.getnode (nodeid)
    if not ar.time_record or not ar.start :
        return
    tr = db.time_record.getnode  (ar.time_record)
    dr = db.daily_record.getnode (ar.daily_record)
    dstart, dend, sp, ep, dur = check_timestamps \
        (db.i18n.gettext, ar.start, ar.end, dr.date)
    if dur != tr.duration :
        db.time_record.set (tr.id, duration = dur)
# end def update_arec

def update_trec (db, cl, nodeid, old_values) :
    """ If time record is changed *and* has a corresponding
        attendance_record backlink, we update "end" if necessary
    """
    tr = cl.getnode (nodeid)
    if not tr.attendance_record :
        return
    assert len (tr.attendance_record) == 1
    arid = tr.attendance_record [0]
    # Check if time record was retired
    if cl.is_retired (nodeid) :
        db.attendance_record.retire (arid)
        return

    # Check what changed, do nothing if only tr_duration changed in timerec
    keys = []
    for k in old_values :
        if k in ['activity', 'attendance_record'] :
            continue
        if getattr (tr, k) != old_values [k] :
            keys.append (k)
    if keys == ['tr_duration'] :
        return
    ar = db.attendance_record.getnode (arid)
    dr = db.daily_record.getnode      (tr.daily_record)
    if ar.start is not None and ar.end is not None :
        dstart, dend, sp, ep, dur = check_timestamps \
            (db.i18n.gettext, ar.start, ar.end, dr.date)
    else :
        sp  = ar.start
        ep  = ar.end
        dur = None
    d = {}
    if dur and dur != tr.duration :
        d ['end'] = compute_endtime (sp, tr.duration)
    if tr.wp :
        wp = db.time_wp.getnode (tr.wp)
        work_location = db.time_project.get (wp.project, 'work_location')
        if work_location :
            d ['work_location'] = work_location
    if d :
        db.attendance_record.set (ar.id, **d)
# end def update_trec

def public_holiday (db, cl, nodeid, old_values) :
    """ Create public holiday if necessary
    """
    dr = cl.getnode (nodeid)
    vacation.try_create_public_holiday (db, nodeid, dr.date, dr.user)
# end def public_holiday

def init (db) :
    if 'time_record' not in db.classes :
        return
    db.time_record.audit  ("create", new_time_record)
    db.time_record.audit  ("set",    check_time_record)
    db.time_record.react  ("create", compute_tr_duration)
    db.time_record.react  ("set",    check_for_retire_and_duration)
    db.time_record.audit  ("retire", check_retire)
    db.time_record.react  ("retire", fix_daily_recs_after_retire)
    db.time_record.audit  ("create", check_obsolete_props, priority = 500)
    db.time_record.audit  ("set",    check_obsolete_props, priority = 500)
    db.time_record.react  ("set",    update_trec)
    att = db.attendance_record
    att.audit             ("create", new_attendance_record)
    att.audit             ("set",    check_att_record)
    att.react             ("create", update_arec)
    att.react             ("set",    update_arec)
    db.daily_record.audit ("create", new_daily_record)
    db.daily_record.audit ("set",    check_daily_record)
    db.daily_record.react ("set",    send_mail_on_deny)
    db.daily_record.audit ("create", check_metadata)
    db.daily_record.audit ("set",    check_metadata)
    db.daily_record.react ("set",    fix_tr_duration, priority = 200)
    db.daily_record.react ("create", fix_tr_duration, priority = 200)
    db.daily_record.react ("create", public_holiday)
# end def init

### __END__ time_record
