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
#
#++
# Name
#    vacation
#
# Purpose
#    Vacation-related routines
#--
#

from math import ceil

from roundup.date import Date, Interval
from freeze       import freeze_date
import common
import user_dynamic

def public_holiday_wp (db, user, date) :
    """ Get first public holiday wp for this user on date.
        Should typically be only one, we use the first in the list
        without further checks.
    """
    opn = db.time_project_status.lookup ('Open')
    prj = db.time_project.filter \
        (None, dict (is_public_holiday = True, status = opn))
    if not prj :
        return None
    wps = \
        ( db.time_wp.filter \
            (None, dict (project = prj, is_public = True))
        + db.time_wp.filter \
            (None, dict (project = prj, bookers = user))
        )
    for wpid in wps :
        w = db.time_wp.getnode (wpid)
        if  (   w.time_start <= date
            and (not w.time_end or date < w.time_end)
            ) :
            return wpid
# end def public_holiday_wp

def try_create_public_holiday (db, daily_record, date, user) :
    st_open = db.daily_record_status.lookup ('open')
    wp      = public_holiday_wp (db, user, date)
    # Don't change anything if status not open
    if db.daily_record.get (daily_record, 'status') != st_open :
        return
    # Only perform public holiday processing if user has a public
    # holiday wp to book on.
    if not wp :
        return
    dyn = user_dynamic.get_user_dynamic (db, user, date)
    wh  = user_dynamic.day_work_hours   (dyn, date)
    if wh :
        loc = db.org_location.get (dyn.org_location, 'location')
        hol = db.public_holiday.filter \
            ( None
            , { 'date'      : common.pretty_range (date, date)
              , 'locations' : loc
              }
            )
        if hol and wh :
            holiday = db.public_holiday.getnode (hol [0])
            if holiday.is_half :
                wh = wh / 2.
            wh = user_dynamic.round_daily_work_hours (wh)
            # Check if there already is a public-holiday time_record
            # Update duration (and wp) if wrong
            trs = db.time_record.filter \
                (None, dict (daily_record = daily_record))
            for trid in trs :
                tr = db.time_record.getnode (trid)
                if tr.wp is None :
                    continue
                tp = db.time_project.getnode \
                    (db.time_wp.get (tr.wp, 'project'))
                if tp.is_public_holiday :
                    d = {}
                    if tr.duration != wh :
                        d ['duration'] = wh
                    if tr.wp != wp :
                        d ['wp'] = wp
                    if d :
                        db.time_record.set (trid, ** d)
                    return
            comment = holiday.name
            if holiday.description :
                comment = '\n'.join ((holiday.name, holiday.description))
            db.time_record.create \
                ( daily_record  = daily_record
                , duration      = wh
                , wp            = wp
                , comment       = comment
                , work_location = db.work_location.lookup ('off')
                )
# end def try_create_public_holiday

def create_daily_recs (db, user, first_day, last_day) :
    d = first_day
    while d <= last_day :
        pr = common.pretty_range (d, d)
        x = db.daily_record.filter (None, dict (user = user, date = pr))
        if x :
            assert len (x) == 1
            x = x [0]
        else :
            dyn = user_dynamic.get_user_dynamic (db, user, d)
            if not dyn :
                d += common.day
                continue
            x = db.daily_record.create \
                ( user              = user
                , date              = d
                , weekend_allowed   = False
                , required_overtime = False
                )
        try_create_public_holiday (db, x, d, user)
        d += common.day
# end def create_daily_recs

def leave_submissions_on_date (db, user, date, filter = None) :
    """ Return all leave records that overlap with the given date.
        Optionally restrict search if filter is specified.
    """
    dts = ';%s' % date.pretty (common.ymd)
    dte = '%s;' % date.pretty (common.ymd)
    d   = dict (user = user, first_day = dts, last_day = dte)
    if filter :
        d.update (filter)
    vs = db.leave_submission.filter (None, d)
    return [db.leave_submission.getnode (v) for v in vs]
# end def leave_submissions_on_date

def leave_days (db, user, first_day, last_day) :
    d = first_day
    s = 0.0
    while d <= last_day :
        dyn = user_dynamic.get_user_dynamic (db, user, d)
        if not dyn :
            d += common.day
            continue
        wh = user_dynamic.day_work_hours (dyn, d)
        ld = leave_duration (db, user, d)
        if ld != 0 :
            s += ceil (ld / wh * 2) / 2.
        d += common.day
    return s
