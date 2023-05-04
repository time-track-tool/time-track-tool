#! /usr/bin/python
# Copyright (C) 2006-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    d_user_dynamic
#
# Purpose
#    Detectors for 'user_dynamic'
#

try :
    from itertools import izip
except ImportError :
    izip = zip
from roundup.exceptions             import Reject
from roundup.date                   import Date

import common
import freeze
import user_dynamic
import vacation
import lib_auto_wp

def check_ranges (cl, nodeid, user, valid_from, valid_to, allow_same = False) :
    """ We allow valid_to == valid_from if allow_same is True
        This results in the record to be retired.
        Of course the caller will set allow_same = False for new records.
    """
    _ = cl.db.i18n.gettext
    if valid_to :
        valid_to.hour   = valid_to.minute   = valid_to.second   = 0
    valid_from.hour     = valid_from.minute = valid_from.second = 0
    if  (   valid_to
        and (  valid_from > valid_to
            or (not allow_same and valid_from == valid_to)
            )
        ) :
        raise Reject \
            (_ ("valid_from (%(valid_from)s) must be > valid_to (%(valid_to)s)")
            % locals ()
            )
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
                raise Reject \
                    (_ ("%(valid_from)s;%(valid_to)s overlaps with "
                        "%(rvalid_from)s;"
                       )
                    % locals ()
                    )
        else :
            # The third case is the one where an existing record is
            # split into two records, this is explicitly allowed
            if not (  valid_from >= rvalid_to
                   or (valid_to and valid_to <= rvalid_from)
                   or (   valid_to and valid_to == rvalid_to
                      and valid_from > rvalid_from
                      and valid_from < rvalid_to
                      )
                   ) :
                # Don't display 'None':
                valid_to = valid_to or ''
                raise Reject \
                    ( _ ("%(valid_from)s;%(valid_to)s overlaps with "
                         "%(rvalid_from)s;%(rvalid_to)s"
                        )
                    % locals ()
                    )
    return valid_from, valid_to
# end def check_ranges

def check_vacation (db, cl, nodeid, attr, new_values) :
    _ = db.i18n.gettext
    vacation = None
    if attr in new_values :
        vacation = new_values [attr]
    elif nodeid :
        vacation = cl.get (nodeid, attr)

    if vacation is None :
        need_vacation = False
        olo = new_values.get ('org_location', None)
        if olo is None and nodeid :
            olo = cl.get (nodeid, 'org_location')
        if olo :
            o = db.org_location.getnode (olo)
            if o.do_leave_process :
                need_vacation = True
        user = new_values.get ('user', None)
        if user is None and nodeid :
            user = cl.get (nodeid, 'user')
        assert user
        ct = None
        if 'contract_type' in new_values :
            ct = new_values ['contract_type']
        elif nodeid :
            ct = cl.get (nodeid, 'contract_type')
        if ct is None :
            ct = -1
        vcorr = db.vacation_correction.filter \
            (None, dict (user = user, absolute = True, contract_type = ct))
        if 'valid_to' in new_values :
            vto = new_values ['valid_to']
        elif nodeid :
            vto = cl.get (nodeid, 'valid_to')
        for vc in vcorr :
            if not vto :
                need_vacation = True
                break
            vac_corr = db.vacation_correction.getnode (vc)
            if vac_corr.date < vto :
                need_vacation = True
                break
        if need_vacation :
            raise Reject \
                (_ ( "%(attr)s is required") % locals ())
    elif vacation <= 0 :
        raise Reject \
            (_ ( "%(attr)s must be positive or empty") % locals ())
    if vacation :
        vac_aliq = None
        if 'vac_aliq' in new_values :
            vac_aliq = new_values ['vac_aliq']
        elif nodeid :
            vac_aliq = cl.get (nodeid, 'vac_aliq')
        if not vac_aliq :
            # org_location is checked to exist
            if 'org_location' in new_values :
                olo = new_values ['org_location']
            else :
                olo = cl.get (nodeid, 'org_location')
            olo = db.org_location.getnode (olo)
            if olo.vac_aliq :
                new_values ['vac_aliq'] = olo.vac_aliq
            else :
                # Take first value
                new_values ['vac_aliq'] = '1'
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
    _ = db.i18n.gettext
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
        raise Reject (_ ("%(spp)s must be empty for this %(ov)s") % locals ())
    if op and not op.weekly and X.supp_weekly_hours is not None :
        swh = _ ("supp_weekly_hours")
        raise Reject (_ ("%(swh)s must be empty for this %(ov)s") % locals ())
    if op and op.required_overtime and X.additional_hours is not None :
       ah = _ ("additional_hours")
       raise Reject (_ ("%(ah)s must be empty for this %(ov)s") % locals ())

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
            raise Reject \
                (_ ("%(fld)s must be specified if %(ov)s is set") % locals ())
    if op and op.weekly and not getattr (X, 'supp_weekly_hours', None) :
        sh = _ ('supp_weekly_hours')
        raise Reject \
            (_ ("%(sh)s must be specified if %(ov)s is set") % locals ())
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
                    (_ ("%(wh)s must be in whole quarter hours") % locals ())
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
                    (_ ("%(dh)s must be in whole quarter hours") % locals ())
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
        raise Reject \
            (_ ("%(ah)s must equal %(wh)s for monthly balance") % locals ())
