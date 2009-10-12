#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import sys
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
tracker = instance.open (os.getcwd ())
db      = tracker.open ('admin')

# loop over all issues in several passes and fix container status

id_depends = {}
cache      = {}

mistaken   = db.kind.lookup ('Mistaken')
obsolete   = db.kind.lookup ('Obsolete')
support    = db.kind.lookup ('Support')
openstatus = db.status.lookup ('open')

for id in db.issue.getnodeids () :
    n = db.issue.getnode (id)
    cache [id] = n
    id_depends [id] = dict.fromkeys (n.composed_of)
while id_depends :
    to_delete = []
    for id, deps in id_depends.iteritems () :
        if not deps :
            n = cache [id]
            if n.composed_of :
                print "%5s: %9s(%8s) ->" % (id, n.status, n.kind),
                if n.kind in (mistaken, obsolete) :
                    db.issue.set (id, kind = support)
                db.issue.set (id, status = openstatus)
                print "%9s" % n.status
            to_delete.append (id)
            if n.part_of :
                del id_depends [n.part_of][id]
    if not to_delete :
        print "Ooops:", id_depends
    assert (to_delete)
    for id in to_delete :
        del id_depends [id]
db.commit ()
