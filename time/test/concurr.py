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
db1     = tracker.open ('admin')
db2     = tracker.open ('admin')

db1.time_record.set (179475, duration = 7)
db1.time_record.set (179475, duration = 8)
tr_d1 = db1.time_record.get  (179475, 'tr_duration')
dr_d1 = db1.daily_record.get (125328, 'tr_duration_ok')
db1.commit ()

dr  = db2.daily_record.getnode (125328)
dud = dr.tr_duration_ok
tr  = db2.time_record.getnode (179475)
dut = tr.tr_duration
db2.commit ()
update_tr_duration (db2, dr)
db2.commit ()

db1.time_record.set (179475, duration = 5)
db1.commit ()

db1.clearCache ()

assert (db1.daily_record.get (125328, 'tr_duration_ok') is None)
