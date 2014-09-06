#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
import csv
from math              import ceil
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

sys.path.insert (1, os.path.join (dir, 'lib'))
import common
import user_dynamic

#      Name                      approval_hr is_vacation
tc_names = \
    { 'Nursing-leave'         : (True,  False)
    , 'Special-leave'         : (True,  False)
    , 'Special-leave-Italy'   : (True,  False)
    , 'Special-leave-Japan'   : (True,  False)
    , 'Special-leave-Romania' : (True,  False)
    , 'Unpaid-leave'          : (True,  False)
    , 'Vacation'              : (False, True)
    , 'Comp\\Flexi-Time'      : (False, False)
    }

for n, (hr, v) in tc_names.iteritems () :
    tp = db.time_project.lookup (n)
    db.time_project.set \
        (tp, approval_required = True, approval_hr = hr, is_vacation = v)

vstatus = \
    { 'open'             : 1
    , 'submitted'        : 2
    , 'accepted'         : 3
    , 'declined'         : 4
    , 'cancel requested' : 5
    , 'cancelled'        : 6
    }
transitions = \
    { 'open'             : ['submitted', 'cancelled']
    , 'submitted'        : ['open', 'accepted', 'declined']
    , 'accepted'         : ['cancel requested']
    , 'cancel requested' : ['accepted', 'cancelled']
    }
for k, v in sorted (vstatus.iteritems (), key = lambda x : x [1]) :
    try :
        val = db.leave_status.lookup (k)
    except KeyError :
        db.leave_status.create (name = k, order = v)
for k, t in transitions.iteritems () :
    id = db.leave_status.lookup (k)
    tr = [db.leave_status.lookup (x) for x in t]
    db.leave_status.set (id, transitions = tr)

for p in db.time_project.getnodeids (retired = False) :
    tp = db.time_project.getnode (p)
    d  = {}
    if not tp.is_vacation :
        d ['is_vacation'] = False
    if not tp.approval_required :
        d ['approval_required'] = False
    if not tp.approval_hr :
        d ['approval_hr'] = False
    # Don't try to set something when cost_center is empty
    # this would throw a reject
    if not tp.cost_center :
        d = None
    if d :
        db.time_project.set (p, ** d)
try :
    db.daily_record_status.lookup ('leave')
except KeyError :
    db.daily_record_status.create \
        (name = 'leave', description = "Accepted leave")

s2014 = date.Date ('2014-01-01')
for u in db.user.getnodeids (retired = False) :
    user = db.user.getnode (u)
    dyn  = user_dynamic.act_or_latest_user_dynamic (db, u)
    while dyn and (not dyn.valid_to or dyn.valid_to >= s2014) :
        if dyn.vacation_yearly :
            if dyn.vacation_day is None or dyn.vacation_month is None :
                db.user_dynamic.set \
                    (dyn.id, vacation_month = 1, vacation_day = 1)
        dyn = user_dynamic.prev_user_dynamic (db, dyn)

for wpid in db.time_wp.getnodeids (retired = False) :
    # Reactor will update is_public to the correct value
    db.time_wp.set (wpid, is_public = False)

broken_int = dict.fromkeys \
    (('2.56'
    ,
    ))
if len (sys.argv) == 2 :
    fd = open (sys.argv [1], 'r')
    cr = csv.reader (fd, delimiter = ';')
    dt = common.pretty_range (s2014, s2014)
    for line in cr :
        if line [0] == 'Username' :
            continue
        username = line [0].strip ().lower ()
        try :
            user = db.user.lookup (username)
        except KeyError :
            # Special hacks for my data, without disclosing usernames
            if username.startswith ('l') :
                username = 'L' + username [1:]
            else :
                username = 'g' + username
            user = db.user.lookup (username)
        rounded = line [5]
        exact   = float (line [9])
        if rounded not in broken_int :
            assert int (rounded) == float (rounded)
            assert ceil (exact) == int (rounded)
        vc = db.vacation_correction.filter \
            (None, dict (user = user, date = dt, absolute = True))
        if not vc :
            db.vacation_correction.create \
                (absolute = True, date = s2014, user = user, days = exact)
        dyn = user_dynamic.get_user_dynamic (db, user, s2014)
        if not dyn :
            dyn = user_dynamic.find_user_dynamic (db, user, s2014)
        while dyn :
            d = {}
            if dyn.vacation_yearly is None :
                d ['vacation_yearly'] = 25
            if dyn.vacation_day is None or dyn.vacation_month is None :
                d ['vacation_day']   = 1
                d ['vacation_month'] = 1
            if d :
                assert 'vacation_yearly' in d
                print "WARN: dyn %s/%s had no vacation_yearly" \
                    % (username, dyn.valid_from.pretty (common.ymd))
                db.user_dynamic.set (dyn.id, ** d)
            dyn = user_dynamic.next_user_dynamic (db, dyn)

db.commit()
