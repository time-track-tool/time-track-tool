#!/usr/bin/python

""" Updates for global TT
"""

import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

try :
    v = db.user_status.lookup ('valid-ad')
except KeyError :
    # Rename old 'valid' user-status
    v = db.user_status.lookup ('valid')
    db.user_status.set (v, name = 'valid-ad', timetracking_allowed = True)
    v = db.user_status.create \
        ( name                 = 'valid'
        , is_nosy              = True
        , timetracking_allowed = True
        , description          = 'Valid user not synced to AD'
        , roles                = 'User,Nosy'
        )
    db.commit ()
