#!/usr/bin/python

# Lifter script for new timetracking interface

from __future__ import print_function
import sys
import os
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')


wldict = dict \
    (( ('1', ('Office',          10))
     , ('8', ('Home-AT',         20))
     , ('2', ('Mobile',          30))
     , ('5', ('Off',             40))
     , ('6', ('Cust./on-site',   50))
     , ('3', ('Off-site/trav.',  60))
    ))

for id in db.work_location.getnodeids (retired = False) :
    wl = db.work_location.getnode (id)
    d = {}
    if id in wldict :
        code, order = wldict [id]
        if not wl.is_valid :
            d ['is_valid'] = True
        if wl.order is None :
            d ['order'] = order
        if wl.code != code :
            d ['code'] = code
        if id == '3' and not wl.travel :
            d ['travel'] = True
        if id == '5' and not wl.durations_allowed :
            d ['durations_allowed'] = True
        if id == '5' and not wl.is_off :
            d ['is_off'] = True
        if d :
            db.work_location.set (id, **d)
db.commit()
