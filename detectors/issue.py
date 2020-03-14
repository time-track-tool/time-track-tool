#! /usr/bin/python
# Copyright (C) 2006-14 Dr. Ralf Schlatterbeck Open Source Consulting.
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

import common
from maturity_index                 import maturity_table

def loopchecks (db, cl, nodeid, new_values) :
    for propname in 'superseder', 'part_of', 'needs', 'depends' :
        if propname in cl.properties and propname in new_values :
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
       or 'part_of'        in new_values
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
# end def update_eff_prio

def update_children (db, cl, nodeid, old_values) :
    if  (   'effective_prio' in old_values
        and old_values ['effective_prio'] != cl.get (nodeid, 'effective_prio')
        ) :
        #print "update_children:", old_values ['effective_prio']
        #print "update_children:", cl.get (nodeid, 'effective_prio')
        closed = db.status.lookup ('closed')
        for child in cl.get (nodeid, 'composed_of') :
            if cl.get (child, 'status') != closed :
                cl.set (child, effective_prio = 0)
# end def update_children

def update_container_status (db, cl, id, new_values = {}) :
    """ Check status of a container -- if all sub-issues are closed and
        the container is open, we have to update. Same if one sub-issue
        is open and the container is closed. Or if all sub-isues are
        closed or suspended.
    """
    closed      = True
    suspended   = True
    stat_closed = db.status.lookup ('closed')
    stat_open   = db.status.lookup ('open')
    stat_susp   = db.status.lookup ('suspended')
    composed_of = \
        (new_values.get ('composed_of', None) or cl.get (id, 'composed_of'))
    if not composed_of :
        return # not a container
    for child in composed_of :
        cstatus = cl.get (child, 'status')
        if cstatus != stat_closed :
            closed = False
        if cstatus != stat_closed and cstatus != stat_susp :
            suspended = False
    status = cl.get (id, 'status')
    if closed :
        if False :
            if new_values :
                new_values ['status'] = stat_closed
            else :
                cl.set (id, status = stat_closed)
    elif suspended :
        if new_values :
            new_values ['status'] = stat_susp
        else :
            cl.set (id, status = stat_susp)
    else :
        if new_values :
            new_values ['status'] = stat_open
            if 'closed' in new_values :
                new_values ['closed'] = None
        else :
            cl.set (id, status = stat_open)
# end def update_container_status

def status_updated (db, cl, nodeid, old_values) :
    parent = cl.get (nodeid, 'part_of')
    if  (   parent and 'status' in old_values
        and old_values ['status'] != cl.get (nodeid, 'status')
        ) :
        update_container_status (db, cl, parent)
# end def status_updated

def composed_of_updated (db, cl, nodeid, new_values) :
    if 'composed_of' in new_values or 'status' in new_values :
        update_container_status (db, cl, nodeid, new_values)
# end def composed_of_updated

def check_container_status (db, cl, nodeid, new_values) :
    """ Don't allow closing of container with open issues.
        We only need to check the first level, because
        container-children will not be in status closed if they have
        open children.
    """
    status_cls = db.getclass (cl.properties ['status'].classname)
    closed = status_cls.lookup ('closed')
    open   = status_cls.lookup ('open')
    composed_of = new_values.get ('composed_of', cl.get (nodeid, 'composed_of'))
    if 'status' not in new_values or not composed_of :
        return
    status = new_values ['status']
    if status not in (open, closed) :
        open_n   = status_cls.get (open,   'name')
        closed_n = status_cls.get (closed, 'name')
        raise Reject, _ \
            ("Container status must be %(open_n)s or %(closed_n)s") % locals ()
    if status != closed :
        return
    for child in composed_of :
        if cl.get (child, 'status') != closed :
            raise Reject, _ ("Can't close container with non-closed children")
# end def check_container_status

