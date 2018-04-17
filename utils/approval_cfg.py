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

for id in db.pr_approval_order.getnodeids (retired = False) :
    r = db.pr_approval_order.getnode (id)
    d = {}
    if r.is_board is None :
        v = False
        if r.role == 'board' :
            v = True
        d ['is_board'] = v
    if r.is_finance is None :
        v = False
        if r.role == 'finance' :
            v = True
        d ['is_finance'] = v
    if d :
        db.pr_approval_order.set (id, **d)

board_roles   = db.pr_approval_order.filter (None, dict (is_board = True))
finance_roles = db.pr_approval_order.filter (None, dict (is_finance = True))

# Check if there are any pr_approval_config entries with board or
# finance roles
for r in (board_roles, finance_roles) :
    ac = db.pr_approval_config.filter (None, dict (role = r))
    if ac :
        break
else :
    assert len (board_roles)   == 1
    assert len (finance_roles) == 1
    db.pr_approval_config.create \
        ( amount        = 10000
        , if_not_in_las = False
        , organisations = []
        , role          = board_roles [0]
        , valid         = True
        )
    db.pr_approval_config.create \
        ( amount        = 1000
        , if_not_in_las = False
        , organisations = []
        , role          = finance_roles [0]
        , valid         = True
        )

db.commit()
