#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

occurrence = ['Sporadic', 'Permanent']
hw_variant = \
    ['B0.A03', 'B2.A', 'B2.B', 'B2.C', 'B2.D', 'C1.A', 'C1.B', 'C1.C', 'C1.D']

for n, k in enumerate (occurrence) :
    try :
        id = db.kpm_occurrence.lookup (k)
    except KeyError :
        id = db.kpm_occurrence.create (name = k, order = n * 100 + 100)
    oc = db.kpm_occurrence.getnode (id)
    if oc.order != n * 100 + 100 :
        db.kpm_occurrence.set (id, order = n * 100 + 100)

for n, k in enumerate (hw_variant) :
    try :
        id = db.kpm_hw_variant.lookup (k)
    except KeyError :
        id = db.kpm_hw_variant.create (name = k, order = n * 100 + 100)
    hv = db.kpm_hw_variant.getnode (id)
    if hv.order != n * 100 + 100 :
        db.kpm_hw_variant.set (id, order = n * 100 + 100)

db.commit()
