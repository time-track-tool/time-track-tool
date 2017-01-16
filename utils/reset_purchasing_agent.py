#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

stati = ['1', '2']
for id in db.purchase_request.filter (None, dict (status = stati)) :
    db.purchase_request.set (id, purchasing_agents = None)

db.commit()
