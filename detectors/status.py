#! /usr/bin/python
# Copyright (C) 2006-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    status
#
# Purpose
#    Detector for status changes
#
#--
#

from roundup                        import roundupdb, hyperdb
from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

def check_status (db, cl, nodeid, new_values) :
    """ Check that the status transition is OK (if any). If the class
        has a "messages" property, we also require a message on any
        state change (Hmm: we require that the set of attached messages
        changes -- removal of msg together with a state-change is near
        to impossible in the web-interface).
        Added: Container changes don't need a message.
        Added: Containers may do invalid state changes -- checked elsewhere
        Added: Allow transition if status field is unset
    """
    oldstatus = cl.get (nodeid, 'status')
    if "status" in new_values and oldstatus :
        status_cl = db.getclass (cl.properties ['status'].classname)
        n_status  = status_cl.getnode (new_values ['status'])
        o_status  = status_cl.getnode (oldstatus)
        trans_cl  = db.getclass (status_cl.properties ['transitions'].classname)
        extended  = trans_cl is not status_cl
        container = \
            'composed_of' in cl.properties and cl.get (nodeid, 'composed_of')
        if o_status.id == n_status.id :
            return
        if extended :
            is_simple = False
            if 'kind' in cl.properties :
                kid = new_values.get ('kind', cl.get (nodeid, 'kind'))
                if kid :
                    is_simple = db.kind.get (kid, 'simple')
            if is_simple :
                trans = o_status.simple_transitions
            else :
                trans = o_status.transitions
            targets = (trans_cl.getnode (t) for t in trans)
            targets = dict ((t.target, t) for t in targets)
        else :
            targets = o_status.transitions
        if n_status.id not in targets and not container :
            raise Reject \
                ( _ ("Invalid Status transition: %(o_s)s -> %(n_s)s") \
                % dict (o_s = o_status.name, n_s = n_status.name)
                )
        need_msg = True
        if 'relaxed' in status_cl.properties and n_status.relaxed :
            need_msg = False
        if extended and not container :
            old_resp  = cl.get (nodeid, "responsible")
            new_resp  = new_values.get ("responsible", old_resp)
            target    = targets [n_status.id]
            need_msg  = target.require_msg
            if target.require_resp_change and new_resp == old_resp :
                raise Reject \
                    (_ ("Responsible must change for this status change"))
        # No msg for container changes
        if container :
            need_msg = False
        if 'messages' in cl.properties :
            if need_msg and not 'messages' in new_values :
                raise Reject (_ ("State change requires a message"))
# end def check_status

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext

    status_classes = \
        ['it_issue', 'it_project', 'issue'
        , 'doc', 'support', 'leave_submission'
        , 'pr_approval', 'purchase_request'
        ]
    for cl in status_classes :
        if cl not in db.classes :
            continue
        # Allow other auditors to set status before checking
        db.getclass (cl).audit ("set", check_status, priority = 200)
# end def init
