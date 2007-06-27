#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    user_dynamic
#
# Purpose
#    access routines for 'user_dynamic'
#

import sys

from time         import gmtime
from bisect       import bisect_left
from operator     import add

from roundup.date import Date, Interval

from common       import ymd, next_search_date, end_of_period, freeze_date
from common       import pretty_range

day          = Interval ('1d')
last_dynamic = None # simple one-element cache

def get_user_dynamic (db, user, date) :
    """ Get a user_dynamic record by user and date.
        Return None if no record could be found.
    """
    global last_dynamic
    user = str  (user)
    date = Date (date)
    if  (   last_dynamic
        and last_dynamic.user == user
        and last_dynamic.valid_from < date
        and (not last_dynamic.valid_to or last_dynamic.valid_to > date)
        ) :
        return last_dynamic
    ids = db.user_dynamic.filter \
        ( None, dict (user = user, valid_from = date.pretty (';%Y-%m-%d'))
        , group = ('-', 'valid_from')
        )
    if ids :
        last_dynamic = db.user_dynamic.getnode (ids [0])
        if not last_dynamic.valid_to or last_dynamic.valid_to > date :
            return last_dynamic
    return None
# end def get_user_dynamic

def first_user_dynamic (db, user, direction = '+', date = None) :
    """Search for first user_dynamic record, optionally starting at
       date.
       
       The direction may be specified as '-' to search for the last
       record, see last_user_dynamic
    """
    filter_dict = dict (user = user)
    if date :
        format = '%Y-%m-%d;'
        if direction == '-' :
            format = ';%Y-%m-%d'
        filter_dict ['valid_from'] = date.pretty (format)
    ids = db.user_dynamic.filter \
        (None, filter_dict, group = (direction, 'valid_from'))
    if ids :
        return db.user_dynamic.getnode (ids [0])
    return None
# end def first_user_dynamic

def last_user_dynamic (db, user, date = None) :
    """Search for last user_dynamic record, optionally searching
       backwards from date.
    """
    return first_user_dynamic (db, user, direction = '-', date = date)
# end def last_user_dynamic

def find_user_dynamic (db, user, date, direction = '+') :
    date = next_search_date (date, direction)
    ids = db.user_dynamic.filter \
        ( None, dict (user = user, valid_from = date)
        , group = (direction, 'valid_from')
        )
    if ids :
        return db.user_dynamic.getnode (ids [0])
    return None
# end def find_user_dynamic

def next_user_dynamic (db, dynuser) :
    return find_user_dynamic (db._db, dynuser.user.id, dynuser.valid_from)
# end def next_user_dynamic

def prev_user_dynamic (db, dynuser) :
    return find_user_dynamic \
        (db._db, dynuser.user.id, dynuser.valid_from, direction = '-')
# end def prev_user_dynamic

def act_or_latest_user_dynamic (db, user) :
    ud = get_user_dynamic (db, user, Date ('.'))
    if not ud :
        ud = last_user_dynamic (db, user)
    return ud
# end def act_or_latest_user_dynamic

wdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

def day_work_hours (dynuser, date) :
    """ Compute hours for a holiday etc from the date """
    wday  = gmtime (date.timestamp ())[6]
    return _day_work_hours (dynuser, wday)
# end def day_work_hours

def _day_work_hours (dynuser, wday) :
    hours = dynuser ['hours_' + wdays [wday]]
    if hours is not None :
        return hours
    if wday in (5, 6) or not dynuser.weekly_hours :
        return 0
    return dynuser.weekly_hours / 5.
# end def _day_work_hours

def weekly_hours (dynuser) :
    return sum (_day_work_hours (dynuser, wday) for wday in range (7))
# end def weekly_hours

def is_work_day (dynuser, date) :
    """ Return True if the given date is a work day for this user.
        Usually returns True if not on a weekend day but individual work
        times can be defined with field_mon, ..., field_sun
    """
    return bool (day_work_hours (dynuser, date))
# end def is_work_day

def use_work_hours (db, dynuser, period) :
    """ Check if work hours for given dynuser record should be used at
        all in overtime computation. They will not be used if the sum of
        required hours or the sum of overtime is zero (period denotes if
        we want the result for week/month/year).
    """
    overtime   = dynuser.additional_hours
    period_id  = dynuser.overtime_period
    dyn_period = None
    if period_id :
        dyn_period = db.overtime_period.get (period_id, 'name')
    else :
        dyn_period = 'week'
    if period == 'week' :
        overtime = dynuser.supp_weekly_hours
    return bool (dynuser.weekly_hours and overtime and dyn_period == period)
