#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2014 Dr. Ralf Schlatterbeck Open Source Consulting.
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

from math                           import ceil
from roundup.exceptions             import Reject
from roundup.date                   import Date, Interval
from roundup.cgi.TranslationService import get_translation
from roundup                        import roundupdb

import common
import freeze
import user_dynamic
import vacation

def check_range (db, nodeid, uid, first_day, last_day) :
    """ Check length of range and if there are any records in the given
        time-range for this user. This means either the first day of an
        existing record is inside the new range or the last day is
        inside the new range or the first day is lower than the first
        day *and* the last day is larger (new interval is contained in
        existing interval).
    """
    if first_day > last_day :
        raise Reject (_ ("First day may not be after last day"))
    if (last_day - first_day) > Interval ('30d') :
        raise Reject (_ ("Max. 30 days for single leave submission"))
    range = common.pretty_range (first_day, last_day)
    both  = (first_day.pretty (';%Y-%m-%d'), last_day.pretty ('%Y-%m-%d;'))
    stati = [x for x in db.leave_status.getnodeids (retired = False)
             if db.leave_status.get (x, 'name') not in ('declined', 'cancelled')
            ]
    for f, l in ((range, None), (None, range), both) :
        d = dict (user = uid, status = stati)
        if f :
            d ['first_day'] = f
        if l :
            d ['last_day'] = l
        r = [x for x in db.leave_submission.filter (None, d) if x != nodeid]
        if r :
            raise Reject \
                (_ ("You already have vacation requests in this time range"))
# end def check_range

def check_wp (db, wp_id, user, first_day, last_day, comment) :
    wp = db.time_wp.getnode (wp_id)
    tp = db.time_project.getnode (wp.project)
    if not tp.approval_required :
        raise Reject (_ ("No approval required for work package"))
    if not wp.is_public and user not in wp.bookers :
        raise Reject (_ ("User may not book on work package"))
    if first_day < wp.time_start or wp.time_end and last_day > wp.time_end :
        raise Reject (_ ("Work package not valid during vacation time"))
    if tp.is_special_leave and not comment :
        raise Reject (_ ("Comment is required for special leave"))
# end def check_wp

def fix_dates (new_values) :
    for d in ('first_day', 'last_day') :
        if d in new_values :
            new_values [d] = common.fix_date (new_values [d])
# end def fix_dates

def new_submission (db, cl, nodeid, new_values) :
    """ Check that new leave submission is allowed and has sensible
        parameters
    """
    uid = db.getuid ()
    st_subm = db.leave_status.lookup ('submitted')
    if 'user' not in new_values :
        user = new_values ['user'] = uid
    else :
        user = new_values ['user']
    common.require_attributes \
        (_, cl, nodeid, new_values, 'first_day', 'last_day', 'user')
    first_day = new_values ['first_day']
    last_day  = new_values ['last_day']
    fix_dates (new_values)
    if 'time_wp' not in new_values :
        wps = vacation.valid_leave_wps \
            ( db
            , user
            , last_day
            , [('-', 'project.is_vacation'), ('-', 'project.approval_hr')]
            )
        if wps :
            new_values ['time_wp'] = wps [0]

    common.require_attributes (_, cl, nodeid, new_values, 'time_wp')
    if freeze.frozen (db, user, first_day) :
        raise Reject (_ ("Frozen"))
    comment = new_values.get ('comment')
    check_range (db, None, user, first_day, last_day)
    check_wp    (db, new_values ['time_wp'], user, first_day, last_day, comment)
    if 'status' in new_values and new_values ['status'] != st_subm :
        raise Reject (_ ('Initial status must be "submitted"'))
    if 'status' not in new_values :
        new_values ['status'] = st_subm
    if user != uid and not common.user_has_role (db, uid, 'HR-vacation') :
        raise Reject \
            (_ ("Only special role may create submission for other user"))
    vacation.create_daily_recs (db, user, first_day, last_day)
    if vacation.leave_days (db, user, first_day, last_day) == 0 :
        raise Reject (_ ("Vacation request for 0 days"))
    check_dr_status (db, user, first_day, last_day, 'open')
    check_dyn_user_params (db, user, first_day, last_day)
# end def new_submission

