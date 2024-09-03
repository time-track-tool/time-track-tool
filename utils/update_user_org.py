#!/usr/bin/python3

import sys
import os
from roundup           import date
from roundup           import instance
from argparse          import ArgumentParser
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

cmd = ArgumentParser ()
cmd.add_argument \
    ( '-u', '--update'
    , help    = 'Do updates'
    , action  = 'store_true'
    )
cmd.add_argument \
    ( '-v', '--verbose'
    , help    = 'Verbose printing, specify several times for more verbosity'
    , action  = 'count'
    , default = 0
    )
args = cmd.parse_args ()

tc_org = set \
    ([ '19', '20', '21', '22', '27', '31', '32', '33', '34', '40'
     , '41', '42', '43', '44', '45', '48', '50', '51', '52', '53'
     , '55', '58', '59', '61', '62', '63', '64', '65', '66'
    ])
ta_org = set (['23', '37', '39', '46', '47', '49', '54', '56', '60'])
seltsam = set (['52', '53', '55', '62', '63', '64', '65'])

tc_org = tc_org - seltsam

sys.path.insert (1, os.path.join (dir, 'lib'))

user_org = {}
changed  = False

for sid in db.sap_cc.getnodeids (retired = False):
    sap_cc = db.sap_cc.getnode (sid)
    if not sap_cc.organisation or not sap_cc.valid:
        continue
    for uid in (sap_cc.responsible, sap_cc.deputy):
        if not uid:
            continue
        u = db.user.getnode (uid)
        if u.status != '1':
            continue
        if uid not in user_org:
            user_org [uid] = set ()
        user_org [uid].add (sap_cc.organisation)
        if args.verbose > 2:
            print ('user%s sap_cc%s' % (uid, sid))
tp_status = db.time_project_status.filter (None, dict (active = True))
for pid in db.psp_element.getnodeids (retired = False):
    psp = db.psp_element.getnode (pid)
    if not psp.valid:
        continue
    tid = psp.project
    tc  = db.time_project.getnode (tid)
    if not tc.organisation or tc.status not in tp_status:
        continue
    for uid in (tc.responsible, tc.deputy):
        if not uid:
            continue
        u = db.user.getnode (uid)
        if u.status != '1':
            continue
        if uid not in user_org:
            user_org [uid] = set ()
        user_org [uid].add (psp.organisation)
        if args.verbose > 2:
            print ('user%s psp%s tc%s' % (uid, pid, tid))

for uid in user_org:
    u = db.user.getnode (uid)
    if args.verbose > 1:
        print ('user%s %s' % (uid, u.username))
    orgs = user_org [uid]
    assert len (orgs) >= 1
    if len (orgs) == 1 and u.organisation == list (orgs) [0]:
        if args.verbose > 1:
            print ('    Same org')
        continue
    if u.organisation:
        orgs.add (u.organisation)
    for oid in orgs:
        org = db.organisation.getnode (oid)
        if args.verbose > 1:
            print ('    organisation%s %s' % (oid, org.name))
    if tc_org.intersection (orgs) and ta_org.intersection (orgs):
        if args.verbose > 1:
            print ('    USER IS IN BOTH ORGS')
        if not u.organisation:
            continue
        assert u.organisation not in tc_org or u.organisation not in ta_org
        t_orgs = tc_org if u.organisation in tc_org else ta_org
        orgs = t_orgs.intersection (orgs)
    opid = db.o_permission.filter (None, dict (user = uid))
    if opid:
        assert len (opid) == 1
        opid = opid [0]
        perm = db.o_permission.getnode (opid)
        # Only update if we would add organisations
        if orgs - set (perm.organisation):
            orgs.update (perm.organisation)
            orgs = list (orgs)
            if args.verbose:
                print ('Update: user%s %s orgs: %s' % (uid, u.username, orgs))
            if args.update:
                db.o_permission.set (opid, organisation = orgs)
                changed = True
    else:
        orgs = list (orgs)
        if args.verbose:
            print ('Create: user%s %s orgs: %s' % (uid, u.username, orgs))
        if args.update:
            opid = db.o_permission.create (user = uid, organisation = orgs)
            changed = True

if changed and args.update:
    db.commit ()
