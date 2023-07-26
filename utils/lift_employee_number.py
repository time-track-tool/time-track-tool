#!/usr/bin/python3
from __future__ import print_function
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for uid in db.user.getnodeids (retired = False):
    user = db.user.getnode (uid)
    if not user.employee_number:
        db.user.set (uid, employee_number = uid)

db.sql \
    ( 'alter table _user add constraint '
      'user_employee_number_unique unique '
      '(_employee_number, __retired__);'
    )

db.commit()
