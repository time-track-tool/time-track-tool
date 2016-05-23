#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import sys
from roundup import instance

tracker = instance.open (os.getcwd ())
db      = tracker.open  ('admin')

# Loop over container(s) given on command line
# Set effort_hours / 8

closed  = db.status.lookup ('closed')

def set_numeric_effort (id) :
    issue = db.issue.getnode (id)
    if issue.status == closed :
        return
    if issue.composed_of :
        for i in issue.composed_of :
            set_numeric_effort (i)
    if issue.effort_hours :
        assert issue.effort_hours % 8 == 0
        db.issue.set (id, effort_hours = issue.effort_hours / 8)
        print ("issue%s" % id)
    

for id in sys.argv [1:] :
    set_numeric_effort (id)
db.commit ()
