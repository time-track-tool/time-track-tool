#!/usr/bin/python
from __future__ import print_function
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for sid in db.user_status.getnodeids (retired = False) :
    us = db.user_status.getnode (sid)
    d  = {}
    if us.is_system is None :
        d ['is_system'] = ('system' in us.name)
    if us.is_internal is None :
        d ['is_internal'] = (us.name == 'valid-ad' or us.name == 'system-ad')
    if d :
        db.user_status.set (sid, **d)

db.commit()
