#!/usr/bin/python3

import sys
import os
from roundup import instance

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')
sys.path.insert (1, 'lib')
from common import user_has_role

olo_groups = dict \
    ( auto_germany =
        ( 'TTTech Auto Germany GmbH; DEU, Ingolstadt, Bayern'
        , 'TTTech Auto Germany GmbH; DEU, München, Bayern'
        , 'TTTech Auto Germany GmbH; DEU, Wolfsburg, Niedersachsen'
        )
    , auto_austria =
        ( 'TTTech Auto AG; AUT, Salzburg'
        , 'TTTech Auto AG; AUT, Wien'
        )
    , auto_china =
        ( 'TTTech Auto China Co., Ltd.; CHN, Beijing'
        , 'TTTech Auto China Co., Ltd.; CHN, Shanghai'
        )
    , auto_korea =
        ( 'TTTech Auto AG Branch Office Korea; KOR, Seoul'
        ,
        )
    , tcag =
        ( 'CLOVER d.o.o. Banja Luka; BIH, Banja Luka'
        , 'FTN-IRAM-RT DOO NOVI SAD; SRB, Novi Sad'
        , 'INSTITUT "RT-RK" DOO Banja Luka; BIH, Banja Luka'
        , 'INSTITUT "RT-RK" DOO Banja Luka; SRB, Novi Sad'
        , 'iWedia doo Novi Sad; SRB, Novi Sad'
        , 'iWedia SA; CHE, Lausanne'
        , 'OBLO LIVING doo Novi Sad; SRB, Belgrade'
        , 'OBLO LIVING doo Novi Sad; SRB, Novi Sad'
        , 'RT-RK DOO NOVI SAD; BIH, Banja Luka'
        , 'RT-RK DOO NOVI SAD; SRB, Belgrade'
        , 'RT-RK DOO NOVI SAD; SRB, Novi Sad'
        , 'TTControl GmbH; AUT, Wien'
        , 'TTControl S.r.l.; ITA, Brixen'
        , 'TTTech Chip IP Design GmbH; AUT, Wien'
        , 'TTTech Computertechnik AG; AUT, Wien'
        , 'TTTech Computertechnik AG, organizacní složka; CZE, Brno'
        , 'TTTech Deutschland GmbH; DEU, München'
        , 'TTTech Development Romania SRL; ROU, Bucharest'
        , 'TTTech Digital Solutions GmbH; AUT, Wien'
        , 'TTTech Flexibilis Oy; FIN, Tampere'
        , 'TTTech Industrial Automation AG; AUT, Wien'
        , 'TTTech Industrial North America Inc.; USA, Milpitas,CA'
        , 'TTTech Innovation Campus Brixen S.r.l.; ITA, Brixen'
        , 'TTTech Japan Corp.; JPN, Nagoya'
        , 'TTTech Japan Expat AUT; JPN, Nagoya'
        , 'TTTECH NORTH AMERICA, INC.; USA, Andover, MA'
        , 'TTTECH NORTH AMERICA, INC.; USA, Houston, TX'
        , 'TTTECH NORTH AMERICA, INC.; USA, Santa Clara, CA'
        , 'TTTech Nexus GmbH; AUT, Wien'
        )
    )

user_by_olo = dict \
    ( auto_germany =
        ('kathan@ds1.internal', 'mike@ds1.internal', 'mauri@ds1.internal')
    , auto_austria =
        ( 'croman@ds1.internal', 'mmarjanovic@ds1.internal'
        , 'haller@ds1.internal', 'mgrundner@ds1.internal'
        , 'wolff@ds1.internal', 'mauri@ds1.internal', 'chiu@ds1.internal'
        , 'zwainz@ds1.internal'
        )
    , auto_china =
        ( 'mmarjanovic@ds1.internal', 'chen@ds1.internal'
        , 'croman@ds1.internal', 'haller@ds1.internal'
        , 'chxu@ds1.internal'
        )
    , auto_korea =
        ( 'mmarjanovic@ds1.internal', 'croman@ds1.internal'
        , 'haller@ds1.internal', 'mauri@ds1.internal'
        )
    , tcag =
        ( 'kusej@ds1.internal',        'auner@ds1.internal'
        , 'aroman@ds1.internal',       'reisner@ds1.internal'
        , 'gallioth@ds1.internal',     'atischler@ds1.internal'
        , 'kargl@ds1.internal',        'koehldorfer@ds1.internal'
        , 'scherer@ds1.internal',      'punkenhofer@ds1.internal'
        , 'risse@ds1.internal',        'machian@ds1.internal'
        , 'ebaumgartner@ds1.internal', 'bindreiter@ds1.internal'
        , 'julcher@ds1.internal',      'bstoeger@ds1.internal'
        )
    )

