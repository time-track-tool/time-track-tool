#!/usr/bin/python3

# Add permission entries for users moved from org19 to org20

import sys
import os
from roundup  import instance
from argparse import ArgumentParser
from csv      import reader

cmd = ArgumentParser ()
cmd.add_argument \
    ( 'csv_file'
    , help  = 'CSV file with user list'
    )
cmd.add_argument \
    ( '--do-update'
    , action = 'store_true'
    , help   = 'Actually perform the database update'
    )
args = cmd.parse_args ()

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')



with open (args.csv_file, 'r') as f:
    cr = reader (f, delimiter = ';')
    for rec in cr:
        if '@' not in rec [8]:
            continue
        username = rec [8]
        try:
            uid = db.user.lookup (username)
        except KeyError:
            print ('WARN: No user %s' % username)
            continue
        prid = db.o_permission.filter (None, dict (user = uid))
        assert len (prid) <= 1
        assert rec [10] in ('yes', 'no')
        assert rec [11] in ('yes', 'no')
        if rec [10] == 'no':
            assert rec [11] == 'no'
            continue
        orgs = ['20']
        if rec [11] == 'no':
            orgs.insert (0, '19')
        doit = 'no '
        if args.do_update:
            doit = ''
        if len (prid) == 1:
            id = prid [0]
            prm = db.o_permission.getnode (id)
            #assert prm.org_group is None, username
            if '20' not in prm.organisation:
                orgs.append ('20')
                if args.do_update:
                    db.o_permission.set (id, organisation = orgs)
                print ('%supdate: %s' % (doit, username))
        else:
            if args.do_update:
                db.o_permission.create (user = uid, organisation = orgs)
            print ('%screate: %s' % (doit, username))
    if args.do_update:
        db.commit ()
