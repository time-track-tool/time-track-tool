#!/usr/bin/python

# Lift data for new ldap sync

from __future__ import print_function
import sys
import os
from roundup           import instance

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

changed = False
va = db.user_status.getnode ('1')
assert va.name == 'valid-ad'
if not va.ldap_prio :
    db.user_status.set ('1', ldap_prio = 1)
    print ("user_status.set ('1', ldap_prio = 1)")
    changed = True
sa = db.user_status.getnode ('6')
assert sa.name == 'system-ad'
if not sa.ldap_prio :
    db.user_status.set ('6', ldap_prio = 2)
    print ("user_status.set ('6', ldap_prio = 2)")
    changed = True
vap = db.user_status.getnode ('8')
assert vap.name == 'valid-ad-nopermission'
d = {}
if not vap.ldap_prio :
    d ['ldap_prio'] = 10
if not vap.ldap_group or vap.ldap_group == 's_or_ad-personal-user' :
    d ['ldap_group'] = 's_or_ad-natural-user'

if d :
    db.user_status.set ('8', **d)
    print ("user_status.set ('8', **%s)" % str (d))
    changed = True


id = db.uc_type.lookup ('Email')
email = db.uc_type.getnode (id)
if email.is_email is None :
    print ("Setting is_email flag for uc_type%s 'Email'" % id)
    db.uc_type.set (id, is_email = True)
    changed = True

for ctid in db.contract_type.getnodeids (retired = False) :
    ct = db.contract_type.getnode (ctid)
    if ct.group_external is None :
        db.contract_type.set (ctid, group_external = False)
        print ("Setting contract_type%s group_external = False" % ctid)
        change = True

if changed :
    db.commit ()

