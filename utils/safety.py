#!/usr/bin/python
import sys
import os
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

safety_levels = \
    [ 'ASIL-A'
    , 'ASIL-B'
    , 'ASIL-C'
    , 'ASIL-D'
    , 'QM'
    , '-None-'
    ]

test_levels = \
    [ 'Unit-Test'
    , 'Int-Test'
    , 'SW-Test'
    , 'Sys-Int-Test'
    , 'AppInt'
    , 'UseCaseTest'
    , 'CustomerTest'
    ]

for sl in safety_levels :
    try :
        db.safety_level.lookup (sl)
    except KeyError :
        db.safety_level.create (name = sl)

for tl in test_levels :
    try :
        db.test_level.lookup (tl)
    except KeyError :
        db.test_level.create (name = tl)

db.commit ()

