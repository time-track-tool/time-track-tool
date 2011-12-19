#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    support
#
# Purpose
#    Detectors for support issues
#
#--
#

email_ok = False
try :
    from email.parser                   import Parser
    from email.message                  import Message
    from email.utils                    import getaddresses
    from email.header                   import decode_header
    email_ok = True
except ImportError :
    pass
from roundup                        import roundupdb, hyperdb
from roundup.date                   import Date
from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation
from roundup.mailgw                 import uidFromAddress
import common

def new_support (db, cl, nodeid, new_values) :
    closed = db.sup_status.lookup ('closed')
    if 'messages'    not in new_values :
        raise Reject, _ ("New %s requires a message") % _ (cl.classname)
    if  ('status' not in new_values or new_values ['status'] == closed) :
        new_values ['status'] = db.sup_status.lookup ('open')
    if 'category'     not in new_values :
        new_values ['category'] = '1'
    if 'prio'         not in new_values :
        new_values ['prio'] = db.sup_prio.lookup ('unknown')
# end def new_support

def check_support (db, cl, nodeid, new_values) :
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'title', 'category', 'status', 'prio', 'responsible'
        )
# end def check_support

def audit_superseder (db, cl, nodeid, new_values) :
    """
      * ensure that we do not set superseder on a new item
      * ensure that superseder gets not set to itself
      * automatically set status to closed
    """
    new_sup = new_values.get ("superseder", None)
    if new_sup :
        if not nodeid :
            raise Reject, _ ("May not set %s on new issue") % _ ('superseder')
        for sup in new_sup :
            if sup == nodeid :
                raise Reject, _ ("Can't set %s to yourself") % _ ('superseder')
        new_values ["status"] = db.sup_status.lookup ('closed')
# end def audit_superseder

def check_closed (db, cl, nodeid, new_values) :
    oldst  = cl.get (nodeid, "status")
    status = new_values.get ("status", None)
    if 'status' not in new_values or oldst == status :
        return
    status_name = db.sup_status.get (status, 'name')
    if status_name == 'closed' :
        new_values ["closed"] = Date ('.')
    else :
        new_values ["closed"] = None
# end def check_closed

def header_utf8 (header) :
    parts = decode_header (header)
    result = []
    for txt, coding in parts :
        if not coding :
            # might be 8 bit
            result.append (txt.decode ('latin1'))
        else :
            result.append (txt.decode (coding))
    return (''.join (result)).encode ('utf-8')
# end def header_utf8

def find_or_create_contact (db, mail, rn, customer = None, frm = None) :
    """ Search for contact with given mail.
        Realname (rn) is used when creating a new customer.
        frm will be fromaddress from newly created customer.
        If customer is already given we only search for mails *of this
        customer* and do not create a new customer / email if not found.
        None is returned in case a customer was given and no email was
        found. Otherwise the contact (which might have been created)
        will be returned.
    """
    mail   = mail.lower ()
    cemail = db.contact_type.lookup ('Email')
    sdict  = dict (contact_type = cemail, contact = mail)
    sdict ['customer.is_valid'] = True
    if customer :
        sdict ['customer'] = customer
    for c in db.contact.filter (None, sdict) :
        cont = db.contact.getnode (c)
        cust = db.customer.getnode (cont.customer)
        # filter uses substring match for strings
        if cont.contact == mail and cust.is_valid :
            return c
    if customer :
        return None
    md    = mail.split ('@') [-1]
    # this also tries subdomains, e.g., country.example.com for the
    # incoming mail will be matched by example.com as the customer mail.
    # Note that we don't allow toplevel domains for the customer (e.g.
    # .com).
    while '.' in md and not customer :
        sdict = dict (is_valid = True, maildomain = md)
        for cu in db.customer.filter (None, sdict) :
            cust = db.customer.getnode (cu)
            if cust.maildomain == md :
                customer = cu
                break
        md = md.split ('.', 1) [1]
    rn = header_utf8 (rn)
    if not customer :
        customer = db.customer.create \
            ( name        = ' '.join ((rn, mail))
            , fromaddress = frm
            , maildomain  = (mail.split ('@') [-1]).lower ()
            )
    c = db.contact.create \
        ( contact_type = cemail
        , contact      = mail
        , customer     = customer
        , description  = rn
        )
    contacts = db.customer.get (customer, 'contacts')
    contacts.append (c)
    db.customer.set (customer, contacts = contacts)
    return c
# end def find_or_create_contact


