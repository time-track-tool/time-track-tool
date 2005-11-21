#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    access routines for 'user_dynamic'
#

from roundup.date import Date
from time         import gmtime


dynamic = {} # cache

def get_user_dynamic (db, user, date) :
    """ Get a user_dynamic record by user and date.
        Return None if no record could be found.
    """
    global dynamic
    user = str  (user)
    date = Date (date)
    if user in dynamic :
        dyn = dynamic [user]
    else :
        dyn = [db.user_dynamic.getnode (i) for i in db.user_dynamic.filter
                (None, {'user' : user}, sort = ('-', 'valid_from'))
              ]
        dynamic [user] = dyn
    # search linearly -- we don't expect more than say 10-30 dynamic
    # user records per user. We dont want to have a binary search
    # algorithm here: the first record found is probably the current one
    # (the one with the latest start date) so we will usually match the
    # first here if not editing old records.
    for d in dyn :
        if date >= d.valid_from :
            if not d.valid_to or date < d.valid_to :
                return d
            break
    return None
# end def get_user_dynamic

def day_work_hours (dynuser, date) :
    """ Compute hours for a holiday etc from the date """
    wday  = gmtime (date.timestamp ())[6]
    field = 'hours_' + ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'][wday]
    hours = dynuser [field]
    if hours :
        return hours
    if wday in (5, 6) or not dynuser.weekly_hours :
        return 0
    return dynuser.weekly_hours / 5.
# end def day_work_hours

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
    hours   = 0.0
    hhours  = 0.0
    dyn     = get_user_dynamic (db, dr.user, dr.date) 
    tr_full = True
    wh      = 0
    if dyn :
        tr_full = dyn.travel_full
        wh      = round_daily_work_hours (day_work_hours (dyn, dr.date))
    trs     = []
    trvl_tr = []
    for t in dr.time_record :
        tr     = db.time_record.getnode (t)
        trs.append (tr)
        hours += tr.duration
        act    = tr.time_activity
        travel = not tr_full and act and db.time_activity.get (act, 'travel')
        if travel :
            hhours  += tr.duration / 2.
            trvl_tr.append (tr)
        else :
            hhours  += tr.duration
    sum, ratio = travel_worktime (hours, hhours, wh)
    for tr in trvl_tr :
        tr_duration = ratio * tr.duration
        if tr.tr_duration != tr_duration :
            db.time_record.set (tr.id, tr_duration = tr_duration)
# end def update_tr_duration

