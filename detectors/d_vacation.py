#! /usr/bin/python
# Copyright (C) 2014-24 Dr. Ralf Schlatterbeck Open Source Consulting.
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

from roundup.exceptions             import Reject
from roundup.date                   import Date, Interval
from roundup.configuration          import InvalidOptionError
from roundup                        import roundupdb

import common
import freeze
import user_dynamic
import vacation
import o_permission

def check_range (db, nodeid, uid, first_day, last_day):
    """ Check length of range and if there are any records in the given
        time-range for this user. This means either the first day of an
        existing record is inside the new range or the last day is
        inside the new range or the first day is lower than the first
        day *and* the last day is larger (new interval is contained in
        existing interval).
    """
    _ = db.i18n.gettext
    if first_day > last_day:
        raise Reject (_ ("First day may not be after last day"))
    if (last_day - first_day) > Interval ('30d'):
        raise Reject (_ ("Max. 30 days for single leave submission"))
    range = common.pretty_range (first_day, last_day)
    both  = (first_day.pretty (';%Y-%m-%d'), last_day.pretty ('%Y-%m-%d;'))
    stati = [x for x in db.leave_status.getnodeids (retired = False)
             if db.leave_status.get (x, 'name') not in ('declined', 'cancelled')
            ]
    for f, l in ((range, None), (None, range), both):
        d = dict (user = uid, status = stati)
        if f:
            d ['first_day'] = f
        if l:
            d ['last_day'] = l
        r = [x for x in db.leave_submission.filter (None, d) if x != nodeid]
        if r:
            raise Reject \
                (_ ("You already have vacation requests in this time range"))
# end def check_range

def check_wp (db, wp_id, user, first_day, last_day, comment):
    _ = db.i18n.gettext
    wp = db.time_wp.getnode (wp_id)
    tp = db.time_project.getnode (wp.project)
    if not tp.approval_required:
        raise Reject (_ ("No approval required for work package"))
    if not wp.is_public and user not in wp.bookers:
        raise Reject (_ ("User may not book on work package %s") % wp_id)
    if first_day < wp.time_start or wp.time_end and last_day > wp.time_end:
        raise Reject (_ ("Work package not valid during vacation time"))
    if tp.is_special_leave and not comment:
        raise Reject (_ ("Comment is required for special leave"))
# end def check_wp

def fix_dates (new_values):
    for d in ('first_day', 'last_day'):
        if d in new_values:
            new_values [d] = common.fix_date (new_values [d])
# end def fix_dates

def new_submission (db, cl, nodeid, new_values):
    """ Check that new leave submission is allowed and has sensible
        parameters
    """
    _ = db.i18n.gettext
    common.reject_attributes (_, new_values, 'approval_hr', 'comment_cancel')
    uid = db.getuid ()
    st_subm = db.leave_status.lookup ('submitted')
    if 'user' not in new_values:
        user = new_values ['user'] = uid
    else:
        user = new_values ['user']
    common.require_attributes \
        (_, cl, nodeid, new_values, 'first_day', 'last_day', 'user')
    first_day = new_values ['first_day']
    last_day  = new_values ['last_day']
    fix_dates (new_values)
    if 'time_wp' not in new_values:
        wps = vacation.valid_leave_wps \
            ( db
            , user
            , last_day
            , [('-', 'project.is_vacation'), ('-', 'project.approval_hr')]
            )
        if wps:
            new_values ['time_wp'] = wps [0]

    common.require_attributes (_, cl, nodeid, new_values, 'time_wp')
    if freeze.frozen (db, user, first_day):
        raise Reject (_ ("Frozen"))
    comment = new_values.get ('comment')
    check_range (db, None, user, first_day, last_day)
    check_wp (db, new_values ['time_wp'], user, first_day, last_day, comment)
    is_admin = (uid == '1')
    if  (   'status' in new_values
        and new_values ['status'] != st_subm
        and not is_admin
        ):
        raise Reject (_ ('Initial status must be "submitted"'))
    if 'status' not in new_values:
        new_values ['status'] = st_subm
    if  (   user != uid
        and not (is_admin or common.user_has_role (db, uid, 'HR-vacation'))
        ):
        raise Reject \
            (_ ("Only special role may create submission for other user"))
    vacation.create_daily_recs (db, user, first_day, last_day)
    if vacation.leave_days (db, user, first_day, last_day) == 0:
        raise Reject (_ ("Vacation request for 0 days"))
    check_dr_status (db, user, first_day, last_day, 'open')
    check_dyn_user_params (db, user, first_day, last_day)
    o_permission.check_new_leave_submission_perm (db, cl, nodeid, new_values)
