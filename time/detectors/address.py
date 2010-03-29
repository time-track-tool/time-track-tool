# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Ralf Schlatterbeck. All rights reserved
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

from rup_utils                      import translate
from roundup.cgi.TranslationService import get_translation

import common

def fix_adr_type (db, cl, nodeid, new_values) :
    if 'adr_type' in new_values :
        type_cat  = db.adr_type_cat.lookup ('ABO')
        adr_types = db.adr_type.find (typecat = type_cat)
        abos = new_values.get ('abos', None)
        if abos is None and nodeid :
            abos = cl.get (nodeid, 'abos')
        else :
            abos = []
        abos = [db.abo.getnode (a) for a in abos]
        adr_type_dict = dict ([(a, 1) for a in new_values ['adr_type']])
        for t in adr_types :
            if t in adr_type_dict :
                del adr_type_dict [t]
        for abo in abos :
            if not abo ['end'] or abo ['end'] > Date ('.') :
                abotype = db.abo_price.get (abo ['aboprice'], 'abotype')
                adrtype = db.abo_type.get  (abotype, 'adr_type')
                assert (adrtype)
                adr_type_dict [adrtype] = 1
        new_values ['adr_type'] = adr_type_dict.keys ()
# end def fix_adr_type

def fix_contacts (db, cl, nodeid, old_values) :
    if old_values is None or 'contacts' in old_values :
        for c in cl.get (nodeid, 'contacts') :
            d = {cl.classname : nodeid}
            db.contact.set (c, **d)
# end def fix_contacts

def check_retire_address (db, cl, nodeid, old_values) :
        oadr = None
        if old_values :
            oadr = old_values.get ('address')
            nadr = db.person.get (nodeid, 'address')
            if nadr and db.address.is_retired (nadr) :
                db.address.restore (nadr)
        else :
            oadr = cl.get (nodeid, 'address')
        if oadr and not common.persons_for_adr (db, oadr) :
            db.address.retire (oadr)
# end def check_retire_address

def set_adr_defaults (db, cl, nodeid, new_values) :
    """ Set some default values for new address """
    if 'lettertitle' in cl.properties :
        if 'lettertitle' not in new_values  and 'title' in new_values :
            new_values ['lettertitle'] = new_values ['title']
    if 'valid' in cl.properties and 'valid' not in new_values :
            new_values ['valid'] = '1'
    if 'firstname' in cl.properties :
        if (   'initial' not in new_values
           and 'firstname'   in new_values and new_values ['firstname']
           ) :
            new_values ['initial'] = new_values ['firstname'][0].upper () + '.'
    if 'country' in cl.properties and 'country' not in new_values :
        raise Reject, _ (''"Country must be set")
# end def set_adr_defaults

def check_address (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'country')
    common.auto_retire (db, cl, nodeid, new_values, 'contacts')
# end def check_address

def check_person (db, cl, nodeid, new_values) :
    common.auto_retire (db, cl, nodeid, new_values, 'contacts')
# end def check_person

def check_contact (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'contact')
    if nodeid :
        common.require_attributes (_, cl, nodeid, new_values, 'contact_type')
    if not nodeid and 'contact_type' not in new_values :
        ct = db.contact_type.filter (None, {}, sort = [('+', 'order')])
        assert (ct)
        new_values ['contact_type'] = ct [0]
# end def check_contact

def check_function (db, cl, nodeid, new_values) :
    return common.check_attribute_lines (_, new_values, 'function', 2)
# end def check_function

def require_cust_supp (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'cust_supp')
# end def require_cust_supp

def check_retire (db, cl, nodeid, old_values) :
    if cl.get (nodeid, 'cust_supp') is None :
        cl.retire (nodeid)
# end def check_retire

def init (db) :
    if 'address' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.address.audit ("create", set_adr_defaults)
    if 'abo' in db.classes :
        db.address.audit ("create", fix_adr_type)
        db.address.audit ("set",    fix_adr_type)
    db.address.audit ("create", common.lookalike_computation)
    db.address.audit ("set",    common.lookalike_computation)
    if 'person' in db.classes :
        db.person.audit  ("create", require_cust_supp)
        db.person.audit  ("create", common.lookalike_computation)
        db.person.audit  ("set",    common.lookalike_computation)
        db.person.audit  ("create", check_function)
        db.person.audit  ("set",    check_function)
        db.person.audit  ("set",    check_person)
        db.person.audit  ("create", set_adr_defaults)
        db.person.react  ("set",    fix_contacts)
        db.person.react  ("create", fix_contacts)
        db.person.react  ("set",    check_retire_address)
        db.person.react  ("retire", check_retire_address)
        db.person.react  ("set",    check_retire)
    else :
        db.address.audit ("create", check_function)
        db.address.audit ("set",    check_function)
        db.address.react ("set",    fix_contacts)
        db.address.react ("create", fix_contacts)
    db.address.audit ("set",    check_address)
    db.contact.audit ("create", check_contact)
    db.contact.audit ("set",    check_contact)
# end def init
