#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-14 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    user_dynamic
#
# Purpose
#    Detectors for 'user_dynamic'
#

from itertools                      import izip
from roundup.exceptions             import Reject
from roundup.date                   import Date
from roundup.cgi.TranslationService import get_translation

import common
import freeze
import user_dynamic

def check_ranges (cl, nodeid, user, valid_from, valid_to) :
    if valid_to :
        valid_to.hour   = valid_to.minute   = valid_to.second   = 0
    valid_from.hour     = valid_from.minute = valid_from.second = 0
    if valid_to and valid_from >= valid_to :
        raise Reject, \
            "valid_from (%(valid_from)s) must be > valid_to (%(valid_to)s)" \
            % locals ()
    dynrecs    = cl.find (user = user)
    empty_seen = False
    for dr in dynrecs :
        if dr == nodeid :
            continue
        r = cl.getnode (dr)
        rvalid_from, rvalid_to = (r.valid_from, r.valid_to)
        if not r.valid_to :
            assert (not empty_seen)
            empty_seen = True
            if (   valid_to
               and valid_from <= rvalid_from
               and valid_to   >  rvalid_from
               ) or (not valid_to and valid_from <= rvalid_from) :
                raise Reject, \
                    ( "%(valid_from)s;%(valid_to)s overlaps with "
                      "%(rvalid_from)s;"
                    % locals ()
                    )
        else :
            if not (  valid_from >= rvalid_to
                   or (valid_to and valid_to <= rvalid_from)
                   ) :
                # Don't display 'None':
                valid_to = valid_to or ''
                raise Reject, \
                    ( _ ("%(valid_from)s;%(valid_to)s overlaps with "
                         "%(rvalid_from)s;%(rvalid_to)s"
                        )
                    % locals ()
                    )
    return valid_from, valid_to
# end def check_ranges

def check_vacation (attr, new_values) :
    if attr in new_values :
        vacation = new_values [attr]
        if vacation is None :
            return
        if vacation <= 0 :
            raise Reject, \
                _ ( "%(attr)s must be positive or empty") % locals ()
# end def check_vacation

def hours_iter () :
    return ('hours_' + wday for wday in user_dynamic.wdays)
# end def hours_iter

def distribute_weekly_hours (h) :
    """ Distribute weekly hours (almost) evenly to workdays
        >>> distribute_weekly_hours (39)
        [7.75, 7.75, 7.75, 7.75, 8.0, 0.0, 0.0]
        >>> distribute_weekly_hours (38.5)
        [7.75, 7.75, 7.75, 7.75, 7.5, 0.0, 0.0]
        >>> distribute_weekly_hours (40)
        [8.0, 8.0, 8.0, 8.0, 8.0, 0.0, 0.0]
        >>> distribute_weekly_hours (41)
        [8.25, 8.25, 8.25, 8.25, 8.0, 0.0, 0.0]
        >>> distribute_weekly_hours (42)
        [8.5, 8.5, 8.5, 8.5, 8.0, 0.0, 0.0]
        >>> distribute_weekly_hours (42.25)
        [8.5, 8.5, 8.5, 8.5, 8.25, 0.0, 0.0]
        >>> distribute_weekly_hours (42.5)
        [8.5, 8.5, 8.5, 8.5, 8.5, 0.0, 0.0]
    """
    r = []
    d = user_dynamic.round_daily_work_hours (h / 5.)
    for n, f in enumerate (hours_iter ()) :
        dl = min (d, h)
        if n == 4 :
            dl = h
        r.append (dl)
        h -= dl
    return r
# end def distribute_weekly_hours