# end def new_submission

def check_dyn_user_params (db, user, first_day, last_day):
    _ = db.i18n.gettext
    d = first_day
    ctype = -1 # contract_type is either None or a string, can't be numeric
    while d <= last_day:
        dyn = user_dynamic.get_user_dynamic (db, user, d)
        if not dyn:
            ymd = common.ymd
            raise Reject (_ ("No dynamic user data for %s") % d.pretty (ymd))
        if dyn.vacation_yearly is None:
            raise Reject (_ ("No yearly vacation for this user"))
        if dyn.vacation_day is None or dyn.vacation_month is None:
            raise Reject (_ ("Vacation date setting is missing"))
        if ctype != dyn.contract_type and ctype != -1:
            raise Reject (_ ("Differing contract types in range"))
        ctype = dyn.contract_type
        d += common.day
# end def check_dyn_user_params

# These are allowed *without* a check of a valid WP because they allow
# to leave an impossible state when a WP is changed *after* someone
# submitted a leave request.
allowed_stati = dict.fromkeys \
    (( ('open',             'cancelled')
    ,  ('submitted',        'cancelled')
    ,  ('submitted',        'open')
    ,  ('accepted',         'cancel requested')
    ,  ('submitted',        'declined')
    ,  ('cancel requested', 'cancelled')
    ))

