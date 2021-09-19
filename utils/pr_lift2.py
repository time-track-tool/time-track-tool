#!/usr/bin/python

from __future__ import print_function

import sys
from math     import ceil
from csv      import DictReader
from argparse import ArgumentParser
from roundup  import instance

def update_currency (db, args) :
    kc  = db.pr_currency.filter (None, dict (key_currency = 1))
    assert len (kc) == 1
    kc  = db.pr_currency.getnode (kc [0])
    for id in db.pr_currency.getnodeids (retired = False) :
        cur = db.pr_currency.getnode (id)
        d   = {}
        if cur.key_currency :
            assert cur.name == 'EUR'
            assert kc.exchange_rate == 1
        if cur.max_group is None or cur.max_group == 20000 :
            d ['max_group'] = ceil (20000. * cur.exchange_rate)
        if cur.max_team is None or cur.max_team == 10000 :
            d ['max_team']  = ceil (10000. * cur.exchange_rate)
        if d :
            print ("Updating currency%s %s: %s" % (id, cur.name, d))
        if d and args.update :
            db.pr_currency.set (id, **d)
# end def update_currency

def main () :
    cmd = ArgumentParser ()
    cmd.add_argument \
        ( '-d', '--directory'
        , dest    = 'dir'
        , help    = 'Tracker instance directory, default=%(default)s'
        , default = '.'
        )
    cmd.add_argument \
        ( '-n', '--no_update'
        , dest    = 'update'
        , help    = 'Do not update tracker'
        , default = True
        , action  = 'store_false'
        )
    args    = cmd.parse_args ()
    tracker = instance.open (args.dir)
    db      = tracker.open ('admin')
    sys.path.insert (1, args.dir)
    update_currency (db, args)

    if args.update :
        db.commit ()
# end def main

if __name__ == '__main__' :
    main ()
