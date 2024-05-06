#! /usr/bin/python
# Copyright (C) 2006-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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

from roundup.date import Date

import freeze
import common
import o_permission
ymd = common.ymd
day = common.day

def get_user_dynamic (db, user, date):
    """ Get a user_dynamic record by user and date.
        Return None if no record could be found.
    """
    user = str  (user)
    date = Date (date)
    # last_dynamic: Simple one-element cache as attribute of db
    try:
        if  (   db.last_dynamic
            and db.last_dynamic.user == user
            and db.last_dynamic.valid_from < date
            and (  not db.last_dynamic.valid_to
                or db.last_dynamic.valid_to > date
                )
            ):
            return db.last_dynamic
    except AttributeError:
        db.last_dynamic = None
        def last_dynamic_clear (db):
            db.last_dynamic = None
        db.registerClearCacheCallback (last_dynamic_clear, db)
    ids = db.user_dynamic.filter \
        ( None, dict (user = user, valid_from = date.pretty (';%Y-%m-%d'))
        , group = ('-', 'valid_from')
        )
    if ids:
        db.last_dynamic = db.user_dynamic.getnode (ids [0])
        if not db.last_dynamic.valid_to or db.last_dynamic.valid_to > date:
            return db.last_dynamic
    return None
# end def get_user_dynamic

def first_user_dynamic (db, user, direction = '+', date = None):
    """Search for first user_dynamic record, optionally starting at
       date.
       
       The direction may be specified as '-' to search for the last
       record, see last_user_dynamic
    """
    filter_dict = dict (user = user)
    if date:
        format = '%Y-%m-%d;'
        if direction == '-':
            format = ';%Y-%m-%d'
        filter_dict ['valid_from'] = date.pretty (format)
    ids = db.user_dynamic.filter \
        (None, filter_dict, group = (direction, 'valid_from'))
    if ids:
        dyn = db.user_dynamic.getnode (ids [0])
        # one record too far?
        if date and direction == '+' and dyn.valid_from > date:
            d = prev_user_dynamic (db, dyn)
            if d and d.valid_from <= date and d.valid_to > date:
                return d
        return dyn
    elif date and direction == '+':
        dyn = last_user_dynamic (db, user)
        if  (   dyn
            and dyn.valid_from <= date
            and (not dyn.valid_to or dyn.valid_to > date)
            ):
            return dyn
    return None
# end def first_user_dynamic

def last_user_dynamic (db, user, date = None):
    """Search for last user_dynamic record, optionally searching
       backwards from date.
    """
    return first_user_dynamic (db, user, direction = '-', date = date)
# end def last_user_dynamic

def find_user_dynamic (db, user, date, direction = '+', ct = -1):
    """ Search for the next user dynamic record in the given direction
        for this user and date. If ct (contract_type) is given, we find
        only dynamic user records with that contract type. Note that the
        contract_type 'None' is special, it searches for the default ct
        which is empty. This is handled specially in the roundup API, it
        uses the *string* '-1' for the id which indicates searching for
        an empty Link or Multilink. That's why a don't-care
        contract_type is encoded with -1 here (something other than
        None).
    """
    date = common.next_search_date (date, direction)
    d    = dict (user = user, valid_from = date)
    if ct != -1:
        if ct is None:
            # '-1' is special, it searches for empty ct
            d.update (contract_type = '-1')
        else:
            d.update (contract_type = ct)
    ids = db.user_dynamic.filter (None, d, group = (direction, 'valid_from'))
    if ids:
        return db.user_dynamic.getnode (ids [0])
    return None
# end def find_user_dynamic

def _next_user_dynamic (db, dynuser, direction = '+', use_ct = False):
    id = dynuser.user
    try:
        db = db._db
        id = id.id
    except AttributeError:
        pass
    vf = dynuser.valid_from
    if not isinstance (vf, Date):
        try:
            vf = Date (dynuser.valid_from._value)
        except (ValueError, AttributeError):
            return None
    ct = -1
    if use_ct:
        ct = dynuser.contract_type
    return find_user_dynamic (db, id, vf, direction = direction, ct = ct)
# end def _next_user_dynamic

def next_user_dynamic (db, dynuser, use_ct = False):
    return _next_user_dynamic (db, dynuser, use_ct = use_ct)
# end def next_user_dynamic

def prev_user_dynamic (db, dynuser, use_ct = False):
    return _next_user_dynamic (db, dynuser, direction = '-', use_ct = use_ct)
# end def prev_user_dynamic

def next_allowed_user_dynamic (db, dynuser, use_ct = False):
    hypdb = db
    try:
        hypdb = db._db
    except AttributeError:
        pass
    uid = hypdb.getuid ()
    dyn = next_user_dynamic (db, dynuser, use_ct)
    allowed = o_permission.dynamic_user_allowed_by_olo
    while dyn and not allowed (hypdb, uid, dyn.id):
        dyn = next_user_dynamic (hypdb, dyn, use_ct)
    return dyn
