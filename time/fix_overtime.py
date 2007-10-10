#!/usr/bin/python2.4
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = '/roundup/tracker/xyzzy'
tracker = instance.open (dir)
db      = tracker.open ('admin')
sys.path.insert (1, os.path.join (dir, 'lib'))
from common       import overtime_period_week
from user_dynamic import get_user_dynamic

try :
    db.overtime_period.lookup ("week")
except KeyError :
    db.overtime_period.create \
        (name = "week", months = 0, weekly = True, order = 0)

month = db.overtime_period.lookup ('month')
db.overtime_period.set (month, months = 1,  weekly = False)
year  = db.overtime_period.lookup ('year')
db.overtime_period.set (year,  months = 12, weekly = False)

# fix dynuser records to use weekly if nothing is specified and a value
# for weekly_hours and supplementary hours is given
otw = overtime_period_week (db)
for id in db.user_dynamic.getnodeids () :
    dyn = db.user_dynamic.getnode (id)
    if not dyn.overtime_period and dyn.weekly_hours and dyn.supp_weekly_hours :
        db.user_dynamic.set (id, overtime_period = otw.id)

# find first freeze records for all users and fix them to have a
# month_validity_date and a value for achieved.
for uid in db.user.getnodeids () :
    fids = db.daily_record_freeze.filter \
        ( None
        , dict (user = uid, frozen = True)
        , group = ('+', 'date')
        )
    if not fids :
        continue
    freeze = db.daily_record_freeze.getnode (fids [0])
    if not freeze.month_validity_date :
	db.daily_record_freeze.set \
	    (freeze.id, month_validity_date = freeze.date)
    if freeze.achieved_hours is None :
	db.daily_record_freeze.set \
	    (freeze.id, achieved_hours = 0)

# fix month_validity_date for the rest which do not have a yearly
# setting
yearly = db.overtime_period.lookup ('year')
for id in db.daily_record_freeze.getnodeids (retired = False) :
    f = db.daily_record_freeze.getnode (id)
    if not f.frozen or f.month_validity_date :
        continue
    dyn = get_user_dynamic (db, f.user, f.date)
    if dyn.overtime_period == yearly :
        continue
    db.daily_record_freeze.set (id, month_validity_date = f.date)

def refreeze (freezelist) :
    d = date.Date ('2005-12-31')
    for f in reversed (freezelist) :
	if f.date != d :
	    db.daily_record_freeze.set (f.id, frozen = False)
    for f in freezelist :
	if f.date != d :
	    db.daily_record_freeze.set (f.id, frozen = True)

# Loop over all freeze recs and thaw them, except for records on 2005-12-31,
# then re-freeze them.
ids = db.daily_record_freeze.filter \
    (None, dict (frozen = True), group = [('+', 'user'), ('+', 'date')])
u   = None
l   = []
for id in ids :
    f = db.daily_record_freeze.getnode (id)
    if f.user != u :
	refreeze (l)
	u = f.user
	l = []
    l.append (f)
refreeze (l)

db.commit ()