# end def check_overtime_parameters

def check_user_dynamic (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    old_ot = cl.get (nodeid, 'overtime_period')
    for i in 'user', :
        if i in new_values and cl.get (nodeid, i) :
            raise Reject (_ ("%(attr)s may not be changed") % {'attr' : _ (i)})
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'valid_from'
        , 'org_location'
        )
    user     = new_values.get ('user',         cl.get (nodeid, 'user'))
    old_from = cl.get (nodeid, 'valid_from')
    val_from = new_values.get ('valid_from',   old_from)
    val_to   = new_values.get ('valid_to',     cl.get (nodeid, 'valid_to'))
    olo      = new_values.get ('org_location', cl.get (nodeid, 'org_location'))
    # Note: The valid_to date is *not* part of the validity interval of
    # the user_dynamic record. So when checking for frozen status we
    # can allow exactly the valid_to date.
    otw = common.overtime_period_week (db)
    nvk = list (sorted (new_values))
    old_flexmax = cl.get (nodeid, 'max_flexitime')
    vac_all  = ('vacation_day', 'vacation_month', 'vacation_yearly', 'vac_aliq')
    vac_aliq = cl.get (nodeid, 'vac_aliq')
    vac_fix  = \
        (   set (nvk) <= set (vac_all)
        and 'vac_aliq' not in nvk or vac_aliq is None
        and db.getuid () == '1'
        )
    flexi_fix = \
        list (new_values) == ['max_flexitime'] and old_flexmax is None
    exemption = \
        (   list (new_values) == ['exemption']
        and new_values ['exemption'] == False
        and db.getuid () == '1'
        )
    if  (   freeze.frozen (db, user, old_from)
        and (  list (new_values) != ['valid_to']
            or not val_to
            or freeze.frozen (db, user, val_to)
            )
        and (  db.getuid () != '1'
            or old_ot
            or not otw
            or new_values != dict (overtime_period = otw.id)
            )
        and (db.getuid () != '1' or not flexi_fix)
        and not vac_fix
        and not exemption
        ) :
        raise Reject (_ ("Frozen: %(old_from)s") % locals ())
    last = user_dynamic.last_user_dynamic (db, user)
    if 'valid_from' in new_values or 'valid_to' in new_values :
        new_values ['valid_from'], new_values ['valid_to'] = \
            check_ranges \
                (cl, nodeid, user, val_from, val_to, allow_same = True)
        val_from = new_values ['valid_from']
        val_to   = new_values ['valid_to']
    if not vac_fix and not flexi_fix and not exemption :
        check_overtime_parameters (db, cl, nodeid, new_values)
        check_vacation (db, cl, nodeid, 'vacation_yearly', new_values)
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
    if not exemption :
        check_weekly_hours (db, cl, nodeid, new_values)
# end def check_user_dynamic

def set_otp_if_all_in (db, cl, nodeid, new_values) :
    if 'all_in' in new_values and new_values ['all_in'] :
        new_values ['overtime_period'] = None
# end def set_otp_if_all_in

