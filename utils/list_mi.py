#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import sys
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
tracker = instance.open (os.getcwd ())
db      = tracker.open ('admin')

# loop over all issues in several passes and fix maturity_index

id_depends = {}
cache      = {}

for id in db.issue.getnodeids () :
    n = db.issue.getnode (id)
    print "%5s: %5s" % (id, n.maturity_index)