# end def leave_days

def leave_duration (db, user, date, ignore_public_holiday = False) :
    """ Duration of leave on a single day to be booked. """
    dyn = user_dynamic.get_user_dynamic (db, user, date)
    wh  = user_dynamic.day_work_hours (dyn, date)
    if not wh :
        return 0.0
    dt  = common.pretty_range (date, date)
    dr  = db.daily_record.filter (None, dict (user = user, date = dt))
    assert len (dr) == 1
    try_create_public_holiday (db, dr [0], date, user)
    trs = db.time_record.filter (None, dict (daily_record = dr [0]))
    bk  = 0.0
    if not ignore_public_holiday :
        for trid in trs :
            tr = db.time_record.getnode (trid)
            if not tr.wp :
                continue
            wp = db.time_wp.getnode (tr.wp)
            tp = db.time_project.getnode (wp.project)
            if tp.is_public_holiday :
                bk += tr.duration
    assert bk <= wh
    return wh - bk
# end def leave_duration

def leave_submission_days (db, user, ctype, start, end, type, * stati) :
    """ Sum leave submissions of the given type
        with the given status in the given time range for the given user
        and ctype (contract_type).
    """
    assert start <= end
    dt   = common.pretty_range (start, end)
    dts  = ';%s' % start.pretty (common.ymd)
    dte  = '%s;' % end.pretty   (common.ymd)
    if type == 'vacation' :
        lwp  = vacation_wps (db)
    elif type == 'flexi' :
        lwp  = flexi_wps (db)
    else :
        lwp  = special_wps (db)
    d    = dict (user = user, status = list (stati), time_wp = lwp)
    d1   = dict (d, first_day = dt)
    vs1  = db.leave_submission.filter (None, d1)
    d2   = dict (d, last_day = dt)
    vs2  = db.leave_submission.filter (None, d2)
    d3   = dict (d, first_day = dts, last_day = dte)
    vs3  = db.leave_submission.filter (None, d3)
    vss  = dict.fromkeys (vs1 + vs2 + vs3).keys ()
    vss  = [db.leave_submission.getnode (i) for i in vss]
    days = 0.0
    for vs in vss :
        first_day = vs.first_day
        last_day  = vs.last_day
        dyn = user_dynamic.get_user_dynamic (db, user, first_day)
        if not dyn :
            continue
        if dyn.contract_type != ctype :
            continue
        if first_day < start :
            assert vs.last_day >= start
            first_day = start
        if last_day > end :
            assert vs.first_day <= end
            last_day  = end
        days += leave_days (db, user, first_day, last_day)
    return days
# end def leave_submission_days

def vacation_submission_days (db, user, ctype, start, end, * stati) :
    """ Sum vacation submissions with the given status in the given time
        range for the given user and ctype (contract_type).
    """
    return leave_submission_days \
        (db, user, ctype, start, end, 'vacation', * stati)
# end def vacation_submission_days

def flexitime_submission_days (db, user, ctype, start, end, * stati) :
    """ Sum flexitime submissions with the given status in the given time
        range for the given user and ctype (contract_type).
    """
    return leave_submission_days \
        (db, user, ctype, start, end, 'flexi', * stati)
# end def flexitime_submission_days

def special_submission_days (db, user, ctype, start, end, * stati) :
    """ Sum special_leave submissions with the given status in the given
        time range for the given user and ctype (contract_type).
    """
    return leave_submission_days \
        (db, user, ctype, start, end, 'special', * stati)
# end def special_submission_days

