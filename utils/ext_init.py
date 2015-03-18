#!/usr/bin/python

import sys, os
from roundup          import instance
from roundup.password import Password

""" Tool to initialize database for use of an external tracker.
    Only relevant for testing external sync.
"""

def main () :
    tracker = instance.open (os.getcwd ())
    db      = tracker.open ('admin')
    et      = None
    try :
        et = db.ext_tracker.lookup ('KPM')
    except KeyError :
        pass
    if not et :
        et = db.ext_tracker.create \
            ( name        = 'KPM'
            , description = 'VW/Audi Konzern Problem Management'
            )
    db.issue.set ('74017', ext_tracker = et, ext_id = '6435580')
    db.issue.set ('74025', ext_tracker = et, ext_id = '6435335')

    eu = None
    try :
        eu = db.user.lookup ('ext_sync')
    except KeyError :
        pass
    if not eu :
        db.user.create \
            ( username = 'ext_sync'
            , nickname = 'ext sync'
            , realname = 'User for Sync of external trackers'
            , password = Password ('ChangeMe')
            , roles    = 'User'
            , address  = 'roundup-admin@tttech.com'
            )

    db.commit ()
# end def main

if __name__ == '__main__' :
    main ()
