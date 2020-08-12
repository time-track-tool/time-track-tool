#!/usr/bin/python
from __future__ import print_function
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

id = db.uc_type.lookup ('Email')
email = db.uc_type.getnode (id)
if email.is_email is None :
    print ("Setting is_email flag for uc_type%s 'Email'" % id)
    db.uc_type.set (id, is_email = True)

db.commit()
