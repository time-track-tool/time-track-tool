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

from UserDict                       import UserDict
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

def fix_is_valid (db, cl, nodeid, new_values) :
    if 'is_valid' not in new_values :
        new_values ['is_valid'] = True
# end def fix_is_valid

class adict (UserDict) :
    def __getattr__ (self, key) :
        if key in self :
            return self [key]
        raise AttributeError, key
    # end def __getattr__
# end class adict

def check_open_hours (db, cl, nodeid, new_values) :
    if not nodeid :
        if 'from_minute' not in new_values :
            new_values ['from_minute'] = 0
        if 'to_minute' not in new_values :
            new_values ['to_minute'] = 0
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'from_hour', 'from_minute', 'to_hour', 'to_minute', 'weekday'
        )
    common.check_attribute_range \
        (_, new_values, 0, 59, 'from_minute', 'to_minute')
    common.check_attribute_range \
        (_, new_values, 0, 23, 'from_hour',   'to_hour')
    if nodeid and adrclass :
        adr = adrclass.filter (None, dict (opening_hours = nodeid))
        assert len (adr) <= 1
        if len (adr) :
            wd  = new_values.get \
                ('weekday', db.opening_hours.get (nodeid, 'weekday'))
            oh1 = adict ()
            for k in 'from_hour', 'from_minute', 'to_hour', 'to_minute' :
                oh1 [k] = new_values.get (k, cl.get (nodeid, k))
            for ohid in adrclass.get (adr [0], 'opening_hours') :
                if ohid == nodeid :
                    continue
                oh = db.opening_hours.getnode (ohid)
                if wd == oh.weekday :
                    check_oh_overlap (db, wd, oh1, oh)
# end def check_open_hours

def retire_unlinked_opening_hours (db, cl, nodeid, new_values) :
    if 'opening_hours' in new_values :
        op = new_values ['opening_hours']
        old_op = cl.get (nodeid, 'opening_hours')
        opd  = dict.fromkeys (op)
        # retire missing:
        for op in old_op :
            if op not in opd :
                db.opening_hours.retire (op)
# end def retire_unlinked_opening_hours

def check_oh_overlap (db, wd, oh1, oh2) :
    mf1 = oh1.from_hour * 60 + oh1.from_minute
    mt1 = oh1.to_hour   * 60 + oh1.to_minute
    mf2 = oh2.from_hour * 60 + oh2.from_minute
    mt2 = oh2.to_hour   * 60 + oh2.to_minute
    if (mf1 <= mf2 < mt1 or mf2 <= mf1 < mt2) :
        weekday = db.weekday.get (wd, 'name')
        oh1fh = oh1.from_hour
        oh1fm = oh1.from_minute
        oh1th = oh1.to_hour
        oh1tm = oh1.to_minute
        oh2fh = oh2.from_hour
        oh2fm = oh2.from_minute
        oh2th = oh2.to_hour
        oh2tm = oh2.to_minute
        raise Reject, _(''
            "%(oh1fh)2d:%(oh1fm)02d-%(oh1th)2d:%(oh1tm)02d /"
            "%(oh2fh)2d:%(oh2fm)02d-%(oh2th)2d:%(oh2tm)02d "
            "overlap for %(weekday)s"
            ) % locals ()
# end def check_oh_overlap

def check_open_hours_for_adr (db, cl, nodeid, new_values) :
    op = []
    if 'opening_hours' in new_values :
        op = new_values ['opening_hours']
    elif nodeid :
        op = cl.get (nodeid, 'opening_hours')
    op = [db.opening_hours.getnode (i) for i in op]
    by_weekday = {}
    for oh in op :
        if oh.weekday not in by_weekday :
            by_weekday [oh.weekday] = []
        by_weekday [oh.weekday].append (oh)
    # overlap check
    for wd, op in by_weekday.iteritems () :
        for n, oh1 in enumerate (op) :
            for i in xrange (n + 1, len (op)) :
                check_oh_overlap (db, wd, oh1, op [i])
# end def check_open_hours_for_adr

def init (db) :
    global _, adrclass
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext

    adrclass = persclass = None
    if 'address' in db.classes :
        adrclass  = persclass = db.address
    if 'person' in db.classes :
        persclass = db.person
    if 'customer' in db.classes :
        adrclass  = persclass = db.customer
        adrclass.audit   ("create", fix_is_valid)

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
    if 'opening_hours' in db.classes :
        db.opening_hours.audit ("create", check_open_hours)
        db.opening_hours.audit ("set",    check_open_hours)
        if adrclass :
            adrclass.audit ("set",    retire_unlinked_opening_hours)
            adrclass.audit ("create", check_open_hours_for_adr)
            adrclass.audit ("set",    check_open_hours_for_adr)
# end def init
