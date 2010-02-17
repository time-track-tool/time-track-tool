#!/usr/bin/python2.4
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()
sys.path.insert (0, os.path.join (dir, 'lib'))
from user_dynamic import update_tr_duration
tracker = instance.open (dir)
db      = tracker.open ('admin')

db.time_record.set (179475, duration = 7)
db.time_record.set (179475, duration = 8)
db.commit ()

db.clearCache ()
assert (db.daily_record.get (125328, 'tr_duration_ok') is None)
assert (db.time_record.get (179475, 'duration') == 8)
assert (db.time_record.get (179475, 'tr_duration') is None)
db.clearCache ()

dr = db.daily_record.getnode (125328)
update_tr_duration (db, dr)
db.commit ()
db.clearCache ()
assert (db.time_record.get (179475, 'duration') == 8)
assert (db.time_record.get (179475, 'tr_duration') == 8)
assert (db.daily_record.get (125328, 'tr_duration_ok') == 8)
