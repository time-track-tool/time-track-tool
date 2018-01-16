#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

linkdict = dict.fromkeys (('pr_offer_item', 'purchase_request'))

for id in db.pr_currency.getnodeids (retired = False) :
    h_old = db.getjournal ('pr_currency', id)
    h_new = []
    for h in h_old :
        if h [3] in ('link', 'unlink') :
            if h [4][0] in linkdict :
                continue
        h_new.append (h)
        print h_new [-1]
    if h_old != h_new :
        db.setjournal ('pr_currency', id, h_new)
    

db.commit()