by_uid  = {}
ogroups = {}
for ogroup in user_by_olo:
    ogroups [ogroup] = []
    for oloname in olo_groups [ogroup]:
        try:
            id = db.org_location.lookup (oloname)
            ogroups [ogroup].append (id)
        except KeyError as msg:
            print ("Warning: %s" % msg)

    for uname in user_by_olo [ogroup]:
        try:
            uid = db.user.lookup (uname)
            if uid not in by_uid:
                by_uid [uid] = []
        except KeyError as msg:
            print ("Warning: %s" % msg)
            continue
        by_uid [uid].extend (ogroups [ogroup])

# Users in only one OLO:
user_olo = [('187', '3'), ('304', '34'), ('5615', '23')]
for uid, olo in user_olo:
    try:
        nd = db.user.getnode (uid)
        un = nd.username
    except IndexError:
        continue
    assert uid not in by_uid
    by_uid [uid] = [olo]

for uid in by_uid:
    oids = db.o_permission.filter (None, dict (user = uid))
    if len (oids) > 1:
        import pdb; pdb.set_trace ()
    assert len (oids) <= 1
    old_olo = set ()
    if oids:
        oid     = oids [0]
        operm   = db.o_permission.getnode (oid)
        old_olo = set (operm.org_location)
    new_olo = by_uid [uid]
    if set (new_olo) != old_olo:
        if old_olo:
            assert operm.user == uid
            db.o_permission.set (oid, org_location = new_olo)
        else:
            db.o_permission.create (user = uid, org_location = new_olo)

# WP fixes
oloids_ = (7, 3, 10, 1, 23, 51, 34, 80, 30, 41, 75, 76, 26, 83, 20, 68, 67, 84)
oloids  = []
for oid in oloids_:
    try:
        olo = db.org_location.getnode (str (oid))
        name = olo.name
    except (KeyError, IndexError) as err:
        print ('Warning: %s' % err)
        continue
    oloids.append (olo.id)
print ("OLO-IDS: %s" % ','.join (oloids))
for wpid in (125, 55693, 4646, 4645, 144):
    try:
        db.time_wp.set \
            (wpid, bookers = [], allowed_olo = oloids, is_public = True)
    except IndexError as err:
        print ('Warning: %s' % err)
print ("Setting TTTech Computertechnik Aux Org/Location for some users")
for dynid, uid in (('15952', '3295'), ('15247', '5548')):
    try:
        dyn = db.user_dynamic.getnode (dynid)
        assert dyn.user == uid
    except IndexError:
        continue
    db.user_dynamic.set (dynid, aux_org_locations = ['1'])
# Add role 'hr-leave-approval' for these users if not present:
hr_leave_users = \
    [ '2548', '34', '5781', '6228', '1434', '711', '2863', '4931'
    , '2861', '1307', '4750'
    ]
for uid in hr_leave_users:
    try:
        if user_has_role (db, uid, 'hr-leave-approval'):
            continue
    except IndexError as err:
        print ('Warning: %s' % err)
        continue
    u = db.user.getnode (uid)
    r = u.roles
    r = r + ',hr-leave-approval'
    db.user.set (uid, roles = r)
view_roles_users = \
    [ '2548', '2851', '2198', '34', '1846', '5781', '6228', '1434', '2371'
    , '711', '304', '5615', '2863', '4931', '2861', '1307', '187', '126'
    , '4750'
    ]
for uid in view_roles_users:
    try:
        if user_has_role (db, uid, 'view-roles'):
            continue
    except IndexError as err:
        print ('Warning: %s' % err)
        continue
    u = db.user.getnode (uid)
    r = u.roles
    if not r:
        r = 'view-roles'
    else:
        r = r + ',view-roles'
    db.user.set (uid, roles = r)
db.commit ()
