#! /usr/bin/python
# Copyright (C) 2017 Dr. Ralf Schlatterbeck Open Source Consulting.
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
# Check lenghts of several fields: The limits are mostly from Active
# Directory -- we sync some fields to AD (see lib/ldap_sync.py)

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

import common

def check_proplen (db, cl, nodeid, new_values, limit = 64) :
    pname = cl.getkey ()
    if pname in new_values :
        common.check_prop_len (_, new_values [pname], pname, limit = 64)
# end def check_proplen

def check_proplen_128 (db, cl, nodeid, new_values) :
    return check_proplen (db, cl, nodeid, new_values, 128)
# end def check_proplen_128

def check_contact_len (db, cl, nodeid, new_values) :
    mail = None
    try :
        mail = db.uc_type.lookup ('Email')
    except KeyError :
        pass
    if 'contact' in new_values :
        ct = new_values.get ('contact_type')
        if not ct and nodeid :
            ct = cl.get (nodeid, 'contact_type')
        limit = 64
        if ct and ct == mail :
            limit = 256
        common.check_prop_len \
            (_, new_values ['contact'], 'contact', limit = limit)
# end def check_contact_len

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    if 'department' in db.classes :
        db.department.audit   ("create", check_proplen)
        db.department.audit   ("set",    check_proplen)
    if 'org_location' in db.classes :
        db.org_location.audit ("create", check_proplen)
        db.org_location.audit ("set",    check_proplen)
    if 'room' in db.classes :
        db.room.audit ("create", check_proplen_128)
        db.room.audit ("set",    check_proplen_128)
    if 'user_contact' in db.classes :
        db.user_contact.audit ("create", check_contact_len)
        db.user_contact.audit ("set",    check_contact_len)
# end def init

### __END__ time_project
