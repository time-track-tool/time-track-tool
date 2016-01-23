#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for id in db.sap_cc.getnodeids (retired = False) :
    sc = db.sap_cc.getnode (id)
    if sc.valid is not None :
        continue
    if 'gelöscht' in sc.name :
        db.sap_cc.set (id, valid = False)
    else :
        db.sap_cc.set (id, valid = True)

db.commit()
