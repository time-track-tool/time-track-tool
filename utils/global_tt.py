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

# Loop over all active time_projects and set is_extern to False
active_stati = db.time_project_status.filter (None, dict (active = True))
for tpid in db.time_project.filter (None, dict (status = active_stati)) :
    tp = db.time_project.getnode (tpid)
    if tp.cost_center is None :
        print ("No productivity: time_project%s" % tpid)
        continue
    if tp.is_extern is None :
        db.time_project.set (tpid, is_extern = False)
db.commit ()

# Set user.reduced_activity_list for caban to 2019-12-19
try :
    caban = db.user.lookup ('caban')
    db.user.set (caban, reduced_activity_list = data.Date ('2019-12-19'))
    db.commit ()
except KeyError : # No user caban
    pass
