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
    if len (sc.name) != 7 and not sc.description :
        name, desc = sc.name.split ('_', 1)
        db.sap_cc.set (id, name = name, description = desc)
    if sc.valid is not None :
        continue
    if 'gelöscht' in sc.name :
        db.sap_cc.set (id, valid = False)
    else :
        db.sap_cc.set (id, valid = True)

db.commit()
