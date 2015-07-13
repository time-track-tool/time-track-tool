#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for wpid in db.time_wp.getnodeids (retired = False) :
    db.time_wp.set (wpid, has_expiration_date = False)
db.commit()
