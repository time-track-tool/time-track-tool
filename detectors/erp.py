#! /usr/bin/python
# Copyright (C) 2007 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#++
# Name
#    discount_group
#
# Purpose
#    Detectors for 'discount_group'
#

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

import common

def check_group_discount (db, new_values) :
    if 'group_discount' not in new_values :
        return
    grp  = _ (''"product_group")
    seen = {}
    for gdid in new_values ['group_discount'] :
        gd = db.group_discount.getnode (gdid)
        for a in 'product_group', 'discount' :
            attr = _ (a)
            if gd [a] is None :
                raise Reject, _ (""'%(attr)s must be specified') % locals ()
        pg = gd.product_group
        groupname = db.product_group.get (pg, 'name')
        if pg in seen :
            raise Reject, _ (""'Duplicate %(grp)s "%(groupname)s"') % locals ()
        seen [pg] = True
# end def check_group_discount

def check_overall_discount (db, new_values) :
    if 'overall_discount' not in new_values :
        return
    ods = [db.overall_discount.getnode (i)
           for i in new_values ['overall_discount']
          ]
    ods.sort (key = lambda od : (od.price, od.discount))
    last = None
    for od in ods :
        if last and (od.price <= last.price or od.discount <= last.discount) :
            pd = "%s: %s%% / %s: %s%%" \
                % (last.price, last.discount, od.price, od.discount)
            raise Reject, _ (''"price/discount must be increasing: %(pd)s") \
                % locals ()
        last = od
# end def check_overall_discount

def check_discount_group (db, cl, nodeid, new_values) :
    common.require_attributes (cl, nodeid, new_values, 'currency')
    check_group_discount   (db, new_values)
    check_overall_discount (db, new_values)
    common.auto_retire (db, cl, nodeid, new_values, 'group_discount')
    common.auto_retire (db, cl, nodeid, new_values, 'overall_discount')
# end def check_discount_group

def new_discount_group (db, cl, nodeid, new_values) :
    check_group_discount   (db, new_values)
    check_overall_discount (db, new_values)
# end def new_discount_group

def check_bank_account (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'bank')
# end def check_bank_account

def new_product_price (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'price', 'currency')
# end def new_product_price

def check_product_price (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'price', 'currency')
    if  (   'currency' in new_values
        and cl.get (nodeid, 'currency') != new_values ['currency']
        ) :
        attr = _ ('currency')
        raise Reject, _ ("%(attr)s must not be changed") % locals ()
# end def check_product_price

def check_product (db, cl, nodeid, new_values) :
    if nodeid :
        common.auto_retire (db, cl, nodeid, new_values, 'product_price')
    else :
        common.default_status (new_values, db.product_status)
# end def check_product

def init (db) :
    if 'discount_group' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.discount_group.audit  ("set",    check_discount_group)
    db.bank_account.audit    ("create", check_bank_account)
    db.bank_account.audit    ("set",    check_bank_account)
    db.product_price.audit   ("create", new_product_price)
    db.product_price.audit   ("set",    check_product_price)
    db.product.audit         ("create", check_product)
    db.product.audit         ("set",    check_product)
# end def init

### __END__ time_wp