def check_overtime_parameters (db, cl, nodeid, new_values) :
    class X : pass
    ov_req = ['additional_hours', 'supp_per_period']
    fields = ov_req + ['weekly_hours', 'overtime_period', 'supp_weekly_hours']
    fields.extend (hours_iter ())
    for f in fields :
        if f in new_values :
            setattr (X, f, new_values [f])
        elif nodeid :
            setattr (X, f, cl.get (nodeid, f))
        else :
            setattr (X, f, None)
    ov = _ ('overtime_period')
    op = None
    if X.overtime_period :
        op = db.overtime_period.getnode (X.overtime_period)

    if op and not op.months and X.supp_per_period is not None :
        spp = _ ("supp_per_period")
        raise Reject, "%(spp)s must be empty for this %(ov)s" % locals ()
    if op and not op.weekly and X.supp_weekly_hours is not None :
        swh = _ ("supp_weekly_hours")
        raise Reject, "%(swh)s must be empty for this %(ov)s" % locals ()
    if op and op.required_overtime and X.additional_hours is not None :
       ah = _ ("additional_hours")
       raise Reject, "%(ah)s must be empty for this %(ov)s" % locals ()

    for f in ov_req :
        # don't allow 0 for additional_hours
        if  (   op
            and op.months
            and not op.required_overtime
            and (  getattr (X, f, None) is None
                or f == 'additional_hours' and not getattr (X, f, None)
                )
            ) :
            fld = _ (f)
            raise Reject, "%(fld)s must be specified if %(ov)s is set" \
                % locals ()
    if op and op.weekly and not getattr (X, 'supp_weekly_hours', None) :
        sh = _ ('supp_weekly_hours')
        raise Reject, "%(sh)s must be specified if %(ov)s is set" % locals ()
    daily = maybe_daily = False
    for f in hours_iter () :
        if f in new_values :
            maybe_daily = True
            if getattr (X, f) is not None :
                daily = True
                break
    else :
        if 'weekly_hours' in new_values and X.weekly_hours :
            if X.weekly_hours % .25 :
                wh = _ ("weekly_hours")
                raise Reject \
                    ("%(wh)s must be in whole quarter hours" % locals ())
            h = X.weekly_hours
            for k, v in izip (hours_iter (), distribute_weekly_hours (h)) :
                new_values [k] = v
                setattr (X, k, v)
            maybe_daily = False
            daily = False
    if daily or maybe_daily :
        sum = 0
        for f in hours_iter () :
            if getattr (X, f) is None :
                new_values [f] = 0
                setattr (X, f, 0)
            if getattr (X, f) % .25 :
                dh = _ (f)
                raise Reject \
                    ("%(dh)s must be in whole quarter hours" % locals ())
            sum += getattr (X, f)
        new_values ['weekly_hours'] = sum
        setattr (X, 'weekly_hours', sum)
    if  (   op
        and not op.weekly
        and op.months
        and not op.required_overtime
        and X.additional_hours != X.weekly_hours
        ) :
        ah = _ ('additional_hours')
        wh = _ ('weekly_hours')
        raise Reject, "%(ah)s must equal %(wh)s for monthly balance" % locals ()
# end def check_overtime_parameters

def update_user_olo_dept (db, user, olo, dept) :
    userupdate = {}
    if db.user.get (user, 'org_location') != olo :
        userupdate ['org_location'] = olo
    if db.user.get (user, 'department') != dept :
        userupdate ['department'] = dept
    if userupdate :
        db.user.set (user, **userupdate)
# end def update_user_olo_dept

def check_user_dynamic (db, cl, nodeid, new_values) :
    old_ot = cl.get (nodeid, 'overtime_period')
    for i in 'user', :
        if i in new_values and cl.get (nodeid, i) :
            raise Reject, "%(attr)s may not be changed" % {'attr' : _ (i)}
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'valid_from'
        , 'org_location'
        , 'department'
        , 'vacation_yearly'
        )
    user     = new_values.get ('user',         cl.get (nodeid, 'user'))
    old_from = cl.get (nodeid, 'valid_from')
    val_from = new_values.get ('valid_from',   old_from)
    val_to   = new_values.get ('valid_to',     cl.get (nodeid, 'valid_to'))
    olo      = new_values.get ('org_location', cl.get (nodeid, 'org_location'))
    dept     = new_values.get ('department',   cl.get (nodeid, 'department'))
    # Note: The valid_to date is *not* part of the validity interval of
    # the user_dynamic record. So when checking for frozen status we
    # can allow exactly the valid_to date.
    otw = common.overtime_period_week (db)
    nvk = list (sorted (new_values.keys ()))
    vac_fix = \
        (   (  nvk == ['vacation_day', 'vacation_month']
            or nvk == ['vacation_day', 'vacation_month', 'vacation_yearly']
            )
        and db.getuid () == '1'
        )
    if  (   freeze.frozen (db, user, old_from)
        and (  new_values.keys () != ['valid_to']
            or not val_to
            or freeze.frozen (db, user, val_to)
            )
        and (  db.getuid () != '1'
            or old_ot
            or not otw
            or new_values != dict (overtime_period = otw.id)
            )
        and not vac_fix
        ) :
        raise Reject, _ ("Frozen: %(old_from)s") % locals ()
    last = user_dynamic.last_user_dynamic (db, user)
    if  (   ('org_location' in new_values or 'department' in new_values)
        and (not val_to or last.id == nodeid or last.valid_from < val_from)
        ) :
        update_user_olo_dept (db, user, olo, dept)
    if 'valid_from' in new_values or 'valid_to' in new_values :
        new_values ['valid_from'], new_values ['valid_to'] = \
            check_ranges (cl, nodeid, user, val_from, val_to)
        val_from = new_values ['valid_from']
        val_to   = new_values ['valid_to']
    if not vac_fix :
        check_overtime_parameters (db, cl, nodeid, new_values)
        check_vacation ('vacation_yearly', new_values)
        if not freeze.frozen (db, user, old_from) :
            user_dynamic.invalidate_tr_duration (db, user, val_from, val_to)
        else :
            old_to = cl.get (nodeid, 'valid_to')
            use_to = val_to
            if old_to :
                if val_to :
                    use_to = min (old_to, val_to)
                else :
                    use_to = old_to
            user_dynamic.invalidate_tr_duration (db, user, use_to, None)
    check_weekly_hours (db, cl, nodeid, new_values)
