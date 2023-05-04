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

# Fix work locations for new time tracking interface
# Also create attendance records for existing time records.
# To be idempotent the scripts stops when encountering a time record
# with a non-empty attendence record backlink.


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

def interval (duration) :
    h = int (duration)
    m = (duration - h) * 60
    return date.Interval ('%02d:%02d' % (h, m))

do_commit = True
try:
    db.sql \
        ( 'create index _attendance_record_time_record_idx on '
          '_attendance_record (_time_record);'
        )
except Exception as err:
    print ("Index creation failed: %s" % err)
    do_commit = False
for id in db.time_record.getnodeids (retired = False) :
    if not do_commit:
        print ("Not creating attendance records, index creation failed")
        break
    tr = db.time_record.getnode (id)
    if tr.attendance_record :
        print ("Not creating attendance records, detected existing record")
        do_commit = False
        break
    d = dict \
        ( daily_record = tr.daily_record
        , time_record  = tr.id
        )
    if tr.end :
        d ['end']   = tr.end
        if tr.start :
            d ['start'] = tr.start
        else :
            print ("\nW:time_record%s: No start" % tr.id)
            if not tr.duration :
                print ("\nE:time_record%s: end but no duration/start" % tr.id)
                continue
            h = int (tr.duration)
            dt = date.Date (d ['end']) - interval (tr.duration)
            d ['start'] = dt.pretty ('%H:%M')
    elif tr.start :
        print ("\nW:time_record%s: No end" % tr.id)
        if not tr.duration :
            print ("\nE:time_record%s: end but no duration/start" % tr.id)
            continue
        dt = date.Date (d ['start']) + interval (tr.duration)
        d ['end'] = dt.pretty ('%H:%M')

    if d.get ('start') :
        if tr.start_generated :
            d ['start_generated'] = tr.start_generated
        if tr.end_generated :
            d ['end_generated'] = tr.end_generated
    if tr.work_location :
        d ['work_location'] = tr.work_location
    arid = db.attendance_record.create (**d)
    print ("created attendance_record%s" % arid, end = '\r')
    # Commit every 10000 records, otherwise this gets quadratically slower
    if int (arid) % 10000 == 0 :
        print ("\ncommit")
        db.commit ()
if do_commit :
    db.commit()
