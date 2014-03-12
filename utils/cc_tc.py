#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from csv     import DictReader
from roundup import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

try :
    default = db.cost_center_group.lookup ("Default")
except KeyError :
    default = db.cost_center_group.create (name = "Default")
st_open = db.cost_center_status.lookup ('Open')

ccs = {}

for cc in db.cost_center.getnodeids () :
    n = db.cost_center.getnode (cc)
    ccs [n.name.strip ()] = cc

cc_file = open ('Cost-Center_Without-hours.csv', 'r')

for line in DictReader (cc_file, delimiter = ';') :
    try :
        tc = line ["Time Category"]
    except KeyError :
        tc = line ["Name  "]
    try :
        cc = line ["Cost Center"].strip ()
    except KeyError :
        cc = line ["Cost Center  "].strip ()
    if not cc :
        assert (tc.startswith ('Gesamt'))
        continue
    try :
        tcid = db.time_project.lookup (tc)
    except KeyError :
        try :
            tcid = db.time_project.lookup (tc.strip ())
        except KeyError :
            print "Not found:", line
            continue
    tcn  = db.time_project.getnode (tcid)
    if cc not in ccs :
        ccs [cc] = db.cost_center.create \
            ( name              = cc
            , status            = st_open
            , cost_center_group = default
            )
    ccid = ccs [cc]
    if tcn.cost_center and tcn.cost_center != ccid :
        print "Oops: Changing cost_center to %s for TC %s" % (ccid, tcid)
    db.time_project.set (tcid, cost_center = ccid)
db.commit ()
