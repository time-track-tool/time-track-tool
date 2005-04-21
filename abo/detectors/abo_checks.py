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

from time              import localtime
from roundup.rup_utils import uni, pretty
from roundup.date      import Date, Interval

Reject = ValueError

def set_defaults (db, cl, nodeid, new_values) :
    print "start of set_defaults"
    for i in ('aboprice', 'subscriber') :
        if not new_values.has_key (i) :
            raise Reject, uni('"%s" muss ausgefüllt werden') % pretty (i)
    for i in ('invoices',) :
        if new_values.has_key (i) :
            raise Reject, uni ('"%s" darf nicht ausgefüllt werden') % pretty (i)
    if not new_values.has_key ('amount') :
        new_values ['amount'] = \
            db.abo_price.get (new_values ['aboprice'], 'amount')
    # if no begin-date is specified, use start of next month
    # or today if the start of month is today.
    if not new_values.has_key ('begin') :
        year, month, day = localtime ()[:3]
        if day != 1 :
            day    = 1
            month += 1
            if month > 12 :
                month = 1
                year += 1
        new_values ['begin'] = Date ('%d-%d-%d' % (year, month, day))
    if not new_values.has_key ('payer') :
        new_values ['payer'] = new_values ['subscriber']
    print "end of set_defaults"
# end def set_defaults

def create_invoice (db, cl, nodeid, oldvalues) :
    print 'create_invoice', nodeid
    db.invoice.create (abo = nodeid)
    print 'after create_invoice'
# end def create_invoice

def update_address (db, cl, nodeid, oldvalues) :
    for lattr, rattr in (('payer', 'payed_abos'), ('subscriber', 'abos')) :
        adr_id = cl.get (nodeid, lattr)
        adr    = db.address.getnode (adr_id)
        l      = adr [rattr] or []
        l.append (nodeid)
        db.address.set (adr_id, ** {rattr : l})
# end def update_address

def init (db) :
    db.abo.audit ("create", set_defaults)
    db.abo.react ("create", update_address)
    db.abo.react ("create", create_invoice)
# end def init
