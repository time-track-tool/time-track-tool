#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

und = db.pr_approval_status.lookup ('undecided')

for id in db.pr_approval.filter (None, dict (status = und)) :
    app = db.pr_approval.getnode (id)
    if app.msg :
        print "pr_approval%s" % id
        db.pr_approval.set (id, msg = None)
db.commit ()

