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

import roundup.date
import common
import user_dynamic

def try_create_public_holiday (db, daily_record, date, user) :
    dyn = user_dynamic.get_user_dynamic (db, user, date)
    wh  = user_dynamic.day_work_hours   (dyn, date)
    if wh :
        # Check if there already is a public-holiday time_record
        trs = db.time_record.filter (None, dict (daily_record = daily_record))
        for tr in trs :
            wp = db.time_record.get (tr, 'wp')
            if wp is None :
                continue
            tp = db.time_project.getnode (db.time_wp.get (wp, 'project'))
            if tp.is_public_holiday :
                return
        loc = db.org_location.get (dyn.org_location, 'location')
        hol = db.public_holiday.filter \
            ( None
            , {'date' : common.pretty_range (date, date), 'locations' : loc}
            )
        if hol and wh :
            wp  = None
            try :
                ok  = db.time_project_status.lookup ('Open')
                prj = db.time_project.filter \
                    (None, dict (is_public_holiday = True, status = ok))
                wps = db.time_wp.filter \
                    (None, dict (project = prj, bookers = user))
                for wpid in wps :
                    w = db.time_wp.getnode (wpid)
                    if  (   w.time_start <= date
                        and (not w.time_end or date < w.time_end)
                        ) :
                        wp = wpid
                        break
            except (IndexError, KeyError) :
                pass
            holiday = db.public_holiday.getnode (hol [0])
            comment = holiday.name
            if holiday.description :
                comment = '\n'.join ((holiday.name, holiday.description))
            if holiday.is_half :
                wh = wh / 2.
            wh = user_dynamic.round_daily_work_hours (wh)
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
            x = db.daily_record.create \
                ( user              = user
                , date              = d
                , weekend_allowed   = False
                , required_overtime = False
                )
        try_create_public_holiday (db, x, d, user)
        d += common.day
# end def create_daily_recs

def leave_submissions_on_date (db, user, date) :
    """ Return all leave records that overlap with the given date
    """
    dts = ';%s' % date.pretty (common.ymd)
    dte = '%s;' % date.pretty (common.ymd)
    vs = db.leave_submission.filter \
        (None, dict (user = user, first_day = dts, last_day = dte))
    return [db.leave_submission.getnode (v) for v in vs]
# end def leave_submissions_on_date

def leave_days (db, user, first_day, last_day) :
    d = first_day
    s = 0.0
    while d <= last_day :
        dyn = user_dynamic.get_user_dynamic (db, user, d)
        if not dyn :
            continue
        wh = user_dynamic.day_work_hours (dyn, d)
        ld = leave_duration (db, user, d)
        if ld != 0 :
            s += ceil (ld / wh * 2) / 2.
        d += common.day
    return s
# end def leave_days

def leave_duration (db, user, date) :
    """ Duration of leave on a single day to be booked. """
    dyn = user_dynamic.get_user_dynamic (db, user, date)
    wh  = user_dynamic.day_work_hours (dyn, date)
    if not wh :
        return 0.0
    dt  = common.pretty_range (date, date)
    dr  = db.daily_record.filter (None, dict (user = user, date = dt))
    assert len (dr) == 1
    trs = db.time_record.filter (None, dict (daily_record = dr [0]))
    bk  = 0.0
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

def vacation_submission_days (db, user, vcode, start, end, * stati) :
    """ Sum vacation submissions with the given status in the given time
        range for the given user and vcode.
    """
    dt   = common.pretty_range (start, end)
    dts  = ';%s' % start.pretty (common.ymd)
    dte  = '%s;' % end.pretty   (common.ymd)
    vwp  = vacation_wps (db)
    d    = dict (user = user, status = list (stati), time_wp = vwp)
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
        if dyn.vcode != vcode :
            continue
        if first_day < start :
            assert vs.last_day > start
            first_day = start
        if last_day > end :
            assert vs.first_day < end
            last_day  = end
        days += leave_days (db, user, first_day, last_day)
    return days
# end def vacation_submission_days

