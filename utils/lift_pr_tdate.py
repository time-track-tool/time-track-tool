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

# Fix pr_status, allow approved->rejected
apr = db.pr_status.getnode (db.pr_status.lookup ('approved'))
rej = db.pr_status.lookup ('rejected')
if rej not in apr.transitions :
    t = []
    t.extend (apr.transitions)
    t.append (rej)
    db.pr_status.set (apr.id, transitions = t)

# Fix approval type HR Confidential: set confidential flag
hrc = db.purchase_type.lookup ('HR Confidential')
hrc = db.purchase_type.getnode (hrc)
if not hrc.confidential :
    db.purchase_type.set (hrc.id, confidential = True)

db.commit()
