#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from csv     import DictReader
from roundup import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

default = db.cost_center_group.create (name = "Default")
st_open = db.cost_center_status.lookup ('Open')

ccs = {}

cc_file = open ('Cost_Center_2010-11-24.csv', 'r')
for line in DictReader (cc_file, delimiter = ';') :
    tc = line ["Time Category"]
    cc = line ["Cost Center"]
    if not cc :
        assert (tc.startswith ('Gesamt'))
        continue
    try :
        tcid = db.time_project.lookup (tc)
    except KeyError :
        print "Not found:", line
        continue
    tcn  = db.time_project.getnode (tcid)
#    if cc not in ccs :
#        ccs [cc] = db.cost_center.create \
#            ( name              = cc
#            , status            = st_open
#            , cost_center_group = default
#            )
#    ccid = ccs [cc]
#    db.time_project.set (tcid, cost_center = ccid)