def next_yearly_vacation_date (db, user, ctype, date) :
    d = date + common.day
    dyn = vac_get_user_dynamic (db, user, ctype, d)
    if not dyn or dyn.vacation_month is None or dyn.vacation_day is None :
        assert 0
        return None
    y = int (d.get_tuple () [0])
    next_date = Date \
        ('%04d-%02d-%02d' % (y, dyn.vacation_month, dyn.vacation_day))
    if next_date < d :
        next_date = Date \
            ('%04d-%02d-%02d' % (y + 1, dyn.vacation_month, dyn.vacation_day))
    # Found a dyn user record too far in the future, can't determine
    # next yearly vacation date
    if dyn.valid_from > next_date :
        # Hmmm, maybe started this year?
        # Or re-started after some years?
        prev = user_dynamic.prev_user_dynamic (db, dyn, use_ct = True)
        if not prev or prev.valid_to < next_date :
            return dyn.valid_from
        return None
    while dyn.valid_from <= next_date :
        if dyn.valid_to > next_date :
            # valid dyn record
            return next_date
        ndyn = vac_next_user_dynamic (db, dyn)
        if  (  not ndyn
            or ndyn.valid_from > next_date
            or ndyn.contract_type != ctype
            ) :
            # use last dyn record, no next or too far in the future
            return next_date
        dyn  = ndyn
        yday = dyn.vacation_day
        ymon = dyn.vacation_month
        if yday is None or ymon is None :
            return next_date
        next_date = Date ('%04d-%02d-%02d' % (y, ymon, yday))
        if next_date < d :
            next_date = Date ('%04d-%02d-%02d' % (y + 1, ymon, yday))
# end def next_yearly_vacation_date

def prev_yearly_vacation_date (db, user, ctype, date) :
    d = date - common.day
    dyn = vac_get_user_dynamic (db, user, ctype, d)
    if  (  not dyn
        or dyn.valid_from > d
        or dyn.vacation_month is None
        or dyn.vacation_day is None
        ) :
        return None
    y = int (d.get_tuple () [0])
    prev_date = Date \
        ('%04d-%02d-%02d' % (y, dyn.vacation_month, dyn.vacation_day))
    if prev_date >= date :
        prev_date = Date \
            ('%04d-%02d-%02d' % (y - 1, dyn.vacation_month, dyn.vacation_day))
    assert prev_date < date
    while dyn.valid_from > prev_date :
        dyn = vac_prev_user_dynamic (db, dyn)
        if not dyn :
            return prev_date
        yday = dyn.vacation_day
        ymon = dyn.vacation_month
        if yday is None or ymon is None :
            return prev_date
        prev_date = Date ('%04d-%02d-%02d' % (y, ymon, yday))
        if prev_date >= date :
            prev_date = Date ('%04d-%02d-%02d' % (y - 1, ymon, yday))
    return prev_date
# end def prev_yearly_vacation_date

def interval_days (iv) :
    """ Compute number of days in a roundup.date Interval. The
        difference should be computed from two dates (without time)
        >>> D = Date
        >>> I = Interval
        >>> interval_days (D ('2014-01-07') - D ('2013-01-07'))
        365
        >>> interval_days (D ('2014-01-07') - D ('2012-01-07'))
        731
        >>> interval_days (I ('23d'))
        23
        >>> interval_days (I ('-23d'))
        -23
        >>> interval_days (D ('2012-01-07') - D ('2014-01-07'))
        -731
    """
    t = iv.get_tuple ()
    assert abs (t [0]) == 1
    assert t [1] == 0
    assert t [2] == 0
    return t [3] * t [0]
# end def interval_days

def get_vacation_correction (db, user, ctype = -1, date = None) :
    """ Get latest absolute vacation_correction.
        Special handling of ctype: None means ctype 'None' while -1
        means "don't care, search for *any* ctype". Note that roundups
        interface for searching specifies -1 when searching for an
        empty link....
    """
    if date is None :
        date = Date ('.')
    dt = ";%s" % date.pretty (common.ymd)
    d = dict \
        ( user          = user
        , absolute      = True
        , date          = dt
        )
    # If no ctype given, try to get dyn. user record on date and use
    # ctype from there. If not found we simply search for the latest
    # vacation correction before date.
    if ctype == -1 :
        dyn = user_dynamic.get_user_dynamic (db, user, date)
        if dyn :
            ctype = dyn.contract_type
    if ctype != -1 :
        d ['contract_type'] = ctype
        if ctype is None :
            d ['contract_type'] = '-1' # roundup: -1 means search empty
    vcs = db.vacation_correction.filter (None, d, sort = [('-', 'date')])
    if not vcs :
        return
    for id in vcs :
        vc = db.vacation_correction.getnode (id)
        if ctype == -1 or vc.contract_type == ctype :
            return vc
# end def get_vacation_correction

def vacation_wps (db) :
    # All time recs with vacation wp in range
    vtp = db.time_project.filter (None, dict (is_vacation = True))
    if not vtp :
        return []
    vwp = db.time_wp.filter (None, dict (project = vtp))
    return vwp
