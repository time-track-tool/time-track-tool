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
from roundup.date                   import Date, Interval
from roundup.cgi.TranslationService import get_translation
from common                         import auto_retire, require_attributes

_ = lambda x : x

def update_customer (db, cl, nodeid, new_values) :
    auto_retire (db, cl, nodeid, new_values, 'bank_account')
    invoice_address = new_values.get \
        ('invoice_address', cl.get (nodeid, 'invoice_address'))
    if 'shipping_address' in new_values :
        if not invoice_address :
            invoice_address = new_values ['shipping_address']
            new_values ['invoice_address'] = invoice_address
# end def update_customer

def new_customer (db, cl, nodeid, new_values) :
    require_attributes (_, cl, nodeid, new_values, 'customer_group')
    customer_group = new_values ['customer_group']
    if 'discount_group' not in new_values :
        new_values ['discount_group'] = db.customer_group.get \
            (customer_group, 'discount_group')
# end def new_customer

def init (db) :
    if 'customer' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.customer.audit ("set",    update_customer)
    db.customer.audit ("create", new_customer)
# end def init
