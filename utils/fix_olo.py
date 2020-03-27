#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

# Set the valid_from date of org_location to the creation date.

for oid in db.org_location.getnodeids (retired = False) :
    olo = db.org_location.getnode (oid)
    if olo.group_external is None :
        db.org_location.set (oid, group_external = False)

db.commit()
