#!/usr/bin/python

import csv
import os
from roundup import instance

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

cat_by_doc_num = {}
modified = False
with open ('doc_cat.csv', 'r') as f :
    dr = csv.DictReader (f, delimiter = ';')
    for rec in dr :
        name    = rec ['name']
        doc_num = rec ['doc_num']
        try :
            id = db.doc_category.lookup (name)
        except KeyError :
            id = db.doc_category.create \
                ( name    = name
                , doc_num = doc_num
                )
            modified = True
        cat_by_doc_num [doc_num] = id
# Now loop over all docs and look up the correct doc_category via the
# department and set the doc_category

for did in db.doc.getnodeids (retired = False) :
    doc = db.doc.getnode (did)
    if doc.doc_category :
        continue
    dep = db.department.getnode (doc.department)
    assert dep.doc_num
    doc_cat = cat_by_doc_num [dep.doc_num]
    db.doc.set (did, doc_category = doc_cat)
    modified = True

if modified :
    db.commit ()
