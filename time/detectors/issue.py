#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
# 
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
#
#++
# Name
#    issue
#
# Purpose
#    Detectors for issue -- used to be done in a nightly check, but
#    since we have a parallel database now we can run them immediately.
#
#--
#

from roundup                        import roundupdb, hyperdb
from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation
common = None

def loopchecks (db, cl, nodeid, new_values) :
    for propname in 'superseder', 'part_of', 'needs', 'depends' :
        if propname in new_values :
            value = new_values [propname]
            common.check_loop (_, cl, nodeid, propname, value, 'id')
# end def loopchecks

def forbidden_props (db, cl, nodeid, new_values) :
    for prop in 'superseder', :
        if prop in new_values :
            raise Reject, _ ('New issue may not define "%s"') % _ (prop)
# end def forbidden_props

def update_eff_prio (db, cl, nodeid, new_values) :
    # Default for priority
    if not nodeid :
        new_values ["priority"] = new_values.get ("priority", 0)
    closed = db.status.lookup ('closed')
    if (  'priority'       in new_values
       or 'effective_prio' in new_values
       or 'status'         in new_values
       ) :
        prio = new_values.get ('priority', None)
        if prio is None :
            prio = cl.get (nodeid, 'priority')
        part = new_values.get ('part_of',  None)
        if not part and nodeid :
            part = cl.get (nodeid, 'part_of')
        new_values ['effective_prio'] = prio
        if part :
            pprio = cl.get (part, 'effective_prio')
            if pprio > prio :
                new_values ['effective_prio'] = pprio
        #print "update_eff_prio:", nodeid, new_values ['effective_prio']
# end def update_eff_prio

def update_children (db, cl, nodeid, old_values) :
    if 'effective_prio' in old_values :
        #print "update_children:", old_values ['effective_prio']
        closed = db.status.lookup ('closed')
        for child in cl.get (nodeid, 'composed_of') :
            if cl.get (child, 'status') != closed :
                cl.set (child, effective_prio = 0)
# end def update_children

def update_container_status (db, cl, id, new_values = {}) :
    """ Check status of a container -- if all sub-issues are closed and
        the container is open, we have to update. Same if one sub-issue
        is open and the container is closed.
    """
    closed      = True
    stat_closed = db.status.lookup ('closed')
    stat_open   = db.status.lookup ('open')
    composed_of = \
        (new_values.get ('composed_of', None) or cl.get (id, 'composed_of'))
    if not composed_of :
        return # not a container
    for child in composed_of :
        if cl.get (child, 'status') != stat_closed :
            closed = False
    status = cl.get (id, 'status')
    if status == stat_closed :
        if not closed :
            if new_values :
                new_values ['status'] = stat_open
            else :
                cl.set (id, status = stat_open)
    else :
        if closed :
            if new_values :
                new_values ['status'] = stat_closed
            else :
                cl.set (id, status = stat_closed)
# end def update_container_status

def status_updated (db, cl, nodeid, old_values) :
    parent = cl.get (nodeid, 'part_of')
    if parent and 'status' in old_values :
        update_container_status (db, cl, parent)
# end def status_updated

def composed_of_updated (db, cl, nodeid, new_values) :
    if 'composed_of' in new_values :
        update_container_status (db, cl, nodeid, new_values)
# end def composed_of_updated

def check_container_statuschange (db, cl, nodeid, new_values) :
    composed_of = \
        new_values.get ('composed_of', cl.get (nodeid, 'composed_of'))
    if composed_of and 'status' in new_values :
        raise Reject, _ ("You may not change container status")
# end def check_container_statuschange

def check_part_of (db, cl, nodeid, new_values) :
    if not 'part_of' in new_values :
        return
    obsolete = db.kind.lookup ('Obsolete')
    mistaken = db.kind.lookup ('Mistaken')
    part_of = cl.getnode (new_values ['part_of'])
    if part_of.kind in (mistaken, obsolete) :
        raise Reject, _ ("May not be part of Obsolete or Mistaken container")
# end def check_part_of

def no_autoclose_container (db, cl, nodeid, new_values) :
    """ This won't work anyway if there are issues in the container,
        because auto-closing will fail. Therefore not enabled currently.
        And maybe it's a good feature after all to be able to make a
        container obsolete and prevent that anything can be attached to
        it after the fact.
    """
    if not 'kind' in new_values :
        return
    obsolete = db.kind.lookup ('Obsolete')
    mistaken = db.kind.lookup ('Mistaken')
    if new_values ['kind'] in (mistaken, obsolete) :
        if new_values.get ('composed_of', cl.get (nodeid, 'composed_of')) :
            raise Reject, _ ("Containers may not be Obsolete/Mistaken")
# end def no_autoclose_container

def init (db) :
    if 'issue' not in db.classes :
        return
    global _, common
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    import common
    db.issue.audit ("set",    loopchecks)
    db.issue.audit ("create", loopchecks)
    db.issue.audit ("set",    update_eff_prio)
    db.issue.audit ("create", update_eff_prio)
    db.issue.audit ("create", forbidden_props)
    db.issue.audit ("create", check_part_of)
    db.issue.audit ("set",    check_part_of)
    db.issue.react ("set",    update_children,              priority =  50)
    db.issue.react ("set",    status_updated,               priority =  50)
    db.issue.audit ("set",    composed_of_updated,          priority = 200)
    db.issue.audit ("set",    composed_of_updated,          priority = 200)
    #db.issue.react ("set",    check_container_statuschange, priority =  90)
# end def init
