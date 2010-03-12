#!/usr/bin/python2.4
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for ud in db.user_dynamic.getnodeids () :
    dyn = db.user_dynamic.getnode (ud)
    if dyn.all_in and dyn.overtime_period :
        u = db.user.get (dyn.user, 'username')
        print "Inkonistent: %s is all_in and has Overtime Period set" % u