def check_submission (db, cl, nodeid, new_values):
    """ Check that changes to a leave submission are ok.
        We basically allow changes of first_day, last_day, and time_wp
        in status 'open'. The user must never change. The status
        transitions are bound to certain roles. Note that this auditor
        is called *after* it has been verified that a requested state
        change is at least possible (although we still have to check the
        role).
    """
    _ = db.i18n.gettext
    common.reject_attributes (_, new_values, 'user', 'approval_hr')
    old  = cl.getnode (nodeid)
    uid  = db.getuid ()
    user = old.user
    old_status = db.leave_status.get (old.status, 'name')
    if old_status != 'accepted':
        common.reject_attributes (_, new_values, 'comment_cancel')
    new_status = db.leave_status.get \
        (new_values.get ('status', old.status), 'name')
    if  (   old_status != 'open'
        and old_status not in ('accepted', 'cancel_requested')
        ):
        common.reject_attributes \
            (_, new_values, 'first_day', 'last_day', 'time_wp', 'comment')
    if old_status in ('accepted', 'cancel_requested'):
        common.reject_attributes \
            (_, new_values, 'first_day', 'last_day', 'comment')
    fix_dates (new_values)
    common.require_attributes \
        (_, cl, nodeid, new_values, 'first_day', 'last_day')
    first_day = new_values.get ('first_day', cl.get (nodeid, 'first_day'))
    last_day  = new_values.get ('last_day',  cl.get (nodeid, 'last_day'))
    if freeze.frozen (db, user, first_day):
        raise Reject (_ ("Frozen"))
    time_wp   = new_values.get ('time_wp',   cl.get (nodeid, 'time_wp'))
    comment   = new_values.get ('comment',   cl.get (nodeid, 'comment'))
    check_range (db, nodeid, user, first_day, last_day)
    # Allow several transitions even if WP is not valid
    # See allowed_stati above for allowed transitions.
    if  (  old_status == new_status
        or (old_status, new_status) not in allowed_stati
        ):
        check_wp    (db, time_wp, user, first_day, last_day, comment)
    # If wp changes accepted->cancel requested->cancelled, allow it if
    # it's the same type as the old one (vacation or public holiday)
    if  (  old_status == 'accepted' and new_status == 'cancel requested'
        or old_status == 'cancel requested' and new_status == 'cancelled'
        ):
        if 'time_wp' in new_values:
            owp = db.time_wp.getnode (cl.get (nodeid, 'time_wp'))
            otp = db.time_project.getnode (owp.project)
            nwp = db.time_wp.getnode (new_values ['time_wp'])
            ntp = db.time_project.getnode (nwp.project)
            if otp.is_vacation and not ntp.is_vacation:
                raise Reject ('Invalid change of WP, must be vacation')
            if otp.is_special_leave and not ntp.is_special_leave:
                raise Reject ('Invalid change of WP, must be special leave')
            if otp.approval_required and not ntp.approval_required:
                raise Reject ('Invalid change of WP, must require approval')
    if old_status in ('open', 'submitted'):
        vacation.create_daily_recs (db, user, first_day, last_day)
    if 'first_day' in new_values or 'last_day' in new_values:
        if vacation.leave_days (db, user, first_day, last_day) == 0:
            raise Reject (_ ("Vacation request for 0 days"))
        check_dyn_user_params (db, user, first_day, last_day)
    if old_status in ('open', 'submitted'):
        check_dr_status (db, user, first_day, last_day, 'open')
    if old_status in ('accepted', 'cancel requested'):
        check_dr_status (db, user, first_day, last_day, 'leave')
    if old_status != new_status:
        if  (old_status == 'accepted' and new_status == 'cancel requested'):
            common.require_attributes \
                (_, cl, nodeid, new_values, 'comment_cancel')
        # Allow special HR role to do any (possible) state changes
        # Except for approval of own records
        if  (  common.user_has_role (db, uid, 'HR-vacation')
            and (  uid != user
                or new_status not in ('accepted', 'declined', 'cancelled')
                )
            ):
            ok = True
        else:
            ok = False
            tp = db.time_project.getnode \
                (db.time_wp.get (old.time_wp, 'project'))
            if  (    not ok
                and (uid == user or common.user_has_role (db, uid, 'Admin'))
                ):
                if old_status == 'open' and new_status == 'submitted':
                    ok = True
                if  (   old_status == 'accepted'
                    and new_status == 'cancel requested'
                    ):
                    ok = True
                if old_status == 'submitted' and new_status == 'open':
                    ok = True
                if old_status == 'submitted' and new_status == 'cancelled':
                    ok = True
                if old_status == 'open' and new_status == 'cancelled':
                    ok = True
            elif not ok:
                clearer = common.tt_clearance_by (db, user)
                dyn     = user_dynamic.get_user_dynamic (db, user, first_day)
                ctype   = dyn.contract_type
                hr_only = vacation.need_hr_approval \
                    (db, tp, user, ctype, first_day, last_day, old_status)
                if  (   uid != user
                    and (   (uid in clearer and not hr_only)
                        or  common.user_has_role (db, uid, 'HR-leave-approval')
                        )
                    ):
                    if  (   old_status == 'submitted'
                        and new_status in ('accepted', 'declined')
                        ):
                        ok = True
                    if  (   old_status == 'cancel requested'
                        and (  new_status == 'cancelled'
                            or new_status == 'accepted'
                            )
                        ):
                        ok = True
            if not ok:
                raise Reject (_ ("Permission denied"))
# end def check_submission

def vac_report (db, cl, nodeid, new_values):
    _ = db.i18n.gettext
    raise Reject (_ ("Creation of vacation report is not allowed"))
# end def vac_report

def daily_recs (db, cl, nodeid, old_values):
    vs = cl.getnode (nodeid)
    vacation.create_daily_recs (db, vs.user, vs.first_day, vs.last_day)
# end def daily_recs

def check_dr_status (db, user, first_day, last_day, st_name):
    _ = db.i18n.gettext
    # All daily records must be in state status
    dt = common.pretty_range (first_day, last_day)
    dr = db.daily_record.filter (None, dict (user = user, date = dt))
    st = db.daily_record_status.lookup (st_name)
    for drid in dr:
        if st != db.daily_record.get (drid, 'status'):
            raise Reject \
                (_ ('Daily record not in status "%(st_name)s"') % locals ())
    # If not open, *all* daily records must exist
    # Maybe this should be an assertion...
    if st_name != 'open':
        iv = last_day + common.day - first_day
        if len (dr) != vacation.interval_days (iv):
            raise Reject (_ ('Daily records must exist'))