def check_dyn_user_params (db, user, first_day, last_day) :
    d = first_day
    ctype = -1 # contract_type is either None or a string, can't be numeric
    while d <= last_day :
        dyn = user_dynamic.get_user_dynamic (db, user, d)
        if not dyn.vacation_yearly :
            raise Reject (_ ("No yearly vacation for this user"))
        if dyn.vacation_day is None or dyn.vacation_month is None :
            raise Reject (_ ("Vacation date setting is missing"))
        if ctype != dyn.contract_type and ctype != -1 :
            raise Reject (_ ("Differing contract types in range"))
        ctype = dyn.contract_type
        d += common.day
# end def check_dyn_user_params

def check_submission (db, cl, nodeid, new_values) :
    """ Check that changes to a leave submission are ok.
        We basically allow changes of first_day, last_day, and time_wp
        in status 'open'. The user must never change. The status
        transitions are bound to certain roles. Note that this auditor
        is called *after* it has been verified that a requested state
        change is at least possible (although we still have to check the
        role).
    """
    common.reject_attributes (_, new_values, 'user')
    old  = cl.getnode (nodeid)
    uid  = db.getuid ()
    user = old.user
    old_status = db.leave_status.get (old.status, 'name')
    new_status = db.leave_status.get \
        (new_values.get ('status', old.status), 'name')
    if old_status != 'open' :
        common.reject_attributes \
            (_, new_values, 'first_day', 'last_day', 'time_wp', 'comment')
    fix_dates (new_values)
    first_day = new_values.get ('first_day', cl.get (nodeid, 'first_day'))
    last_day  = new_values.get ('last_day',  cl.get (nodeid, 'last_day'))
    if freeze.frozen (db, user, first_day) :
        raise Reject (_ ("Frozen"))
    time_wp   = new_values.get ('time_wp',   cl.get (nodeid, 'time_wp'))
    comment   = new_values.get ('comment',   cl.get (nodeid, 'comment'))
    check_range (db, nodeid, user, first_day, last_day)
    check_wp    (db, time_wp, user, first_day, last_day, comment)
    if 'first_day' in new_values or 'last_day' in new_values :
        vacation.create_daily_recs (db, user, first_day, last_day)
        if vacation.leave_days (db, user, first_day, last_day) == 0 :
            raise Reject (_ ("Vacation request for 0 days"))
        check_dyn_user_params (db, user, first_day, last_day)
    if old_status in ('open', 'submitted') :
        check_dr_status (db, user, first_day, last_day, 'open')
    if old_status in ('accepted', 'cancel requested') :
        check_dr_status (db, user, first_day, last_day, 'leave')
    if old_status != new_status :
        # Allow special HR role to do any (possible) state changes
        # Except for approval of own records
        if  (  common.user_has_role (db, uid, 'HR-vacation')
            and (  uid != user
                or new_status not in ('accepted', 'declined', 'cancelled')
                )
            ) :
            ok = True
        else :
            ok = False
            tp = db.time_project.getnode \
                (db.time_wp.get (old.time_wp, 'project'))
            if not ok and uid == user :
                if old_status == 'open' and new_status == 'submitted' :
                    ok = True
                if  (   old_status == 'accepted'
                    and new_status == 'cancel requested'
                    ) :
                    ok = True
                if old_status == 'submitted' and new_status == 'open' :
                    ok = True
                if old_status == 'open' and new_status == 'cancelled' :
                    ok = True
            elif not ok :
                clearer = common.clearance_by (db, user)
                dyn     = user_dynamic.get_user_dynamic (db, user, first_day)
                ctype   = dyn.contract_type
                hr_only = vacation.need_hr_approval \
                    (db, tp, user, ctype, first_day, last_day)
                if  (   uid != user
                    and (   (uid in clearer and not hr_only)
                        or  common.user_has_role (db, uid, 'HR-leave-approval')
                        )
                    ) :
                    if  (   old_status == 'submitted'
                        and new_status in ('accepted', 'declined')
                        ) :
                        ok = True
                    if  (   old_status == 'cancel requested'
                        and (  new_status == 'cancelled'
                            or new_status == 'accepted'
                            )
                        ) :
                        ok = True
            if not ok :
                raise Reject (_ ("Permission denied"))
# end def check_submission

