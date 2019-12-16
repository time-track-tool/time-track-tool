#!/usr/bin/python

""" Updates for global TT
"""

import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()
sys.path.insert (1, os.path.join (dir, 'lib'))

import common

tracker = instance.open (dir)
db      = tracker.open ('admin')

try :
    v = db.user_status.lookup ('valid-ad')
except KeyError :
    # Rename old 'valid' user-status
    v = db.user_status.lookup ('valid')
    db.user_status.set (v, name = 'valid-ad', timetracking_allowed = True)
    v = db.user_status.create \
        ( name                 = 'valid'
        , is_nosy              = True
        , timetracking_allowed = True
        , description          = 'Valid user not synced to AD'
        , roles                = 'User,Nosy'
        )
    db.commit ()

# Check if appropriate permission exist
# Loop over *all* valid* users and check roles:
# - Move legacy 'Domain-User-Edit' role to 'Dom-User-Edit-GTT'
# - Add 'Dom-User-Edit-HR' to users with 'HR' role (if not yet added)
# - Add 'Dom-User-Edit-Office' to users with 'Office' role
# case-insensitive substring match:
valid = db.user_status.filter (None, dict (name = 'valid'))
for u in db.user.filter (None, dict (status = valid)) :
    user = db.user.getnode (u)
    roles = set (common.role_list (user.roles))
    if 'domain-user-edit' in roles :
        roles.discard ('domain-user-edit')
        roles.add ('dom-user-edit-gtt')
    # the dom-user roles restrict what you may edit, don't do this to it
    if 'it' not in roles :
        if 'hr' in roles :
            roles.add ('dom-user-edit-hr')
        if 'office' in roles :
            roles.add ('dom-user-edit-office')
        if 'facility' in roles :
            roles.add ('dom-user-edit-facility')
    if roles != set (common.role_list (user.roles)) :
        db.user.set (u, roles = ','.join (sorted (roles)))
        print (user.username)
db.commit ()
