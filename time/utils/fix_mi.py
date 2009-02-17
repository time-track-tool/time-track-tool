#!/usr/bin/python2.4
# -*- coding: iso-8859-1 -*-
import os
import sys
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
tracker = instance.open (os.getcwd ())
db      = tracker.open ('admin')

# loop over all issues in several passes and fix maturity_index

id_depends = {}
cache      = {}

for id in db.issue.getnodeids () :
    n = db.issue.getnode (id)
    cache [id] = n
    id_depends [id] = dict.fromkeys (n.composed_of)
while id_depends :
    to_delete = []
    for id, deps in id_depends.iteritems () :
        if not deps :
            n = cache [id]
            print "%s->%s" % (id, n.part_of)
            to_delete.append (id)
            if n.part_of :
                del id_depends [n.part_of][id]
    if not to_delete :
        print "Ooops:", id_depends
    assert (to_delete)
    for id in to_delete :
        del id_depends [id]