def next_yearly_vacation_date (db, user, vcode, date) :
    d = date + common.day
    dyn = vac_get_user_dynamic (db, user, vcode, d)
    if not dyn or dyn.vacation_month is None or dyn.vacation_day is None :
        return None
    y = int (d.get_tuple () [0])
    next_date = roundup.date.Date \
        ('%04d-%02d-%02d' % (y, dyn.vacation_month, dyn.vacation_day))
    if next_date < d :
        next_date = roundup.date.Date \
            ('%04d-%02d-%02d' % (y + 1, dyn.vacation_month, dyn.vacation_day))
    # Found a dyn user record too far in the future, can't determine
    # next yearly vacation date
    if dyn.valid_from > next_date :
        return None
    while dyn.valid_from <= next_date :
        if dyn.valid_to > next_date :
            # valid dyn record
            return next_date
        ndyn = vac_next_user_dynamic (db, dyn)
        if  (  not ndyn
            or ndyn.valid_from > next_date
            or ndyn.vcode != vcode
            ) :
            # use last dyn record, no next or too far in the future
            return next_date
        dyn  = ndyn
        yday = dyn.vacation_day
        ymon = dyn.vacation_month
        if yday is None or ymon is None :
            return next_date
        next_date = roundup.date.Date ('%04d-%02d-%02d' % (y, ymon, yday))
        if next_date < d :
            next_date = roundup.date.Date \
                ('%04d-%02d-%02d' % (y + 1, ymon, yday))
# end def next_yearly_vacation_date

def prev_yearly_vacation_date (db, user, vcode, date) :
    d = date - common.day
    dyn = vac_get_user_dynamic (db, user, vcode, d)
    if  (  not dyn
        or dyn.valid_from > d
        or dyn.vacation_month is None
        or dyn.vacation_day is None
        ) :
        return None
    y = int (d.get_tuple () [0])
    prev_date = roundup.date.Date \
        ('%04d-%02d-%02d' % (y, dyn.vacation_month, dyn.vacation_day))
    if prev_date >= date :
        prev_date = roundup.date.Date \
            ('%04d-%02d-%02d' % (y - 1, dyn.vacation_month, dyn.vacation_day))
    assert prev_date < date
    while dyn.valid_from > prev_date :
        dyn = vac_prev_user_dynamic (db, dyn)
        if not dyn :
            return None
        yday = dyn.vacation_day
        ymon = dyn.vacation_month
        if yday is None or ymon is None :
            return prev_date
        prev_date = roundup.date.Date ('%04d-%02d-%02d' % (y, ymon, yday))
        if prev_date >= date :
            prev_date = roundup.date.Date \
                ('%04d-%02d-%02d' % (y - 1, ymon, yday))
    return prev_date
# end def prev_yearly_vacation_date