# end def vacation_wps

def special_wps (db) :
    # All time recs with special-leave wp in range
    vtp = db.time_project.filter (None, dict (is_special_leave = True))
    if not vtp :
        return []
    vwp = db.time_wp.filter (None, dict (project = vtp))
    return vwp
# end def vacation_wps

def flexi_wps (db) :
    # All time recs with flexitime wp in range
    vtp = db.time_project.filter \
        (None, dict (max_hours = 0, approval_required = True))
    if not vtp :
        return []
    vwp = db.time_wp.filter (None, dict (project = vtp))
    return vwp
# end def flexi_wps

def vacation_time_sum (db, user, ctype, start, end) :
    dt  = common.pretty_range (start, end)
    dr  = db.daily_record.filter (None, dict (user = user, date = dt))
    dtt = [('+', 'daily_record.date')]
    vwp = vacation_wps (db)
    trs = db.time_record.filter \
        (None, dict (daily_record = dr, wp = vwp), sort = dtt)
    vac = 0.0
    if ctype == -1 :
        ctype = _get_ctype (db, user, Date ('.'))
    by_dr = {}
    for tid in trs :
        tr  = db.time_record.getnode  (tid)
        dr  = db.daily_record.getnode (tr.daily_record)
        dyn = user_dynamic.get_user_dynamic (db, user, dr.date)
        # dyn is None if time_records booked but dyn record revoked for this period:
        if not dyn or dyn.contract_type != ctype :
            continue
        wh  = user_dynamic.day_work_hours (dyn, dr.date)
        assert wh
        if dr.id not in by_dr :
            by_dr [dr.id] = (wh, [])
        assert by_dr [dr.id][0] == wh
        by_dr [dr.id][1].append (tr.duration)
    for wh, durs in by_dr.itervalues () :
        vac += ceil (sum (durs) / wh * 2) / 2.
    return vac
# end def vacation_time_sum

def _get_ctype (db, user, date) :
    # None is a valide contract_type, return -1 in case of error
    dyn = user_dynamic.get_user_dynamic (db, user, date)
    if not dyn :
        dyn = user_dynamic.last_user_dynamic (db, user, date)
    if not dyn :
        return -1
    return dyn.contract_type
# end def _get_ctype

def remaining_vacation \
    (db, user, ctype = -1, date = None, cons = None, to_eoy = True) :
    """ Compute remaining vacation on the given date
    """
    if date is None :
        date = Date ('.')
    pdate = date.pretty (common.ymd)
    if ctype == -1 :
        ctype = _get_ctype (db, user, date)
    if ctype == -1 :
        return
    vac   = None
    try :
        vac = db.rem_vac_cache.get ((user, ctype, pdate, to_eoy))
    except AttributeError :
        def vac_clear_cache (db) :
            db.rem_vac_cache = {}
        db.registerClearCacheCallback (vac_clear_cache, db)
        db.rem_vac_cache = {}
    if vac is not None :
        return vac
    vc = get_vacation_correction (db, user, ctype, date)
    if not vc :
        return
    ed  = next_yearly_vacation_date (db, user, ctype, date)
    if not to_eoy :
        ed = min (ed, date)
    if cons is None :
        cons = consolidated_vacation (db, user, ctype, date, vc, to_eoy)
    vac = cons
    vac -= vacation_time_sum (db, user, ctype, vc.date, ed)
    # All vacation_correction records up to date but starting with one
    # day later (otherwise we'll find the absolute correction)
    # Also one day *earlier* than ed for the same reason.
    dt  = common.pretty_range (vc.date + common.day, ed - common.day)
    d   = dict (user = user, date = dt)
    if ctype is not None :
        d ['contract_type'] = ctype
    ds  = [('+', 'date')]
    vcs = db.vacation_correction.filter (None, d, sort = ds)
    for vcid in vcs :
        vc = db.vacation_correction.getnode (vcid)
        if vc.contract_type != ctype :
            continue
        assert not vc.absolute
        vac += vc.days
    db.rem_vac_cache [(user, ctype, pdate, to_eoy)] = vac
    return vac
# end def remaining_vacation