def check_part_of (db, cl, nodeid, new_values) :
    p_id = new_values.get ('part_of')
    if not p_id and nodeid :
        p_id = cl.get (nodeid, 'part_of')
    if not p_id :
        return
    part_of = cl.getnode (p_id)
    if 'kind' in cl.properties :
        obsolete = db.kind.lookup   ('Obsolete')
        mistaken = db.kind.lookup   ('Mistaken')
        if part_of.kind in (mistaken, obsolete) :
            raise Reject \
                (_ ("May not be part of Obsolete or Mistaken container"))
    status_cls = db.getclass (cl.properties ['status'].classname)
    open   = status_cls.lookup ('open')
    # Allow change of effort_hours and numeric_effort if latter is set
    # to false
    if  (   len (new_values) == 2
        and 'numeric_effort' in new_values
        and 'effort_hours' in new_values
        and new_values ['numeric_effort'] is None
        ) :
        return
    if part_of.status != open :
        raise Reject, _ ("Parent container must be in state open")
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

def set_maturity_index (db, cl, nodeid, new_values, do_update = False) :
    """ Set the maturity index for a node if it was not already present.
        If the maturity_index in new_values is None, we recompute.
        We also recompute if any relevant fields changed or do_update
        ist True (in which case some of the children changed and we were
        called by a reactor)
    """
    mi    = new_values.get ('maturity_index')
    omi   = mi
    co    = new_values.get ('composed_of')
    minor = db.severity.lookup ('Minor')
    kid   = new_values.get ('kind')
    if nodeid :
        if 'composed_of' not in new_values :
            co = cl.get (nodeid, 'composed_of')
        omi = cl.get (nodeid, 'maturity_index')
        if 'maturity_index' not in new_values :
            mi = omi
        if 'kind' not in new_values :
            kid = cl.get (nodeid, 'kind')
    is_simple = False
    if kid :
        kind = db.kind.getnode (kid)
        is_simple = kind.simple
    if  (   mi is None or omi is None
        or 'status' in new_values or 'severity' in new_values
        or 'composed_of' in new_values
        or do_update
        ) :
        if co :
            mi = 0
            for k in co :
                mi += db.issue.get (k, 'maturity_index')
        elif is_simple :
            mi = 0
        else :
            status = new_values.get  ('status')   or cl.get (nodeid, 'status')
            sev    = new_values.get  ('severity') or cl.get (nodeid, 'severity')
            if not sev :
                sev = minor
            status = db.status.get   (status, 'name')
            sev    = db.severity.get (sev, 'name')
            mi     = maturity_table.get ((sev, status), 0)
        new_values ['maturity_index'] = mi
        if do_update :
            cl.set (nodeid, maturity_index = mi)
    return mi
# end def set_maturity_index

def update_maturity_index (db, cl, nodeid, old_values, is_new = False) :
    """ Reactor to update maturity index for all predecessors. We walk
        the predecessor chain, if the maturity_index is undefined, we
        compute it via all the children, otherwise we do a simple update
        with the changed maturity_index of the current node.
    """
    old_values = old_values or {}
    part_of    = cl.get (nodeid, 'part_of')
    opart_of   = old_values.get ('part_of', part_of)
    mi         = cl.get (nodeid, 'maturity_index')
    o_mi       = old_values.get ('maturity_index', 0)
    if  (   is_new
        or  part_of != opart_of
        or  'maturity_index' in old_values
        and old_values ['maturity_index'] != mi
        ) :
        parts = dict.fromkeys ((part_of, opart_of)).keys ()
        for p in parts :
            if p :
                parent_mi = cl.get (p, 'maturity_index')
                force     = part_of != opart_of
                set_maturity_index (db, cl, p, {}, True)
# end def update_maturity_index

def creat_update_maturity_index (db, cl, nodeid, old_values) :
    """ Reactor to update maturity_index -- see update_maturity_index
        which does the real work, we only need information if the node
        was just created or already existed.
    """
    update_maturity_index (db, cl, nodeid, old_values, True)
# end def creat_update_maturity_index

def fix_effort (db, cl, nodeid, new_values) :
    """ If effort is changed and not None, round to nearest int. """
    ne = 'effort_hours'
    if ne in new_values and new_values [ne] is not None :
        new_values [ne] = int (new_values [ne] + .5)
    elif ne not in new_values and nodeid :
        effort = cl.get (nodeid, ne)
        if effort and effort % 1 :
            new_values [ne] = int (effort + .5)
# end def fix_effort

def no_numeric_effort (db, cl, nodeid, new_values) :
    if new_values.get ('numeric_effort', None) is not None :
        raise Reject (_ ("Please use new effort_hours field"))
