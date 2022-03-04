#!/usr/bin/python
import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for id in db.time_project.getnodeids (retired = False) :
    tp = db.time_project.getnode (id)
    if tp.nosy :
        db.time_project.set (id, nosy = None)
        print ('time_project%s' % id)

db.commit()
