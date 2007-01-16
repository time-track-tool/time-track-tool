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

from roundup.exceptions import Reject
from roundup.date       import Date
from roundup.rup_utils  import translate

def fix_adr_type (db, cl, nodeid, new_values) :
    if 'adr_type' in new_values :
        type_cat  = db.adr_type_cat.lookup ('ABO')
        adr_types = db.adr_type.find (typecat = type_cat)
        abos = new_values.get ('abos', None)
        if abos is None and nodeid :
            abos = cl.get (nodeid, 'abos')
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
# end def check_adr_type

def set_adr_defaults (db, cl, nodeid, new_values) :
    """ Set some default values for new address """
    if 'lettertitle' not in new_values  and 'title' in new_values :
        new_values ['lettertitle'] = new_values ['title']
    if 'valid' not in new_values :
        new_values ['valid'] = '1'
    if (   'initial' not in new_values
       and 'firstname'   in new_values and new_values ['firstname']
       ) :
        new_values ['initial'] = new_values ['firstname'][0].upper () + '.'
    if 'country' not in new_values :
        raise Reject, _ (''"Country must be set")
# end def set_adr_defaults

def check_missing (db, cl, nodeid, new_values) :
    if 'country' in new_values and not new_values ['country'] :
        raise Reject, _ (''"Country must be set")
# end def check_missing

def lookalike_computation (db, cl, nodeid, new_values) :
    if 'firstname' in new_values or 'lastname' in new_values :
        new_values ['lookalike_name'] = translate (firstname + ' ' + lastname)
# end def lookalike_computation

def init (db) :
    db.address.audit ("create", set_adr_defaults)
    db.address.audit ("create", fix_adr_type)
    db.address.audit ("set",    fix_adr_type)
    db.address.audit ("create", lookalike_computation)
    db.address.audit ("set",    lookalike_computation)
    db.address.audit ("set",    check_missing)
# end def init