def vac_report (db, cl, nodeid, new_values) :
    raise Reject (_ ("Creation of vacation report is not allowed"))
# end def vac_report

def daily_recs (db, cl, nodeid, old_values) :
    vs = cl.getnode (nodeid)
    vacation.create_daily_recs (db, vs.user, vs.first_day, vs.last_day)
# end def daily_recs

def check_dr_status (db, user, first_day, last_day, st_name) :
    # All daily records must be in state status
    dt = common.pretty_range (first_day, last_day)
    dr = db.daily_record.filter (None, dict (user = user, date = dt))
    st = db.daily_record_status.lookup (st_name)
    for drid in dr :
        if st != db.daily_record.get (drid, 'status') :
            raise Reject \
                (_ ('Daily record not in status "%(st_name)s"') % locals ())
    # If not open, *all* daily records must exist
    # Maybe this should be an assertion...
    if st_name != 'open' :
        iv = last_day + common.day - first_day
        if len (dr) != vacation.interval_days (iv) :
            raise Reject (_ ('Daily records must exist'))
# end def check_dr_status

def state_change_reactor (db, cl, nodeid, old_values) :
    vs         = cl.getnode (nodeid)
    old_status = old_values.get ('status')
    new_status = vs.status
    accepted   = db.leave_status.lookup ('accepted')
    declined   = db.leave_status.lookup ('declined')
    submitted  = db.leave_status.lookup ('submitted')
    cancelled  = db.leave_status.lookup ('cancelled')
    crq        = db.leave_status.lookup ('cancel requested')
    if old_status == new_status :
        return
    dt  = common.pretty_range (vs.first_day, vs.last_day)
    drs = db.daily_record.filter (None, dict (user = vs.user, date = dt))
    trs = db.time_record.filter (None, dict (daily_record = drs))
    tp  = db.time_project.getnode (db.time_wp.get (vs.time_wp, 'project'))
    if new_status == accepted :
        handle_accept  (db, vs, trs, old_status)
    elif new_status == declined :
        handle_decline (db, vs)
    elif new_status == submitted :
        dyn     = user_dynamic.get_user_dynamic (db, vs.user, vs.first_day)
        ctype   = dyn.contract_type
        hr_only = vacation.need_hr_approval \
            (db, tp, vs.user, ctype, vs.first_day, vs.last_day, booked = True)
        handle_submit  (db, vs, hr_only)
    elif new_status == cancelled :
        handle_cancel  (db, vs, trs, old_status == crq)
# end def state_change_reactor

