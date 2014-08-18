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

tc_names = \
    { 'Nursing-leave'         : True
    , 'Special-leave'         : True
    , 'Special-leave-Italy'   : True
    , 'Special-leave-Japan'   : True
    , 'Special-leave-Romania' : True
    , 'Unpaid-leave'          : True
    , 'Vacation'              : False
    , 'Comp\\Flexi-Time'      : False
    }

for n, req in tc_names.iteritems () :
    tp = db.time_project.lookup (n)
    db.time_project.set (tp, approval_required = True, approval_hr = req)

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
        val = db.vacation_status.lookup (k)
    except KeyError :
        db.vacation_status.create (name = k, order = v)
for k, t in transitions.iteritems () :
    id = db.vacation_status.lookup (k)
    tr = [db.vacation_status.lookup (x) for x in t]
    db.vacation_status.set (id, transitions = tr)

db.commit()
