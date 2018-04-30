#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup      import instance
from roundup.date import Date
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

# Loop over all user-dynamic records and find the ones that are
# currently valid (since start of year). Set max_flexitime for all of
# them that have all_in set.
year  = Date ('2018-01-01')
now   = Date ('.')
udids = db.user_dynamic.getnodeids (retired = False)
for udid in udids :
    dyn = db.user_dynamic.getnode (udid)
    if not dyn.all_in :
        continue
    if dyn.max_flexitime :
        continue
    if dyn.valid_to and dyn.valid_to < year :
        continue
    username = db.user.get (dyn.user, 'username')
    print ("Setting user_dynamic%s: %s %s-%s" % \
        (dyn.id, username, dyn.valid_from, dyn.valid_to))
    db.user_dynamic.set (dyn.id, max_flexitime=5)

db.commit ()
