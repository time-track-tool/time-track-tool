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
import common

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
for r in ('hr-leave-approval', 'hr-vacation', 'hr'):
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
# A list of first-day/last-day vacation
('2026-xx-xx', '2026-xx-xx')
vac_by_user = \
    {  '179': [('2026-06-16', '2026-06-19'), ('2026-08-17', '2026-08-21')
              ,('2026-09-07', '2026-09-18'), ('2026-12-21', '2026-12-30')]
    ,  '181': [('2026-08-03', '2026-08-28'), ('2026-12-28', '2027-01-08')]
    ,  '192': []
#    ,  '192': [('2026-06-23', '2026-06-25'), ('2026-07-01', '2026-07-17')
#              ,('2026-07-30', '2026-07-30'), ('2026-08-30', '2026-08-30')
#              ]
    ,  '290': [('2026-07-28', '2026-08-07'), ('2026-08-31', '2026-09-11')
              ,('2026-12-28', '2026-12-30')]
    ,  '304': []
#    ,  '304': [('2026-06-22', '2026-06-26'), ('2026-07-06', '2026-07-13')
#              ,('2026-08-03', '2026-08-12'), ('2026-12-28', '2026-12-30')]
    ,  '365': [('2026-06-18', '2026-06-19'), ('2026-07-27', '2026-08-07')
              ,('2026-09-09', '2026-09-16'), ('2026-12-21', '2026-12-30')]
    ,  '432': []
#    ,  '432': [('2026-06-22', '2026-06-22'), ('2026-07-27', '2026-07-27')
#              ,('2026-08-10', '2026-08-10'), ('2026-08-17', '2026-08-17')
#              ,('2026-09-03', '2026-09-17'), ('2026-10-19', '2026-10-19')
#              ,('2026-11-16', '2026-11-16'), ('2026-12-23', '2026-12-23')
#              ,('2026-12-29', '2026-12-30')]
    ,  '918': [('2026-06-29', '2026-07-10'), ('2026-12-21', '2026-12-30')
              ,('2027-01-04', '2027-01-05')]
    , '1466': [('2026-06-22', '2026-06-26'), ('2026-07-03', '2026-07-03')
              ,('2026-07-10', '2026-07-10'), ('2026-07-17', '2026-07-17')
              ,('2026-07-24', '2026-07-24'), ('2026-07-31', '2026-07-31')
              ,('2026-08-07', '2026-08-07'), ('2026-08-14', '2026-08-14')
              ,('2026-08-21', '2026-08-21'), ('2026-08-28', '2026-08-28')
              ,('2026-12-21', '2026-12-30')]
    , '2256': [('2026-08-24', '2026-08-31'), ('2026-12-28', '2026-12-30')]
#    , '3048': [('2026-12-23', '2026-12-23'), ('2026-12-29', '2026-12-30')]
    , '3048': []
    , '6737': [('2026-08-21', '2026-08-28'), ('2026-09-02', '2026-09-04')
              ,('2026-12-21', '2026-12-30')]
    }
dt_jan = date.Date ('2026-01-01')
va = db.vac_aliq.lookup ('Romania')
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
        if dyn.vac_aliq != va:
            d.update (vac_aliq = va)
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
    # Find time recs <= 2026-05-31 with time_project1429 (vacation subsi)
    d = {}
    d ['daily_record.user'] = u
    d ['daily_record.date'] = '2026-01-01;2026-05-31'
    d ['wp.project']        = '1429'
    trids = db.time_record.filter (None, d)
    d  = dict (bookers = u, project = '6', time_end = '-')
    wp = db.time_wp.filter (None, d)
    assert len (wp) <= 1
    if len (wp) == 0:
        continue
    vac_wp = wp [0]
    dyn = user_dynamic.get_user_dynamic (db, u, date = dt_jan)
    for trid in trids:
        tr   = db.time_record.getnode (trid)
        dr   = db.daily_record.getnode (tr.daily_record)
        wday = common.week_day (dr.date)
        wdn  = common.wday_name (wday)
        exp  = getattr (dyn, 'hours_%s' % wdn)
        assert tr.duration in (exp, exp / 2)
        db.time_record.set (trid, wp = vac_wp)
    # Find time_recs >= 2026-06-01 with time_project1429 (vacation subsi)
    # Delete those, we'll then create the respective vacation
    d = {}
    d ['daily_record.user'] = u
    d ['daily_record.date'] = '2026-06-01;'
    d ['wp.project']        = '1429'
    trids = db.time_record.filter (None, d)
    for trid in trids:
        tr = db.time_record.getnode (trid)
        dr = db.daily_record.getnode (tr.daily_record)
        if dr.status != '1':
            db.daily_record.set (dr.id, status = '1')
        db.time_record.retire (trid)
    # Create leave requests
    for fd, ld in vac_by_user [u]:
        ls = db.leave_submission.filter (None, dict (user = u, first_day = fd))
        if ls:
            assert len (ls) == 1
            ls = db.leave_submission.getnode (ls [0])
            assert ls.time_wp  == vac_wp
            assert ls.last_day == date.Date (ld)
        else:
            # First set daily records to open
            d   = dict (user = u, date = '%s;%s' % (fd, ld), status = '2')
            drs = db.daily_record.filter (None, d)
            for drid in drs:
                db.daily_record.set (drid, status = '1')
            print ('Create leave for user%s %s-%s' % (u, fd, ld))
            db.leave_submission.create \
                ( user      = u
                , first_day = date.Date (fd)
                , last_day  = date.Date (ld)
                , time_wp   = vac_wp
                )

db.commit()
