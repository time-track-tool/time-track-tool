#!/usr/bin/python
from __future__ import print_function
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for id in db.user_dynamic.getnodeids (retired = False) :
    dyn = db.user_dynamic.getnode (id)
    if dyn.exemption is None :
        db.user_dynamic.set (id, exemption = False)

db.commit()
