#!/usr/bin/python3

import os
from roundup import instance

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

olo_list = dict \
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
    )

user_by_olo = dict \
    ( auto_germany =
        ('kathan@ds1.internal', 'mike@ds1.internal', 'mauri@ds1.internal')
    , auto_austria =
        ('croman@ds1.internal', 'mmarjanovic@ds1.internal'
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
    )

for ogroup in user_by_olo:
    for uname in user_by_olo [ogroup]:
        try:
            uid = db.user.lookup (uname)
        except KeyError as msg:
            print ("Warning: %s" % msg)
            continue
        ops = db.o_permission.filter (None, dict (user = uid))
        assert len (ops) <= 1
        if ops:
            continue
        oids = []
        for oloname in olo_list [ogroup]:
            try:
                oids.append (db.org_location.lookup (oloname))
            except KeyError as msg:
                print ("Warning: %s" % msg)
                continue
        db.o_permission.create (user = uid, org_location = oids)
db.commit ()

