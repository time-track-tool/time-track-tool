#!/usr/bin/python3

import sys
import os
from roundup  import instance
from argparse import ArgumentParser
directory = os.getcwd ()
tracker   = instance.open (directory)
db        = tracker.open ('admin')

def get_new_sap_cc (db, sap_cc_id):
    ccn = db.sap_cc.get (sap_cc_id, 'name')
    # Check if we can find a sap_cc with the same name and not retired
    new_sap_cc = db.sap_cc.filter \
            (None, {}, exact_match_spec = dict (name = '%s' % ccn))
    assert len (new_sap_cc) <= 1
    if len (new_sap_cc) == 0:
        return None, ccn
    return new_sap_cc [0], ccn
# end def get_new_sap_cc

cmd = ArgumentParser ()
cmd.add_argument \
    ( '-u', '--update'
    , help    = 'Do updates'
    , action  = 'store_true'
    )
args = cmd.parse_args ()

# This is broken: It has both a sap_cc and a psp-element and it is not attached
# to any PR
db.pr_offer_item.retire ('31797')

# Replace retired SAP-CC entries in offer items with equivalent (same name)
# SAP-CC that is *not* retired.
for id in db.pr_offer_item.getnodeids (retired = False):
    oi = db.pr_offer_item.getnode (id)
    if oi.sap_cc is None or not db.sap_cc.is_retired (oi.sap_cc):
        continue
    new_sap_cc, ccn = get_new_sap_cc (db, oi.sap_cc)
    if new_sap_cc is None:
        continue
    print ('Retired sap-cc: pr_offer_item%s name=%s' % (id, ccn))
    print \
        ('pr_offer_item%s: sap_cc%s->sap_cc%s' % (id, oi.sap_cc, new_sap_cc))
    db.pr_offer_item.set (id, sap_cc = new_sap_cc)
# Replace retired SAP-CC entries in PRs with equivalent (same name)
# SAP-CC that is *not* retired.
for id in db.purchase_request.getnodeids (retired = False):
    pr = db.purchase_request.getnode (id)
    if pr.sap_cc is None or not db.sap_cc.is_retired (pr.sap_cc):
        continue
    new_sap_cc, ccn = get_new_sap_cc (db, pr.sap_cc)
    if new_sap_cc is None:
        continue
    print ('Retired sap-cc: purchase_request%s name=%s' % (id, ccn))
    print \
        ('purchase_request%s: sap_cc%s->sap_cc%s' % (id, pr.sap_cc, new_sap_cc))
    db.purchase_request.set (id, sap_cc = new_sap_cc)
if args.update:
	db.commit ()
