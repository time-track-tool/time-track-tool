#!/usr/bin/python


import sys, os
from roundup           import date
from roundup           import instance
tracker = sys.argv [1]
sys.path.insert (1, os.path.join (tracker, 'lib'))
from common            import tt_clearance_by

tracker = instance.open (tracker)
db      = tracker.open  ('admin')

submitted = db.daily_record_status.lookup ('submitted')
drecs     = db.daily_record.find (status = submitted)
users     = {}
clearers  = {}
for dr in drecs :
    users [db.daily_record.get (dr, 'user')] = 1
for u in users :
    for c in tt_clearance_by (db, u, only_subs = True) :
        clearers [c] = 1
print clearers
