#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

all_stati  = db.status.getnodeids ()
testing    = db.status.lookup ("testing")
no_testing = [s for s in all_stati if s != testing]

for s in db.doc_issue_status.getnodeids () :
    docstatus = db.doc_issue_status.getnode (s)
    stati     = all_stati
    if docstatus.name == 'undecided' :
        stati = no_testing
    db.doc_issue_status.set (s, may_change_state_to = stati)
db.commit ()
