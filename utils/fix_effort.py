#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import sys
from roundup import instance

tracker = instance.open (os.getcwd ())
db      = tracker.open  ('admin')

# Loop over all issues and set effort_hours from numeric_effort * 8

ids = db.issue.getnodeids (retired = False)
ids.sort (key = int)
print "Last issue: %s" % ids [-1]
for id in ids :
    if (int (id) % 100) == 0 :
        print "\r%s" % id,
        sys.stdout.flush ()
    issue = db.issue.getnode (id)
    if issue.numeric_effort is None :
        continue
    hours = issue.numeric_effort * 8
    if issue.numeric_effort and not issue.effort_hours :
        db.issue.set (id, effort_hours = hours, numeric_effort = None)
print ""
db.commit ()