# end def check_dr_status

def creation_reactor (db, cl, nodeid, old_values):
    vs = cl.getnode (nodeid)
    # New submission start in state 'submitted'
    handle_submit  (db, vs)
# end def creation_reactor

def state_change_reactor (db, cl, nodeid, old_values):
    vs         = cl.getnode (nodeid)
    old_status = old_values.get ('status')
    new_status = vs.status
    accepted   = db.leave_status.lookup ('accepted')
    declined   = db.leave_status.lookup ('declined')
    submitted  = db.leave_status.lookup ('submitted')
    cancelled  = db.leave_status.lookup ('cancelled')
    crq        = db.leave_status.lookup ('cancel requested')
    if old_status == new_status:
        return
    dt  = common.pretty_range (vs.first_day, vs.last_day)
    drs = db.daily_record.filter (None, dict (user = vs.user, date = dt))
    ars = db.attendance_record.filter (None, dict (daily_record = drs))
    trs = db.time_record.filter (None, dict (daily_record = drs))
    if new_status == accepted:
        handle_accept    (db, vs, ars, trs, old_status)
    elif new_status == declined:
        handle_decline   (db, vs)
    elif new_status == submitted:
        handle_submit    (db, vs)
    elif new_status == cancelled:
        handle_cancel    (db, vs, drs, ars, trs, old_status == crq)
    elif new_status == crq:
        handle_cancel_rq (db, vs)
# end def state_change_reactor

def get_leave_email (db, leave):
    """ Determine all users with HR-leave-approval role and correct
        permission on this user.
    """
    now  = Date ('.')
    role = 'HR-leave-approval'
    filter  = dict (roles = role)
    filter ['status.is_nosy'] = True
    userids = db.user.filter (None, filter)
    email_users = []
    for approve_user in userids:
        # User themselves should not approve
        if leave.user == approve_user:
            continue
        if not common.user_has_role (db, approve_user, role):
            continue
        if not o_permission.user_allowed_by_olo \
            (db, approve_user, leave.user, now):
            continue
        email_users.append (db.user.getnode (approve_user))
    return tuple (u.address for u in email_users)
# end def get_leave_email

def try_send_mail (db, vs, now, var_text, var_subject, var_mail = None, ** kw):
    """ Two methods to specify destination emails: With a pointer to the
        config variable in var_mail or directly with the email
        parameter.
    """
    mailer         = roundupdb.Mailer (db.config)
    now            = Date ('.')
    wp             = db.time_wp.getnode (vs.time_wp)
    user           = db.user.getnode (vs.user)
    username       = user.username
    lastname       = user.lastname
    firstname      = user.firstname
    comment        = vs.comment
    comment_cancel = vs.comment_cancel
    wp_name        = wp.name
    tp_name        = db.time_project.get (wp.project, 'name')
    first_day      = vs.first_day.pretty (common.ymd)
    last_day       = vs.last_day.pretty  (common.ymd)
    nl             = '\n'
    d              = dict (locals ())
    d.update (kw)
    notify_text    = None
    notify_mail    = None
    notify_subj    = None
    try:
        notify_text = getattr (db.config.ext, var_text)
        notify_subj = getattr (db.config.ext, var_subject)
        if var_mail is not None:
            notify_mail = (getattr (db.config.ext, var_mail),)
        elif 'email' in kw:
            notify_mail = kw ['email']
        else:
            notify_mail = (user.address,)
    except InvalidOptionError:
        pass
    if notify_text and notify_subj and notify_mail:
        subject = \
            notify_subj.replace ('$', '%').replace ('\n', ' ') % d
        msg     = notify_text.replace ('$', '%') % d
        sender  = None
        try:
            sname = getattr (db.config.ext, 'MAIL_SENDER_NAME', None)
            smail = getattr (db.config.ext, 'MAIL_SENDER_ADDR', None)
            if sname and smail:
                sender = (sname, smail)
        except InvalidOptionError:
            pass
        try:
            mailer.standard_message (notify_mail, subject, msg, sender)
        except roundupdb.MessageSendError as message:
            raise roundupdb.DetectorError (message)
