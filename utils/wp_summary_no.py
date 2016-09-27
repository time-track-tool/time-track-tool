#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')


items = \
    [ 'Project management'
    , 'Configuration management'
    , 'Training'
    , 'Quality'
    , 'Requirements'
    , 'Design'
    , 'Implementation'
    , 'Module, Unit test'
    , 'Integration'
    , 'Production transition'
    , 'System test, Verification'
    , 'Verification by analysis'
    , 'Documentation'
    , 'Release, Shipment'
    , 'Buffer'
    , 'On-site engineering'
    , 'Conceptual Design, Architecture'
    , 'Certification activities'
    , 'SWP 19'
    , 'SWP 20'
    ]

for n, item in enumerate (items) :
    db.time_wp_summary_no.create (name = item, order = (n + 1) * 100)

wps = db.time_wp.getnodeids (retired = False)
for wpid in wps :
    wp = db.time_wp.getnode (wpid)
    if wp.wp_no  :
        x = wp.wp_no
        if '.' in x :
            x = x.split ('.', 1) [0]
        no = -1
        try :
            no = int (x)
        except ValueError :
            pass

        if no <= 0 or no > 20 :
            continue
            #print "%s: %s" % (wp.id, wp.wp_no)
        db.time_wp.set (wpid, time_wp_summary_no = str (no))

db.commit()
