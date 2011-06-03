#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = sys.argv [1]
tracker = instance.open (dir)
db      = tracker.open ('admin')

sys.path.insert (1,os.path.join(dir, 'extensions'))
from ldap_rup_sync import LDAP_Roundup_Sync

l = LDAP_Roundup_Sync (db)
if len (sys.argv) > 2 :
    for username in sys.argv [2:] :
        l.sync_user_from_ldap (username)
else :
    for uid in db.user.getnodeids () :
        username = db.user.get (uid, 'username')
        l.sync_user_from_ldap (username)

