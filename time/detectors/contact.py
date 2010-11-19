# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Ralf Schlatterbeck. All rights reserved
# Reichergasse 131, A-3411 Weidling
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
from roundup.date                   import Date

from roundup.cgi.TranslationService import get_translation

import common

def fix_contacts (db, cl, nodeid, old_values, cls = 'contact') :
    if old_values is None or 'contacts' in old_values :
        for c in cl.get (nodeid, 'contacts') :
            d = {cl.classname : nodeid}
            db.getclass (cls).set (c, **d)
# end def fix_contacts

def fix_user_contacts (db, cl, nodeid, old_values) :
    fix_contacts (db, cl, nodeid, old_values, cls = 'user_contact')
# end def fix_user_contacts

def create_email_contacts (db, cl, nodeid, new_values) :
    email_type = db.uc_type.lookup ('Email')
    ctct = new_values.get ('contacts', [])
    if 'address' in new_values :
        x = db.user_contact.create \
            ( contact      = new_values ['address']
            , contact_type = email_type
            , order        = 0
            , visible      = True
            )
        ctct.append (x)
    if 'alternate_addresses' in new_values :
        for n, a in enumerate (new_values ['alternate_addresses'].split ('\n')) :
            a = a.strip ()
            if not a :
                continue
            x = db.user_contact.create \
                ( contact      = a
                , contact_type = email_type
                , order        = n + 1
                , visible      = True
                )
            ctct.append (x)
    new_values ['contacts'] = ctct
    print "create_email_contacts:", new_values
# end def create_email_contacts

def fix_emails (db, cl, nodeid, new_values) :
    if 'contacts' not in new_values :
        return
    email_type = db.uc_type.lookup ('Email')
    emails = []
    for c in new_values ['contacts'] :
        if db.user_contact.get (c, 'contact_type') == email_type :
            emails.append (db.user_contact.getnode (c))
    alternate = []
    for n, e in enumerate (sorted (emails, key = lambda x : x.order)) :
        if n :
            alternate.append (e.contact)
        else :
            new_values ['address'] = e.contact
        print e.contact
    new_values ['alternate_addresses'] = '\n'.join (alternate)
# end def fix_emails

def auto_retire_contacts (db, cl, nodeid, new_values) :
    common.auto_retire (db, cl, nodeid, new_values, 'contacts')
# end def auto_retire_contacts

def check_contact (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'contact')
    if nodeid :
        common.require_attributes (_, cl, nodeid, new_values, 'contact_type')
    if not nodeid and 'contact_type' not in new_values :
        ct = db.contact_type.filter (None, {}, sort = [('+', 'order')])
        assert (ct)
        new_values ['contact_type'] = ct [0]
# end def check_contact

def new_user_contact (db, cl, nodeid, new_values) :
    if 'visible' not in new_values :
        ct = db.uc_type.getnode (new_values ['contact_type'])
        new_values ['visible'] = ct.visible
# end def new_user_contact

def check_email (db, cl, nodeid, new_values) :
    if 'name' in new_values and cl.get (nodeid, 'name') == 'Email' :
        raise reject, _ ("Name Email must not be changed")
# end def check_email

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext

    persclass = None
    if 'address' in db.classes :
        persclass = db.address
    if 'person' in db.classes :
        persclass = db.person
    if 'customer' in db.classes :
        persclass = db.customer

    if persclass :
        persclass.audit  ("set",    auto_retire_contacts)
        persclass.react  ("set",    fix_contacts)
        persclass.react  ("create", fix_contacts)
    if 'contacts' in db.user.properties :
        db.user.audit    ("set",    auto_retire_contacts)
        db.user.react    ("set",    fix_user_contacts)
        db.user.react    ("create", fix_user_contacts)
        db.user.audit    ("create", fix_emails, priority = 120)
        db.user.audit    ("set",    fix_emails, priority = 120)
        db.user.audit    ("create", create_email_contacts)
    if 'room' in db.classes and 'contacts' in db.room.properties :
        db.room.audit    ("set",    auto_retire_contacts)
        db.room.react    ("set",    fix_user_contacts)
        db.room.react    ("create", fix_user_contacts)
    if 'contact' in db.classes :
        db.contact.audit ("create", check_contact)
        db.contact.audit ("set",    check_contact)
    if 'user_contact' in db.classes :
        db.user_contact.audit ("create", check_contact)
        db.user_contact.audit ("create", new_user_contact, priority = 150)
        db.user_contact.audit ("set",    check_contact)
    if 'uc_type' in db.classes :
        db.uc_type.audit ("set", check_email)
# end def init
