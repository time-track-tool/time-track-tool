#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for n in 'yes', 'no' :
    try :
        db.pr_ext_resource.lookup (n)
    except KeyError :
        db.pr_ext_resource.create (name = n)

# Remove forced approval role from purchase_type9
pt9 = db.purchase_type.getnode ('9')
if '12' in pt9.pr_forced_roles :
    n = set (pt9.pr_forced_roles) - set (('12',))
    db.purchase_type.set ('9', pr_forced_roles = list (n))
# Modify unused approval config in place
ac = db.pr_approval_config.getnode ('2')
if not ac.valid :
    db.pr_approval_config.set \
        ( '2'
        , valid           = True
        , role            = '12'
        , amount          = 0
        , if_not_in_las   = False
        , pr_ext_resource = '1'
        )
# Fix existing approval_config 1 to include all purchase_types except 14
ac = db.pr_approval_config.getnode ('1')
if not ac.purchase_type :
    all_pt = db.purchase_type.getnodeids (retired = False)
    pts    = set (all_pt) - set (('14', ))
    db.pr_approval_config.set \
        ( '1'
        , purchase_type = list (pts)
        )

db.commit()
