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

for u in db.user.getnodeids () :
    lop = None
    dyn = first_user_dynamic (db, u)
    while dyn :
        lop = dyn.overtime_period
        dyn = next_user_dynamic (db, dyn)
        if lop and dyn and dyn.overtime_period is None :
            u = db.user.get (dyn.user, 'username')
            d1 = dyn.valid_from.pretty ('%Y-%m-%d')
            d2 = ''
            if dyn.valid_to :
                d2 = dyn.valid_to.pretty ('%Y-%m-%d')
            print 'user_dynamic%s change: %s %s-%10s' \
                % (ud, u, d1, d2)
