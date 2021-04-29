#!/usr/bin/python

import csv
import os
from roundup import instance

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

modified = False
with open ('doc_cat.csv', 'r') as f :
    dr = csv.DictReader (f, delimiter = ';')
    for rec in dr :
        name = rec ['name']
        try :
            db.doc_category.lookup (name)
        except KeyError :
            db.doc_category.create \
                ( name    = name
                , doc_num = rec ['doc_num']
                )
            modified = True
if modified :
    db.commit ()
