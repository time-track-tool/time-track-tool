#!/usr/bin/python3


import sys
import os
from roundup           import instance
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

db.commit ()
