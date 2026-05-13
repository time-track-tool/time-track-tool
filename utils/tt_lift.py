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
    if not olo.vacation_legal_year:
        d.update (vacation_legal_year = True)
    if not olo.vac_aliq:
        d.update (vac_aliq = va [id])
    if d:
        db.org_location.set (id, **d)

# Intermediate commit
db.commit ()

# Disable old and create new auto wps for vacation, special leave, flexi-time
a_vac = db.auto_wp.filter \
    (None, dict (org_location = '34', time_project = '1429', is_valid = True))
for a in a_vac:
    db.auto_wp.set (a, is_valid = False)
a_vac = db.auto_wp.filter (None, dict (org_location = '34', time_project = '6'))
if not a_vac:
    db.auto_wp.create \
        ( org_location      = '34'
        , time_project      = '6'
        , name              = 'Vacation Romania'
        , is_valid          = True
        , durations_allowed = True
        , all_in            = True
        )
    db.auto_wp.create \
        ( org_location      = '34'
        , time_project      = '6'
        , name              = 'Vacation Romania'
        , is_valid          = True
        , durations_allowed = True
        , all_in            = True
        , contract_type     = '3'
        )
a_sp = db.auto_wp.filter \
    (None, dict (org_location = '34', time_project = '1450', is_valid = True))
for a in a_sp:
    db.auto_wp.set (a, is_valid = False)
a_sp = db.auto_wp.filter (None, dict (org_location = '34', time_project = '7'))
if not a_sp:
    a_sp = db.auto_wp.create \
        ( org_location      = '34'
        , time_project      = '7'
        , name              = 'Special Leave Romania'
        , is_valid          = True
        , durations_allowed = True
        , all_in            = True
        )
    a_sp = db.auto_wp.create \
        ( org_location      = '34'
        , time_project      = '7'
        , name              = 'Special Leave Romania'
        , is_valid          = True
        , durations_allowed = True
        , all_in            = True
        , contract_type     = '3'
        )
a_fl = db.auto_wp.filter \
    (None, dict (org_location = '34', time_project = '1430', is_valid = True))
for a in a_fl:
    db.auto_wp.set (a, is_valid = False)
a_fl = db.auto_wp.filter (None, dict (org_location = '34', time_project = '1'))
if not a_fl:
    a_fl = db.auto_wp.create \
        ( org_location      = '34'
        , time_project      = '1'
        , name              = 'Flexi-Time Romania'
        , is_valid          = True
        , durations_allowed = True
        , all_in            = True
        )
    a_fl = db.auto_wp.create \
        ( org_location      = '34'
        , time_project      = '1'
        , name              = 'Flexi-Time Romania'
        , is_valid          = True
        , durations_allowed = True
        , all_in            = True
        , contract_type     = '3'
        )

# Vacation and vac correction per user:
# User vac/year vac_corr '26
user_v = \
    [ ( '179', 25,  0) #
    , ( '181', 25,  8) #
    , ( '192', 25, 38) #
    , ( '290', 25, -2) #
    , ( '304', 25,  2) #
    , ( '365', 25,  1) #
    , ( '432', 25, -1) #
    , ( '918', 25,  5) #
    , ('1466', 25,  3) #
    , ('2256', 25,  3) #
    , ('3048', 24,  9) #
    , ('6737', 21,  0) #
    ]
dt_jan = date.Date ('2026-01-01')
for u, vac, corr in user_v:
    first = True
    # Get dyn user on jan 2026
    dyn = user_dynamic.get_user_dynamic (db, u, date = dt_jan)
    if not dyn:
        print ('No dyn user for user%s' % u)
        continue
    # Create new dyn user starting january if necessary
    if first and dyn.valid_from < dt_jan:
        f = set (('id', 'creation', 'creator', 'activity', 'actor'))
        d = dict ((k, dyn [k]) for k in dyn.keys () if k not in f)
        d.update (valid_from = dt_jan)
        id = db.user_dynamic.create (**d)
        dyn = db.user_dynamic.getnode (id)
        first = False
    while dyn:
        d = {}
        if dyn.vacation_yearly != vac:
            print ( 'user_dynamic%s user%s vacation %s->%s'
                  % (dyn.id, u, dyn.vacation_yearly, vac)
                  )
            d.update (vacation_yearly = vac)
        if dyn.vacation_day != 1:
            d.update (vacation_day = 1)
#        if dyn.vacation_month != 1:
#            d.update (vacation_month = 1)
        if d:
            db.user_dynamic.set (dyn.id, **d)
        dyn = user_dynamic.next_user_dynamic (db, dyn)
        first = False
    # Vacation correction on jan 1 2026
    vc = vacation.get_vacation_correction (db, u)
    if vc:
        assert vc.days == corr
    else:
        db.vacation_correction.create \
            ( user     = u
            , date     = dt_jan
            , absolute = True
            , days     = corr
            )

db.commit()