# end def check_user_dynamic

def set_otp_if_all_in (db, cl, nodeid, new_values) :
    if 'all_in' in new_values and new_values ['all_in'] :
        new_values ['overtime_period'] = None
# end def set_otp_if_all_in

def new_user_dynamic (db, cl, nodeid, new_values) :
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'user'
        , 'valid_from'
        , 'org_location'
        , 'department'
        , 'vacation_yearly'
        )
    user       = new_values ['user']
    valid_from = new_values ['valid_from']
    valid_to   = new_values.get ('valid_to', None)
    olo        = new_values ['org_location']
    dept       = new_values ['department']
    if freeze.frozen (db, user, valid_from) :
        raise Reject, _ ("Frozen: %(valid_from)s") % locals ()
    last = user_dynamic.last_user_dynamic (db, user)
    if not valid_to or not last or last.valid_from < valid_from :
        update_user_olo_dept (db, user, olo, dept)
    if 'durations_allowed' not in new_values :
        new_values ['durations_allowed'] = False
    new_values ['valid_from'], new_values ['valid_to'] = \
        check_ranges (cl, nodeid, user, valid_from, valid_to)
    check_overtime_parameters (db, cl, nodeid, new_values)
    user_dynamic.invalidate_tr_duration \
        (db, user, new_values ['valid_from'], new_values ['valid_to'])
    orgl = db.org_location.getnode (olo)
    prev_dyn = user_dynamic.find_user_dynamic (db, user, valid_from, '-')
    if 'vacation_month' not in new_values and 'vacation_day' not in new_values :
        if prev_dyn :
            new_values ['vacation_month'] = prev_dyn.vacation_month
            new_values ['vacation_day']   = prev_dyn.vacation_day
        elif orgl.vacation_legal_year :
            new_values ['vacation_month'] = 1
            new_values ['vacation_day']   = 1
        else :
            d = new_values ['valid_from']
            month, mday = (int (x) for x in d.get_tuple () [1:3])
            if month == 2 and mday == 29 :
                mday = 28
            new_values ['vacation_month'] = month
            new_values ['vacation_day']   = mday
    if 'vacation_yearly' not in new_values :
        if prev_dyn :
            new_values ['vacation_yearly'] = prev_dyn.vacation_yearly
        elif orgl.vacation_yearly :
            new_values ['vacation_yearly'] = orgl.vacation_yearly
    check_vacation ('vacation_yearly', new_values)
    check_weekly_hours (db, cl, nodeid, new_values)
# end def new_user_dynamic

def check_weekly_hours (db, cl, nodeid, new_values) :
    spp = new_values.get ('supp_per_period')
    if spp is None and nodeid :
        spp = cl.get (nodeid, 'supp_per_period')
    swh = new_values.get ('supp_weekly_hours')
    if swh is None and nodeid :
        swh = cl.get (nodeid, 'supp_weekly_hours')
    wh  = new_values.get ('weekly_hours')
    if wh is None and nodeid :
        wh = cl.get (nodeid, 'weekly_hours')
    if spp or swh :
        common.require_attributes (_, cl, nodeid, new_values, 'weekly_hours')
        # weekly_hours must not be 0 in case we have overtime
        if not wh :
            msg = ''"Weekly hours must not be 0 when user has " \
                  "supplementary hours (weeky or otherwise)"
            raise Reject (_ (msg))
# end def check_weekly_hours

def user_dyn_react (db, cl, nodeid, old_values) :
    """ If this is the first user_dynamic record for this user: create
        or update initial vacation_correction record if
        'do_leave_process' is set on the org_location.
    """
    dyn  = cl.getnode (nodeid)
    if not dyn.vacation_yearly :
        return
    if not db.org_location.get (dyn.org_location, 'do_leave_process') :
        return
    ud   = db.user_dynamic.filter (None, dict (user = dyn.user))
    if len (ud) == 1 :
        assert ud [0] == nodeid
        year = dyn.valid_from.get_tuple () [0]
        date = Date \
            ('%s-%02d-%02d' % (year, dyn.vacation_month, dyn.vacation_day))
        vc = db.vacation_correction.filter (None, dict (user = dyn.user))
        if len (vc) == 1 and not freeze.frozen (db, dyn.user, date) :
            db.vacation_correction.set \
                (vc [0], date = date, absolute = True, days = 0)
        elif len (vc) == 0 and old_values is None :
            db.vacation_correction.create \
                (user = dyn.user, date = date, absolute = True, days = 0)
