#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************

import time
from   roundup import roundupdb

def union (* lists) :
    """Compute the union of lists.
       >>> sorted (union (['a', 'b', 'c'], ['0', 'b', 'c', 'd', 'e']))
       ['0', 'a', 'b', 'c', 'd', 'e']
    """
    tab = {}
    for l in lists :
        tab.update ((x, 1) for x in l)
    return sorted (tab.keys ())
# end def union

def update_composed_of (db, cl, nodeid, oldvalues) :
    """Update the `composed_of` field of the issues to which this issue
       refers to in its `part_of` field.
    """
    container = cl.get (nodeid, "part_of")
    if container :
        old_parts = sorted (cl.get (container, "composed_of"))
        new_parts = union (old_parts, [str(nodeid)])
        # only set if parts really have changed
        if old_parts != new_parts :
            cl.set (container, composed_of = new_parts)
# end def update_composed_of

def join_nosy_lists (db, cl, nodeid, oldvalues) :
    """Update the nosy list of the superseders with the nosy list of
       this issue.
    """
    oss = oldvalues.get ('superseder', None)
    nss = cl.get (nodeid, 'superseder')
    if nss and oss != nss :
        my_nosy     = cl.get (nodeid, "nosy")
        for ss in nss :
            ss_nosy_old = sorted (cl.get (ss, "nosy"))
            ss_nosy_new = union (ss_nosy_old, my_nosy)
            # only set if list really has changed
            if ss_nosy_old != ss_nosy_new :
                cl.set (ss, nosy = ss_nosy_new)
# end def join_nosy_lists

def init (db) :
    if 'issue' in db.classes :
        if 'composed_of' in db.issue.properties :
            db.issue.react    ("create", update_composed_of, priority = 50)
            db.issue.react    ("set",    update_composed_of, priority = 50)
        db.issue.react    ("set",    join_nosy_lists,    priority = 50)
    if 'it_issue' in db.classes :
        db.it_issue.react ("set", join_nosy_lists,   priority = 50)
        if 'composed_of' in db.it_issue.properties :
            db.it_issue.react ("create", update_composed_of, priority = 50)
            db.it_issue.react ("set",    update_composed_of, priority = 50)
# end def init
