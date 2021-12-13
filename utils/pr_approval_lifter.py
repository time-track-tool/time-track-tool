#!/usr/bin/python
import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

for aoid in db.pr_approval_order.getnodeids (retired = False) :
    ao = db.pr_approval_order.getnode (aoid)
    if ao.only_nosy is None :
        ao.only_nosy = False
    if ao.want_no_messages is None :
        ao.want_no_messages = False

db.commit()
