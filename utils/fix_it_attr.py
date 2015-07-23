#!/usr/bin/python

import os
import sys
from   roundup           import instance

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for cat in db.it_category.getnodeids (retired = False) :
    if db.it_category.get (cat, 'valid') is None :
        db.it_category.set (cat, valid = True)

for n, k in enumerate (('Incident', 'Change request')) :
    try :
        db.it_request_type.lookup (k)
    except KeyError :
        db.it_request_type.create (name = k, order = n)

db.commit ()