# end def no_numeric_effort

def doc_issue_status (db, cl, nodeid, new_values) :
    """ Check if doc_issue_status is set, if no we set it to undecided.
        Don't allow to set this to empty.
    """
    n = 'doc_issue_status'
    old = cl.get (nodeid, n)
    if old :
        common.require_attributes (_, cl, nodeid, new_values, n)
    else :
        if n not in new_values or not new_values [n] :
            new_values [n] = db.doc_issue_status.filter \
                (None, {}, sort = [('+', 'order')]) [0]
    if  (n in new_values) :
        di = db.doc_issue_status.getnode (new_values [n])
        if di.need_msg and 'messages' not in new_values :
            raise Reject, _ \
                ("Change of %(doc_issue_status)s requires a message") \
                % {n : _ (n)}
# end def doc_issue_status

def new_doc_issue_status (db, cl, nodeid, new_values) :
    n = 'doc_issue_status'
    if n not in new_values or not new_values [n] :
        new_values [n] = db.doc_issue_status.filter \
            (None, {}, sort = [('+', 'order')]) [0]
# end new_doc_issue_status

def add_ext_company (db, cl, nodeid, new_values) :
    """ Add external company to new issue of a user if the user has one """
    user = db.user.getnode (db.getuid ())
    if 'external_company' not in new_values and user.external_company :
        new_values ['external_company'] = [user.external_company]
# end def add_ext_company

def add_ext_user (db, cl, nodeid, new_values) :
    """ Add user to external_users of new issue if user has role
        External.
    """
    if common.user_has_role (db, db.getuid (), 'External') :
        new_values ['external_users'] = [db.getuid ()]
# end def add_ext_user

def check_ext_user_container (db, cl, nodeid, new_values) :
    """ Check that new responsible of a container isn't an external
        user (role External).
    """
    co = new_values.get ('composed_of', cl.get (nodeid, 'composed_of'))
    u  = new_values.get ('responsible', cl.get (nodeid, 'responsible'))
    if co and common.user_has_role (db, u, 'External') :
        if 'responsible' in new_values :
            raise Reject, _ \
                ("External user may not be responsible for container")
        else :
            raise Reject, _ \
                ("Operation would create a container "
                 "with an external user as owner"
                )
# end def check_ext_user_container

def check_ext_user_part_of (db, cl, nodeid, new_values) :
    if 'part_of' in new_values :
        container = new_values ['part_of']
        if  (not db.security.hasPermission
                ('View', db.getuid (), cl.classname, 'title', container)
            ) :
            raise Reject, _ \
                ("Part of can be set to visible container only")
# end def check_ext_user_part_of

def check_ext_user_responsible (db, cl, nodeid, new_values) :
    if 'responsible' in new_values :
        u = db.user.getnode (new_values ['responsible'])
        x = db.user_status.lookup ('external')
        if u.status == x :
            if 'external_users' in new_values :
                xu = new_values.get ('external_users')
            elif 'nodeid' :
                xu = cl.get (nodeid, 'external_users')
            else :
                xu = []
            xu = dict.fromkeys (xu)
            xu [u.id] = True
            new_values ['external_users'] = xu.keys ()
# end def check_ext_user_responsible

def check_ext_msg (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'ext_tracker', 'ext_id', 'msg')
    new_values ['key'] = ':'.join \
        ((new_values ['ext_tracker'], new_values ['ext_id']))
# end def check_ext_msg

def set_ext_msg (db, cl, nodeid, new_values) :
    common.reject_attributes (_, new_values, 'ext_tracker', 'key', 'ext_id')
# end def set_ext_msg

def check_kpm (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'issue')
    if new_values.get ('ready_for_sync', None) :
        # required fields only for *new* kpm issue. Issues that were
        # synced *from* KPM have these fields marked non-editable.
        iid = new_values.get ('issue')
        if not iid :
            iid = cl.get (nodeid, 'issue')
        kpmtr = db.ext_tracker.lookup ('KPM')
        common.require_attributes (_, db.issue, iid, {}, 'release', 'severity')
        ets = db.ext_tracker_state.filter \
            (None, dict (issue = iid, ext_tracker = kpmtr))
        assert len (ets) <= 1
        if not ets :
            common.require_attributes \
                ( _, cl, nodeid, new_values
                , 'description', 'fault_frequency', 'reproduceable'
                )