# end def user_dyn_react

def close_existing (db, cl, nodeid, old_values) :
    """ Check if there is already a user_dynamic record with no valid_to
        date. If there is one and the current record created also has no
        valid_to date, we set the valid_to of the found record to the
        valid_from of the current record.
    """
    current = cl.getnode (nodeid)
    dynrecs = cl.find (user = current.user)
    for dr in dynrecs :
        if dr == nodeid :
            continue
        r = cl.getnode (dr)
        if not r.valid_to and current.valid_from >= r.valid_from :
            cl.set (dr, valid_to = current.valid_from)
            break
# end def close_existing

def overtime_check (db, cl, nodeid, new_values) :
    if not nodeid and 'required_overtime' not in new_values :
        new_values ['required_overtime'] = False
    common.require_attributes \
        (_, cl, nodeid, new_values
        , 'name', 'months', 'weekly', 'required_overtime'
        )
    if 'months' in new_values :
        months = new_values ['months'] = int (new_values ['months'])
    else :
        months = int (cl.get (nodeid, 'months'))
    if 'weekly' in new_values :
        weekly = new_values ['weekly']
    else :
        weekly = cl.get (nodeid, 'weekly')
    if 'required_overtime' in new_values :
        rov    = new_values ['required_overtime']
    else :
        rov    = cl.get (nodeid, 'required_overtime')
    same   = cl.filter \
        (None, dict (months = months, weekly = weekly, required_overtime = rov))
    mname  = _ ("months")
    wname  = _ ("weekly")
    rname  = _ ("required_overtime")
    if same and (len (same) > 1 or same [0] != nodeid) :
        raise Reject, _ \
            ("No entries with same %(mname)s, %(wname)s, %(rname)s allowed") \
            % locals ()
    if not months and not weekly :
        raise Reject, _ \
            ("One of %(mname)s, %(wname)s must be specified") % locals ()
    if months < 0 or months and 12 % months :
        raise Reject, _ \
            ("Invalid number of %(mname)s, must be 0 or a divisor of 12") \
            % locals ()
    if rov and months != 1 :
        raise Reject, _ \
            ("Invalid number of %(mname)s, must be 1 if %(rname)s is given") \
            % locals ()
    if rov and weekly :
        raise Reject, _ \
            ("Only one of %(rname)s, %(wname)s is allowed") % locals ()
# end def overtime_check

def vacation_check (db, cl, nodeid, new_values) :
    mlist = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if  (   new_values.get ('vacation_day') is None
        and new_values.get ('vacation_month') is None
        and new_values.get ('vacation_yearly') is None
        ) :
        return
    # if one attribute is defined, all need to be
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'vacation_month', 'vacation_day', 'vacation_yearly'
        )
    vm = new_values.get ('vacation_month')
    vd = new_values.get ('vacation_day')
    vy = new_values.get ('vacation_yearly')
    if vm is None and nodeid :
        vm = cl.get (nodeid, 'vacation_month')
    if vd is None and nodeid :
        vd = cl.get (nodeid, 'vacation_day')
    if vy is None and nodeid :
        vy = cl.get (nodeid, 'vacation_yearly')
    vm = int (vm)
    vd = int (vd)
    vy = int (vy)
    if vm < 1 or vm > 12 :
        raise Reject (_ ("Wrong month: %(vm)s" % locals ()))
    if vd < 1 or vd > mlist [vm - 1] :
        raise Reject (_ ("Wrong day of month: %(vm)s-%(vd)s" % locals ()))
    new_values ['vacation_yearly'] = vy
    new_values ['vacation_month']  = vm
    new_values ['vacation_day']    = vd
# end def vacation_check

def init (db) :
    if 'user_dynamic' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.user_dynamic.audit    ("create", new_user_dynamic)
    db.user_dynamic.audit    ("set",    check_user_dynamic)
    db.user_dynamic.audit    ("create", vacation_check, priority = 120)
    db.user_dynamic.audit    ("set",    vacation_check, priority = 120)
    db.user_dynamic.audit    ("create", set_otp_if_all_in, priority = 20)
    db.user_dynamic.audit    ("set",    set_otp_if_all_in, priority = 20)
    db.user_dynamic.react    ("create", close_existing)
    db.user_dynamic.react    ("create", user_dyn_react)
    db.user_dynamic.react    ("set",    user_dyn_react)
    db.overtime_period.audit ("create", overtime_check)
    db.overtime_period.audit ("set",    overtime_check)
# end def init

### __END__ user_dynamic
