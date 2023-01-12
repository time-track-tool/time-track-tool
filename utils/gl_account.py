#!/usr/bin/python3

import sys
import os
import csv
from roundup import instance
from roundup.date import Date
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for ptid in db.purchase_type.getnodeids (retired = False):
    pt = db.purchase_type.getnode (ptid)
    d  = {}
    if pt.allow_gl_account is None:
        if pt.name == 'Material / Stock':
            d.update (allow_gl_account = False)
        else:
            d.update (allow_gl_account = True)
    if d:
        db.purchase_type.set (ptid, **d)

# Fix locations
with open (sys.argv [1], 'r') as f:
    dr = csv.DictReader (f, delimiter = ';')
    for rec in dr:
        try:
            loc = db.location.getnode (rec ['id'])
            loc.name
        except IndexError:
            print ("Warning: location%s not existing" % rec ['id'])
            db.location.create \
                ( name       = rec ['name']
                , country    = rec ['country']
                , city       = rec ['city']
                , address    = rec ['address']
                , valid_from = Date ('2022-12-12')
                )
            continue
        if not rec ['city']:
            if not loc.valid_to:
                db.location.set (loc.id, valid_to = Date ('2022-12-12'))
        else:
            assert rec ['address']
            assert not rec ['valid_to']
            d = {}
            for a in 'name', 'country', 'city', 'address', 'valid_from':
                v = rec [a]
                if a == 'valid_from':
                    v = Date (v)
                if loc [a] != v:
                    d [a] = v
            if d:
                db.location.set (loc.id, **d)

db.commit ()
