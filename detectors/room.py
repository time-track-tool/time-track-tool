#! /usr/bin/python
# Copyright (C) 2020 Dr. Ralf Schlatterbeck Open Source Consulting.
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

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

import common
try :
    import ldap_sync
except ImportError :
    ldap_sync = None

def check_room (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'location')
    if 'name' in new_values :
        l_id = new_values.get ('location', None)
        if not l_id :
            # No check necessary, we require the location exists above
            l_id = cl.get (nodeid, 'location')
        location = db.location.getnode (l_id)
        pfx = location.room_prefix
        if pfx and not new_values ['name'].startswith (pfx) :
            raise Reject \
                (_ ('Room name must start with prefix "%(pfx)s"') % locals ())
# end def check_room

def check_retire_room (db, cl, nodeid, new_values) :
    """ Check if the room is in use
        Do not allow retire if any user has a link to this room.
        Note that we're searching only for users that have a status !=
        obsolete.
    """
    stati = []
    for sid in db.user_status.getnodeids () :
        if db.user_status.get (sid, 'name') != 'obsolete' :
            stati.append (sid)
    users  = db.user.filter (None, dict (room = nodeid, status = stati))
    if users :
        room = cl.get (nodeid, 'name')
        raise Reject (_ ('Room "%(room)s" is in use') % locals ())
# end def check_retire_room

def sync_room_to_ldap (db, cl, nodeid, old_values) :
    """ Reactor to ldap-sync all users with this room if room name changes
    """
    if 'name' not in old_values :
        return
    oldname = old_values.get ('name')
    newname = cl.get (nodeid, 'name')
    if oldname != newname :
        users = db.user.filter (None, dict (room = nodeid))
        if users :
            ld = ldap_sync.LDAP_Roundup_Sync (db, verbose = 0)
            for u in users :
                user = db.user.getnode (u)
                if user.status not in ld.status_sync :
                    continue
                if user.status == ld.status_obsolete :
                    continue
                ld.sync_user_to_ldap (user.username)
# end def sync_room_to_ldap

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    if 'room' in db.classes :
        db.room.audit   ("create", check_room)
        db.room.audit   ("set",    check_room)
        db.room.audit   ("retire", check_retire_room)
        # Register ldap sync backend only if we're syncing to ldap
        if ldap_sync and ldap_sync.check_ldap_config (db) :
            db.room.react   ("set", sync_room_to_ldap)
# end def init
