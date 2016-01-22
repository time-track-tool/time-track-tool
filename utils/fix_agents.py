#!/usr/bin/python
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for id in db.time_project.getnodeids (retired = False) :
    tp = db.time_project.getnode (id)
    if not tp.purchasing_agent :
        continue
    db.time_project.set \
        (id, purchasing_agents = [tp.purchasing_agent], purchasing_agent = None)

for id in db.sap_cc.getnodeids (retired = False) :
    sc = db.sap_cc.getnode (id)
    if not sc.purchasing_agent :
        continue
    db.sap_cc.set \
        (id, purchasing_agents = [sc.purchasing_agent], purchasing_agent = None)

db.commit()
