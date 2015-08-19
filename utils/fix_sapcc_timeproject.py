#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

closed  = db.time_project_status.lookup ('Closed')
for id in db.time_project.getnodeids () :
    tp = db.time_project.getnode (id)
    if tp.status == closed :
        continue
    if tp.cost_center is None :
        print 'Empty productivity: %s %s' % (id, tp.name)
        continue
    oh = bool (tp.description and 'only hours' in tp.description.lower ())
    if oh != tp.only_hours :
        db.time_project.set (id, only_hours = oh)
        print id

for id in db.sap_cc.getnodeids () :
    sc = db.sap_cc.getnode (id)
    if sc.description and sc.description.startswith ('Responsible:') :
        nick = sc.description.split (':', 1) [1].strip ().lower ()
        users = db.user.filter (None, dict (nickname = nick))
        for u in users :
            if db.user.get (u, 'nickname') == nick :
                break
        else :
            raise ValueError ("Nickname: %s not found" % nick)
        if sc.responsible != u :
            db.sap_cc.set (id, responsible = u)

db.commit()
