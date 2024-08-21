#!/usr/bin/python3
import sys
import os
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

sys.path.insert (1, os.path.join (dir, 'lib'))
import common

obsolete = \
    {'procurement', 'pr-view', 'procure-approval', 'measurement-approval'}

changed = False
for uid in db.user.getnodeids (retired = False):
    u  = db.user.getnode (uid)
    rl = common.role_list (u.roles)
    if obsolete.intersection (rl):
        roles = ','.join (r for r in rl if r not in obsolete)
        db.user.set (uid, roles = roles)
        print ('Fixed roles for "%s"' % u.username)
        changed = True
if changed:
    db.commit ()