# end def use_work_hours

def work_days (dynuser) :
    """ Work days per week for this user. Returns number of days for
        which a non-zero day_work_hours is defined. This is used for
        overtime and additional time computation: We need to know the
        ratio for a given day...
    """
    sum   = reduce (add, (bool (dynuser ['hours_' + f]) for f in wdays))
    return sum or 5
# end def work_days

def round_daily_work_hours (hours) :
    """ Rounding of daily work hours.
        >>> round_daily_work_hours (38.5 / 5)
        7.75
    """
    return int (hours * 4. + .5) / 4.
# end def round_daily_work_hours

def travel_worktime (full_hours, half_hours, daily_hours) :
    """Compute the time taking halved travel into account. Return a
       tuple consisting of the travel work-time and the ratio by which
       the work-time was reduced.
    
       >>> travel_worktime ( 8,  4, 8)
       (8, 1.0)
       >>> travel_worktime (12,  6, 8)
       (8, 0.66666666666666663)
       >>> travel_worktime (12,  9, 8)
       (9, 0.5)
       >>> travel_worktime (16,  8, 8)
       (8, 0.5)
       >>> travel_worktime (18,  9, 8)
       (9, 0.5)
       >>> travel_worktime (18, 11, 8)
       (11, 0.5)
       >>> travel_worktime (18, 11, 0)
       (11, 0.5)
       >>> travel_worktime ( 2,  1, 0)
       (1, 0.5)
    """
    ret     = min (full_hours, daily_hours)
    travel  = (full_hours - half_hours) * 2.
    if half_hours > daily_hours :
        ret = half_hours
    if travel :
        ratio = (travel - (full_hours - ret)) / travel
    else :
        ratio = 1.0
    return ret, ratio
# end def travel_worktime

def update_tr_duration (db, dr)  :
    """Compute duration including travel for the given daily record.
       The dr must be the node from the db not just the id.
       Travel time records will have their tr_duration field updated.
    """
    if dr.tr_duration_ok is not None :
        return dr.tr_duration_ok
    hours   = 0.0
    hhours  = 0.0
    dyn     = get_user_dynamic (db, dr.user, dr.date) 
    tr_full = True
    wh      = 0
    if dyn :
        tr_full = dyn.travel_full
        wh      = round_daily_work_hours (day_work_hours (dyn, dr.date))
    trs     = []
    trvl_tr = {}
    for t in dr.time_record :
        tr     = db.time_record.getnode (t)
        trs.append (tr)
        hours += tr.duration
        act    = tr.time_activity
        travel = not tr_full and act and db.time_activity.get (act, 'travel')
        if travel :
            hhours  += tr.duration / 2.
            trvl_tr [tr.id] = tr
        else :
            hhours  += tr.duration
    sum, ratio = travel_worktime (hours, hhours, wh)
    for tr in trs :
        if tr.id in trvl_tr :
            tr_duration = ratio * tr.duration
        else :
            tr_duration = tr.duration
        if tr.tr_duration != tr_duration :
            db.time_record.set (tr.id, tr_duration = tr_duration)
    db.daily_record.set (dr.id, tr_duration_ok = sum)
    return sum
# end def update_tr_duration

daily_record_cache = {}
dr_user_date       = {}

def _update_empty_dr (user, date, next) :
    d = next
    while d <= date :
        daily_record_cache [(user, d.pretty (ymd))] = None
        d = d + day
# end def _update_empty_dr

def get_daily_record (db, user, date) :
    """ Use caching: prefetch all records from given date until now and
        store them. Use a per-user cache of the earliest dr found.
    """
    pdate = date.pretty (ymd)
    date  = Date (pdate)
    now   = Date (Date ('.').pretty (ymd))
    if (user, pdate) not in daily_record_cache :
        if date < now :
            start = date
            end   = now
        else :
            start = now
            end   = date
        if user in dr_user_date :
            s, e = dr_user_date [user]
            assert (start < s or end > e)
            if start > s :
                start = e + day
            if end < e :
                end = s - day
        range = pretty_range (start, end)
        drs = db.daily_record.filter \
            (None, dict (user = user, date = range), sort = ('+', 'date'))
        next = start
        for drid in drs :
            dr = db.daily_record.getnode (drid)
            _update_empty_dr (user, dr.date, next)
            daily_record_cache [(user, dr.date.pretty (ymd))] = dr
            next = dr.date + day
        _update_empty_dr (user, end, next)
    return daily_record_cache [(user, pdate)]
