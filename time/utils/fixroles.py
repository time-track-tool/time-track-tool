#!/usr/bin/python
import os
from roundup           import instance
from roundup.password  import Password, encodePassword
from optparse          import OptionParser

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

"""
    Fix roles: loop over all users and clean up roles that don't exist.
"""

cmd = OptionParser ()
cmd.add_option \
    ( '-a', '--action'
    , dest   = 'action'
    , help   = 'Really remove roles (do a commit)'
    , action = 'store_true'
    )
cmd.add_option \
    ( '-v', '--verbose'
    , dest   = 'verbose'
    , help   = 'Verbose reporting'
    , action = 'store_true'
    )
opt, args = cmd.parse_args ()
if len (args) :
    cmd.error ('No arguments please')
    sys.exit  (23)

for uid in db.user.getnodeids () :
    u      = db.user.getnode (uid)
    if u.roles is None :
        if opt.verbose :
            print "User %s: has no roles" % u.username
        continue
    elif not u.roles :
        db.user.set (uid, roles = None)
        if opt.verbose :
            print "User %s: set empty role to None" % u.username
        continue
    roles  = dict.fromkeys (r.strip () for r in u.roles.split (','))
    change = False
    for r in roles.keys () :
        rl = r.lower ()
        if rl not in db.security.role :
            change = True
            del roles [r]
            print "User %s: delete role: %s" % (u.username, r)
    if change :
        db.user.set (uid, roles = ','.join (roles.iterkeys ()))

if opt.action :
    db.commit()