# end def next_allowed_user_dynamic

def prev_allowed_user_dynamic (db, dynuser, use_ct = False):
    hypdb = db
    try:
        hypdb = db._db
    except AttributeError:
        pass
    uid = hypdb.getuid ()
    dyn = prev_user_dynamic (db, dynuser, use_ct)
    allowed = o_permission.dynamic_user_allowed_by_olo
    while dyn and not allowed (hypdb, uid, dyn.id):
        dyn = prev_user_dynamic (hypdb, dyn, use_ct)
    return dyn
# end def prev_allowed_user_dynamic

def act_or_latest_user_dynamic (db, user, check_o_perm = True):
    """ Used typically from web interface
    """
    uid = db.getuid ()
    ud  = get_user_dynamic (db, user, Date ('.'))
    if check_o_perm:
        allowed = o_permission.dynamic_user_allowed_by_olo
    else:
        def allowed (*args):
            return True
    if not ud or not allowed (db, uid, ud.id):
        ud = last_user_dynamic (db, user)
    if ud and allowed (db, uid, ud.id):
        return ud
    return None
# end def act_or_latest_user_dynamic

wdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

def day_work_hours (dynuser, date):
    """ Compute hours for a holiday etc from the date """
    wday  = gmtime (date.timestamp ())[6]
    return _day_work_hours (dynuser, wday)
# end def day_work_hours

def _day_work_hours (dynuser, wday):
    if not dynuser:
        return 0
    hours = dynuser ['hours_' + wdays [wday]]
    if hours is not None:
        return hours
    if wday in (5, 6) or not dynuser.weekly_hours:
        return 0
    return dynuser.weekly_hours / 5.
# end def _day_work_hours

def weekly_hours (dynuser):
    return sum (_day_work_hours (dynuser, wday) for wday in range (7))
# end def weekly_hours

def is_work_day (dynuser, date):
    """ Return True if the given date is a work day for this user.
        Usually returns True if not on a weekend day but individual work
        times can be defined with field_mon, ..., field_sun
    """
    return bool (day_work_hours (dynuser, date))
# end def is_work_day

def use_work_hours (db, dynuser, period):
    """ Check if work hours for given dynuser record should be used at
        all in overtime computation. They will not be used if the sum of
        required hours or the sum of overtime is zero (period denotes if
        we want the result for week/month/year).
    """
    if not dynuser:
        return False
    overtime   = dynuser.additional_hours
    period_id  = dynuser.overtime_period
    if common.period_is_weekly (period):
        overtime = dynuser.supp_weekly_hours
    if period.required_overtime:
        overtime = True
    return bool (dynuser.weekly_hours and overtime and period_id == period.id)
# end def use_work_hours

def work_days (dynuser):
    """ Work days per week for this user. Returns number of days for
        which a non-zero day_work_hours is defined. This is used for
        overtime and additional time computation: We need to know the
        ratio for a given day...
    """
    s = sum (bool (dynuser ['hours_' + f]) for f in wdays)
    return s or 5
# end def work_days

def round_daily_work_hours (hours):
    """ Rounding of daily work hours.
        >>> round_daily_work_hours (38.5 / 5)
        7.75
    """
    return int (hours * 4. + .5) / 4.
# end def round_daily_work_hours

