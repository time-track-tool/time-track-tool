#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
from common                         import user_has_role
from roundup.date                   import Date

def new_it (db, cl, nodeid, new_values) :
    if 'messages'    not in new_values :
        raise Reject, _ ("New %s requires a message") % _ (cl.classname)
    if  (  'status' not in new_values
        or not user_has_role (db, db.getuid (), 'IT')
        ) :
        new_values ['status'] = '1'
    if 'category'     not in new_values :
        new_values ['category'] = '1'
    if 'responsible'  not in new_values :
        new_values ['responsible'] = db.user.lookup ('helpdesk')
    if 'stakeholder'  not in new_values :
        new_values ['stakeholder'] = db.getuid ()
    if 'it_prio'      not in new_values :
        new_values ['it_prio'] = db.it_prio.lookup ('unknown')
    if 'confidential' not in new_values :
        new_values ['confidential'] = 1
    # Always make new issues confidential.
    new_values ['confidential'] = True
    # Defaults for some attributes only in it_issue
    # We chose the item with lowest order as default
    for attr in 'int_prio', 'it_request_type' :
        if attr in cl.properties and attr not in new_values :
            cls = db.getclass (cl.properties [attr].classname)
            values = cls.filter (None, {}, [('+', 'order')])
            if values :
                new_values [attr] = values [0]
# end def new_it

def check_it (db, cl, nodeid, new_values) :
    for i in 'title', 'category', 'status', 'it_prio', 'responsible' :
        if i in new_values and not new_values [i] :
            raise Reject, _ ("%(attr)s may not be undefined") % {'attr' : _ (i)}
    if new_values.get ('responsible', None) == db.user.lookup ('helpdesk') :
        raise Reject, _ ("User may not be set to helpdesk")

    if 'status' in new_values :
	st   = new_values ['status']
	rsp  = new_values.get ('responsible', cl.get (nodeid, 'responsible'))
	if not db.it_issue_status.get (st, 'relaxed') :
	    if rsp  == db.user.lookup ('helpdesk') :
		raise Reject, _ ('Must change user, "helpdesk" is not allowed')
	    prio = new_values.get ('it_prio',     cl.get (nodeid, 'it_prio'))
	    if prio == db.it_prio.lookup ('unknown') :
		raise Reject, _ ('Must change %s, "unknown" is not allowed') \
		    % _ ('it_prio')
# end def check_it

def audit_superseder (db, cl, nodeid, new_values) :
    """
      * ensure that we do not set superseder on a new item
      * ensure that superseder gets not set to itself
      * automatically set status to closed
    """
    new_sup = new_values.get ("superseder", None)
    if new_sup :
        if not nodeid :
            raise Reject (_ ("May not set %s on new issue") % _ ('superseder'))
        for sup in new_sup :
            if sup == nodeid :
                raise Reject \
                    (_ ("Can't set %s to same issue") % _ ('superseder'))
        closed = db.it_issue_status.getnode \
            (db. it_issue_status.lookup ('closed'))
        if not closed.relaxed :
            if 'messages' not in new_values :
                msg = db.msg.create \
                    ( content = "Closing a duplicate"
                    , author  = db.getuid ()
                    , date    = Date ('.')
                    )
                msgs = cl.get (nodeid, 'messages')
                msgs.append (msg)
                new_values ['messages'] = msgs
            rsp = new_values.get ('responsible', cl.get (nodeid, 'responsible'))
            if db.user.get (rsp, 'username') == 'helpdesk' :
                new_values ['responsible'] = db.getuid ()
	    prio = new_values.get ('it_prio',    cl.get (nodeid, 'it_prio'))
	    if prio == db.it_prio.lookup ('unknown') :
                new_values ['it_prio'] = db.it_prio.lookup ('assistance')
        new_values ["status"] = closed.id
# end def audit_superseder

def reopen_on_message (db, cl, nodeid, new_values) :
    """ Re-Open an issue when a message is received
        Note this will reject the message if the user
        is not in role IT due to "stay_closed" below.
    """
    if 'messages' in new_values and 'status' not in new_values :
        ost = cl.get (nodeid, 'status')
        if ost == db.it_issue_status.lookup ('closed') :
            op = db.it_issue_status.lookup ('open')
            new_values ['status'] = op
# end def reopen_on_message

def stay_closed (db, cl, nodeid, new_values) :
    if 'status' in new_values :
        nst = new_values ['status']
        ost = cl.get (nodeid, 'status')
        if nst != ost and ost == db.it_issue_status.lookup ('closed') :
            if not user_has_role (db, db.getuid (), 'IT') :
                raise Reject \
                    ( _ ("This %(it_issue)s is already closed.\n"
                         "Please create a new issue or have it "
                         "reopened via a phone call to IT.\n"
                         "This can also mean you have chosen a subject "
                         "line of your email that matches an old closed "
                         "issue. Please chose another subject in that case."
                        ) % dict (it_issue = _ ('it_issue'))
                    )
# end def stay_closed

def init (db) :
    if 'it_issue' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    for cls in db.it_issue, db.it_project :
        cls.audit     ("create", new_it, priority = 50)
        cls.audit     ("set",    check_it)
    db.it_issue.audit ("create", audit_superseder)
    db.it_issue.audit ("set",    audit_superseder)
    db.it_issue.audit ("set",    reopen_on_message)
    db.it_issue.audit ("set",    stay_closed, priority = 150)
# end def init