# end def try_send_mail

def handle_accept (db, vs, ars, trs, old_status):
    cancr   = db.leave_status.lookup ('cancel requested')
    warn_tr = []
    warn_ar = []
    if old_status != cancr:
        arid_dict = {}
        for trid in trs:
            tr  = db.time_record.getnode (trid)
            wp  = tp = None
            if tr.wp is not None:
                wp  = db.time_wp.getnode (tr.wp)
                tp  = db.time_project.getnode (wp.project)
            trd = db.daily_record.get (tr.daily_record, 'date')
            if tp is None or not tp.is_public_holiday:
                if wp is None or wp.id != vs.time_wp:
                    dt = trd.pretty (common.ymd)
                    wn = (wp and wp.name) or ''
                    tn = (tp and tp.name) or ''
                    warn_tr.append ((dt, tn, wn, tr.duration))
                db.time_record.retire (trid)
            else:
                # All public holiday tr have a linked ar, we do not
                # retire the ar in that case
                assert len (tr.attendance_record) == 1
                arid_dict [tr.attendance_record [0]] = 1
        for arid in ars:
            ar  = db.attendance_record.getnode (arid)
            if ar.id in arid_dict:
                continue
            trd = db.daily_record.get (ar.daily_record, 'date')
            dt = trd.pretty (common.ymd)
            wl = ar.work_location or ''
            if wl:
                wl = db.work_location.get (wl, 'code')
            st = ar.start or ''
            en = ar.end   or ''
            warn_ar.append ((dt, wl, st, en))
            db.attendance_record.retire (arid)
        d = vs.first_day
        off = db.work_location.filter (None, dict (is_off = True)) [0]
        while (d <= vs.last_day):
            ld = du = vacation.leave_duration (db, vs.user, d)
            dt = common.pretty_range (d, d)
            dr = db.daily_record.filter (None, dict (user = vs.user, date = dt))
            wp = db.time_wp.getnode (vs.time_wp)
            tp = db.time_project.getnode (wp.project)
            if tp.max_hours is not None:
                du = min (ld, tp.max_hours)
            assert len (dr) == 1
            if ld:
                trn = db.time_record.create \
                    ( daily_record  = dr [0]
                    , duration      = du
                    , wp            = vs.time_wp
                    )
                db.attendance_record.create \
                    ( daily_record  = dr [0]
                    , time_record   = trn
                    , work_location = off
                    )
            leave = db.daily_record_status.lookup ('leave')
            db.daily_record.set (dr [0], status = leave)
            d += common.day
    deleted_records = ''
    if warn_tr or warn_ar:
        d = []
        tdl = wdl = 0
        if warn_tr:
            try:
                d.append ('')
                t = db.config.ext.MAIL_LEAVE_USER_ACCEPT_TIMERECS_TEXT.rstrip ()
                d.append (t)
            except KeyError:
                pass
        for w in warn_tr:
            tdl = max (tdl, len (w [1]))
            wdl = max (wdl, len (w [2]))
        fmt = "%%s: %%%ds / %%%ds duration: %%s" % (tdl, wdl)
        for w in warn_tr:
            d.append (fmt % w)
        if warn_ar:
            try:
                d.append ('')
                t = db.config.ext.MAIL_LEAVE_USER_ACCEPT_ATTRECS_TEXT.rstrip ()
                d.append (t)
            except KeyError:
                pass
        tll = max (len (w [1]) for w in warn_ar)
        fmt = "%%s: %%%ds %%5s-%%5s" % tll
        for w in warn_ar:
            d.append (fmt % w)
        deleted_records = '\n'.join (d) + '\n'

    now = Date ('.')
    if old_status == cancr:
        try_send_mail \
            ( db, vs, now
            , 'MAIL_LEAVE_USER_NOT_CANCELLED_TEXT'
            , 'MAIL_LEAVE_USER_NOT_CANCELLED_SUBJECT'
            )
    else:
        try_send_mail \
            ( db, vs, now
            , 'MAIL_LEAVE_USER_ACCEPT_TEXT'
            , 'MAIL_LEAVE_USER_ACCEPT_SUBJECT'
            , deleted_records = deleted_records
            )
    if old_status != cancr:
        try_send_mail \
            ( db, vs, now
            , 'MAIL_LEAVE_NOTIFY_TEXT'
            , 'MAIL_LEAVE_NOTIFY_SUBJECT'
            , 'MAIL_LEAVE_NOTIFY_EMAIL'
            )
        if tp.is_special_leave:
            try_send_mail \
                ( db, vs, now
                , 'MAIL_SPECIAL_LEAVE_NOTIFY_TEXT'
                , 'MAIL_SPECIAL_LEAVE_NOTIFY_SUBJECT'
                , email = get_leave_email (db, vs)
                )
