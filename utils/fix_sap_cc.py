#!/usr/bin/python3

import sys
import os
from roundup           import instance
directory = os.getcwd ()
tracker   = instance.open (directory)
db        = tracker.open ('admin')

# Replace retired SAP-CC entries in PRs with equivalent (same name)
# SAP-CC that is *not* retired.
for id in db.purchase_request.getnodeids (retired = False):
    pr = db.purchase_request.getnode (id)
    if pr.sap_cc is None or not db.sap_cc.is_retired (pr.sap_cc):
        continue
    ccn = db.sap_cc.get (pr.sap_cc, 'name')
    # Check if we can find a sap_cc with the same name and not retired
    new_sap_cc = db.sap_cc.filter \
        (None, {}, exact_match_spec = dict (name = '%s:' % ccn))
    assert len (new_sap_cc) <= 1
    if len (new_sap_cc) == 0:
        continue
    #db.purchase_request.set (id, sap_cc = new_sap_cc)
    print ('sap_cc%s->sap_cc%s' % (pr.sap_cc, new_sap_cc))
#db.commit ()
