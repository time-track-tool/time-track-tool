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
        valid   = bool (int (rec ['valid']))
        ids     = db.doc_category.filter (None, dict (doc_num = doc_num))
        if ids :
            assert len (ids) == 1
            id = ids [0]
            node = db.doc_category.getnode (id)
            d = {}
            if node.name != name :
                d ['name'] = name
            if node.valid != valid :
                d ['valid'] = valid
            if d :
                db.doc_category.set (id, ** d)
                modified = True
        else :
            id = db.doc_category.create \
                ( name    = name
                , doc_num = doc_num
                , valid   = valid
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