def month_diff (d1, d2) :
    """ Difference of two month which may be in suceeding years
    >>> month_diff (Date ('2018-01-02'), Date ('2018-12-01'))
    11
    >>> month_diff (Date ('2018-12-01'), Date ('2019-01-01'))
    1
    >>> month_diff (Date ('2018-12-12'), Date ('2019-12-11'))
    12
    >>> month_diff (Date ('2018-12-12'), Date ('2019-12-12'))
    12
    """
    yd = d2.year  - d1.year
    md = d2.month - d1.month
    return md + 12 * yd
# end def month_diff

def consolidated_vacation \
    (db, user, ctype = -1, date = None, vc = None, to_eoy = True) :
    """ Compute remaining vacation on the given date
    """
    if date is None :
        date = Date ('.')
    if ctype == -1 :
        ctype = _get_ctype (db, user, date)
    if ctype == -1 :
        return
    vc  = vc or get_vacation_correction (db, user, ctype, date)
    if not vc :
        return None
    ed  = next_yearly_vacation_date (db, user, ctype, date)
    if not to_eoy :
        ed = min (ed, date + common.day)
    d   = vc.date
    dyn = vac_get_user_dynamic (db, user, ctype, d)
    while dyn and dyn.valid_to and dyn.valid_to <= d :
        dyn = vac_next_user_dynamic (db, dyn)
    if dyn is None :
        return None
    vac = float (vc.days)
    msg = "vac_aliq None for user_dynamic%s" % dyn.id
    assert dyn.vac_aliq, msg
    va = db.vac_aliq.getnode (dyn.vac_aliq)
    assert va.name in ('Daily', 'Monthly')
    # Need to skip first period without a dyn user record
    # sd is the current start date for german aliquotation
    # We subtract 1 day to easily compare the day of the ending-date
    # with the day of the start date
    sd = d
    # This is used for corrections if the start day lies beyond 28 -- in
    # that case there are months that simply don't have that date. So we
    # must correct for this in months with less days.
    sd_day = 0
    if dyn.valid_from > d :
        sd = d = dyn.valid_from
    while dyn and d < ed :
        if dyn.valid_from > d :
            # We want to check if the days that are lost here whenever a
            # jump in dyn user records occurs are OK for monthly aliqotation
            sd = d = dyn.valid_from
            continue
        assert not dyn.valid_to or dyn.valid_to > d
        eoy = Date ('%s-12-31' % d.year)
        msg = "vacation_yearly None for user_dynamic%s" % dyn.id
        assert dyn.vacation_yearly is not None, msg
        msg = ( "vac_aliq changes w/o absolute vac_corr for user_dynamic%s"
              % dyn.id
              )
        assert dyn.vac_aliq == va.id, msg
        if dyn.valid_to and dyn.valid_to <= ed and dyn.valid_to < eoy :
            if va.name == 'Daily' :
                yd = float (common.ydays (dyn.valid_to))
                vac += interval_days \
                    (dyn.valid_to - d) * dyn.vacation_yearly / yd
            else :
                md  = month_diff (sd, dyn.valid_to)
                dy  = sd_day or sd.day
                if dyn.valid_to.day < dy :
                    md -= 1
                    # Example: sd = 2018-04-03 valid_to = 2018-06-01
                    # Need to set sd=2018-05-03, i.e. the next start
                    # day before valid_to
                    # Even more complex is the case where e.g.
                    # sd = 2018-03-31 valid_to = 2018-05-01
                    # We set sd=2018-04-30 and sd_day=31
                    # Get last day of last month
                    lm = dyn.valid_to - Interval ('%sd' % dyn.valid_to.day)
                    em = common.end_of_month (lm)
                    if dy > em.day :
                        sd_day = sd.day
                        sd = em
                    else :
                        sd = Date (lm.pretty ("%%Y-%%m-%s" % sd.day))
                        sd_day = 0
                else :
                    sd = Date (dyn.valid_to.pretty ("%%Y-%%m-%s" % sd.day))
                    sd_day = 0
                d = dyn.valid_to
                vac += dyn.vacation_yearly * md / 12.0
            dyn = vac_next_user_dynamic (db, dyn)
        elif eoy < ed :
            if va.name == 'Daily' :
                yd = float (common.ydays (eoy))
                iv = eoy + common.day - d
                vac += interval_days (iv) * dyn.vacation_yearly / yd
            else :
                md  = month_diff (sd, eoy)
                dy  = sd_day or sd.day
                assert eoy.day >= dy
                if dy == 1 :
                    md += 1
                    sd = eoy + common.day
                else :
                    sd = Date (eoy.pretty ("%%Y-%%m-%s" % sd.day))
                sd_day = 0
                vac += dyn.vacation_yearly * md / 12.0
            d  = eoy + common.day
            if dyn.valid_to == d :
                dyn = vac_next_user_dynamic (db, dyn)
        else :
            if va.name == 'Daily' :
                yd = float (common.ydays (ed - common.day))
                vac += interval_days (ed - d) * dyn.vacation_yearly / yd
            else :
                md = month_diff (sd, ed)
                dy  = sd_day or sd.day
                if ed.day < dy :
                    md -= 1
                sd = ed
                vac += dyn.vacation_yearly * md / 12.0
            d = ed
    return vac
