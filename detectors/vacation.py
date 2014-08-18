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

from roundup.exceptions             import Reject
from roundup.date                   import Interval
from roundup.cgi.TranslationService import get_translation
from common import reject_attributes, ymd, clearance_by, require_attributes
from common import user_has_role

def check_range (db, nodeid, uid, first_day, last_day) :
    """ Check length of range and if there are any records in the given
        time-range for this user. This means either the first day of an
        existing record is inside the new range or the last day is
        inside the new range or the first day is lower than the first
        day *and* the last day is larger (new interval is contained in
        existing interval).
    """
    if (last_day - first_day) > Interval ('30d') :
        raise Reject (_ ("Max. 30 days for single vacation submission"))
    range = ';'.join ((first_day.pretty (ymd), last_day.pretty (ymd)))
    both  = (first_day.pretty (';%Y-%m-%d'), last_day.pretty ('%Y-%m-%d;'))
    for f, l in ((range, None), (None, range), both) :
        d = dict (user = uid)
        if f :
            d ['first_day'] = f
        if l :
            d ['last_day'] = l
        r = [x for x in db.vacation_submission.filter (None, d) if x != nodeid]
        if r :
            raise Reject \
                (_ ("You already have vacation requests in this time range"))
# end def check_range

def check_wp (db, wp_id) :
    wp = db.time_wp.getnode (wp_id)
    tp = db.time_project.getnode (wp.project)
    if not tp.approval_required :
        raise Reject (_ ("No approval required for work package"))
# end def check_wp

def new_submission (db, cl, nodeid, new_values) :
    """ Check that new vacation submission is allowed and has sensible
        parameters
    """
    uid = db.getuid ()
    st_open = db.vacation_status.lookup ('open')
    require_attributes \
        (_, cl, nodeid, new_values, 'first_day', 'last_day', 'time_wp')
    if 'user' not in new_values :
        user = new_values ['user'] = uid
    else :
        user = new_values ['user']
    first_day = new_values ['first_day']
    last_day  = new_values ['last_day']
    check_range (db, None, user, first_day, last_day)
    check_wp    (db, new_values ['time_wp'])
    if 'status' in new_values and new_values ['status'] != st_open :
        raise Reject (_ ('Initial status must be "open"'))
    if 'status' not in new_values :
        new_values ['status'] = st_open
    if user != uid and not user_has_role (db, uid, 'HR-vacation') :
        raise Reject \
            (_ ("Only special role may create submission for other user"))
# end def new_submission

def check_submission (db, cl, nodeid, new_values) :
    """ Check that changes to a vacation submission are ok.
        We basically allow changes of first_day, last_day, and time_wp
        in status 'open'. The user must never change. The status
        transitions are bound to certain roles. Note that this auditor
        is called *after* it has been verified that a requested state
        change is at least possible (although we still have to check the
        role).
    """
    reject_attributes (_, new_values, 'user')
    old = cl.getnode (nodeid)
    uid = db.getuid ()
    old_status = db.vacation_status.get (old.status, 'name')
    new_status = db.vacation_status.get \
        (new_values.get ('status', old.status), 'name')
    if old_status != new_status or old_status != 'open' :
        reject_attributes (_, new_values, 'first_day', 'last_day', 'time_wp')
    first_day = new_values.get ('first_day', cl.get (nodeid, 'first_day'))
    last_day  = new_values.get ('last_day',  cl.get (nodeid, 'last_day'))
    time_wp   = new_values.get ('time_wp',   cl.get (nodeid, 'time_wp'))
    check_range (db, nodeid, old.user, first_day, last_day)
    check_wp    (db, time_wp)
    if old_status != new_status :
        # Allow special HR role to do any (possible) state changes
        if user_has_role (db, uid, 'HR-vacation') :
            ok = True
        else :
            ok = False
            tp = db.time_project.getnode \
                (db.time_wp.get (old.time_wp, 'project'))
            if not ok and uid == old.user :
                if old_status == 'open' and new_status == 'submitted' :
                    ok = True
                if old_status == 'accepted' :
                    ok = True
                if old_status == 'submitted' and new_status == 'open' :
                    ok = True
            clearer = clearance_by (db, old.user)
            if  (  not ok
                and (   (uid in clearer and not tp.approval_hr)
                    or  (   user_has_role (db, uid, 'HR-leave-approval')
                        and tp.approval_hr
                        )
                    )
                ) :
                if  (   old_status == 'submitted'
                    and new_status in ('accepted', 'declined')
                    ) :
                    ok = True
                if old_status == 'cancel requested' :
                    ok = True
            if not ok :
                raise Reject (_ ("Permission denied"))
# end def check_submission

def vac_report (db, cl, nodeid, new_values) :
    raise Reject (_ ("Creation of vacation report is not allowed"))
# end def vac_report

# FIXME: Side-effects for state transitions
# - Email
# - Creating daily record / creating/removing time_record

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext

    if 'vacation_submission' not in db.classes :
        return
    # Status is checked with prio 200, we come later.
    db.vacation_submission.audit ("set",    check_submission, priority = 300)
    db.vacation_submission.audit ("create", new_submission)
    db.vacation_report.audit     ("create", vac_report)
# end def init
