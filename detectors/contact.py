# Copyright (C) 2010-25 Ralf Schlatterbeck. All rights reserved
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

import string
from roundup.exceptions             import Reject
from roundup.date                   import Date
from roundup.hyperdb                import Link

import common
from   libcontact import cid

def get_email_types (db):
    return db.uc_type.filter \
        (None, dict (is_email = True), sort = ('+', 'order'))
# end def get_email_types

def no_email_contacts (db, cl, nodeid, new_values):
    """ Do not allow specification of alternate_addresses when creating
        a new user. Note that 'address' is given during tracker setup
        for the admin user.
    """
    _ = db.i18n.gettext
    common.reject_attributes (_, new_values, 'alternate_addresses')
# end def no_email_contacts

def add_contact (db, cl, nodeid, old_values):
    """ A user may have been created with an address but no contact,
        create contact if this is the case.
    """
    node = cl.getnode (nodeid)
    email_type = get_email_types (db) [0]
    if node.address and not node.contacts:
        db.user_contact.create \
            ( contact      = node.address
            , user         = nodeid
            , contact_type = email_type
            , order        = 1
            )
# end def add_contact

def fix_emails (db, cl, nodeid, new_values):
    email_types = set (get_email_types (db))
    contact = cl.getnode (nodeid)
    if contact.contact_type not in email_types:
        return
    item = db.user.getnode (contact.user)
    
    emails = []
    for c in item.contacts:
        if cl.get (c, 'contact_type') in email_types:
            emails.append (cl.getnode (c))
    alternate = []
    d = {}
    for n, e in enumerate (sorted (emails, key = lambda x : x.order or 0)):
        if n:
            alternate.append (e.contact)
        else:
            d ['address'] = e.contact
    d ['alternate_addresses'] = '\n'.join (alternate)
    db.user.set (item.id, **d)
# end def fix_emails

def check_contact (db, cl, nodeid, new_values):
    if cl.classname == 'user_contact':
        rqprop = 'user'
    else:
        rqprop = _get_persclass (db).classname
    common.require_attributes \
        (db.i18n.gettext, cl, nodeid, new_values, 'contact', rqprop)
    # get correct contact_type class
    tc = db.getclass (cl.properties ['contact_type'].classname)
    if nodeid:
        common.require_attributes \
            (db.i18n.gettext, cl, nodeid, new_values, 'contact_type')
    if not nodeid and 'contact_type' not in new_values:
        ct = tc.filter (None, {}, sort = [('+', 'order')])
        assert (ct)
        new_values ['contact_type'] = ct [0]
    # Make emails lowercase but not for user_contact
    if 'contact' in new_values and cl.classname != 'user_contact':
        ct = new_values.get ('contact_type')
        if not ct:
            ct = cl.get (nodeid, 'contact_type')
        name = tc.get (ct, 'name')
        if 'is_email' in tc.properties:
            if tc.get (ct, 'is_email'):
                new_values ['contact'] = new_values ['contact'].lower ()
        elif name == 'Email':
            new_values ['contact'] = new_values ['contact'].lower ()
# end def check_contact

def retire_callerid (db, cl, nodeid, new_values):
    """ Destroy (yes, really) all callerids linking to us (should be
        only one but this is not checked)
    """
    ids = db.callerid.filter (None, dict (contact = nodeid))
    for id in ids:
        db.callerid.destroy (id)
# end def retire_callerid

def new_callerid (db, cl, nodeid, old_values):
    c  = cl.getnode (nodeid)
    if not db.contact_type.get (c.contact_type, 'use_callerid'):
        return
    ct = cl.get (nodeid, 'contact')
    db.callerid.create (number = cid (db, ct), contact = nodeid)
# end def new_callerid

def fix_callerid (db, cl, nodeid, old_values):
    """ Create callerid information consisting of digits as coming in
        via phone line.
    """
    c   = cl.getnode (nodeid)
    ct  = db.contact_type.getnode (c.contact_type)
    ot  = db.contact_type.getnode (old_values.get ('contact_type', ct.id))
    num = c.contact
    ids = db.callerid.filter (None, dict (contact = nodeid))
    if not ids:
        if ct.use_callerid:
            db.callerid.create (number = cid (db, num), contact = nodeid)
    else:
        assert len (ids) == 1
        id = ids [0]
        if ct.use_callerid:
            db.callerid.set (id, number = cid (db, num), contact = nodeid)
        else:
            db.callerid.destroy (id)
# end def fix_callerid

def changed_contact (db, cl, nodeid, old_values):
    """ Update the user address information if an email changes """
    contact = cl.getnode (nodeid)
    if ('contact' not in old_values and 'contact_type' not in old_values):
        return
    if  (   old_values ['contact']      == contact.contact
        and old_values ['contact_type'] == contact.contact_type
        and old_values ['order']        == contact.order
        ):
        return
    email_types = get_email_types (db)
    if  (   contact.contact_type not in email_types
        and old_values.get ('contact_type') not in email_types
        ):
        return
    common.update_emails (db, contact.user)
# end def changed_contact

def new_user_contact (db, cl, nodeid, new_values):
    if 'visible' not in new_values:
        ct = db.uc_type.getnode (new_values ['contact_type'])
        new_values ['visible'] = ct.visible
# end def new_user_contact

def _get_persclass (db):
    persclass = None
    if 'address' in db.classes:
        persclass = db.address
    if 'person' in db.classes:
        persclass = db.person
    if 'customer' in db.classes:
        persclass = db.customer
    return persclass
# end def _get_persclass

def init (db):
    persclass = _get_persclass (db)
    if 'contact' in db.classes:
        db.contact.audit ("create",  check_contact)
        db.contact.audit ("set",     check_contact)
        if 'callerid' in db.classes:
            db.contact.react ("create", new_callerid, priority = 120)
            db.contact.react ("set",    fix_callerid, priority = 120)
            db.contact.react ("retire", retire_callerid)
    if 'user_contact' in db.classes:
        db.user.audit         ("create",  no_email_contacts)
        db.user.react         ("create",  add_contact)
        db.user_contact.audit ("create",  check_contact)
        db.user_contact.audit ("create",  new_user_contact, priority = 150)
        db.user_contact.audit ("set",     check_contact)
        db.user_contact.react ("set",     changed_contact)
        db.user_contact.react ("create",  fix_emails)
# end def init