# end def consolidated_vacation

def valid_wps (db, filter = {}, user = None, date = None, srt = None) :
    srt  = srt or [('+', 'id')]
    wps  = {}
    date = date or Date ('.')
    dt   = (date + common.day).pretty (common.ymd)
    d    = dict (time_start = ';%s' % date.pretty (common.ymd))
    # Only select WPs that are not exclusively managed by external tool
    d ['is_extern']         = False
    d ['project.is_extern'] = False
    d.update (filter)

    wp  = []
    if user :
        d1  = dict (d, is_public = True, has_expiration_date = False)
        wp.extend (db.time_wp.filter (None, d1, srt))
        d1  = dict (d, is_public = True, time_end = '%s;' % dt)
        wp.extend (db.time_wp.filter (None, d1, srt))
        d1  = dict (d, bookers = user, has_expiration_date = False)
        wp.extend (db.time_wp.filter (None, d1, srt))
        d1  = dict (d, bookers = user, time_end = '%s;' % dt)
        wp.extend (db.time_wp.filter (None, d1, srt))
    else :
        d1 = dict (d, has_expiration_date = False)
        wp.extend (db.time_wp.filter (None, d1, srt))
        d1 = dict (d, time_end = '%s;' % dt)
        wp.extend (db.time_wp.filter (None, d1, srt))
    # Filter again via db to get sorting right
    return db.time_wp.filter (wp, {}, sort = srt)
# end def valid_wps

def valid_leave_wps (db, user = None, date = None, srt = None, thawed = None) :
    """ If thawed is given, find only WPs with an end-time > freeze date
        If thawed *and* a date is given we use the *later* date
        Note that for thawed to work a user must be given
    """
    if thawed and user :
        freeze = freeze_date (db, user)
        if freeze and date :
            date = max (freeze, date)
        elif freeze :
            date = freeze
    d = {'project.approval_required' : True}
    return valid_wps (db, d, user, date, srt)
# end def valid_leave_wps

def valid_leave_projects (db) :
    return db.time_project.filter (None, dict (approval_required = True))
# end def valid_leave_projects

def vac_get_user_dynamic (db, user, ctype, date) :
    """ Get user_dynamic record for a vacation computation on the given
        date. Note that there are cases where no dyn user record exists
        exactly for the date but before -- or after. If the record
        starts a vacation period (e.g. an initial absolute vacation
        correction) there doesn't necessarily already exist a dynamic
        user record. On the other hand when computing the vacation at
        the end of a period no dyn user record may be available anymore
        (e.g., because the person has left).
    """
    dyn = user_dynamic.get_user_dynamic (db, user, date)
    if not dyn :
        dyn = user_dynamic.find_user_dynamic (db, user, date, '-')
    if  (   dyn
        and (  dyn.contract_type != ctype
            or not dyn.vacation_month
            or not dyn.vacation_day
            )
        ) :
        dyn = vac_prev_user_dynamic (db, dyn, ctype)
    if not dyn :
        dyn = user_dynamic.find_user_dynamic (db, user, date, '+')
    if  (   dyn
        and (  dyn.contract_type != ctype
            or not dyn.vacation_month
            or not dyn.vacation_day
            )
        ) :
        dyn = vac_next_user_dynamic (db, dyn, ctype)
    return dyn
# end def vac_get_user_dynamic

def vac_next_user_dynamic (db, dyn, ctype = -1) :
    if ctype == -1 :
        ctype = dyn.contract_type
    dyn   = user_dynamic.next_user_dynamic (db, dyn)
    while (   dyn
          and (  dyn.contract_type != ctype
              or not dyn.vacation_month
              or not dyn.vacation_day
              )
          ) :
        dyn = user_dynamic.next_user_dynamic (db, dyn)
    return dyn
