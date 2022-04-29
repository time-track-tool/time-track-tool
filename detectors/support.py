#! /usr/bin/python
# Copyright (C) 2010-14 Dr. Ralf Schlatterbeck Open Source Consulting.
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

import re
email_ok = False
try :
    from email.parser                   import Parser
    from email.message                  import Message
    from email.utils                    import getaddresses
    from email.header                   import decode_header
    email_ok = True
except ImportError :
    pass
from itertools                      import chain
from roundup                        import roundupdb, hyperdb
from roundup.date                   import Date
from roundup.exceptions             import Reject
from roundup.mailgw                 import uidFromAddress
import common

def new_support (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
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
        ( db.i18n.gettext, cl, nodeid, new_values
        , 'title', 'category', 'status', 'prio', 'responsible'
        )
# end def check_support

def audit_superseder (db, cl, nodeid, new_values) :
    """
      * ensure that we do not set superseder on a new item
      * ensure that superseder gets not set to itself
      * automatically set status to closed
    """
    _ = db.i18n.gettext
    new_sup = new_values.get ("superseder", None)
    if new_sup :
        if not nodeid :
            raise Reject, _ ("May not set %s on new issue") % _ ('superseder')
        for sup in new_sup :
            if sup == nodeid :
                raise Reject, _ ("Can't set %s to yourself") % _ ('superseder')
        new_values ["status"] = db.sup_status.lookup ('closed')
# end def audit_superseder

def serial_num (db, cl, nodeid, new_values) :
    if  (   'serial_number'   not in new_values
        and 'number_effected' not in new_values
        ) :
        return
    sn = None
    if 'serial_number' in new_values :
        sn = new_values ['serial_number']
    elif nodeid :
        sn = cl.get (nodeid, 'serial_number')
    if not sn :
        return
    sn = [s.strip () for s in sn.split ('\n')]
    sn = [s.upper () for s in sn if s]
    if len (sn) :
        new_values ['number_effected'] = len (sn)
    new_values ['serial_number']   = '\n'.join (sn) or None
# end def serial_num

def initial_values (db, cl, nodeid, new_values) :
    if 'type' not in new_values :
        new_values ['type'] = db.sup_type.lookup ('Support Issue')
# end def initial_values

def set_first_reply (db, cl, nodeid, new_values) :
    """ Set first_reply field in case the support issue hasn't set this
        yet *and* status goes to closed or satisfied.
    """
    issue = cl.getnode (nodeid)
    if issue.first_reply :
        return
    if 'status' in new_values and 'first_reply' not in new_values :
        closed = db.sup_status.lookup ('closed')
        satis  = db.sup_status.lookup ('satisfied')
        cust   = db.sup_status.lookup ('customer')
        if new_values ['status'] in (closed, satis, cust) :
            new_values ['first_reply'] = Date ('.')
    elif new_values.get ('set_first_reply', None) :
        new_values ['first_reply'] = Date ('.')
# end def set_first_reply

def check_dates (db, cl, nodeid, new_values) :
    oldst  = cl.get (nodeid, "status")
    status = new_values.get ("status", None)
    if 'status' not in new_values or oldst == status :
        return
    status_name = db.sup_status.get (status, 'name')
    now = Date ('.')
    if status_name == 'closed' :
        new_values ["closed"] = now
        if not cl.get (nodeid, 'satisfied') :
            new_values ["satisfied"] = now
    else :
        new_values ["closed"] = None
    if status_name == 'satisfied' :
        new_values ["satisfied"] = now
    if status_name in ['open', 'customer'] :
        new_values ["satisfied"] = None
# end def check_dates

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

def find_or_create_contact \
    (db, mail, rn, customer = None, frm = None, subject = None) :
    """ Search for contact with given mail.
        Realname (rn) is used when creating a new customer.
        frm will be fromaddress from newly created customer.
        If customer is already given we only search for mails *of this
        customer* and do not create a new customer / email if not found.
        None is returned in case a customer was given and no email was
        found. Otherwise the contact (which might have been created)
        will be returned.
        Note that if a customer with name 'SPAM' exists and the message
        subject matches a spam pattern we will return the SPAM customer.
    """
    mail   = mail.lower ()
    cemail = db.contact_type.lookup ('Email')
    sdict  = dict (contact_type = cemail, contact = mail)
    md     = mail.split ('@') [-1]
    sdict ['customer.is_valid'] = True
    if customer :
        sdict ['customer'] = customer
    for c in db.contact.filter (None, sdict) :
        cont = db.contact.getnode (c)
        cust = db.customer.getnode (cont.customer)
        # filter uses substring match for strings
        if cont.contact == mail and cust.is_valid :
            return c
    # Spam Handling: Try to match subject against spam pattern from spamfilter
    # If found return first contact of spam customer (we don't want to
    # keep all the mails from incoming spam)
    if subject and not customer :
        spam_customer = None
        try :
            spam_customer = db.customer.lookup ('SPAM')
        except KeyError :
            pass
        if spam_customer :
            spam_re = getattr \
                (db.config.ext, 'MAILGW_SPAM_PATTERN', r'^[[].?S[pP][aA][mM]')
            spam_re = re.compile (spam_re.strip ())
            if spam_re.search (subject) :
                spc = db.customer.getnode (spam_customer)
                return spc.contacts [0]
        
    # this also tries subdomains, e.g., country.example.com for the
    # incoming mail will be matched by example.com as the customer mail.
    # Note that we don't allow toplevel domains for the customer (e.g.
    # .com).
    customer_found = False
    while '.' in md and not customer_found :
        sdict = dict (is_valid = True, maildomain = md)
        for cu in db.customer.filter (None, sdict) :
            cust = db.customer.getnode (cu)
            if cust.maildomain == md :
                if customer and customer != cu :
                    continue
                customer = cu
                customer_found = True
                break
        md = md.split ('.', 1) [1]
    if customer and not customer_found :
        return None
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

def fix_emails (email_list) :
    """ Remove '\r' to work around email parse bug in python2.7
    """
    r = []
    for m in email_list :
        r.append (m.replace ('\r', ''))
    return r
# end def fix_emails

def header_check (db, cl, nodeid, new_values) :
    """ Check header of new messages and determine original customer
        from that header -- only if sender is the support special
        account (any account with system status).  If send_to_customer
        flag is set *and* account is not a system account, munge
        the headers and add X-ROUNDUP-TO and X-ROUNDUP-CC headers.
    """
    _ = db.i18n.gettext
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
            frm  = fix_emails (h.get_all ('From'))
            subj = header_utf8 (h.get_all ('Subject') [0])
            if  (   frm
                and 'customer' not in new_values
                and 'emails' not in new_values
                ) :
                cc  = {}
                if not nodeid :
                    # use only first 'From' address (there shouldn't be more)
                    rn, mail = getaddresses (frm) [0]
                    # the *to* address in this mail is the support user we
                    # want as a from-address for future mails *to* this user
                    autad = None
                    hto = fix_emails (h.get_all ('To'))
                    if hto :
                        torn, autad = getaddresses (hto) [0]
                        if not autad.startswith ('support') :
                            autad = None
                    c = find_or_create_contact \
                        (db, mail, rn, frm = autad, subject = subj)
                    cust  = new_values ['customer'] = \
                        db.contact.get (c, 'customer')
                    new_values ['emails'] = [c]
                else :
                    supi = cl.getnode (nodeid)
                    cust = supi.customer
                    new_values ['emails']    = supi.emails
                    new_values ['cc_emails'] = supi.cc_emails
                    if supi.cc :
                        cc = dict.fromkeys \
                            (x.strip ().lower () for x in supi.cc.split (','))
                # Parse To and CC headers to find more customer email
                # addresses. Check if these contain the same domain
                # part as the From.
                ccs = h.get_all ('CC') or []
                tos = h.get_all ('To') or []
                if nodeid :
                    tos.extend (frm)
                cfrm = db.customer.get (cust, 'fromaddress')
                alltocc = dict.fromkeys (new_values ['emails'])
                if 'cc_emails' in new_values :
                    alltocc.update (dict.fromkeys (new_values ['cc_emails']))
                for addrs, field in ((tos, 'emails'), (ccs, 'cc_emails')) :
                    addrs = fix_emails (addrs)
                    for rn, mail in getaddresses (addrs) :
                        if mail == cfrm :
                            continue
                        c = find_or_create_contact \
                            (db, mail, rn, customer = cust)
                        if c :
                            if field not in new_values :
                                new_values [field] = []
                            if c not in alltocc :
                                new_values [field].append (c)
                                alltocc [c] = 1
                        elif uidFromAddress (db, (rn, mail), create = 0) :
                            # ignore internal addresses
                            pass
                        else :
                            cc [mail.lower ()] = 1
                if cc :
                    new_values ['cc'] = ', '.join (cc.keys ())
        else :
            if send_to_customer :
                mails = []
                cc = []
                if 'emails' in new_values :
                    mails = new_values ['emails']
                elif nodeid :
                    mails = cl.get (nodeid, 'emails')
                if 'cc_emails' in new_values :
                    mcc = new_values ['cc_emails']
                elif nodeid :
                    mcc = cl.get (nodeid, 'cc_emails')
                mails = mails or []
                mcc   = mcc or []
                mails = (db.contact.get (x, 'contact') for x in mails)
                mcc   = (db.contact.get (x, 'contact') for x in mcc)
                if 'cc' in new_values :
                    cc = new_values ['cc']
                elif nodeid :
                    cc = cl.get (nodeid, 'cc')
                m  = ','.join (mails)
                mc = ','.join (mcc)
                if mc :
                    if cc :
                        mc = ','.join ((mc, cc))
                else :
                    mc = cc
                if not m and not mc :
                    raise Reject, \
                        _ ("Trying to send to customer with empty CC and "
                           "without configured contact-email for customer"
                          )
                if m :
                    h.add_header ('X-ROUNDUP-TO', m)
                if mc :
                    h.add_header ('X-ROUNDUP-CC', mc)
                if 'bcc' in new_values :
                    bcc = new_values ['bcc']
                elif nodeid :
                    bcc = cl.get (nodeid, 'bcc')
                if bcc :
                    h.add_header ('X-ROUNDUP-BCC', bcc)
                # Time-Stamp of first reply to customer
                if not nodeid or not cl.get (nodeid, 'first_reply') :
                    new_values ['first_reply'] = Date ('.')
        h = h.as_string ()
        if h != '\n' and h != msg.header :
            db.msg.set (msgid, header = h)
# end def header_check

def check_require_message (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    if 'messages' in new_values :
        return
    for prop in ('responsible',) :
        if prop in new_values :
            raise Reject, _ ("Change of %s requires a message") % _ (prop)
# end def check_require_message

def check_resp_not_support (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
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
    if not new_values.get ('fromaddress', None) :
        msf = getattr (db.config.ext, 'MAILGW_SUPPORT_FROM', None)
        if msf :
            new_values ['fromaddress'] = msf
        else :
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
    _ = db.i18n.gettext
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
    common.require_attributes (db.i18n.gettext, cl, nodeid, new_values, 'nosy')
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

def set_prodcat (db, cl, nodeid, new_values) :
    """ Set level-3 product category for support issue depending on
        product and category.
        - product setting overrules explicit prodcat or category setting
        - explicit prodcat overrules category
        - category.prodcat is last resort
    """
    pc = prod = cat = None
    if 'prodcat' in new_values :
        pc = new_values ['prodcat']
    elif nodeid :
        pc = cl.get (nodeid, 'prodcat')
    if 'product' in new_values :
        prod = new_values ['product']
    elif nodeid :
        prod = cl.get (nodeid, 'product')
    if prod :
        prod = db.product.getnode (prod)
        pcp  = db.prodcat.getnode (prod.product_family)
        assert pcp.level == 3
        if pcp.id != pc :
            new_values ['prodcat'] = pcp.id
            return
    if pc :
        return
    if 'category' in new_values :
        cat = new_values ['category']
    elif nodeid :
        cat = cl.get (nodeid, 'category')
    if cat :
        pcc = db.category.get (cat, 'prodcat')
        if pcc :
            new_values ['prodcat'] = pcc
# end def set_prodcat

suppclaim = ('customer', 'warranty')
mandatory_by_type = \
    { 'RMA Issue'          : ('customer', 'prodcat', 'product', 'warranty')
    , 'Supplier Claim'     : suppclaim
    , 'Supplier Claim RMA' : suppclaim
    , 'Supplier Claim IGC' : suppclaim
    , 'Support Issue'      : ('customer',)
    , 'Other'              : ('customer',)
    }

def check_params (db, cl, nodeid, new_values) :
    """ Check for existence of mandatory parameters
    """
    st_open = db.sup_status.lookup ('open')
    if 'status' not in new_values or new_values ['status'] == st_open :
        return
    common.require_attributes (db.i18n.gettext, cl, nodeid, new_values, 'type')
    type = new_values.get ('type')
    if not type :
        type = cl.get (nodeid, 'type')
    type     = db.sup_type.get (type, 'name')
    required = mandatory_by_type [type]
    closed   = db.sup_status.lookup ('closed')
    common.require_attributes \
        (db.i18n.gettext, cl, nodeid, new_values, * required)
    if type == 'RMA Issue' and new_values ['status'] == closed :
        common.require_attributes \
            ( db.i18n.gettext, cl, nodeid, new_values
            , 'execution', 'classification'
            )
# end def check_params

def check_prodcat (db, cl, nodeid, new_values) :
    """ Check that prodcat level is correct.
    """
    _ = db.i18n.gettext
    if 'valid' in new_values and not new_values ['valid'] :
        return
    common.require_attributes (_, cl, nodeid, new_values, 'name')
    if 'name' in new_values :
        name = new_values ['name']
    else :
        name = cl.get (nodeid, 'name')
    if 'level' in new_values :
        level = new_values.get ('level')
    elif nodeid :
        level = cl.get (nodeid, 'level')
    if not level :
        new_values ['level'] = 1
    if level > 4 :
        raise Reject, _ ('Max. %s is ') % _ ('level')
# end def check_prodcat

def cust_agree (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    common.require_attributes (_, cl, nodeid, new_values, 'description')
    customer = product = None
    if 'customer' in new_values :
        customer = new_values ['customer']
    elif nodeid :
        customer = cl.get (nodeid, 'customer')
    if 'product' in new_values :
        product = new_values ['product']
    elif nodeid :
        product = cl.get (nodeid, 'product')
    if not customer and not product :
        raise Reject \
            ( _ ("At least one of %(customer)s or %(product)s must be defined") 
            % dict ((k, _ (k)) for k in ('product', 'customer'))
            )
# end def cust_agree

def close_spammy_customer (db, cl, nodeid, old_values) :
    ocust = old_values.get ('customer')
    ostat = old_values.get ('status')
    if not ocust or not ostat :
        return
    issue = cl.getnode (nodeid)
    ncust = issue.customer
    nstat = issue.status
    if ncust == ocust or nstat == ostat :
        return
    if db.customer.get (ncust, 'name') != 'SPAM' :
        return
    if db.sup_status.get (nstat, 'name') != 'closed' :
        return
    # OK, this support issue was closed as spam, old customer is *not*
    # the spam customer (checked above they're different) so we mark
    # the customer invalid -- if not already invalid
    if db.customer.get (ocust, 'is_valid') :
        db.customer.set (ocust, is_valid = False)
# end def close_spammy_customer

def check_bu (db, cl, nodeid, new_values) :
    """ Check BU is set
        Make an exception for the SPAM customer when closing the support
        issue. Another exception is when status moves to open, this
        happens when an incoming mail re-opens an issue.
    """
    # only check if status changed: we don't want simple email replies
    # to fail
    if 'status' in new_values :
        closed = db.sup_status.lookup ('closed')
        open   = db.sup_status.lookup ('open')
        if new_values ['status'] == closed :
            cust = new_values.get ('customer', cl.get (nodeid, 'customer'))
            spam = db.customer.lookup ('SPAM')
            if cust == spam :
                return
        if new_values ['status'] == open :
            return
        common.require_attributes \
            (db.i18n.gettext, cl, nodeid, new_values, 'business_unit')
# end def check_bu

def set_bu (db, cl, nodeid, new_values) :
    """ Get BU from customer if not set on new item
    """
    if 'business_unit' not in new_values and 'customer' in new_values :
        cust = db.customer.getnode (new_values ['customer'])
        bu   = cust.business_unit
        if bu :
            new_values ['business_unit'] = bu
# end def set_bu

def init (db) :
    if 'prodcat' in db.classes :
        db.prodcat.audit ("set",    check_prodcat)
        db.prodcat.audit ("create", check_prodcat)
    if 'support' not in db.classes :
        return
    assert (email_ok)
    db.support.audit   ("set",    check_resp_not_support,   priority = 20)
    db.support.audit   ("create", new_support,              priority = 50)
    db.support.audit   ("set",    check_support,            priority = 40)
    db.support.audit   ("create", audit_superseder)
    db.support.audit   ("set",    audit_superseder)
    db.support.audit   ("create", serial_num)
    db.support.audit   ("set",    serial_num)
    db.support.audit   ("create", initial_values)
    db.support.audit   ("set",    set_first_reply)
    db.support.audit   ("set",    check_dates,              priority = 200)
    db.support.audit   ("set",    check_require_message,    priority = 200)
    db.support.audit   ("create", header_check,             priority = 200)
    db.support.audit   ("set",    header_check,             priority = 200)
    db.support.audit   ("create", initial_props,            priority = 300)
    db.support.audit   ("set",    remove_support_from_nosy, priority = 300)
    db.support.audit   ("set",    set_status,               priority = 350)
    db.support.audit   ("create", set_prodcat,              priority = 400)
    db.support.audit   ("set",    set_prodcat,              priority = 400)
    db.support.audit   ("set",    check_params,             priority = 450)
    db.support.audit   ("create", set_bu,                   priority = 450)
    db.support.audit   ("set",    check_bu,                 priority = 450)
    db.support.react   ("set",    close_spammy_customer)

    db.customer.audit  ("create", new_customer,             priority = 90)
    db.customer.audit  ("create", check_maildomain)
    db.customer.audit  ("set",    check_maildomain,         priority = 150)
    db.customer.react  ("set",    check_retire)

    db.mailgroup.audit ("create", check_mailgroup)
    db.mailgroup.audit ("set",    check_mailgroup)

    db.customer_agreement.audit ("create", cust_agree)
    db.customer_agreement.audit ("set",    cust_agree)
# end def init