def max_flexi (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    if 'all_in' in new_values or 'max_flexitime' in new_values :
        ft = new_values.get ('max_flexitime')
        if ft is None and nodeid :
            ft = cl.get (nodeid, 'max_flexitime')
        ai = new_values.get ('all_in')
        if ai is None and nodeid :
            ai = cl.get (nodeid, 'all_in')
        if ai :
            common.require_attributes \
                (_, cl, nodeid, new_values, 'max_flexitime')
        else :
            new_values ['max_flexitime'] = None
# end def max_flexi

def check_avc (db, cl, nodeid, new_values) :
    """ Check that an absolute vacation correction exists at the date of
        the user_dynamic record if either the vac_aliq changed or the
        vac_aliq is monthly and the vacation changed (compared to the
        last user_dynamic record). We currently do not require a
        vacation correction if one already exists *and* there is a gap
        in user_dynamic record validity ranges.
    """
    _ = db.i18n.gettext
    # At least one of the following attributes must be in new_values
    # otherwise we don't have anything to check.
    attrs = ('vac_aliq', 'vacation_yearly', 'valid_from')
    for a in attrs :
        if a in new_values :
            break
    else :
        return
    va = new_values.get ('vac_aliq')
    if not va and nodeid :
        va = cl.get (nodeid, 'vac_aliq')
    vy = new_values.get ('vacation_yearly')
    if vy is None and nodeid :
        vy = cl.get (nodeid, 'vacation_yearly')
    # User must exist
    user = new_values.get ('user')
    if not user :
        user = cl.get (nodeid, 'user')
    # valid_from must exist
    valid_from = new_values.get ('valid_from')
    if not valid_from :
        valid_from = cl.get (nodeid, 'valid_from')
    prev_dyn = user_dynamic.find_user_dynamic (db, user, valid_from, '-')
    if not prev_dyn :
        return
    # Check if there is an absolute vacation correction for our
    # valid_from, everything ok if there is:
    dt  = valid_from.pretty (common.ymd)
    vcs = db.vacation_correction.filter \
        (None, dict (user = user, date = dt, absolute = True))
    assert len (vcs) <= 1
    if not vcs :
        # Find the next vc backwards and check if it is at the end of
        # employment, sort negative by date, i.e. newest first
        vcs = db.vacation_correction.filter \
            ( None
            , dict (user = user, date = ';%s' % dt, absolute = True)
            , sort = ('-', 'date')
            )
        if vcs :
            vc = db.vacation_correction.getnode (vcs [0])
            day = common.day
            # - day because we don't want to find the currently-change dyn
            vcdyn = user_dynamic.last_user_dynamic (db, user, valid_from - day)
            if not vcdyn.valid_to or vcdyn.valid_to > vc.date + day :
                vcs = []
    if vcs :
        assert db.vacation_correction.get (vcs [0], 'date') <= valid_from
        return
    if prev_dyn.vac_aliq != va :
        van = _ ('vac_aliq')
        raise Reject \
            ( _ ('Change of "%(van)s" without absolute vacation correction')
            % locals ()
            )
    vyo = prev_dyn.vacation_yearly
    if db.vac_aliq.get (va, 'name') == 'Monthly' and vy != vyo :
        vyn = _ ('vacation_yearly')
        raise Reject \
            ( _ ('Change of "%(vyn)s" without absolute vacation correction')
            % locals ()
            )
# end def check_avc

def new_user_dynamic (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'user'
        , 'valid_from'
        , 'org_location'
        )
    user       = new_values ['user']
    valid_from = new_values ['valid_from']
    valid_to   = new_values.get ('valid_to', None)
    olo        = new_values ['org_location']
    if freeze.frozen (db, user, valid_from) :
        raise Reject (_ ("Frozen: %(valid_from)s") % locals ())
    last = user_dynamic.last_user_dynamic (db, user)
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
    check_vacation (db, cl, nodeid, 'vacation_yearly', new_values)
    check_weekly_hours (db, cl, nodeid, new_values)
# end def new_user_dynamic

def check_weekly_hours (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
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
                  "supplementary hours (weekly or otherwise)"
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
        # Probably something ancient being modified during an update:
        if dyn.vacation_month is None or dyn.vacation_day is None :
            return
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

def try_fix_vacation (db, cl, nodeid, old_values) :
    """ If the working time per day is changed for a user we need to
        correct the already-booked vacations in that time-range.
        We also need to correct public holidays.
    """
    days  = 'mon tue wed thu fri sat sun'.split ()
    props = list ('hours_' + x for x in days)
    props.append ('weekly_hours')
    props.append ('valid_from')
    props.append ('valid_to')
    item = cl.getnode (nodeid)
    if old_values is not None :
        for p in props :
            if p in old_values and item [p] != old_values [p] :
                break
        else :
            return
    to = item.valid_to
    if to :
        to = to - common.day
    vacation.update_public_holidays (db, cl.getnode (nodeid))
    vacation.fix_vacation (db, item.user, item.valid_from, to)
# end def try_fix_vacation

def retire_if_empty_range (db, cl, nodeid, old_values) :
    """ If valid_from == valid_to retire this record
    """
    node = cl.getnode (nodeid)
    if node.valid_from == node.valid_to :
        cl.retire (nodeid)
# end def retire_if_empty_range

def close_existing (db, cl, nodeid, old_values) :
    """ Check if there is already a user_dynamic record with the same
        valid_to date or empty. This can either mean the valid_to is
        empty for the existing record or the same date for both records
        (including both empty). If there is one that fulfill these
        conditions, we set the valid_to of the found record to the
        valid_from of the current record.
    """
    current = cl.getnode (nodeid)
    dynrecs = cl.find (user = current.user)
    for dr in dynrecs :
        if dr == nodeid :
            continue
        r = cl.getnode (dr)
        if  (   (current.valid_to  == r.valid_to or r.valid_to is None)
            and current.valid_from >= r.valid_from
            ) :
            cl.set (dr, valid_to = current.valid_from)
            break
# end def close_existing

def overtime_check (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
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
        raise Reject \
            (_ ("No entries with same %(mname)s, %(wname)s, %(rname)s allowed")
            % locals ()
            )
    if not months and not weekly :
        raise Reject \
            (_ ("One of %(mname)s, %(wname)s must be specified") % locals ())
    if months < 0 or months and 12 % months :
        raise Reject \
            (_ ("Invalid number of %(mname)s, must be 0 or a divisor of 12")
            % locals ()
            )
    if rov and months != 1 :
        raise Reject \
            (_ ("Invalid number of %(mname)s, must be 1 if %(rname)s is given")
            % locals ()
            )
    if rov and weekly :
        raise Reject \
            (_ ("Only one of %(rname)s, %(wname)s is allowed") % locals ())
# end def overtime_check

def vacation_check (db, cl, nodeid, new_values) :
    """Check correctness of vacation_day/month/yearly entires"""
    _ = db.i18n.gettext
    mlist = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # if nothing changed, return
    if  (   new_values.get ('vacation_day') is None
        and new_values.get ('vacation_month') is None
        and new_values.get ('vacation_yearly') is None
        ) :
        return
    # if one attribute is defined, all need to be
    # create error if not all attributes are set
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'vacation_month', 'vacation_day', 'vacation_yearly'
        )
    # if we have all attributes, check them
    # handle set and create method
    # for create and set if values changed
    vm = new_values.get ('vacation_month')
    vd = new_values.get ('vacation_day')
    vy = new_values.get ('vacation_yearly')
    # value did not change
    if vm is None and nodeid :
        vm = cl.get (nodeid, 'vacation_month')
    if vd is None and nodeid :
        vd = cl.get (nodeid, 'vacation_day')
    if vy is None and nodeid :
        vy = cl.get (nodeid, 'vacation_yearly')
    vm = int (vm)
    vd = int (vd)
    vy = float (int (vy))
    if vm < 1 or vm > 12 :
        raise Reject (_ ("Wrong month: %(vm)s" % locals ()))
    if vd < 1 or vd > mlist [vm - 1] :
        raise Reject (_ ("Wrong day of month: %(vm)s-%(vd)s" % locals ()))
    new_values ['vacation_yearly'] = vy
    new_values ['vacation_month']  = vm
    new_values ['vacation_day']    = vd
# end def vacation_check

def olo_check (db, cl, nodeid, new_values) :
    """ Require vac_aliq if do_leave_process is turned on """
    lp = new_values.get ('do_leave_process')
    if lp is None and nodeid :
        lp = cl.get (nodeid, 'do_leave_process')
    if lp :
        common.require_attributes \
            (db.i18n.gettext, cl, nodeid, new_values, 'vac_aliq')
# end def olo_check

def find_existing_leave (db, cl, nodeid, new_values) :
    """ Search for existing leave requests when start/end date changes.
        Reject if valid records are found.
    """
    _ = db.i18n.gettext
    stati = ('open', 'submitted', 'accepted', 'cancel requested')
    stati = list (db.leave_status.lookup (x) for x in stati)
    if 'valid_to' not in new_values and 'valid_from' not in new_values :
        return
    dyn = cl.getnode (nodeid)
    if 'valid_to' in new_values :
        # check if another dynamic user record exists
        valid_to = new_values ['valid_to']
        if valid_to is not None :
            next = user_dynamic.next_user_dynamic (db, dyn)
            if not next or next.valid_from > valid_to :
                leaves = db.leave_submission.filter \
                    ( None
                    , dict
                        ( user     = dyn.user
                        , last_day = common.pretty_range (valid_to)
                        , status   = stati
                        )
                    )
                if next :
                    new_leaves = []
                    for id in leaves :
                        leave = db.leave_submission.getnode (id)
                        if valid_to <= leave.first_day < next.valid_from :
                            new_leaves.append (id)
                            continue
                        if valid_to <= leave.last_day < next.valid_from :
                            new_leaves.append (id)
                            continue
                        if  (   leave.first_day < valid_to
                            and leave.last_day >= next.valid_from
                            ) :
                            new_leaves.append (id)
                            continue
                    leaves = new_leaves
                if leaves :
                    raise Reject \
                        (_ ("There are open leave requests at or after %s"
                           % valid_to.pretty (common.ymd)
                           )
                        )

    if 'valid_from' in new_values :
        # check if another dynamic user record exists
        valid_from = new_values ['valid_from']
        prev = user_dynamic.prev_user_dynamic (db, dyn)
        if not prev or prev.valid_to < valid_from :
            leaves = db.leave_submission.filter \
                ( None
                , dict
                    ( user      = dyn.user
                    , first_day = common.pretty_range (None, valid_from - common.day)
                    , status    = stati
                    )
                )
            if prev :
                new_leaves = []
                for id in leaves :
                    leave = db.leave_submission.getnode (id)
                    if prev.valid_to <= leave.first_day < valid_from :
                        new_leaves.append (id)
                        continue
                    if prev.valid_to <= leave.last_day < valid_from :
                        new_leaves.append (id)
                        continue
                    if  (   leave.first_day < prev.valid_to
                        and leave.last_day >= valid_from
                        ) :
                        new_leaves.append (id)
                        continue
                leaves = new_leaves
            if leaves :
                raise Reject \
                    (_ ("There are open leave requests before %s"
                        % valid_from.pretty (common.ymd)
                        )
                    )
# end def find_existing_leave

def find_time_records (db, cl, nodeid, new_values) :
    """ Search for existing time records when start/end date changes.
        Reject if valid records other than public holidays are found.
    """
    _ = db.i18n.gettext
    if 'valid_to' not in new_values and 'valid_from' not in new_values :
        return
    dyn = cl.getnode (nodeid)
    valid_to   = new_values.get ('valid_to')
    valid_from = new_values.get ('valid_from')
    next = user_dynamic.next_user_dynamic (db, dyn)
    prev = user_dynamic.prev_user_dynamic (db, dyn)
    to = next and (next.valid_from - common.day)
    frm = prev and (prev.valid_to)
    ranges = dict \
        ( valid_to   = common.pretty_range (valid_to, to)
        , valid_from = common.pretty_range (frm, valid_from - common.day)
        )
    gaps = dict \
        ( valid_to   = not next or next.valid_from > valid_to
        , valid_from = not prev or prev.valid_to   < valid_from
        )
    msgs = dict \
        ( valid_to   = _
            ( "There are (non public holiday) "
              "time records at or after %s"
            )
        , valid_from = _
            ( "There are (non public holiday) "
              "time records before %s"
            )
        )
    for k in ('valid_to', 'valid_from') :
        value = new_values.get (k)
        if value is not None and gaps [k] :
            trs = db.time_record.filter \
                ( None
                , { 'daily_record.user': dyn.user
                  , 'daily_record.date': ranges [k]
                  }
                )
            # loop for checking if time recs are public holiday
            for id in trs :
                tr = db.time_record.getnode (id)
                # case where no wp was entered yet
                if tr.wp is None :
                    raise Reject (msgs [k] % value.pretty (common.ymd))
                # case where wp was set
                wp = db.time_wp.getnode (tr.wp)
                tc = db.time_project.getnode (wp.project)
                if not tc.is_public_holiday :
                    raise Reject (msgs [k] % value.pretty (common.ymd))
            # loop entirely for retiring public holidys
            for id in trs :
                tr = db.time_record.getnode (id)
                assert tr.wp
                wp = db.time_wp.getnode (tr.wp)
                tc = db.time_project.getnode (wp.project)
                assert tc.is_public_holiday
                db.time_record.retire (id)
# end def find_time_records

def _auto_wp_loop (db, d, uid) :
    auto_wp = db.auto_wp.filter (None, d)
    for aid in auto_wp :
        lib_auto_wp.check_auto_wp (db, aid, uid)
# end _auto_wp_loop

def auto_wp_loop (db, dyn, old_olo = None, old_ct = None) :
    """ Find auto_wps for this setting and call updater
    """
    # First handle *old* auto_wps (close wps)
    if old_olo or old_ct :
        d = dict \
            ( contract_type = old_ct or dyn.contract_type or '-1'
            , is_valid      = True
            , org_location  = old_olo or dyn.org_location
            )
        _auto_wp_loop (db, d, dyn.user)
    # Then handle new ones
    d   = dict \
        ( contract_type = dyn.contract_type or '-1'
        , is_valid      = True
        , org_location  = dyn.org_location
        )
    _auto_wp_loop (db, d, dyn.user)
# end def auto_wp_loop

def auto_wp_magic (db, cl, nodeid, old_values) :
    """ Whenever properties relevant for auto workpackage processing are
        touched, we call the auto_wp routine
    """
    props = \
        ( 'booking_allowed'
        , 'contract_type'
        , 'do_auto_wp'
        , 'org_location'
        , 'valid_from'
        , 'valid_to'
        , 'all_in'
        )
    dyn = cl.getnode (nodeid)
    # Only check if do_auto_wp is set and some of the relevant
    # attributes changed *or* the do_auto_wp attribute changed
    if old_values :
        if 'contract_type' in old_values or 'org_location' in old_values :
            # Handle *old* values which change the used auto_wp first
            if  (  dyn.org_location  != old_values ['org_location']
                or dyn.contract_type != old_values ['contract_type']
                ) :
                auto_wp_loop \
                    ( db, dyn
                    , old_olo = old_values ['org_location']
                    , old_ct  = old_values ['contract_type'] or '-1'
                    )
        if dyn.do_auto_wp :
            for p in props :
                if p in old_values and getattr (dyn, p) != old_values [p] :
                    auto_wp_loop (db, dyn)
                    break
        else :
            p = 'do_auto_wp'
            if p in old_values and getattr (dyn, p) != old_values [p] :
                auto_wp_loop (db, dyn)
    elif dyn.do_auto_wp :
        # For new record we only need to call the updater if do_auto_wp
        auto_wp_loop (db, dyn)
# end def auto_wp_magic

def auto_wp_check (db, cl, nodeid, new_values) :
    """ Check auto_wp properties
    """
    _ = db.i18n.gettext
    # These properties must not change:
    props = \
        ( 'contract_type'
        , 'org_location'
        , 'time_project'
        )
    if nodeid :
        for p in props :
            if p in new_values :
                raise Reject (_ ('Property "%s" must not change') % _ (p))
    else :
        common.require_attributes \
            ( _, cl, nodeid, new_values
            , 'org_location'
            , 'time_project'
            , 'name'
            )
        if 'durations_allowed' not in new_values :
            new_values ['durations_allowed'] = False
        if 'is_valid' not in new_values :
            new_values ['is_valid'] = False
        if 'all_in' not in new_values :
            new_values ['all_in'] = True
# end def auto_wp_check

def auto_wp_modify (db, cl, nodeid, old_values) :
    """ Generate/Modify WPs for new/changed auto_wp
    """
    # Find all dynamic user records that have do_auto_wp enabled and
    # use a contract type and org_location that matches.
    auto_wp = cl.getnode (nodeid)
    ct      = auto_wp.contract_type or '-1'
    d       = dict \
        ( contract_type = ct
        , org_location  = auto_wp.org_location
        , do_auto_wp    = True
        )
    dynids  = db.user_dynamic.filter (None, d)
    users   = {}
    for dynid in dynids :
        dyn = db.user_dynamic.getnode (dynid)
        users [dyn.user] = True
    for u in users :
        lib_auto_wp.check_auto_wp (db, nodeid, u)
# end def auto_wp_modify

def auto_wp_change_da (db, cl, nodeid, old_values) :
    """ Fix all not-completely-frozen WP when durations_allowed changes
    """
    dao = old_values.get ('durations_allowed', None)
    dan = cl.get (nodeid, 'durations_allowed')
    # Only do something if durations_allowed changed
    if dao == dan :
        return
    wps = db.time_wp.filter \
        (None, dict (auto_wp = nodeid), sort = ('+', 'bookers'))
    uid = None
    fdt = None
    for wpid in wps :
        wp = db.time_wp.getnode (wpid)
        if wp.durations_allowed == dan :
            continue
        assert len (wp.bookers) == 1
        if uid != wp.bookers [0] :
            uid = wp.bookers [0]
            fdt = freeze.freeze_date (db, uid)
        if wp.time_end and wp.time_end < fdt :
            continue
        db.time_wp.set (wpid, durations_allowed = dan)
# end def auto_wp_change_da

def init (db) :
    if 'user_dynamic' not in db.classes :
        return
    db.user_dynamic.audit    ("create", new_user_dynamic)
    db.user_dynamic.audit    ("set",    check_user_dynamic)
    db.user_dynamic.audit    ("create", vacation_check, priority = 120)
    db.user_dynamic.audit    ("set",    vacation_check, priority = 120)
    db.user_dynamic.audit    ("create", set_otp_if_all_in, priority = 20)
    db.user_dynamic.audit    ("set",    set_otp_if_all_in, priority = 20)
    db.user_dynamic.audit    ("create", max_flexi)
    db.user_dynamic.audit    ("set",    max_flexi)
    db.user_dynamic.audit    ("create", check_avc, priority = 150)
    db.user_dynamic.audit    ("set",    check_avc, priority = 150)
    db.user_dynamic.react    ("create", close_existing)
    db.user_dynamic.react    ("create", user_dyn_react)
    db.user_dynamic.react    ("set",    user_dyn_react)
    db.user_dynamic.react    ("set",    try_fix_vacation)
    db.user_dynamic.react    ("create", try_fix_vacation)
    db.user_dynamic.audit    ("set",    find_existing_leave)
    db.user_dynamic.audit    ("set",    find_time_records, priority = 120)
    db.user_dynamic.react    ("set",    retire_if_empty_range, priority = 200)
    db.overtime_period.audit ("create", overtime_check)
    db.overtime_period.audit ("set",    overtime_check)
    db.org_location.audit    ("create", olo_check)
    db.org_location.audit    ("set",    olo_check)
    db.user_dynamic.react    ("create", auto_wp_magic, priority = 200)
    db.user_dynamic.react    ("set",    auto_wp_magic, priority = 200)
    db.auto_wp.audit         ("create", auto_wp_check, priority = 90)
    db.auto_wp.audit         ("set",    auto_wp_check, priority = 90)
    db.auto_wp.react         ("create", auto_wp_modify)
    db.auto_wp.react         ("set",    auto_wp_modify)
    db.auto_wp.react         ("set",    auto_wp_change_da, priority = 90)
# end def init

### __END__ user_dynamic