# end def handle_accept

def handle_cancel (db, vs, drs, ars, trs, is_crq):
    if is_crq:
        ard = {}
        for trid in trs:
            tr  = db.time_record.getnode (trid)
            if tr.wp:
                wp  = db.time_wp.getnode (tr.wp)
                tp  = db.time_project.getnode (wp.project)
                if not tp.is_public_holiday:
                    assert tp.approval_required
                    db.time_record.retire (trid)
                else:
                    assert len (tr.attendance_record) == 1
                    ard [tr.attendance_record [0]] = 1
            else:
                # inconsistency with missing wp
                db.time_record.retire (trid)
        for arid in ars:
            if arid not in ard:
                db.attendance_record.retire (arid)
        st_open = db.daily_record_status.lookup ('open')
        for dr in drs:
            db.daily_record.set (dr, status = st_open)

        now = Date ('.')
        try_send_mail \
            ( db, vs, now
            , 'MAIL_LEAVE_USER_CANCELLED_TEXT'
            , 'MAIL_LEAVE_USER_CANCELLED_SUBJECT'
            )
        try_send_mail \
            ( db, vs, now
            , 'MAIL_LEAVE_CANCEL_TEXT'
            , 'MAIL_LEAVE_CANCEL_SUBJECT'
            , 'MAIL_LEAVE_CANCEL_EMAIL'
            )
        if tp.is_special_leave:
            try_send_mail \
                ( db, vs, now
                , 'MAIL_SPECIAL_LEAVE_CANCEL_TEXT'
                , 'MAIL_SPECIAL_LEAVE_CANCEL_SUBJECT'
                , email = get_leave_email (db, vs)
                )
# end def handle_cancel

def handle_crq_or_submit (db, vs, now, conf_string, hr_only):
    user    = db.user.getnode (vs.user)
    # always send to supervisor (and/or substitute), too.
    emails  = [db.user.get (x, 'address')
               for x in common.tt_clearance_by (db, vs.user)
              ]
    if hr_only:
        emails.extend (get_leave_email (db, vs))
    url     = '%sleave_submission?@template=approve' % db.config.TRACKER_WEB
    approval_type = ''
    try:
        if hr_only:
            s = 'MAIL_LEAVE_SUPERVISOR_%s_APPROVE_HR' % conf_string
        else:
            s = 'MAIL_LEAVE_SUPERVISOR_%s_APPROVE_SV' % conf_string
        approval_type = getattr (db.config.ext, s)
    except InvalidOptionError:
        pass
    try_send_mail \
        ( db, vs, now
        , 'MAIL_LEAVE_SUPERVISOR_%s_TEXT'    % conf_string
        , 'MAIL_LEAVE_SUPERVISOR_%s_SUBJECT' % conf_string
        , url           = url
        , approval_type = approval_type
        , email         = emails
        )
# end def handle_crq_or_submit

def handle_cancel_rq (db, vs):
    now = Date ('.')
    handle_crq_or_submit (db, vs, now, 'CRQ', False)
# end def handle_cancel_rq

def handle_decline (db, vs):
    now = Date ('.')
    try_send_mail \
        ( db, vs, now
        , 'MAIL_LEAVE_USER_DECLINE_TEXT'
        , 'MAIL_LEAVE_USER_DECLINE_SUBJECT'
        )
# end def handle_decline

