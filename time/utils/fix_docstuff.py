#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
import re
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()

tracker = instance.open (dir)
db      = tracker.open ('admin')

name_txt  = "[0-9a-zA-Z/]+"
name_re   = re.compile ("^%s$" % name_txt)

for id in db.department.getnodeids (retired = False) :
    name = db.department.get (id, 'doc_num')
    if name and not name_re.match (name) :
        print >> sys.stderr, "Wrong name for department %s: %s" % (id, name)
for cl in db.product_type, db.reference, db.artefact :
    for id in cl.getnodeids (retired = False) :
        name = cl.get (id, 'name')
        if not name :
            print >> sys.stderr, "Wrong name (empty or None) for %s %s" \
                % (cl.classname, id)
            continue
        if not name_re.match (name) :
            print >> sys.stderr, \
                "Wrong name for %s %s: %s" % (cl.classname, id, name)

stati = {}
for id in db.doc_status.getnodeids () :
    n = db.doc_status.getnode (id)
    stati [n.name] = id
in_progress = stati ['work in progress']
for id in db.doc.getnodeids (retired = False) :
    owner = db.doc.get (id, 'owner')
    resp  = db.doc.get (id, 'responsible')
    if owner and not resp :
        db.doc.set (id, responsible = owner)
    if not db.doc.get (id, 'status') :
        db.doc.set (id, status = in_progress)
obs = stati ['obsolete']
for name, id in stati.iteritems () :
    if name == 'work in progress' :
        db.doc_status.set (id, transitions = [stati ['draft'], obs])
    elif name == 'draft' :
        db.doc_status.set (id, transitions = [stati ['released'], obs])
    elif name == 'released' :
        db.doc_status.set (id, transitions = [obs])
    elif name == 'obsolete' :
        db.doc_status.set (id, transitions = [stati ['work in progress']])

db.commit ()

