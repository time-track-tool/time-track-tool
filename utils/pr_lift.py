#!/usr/bin/python

from __future__ import print_function

import sys
from math     import ceil
from csv      import DictReader
from argparse import ArgumentParser
from roundup  import instance

def export_iter (f) :
    found = False
    for line in f :
        if found :
            yield (line)
        else :
            if 'Id;' in line :
                yield (line)
                found = True
# end def export_iter

def get_user (db, username) :
    if not username :
        return None
    try :
        return db.user.lookup (username)
    except KeyError :
        print ('username not found: "%s"' % username, file = sys.stderr)
# end def get_user

def main () :
    cmd = ArgumentParser ()
    cmd.add_argument \
        ( 'cc'
        , help = 'SAP Cost Center file'
        )
    cmd.add_argument \
        ( 'tc'
        , help = 'Time Category file'
        )
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
    cmd.add_argument \
        ( '-N', '--no-verify-id'
        , dest    = 'verify_id'
        , help    = "Don't verify IDs of sap_cc and TC "
                    "(if importing into prtracker directly for testing)"
        , default = True
        , action  = 'store_false'
        )
    args    = cmd.parse_args ()
    tracker = instance.open (args.dir)
    db      = tracker.open ('admin')
    sys.path.insert (1, args.dir)

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

    with open (args.tc, 'rb') as f :
        dr = DictReader (export_iter (f), delimiter = ';')
        for rec in dr :
            name  = rec ['Name']
            dname = name.decode ('utf-8')
            try :
                tcid = db.time_project.lookup (name)
            except KeyError :
                print ('TC not found: "%s"' % dname, file = sys.stderr)
                continue

            tc   = db.time_project.getnode (tcid)
            rid  = rec ['Id'].decode ('utf-8')
            if args.verify_id and tcid != rid :
                raise ValueError \
                    ( "Non-matching ID for %r: got %s expected %s"
                    % (tc.name, tcid, rid)
                    )
            d  = {}
            gl = get_user \
                (db, (rec ['Grouplead'] or b'').decode ('utf-8').strip ())
            if gl :
                d ['group_lead'] = gl
            tl = get_user \
                (db, (rec ['Teamlead'] or b'').decode ('utf-8').strip ())
            if tl :
                d ['team_lead'] = tl
            if d :
                print ("Updating time_project%s %s: %s" % (tcid, tc.name, d))
            if d and args.update :
                db.time_project.set (tcid, **d)
    with open (args.cc, 'rb') as f :
        dr = DictReader (export_iter (f), delimiter = ';')
        for rec in dr :
            name  = rec ['Name']
            dname = name.decode ('utf-8')
            try :
                ccid = db.sap_cc.lookup (name)
            except KeyError :
                print ('CC not found: "%s"' % dname, file = sys.stderr)
                continue
            cc   = db.sap_cc.getnode (ccid)
            rid  = rec ['Id'].decode ('utf-8')
            if args.verify_id and ccid != rid :
                raise ValueError \
                    ( "Non-matching ID for %r: got %s expected %s"
                    % (cc.name, ccid, rid)
                    )
            d  = {}
            gl = get_user \
                (db, (rec ['Grouplead'] or b'').decode ('utf-8').strip ())
            if gl :
                d ['group_lead'] = gl
            tl = get_user \
                (db, (rec ['Teamlead'] or b'').decode ('utf-8').strip ())
            if tl :
                d ['team_lead'] = tl
            if d :
                print ("Updating sap_cc%s %s: %s" % (ccid, cc.name, d))
            if d and args.update :
                db.sap_cc.set (ccid, **d)
    if args.update :
        db.commit ()
# end def main

if __name__ == '__main__' :
    main ()
