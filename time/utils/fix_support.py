#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')
sys.path.insert (1, os.path.join (dir, 'lib'))

# newer postgres
#n = '_prodcat__name__parent_key'
#db.sql ('ALTER TABLE _prodcat DROP CONSTRAINT IF EXISTS %s;' % n)
# old postgres on Suse
n = '_prodcat__name_key'
db.sql ('ALTER TABLE _prodcat DROP CONSTRAINT %s;' % n)
db.sql ('ALTER TABLE _prodcat ADD UNIQUE (_name, _parent);')

types = \
    [ dict (order = 1, name = 'Support Issue')
    , dict (order = 2, name = 'RMA Issue')
    , dict (order = 3, name = 'Supplier Claim')
    , dict (order = 4, name = 'Other')
    ]
exe = \
    [ dict (order = 1, name = 'Repair')
    , dict (order = 2, name = 'Replace')
    , dict (order = 3, name = 'Refund')
    , dict (order = 4, name = 'Return')
    ]

for t in types :
    try :
        r = db.sup_type.lookup (t ['name'])
    except KeyError :
        db.sup_type.create (**t)
        print "created:", t
support_issue = db.sup_type.lookup (types [0]['name'])
rma_issue     = db.sup_type.lookup (types [1]['name'])
for e in exe :
    try :
        r = db.sup_execution.lookup (e ['name'])
    except KeyError :
        db.sup_execution.create (**e)
        print "created:", e

try :
    satisfied = db.sup_status.lookup ('satisfied')
except KeyError :
    satisfied = db.sup_status.create \
        ( name        = 'satisfied'
        , description = 'Customer is satisfied'
        , order       = 3
        , relaxed     = False
        )
customer = []
try :
    customer = [db.sup_status.lookup ('customer')]
except KeyError :
    pass

open   = db.sup_status.lookup ('open')
closed = db.sup_status.lookup ('closed')
db.sup_status.set (open,      transitions = [closed, satisfied] + customer)
db.sup_status.set (closed,    transitions = [open,   satisfied] + customer)
db.sup_status.set (satisfied, transitions = [open,   closed]    + customer)
if customer :
    db.sup_status.set (customer [0], transitions = [open, closed, satisfied])
    db.sup_status.set (satisfied, order = 4, relaxed = False)
    db.sup_status.set (closed,    order = 5)

for si in db.support.getnodeids () :
    sup = db.support.getnode (si)
    # Fix case of existing serial numbers
    sn = sup.serial_number
    if sn :
        newsn = sn.decode ('utf-8').upper ().encode ('utf-8')
        if sn != newsn :
            db.support.set (si, serial_number = newsn)
            print "SN: %s -> %s" % (sn, newsn)
    # Set type to support issue if not set
    if not sup.type :
        if sup.title.startswith ('RMA') :
            db.support.set (si, type = rma_issue)
        else :
            db.support.set (si, type = support_issue)
    elif sup.title.startswith ('RMA') :
        db.support.set (si, type = rma_issue)
    # Loop over messages in id order and find first customer mail
    for m in sorted (int (i) for i in sup.messages) :
        msg = db.msg.getnode (str (m))
        if msg.header and 'X-ROUNDUP-CC' in msg.header :
            db.support.set (si, first_reply = msg.date)
            break

# Set all existing classifications to valid
for c in db.sup_classification.getnodeids () :
    db.sup_classification.set (c, valid = True)

for cid in db.customer.getnodeids (retired = False) :
    cu = db.customer.getnode (cid)
    settings = {}
    if not cu.is_customer and not cu.is_supplier :
        settings ['is_customer'] = True
        settings ['is_supplier'] = False
    if cu.fromaddress :
        if not cu.rmafrom :
            settings ['rmafrom']       = cu.fromaddress
        if not cu.suppclaimfrom :
            settings ['suppclaimfrom'] = cu.fromaddress
    if settings :
        db.customer.set (cid, ** settings)

db.commit ()