def header_check (db, cl, nodeid, new_values) :
    """ Check header of new messages and determine original customer
        from that header -- only if sender is the support special
        account (any account with system status).  If send_to_customer
        flag is set *and* account is not a system account, munge
        the headers and add X-ROUNDUP-CC header.
    """
    send_to_customer = False
    # Be sure to alway set send_to_customer to False!
    if 'send_to_customer' in new_values :
        send_to_customer = new_values ['send_to_customer']
        new_values ['send_to_customer'] = False
    newmsgs = new_values.get ('messages')
    if not newmsgs :
        return
    newmsgs = set (newmsgs)
    if nodeid :
        oldmsgs = set (cl.get (nodeid, 'messages'))
    else :
        oldmsgs = set ()
    system  = db.user_status.lookup ('system')
    cemail  = db.contact_type.lookup ('Email')
    for msgid in newmsgs.difference (oldmsgs) :
        msg    = db.msg.getnode (msgid)
        h      = None
        if msg.header :
            h = Parser ().parsestr (msg.header, headersonly = True)
        else :
            h = Message ()
        if db.user.get (msg.author, 'status') == system :
            frm = h.get_all ('From')
            if  (   not nodeid
                and frm
                and 'customer' not in new_values
                and 'emails' not in new_values
                ) :
                # use only first 'From' address (there shouldn't be more)
                rn, mail = getaddresses (frm) [0]
                # the from address in this mail is the support user we
                # want as a from-address for future mails *to* this user
                autad = db.user.get (msg.author, 'address')
                c     = find_or_create_contact (db, mail, rn, frm = autad)
                cust  = new_values ['customer'] = db.contact.get (c, 'customer')
                new_values ['emails'] = [c]
                # Parse To and CC headers to find more customer email
                # addresses. Check if these contain the same domain
                # part as the From.
                ccs = h.get_all ('CC')
                tos = h.get_all ('To')
                cc  = []
                for rn, mail in getaddresses (ccs + tos) :
                    c = find_or_create_contact (db, mail, rn, customer = cust)
                    print "huhu", mail
                    if c :
                        new_values ['emails'].append (c)
                    elif uidFromAddress (db, (rn, mail)) :
                        print "hu?"
                        pass
                    else :
                        cc.append (mail)
                if cc :
                    new_values ['cc'] = ', '.join (cc)
        else :
            if send_to_customer :
                mails = None
                if 'emails' in new_values :
                    mails = new_values ['emails']
                elif nodeid :
                    mails = cl.get (nodeid, 'emails')
                if not mails :
                    raise Reject, \
                        _ ("Trying to send to customer without "
                           "configured contact-email for customer"
                          )
                mails = (db.contact.get (x, 'contact') for x in mails)
                if 'cc' in new_values :
                    cc = new_values ['cc']
                elif nodeid :
                    cc = cl.get (nodeid, 'cc')
                m = ','.join (mails)
                if cc :
                    m = ','.join ((m, cc))
                h.add_header ('X-ROUNDUP-CC', m)
                print new_values, nodeid
                if 'bcc' in new_values :
                    bcc = new_values ['bcc']
                elif nodeid :
                    bcc = cl.get (nodeid, 'bcc')
                if bcc :
                    h.add_header ('X-ROUNDUP-BCC', bcc)
        h = h.as_string ()
        if h != '\n' and h != msg.header :
            db.msg.set (msgid, header = h)
# end def header_check

def check_require_message (db, cl, nodeid, new_values) :
    if 'messages' in new_values :
        return
    for prop in ('responsible',) :
        if prop in new_values :
            raise Reject, _ ("Change of %s requires a message") % _ (prop)
# end def check_require_message

def check_resp_not_support (db, cl, nodeid, new_values) :
    sup = db.user.lookup ('support')
    rsp = new_values.get ('responsible', cl.get (nodeid, 'responsible'))
    if rsp == sup and ('status' in new_values or 'confidential' in new_values) :
        raise Reject, _ ("Requires change of user (support not allowed)")
# end def check_resp_not_support

def remove_support_from_nosy (db, cl, nodeid, new_values) :
    """ Remove user "support" from nosy list if setting to confidential.
    """
    conf = new_values.get ('confidential', cl.get (nodeid, 'confidential'))
    nosy = new_values.get ('nosy',         cl.get (nodeid, 'nosy'))
    nosy = dict.fromkeys (nosy)
    sup = db.user.lookup ('support')
    if conf and sup in nosy :
        del nosy [sup]
        new_values ['nosy'] = nosy.keys ()
# end def remove_support_from_nosy

