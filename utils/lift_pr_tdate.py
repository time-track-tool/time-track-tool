#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

sys.path.insert (1, os.path.join (dir, 'lib'))

import common

# Find PRs with continuous obligation
prs = db.purchase_request.filter (None, dict (continuous_obligation = True))

for prid in prs :
    pr = db.purchase_request.getnode (prid)
    if pr.termination_date and not pr.intended_duration :
        pdate = pr.termination_date.pretty (common.ymd)
        print prid, pdate
        db.purchase_request.set (prid, intended_duration = pdate)

db.commit()
