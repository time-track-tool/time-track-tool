#!/usr/bin/python
from __future__ import print_function
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for sid in db.user_status.filter (None, dict (name = 'system')) :
    us = db.user_status.getnode (sid)
    if us.is_system is None :
        db.user_status.set (sid, is_system = True)

db.commit()
