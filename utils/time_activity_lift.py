#!/usr/bin/python
from __future__ import print_function
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

# Do *not* create the on-call duty permission:
#try :
#    tap = db.time_activity_perm.lookup ('on-call duty')
#except KeyError :
#    tap = db.time_activity_perm.create \
#        ( name        = 'on-call duty'
#        , description = 'Allowed to book on on-call duty'
#        )
#act = db.time_activity.getnode ('24')
#assert 'on-call' in act.name
#
#if not act.time_activity_perm :
#    db.time_activity.set (act.id, time_activity_perm = tap)

for id in '10', '11', '24' :
    if db.time_activity.get (id, 'is_valid') is None :
        db.time_activity.set (id, is_valid = True)

db.commit()