# Always called in a reactor
# But the vacation sum uses time records for computing the already-taken
# vacation. These are never exiting at this point since we're in status
# submitted. So it is wrong to call vacation.need_hr_approval with
# 'booked' set to True.
def handle_submit (db, vs):
    now     = Date ('.')
    wp      = db.time_wp.getnode (vs.time_wp)
    tp      = db.time_project.getnode (wp.project)
    dyn     = user_dynamic.get_user_dynamic (db, vs.user, vs.first_day)
    ctype   = dyn.contract_type
    hr_only = vacation.need_hr_approval \
        (db, tp, vs.user, ctype, vs.first_day, vs.last_day, 'submitted')
    handle_crq_or_submit (db, vs, now, 'SUBMIT', hr_only)
    if tp.is_special_leave:
        try_send_mail \
            ( db, vs, now
            , 'MAIL_SPECIAL_LEAVE_USER_TEXT'
            , 'MAIL_SPECIAL_LEAVE_USER_SUBJECT'
            )
# end def handle_submit

def check_correction (db, cl, nodeid, new_values):
    _ = db.i18n.gettext
    common.require_attributes \
        (_, cl, nodeid, new_values, 'user', 'date', 'day')
    if nodeid:
        common.require_attributes \
            (_, cl, nodeid, new_values, 'absolute')
        for i in 'user',:
            if i in new_values:
                raise Reject \
                    (_ ("%(attr)s may not be changed") % {'attr': _ (i)})
    else:
        common.require_attributes \
            (_, cl, nodeid, new_values, 'user', 'date')
        date = new_values ['date']
        o_permission.check_valid_user (db, cl, nodeid, new_values, date = date)
        if 'absolute' not in new_values:
            new_values ['absolute'] = False
    user = new_values.get ('user')
    if user is None:
        user = cl.get (nodeid, 'user')
    if 'date' in new_values:
        new_values ['date'] = common.fix_date (new_values ['date'])
    date = new_values.get ('date')
    if date is None:
        date = cl.get (nodeid, 'date')
    if freeze.frozen (db, user, date):
        # Allow admin to add (initial) absolute correction
        if  (  nodeid is not None
            or db.getuid () != '1'
            or not new_values.get ('absolute')
            ):
            raise Reject (_ ("Frozen"))
    # Check that there is no other record for that user and date
    common.check_unique \
        (_, cl, nodeid, date = date.pretty (common.ymd), user = user)
    # Check that vacation parameters exist in dyn. user records
    dyn  = user_dynamic.get_user_dynamic (db, user, date)
    fdyn = dyn
    ndyn = dyn
    username = db.user.get (user, 'username')
    # Check for initial creation of user/dynamic user record where
    # the creation of a vacation correction is triggered
    if not dyn:
        dyn  = user_dynamic.first_user_dynamic (db, user)
        ndyn = user_dynamic.first_user_dynamic (db, user, date = date)
    if not fdyn and ndyn.valid_from < date - common.day:
        raise Reject \
            (_ ('No current dyn. user record for "%(username)s"') % locals ())
    # Check that no vacation correction is created in a year before the
    # first dynamic user record
    if dyn.valid_from.year > date.year:
        raise Reject \
            (_ ('Dyn. user record starts too late for "%(username)s"')
            % locals ()
            )
    while dyn and (not dyn.valid_to or dyn.valid_to > date):
        if  (  dyn.vacation_yearly is None
            or not dyn.vacation_month
            or not dyn.vacation_day
            ):
            raise Reject \
                (_ ('Missing vacation parameters in dyn. user record(s)'))
        dyn = user_dynamic.prev_user_dynamic (db, dyn)
# end def check_correction

def init (db):
    if 'leave_submission' not in db.classes:
        return
    # Status is checked with prio 200, we come later.
    db.leave_submission.audit    ("set",    check_submission, priority = 300)
    db.leave_submission.audit    ("create", new_submission)
    db.leave_submission.react    ("create", daily_recs, priority = 80)
    db.leave_submission.react    ("set",    daily_recs, priority = 80)
    db.leave_submission.react    ("set",    state_change_reactor)
    db.leave_submission.react    ("create", creation_reactor)
    db.vacation_report.audit     ("create", vac_report)
    db.vacation_correction.audit ("create", check_correction)
    db.vacation_correction.audit ("set",    check_correction)
# end def init
