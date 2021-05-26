#!/usr/bin/python
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for id in db.substance.getnodeids (retired = False) :
    s = db.substance.getnode (id)
    #print (id)
    if s.is_raw_material is None :
        db.substance.set (id, is_raw_material = not s.ingredients)

db.commit()
