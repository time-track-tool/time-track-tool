#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

org_map = \
    {  1 : 19
    ,  2 : 20
    ,  3 : 21
    ,  4 : 22
    ,  5 : 23
    ,  6 : None
    ,  7 : None
    ,  8 : 24
    , 10 : 25
    , 11 : 26
    , 12 : 27
    , 13 : 32
    , 14 : 28
    , 15 : 33
    , 17 : 30
    , 18 : 31
    }

for id in db.pr_supplier_rating.getnodeids (retired = False) :
    sr  = db.pr_supplier_rating.getnode (id)
    oid = int (sr.organisation)
    if db.organisation.is_retired (oid) :
        if oid not in org_map :
            print "pr_supplier_rating%s: Not in org_map: %s" % (id, oid)
            continue
        if org_map [oid] is not None :
	    print "pr_supplier_rating%s: org %s->%s" % (id, oid, org_map [oid])
	    db.pr_supplier_rating.set (id, organisation = str (org_map [oid]))
        else :
            print "pr_supplier_rating%s: retire" % (id)
            db.pr_supplier_rating.retire (id)

#db.commit()