# end def check_kpm

def check_ext_tracker_state (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'issue')
# end def check_ext_tracker_state

def inherit_safety_level (db, cl, nodeid, new_values) :
    """ Inherit safety level from container, but only if not yet set
        (i.e. always for new issues)
    """
    if 'safety_level' in new_values :
        return
    if nodeid and cl.get (nodeid, 'safety_level') :
        return
    container = new_values.get ('part_of')
    # New issue with container or container change
    if container :
        new_values ['safety_level'] = cl.get (container, 'safety_level')
# end def inherit_safety_level

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    if 'issue' in db.classes :
        db.issue.audit ("create", forbidden_props)
        if 'safety_level' in db.issue.properties :
            db.issue.audit ("set",    inherit_safety_level)
            db.issue.audit ("create", inherit_safety_level)
        if 'effective_prio' in db.issue.properties :
            db.issue.audit ("set",    update_eff_prio)
            db.issue.audit ("create", update_eff_prio)
        if 'composed_of' in db.issue.properties :
            db.issue.audit ("set",    loopchecks)
            db.issue.audit ("create", loopchecks)
            db.issue.audit ("create", check_part_of)
            db.issue.audit ("set",    check_part_of)
            db.issue.audit ("set",    check_container_status)
            # No longer automagically open/close containers, instead
            # - Don't allow adding issue to closed container
            # - Don't allow re-open of closed issue in closed container
            # - forbit all other operations on issues in closed container
            # - Don't allow closing of container with non-closed issues
            # -> see check_part_of
            if False :
                db.issue.react ("set", status_updated,           priority =  49)
                db.issue.audit ("set", composed_of_updated,      priority = 200)
                db.issue.audit ("set", composed_of_updated,      priority = 200)
            db.issue.react ("set",    update_children,          priority =  50)
        if 'maturity_index' in db.issue.properties :
            db.issue.audit ("set",    set_maturity_index,       priority = 300)
            db.issue.audit ("create", set_maturity_index,       priority = 300)
            db.issue.react ("set",    update_maturity_index)
            db.issue.react ("create", creat_update_maturity_index)
        if 'effort_hours' in db.issue.properties :
            db.issue.audit ("set",    fix_effort)
            db.issue.audit ("create", fix_effort)
            if 'numeric_effort' in db.issue.properties :
                db.issue.audit ("set",    no_numeric_effort, priority = 80)
                db.issue.audit ("create", no_numeric_effort, priority = 80)
        if 'doc_issue_status' in db.issue.properties :
            db.issue.audit ("set",    doc_issue_status,     priority = 110)
            db.issue.audit ("create", new_doc_issue_status, priority = 110)
        if 'external_company' in db.issue.properties :
            db.issue.audit ("create", add_ext_company)
        if 'external_users' in db.issue.properties :
            db.issue.audit ("create", add_ext_user)
            db.issue.audit ("set",    check_ext_user_container)
            db.issue.audit ("create", check_ext_user_part_of)
            db.issue.audit ("set",    check_ext_user_part_of)
            db.issue.audit ("create", check_ext_user_responsible)
            db.issue.audit ("set",    check_ext_user_responsible)
        if 'ext_msg' in db.classes :
            db.ext_msg.audit ("create", check_ext_msg)
            db.ext_msg.audit ("set",    set_ext_msg)
        if 'kpm' in db.classes :
            db.kpm.audit     ("create", check_kpm)
            db.kpm.audit     ("set",    check_kpm)
        if 'ext_tracker_state' in db.classes :
            db.ext_tracker_state.audit ("create", check_ext_tracker_state)
            db.ext_tracker_state.audit ("set",    check_ext_tracker_state)
    if 'it_issue' in db.classes :
        if 'composed_of' in db.it_issue.properties :
            db.it_issue.audit ("set",    loopchecks)
            db.it_issue.audit ("create", loopchecks)
            db.it_issue.audit ("create", check_part_of)
            db.it_issue.audit ("set",    check_part_of)
            db.it_issue.audit ("set",    check_container_status)
# end def init