def handle_accept (db, vs, trs, old_status) :
    cancr = db.leave_status.lookup ('cancel requested')
    warn  = []
    if old_status != cancr :
        for trid in trs :
            tr  = db.time_record.getnode (trid)
            wp  = tp = None
            if tr.wp is not None :
                wp  = db.time_wp.getnode (tr.wp)
                tp  = db.time_project.getnode (wp.project)
            trd = db.daily_record.get (tr.daily_record, 'date')
            if tp is None or not tp.is_public_holiday :
                if wp is None or wp.id != vs.time_wp :
                    dt = trd.pretty (common.ymd)
                    st = tr.start or ''
                    en = tr.end   or ''
                    wn = (wp and wp.name) or ''
                    tn = (tp and tp.name) or ''
                    warn.append ((dt, tn, wn, st, en, tr.duration))
                db.time_record.retire (trid)
        d = vs.first_day
        off = db.work_location.lookup ('off')
        while (d <= vs.last_day) :
            ld = du = vacation.leave_duration (db, vs.user, d)
            dt = common.pretty_range (d, d)
            dr = db.daily_record.filter (None, dict (user = vs.user, date = dt))
            wp = db.time_wp.getnode (vs.time_wp)
            tp = db.time_project.getnode (wp.project)
            if tp.max_hours is not None :
                du = min (ld, tp.max_hours)
            assert len (dr) == 1
            if ld :
                db.time_record.create \
                    ( daily_record  = dr [0]
                    , duration      = du
                    , work_location = off
                    , wp            = vs.time_wp
                    )
            leave = db.daily_record_status.lookup ('leave')
            db.daily_record.set (dr [0], status = leave)
            d += common.day
    mailer  = roundupdb.Mailer (db.config)
    now     = Date ('.')
    wp      = db.time_wp.getnode (vs.time_wp)
    user    = db.user.getnode (vs.user)
    email   = user.address
    wpn     = wp.name
    tpn     = db.time_project.get (wp.project, 'name')
    fday    = vs.first_day.pretty (common.ymd)
    lday    = vs.last_day.pretty  (common.ymd)
    if old_status == cancr :
        subject = _ \
            (""'Leave "%(tpn)s/%(wpn)s" %(fday)s-%(lday)s not cancelled') \
            % locals ()
        content = _ \
            (""'Your cancel request "%(tpn)s/%(wpn)s" was not granted.\n') \
            % locals ()
        content += _ (''"Please contact your supervisor.\n")
    else :
        subject = _ \
            (""'Leave "%(tpn)s/%(wpn)s" %(fday)s-%(lday)s accepted') \
            % locals ()
        content = _ \
            (""'Your absence request "%(tpn)s/%(wpn)s" has been accepted.\n') \
            % locals ()
    if warn :
        content = [content]
        content.append \
            (_ (""'The following existing time records have been deleted:'))
        tdl = wdl = 0
        for w in warn :
            tdl = max (tdl, len (w [1]))
            wdl = max (wdl, len (w [2]))
        fmt = "%%s: %%%ds / %%%ds %%5s-%%5s duration: %%s" % (tdl, wdl)
        for w in warn :
            content.append (fmt % w)
        content = '\n'.join (content)
    try :
        mailer.standard_message ((email,), subject, content)
    except roundupdb.MessageSendError, message :
        raise roundupdb.DetectorError, message

    if old_status != cancr :
        username    = user.username
        lastname    = user.lastname
        firstname   = user.firstname
        wp_name     = wpn
        tp_name     = tpn
        first_day   = fday
        last_day    = lday
        notify_text = None
        notify_mail = None
        nl          = '\n'
        try :
            notify_text = db.config.ext.MAIL_LEAVE_NOTIFY_TEXT
            notify_mail = db.config.ext.MAIL_LEAVE_NOTIFY_EMAIL
        except KeyError :
            pass
        if notify_text and notify_mail :
            subject = _ \
                (""'Leave "%(tpn)s/%(wpn)s" %(fday)s-%(lday)s accepted') \
                % locals ()
            msg = notify_text.replace ('$', '%') % locals ()
            try :
                mailer.standard_message ((notify_mail,), subject, msg)
            except roundupdb.MessageSendError, message :
                raise roundupdb.DetectorError, message
        notify_text = notify_mail = None
        if tp.is_special_leave :
            try :
                notify_text = db.config.ext.MAIL_SPECIAL_LEAVE_NOTIFY_TEXT
                notify_mail = db.config.ext.MAIL_SPECIAL_LEAVE_NOTIFY_EMAIL
            except KeyError :
                pass
        if notify_text and notify_mail :
            msg = notify_text.replace ('$', '%') % locals ()
            subject = _ \
                (""'Leave "%(tpn)s/%(wpn)s" %(fday)s-%(lday)s accepted') \
                % locals ()
            try :
                mailer.standard_message ((notify_mail,), subject, msg)
            except roundupdb.MessageSendError, message :
                raise roundupdb.DetectorError, message
# end def handle_accept

def handle_cancel (db, vs, trs, is_crq) :
    drs = {}
    if is_crq :
        for trid in trs :
            tr  = db.time_record.getnode (trid)
            wp  = db.time_wp.getnode (tr.wp)
            tp  = db.time_project.getnode (wp.project)
            trd = db.daily_record.get (tr.daily_record, 'date')
            if not tp.is_public_holiday :
                assert tp.approval_required
                db.time_record.retire (trid)
            drs [tr.daily_record] = 1
        for dr in drs :
            st_open = db.daily_record_status.lookup ('open')
            db.daily_record.set (dr, status = st_open)
# end def handle_cancel

