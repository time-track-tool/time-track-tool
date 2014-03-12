#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Copy effort to numeric effort, changing everything to person days
import sys
import os
import re
from roundup           import instance
tracker = instance.open (os.getcwd ())
db      = tracker.open  ('admin')

_effort_pattern = r"(\d+) \s* ([PM][DWM]) (?:\s+ \(([^)]+)\))?"
_effort_regex   = re.compile (_effort_pattern, re.VERBOSE)

excpt = { '>150MD' : '150MD', '1' : '1PD', '3' : '3PD', '3D' : '3PD' }

factor = { 'D' : 1, 'W' : 5, 'M' : 20 }

for id in db.issue.getnodeids (retired = False) :
    n = db.issue.getnode (id)
    if n.effort :
        effort = excpt.get (n.effort, n.effort)
        m = _effort_regex.match (effort)
        if not m :
            print n.id
        assert (m)
        n_effort = int (m.groups ()[0]) * factor [m.groups ()[1][1]]
        print '%5s: "%s" = %s' % (id, effort, n_effort)
        db.issue.set (id, numeric_effort = n_effort)
        db.issue.set (id, effort = None)
db.commit ()
