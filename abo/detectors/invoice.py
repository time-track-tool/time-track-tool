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

Reject = ValueError
from roundup.rup_utils import uni, pretty, abo_max_invoice
from roundup.date      import Date, Interval

def new_invoice (db, cl, nodeid, new_values) :
    for i in ('abo', ) :
        if not i in new_values :
            raise Reject, uni ('"%s" muss ausgefüllt werden') % pretty (i)
    abo_id    = new_values.get       ('abo', None)
    abo       = db.abo.getnode       (abo_id)
    abo_price = db.abo_price.getnode (abo ['aboprice'])
    abo_type  = db.abo_type.getnode  (abo_price ['abotype'])
    for i in \
        ( 'balance_open', 'n_sent', 'last_sent', 'payer', 'subscriber'
        , 'date_payed', 'bookentry', 'receipt_no', 'send_it'
        , 'period_start', 'period_end', 'invoice_no', 'payment'
        , 'invoice_group'
        ) :
        if i in new_values :
            raise Reject, uni ('"%s" darf nicht ausgefüllt werden') % pretty (i)
    if 'amount' not in new_values :
        new_values ['amount']   = abo        ['amount']
    if 'currency' not in new_values :
        new_values ['currency'] = abo_price  ['currency']
    new_values ['balance_open'] = new_values ['amount']
    new_values ['payment']      = 0.0
    new_values ['open']         = new_values ['balance_open'] > 0
    new_values ['n_sent']       = 0
    new_values ['payer']        = abo ['payer']
    new_values ['subscriber']   = abo ['subscriber']
    new_values ['send_it']      = False
    if not len (abo ['invoices']) :
        start  = abo ['begin']
    else :
        maxinv = abo_max_invoice (db, abo)
        start  = maxinv ['period_end'] + Interval ('1d')
    end = start + Interval ('%dm' % abo_type ['period'])
    end = end   - Interval ('1d')
    new_values ['period_start'] = start
    new_values ['period_end']   = end
    new_values ['invoice_no']   = "R%s%s" % (abo_id, end.pretty ('%m%y'))
# end def new_invoice

def add_to_abo_payer (db, cl, nodeid, oldvalues) :
    abo_id   = cl.get         (nodeid, 'abo')
    invoices = db.abo.get     (abo_id, 'invoices') or []
    payer    = db.abo.get     (abo_id, 'payer')
    invoices.append           (nodeid)
    db.abo.set                (abo_id, invoices = invoices)
    invoices = db.address.get (payer, 'invoices') or []
    invoices.append           (nodeid)
    db.address.set            (payer, invoices = invoices)
# end def add_to_abo_payer

def check_invoice (db, cl, nodeid, new_values) :
    now = Date ('.')
    for i in \
        ( 'abo', 'invoice_no', 'period_start', 'period_end'
        , 'payer', 'subscriber', 'open', 'receipt_no'
        ) :
        if i in new_values :
            raise Reject, uni ('"%s" darf nicht geändert werden') % pretty (i)
    invoice = db.invoice.getnode (nodeid)
    balance = new_values.get ('balance_open', cl.get (nodeid, 'balance_open'))
    amount  = new_values.get ('amount',       cl.get (nodeid, 'amount'))
    payment = new_values.get ('payment',      cl.get (nodeid, 'payment'))
    date_p  = new_values.get ('date_payed',   cl.get (nodeid, 'date_payed'))
    receipt = new_values.get ('receipt_no',   cl.get (nodeid, 'receipt_no'))
    inv_no  = cl.get (nodeid, 'invoice_no')
    abo     = db.abo.getnode (cl.get (nodeid, 'abo'))
    if abo ['end'] and new_values.keys () != ['invoice_group']:
        raise Reject, uni ('Kein Buchen bei storniertem Abo')
    if balance is None or amount is None or payment is None :
        raise Reject, uni ('"%s", "%s", "%s": nur Zahlen erlaubt') % \
            (pretty ('payment'), pretty ('balance_open'), pretty ('amount'))
    if 'amount' in new_values :
        if cl.get (nodeid, 'payment') > 0 :
            raise Reject, uni ('Betrag darf nicht nach Zahlung geändert werden')
    if 'payment' in new_values and 'balance_open' in new_values :
        if amount - payment != balance :
            raise Reject, uni ('Inkonsistenz von %s:%s und %s:%s') % \
                (pretty ('payment'), payment, pretty ('balance_open'), balance)
    elif 'payment' in new_values :
        new_values ['balance_open'] = amount - payment
    elif 'balance_open' in new_values :
        new_values ['payment']      = amount - balance
    if balance > amount :
        raise Reject, uni ('Zahlung darf Betrag nicht übersteigen')
    # is there too now if only balance changed:
    if 'payment' in new_values :
        new_values ['bookentry'] = now
        if not receipt :
            rnum = inv_no.replace ('R', 'B')
            if rnum [0] != 'B' : rnum = 'b' + rnum
            new_values ['receipt_no'] = rnum
    if not balance :
        new_values ['open'] = False
    else :
        new_values ['open'] = True
    if not balance and not date_p :
        new_values ['date_payed'] = now
# end def check_invoice

def create_new_invoice (db, cl, nodeid, oldvalues) :
    abo_id = cl.get (nodeid, 'abo')
    abo    = db.abo.getnode (abo_id)
    if 'open' in oldvalues and not cl.get (nodeid, 'open') :
        invoice = abo_max_invoice (db, abo)
        if not invoice ['open'] :
            db.invoice.create (abo = abo_id)
# end def create_new_invoice

def init (db) :
    db.invoice.audit ("create", new_invoice)
    db.invoice.react ("create", add_to_abo_payer)
    db.invoice.audit ("set",    check_invoice)
    db.invoice.react ("set",    create_new_invoice)
# end def init
#SHA: 70083841a9880545aa67478d9946b11f2b7aa127