# end def vac_next_user_dynamic

def vac_prev_user_dynamic (db, dyn, ctype = -1) :
    if ctype == -1 :
        ctype = dyn.contract_type
    dyn   = user_dynamic.prev_user_dynamic (db, dyn)
    while (   dyn
          and (  dyn.contract_type != ctype
              or not dyn.vacation_month
              or not dyn.vacation_day
              )
          ) :
        dyn = user_dynamic.prev_user_dynamic (db, dyn)
    return dyn
# end def vac_prev_user_dynamic

def need_hr_approval \
    (db, tp, user, ctype, first_day, last_day, stname, booked = False) :
    if tp.approval_hr :
        return True
    if stname != 'submitted' :
        return False
    if not tp.is_vacation :
        # Flexitime
        if tp.no_overtime and tp.max_hours == 0 :
            dyn = user_dynamic.get_user_dynamic (db, user, first_day)
            if not dyn or not dyn.all_in :
                return False
            fd = first_day
            if first_day.year != last_day.year :
                while fd.year != last_day.year :
                    eoy = common.end_of_year (fd)
                    rem = flexi_remain (db, user, fd, ctype)
                    dur = leave_days (db, user, fd, eoy)
                    if rem - dur < 0 :
                        return True
                    fd = eoy + common.day
            rem = flexi_remain (db, user, fd, ctype)
            dur = leave_days (db, user, fd, last_day)
            return rem - dur < 0
        else :
            return False
    day = common.day
    ed  = next_yearly_vacation_date (db, user, ctype, last_day) - day
    vac = remaining_vacation (db, user, ctype, ed)
    assert vac is not None
    dur = leave_days (db, user, first_day, last_day)
    # don't count duration if this is already booked, so we would count
    # this vacation twice.
    if booked :
        dur = 0
    return ceil (vac) - dur < 0
# end def need_hr_approval

def vacation_params (db, user, date, vc, hv = False) :
    """ Compute parameters needed for initializing vacation report,
        returns the last total vacation (initial carry-over for start of
        vacation or consolidated vacation from last year) and the
        current carry (initial carry-over for start of vacation or last
        remaining vacation). This is used for summary data in the
        summary report and for vacation display in the leave mask.
    """
    day   = common.day
    carry = None
    ltot  = None
    ctype = vc.contract_type
    yday  = next_yearly_vacation_date (db, user, ctype, date) - day
    if yday :
        pd = prev_yearly_vacation_date (db, user, ctype, yday)
        if not pd or vc.date == pd :
            pd    = vc.date
            carry = ltot = vc.days
        else :
            carry = remaining_vacation    (db, user, ctype, pd - day)
            ltot  = consolidated_vacation (db, user, ctype, pd - day)
    carry = carry or 0.0
    ltot  = ltot  or 0.0
    return yday, pd, carry, ltot
# end def vacation_params

def get_current_ctype (db, user, dt = None) :
    if dt is None :
        dt = Date ('.')
    dyn   = user_dynamic.get_user_dynamic (db, user, dt)
    if not dyn :
        return None
    ctype = dyn.contract_type
    return ctype
# end def get_current_ctype

def flexi_alliquot (db, user, date_in_year, ctype) :
    """ Loop over all dyn records in this year and use only those with
        all-in set. For those we count the days and compute the
        year-alliquot number of max_flexitime days.
    """
    y     = common.start_of_year (date_in_year)
    eoy   = common.end_of_year   (y)
    flex  = 0.0
    dsecs = 0.0
    ds    = 24 * 60 * 60
    for dyn in user_dynamic.user_dynamic_year_iter (db, user, y) :
        if not dyn.all_in or dyn.contract_type != ctype :
            continue
        vf = dyn.valid_from
        if vf < y :
            vf = y
        vt = dyn.valid_to
        if not vt or vt > eoy + common.day :
            vt = eoy + common.day
        flex  += (vt - vf).as_seconds () * (dyn.max_flexitime or 0)
        dsecs += (vt - vf).as_seconds ()
    assert dsecs / ds <= 366
    if not flex :
        return 0.0
    days  = float ((eoy + common.day - y).as_seconds () / ds)
    flex /= ds
    return ceil (flex / days)
# end def flexi_alliquot

