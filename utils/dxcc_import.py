#!/usr/bin/python
import os
import sys
from roundup           import instance
from afu               import dxcc
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

continents = \
    [ ('AF', 'Africa')
    , ('AN', 'Antarctica')
    , ('AS', 'Asia')
    , ('EU', 'Europe')
    , ('NA', 'North America')
    , ('OC', 'Oceania')
    , ('SA', 'South America')
    ]

for code, name in continents :
    try :
        c = db.continent.lookup (code)
    except KeyError :
        db.continent.create (code = code, name = name)
db.commit ()

dx = dxcc.DXCC_File ()
dx.parse ()
for l in dx.dxcc_list :
    if l.entity_type == 'CURRENT' :
        for e in l.entries :
            try :
                d = db.dxcc_entity.lookup (e.code)
            except KeyError :
                cont = e.continent.split (',')
                cont = [db.continent.lookup (x) for x in cont]
                d = dict \
                    ( code      = e.code
                    , name      = e.name
                    , continent = cont
                    )
                try :
                    cq = int (e.cqz)
                    d ['cq_zone'] = cq
                except ValueError :
                    pass
                try :
                    ituz = int (e.ituz)
                    d ['itu_zone'] = ituz
                except ValueError :
                    pass
                db.dxcc_entity.create (**d)

db.commit ()
