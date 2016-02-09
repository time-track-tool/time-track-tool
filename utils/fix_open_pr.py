#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

op = db.pr_status.lookup ('open')

for id in db.purchase_request.filter (None, dict (status = op)) :
    pr = db.purchase_request.getnode (id)
    if pr.total_cost is not None :
        print pr.title
        db.purchase_request.set (id, total_cost = None)

#db.commit()
