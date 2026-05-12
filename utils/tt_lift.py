#!/usr/bin/python
import sys
import os
from roundup import instance, date
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')
sys.path.insert (1, 'lib')

import vacation
import user_dynamic

countries = set (('Austria', 'Germany', 'Finland', 'Czechia', 'Romania'))

for id in db.vac_aliq.getnodeids (retired = False):
    va = db.vac_aliq.getnode (id)
    if va.name == 'Daily':
        db.vac_aliq.set (id, name = 'Austria')
        countries.remove ('Austria')
        continue
    elif va.name == 'Monthly':
        db.vac_aliq.set (id, name = 'Germany')
        countries.remove ('Germany')
        continue
    elif va.name in countries:
        countries.remove (va.name)
        continue
    else:
        print (va.name)
        assert 0
# Create remaining countries
for c in sorted (countries):
    db.vac_aliq.create (name = c)

# Permission for a user
user  = db.user.getnode ('304')
roles = user.roles
if roles:
    roles = set (x.strip () for x in user.roles.split (',') if x)
else:
    roles = set (('user', 'nosy'))
update_roles = False
for r in ('hr-leave-approval', 'hr-vacation'):
    if r not in roles:
        roles.add (r)
        update_roles = True
if update_roles:
    db.user.set (user.id, roles = ','.join (sorted (roles)))


# Unfreeze existing users until jan
# First find dyn users for org_location

dynids = db.user_dynamic.filter (None, dict (org_location = '34'))
users = set ()
for id in dynids:
    dyn = db.user_dynamic.getnode (id)
    users.add (dyn.user)
srt = [('+', 'user'), ('-', 'date')]
freeze = db.daily_record_freeze.filter \
    (None, dict (user = list (users)), sort = srt)

cutoff = date.Date ('2026-01-01')
for f in freeze:
    frz = db.daily_record_freeze.getnode (f)
    if frz.date > cutoff and frz.frozen:
        db.daily_record_freeze.set (f, frozen = False)

# Enable do_leave_process in relevant org_location(s)
va = { '34': db.vac_aliq.lookup ('Romania') }
for id in ('34',):
    olo = db.org_location.getnode (id)
    d   = {}
    if not olo.do_leave_process:
        d.update (do_leave_process = True)
    if not olo.vac_aliq:
        d.update (vac_aliq = va [id])
    if d:
        db.org_location.set (id, **d)

# Vacation and vac correction per user:
# User vac/year vac_corr '26
user_v = \
    [ ( '918', 25,  5) #
    , ( '181', 25,  8) #
    , ('2256', 25,  3) #
    , ( '192', 25, 38) #
    , ('1466', 25,  3) #
    , ( '365', 25,  1) #
    , ( '304', 25,  2) #
    , ( '432', 25, -1) #
    , ('3048', 24,  9) #
    , ( '179', 25,  0) #
    , ('6737', 21,  0) #
    , ( '290', 25, -2) #
    ]
for u, vac, corr in user_v:
    # Get dyn user on jan 2026
    dt = date.Date ('2026-01-01')
    dyn = user_dynamic.get_user_dynamic (db, u, date = dt)
    if not dyn:
        print ('No dyn user for user%s' % u)
        continue
    while dyn:
        if dyn.vacation_yearly != vac:
            print ( 'user_dynamic%s user%s vacation %s->%s'
                  % (dyn.id, u, dyn.vacation_yearly, vac)
                  )
        db.user_dynamic.set (dyn.id, vacation_yearly = vac)
        dyn = user_dynamic.next_user_dynamic (db, dyn)
    # Vacation correction on jan 1 2026
    vc = vacation.get_vacation_correction (db, u)
    if vc:
        assert vc.days == corr
    else:
        db.vacation_correction.create \
            ( user     = u
            , date     = dt
            , absolute = True
            , days     = corr
            )

db.commit()
