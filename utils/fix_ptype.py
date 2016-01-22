#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for id in db.purchase_type.getnodeids (retired = False) :
    pt = db.purchase_type.getnode (id)
    if pt.valid is None :
        db.purchase_type.set (id, valid = True)

db.commit()