def interval_days (iv) :
    """ Compute number of days in a roundup.date Interval. The
        difference should be computed from two dates (without time)
        >>> D = roundup.date.Date
        >>> I = roundup.date.Interval
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
    assert t [4] == 0
    return t [3] * t [0]
# end def interval_days

def get_vacation_correction (db, user, vcode, date) :
    """ Get latest absolute vacation_correction.
    """
    dt = ";%s" % date.pretty (common.ymd)
    d = dict \
        ( user          = user
        , absolute      = True
        , date          = dt
        )
    if vcode is not None :
        d ['vcode'] = vcode
    vcs = db.vacation_correction.filter (None, d, sort = [('-', 'date')])
    if not vcs :
        return
    for id in vcs :
        vc = db.vacation_correction.getnode (id)
        if vc.vcode == vcode :
            return vc
# end def get_vacation_correction

def vacation_wps (db) :
    # All time recs with vacation wp in range
    vtp = db.time_project.filter (None, dict (is_vacation = True))
    assert vtp
    vwp = db.time_wp.filter (None, dict (project = vtp))
    return vwp
# end def vacation_wps

def vacation_time_sum (db, user, vcode, start, end) :
    dt  = common.pretty_range (start, end)
    dr  = db.daily_record.filter (None, dict (user = user, date = dt))
    dtt = [('+', 'daily_record.date')]
    vwp = vacation_wps (db)
    trs = db.time_record.filter \
        (None, dict (daily_record = dr, wp = vwp), sort = dtt)
    vac = 0.0
    for tid in trs :
        tr  = db.time_record.getnode  (tid)
        dr  = db.daily_record.getnode (tr.daily_record)
        dyn = user_dynamic.get_user_dynamic (db, user, dr.date)
        if dyn.vcode != vcode :
            continue
        wh  = user_dynamic.day_work_hours (dyn, dr.date)
        assert wh
        vac += ceil (tr.duration / wh * 2) / 2.
    return vac
# end def vacation_time_sum

def remaining_vacation \
    (db, user, vcode = None, date = None, cons = None, to_eoy = True) :
    """ Compute remaining vacation on the given date
    """
    if date is None :
        date  = roundup.date.Date ('.')
    if vcode is None :
        dyn   = user_dynamic.get_user_dynamic (db, user, date)
        if not dyn :
            return
        vcode = dyn.vcode
    vc = get_vacation_correction (db, user, vcode, date)
    if not vc :
        return
    ed  = next_yearly_vacation_date (db, user, vcode, date)
    if not to_eoy :
        ed = min (ed, date)
    if cons is None :
        cons = consolidated_vacation (db, user, vcode, date, vc, to_eoy)
    vac = cons
    vac -= vacation_time_sum (db, user, vcode, vc.date, ed)
    # All vacation_correction records up to date but starting with one
    # day later (otherwise we'll find the absolute correction)
    dt  = common.pretty_range (vc.date + common.day, ed)
    d   = dict (user = user, date = dt)
    if vcode is not None :
        d ['vcode'] = vcode
    ds  = [('+', 'date')]
    vcs = db.vacation_correction.filter (None, d, sort = ds)
    for vcid in vcs :
        vc = db.vacation_correction.getnode (vcid)
        if vc.vcode != vcode :
            continue
        assert not vc.absolute
        vac += vc.days
    return vac
# end def remaining_vacation

def consolidated_vacation (db, user, vcode, date, vc = None, to_eoy = True) :
    """ Compute remaining vacation on the given date
    """
    vc  = vc or get_vacation_correction (db, user, vcode, date)
    if not vc :
        return None
    ed  = next_yearly_vacation_date (db, user, vcode, date)
    if not to_eoy :
        ed = min (ed, date + common.day)
    d   = vc.date
    dyn = vac_get_user_dynamic (db, user, vcode, d)
    while dyn and dyn.valid_to and dyn.valid_to < d :
        dyn = vac_next_user_dynamic (db, dyn)
    if dyn is None :
        return None
    vac = float (vc.days)
    while dyn and d < ed :
        if dyn.valid_from > d :
            d = dyn.valid_from
            continue
        assert not dyn.valid_to or dyn.valid_to > d
        eoy = roundup.date.Date ('%s-12-31' % d.year)
        if dyn.valid_to and dyn.valid_to <= ed and dyn.valid_to < eoy :
            yd = float (common.ydays (dyn.valid_to))
            vac += interval_days (dyn.valid_to - d) * dyn.vacation_yearly / yd
            dyn = vac_next_user_dynamic (db, dyn)
        elif eoy < ed :
            yd = float (common.ydays (eoy))
            iv = eoy + common.day - d
            vac += interval_days (iv) * dyn.vacation_yearly / yd
            d  = eoy + common.day
        else :
            yd = float (common.ydays (ed - common.day))
            vac += interval_days (ed - d) * dyn.vacation_yearly / yd
            d = ed
    return vac
# end def consolidated_vacation

def valid_wps (db, filter = {}, user = None, date = None, srt = None) :
    srt  = srt or [('+', 'id')]
    wps  = {}
    date = date or roundup.date.Date ('.')
    d    = dict (time_start = ';%s' % date.pretty (common.ymd))
    d.update (filter)

    if user :
        d1  = dict (d, is_public = True)
        wp1 = db.time_wp.filter (None, d1, srt)
        d2  = dict (d, bookers = user)
        wp2 = db.time_wp.filter (None, d2, srt)
        wps = [db.time_wp.getnode (w) for w in wp1 + wp2]
    else :
        wps = [db.time_wp.getnode (w) for w in db.time_wp.filter (None, d, srt)]
    wps  = [w for w in wps if not w.time_end or w.time_end > date]
    return [w.id for w in wps]
# end def valid_wps

def valid_leave_wps (db, user = None, date = None, srt = None) :
    d = {'project.approval_required' : True}
    return valid_wps (db, d, user, date, srt)
# end def valid_leave_wps

def valid_leave_projects (db) :
    return db.time_project.filter (None, dict (approval_required = True))
# end def valid_leave_projects

def vac_get_user_dynamic (db, user, vcode, date) :
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
    if dyn and dyn.vcode != vcode :
        dyn = vac_prev_user_dynamic (db, dyn)
    if not dyn :
        dyn = user_dynamic.find_user_dynamic (db, user, date, '+')
    if dyn.vcode != vcode :
        dyn = vac_next_user_dynamic (db, dyn)
    return dyn
# end def vac_get_user_dynamic

def vac_next_user_dynamic (db, dyn) :
    vcode = dyn.vcode
    dyn   = user_dynamic.next_user_dynamic (db, dyn)
    while dyn and dyn.vcode != vcode :
        dyn = user_dynamic.next_user_dynamic (db, dyn)
    return dyn
# end def vac_next_user_dynamic

def vac_prev_user_dynamic (db, dyn) :
    vcode = dyn.vcode
    dyn   = user_dynamic.prev_user_dynamic (db, dyn)
    while dyn and dyn.vcode != vcode :
        dyn = user_dynamic.prev_user_dynamic (db, dyn)
    return dyn
### __END__
