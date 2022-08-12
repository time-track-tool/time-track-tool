#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Cron-job for updating adr-type for valid or closed abos.
# Should be run in the early morning of every 1st of a month.

import sys
from roundup.date      import Date
from roundup           import instance
tracker = instance.open (sys.argv [1])
db      = tracker.open  ('admin')

now           = Date ('.')
type_cat      = db.adr_type_cat.lookup ('ABO')
abo_adr_types = db.adr_type.find (typecat = type_cat)
adr           = db.address.filter (None, {'adr_type' : abo_adr_types})
adr           = dict ([(k, 1) for k in adr])

valid_abos    = db.abo.filter (None, {'end' : '-1'})
storno_abos   = db.abo.filter (None, {'end' : now.pretty (';%Y-%m-%d')})

for abo in valid_abos + storno_abos :
    adr [db.abo.get (abo, 'subscriber')] = 1

for a in adr :
    # May seem like a noop -- leave the correct updating to the auditor.
    db.address.set (a, adr_type = db.address.get (a, 'adr_type'))
db.commit ()
