#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import sys
from roundup           import instance
tracker = instance.open (os.getcwd ())
db      = tracker.open ('admin')
sys.path.insert (0, 'lib')
import common

# Add 'Nosy' role to all active users

valid = db.user_status.lookup ('valid')

for u in db.user.getnodeids (retired = False) :
    if db.user.get (u, 'status') != valid :
        continue
    if not common.user_has_role (db, u, 'Nosy') :
        r = db.user.get (u, 'roles')
        if r :
            r = r + ',Nosy'
        else :
            r = 'Nosy'
        db.user.set (u, roles = r)

db.commit ()
