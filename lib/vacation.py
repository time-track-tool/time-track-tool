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

import roundup.date

from common       import day, pretty_range
from user_dynamic import get_user_dynamic, day_work_hours
from user_dynamic import round_daily_work_hours

def try_create_public_holiday (db, daily_record, date, user) :
    dyn = get_user_dynamic (db, user, date)
    wh  = day_work_hours   (dyn, date)
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
            (None, {'date' : pretty_range (date, date), 'locations' : loc})
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
            wh = round_daily_work_hours (wh)
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
        pr = pretty_range (d, d)
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
        d += day
# end def create_daily_recs

def leave_days (db, user, first_day, last_day) :
    d = first_day
    s = 0.0
    while d <= last_day :
        dyn = get_user_dynamic (db, user, d)
        if not dyn :
            continue
        wh = day_work_hours (dyn, date)
        vd = vacation_duration (db, user, d)
        s += (vd / wh * 2 + 1) / 2
        d += day
    return s
# end def leave_days

def vacation_duration (db, user, date) :
    """ Duration of vacation on a single day to be booked. """
    dyn = get_user_dynamic (db, user, date)
    wh  = day_work_hours (dyn, date)
    if not wh :
        return 0.0
    dt  = pretty_range (date, date)
    dr  = db.daily_record.filter (None, dict (user = user, date = dt))
    assert len (dr) == 1
    trs = db.time_record.filter (None, dict (daily_record = dr [0]))
    bk  = 0.0
    for trid in trs :
        tr = db.time_record.getnode (trid)
        wp = db.time_wp.getnode (tr.wp)
        tp = db.time_project.getnode (wp.project)
        if tp.is_public_holiday :
            bk += tr.duration
    assert bk <= wh
    return wh - bk
# end def vacation_duration

def remaining_vacation (db, user, date) :
    """ Compute remaining vacation on the given date
    """
    pass
# end def remaining_vacation

### __END__
