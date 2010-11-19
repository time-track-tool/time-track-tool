# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-10 Ralf Schlatterbeck. All rights reserved
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
# end def set_adr_defaults

def require_country (db, cl, nodeid, new_values) :
    if not cl.key :
        common.require_attributes (_, cl, nodeid, new_values, 'country')
# end def require_country

def check_function (db, cl, nodeid, new_values) :
    return common.check_attribute_lines (_, new_values, 'function', 2)
# end def check_function

def require_cust_supp (db, cl, nodeid, new_values) :
    if 'cust_supp' in cl.properties :
        common.require_attributes (_, cl, nodeid, new_values, 'cust_supp')
# end def require_cust_supp

def check_retire (db, cl, nodeid, old_values) :
    if 'cust_supp' in cl.properties and cl.get (nodeid, 'cust_supp') is None :
        cl.retire (nodeid)
# end def check_retire

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext

    adrclass = persclass = None
    if 'address' in db.classes :
        adrclass  = persclass = db.address
    if 'person' in db.classes :
        persclass = db.person
    if 'customer' in db.classes :
        adrclass  = persclass = db.customer

    if 'abo' in db.classes and adrclass :
        adrclass.audit   ("create", fix_adr_type)
        adrclass.audit   ("set",    fix_adr_type)
    if adrclass :
        adrclass.audit   ("create", common.lookalike_computation)
        adrclass.audit   ("set",    common.lookalike_computation)
        adrclass.audit   ("create", require_country)
        adrclass.audit   ("set",    require_country)
        adrclass.audit   ("create", set_adr_defaults)
    if persclass and persclass != adrclass :
        persclass.audit  ("create", common.lookalike_computation)
        persclass.audit  ("set",    common.lookalike_computation)
        persclass.audit  ("create", set_adr_defaults)
        persclass.react  ("set",    check_retire_address)
        persclass.react  ("retire", check_retire_address)
    if persclass :
        persclass.audit  ("create", require_cust_supp)
        persclass.audit  ("create", check_function)
        persclass.audit  ("set",    check_function)
        persclass.react  ("set",    check_retire)
# end def init