# end def get_daily_record

duration_cache = {}

def durations (db, user, date) :
    pdate = date.pretty (ymd)
    if (user, pdate) not in duration_cache :
        wday  = gmtime (date.timestamp ())[6]
        dyn   = get_user_dynamic (db, user, date)
        duration_cache [(user, pdate)] = \
            [0, 0, 0, 0, False, False, None, None, 0]
        if dyn :
            duration_cache [(user, pdate)] = \
                [ 0
                , day_work_hours (dyn, date)
                , (dyn.supp_weekly_hours or 0) * is_work_day (dyn, date)
                  / work_days (dyn)
                , (dyn.additional_hours  or 0) * is_work_day (dyn, date)
                  / work_days (dyn)
                , use_work_hours (db, dyn, 'week')
                , (  use_work_hours (db, dyn, 'month')
                  or use_work_hours (db, dyn, 'year')
                  )
                , None
                , None
                , dyn.supp_per_period
                ]
            dr = get_daily_record (db, user, date)
            if dr :
                duration_cache [(user, pdate)][0] = update_tr_duration (db, dr)
                duration_cache [(user, pdate)][6] = dr.status
                duration_cache [(user, pdate)][7] = dr.required_overtime
    return duration_cache [(user, pdate)]
# end def durations

def overtime (db, user, start, end, end_ov, use_additional) :
    overtime = 0
    required = 0
    worked   = 0
    compute  = False
    date     = start
    over_per = 0
    while date <= end_ov :
        dur      = durations (db, user, date)
        over_per = (use_additional and dur [8]) or 0
        work     = dur [0]
        req      = dur [1]
        over     = dur [2]
        do_over  = dur [4]
        if date > end :
            work = 0
            req  = 0
        if use_additional :
            over     = dur  [3]
            do_over  = dur  [5]
        overtime += over * do_over
        required += req  * do_over
        worked   += work * do_over
        compute   = compute or do_over
        date += Interval ('1d')
    overtime += over_per * do_over
    if worked > overtime :
        return worked - overtime
    elif worked < required :
        return worked - required
    return 0
# end def overtime

def invalidate_cache (user, date) :
    pdate = date.pretty (ymd)
    if (user, pdate) in duration_cache :
        del duration_cache [(user, pdate)]
# end def invalidate_cache

def compute_balance \
    (db, user, date, period, sharp_end = False, not_after = False) :
    day            = Interval ('1d')
    end            = freeze_date   (date, period)
    eop            = end_of_period (date + day, period)
    if not_after :
        eop        = date
    use_additional = period != 'week'
    id = db.daily_record_freeze.filter \
        ( None
        , dict ( user   = user
               , date   = (eop - day).pretty (';%Y-%m-%d')
               , frozen = True
               )
        , group = [('-', 'date')]
        )
    if id :
        prev = db.daily_record_freeze.getnode (id [0])
        p_balance = prev [period + '_balance']
        p_end     = freeze_date (prev.date, period)
        p_date    = p_end + day # start at day after last period ends
    else :
        dyn       = last_user_dynamic  (db, user)
        assert (not dyn.valid_to or dyn.valid_to >= date)
        fdyn      = dyn = first_user_dynamic (db, user)
        # loop over dyn recs until we find a hole or have reached the
        # freeze date. The first dyn record that reaches the freeze date
        # without a hole in between is our candidate.
        while dyn and dyn.valid_to and dyn.valid_to <= date :
            ldyn = dyn
            dyn  = find_user_dynamic \
                (db, dyn.user, dyn.valid_from, direction = '+')
            if dyn and dyn.valid_from > ldyn.valid_to :
                fdyn = dyn
        dyn = fdyn
        p_date    = dyn.valid_from
        p_balance = 0
        if p_date > end :
            return 0
    corr = db.overtime_correction.filter \
        (None, dict (user = user, date = pretty_range (p_date, end)))
    for c in corr :
        oc  = db.overtime_correction.getnode (c)
        dyn = get_user_dynamic (db, user, oc.date)
        if dyn and use_work_hours (db, dyn, period) :
            p_balance += oc.value or 0
    while p_date < end :
        eop = end_of_period (p_date, period)
        p_balance += overtime (db, user, p_date, eop, eop, use_additional)
        p_date = eop + day
    assert (p_date == end + day)
    eop = end_of_period (date, period)
    if sharp_end and date != eop :
        p_balance += overtime (db, user, p_date, date, eop, use_additional)
    return p_balance
# end def compute_balance

