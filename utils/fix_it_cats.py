#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

stati   = [db.it_issue_status.lookup (i) for i in ('new', 'open', 'feedback')]
cid_tbl = {}

invalid_cats = db.it_category.filter (None, dict (valid = False))
for cid in invalid_cats :
    cat = db.it_category.getnode (cid)
    if cat.name.startswith ('ID ') :
        newcat = db.it_category.lookup (cat.name [3:])
        cid_tbl [cat.id] = newcat

incident  = db.it_request_type.lookup ('Incident')
change_rq = db.it_request_type.lookup ('Change request')

it_issues = db.it_issue.filter \
    (None, dict (category = invalid_cats, status = stati))
for id in it_issues :
    it_issue = db.it_issue.getnode (id)
    d = {}
    if it_issue.category in cid_tbl :
        d ['category'] = cid_tbl [it_issue.category]
        if it_issue.it_request_type is None :
            d ['it_request_type'] = incident
        db.it_issue.set (id, ** d)
        print ("it_issue%s: %s" % (id, d))
    else :
        itcat = db.it_category.get (it_issue.category, 'name')
        print ("it_issue%s with invalid category: %s" % (id, itcat))

valid_cats = db.it_category.filter (None, dict (valid = True))
it_issues = db.it_issue.filter \
    (None, dict (category = valid_cats, status = stati))
for id in it_issues :
    it_issue = db.it_issue.getnode (id)
    if it_issue.it_request_type is None :
        db.it_issue.set (id, it_request_type = change_rq)
        print ("it_issues%s setting to Change request" % id)
        
#db.commit()
