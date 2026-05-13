#!/usr/bin/python3
import sys
import os
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

names   = ( 'John Romiller', 'Emily Rojohnson', 'Michael Roanderson'
          , 'Sarah Rothompson', 'David Robrown'
          )
dates   = ( '2026-03-01', '2026-04-01', '2026-02-16', '2025-09-16'
          , '2025-10-01', '2025-07-16'
          )

for i, name in enumerate (names):
    # lookup
    vn, nn = name.split ()
    un  = nn.lower () 
    sup = '1434'
    try:
        uid  = db.user.lookup (un)
        user = db.user.getnode (uid)
        if not user.roles:
            db.user.set (uid, roles = 'user,nosy')
    except KeyError:
        uid = db.user.create \
            ( username  = un
            , firstname = vn
            , lastname  = nn
            , supervisor = sup
            )
    va  = db.vac_aliq.lookup ('Romania')
    olo = '34'
    # Find out if a dyn user is existing
    dynids = db.user_dynamic.filter (None, dict (user = uid))
    if dynids:
        print ('Existing dyn for username %s: %s' % (un, dynids))
        if len (dynids) == 1:
            dyn = db.user_dynamic.getnode (dynids [0])
            d = {}
            if not dyn.booking_allowed:
                d.update (booking_allowed = True)
            if dyn.vacation_day != 1:
                d.update (vacation_day = 1)
            if dyn.vacation_month != 1:
                d.update (vacation_month = 1)
            if not dyn.weekly_hours:
                d.update (weekly_hours = 40)
            if not dyn.do_auto_wp:
                d.update (do_auto_wp = True)
            if d:
                db.user_dynamic.set (dyn.id, **d)
    else:
        dyn = db.user_dynamic.create \
            ( user            = uid
            , valid_from      = date.Date (dates [i])
            , org_location    = olo
            , vacation_yearly = 25.0
            , vac_aliq        = va
            , booking_allowed = True
            , vacation_day    = 1
            , vacation_month  = 1
            , weekly_hours    = 40
            , do_auto_wp      = True
            )
    vcs = db.vacation_correction.filter (None, dict (user = dyn.user))
    if not vcs:
        vc = db.vacation_correction.create \
            ( user     = dyn.user
            , date     = dyn.valid_from
            , absolute = True
            )
    else:
        assert len (vcs) == 1
        vc = vcs [0]

db.commit()