def initial_props (db, cl, nodeid, new_values) :
    """ Initial properties of support issue copied from customer.
        Fix initial nosy list: include nosy and nosygroups from the
        customer (if available).
        Make issue confidential if customer has confidential flag
        Fix responsible
    """
    cust = new_values.get ('customer', None)
    supp = db.user.lookup ('support')
    if not cust :
        if 'responsible' not in new_values :
            new_values ['responsible'] = supp
        return
    cust = db.customer.getnode (cust)
    nosy = dict.fromkeys (new_values.get ('nosy', []))
    if cust.nosy :
        for k in cust.nosy :
            nosy [k] = 1
    if cust.nosygroups :
        for g in cust.nosygroups :
            grp = db.mailgroup.getnode (g)
            for k in grp.nosy :
                nosy [k] = 1
    new_values ['nosy'] = nosy.keys ()
    if 'confidential' not in new_values :
        if cust.confidential :
            new_values ['confidential'] = True
        else :
            new_values ['confidential'] = False
    if 'responsible' not in new_values :
        new_values ['responsible'] = cust.responsible or supp
# end def initial_props

def new_customer (db, cl, nodeid, new_values) :
    """ Some initial values for a new customer
    """
    support = db.user.lookup ('support')
    if 'nosy' not in new_values and 'nosygroups' not in new_values :
        ngs = db.mailgroup.filter (None, dict (default_nosy = True))
        if (ngs) :
            new_values ['nosygroups'] = ngs
        if 'nosygroups' not in new_values :
            new_values ['nosy'] = [support]
    if 'fromaddress' not in new_values :
        new_values ['fromaddress'] = db.user.get (support, 'address')
    if 'confidential' not in new_values :
        new_values ['confidential'] = False
    new_values ['is_valid'] = True
# end def new_customer

def check_maildomain (db, cl, nodeid, new_values) :
    """ Delete maildomain if setting customer to invalid.
        Otherwise check that maildomain isn't a duplicate and is
        wellformed.
    """
    ovalid = None
    if nodeid :
        ovalid = cl.get (nodeid, 'is_valid')
    valid = new_values.get ('is_valid', ovalid)
    if not valid :
        new_values ['maildomain'] = None
    md = new_values.get ('maildomain', None)
    if not md :
        return
    if '.' not in md :
        raise Reject, \
            _ ('Toplevel domain "%(maildomain)s" not allowed, '
               'must contain "."'
              ) \
            % dict (maildomain = _ ('maildomain'))
    md = new_values ['maildomain'] = md.lower ()
    common.check_unique (_, cl, nodeid, maildomain = md)
# end def check_maildomain

def check_retire (db, cl, nodeid, old_values) :
    if not cl.get (nodeid, 'is_valid') :
        cl.retire (nodeid)
# end def check_retire

def check_mailgroup (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'nosy')
# end def check_mailgroup

def set_status (db, cl, nodeid, new_values) :
    """ Set status to open if changing user is a system user
        and the status isn't set explicitly and we have a message
    """
    system  = db.user_status.lookup ('system')
    ustatus = db.user.get (db.getuid (), 'status')
    if  (   'status' not in new_values
        and ustatus == system
        and 'messages' in new_values
        ) :
        new_values ['status'] = db.sup_status.lookup ('open')
# end def set_status

def init (db) :
    if 'support' not in db.classes :
        return
    assert (email_ok)
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.support.audit   ("set",    check_resp_not_support,   priority = 20)
    db.support.audit   ("create", new_support,              priority = 50)
    db.support.audit   ("set",    check_support,            priority = 40)
    db.support.audit   ("create", audit_superseder)
    db.support.audit   ("set",    audit_superseder)
    db.support.audit   ("set",    check_closed,             priority = 200)
    db.support.audit   ("set",    check_require_message,    priority = 200)
    db.support.audit   ("create", header_check,             priority = 200)
    db.support.audit   ("set",    header_check,             priority = 200)
    db.support.audit   ("create", initial_props,            priority = 300)
    db.support.audit   ("set",    remove_support_from_nosy, priority = 300)
    db.support.audit   ("set",    set_status,               priority = 350)

    db.customer.audit  ("create", new_customer,             priority = 90)
    db.customer.audit  ("create", check_maildomain)
    db.customer.audit  ("set",    check_maildomain,         priority = 150)
    db.customer.react  ("set",    check_retire)

    db.mailgroup.audit ("create", check_mailgroup)
    db.mailgroup.audit ("set",    check_mailgroup)
# end def init
