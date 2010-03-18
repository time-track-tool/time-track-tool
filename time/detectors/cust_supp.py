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

import operator
from roundup.exceptions             import Reject
from roundup.date                   import Date, Interval
from roundup.cgi.TranslationService import get_translation
import common

_ = lambda x : x

def update_cust_supp (db, cl, nodeid, new_values) :
    common.auto_retire (db, cl, nodeid, new_values, 'bank_account')
    cstat  = new_values.get \
        ('customer_status', cl.get (nodeid, 'customer_status'))
    cvalid = cstat and db.customer_status.get (cstat, 'valid')
    cgroup = new_values.get \
        ('customer_group',  cl.get (nodeid, 'customer_group'))
    dgroup = new_values.get \
        ('discount_group',  cl.get (nodeid, 'discount_group'))
    if cvalid and cgroup and not dgroup :
        new_values ['discount_group'] = db.customer_group.get \
            (customer_group, 'discount_group')
# end def update_cust_supp

def new_cust_supp (db, cl, nodeid, new_values) :
    common.default_status \
        ( new_values
        , db.customer_status
        , status = 'customer_status'
        , valid  = False
        )
    common.default_status \
        ( new_values
        , db.supplier_status
        , status = 'supplier_status'
        , valid  = False
        )
# end def new_cust_supp

def check_name_len (db, cl, nodeid, new_values) :
    return common.check_attribute_lines (_, new_values, 'name', 2)
# end def check_name_len

def init (db) :
    if 'cust_supp' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.cust_supp.audit ("set",    update_cust_supp)
    db.cust_supp.audit ("create", new_cust_supp)
    db.cust_supp.audit ("create", check_name_len)
    db.cust_supp.audit ("set",    check_name_len)
    db.cust_supp.audit ("create", common.lookalike_computation)
    db.cust_supp.audit ("set",    common.lookalike_computation)


# end def init
