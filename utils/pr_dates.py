#!/usr/bin/python
import sys
import os
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for prid in db.purchase_request.getnodeids (retired = False) :
    pr = db.purchase_request.getnode (prid)
    if pr.date_ordered or pr.date_approved :
        continue
    if pr.status in ('1', '2', '4', '5') :
        continue
    hist  = db.getjournal ('purchase_request', prid)
    #print prid
    status = pr.status
    date_approved = date_ordered = None
    for h in sorted (hist, key = lambda x : x [1], reverse = True) :
        if h [3] != 'set' :
            continue
        if 'status' not in h [4] :
            continue
        # approved
        if status == '3' and not date_approved :
            date_approved = h [1]
        # ordered
        if status == '6' and not date_ordered :
            date_ordered = h [1]
        #print status, h
        status = h [4]['status']
    print prid, date_approved, date_ordered
    assert not date_ordered or date_approved
    d = {}
    if date_approved :
        d ['date_approved'] = date_approved
    if date_ordered :
        d ['date_ordered']  = date_ordered
    db.purchase_request.set (prid, **d)

db.commit()
