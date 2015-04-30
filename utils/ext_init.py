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

    kw = None
    try :
        kw = db.msg_keyword.lookup ('External Sync')
    except KeyError :
        pass
    if kw is None :
        db.msg_keyword.create \
            ( name        = 'External Sync'
            , description = 'Synchronize this message to external tracker'
            )

    db.commit ()
# end def main

if __name__ == '__main__' :
    main ()