def travel_worktime (full_hours, half_hours, daily_hours):
    """Compute the time taking halved travel into account. Return a
       tuple consisting of the travel work-time and the ratio by which
       the work-time was reduced.
    
       >>> travel_worktime ( 8,  4, 8)
       (8, 1.0)
       >>> print ("%d %.6f" % travel_worktime (12,  6, 8))
       8 0.666667
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
    if half_hours > daily_hours:
        ret = half_hours
    if travel:
        ratio = (travel - (full_hours - ret)) / travel
    else:
        ratio = 1.0
    return ret, ratio
# end def travel_worktime

def update_tr_duration (db, dr):
    """Compute duration including travel for the given daily record.
       The dr must be the node from the db not just the id.
       Travel time records will have their tr_duration field updated.
    """
    if dr.tr_duration_ok is not None:
        return dr.tr_duration_ok
    hours   = 0.0
    hhours  = 0.0
    dyn     = get_user_dynamic (db, dr.user, dr.date) 
    tr_full = True
    wh      = 0
    if dyn:
        tr_full = dyn.travel_full
        wh      = round_daily_work_hours (day_work_hours (dyn, dr.date))
        if dyn.overtime_period:
            otp = db.overtime_period.getnode (dyn.overtime_period)
            if otp.required_overtime:
                rotp, wd, rq = required_overtime_params \
                    (db, dr.user, dr.date, dyn, otp)
                wh += rq
    trs     = []
    trvl_tr = {}
    for t in dr.time_record:
        tr     = db.time_record.getnode (t)
        trs.append (tr)
        hours += tr.duration
        act    = tr.time_activity
        travel = not tr_full and act and db.time_activity.get (act, 'travel')
        if travel:
            hhours  += tr.duration / 2.
            trvl_tr [tr.id] = tr
        else:
            hhours  += tr.duration
    sum, ratio = travel_worktime (hours, hhours, wh)
    for tr in trs:
        if tr.id in trvl_tr:
            tr_duration = ratio * tr.duration
        else:
            tr_duration = tr.duration
        if tr.tr_duration != tr_duration:
            db.time_record.set (tr.id, tr_duration = tr_duration)
    db.daily_record.set (dr.id, tr_duration_ok = sum)
    return sum
# end def update_tr_duration

def _update_empty_dr (db, user, date, next):
    d = next
    while d <= date:
        db.daily_record_cache [(user, d.pretty (ymd))] = None
        d = d + day
# end def _update_empty_dr

def get_daily_record (db, user, date):
    """ Use caching: prefetch all records from given date until now and
        store them. Use a per-user cache of the earliest dr found.
    """
    pdate = date.pretty (ymd)
    date  = Date (pdate)
    now   = Date (Date ('.').pretty (ymd))
    if not getattr (db, 'daily_record_cache', None):
        db.daily_record_cache = {}
        def daily_record_cache_clear (db):
            db.daily_record_cache = {}
        db.registerClearCacheCallback (daily_record_cache_clear, db)
    if (user, pdate) not in db.daily_record_cache:
        if date < now:
            start = date
            end   = now
        else:
            start = now
            end   = date
        range = common.pretty_range (start, end)
        drs = db.daily_record.filter \
            (None, dict (user = user, date = range), sort = ('+', 'date'))
        next = start
        for drid in drs:
            dr = db.daily_record.getnode (drid)
            _update_empty_dr (db, user, dr.date, next)
            db.daily_record_cache [(user, dr.date.pretty (ymd))] = dr
            next = dr.date + day
        _update_empty_dr (db, user, end, next)
    return db.daily_record_cache [(user, pdate)]
# end def get_daily_record

def req_overtime_quotient (db, dyn, user, date):
    """ Compute the required overtime for this day as a quotient of
        - duration of packages without overtime_reduction 
        - overall duration of day
        we use a cache.
    """
    if not dyn:
        return 0.0
    key = (user, str (date))
    if not getattr (db, 'cache_required_overtime_quotient', None):
        def cache_required_overtime_quotient_clear (db):
            db.cache_required_overtime_quotient = {}
        db.registerClearCacheCallback \
            (cache_required_overtime_quotient_clear, db)
        db.cache_required_overtime_quotient = {}
    if key in db.cache_required_overtime_quotient:
        return db.cache_required_overtime_quotient [key]
    dr  = get_daily_record (db, user, date)
    otr = 0.0
    all = 0.0
    if dr:
        for t in dr.time_record:
            tr = db.time_record.getnode (t)
            if tr.wp:
                wp = db.time_wp.getnode (tr.wp)
                pr = db.time_project.getnode (wp.project)
                if pr.overtime_reduction:
                    otr += tr.duration
            all += tr.duration
    # If we wanted to set the required overtime to 0 for a
    # holiday or other payed leave, we'd use
    # otd = float (not otr)
    # instead of the following averaging expression:
    otd = 1.0
    if all:
        otd = ((all - otr) / all)
    otd *= is_work_day (dyn, date)
    db.cache_required_overtime_quotient [key] = otd
    return otd
# end def req_overtime_quotient

def required_overtime_in_period (db, user, date, period):
    """ Loop over a whole period and compute the required overtime in
        that period and the number of workdays in that period.
        Return a tuple of overtime, workdays.
    """
    assert period.required_overtime
    sop = common.start_of_period (date, period)
    eop = common.end_of_period   (date, period)
    key = (user, str (sop))
    if not getattr (db, 'cache_required_overtime_in_period', None):
        def cache_required_overtime_in_period_clear (db):
            db.cache_required_overtime_in_period = {}
        db.registerClearCacheCallback \
            (cache_required_overtime_in_period_clear, db)
        db.cache_required_overtime_in_period = {}
    if key in db.cache_required_overtime_in_period:
        return db.cache_required_overtime_in_period [key]
    wd   = 0.0
    spp  = 0.0
    date = sop
    #print >> sys.stderr, sop, eop
    while date <= eop:
        dyn   = get_user_dynamic (db, user, date)
        is_wd = is_work_day (dyn, date)
        if not dyn:
            wday  = gmtime (date.timestamp ())[6]
            is_wd = wday < 5
        wd += 1.0 * is_wd
        if dyn and period.id == dyn.overtime_period:
            otd  = req_overtime_quotient (db, dyn, user, date)
            if dyn.supp_per_period:
                spp += dyn.supp_per_period * otd
        date += day
    # otdsum (the sum of all overtime day ratios, sum of otd above)
    # spp / otdsum is dyn.supp_per_period if supp_per_period doesn't change
    # otherwise we get a weighted average
    # then we have to multiply the weighted average with the quotient of
    # overtime_days and workdays (otd / wd), this yields
    # (otdsum / wd) * (spp / otdsum)
    # which can be reduced to (spp / wd)
    # that's why we don't compute otdsum.
    if not spp:
        # probably wd is also 0 here, avoid division by zero
        r = db.cache_required_overtime_in_period [key] = (0.0, wd)
    else:
        r = db.cache_required_overtime_in_period [key] = (spp / wd, wd)
    return r
# end def required_overtime_in_period

def required_overtime_params (db, user, date, dyn, period):
    """ Convenience method returning all required overtime parameters.
        The tuple (overtime, workdays, overtime_quotient)
    """
    if dyn and period and period.required_overtime:
        spp = dyn.supp_per_period or 0
        rotp, wd = required_overtime_in_period (db, user, date, period)
        if not wd:
            # probably spp is also 0 here, avoid division by zero
            rq = 0.0
        else:
            rq = req_overtime_quotient (db, dyn, user, date) * spp / wd
        return (rotp, wd, rq)
    return (0.0, 1.0, 0.0)
# end def required_overtime_params


class Duration (object):
    def __init__ \
        ( self
        , db
        , user
        , date
        , dyn               = None
        , tr_duration       = 0
        , day_work_hours    = 0
        , supp_weekly_hours = 0
        , additional_hours  = 0
        , dr_status         = None
        , supp_per_period   = 0
        , req_overtime_pp   = 0.0
        , work_days         = 1.0
        , required_overtime = 0.0
        ):
        self.db                = db
        self.dyn               = dyn
        self.user              = user
        self.date              = date
        self.tr_duration       = tr_duration
        self.day_work_hours    = day_work_hours
        self.supp_weekly_hours = supp_weekly_hours
        self.additional_hours  = additional_hours
        self.dr_status         = dr_status
        self.supp_per_period   = supp_per_period
        self.req_overtime_pp   = req_overtime_pp
        self.work_days         = work_days
        self.required_overtime = required_overtime
        if dyn:
            self.supp_per_period = dyn.supp_per_period
    # end def __init__

    def __str__ (self):
        return "Duration (%(user)s, %(date)s)" % self.__dict__
    __repr__ = __str__
# end class Duration

def durations (db, user, date):
    pdate = date.pretty (ymd)
    wday  = gmtime (date.timestamp ())[6]
    dyn   = get_user_dynamic (db, user, date)
    if dyn:
        if dyn.overtime_period:
            period = db.overtime_period.getnode (dyn.overtime_period)
        else:
            period = None
        rotp, wd, rq = required_overtime_params (db, user, date, dyn, period)
        dc = Duration \
            ( db
            , user
            , date
            , dyn
            , day_work_hours    = day_work_hours (dyn, date)
            , supp_weekly_hours = \
                (dyn.supp_weekly_hours or 0) * is_work_day (dyn, date)
                / work_days (dyn)
            , additional_hours  = \
                (dyn.additional_hours  or 0) * is_work_day (dyn, date)
                / work_days (dyn)
            , req_overtime_pp   = rotp
            , work_days         = wd
            , required_overtime = rq
            )
        dr = get_daily_record (db, user, date)
        if dr:
            dc.tr_duration      = update_tr_duration (db, dr)
            dc.dr_status        = dr.status
    else:
        dc = Duration (db, user, date)
    return dc
# end def durations

class Period_Data (object):
    def __init__ \
        ( self
        , db
        , user
        , start
        , end
        , period
        , start_balance
        , overtime_corrections = {}
        ):
        use_additional        = not period.weekly
        overtime              = 0.0
        overtadd              = 0.0
        required              = 0.0
        worked                = 0.0
        over_per              = 0.0
        over_per_2            = 0.0
        days                  = 0.0
        self.achieved_supp    = 0.0
        self.overtime_balance = 0.0
        self.start_balance    = start_balance
        self.period           = period
        date                  = common.start_of_period (start, self.period)
        eop                   = common.end_of_period   (end,   self.period)
        try:
            s, e, p           = overtime_period (db, user, start, end, period)
        except TypeError:
            s, e, p           = eop + day, eop + day, self.period
        assert (p.id == self.period.id)
        opp = 0
        while date <= eop:
            days     += 1.0
            d         = date
            date     += day
            if d < s or d > e:
                continue
            dur       = durations (db, user, d)

            if  (   dur.dyn
                and period.required_overtime
                and dur.dyn.overtime_period == period.id
                ):
                if opp == 0:
                    opp = dur.req_overtime_pp
                elif opp != dur.req_overtime_pp:
                    #print >> sys.stderr, "Oops:", opp, dur.req_overtime_pp
                    opp = None
            over_per += \
                (   period.months
                and dur.dyn
                and dur.dyn.overtime_period == self.period.id
                and dur.supp_per_period
                ) or 0
        assert (days)
        if period.required_overtime:
            self.overtime_per_period = opp
        else:
            self.overtime_per_period = over_per / days
        date = start
        while date <= end:
            dur       = durations (db, user, date)
            work      = dur.tr_duration
            req       = dur.day_work_hours
            over      = dur.supp_weekly_hours
            do_over   = use_work_hours (db, dur.dyn, period)
            oc        = overtime_corrections.get (date.pretty (ymd), [])
            for o in oc:
                self.overtime_balance += o.value or 0
            if use_additional:
                over  = dur.additional_hours
            if period.required_overtime:
                over  = req + dur.required_overtime
            overtime += over * do_over
            if period.months and date <= end:
                overtadd += dur.additional_hours * do_over
            required += req  * do_over
            worked   += work * do_over
            eow       = common.week_from_date (date) [1]
            if  (   date == eow
                and period.months
                and (period.weekly or period.required_overtime)
                ):
                if period.required_overtime:
                    self.overtime_balance += worked - overtime
                else:
                    if worked > overtadd:
                        self.achieved_supp += min (worked, overtime) - overtadd
                    if worked > overtime:
                        self.overtime_balance += worked - overtime
                    elif worked < required:
                        self.overtime_balance += worked - required
                overtadd = overtime = worked = required = 0.0
                self._consolidate ()
            # increment at end (!)
            date += day

        if not period.weekly and not period.required_overtime:
            overtime += self.overtime_per_period
        if worked > overtadd and period.months:
            if period.weekly:
                self.achieved_supp += min (worked, overtime) - overtadd
            elif not period.required_overtime:
                self.achieved_supp += worked - overtadd
        if worked > overtime:
            self.overtime_balance += worked - overtime
        elif period.required_overtime:
            if worked < overtime:
                self.overtime_balance += worked - overtime
        else:
            if worked < required:
                self.overtime_balance += worked - required
        self._consolidate  ()
        if self.overtime_per_period is None:
            self.achieved_supp = None
        else:
            self.achieved_supp = min \
                (self.achieved_supp, self.overtime_per_period)
    # end def __init__

    def _consolidate (self):
        """ consolidate overtime_balance and achieved_supp:
            - achieved_supp must not exceed overtime_per_period
              exceeding hours are added to overtime_balance
            - if balance is negative, use hours from achieved first
        """
        if self.period.months and self.period.weekly:
            if self.achieved_supp > self.overtime_per_period:
                self.overtime_balance += \
                    self.achieved_supp - self.overtime_per_period
                self.achieved_supp = self.overtime_per_period
            if self.overtime_balance + self.start_balance < 0:
                #print "Balance underrun:",
                #print self.overtime_balance + self.start_balance,
                #print self.achieved_supp
                to_add = min \
                    ( self.achieved_supp
                    , - (self.overtime_balance + self.start_balance)
                    )
                self.overtime_balance  += to_add
                self.achieved_supp     -= to_add
    # end def _consolidate
# end class Period_Data

def overtime_periods (db, user, start, end):
    """ Compute list of 3-tuples start, end, overtime_period. """
    periods = []
    if start > end:
        return periods
    dyn = first_user_dynamic (db, user, date = start)
    while (dyn and dyn.valid_from <= end):
        if dyn.overtime_period:
            ot  = db.overtime_period.getnode (dyn.overtime_period)
            frm = max (dyn.valid_from, start)
            to  = end
            if dyn.valid_to:
                to = min (dyn.valid_to - day, end)
            if periods and periods [-1][2].id == ot.id:
                periods [-1][1] = to
            else:
                periods.append ([frm, to, ot])
        dyn = next_user_dynamic (db, dyn)
    return periods
# end def overtime_periods

def overtime_period (db, user, start, end, period):
    """ Return triple start, end, period for the given date which represents a
        contiguous range of the same overtime_period in this users dynamic user
        data
    """
    periods = []
    sop     = common.start_of_period (start, period)
    eop     = common.end_of_period   (end,   period)
    otp     = overtime_periods (db, user, sop, eop)
    for s, e, p in otp:
        #print period.id, p.id, start, s, e, end
        if  (   p.id == period.id
            and start >= s and start < e or end > s and end <= e
            ):
            periods.append ((s, e, p))
    #print user, sop, eop, otp
    # this fails if somebody has the idea of switching twice within a week or so
    assert (len (periods) <= 1)
    if not periods:
        return None
    return periods [0]
# end def overtime_period

def compute_saved_balance (db, user, start, date, not_after = False):
    """ Compute the saved overtime balance before or at the given day
        and the date on which this balance is valid.
        
        This looks through saved values in freeze records and determines
        a matching freeze record and returns the value for the given
        weekly/monthly period.

        If not_after is True, we use the next end of period for
        searching for existing freeze records. This is used for
        freezing: we don't want to find records at the freeze date.

        Implementation note: we search for freeze records before the end
        of period one day *after* date. This is exactly the same end of
        period as for date in the usual case. In case date *is* the end
        of period, this will include freeze records with freeze_date ==
        date.
    """
    period = None
    dyn = get_user_dynamic (db, user, date)
    if dyn and dyn.overtime_period:
        period = db.overtime_period.getnode (dyn.overtime_period)
    eop = date
    if period and not not_after:
        eop = common.end_of_period (date + day, period)
    r = freeze.find_prev_dr_freeze (db, user, eop)
    if r:
        achieved = bool (date == r.validity_date) * r.achieved_hours
        return r.balance, r.validity_date, achieved
    return 0.0, None, 0.0
# end def compute_saved_balance

def overtime_corr (db, user, start, end):
    """ Return overtime corrections in given time range. """
    cids = db.overtime_correction.filter \
        (None, dict (user = user, date = common.pretty_range (start, end)))
    corr = {}
    for c in cids:
        oc  = db.overtime_correction.getnode (c)
        dyn = get_user_dynamic (db, user, oc.date)
        if dyn:
            d = oc.date.pretty (ymd)
            if d not in corr:
                corr [d] = []
            corr [d].append (oc)
    return corr
# end def overtime_corr

def compute_running_balance \
    (db, user, start, date, period, sharp_end = False, start_balance = 0.0):
    """ Compute the overtime balance at the given date.
        if not_after is True, we use the next end of period for
        searching for existing freeze records.

        If sharp_end is True, we compute the exact balance on that day,
        not on the end of previous period.

        If not_after is True, we use the next end of period for
        searching for existing freeze records. This is used for
        freezing: we don't want to find records at the freeze date.
    """
    c_end = end = common.freeze_date (date, period)
    if sharp_end:
        c_end  = date
    p_date     = start
    p_balance  = start_balance
    p_achieved = 0

    corr = overtime_corr (db, user, p_date, c_end)
    while p_date <= end:
        eop = common.end_of_period (p_date, period)
        #print >> sys.stderr, "OTB1: pd: %s d: %s e:%s eop:%s" \
        #    % ( p_date.pretty (ymd)
        #      , date.pretty   (ymd)
        #      , end.pretty    (ymd)
        #      , eop.pretty    (ymd)
        #      )
        pd  = Period_Data (db, user, p_date, eop, period, p_balance, corr)
        p_balance += pd.overtime_balance
        p_achieved = pd.achieved_supp
        #print >> sys.stderr, "OTB1: bal:%.2f as:%.2f" \
        #    % (pd.overtime_balance, pd.achieved_supp)
        p_date = eop + day
    #print "pdate: %(p_date)s, end: %(end)s, date: %(date)s" % locals ()
    #print "bal:", p_balance - start_balance
    assert (p_date <= date + day)
    eop = common.end_of_period (date, period)
    #print >> sys.stderr, "before 2nd call", sharp_end, date, eop, p_date, end
    if sharp_end and date != eop and p_date <= date:
        #print >> sys.stderr, "OTB2: pd: %s d: %s e:%s eop:%s" \
        #    % ( p_date.pretty (ymd)
        #      , date.pretty   (ymd)
        #      , end.pretty    (ymd)
        #      , eop.pretty    (ymd)
        #      )
        pd = Period_Data (db, user, p_date, date, period, p_balance, corr)
        p_balance += pd.overtime_balance
        p_achieved = pd.achieved_supp
        #print >> sys.stderr, "OTB2: bal:%.2f as:%.2f" \
        #    % (pd.overtime_balance, pd.achieved_supp)
        #print eop.pretty (ymd), "%.02f %.02f %.02f" \
        #    % (pd.overtime_balance, pd.achieved_supp, pd.overtime_per_period)
    #print "bal:", p_balance - start_balance
    return p_balance - start_balance, p_achieved
# end def compute_running_balance

def compute_balance (db, user, date, sharp_end = False, not_after = False):
    """ Compute the overtime balance at the given day.
        if not_after is True, we use the next end of period for
        searching for existing freeze records.

        If sharp_end is True, we compute the exact balance on that day,
        not on the end of previous period.

        If not_after is True, we use the next end of period for
        searching for existing freeze records. This is used for
        freezing: we don't want to find records at the freeze date.
    """
    dyn       = first_user_dynamic (db, user)
    if dyn:
        start = dyn.valid_from
    else:
        start = date + day
    balance, n_start, achieved = compute_saved_balance \
        (db, user, start, date, not_after)
    if n_start:
        start = n_start + day # start after freeze date
    #print >> sys.stderr, "OTP:", start, date
    periods   = overtime_periods (db, user, start, date)
    corr = overtime_corr (db, user, start, date)
    if periods:
        end   = periods [-1][1]
    for frm, to, otp in periods:
        # compute sharp end for intermediate periods *and* if the last
        # period happens to end before our end date in which case we
        # need to take the last several days of the last period into
        # account.
        sharp = sharp_end or to != end or end < date
        rb, ach = compute_running_balance \
            (db, user, frm, to, otp, sharp, start_balance = balance)
        balance  += rb
        achieved  = ach
        for d in overtime_corr (db, user, frm, to):
            del corr [d]
    # overtime corrections not yet covered:
    for k in corr:
        for c in corr [k]:
            balance += c.value or 0
    if abs (balance)  < 1e-14:
        balance  = 0.0
    if abs (achieved) < 1e-14:
        achieved = 0.0
    #print date, balance, achieved
    return balance, achieved
# end compute_balance

def hr_olo_role_for_this_user_dyn (db, dbuid, userdyn):
    """ Given db uid has role HR-Org-Location and the given dynamic user
        is in the same Org-Location as the uid.
        With introduction of o_permission HR and HR-Org-Location roles
        are equal. We now use the o_permission check.
    """
    if not common.user_has_role (db, dbuid, 'HR', 'HR-Org-Location'):
        return False
    return o_permission.dynamic_user_allowed_by_olo (db, dbuid, userdyn.id)
# end def hr_olo_role_for_this_user_dyn

def hr_olo_role_for_this_user (db, dbuid, userid, date = None):
    """ dbuid has role HR or HR-Org-Location and the given user is in
        the same Org-Location (on given date) as the dbuid.
        Use todays date for the check if no date given.
    """
    if not date:
        date = Date ('.')
    dyn = get_user_dynamic (db, userid, date)
    if not dyn:
        return False
    return hr_olo_role_for_this_user_dyn (db, dbuid, dyn)
# end def hr_olo_role_for_this_user

def required_overtime (db, user, frm):
    """ If required_overtime flag is set for overtime_period of dynamic
        user record at frm, we return the overtime_period belonging to
        this dyn user record. Otherwise return None.
    """
    dyn = get_user_dynamic (db, user, frm)
    if dyn and dyn.overtime_period:
        otp = db.overtime_period.getnode (dyn.overtime_period)
        if otp.required_overtime:
            return otp
    return None
# end def required_overtime

def invalidate_tr_duration (db, uid, v_frm, v_to):
    """ Invalidate all cached tr_duration_ok values in all daily records
        in the given range for the given uid.
        We modify v_frm and/or v_to if these use required_overtime in
        their overtime_period: In that case we need to invalidate the
        whole month.
        We also invalidate computations on v_to (which is too far) but
        these get recomputed (we're in a non-frozen range anyway).
        Make sure the tr_duration_ok is *really* set even if our cached
        value is None.
    """
    otp = required_overtime (db, uid, v_frm)
    if otp:
        start = common.start_of_period (v_frm, otp)
        if freeze.frozen (db, uid, start):
            frz    = freeze.find_next_dr_freeze (db, uid, start)
            start  = frz.date
            assert (start <= v_frm)
        v_frm = start

    if v_to is None:
        pdate = v_frm.pretty (ymd) + ';'
    else:
        otp = required_overtime (db, uid, v_to)
        if otp:
            v_to = common.end_of_period (v_to, otp)
        pdate = ';'.join ((v_frm.pretty (ymd), v_to.pretty (ymd)))
    for dr in db.daily_record.filter (None, dict (date = pdate, user = uid)):
        db.daily_record.set (dr, tr_duration_ok = 0)
        db.daily_record.set (dr, tr_duration_ok = None)
# end def invalidate_tr_duration

def user_dynamic_year_iter (db, user, date_in_year):
    y   = common.start_of_year (date_in_year)
    eoy = common.end_of_year (y)
    dyn = get_user_dynamic (db, user, y)
    if not dyn:
        dyn = first_user_dynamic (db, user, date = y)
    if not dyn:
        return
    yield dyn
    while dyn:
        dyn = next_user_dynamic (db, dyn)
        if not dyn or dyn.valid_from > eoy:
            return
        yield (dyn)
# end def user_dynamic_year_iter

dynuser_copyfields = \
     [ 'user'
     , 'booking_allowed'
     , 'durations_allowed'
     , 'daily_worktime'
     , 'weekend_allowed'
     , 'travel_full'
     , 'vacation_yearly'
     , 'weekly_hours'
     , 'supp_weekly_hours'
     , 'supp_per_period'
     , 'hours_mon'
     , 'hours_tue'
     , 'hours_wed'
     , 'hours_thu'
     , 'hours_fri'
     , 'hours_sat'
     , 'hours_sun'
     , 'org_location'
     , 'all_in'
     , 'additional_hours'
     , 'overtime_period'
     , 'sap_cc'
     , 'contract_type'
     , 'vac_aliq'
     , 'max_flexitime'
     , 'valid_to'
     , 'do_auto_wp'
     ]

def is_tt_user_status (db, status):
    """ Get all stati with 'timetracking_allowed' set if property exists
        Otherwise simply use 'valid' status
    """
    s = None
    assert 'user_status' in db.classes
    if 'timetracking_allowed' in db.user_status.properties:
        s = db.user_status.filter (None, dict (timetracking_allowed = True))
    else:
        s = [db.user_status.lookup ('valid')]
    if s is not None:
        return status in s
    return True
# end def is_tt_user_status

def check_email (db, contacts, email, t_email):
    for c in contacts:
        contact = db.user_contact.getnode (c)
        if (contact.contact == email and contact.contact_type == t_email):
            return True
    return False
# end def check_email

def user_create_magic (db, uid, olo):
    """ Perform magic on new user creation
        We used to create a dynamic user record here, this is no longer
        done.
        If at least the org_location is given, we look up the mail
        domain and create email addresses if the user doesn't have any
        contacts yet.
        We also set nickname and lunch duration/lunch_start values if
        those are not yet set for the user.
        And of course we do all this only for timetracking users.
    """
    assert 'user_status' in db.classes
    cl   = db.user
    user = cl.getnode (uid)
    if not is_tt_user_status (db, user.status):
        return
    org_location = None
    if olo:
        org_location = db.org_location.getnode (olo)
    _ = db.i18n.gettext

    update_dict = {}
    if  (   'nickname' in cl.properties and 'firstname' in cl.properties
        and not user.nickname
        ):
        fn    = user.firstname
        ln    = user.lastname
        lfn   = common.tolower_ascii (fn)
        lln   = common.tolower_ascii (ln)
        cnick = getattr (db.config.ext, 'MISC_CREATE_NICKNAME', None)
        if cnick is None:
            cnick = 'yes'
        cnick = cnick.lower () in ('yes', 'true')
        if cnick:
            nickname = common.new_nickname (_, cl, uid, lfn, lln)
            if nickname:
                update_dict ['nickname'] = nickname

    maildomain = None
    if org_location and 'mail_domain' in db.organisation.properties:
        maildomain = db.organisation.get \
            (org_location.organisation, 'mail_domain')
    if maildomain and not user.contacts:
        assert not user.address and not user.alternate_addresses
        if 'contacts' in cl.properties:
            try:
                email = db.uc_type.lookup ('Email')
            except KeyError:
                email = None
            contacts = []
            ms = \
                ( '@'.join (('.'.join ((lfn, lln)), maildomain))
                , '@'.join ((user.username, maildomain))
                )
            for n, m in enumerate (ms):
                if not check_email (db, contacts, m, email):
                    c = db.user_contact.create \
                        ( contact      = m
                        , contact_type = email
                        , order        = 1 + n
                        )
                    contacts.append (c)
            if contacts:
                update_dict ['contacts'] = contacts
    if 'lunch_duration' in cl.properties:
        if not user.lunch_duration:
            update_dict ['lunch_duration'] = .5
        if not user.lunch_start:
            update_dict ['lunch_start'] = '12:00'
    if update_dict:
        db.user.set (uid, **update_dict)
    db.commit ()
# end def user_create_magic

def find_dynuser_gaps (db, start_date = None, users = None, olo = None):
    """ Loop over dynamic users and find gaps where the user was not
        employed. Optionally filter list by o_permission on the *later*
        record of each pair.
    """
    if start_date is None:
        start_date = Date ('.')
    filt = dict (valid_from = common.pretty_range (start_date))
    if users:
        filt.update (user = users)
    if olo:
        filt.update (org_location = olo)
    sort = [('+', 'user'), ('+', 'valid_from')]
    user = None
    ret  = []
    prev = None
    seen = set ()
    for dynid in db.user_dynamic.filter (None, filt, sort = sort):
        dyn = db.user_dynamic.getnode (dynid)
        if dyn.user != user:
            user = dyn.user
            prev = dyn
            dynp = prev_user_dynamic (db, dyn)
            if dynp and dynp.id not in seen:
                if dyn.valid_from != dynp.valid_to:
                    ret.append ((dynp, dyn))
            continue
        if dyn.valid_from != prev.valid_to:
            ret.append ((prev, dyn))
        prev = dyn
        seen.add (dyn.id)
    return ret
# end def find_dynuser_gaps

def find_dynuser_company_changes (db, start_date):
    filt = dict (valid_from = common.pretty_range (start_date))
    sort = [('+', 'user'), ('+', 'valid_from')]
    olo  = None
    user = None
    ret  = []
    prev = None
    for dynid in db.user_dynamic.filter (None, filt, sort = sort):
        dyn = db.user_dynamic.getnode (dynid)
        if dyn.user != user:
            user = dyn.user
            olo  = dyn.org_location
            prev = dyn
            continue
        if dyn.org_location != olo:
            ret.append ((prev, dyn))
            olo  = dyn.org_location
        prev = dyn
    return ret
# end def find_dynuser_company_changes

#END
