#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
from optparse          import OptionParser
dir     = os.getcwd ()

sys.path.insert (1, os.path.join (dir, 'lib'))
import common

cmd = OptionParser ()
cmd.add_option \
    ( '-u', '--update'
    , dest   = 'update'
    , help   = 'Really fix emails (do a commit)'
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

tracker = instance.open (dir)
db      = tracker.open ('admin')
for u in db.user.getnodeids (retired = False) :
    common.update_emails (db, u, verbose = opt.verbose)
if opt.update :
    db.commit ()
