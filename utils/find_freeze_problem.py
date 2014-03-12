#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()
sys.path.insert (0, os.path.join (dir, 'lib'))
from user_dynamic import first_user_dynamic, next_user_dynamic, compute_balance
from common       import start_of_period, end_of_period, day
tracker = instance.open (dir)
db      = tracker.open ('admin')
ymd     = '%Y-%m-%d'

for u in db.user.getnodeids () :
    lop  = None
    dyn  = first_user_dynamic (db, u)
    while dyn :
        lop  = dyn.overtime_period
        dt   = dyn.valid_to
        dyn  = next_user_dynamic (db, dyn)
        if not dt and dyn :
            dt = dyn.valid_from
        if lop and dyn and dyn.overtime_period is None :
            otp = db.overtime_period.getnode (lop)
            eop = end_of_period   (dt - day, otp)
            sop = start_of_period (dt - day, otp)
            is_eop = eop == dt - day
            un = db.user.get (dyn.user, 'username')
            d1 = dyn.valid_from.pretty ('%Y-%m-%d')
            d2 = ''
            if dyn.valid_to :
                d2 = dyn.valid_to.pretty ('%Y-%m-%d')
            b1, bla = compute_balance (db, u, sop - day, sharp_end = True)
            b2, bla = compute_balance (db, u, dt  - day, sharp_end = True)
            if not is_eop :
                print 'user_dynamic%-4s: %11s %s-%10s %s-%s %6.2f' % \
                    ( dyn.id
                    , un
                    , d1
                    , d2
                    , sop.pretty (ymd)
                    , (dt-day).pretty (ymd)
                    , b2 - b1
                    )
