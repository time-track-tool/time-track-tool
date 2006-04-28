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
#    it
#
# Purpose
#    Detectors for it issues and projects
#
#--
#

from roundup                        import roundupdb, hyperdb
from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation
common = None


def new_it (db, cl, nodeid, new_values) :
    user_has_role = common.user_has_role
    if 'messages'    not in new_values :
        raise Reject, _ ("New %s requires a message") % _ (cl.classname)
    new_values ['status'] = '1'
    if 'category'    not in new_values :
        new_values ['category'] = '1'
    if 'responsible' not in new_values :
        new_values ['responsible'] = db.user.lookup ('helpdesk')
    if 'stakeholder' not in new_values :
        new_values ['stakeholder'] = db.getuid ()
    if 'it_prio'     not in new_values :
        new_values ['it_prio'] = db.it_prio.lookup ('unknown')
    # Don't allow non-it users to create a project
    if cl is db.it_project and not user_has_role (db, db.getuid (), 'IT') :
        raise Reject, _ ('Not allowed to create new %s') % _ ('it_project')
# end def new_it

def check_it (db, cl, nodeid, new_values) :
    for i in 'title', 'category', 'status', 'it_prio', 'responsible' :
        if i in new_values and not new_values [i] :
            raise Reject, _ ("%(attr)s may not be undefined") % {'attr' : _ (i)}
    if new_values.get ('responsible', None) == db.user.lookup ('helpdesk') :
        raise Reject, _ ("User may not be set to helpdesk")

    if not common.user_has_role (db, db.getuid (), 'IT') :
        allowed = {'messages' : 1, 'nosy' : 1, 'files' : 1}
        # Don't use iterkeys () here, we change the dict.
        for prop in new_values.keys () :
            if prop == 'title' :
                del new_values ['title']
            elif prop not in allowed :
                raise Reject, _ ('Not allowed to edit %(prop)s' % locals ())
    if 'status' in new_values :
        rsp  = new_values.get ('responsible', cl.get (nodeid, 'responsible'))
        if rsp  == db.user.lookup ('helpdesk') :
            raise Reject, _ ('Must change user, "helpdesk" is not allowed')
        prio = new_values.get ('it_prio',     cl.get (nodeid, 'it_prio'))
        if prio == db.it_prio.lookup ('unknown') :
            raise Reject, _ ('Must change %s, "unknown" is not allowed') \
                % _ ('it_prio')
# end def new_it

def audit_superseder (db, cl, nodeid, new_values) :
    """
      * ensure that we do not set superseder on a new item
      * ensure that superseder gets not set to itself
      * automatically set status to closed
    """
    new_sup = new_values.get ("superseder", None)
    if new_sup :
        if not nodeid :
            raise Reject, _ ("May not set %s on new issue") % _ ('superseder')
        for sup in new_sup :
            if sup == nodeid :
                raise Reject, _ ("Can't set %s to yourself") % _ ('superseder')
        new_values ["status"] = db.it_issue_status.lookup ('closed')
# end def audit_superseder

def init (db) :
    global _, common
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    import common
    for cls in db.it_issue, db.it_project :
        cls.audit     ("create", new_it, priority = 50)
        cls.audit     ("set",    check_it)
    db.it_issue.audit ("create", audit_superseder)
    db.it_issue.audit ("set",    audit_superseder)
# end def init
