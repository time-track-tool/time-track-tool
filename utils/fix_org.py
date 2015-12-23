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

orgs = \
    ( 'TTTech'
    , 'TTTech Chip'
    , 'TTControl GmbH Wien'
    , 'TTControl Srl Brixen'
    , 'TTTech USA'
    , 'TTTech Automotive'
    , 'FTS'
    , 'TTTech Germany'
    , 'TTTech Japan KK'
    , 'TTTech Dev Rom'
    )

for org in orgs :
    id = db.organisation.lookup (org)
    db.organisation.set (id, may_purchase = True)

db.commit()
