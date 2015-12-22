#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
import csv
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

dr = csv.DictReader (open (sys.argv [1], 'r'), delimiter = ';')

# Importer for departments for pr-tracker until departments are correct
# in time-tracker

for line in dr :
    name = line ['Department'].strip ()
    head = line ['Head'].strip ()
    depu = line ['Deputy'].strip ()
    if head == 'kopetz' :
        head = 'gkopetz'
    if depu == 'kopetz' :
        depu = 'gkopetz'
    if head :
        head = db.user.lookup (head)
    else :
        head = None
    if depu :
        depu = db.user.lookup (depu)
    else :
        depu = None
    print name, head, depu
    try :
        dept = db.department.lookup (name)
        db.department.set (dept, manager = head, deputy = depu)
    except KeyError :
        dept = db.department.create (name = name, manager = head, deputy = depu)

for did in db.department.getnodeids (retired = False) :
    dept = db.department.getnode (did)
    if not dept.manager :
        db.department.retire (did)


db.commit()

