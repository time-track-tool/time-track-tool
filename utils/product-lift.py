#!/usr/bin/python
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

types = \
    [ ('KOAT',    'coating/varnish')
    , ('BOND',    'adhesive')
    , ('PRIKOAT', 'primer/precoat')
    ]

for name, desc in types :
    try :
        id = db.rc_product_type.lookup (name)
        n = db.rc_product_type.getnode (id)
        if n.description != desc :
            db.rc_product_type.set (id, description = desc)
    except KeyError :
        db.rc_product_type.create (name = name, description = desc)

applications = \
    [ ('FP', 'Flexible Packaging')
    , ('LP', 'Label Printing')
    , ('PP', 'Paper Packaging')
    , ('PC', 'Publication and Commercial')
    , ('DP', 'Digital Printing')
    ]

for name, desc in applications :
    try :
        id = db.rc_application.lookup (name)
        n = db.rc_application.getnode (id)
        if n.description != desc :
            db.rc_application.set (id, description = desc)
    except KeyError :
        db.rc_application.create (name = name, description = desc)

substrates = \
    [ ('P', 'Paper')
    , ('F', 'Film')
    ]

for name, desc in substrates :
    try :
        id = db.rc_substrate.lookup (name)
        n = db.rc_substrate.getnode (id)
        if n.description != desc :
            db.rc_substrate.set (id, description = desc)
    except KeyError :
        db.rc_substrate.create (name = name, description = desc)

sui = [('LM', 'Low Migration')]
for name, desc in sui :
    try :
        id = db.rc_suitability.lookup (name)
        n = db.rc_suitability.getnode (id)
        if n.description != desc :
            db.rc_suitability.set (id, description = desc)
    except KeyError :
        db.rc_suitability.create (name = name, description = desc)

cap = \
    [ ('stampable',      'hotfoil stampable')
    , ('glueable',       '')
    , ('thermotransfer', '')
    ]
for name, desc in cap :
    try :
        id = db.rc_capability.lookup (name)
        n = db.rc_capability.getnode (id)
        if n.description != desc :
            db.rc_capability.set (id, description = desc)
    except KeyError :
        db.rc_capability.create (name = name, description = desc)

try:
    db.rc_brand.lookup (sys.argv [1])
except KeyError :
    db.rc_brand.create (name = sys.argv [1])

db.commit()
