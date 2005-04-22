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
from roundup.rup_utils import uni, pretty, abo_max_invoice
from roundup.date      import Date, Interval

Reject = ValueError

month  = Interval ('1m')
month2 = Interval ('2m')

errmsgs = \
    { 'mandatory' : uni ('"%s" muss ausgefüllt werden')
    , 'forbidden' : uni ('"%s" darf nicht ausgefüllt werden')
    , 'nochange'  : uni ('"%s" darf nicht geändert werden')
    , 'nonzero'   : uni ('"%s" darf nicht 0 werden')
    , 'endtime'   : uni ('Storno: Endzeit muss größer/gleich Startzeit sein')
    , 'month'     : uni ('"%s" (Storno) nur +/- ein Monat')
    , 'period'    : uni ('"%s" nur im Bereich letzte Rechnungsperiode: %s-%s')
    , 'delete'    : uni ('Storno mit Löschen nur für unbezahlte neue Abos')
    , 'closefree' : uni ('Wiederaufnahme Abo nur innerhalb Zweimonatsfrist')
    , 'closepay'  : uni ('Wiederaufnahme Abo nur innerhalb letzter Periode')
    , 'openfail'  : uni ('Wiederaufnahme/Änderung nur für gültige Abos')
    }

def err (msg, * param) :
    return errmsgs [msg] % tuple ([pretty (str (p)) for p in param])
# end def err

def set_defaults (db, cl, nodeid, new_values) :
    print "start of set_defaults"
    for i in ('aboprice', 'subscriber') :
        if not new_values.has_key (i) :
            raise Reject, err ('mandatory', i)
    for i in ('invoices',) :
        if new_values.has_key (i) :
            raise Reject, err ('forbidden', i)
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
    if db.abo_price.get (cl.get (nodeid, 'aboprice'), 'amount') :
        db.invoice.create (abo = nodeid)
# end def create_invoice

def update_address (db, cl, nodeid, oldvalues) :
    for lattr, rattr in (('payer', 'payed_abos'), ('subscriber', 'abos')) :
        adr_id = cl.get (nodeid, lattr)
        adr    = db.address.getnode (adr_id)
        l      = adr [rattr] or []
        l.append (nodeid)
        db.address.set (adr_id, ** {rattr : l})
# end def update_address

def check_change (db, cl, nodeid, new_values) :
    """
        We allow closing of an abo with the end date == begin date if
        there is at most one un-payed invoice. In this case we remove
        this abo from the address and remove the corresponding invoice
        from the address, too.

        Re-opening (deletion of "end") is only possible if the last
        invoice for this abo is withing the current period, i.e., if the
        period_end of the last invoice is > now. Otherwise a new abo has
        to be created by hand.
    """
    abo = cl.getnode (nodeid)
    for i in ('aboprice', 'begin') :
        if i in new_values :
            raise Reject, err ('nochange', i)
    if 'amount' in new_values :
        if new_values ['amount'] == 0 and abo ['amount'] > 0 :
            raise Reject, err ('nonzero', 'amount')
    # Changing 'end':
    if  'end' in new_values :
        o_end   = abo        ['end']
        n_end   = new_values ['end']
        now     = Date ('.')
        invoice = abo_max_invoice (db, abo)
        # Attempt to change error-closed abo (unlinked from address)
        if o_end == abo ['begin'] :
            raise Reject, err ('openfail')
        # Attempt to resurrect a closed abo:
        if  (not n_end and o_end) :
            if invoice :
                if o_end < now - month2 :
                    raise Reject, err ('closefree')
            else :
                if invoice ['period_end'] < now :
                    raise Reject, err ('closepay')
        # Attempt to close (or modify close date), check end-date:
        if  (n_end) :
            if n_end < abo ['begin'] :
                raise Reject, err ('endtime')
            if not invoice and (n_end < now - month or n_end > now + month) :
                raise Reject, err ('month', 'end')
            if  (   invoice
                and (  n_end < invoice ['period_start']
                    or n_end > invoice ['period_end']
                    )
                ) :
                raise Reject, err \
                    ('period'
                    , 'end'
                    , * [invoice [x].pretty ('%Y-%m-%d')
                         for x in ('period_start', 'period_end')
                        ]
                    )
            if n_end == abo ['begin'] :
                if  (  len (abo ['invoices']) > 1
                    or (invoice and not invoice ['open'])
                    ) :
                    raise Reject, err ('delete')
                # unlink abo from payer/subscriber addresses
                for lattr, rattr in \
                    (('payer', 'payed_abos'), ('subscriber', 'abos')) :
                    id   = abo [lattr]
                    abos = db.address.get (id, rattr)
                    l    = [a for a in abos if a != nodeid]
                    db.address.set (id, ** {rattr : l})
                # unlink invoice from payer address
                if invoice :
                    id  = invoice ['payer']
                    inv = db.address.get (id, 'invoices')
                    l   = [i for i in inv if i != invoice ['id']]
                    db.address.set (id, invoices = l)
# end def check_change

def init (db) :
    db.abo.audit ("create", set_defaults)
    db.abo.audit ("set",    check_change)
    db.abo.react ("create", update_address)
    db.abo.react ("create", create_invoice)
# end def init