def avg_hours_per_week_this_year (db, user, date_in_year) :
    """ Loop over all dyn records in this year and use only those with
        all-in set. For those we count the hours and compute the
        average over all all-in days.
    """
    y     = common.start_of_year (date_in_year)
    eoy   = common.end_of_year   (y)
    now   = Date ('.')
    if eoy > now :
        eoy = now
    hours = 0.0
    dsecs = 0.0
    ds    = 24 * 60 * 60
    for dyn in user_dynamic.user_dynamic_year_iter (db, user, y) :
        if not dyn.all_in :
            continue
        vf = dyn.valid_from
        if vf < y :
            vf = y
        vt = dyn.valid_to
        if not vt or vt > eoy + common.day :
            vt = eoy + common.day
        dsecs += (vt - vf).as_seconds ()
        drs = db.daily_record.filter \
            (None, dict (date = common.pretty_range (vf, vt), user = user))
        for drid in drs :
            dr  = db.daily_record.getnode (drid)
            dur = user_dynamic.update_tr_duration (db, dr)
            hours += dur
    days = dsecs / ds
    assert days <= 366
    if not days :
        return 0
    avgday = hours / float (days)
    return avgday * 7
# end def avg_hours_per_week_this_year

def get_all_in_ctypes (db, user, y) :
    ctypes = set ()
    for dyn in user_dynamic.user_dynamic_year_iter (db, user, y) :
        if not dyn.all_in :
            continue
        ctypes.add (dyn.contract_type)
    return ctypes
# end def get_all_in_ctypes

def flexi_remain (db, user, date_in_year, ctype) :
    y     = common.start_of_year (date_in_year)
    eoy   = common.end_of_year   (y)
    fa    = flexi_alliquot (db, user, date_in_year, ctype)
    acpt  = db.leave_status.lookup ('accepted')
    cnrq  = db.leave_status.lookup ('cancel requested')
    if not fa :
        return 0
    sd = 0
    dyn = user_dynamic.get_user_dynamic (db, user, y)
    if not dyn :
        dyn = user_dynamic.first_user_dynamic (db, user, y)
    while dyn :
        # Check the case that we found a dyn user record far in the past
        if dyn.valid_to and dyn.valid_to < y :
            dyn = user_dynamic.next_user_dynamic (db, dyn)
            continue
        if dyn.contract_type == ctype :
            b = dyn.valid_from
            if b < y :
                b = y
            if b > eoy :
                break
            e = dyn.valid_to
            if e > eoy or not e :
                e = eoy
            else :
                e -= common.day
            ct = dyn.contract_type
            if dyn.all_in :
                sd += flexitime_submission_days (db, user, ct, b, e, acpt, cnrq)
        dyn = user_dynamic.next_user_dynamic (db, dyn)
    return fa - sd
# end def flexi_remain

def fix_vacation (db, uid, date_from = None, date_to = None) :
    """ Fix vacation for a user where the dyn. user record has been
        changed *after* the user already booked vacation.
        We search for all time-records with a daily-record in state
        'leave' since the last frozen time or date_from if given.
    """
    #print ("fix_vacation: %s %s %s" % (uid, date_from, date_to))
    if date_from is None :
        date_from = Date ('2000-01-01')
        frozen = db.daily_record_freeze.filter \
            (None, dict (user = uid, frozen = True), sort = ('-', 'date'))
        if frozen :
            frozen = db.daily_record_freeze.getnode (frozen [0])
            date_from = frozen.date + common.day
    leave = db.daily_record_status.lookup ('leave')
    d = dict ()
    d ['daily_record.user']   = uid
    d ['daily_record.date']   = common.pretty_range (date_from, date_to)
    d ['daily_record.status'] = leave
    trs = db.time_record.filter (None, d)
    for trid in trs :
	tr = db.time_record.getnode  (trid)
	dr = db.daily_record.getnode (tr.daily_record)
	wp = db.time_wp.getnode      (tr.wp)
	tp = db.time_project.getnode (wp.project)
	if not tp.is_vacation and not tp.is_public_holiday :
	    continue
	du = leave_duration (db, uid, dr.date, tp.is_public_holiday)
	if tr.duration != du :
	    #print "Wrong: time_record%s: %s->%s" % (trid, tr.duration, du)
	    db.time_record.set (trid, duration = du)
# end def fix_vacation

### __END__
