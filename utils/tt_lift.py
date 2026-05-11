#!/usr/bin/python
import sys
import os
from roundup import instance, date
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

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

db.commit()
