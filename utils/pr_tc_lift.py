#!/usr/bin/python3

import sys
import os
from roundup import instance

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

# Terms & Conditions new values

new = set \
    (( 'based on contract in nego/finalisation'
    ,  'based on signed contract'
    ,  'based on individual offer'
    ,  'Online/Webshop'
    ))

for id in db.terms_conditions.getnodeids (retired = False):
    tc = db.terms_conditions.getnode (id)
    if tc.name in new:
        new.remove (tc.name)
        continue
    if tc.is_valid != False:
        db.terms_conditions.set (id, is_valid = False)
for n, name in enumerate (new):
    db.terms_conditions.create (name = name, is_valid = True, order = n + 3)
db.commit ()