def handle_decline (db, vs) :
    mailer  = roundupdb.Mailer (db.config)
    now     = Date ('.')
    wp      = db.time_wp.getnode (vs.time_wp)
    email   = db.user.get (vs.user, 'address')
    wpn     = wp.name
    tpn     = db.time_project.get (wp.project, 'name')
    fday    = vs.first_day.pretty (common.ymd)
    lday    = vs.last_day.pretty  (common.ymd)
    subject = _ \
        (""'Leave "%(tpn)s/%(wpn)s" %(fday)s-%(lday)s declined') % locals ()
    content = \
        (""'Your absence request "%(tpn)s/%(wpn)s" has been declined.\n') \
        % locals ()
    content += _ (''"Please contact your supervisor.\n")
    try :
        mailer.standard_message ((email,), subject, content)
    except roundupdb.MessageSendError, message :
        raise roundupdb.DetectorError, message
# end def handle_decline

def handle_submit (db, vs, hr_only) :
    mailer  = roundupdb.Mailer (db.config)
    now     = Date ('.')
    wp      = db.time_wp.getnode (vs.time_wp)
    user    = db.user.getnode (vs.user)
    # always send to supervisor (and/or substitute), too.
    emails  = [db.user.get (x, 'address')
               for x in common.clearance_by (db, vs.user)
              ]
    if hr_only :
        emails.extend \
            (db.user.get (u, 'address')
             for u in common.get_uids_with_role (db, 'HR-leave-approval')
            )
    wpn     = wp.name
    tp      = db.time_project.getnode (wp.project)
    tpn     = tp.name
    fday    = vs.first_day.pretty (common.ymd)
    lday    = vs.last_day.pretty  (common.ymd)
    realnm  = user.realname
    nick    = user.nickname.upper ()
    url     = '%sleave_submission?@template=approve' % db.config.TRACKER_WEB
    subject = \
        (""'Leave request "%(tpn)s/%(wpn)s" from %(nick)s') % locals ()
    content = \
        (""'%(realnm)s has submitted a leave request "%(tpn)s/%(wpn)s".') \
        % locals ()
    if vs.comment :
        content += "\nComment from user:\n%s\n" % vs.comment
    if hr_only :
        content += "\nNeeds approval by HR."
    content += '\n' + url
    try :
        mailer.standard_message (emails, subject, content)
    except roundupdb.MessageSendError, message :
        raise roundupdb.DetectorError, message
    notify_text = None
    if tp.is_special_leave :
        username    = user.username
        lastname    = user.lastname
        firstname   = user.firstname
        wp_name     = wpn
        tp_name     = tpn
        first_day   = fday
        last_day    = lday
        nl          = '\n'
        try :
            notify_text = db.config.ext.MAIL_SPECIAL_LEAVE_USER_TEXT
        except KeyError :
            pass
    if notify_text :
        msg = notify_text.replace ('$', '%') % locals ()
        subject = \
            (""'Your Leave "%(tpn)s/%(wpn)s" %(fday)s-%(lday)s') % locals ()
        try :
            mailer.standard_message ((user.address,), subject, msg)
        except roundupdb.MessageSendError, message :
            raise roundupdb.DetectorError, message
# end def handle_submit

def check_correction (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'user', 'date', 'day')
    if nodeid :
        common.require_attributes \
            (_, cl, nodeid, new_values, 'absolute')
    else :
        if 'absolute' not in new_values :
            new_values ['absolute'] = False
    user = new_values.get ('user')
    if user is None :
        user = cl.get (nodeid, 'user')
    if 'date' in new_values :
        new_values ['date'] = common.fix_date (new_values ['date'])
    date = new_values.get ('date')
    if date is None :
        date = cl.get (nodeid, 'date')
    if freeze.frozen (db, user, date) :
        # Allow admin to add (initial) absolute correction
        if  (  nodeid is not None
            or db.getuid () != '1'
            or not new_values.get ('absolute')
            ) :
            raise Reject (_ ("Frozen"))
# end def check_correction

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext

    if 'leave_submission' not in db.classes :
        return
    # Status is checked with prio 200, we come later.
    db.leave_submission.audit    ("set",    check_submission, priority = 300)
    db.leave_submission.audit    ("create", new_submission)
    db.leave_submission.react    ("create", daily_recs, priority = 80)
    db.leave_submission.react    ("set",    daily_recs, priority = 80)
    db.leave_submission.react    ("set",    state_change_reactor)
    db.vacation_report.audit     ("create", vac_report)
    db.vacation_correction.audit ("create", check_correction)
    db.vacation_correction.audit ("set",    check_correction)
# end def init
