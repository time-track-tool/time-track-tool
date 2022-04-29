# Copyright (C) 2004-21 Ralf Schlatterbeck. All rights reserved
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
from rup_utils                      import abo_max_invoice
import common

def new_invoice (db, cl, nodeid, new_values) :
    common.require_attributes (db.i18n.gettext, cl, nodeid, new_values, 'abo')
    abo_id    = new_values.get       ('abo', None)
    abo       = db.abo.getnode       (abo_id)
    abo_price = db.abo_price.getnode (abo ['aboprice'])
    abo_type  = db.abo_type.getnode  (abo_price ['abotype'])
    common.reject_attributes \
        ( db.i18n.gettext
        , new_values
        , 'balance_open'
        , 'n_sent'
        , 'last_sent'
        , 'payer'
        , 'subscriber'
        , 'send_it'
        , 'period_start'
        , 'period_end'
        , 'invoice_no'
        , 'payment'
        , 'invoice_group'
        )
    if 'amount' not in new_values :
        new_values ['amount']   = abo        ['amount']
    if 'currency' not in new_values :
        new_values ['currency'] = abo_price  ['currency']
    new_values ['balance_open'] = new_values ['amount']
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
    _ = db.i18n.gettext
    now = Date ('.')
    common.reject_attributes \
        ( _
        , new_values
        , 'abo'
        , 'invoice_no'
        , 'period_start'
        , 'period_end'
        , 'payer'
        , 'subscriber'
        , 'open'
        , 'receipt_no'
        , 'amount_payed'
        , 'balance_open'
        )
    invoice = db.invoice.getnode (nodeid)
    amount  = new_values.get ('amount', cl.get (nodeid, 'amount'))
    if amount is None :
        raise Reject (_ ('"amount": only numbers allowed'))
    if 'amount' in new_values and payment :
        raise Reject (_ ('amount may not be changed after payment'))
    if 'payment' in new_values :
        payment = dict.fromkeys (new_values.get ('payment'))
        new_values ['payment'] = payment = list (sorted (payment))
        payed   = sum (db.payment.get (i, 'amount') for i in payment)
        new_values ['amount_payed'] = payed
        balance = new_values ['balance_open'] = amount - payed
        if balance <  0 :
            raise Reject (_ ('payment may not exceed the open balance'))
        if balance == 0 :
            new_values ['open'] = False
        else :
            new_values ['open'] = True
    inv_no  = cl.get (nodeid, 'invoice_no')
    abo     = db.abo.getnode (cl.get (nodeid, 'abo'))
    if abo ['end'] and list (new_values) != ['invoice_group'] :
        raise Reject (_ ('no change of closed subscription'))
    common.auto_retire (db, cl, nodeid, new_values, 'payment')
# end def check_invoice

def create_new_invoice (db, cl, nodeid, oldvalues) :
    abo_id = cl.get (nodeid, 'abo')
    abo    = db.abo.getnode (abo_id)
    if 'open' in oldvalues and not cl.get (nodeid, 'open') :
        invoice = abo_max_invoice (db, abo)
        if not invoice ['open'] :
            db.invoice.create (abo = abo_id)
# end def create_new_invoice

def new_payment (db, cl, nodeid, new_values) :
    common.require_attributes \
        (db.i18n.gettext, cl, nodeid, new_values, 'amount', 'invoice')
    inv = db.invoice.getnode (new_values ['invoice'])
    if new_values ['receipt_no'] == 'auto' :
        rnum = inv.invoice_no.replace ('R', 'B')
        if rnum [0] != 'B' : rnum = 'b' + rnum
        max = 0
        for p_id in inv.payment :
            rn = db.payment.get (p_id, 'receipt_no')
            if not rn.startswith (rnum) or rn == rnum :
                continue
            n = int (rn [len (rnum):], base = 10)
            if n > max :
                max = n
        new_values ['receipt_no'] = rnum + '%s' % (max + 1)
    if 'date_payed' not in new_values :
        new_values ['date_payed'] = Date ('.')
# end def new_payment

def check_payment (db, cl, nodeid, new_values) :
    common.require_attributes \
        ( db.i18n.gettext, cl, nodeid, new_values
        , 'amount', 'date_payed', 'receipt_no'
        )
    common.reject_attributes (db.i18n.gettext, new_values, 'invoice')
# end def check_payment

def update_payment (db, cl, nodeid, oldvalues) :
    """ Trigger payment update after amount changed
    """
    if  (   'amount' in oldvalues
        and oldvalues ['amount'] != cl.get (nodeid, 'amount')
        ) :
        inv = db.invoice.getnode (cl.get (nodeid, 'invoice'))
        pay = inv.payment
        pay.append (pay [0])
        db.invoice.set (inv.id, payment = pay)
# end def update_payment

def init (db) :
    if 'invoice' not in db.classes :
        return
    db.invoice.audit ("create", new_invoice)
    db.invoice.react ("create", add_to_abo_payer)
    db.invoice.audit ("set",    check_invoice)
    db.invoice.react ("set",    create_new_invoice)
    if 'payment' in db.classes :
        db.payment.audit ("create", new_payment)
        db.payment.audit ("set",    check_payment)
        db.payment.react ("set",    update_payment)
# end def init
