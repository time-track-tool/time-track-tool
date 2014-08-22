#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

sys.path.insert (1, os.path.join (dir, 'lib'))

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
    { 'open'             : ['submitted']
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

db.commit()
