#!/usr/bin/python3

import os
from roundup import instance

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

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
        ( 'TTTech Chip IP Design GmbH; AUT, Wien'
        , 'TTTech Computertechnik AG; AUT, Wien'
        , 'TTTech Computertechnik AG, organizacní složka; CZE, Brno'
        , 'TTTech Deutschland GmbH; DEU, München'
        , 'TTTech Development Romania SRL; ROU, Bucharest'
        , 'TTTech Digital Solutions GmbH; AUT, Wien'
        , 'TTTech Flexibilis Oy; FIN, Tampere'
        , 'TTTech Industrial Automation AG; AUT, Wien'
        , 'TTTech Innovation Campus Brixen S.r.l.; ITA, Brixen'
        , 'TTTech Japan Corp.; JPN, Nagoya'
        , 'TTTech Japan Expat AUT; JPN, Nagoya'
        , 'TTTECH NORTH AMERICA, INC.; USA, Andover, MA'
        , 'TTTECH NORTH AMERICA, INC.; USA, Houston, TX'
        , 'TTTECH NORTH AMERICA, INC.; USA, Santa Clara, CA'
        , 'TTControl GmbH; AUT, Wien'
        , 'TTControl S.r.l.; ITA, Brixen'
        , 'TTech Industrial North America Inc.; USA, Milpitas,CA'
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
        ('mmarjanovic@ds1.internal', 'chen@ds1.internal')
    , auto_korea =
        ( 'mmarjanovic@ds1.internal', 'croman@ds1.internal'
        , 'haller@ds1.internal', 'mauri@ds1.internal'
        )
    , tcag =
        ( 'atischler@ds1.internal', 'reisner@ds1.internal'
        , 'koehldorfer@ds1.internal', 'kusej@ds1.internal'
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

for uid in by_uid:
    oids = db.o_permission.filter (None, dict (user = uid))
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
db.commit ()
