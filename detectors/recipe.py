# Copyright (C) 2021 Ralf Schlatterbeck. All rights reserved
# Reichergasse 131, A-3411 Weidling
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

from roundup.exceptions             import Reject
import common

prime_increment = 9923
maxnum = 10000
def set_defaults (db, cl, nodeid, new_values) :
    """ We assign a number modulo maxnum which is a multiple of a large
        prime (or at least a number relative prime to maxnum). The hope
        is that the last-created rc_product is also the last used such
        number.
    """
    lastid = db.rc_product.filter \
        (None, {}, sort = ('-', 'creation'), limit = 1)
    if lastid :
        number = int (cl.get (lastid [0], 'number'))
        number = (number + prime_increment) % maxnum
    else :
        number = prime_increment
    try :
        while db.rc_product.lookup (str (number)) :
            number = (number + prime_increment) % maxnum
    except KeyError :
        pass
    num = new_values.get ('number', '-')
    assert num == '-'
    new_values ['number'] = "%04d" % number
    common.require_attributes \
        ( db.i18n.gettext, cl, nodeid, new_values
        , 'rc_brand', 'rc_product_type', 'substance', 'number'
        )
# end def set_defaults

def check_product (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'rc_brand', 'rc_product_type', 'substance', 'number'
        )
    if 'number' in new_values :
        num = new_values ['number']
        try :
            n = int (num)
        except ValueError :
            raise Reject (_ ('Product number must be numeric, got "%s"') % num)
# end def check_product

def require_ingr (db, cl, nodeid, new_values) :
    common.require_attributes \
        ( db.i18n.gettext, cl, nodeid, new_values
        , 'substance', 'ingredient', 'quantity'
        )
# end def require_ingr

def subst_default (db, cl, nodeid, new_values) :
    if 'is_raw_material' not in new_values :
        new_values ['is_raw_material'] = True
    common.require_attributes \
        (db.i18n.gettext, cl, nodeid, new_values, 'name')
# end def subst_default

def require_subst (db, cl, nodeid, new_values) :
    common.require_attributes \
        (db.i18n.gettext, cl, nodeid, new_values, 'name')
    subst = cl.getnode (nodeid)
    raw = new_values.get ('is_raw_material', subst.is_raw_material)
    if raw and subst.ingredients :
        new_values ['is_raw_material'] = False
# end def require_subst

def init (db) :
    if 'substance' not in db.classes :
        return
    ingr = db.ingredient_used_by_substance
    db.rc_product.audit   ("create", set_defaults)
    db.rc_product.audit   ("set",    check_product)
    db.substance.audit    ("create", subst_default)
    db.substance.audit    ("set",    require_subst)
    ingr.audit            ("create", require_ingr)
    ingr.audit            ("set",    require_ingr)
# end def init
