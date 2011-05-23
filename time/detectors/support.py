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

from email.parser                   import Parser
from email.message                  import Message
from email.utils                    import getaddresses
from email.header                   import decode_header
from roundup                        import roundupdb, hyperdb
from roundup.date                   import Date
from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation
from common                         import user_has_role, require_attributes

def new_support (db, cl, nodeid, new_values) :
    closed = db.sup_status.lookup ('closed')
    if 'messages'    not in new_values :
        raise Reject, _ ("New %s requires a message") % _ (cl.classname)
    if  ('status' not in new_values or new_values ['status'] == closed) :
        new_values ['status'] = db.sup_status.lookup ('open')
    if 'category'     not in new_values :
        new_values ['category'] = '1'
    if 'responsible'  not in new_values :
        new_values ['responsible'] = db.getuid ()
    if 'prio'         not in new_values :
        new_values ['prio'] = db.sup_prio.lookup ('unknown')
    if 'confidential' not in new_values :
        new_values ['confidential'] = 0
# end def new_support

def check_support (db, cl, nodeid, new_values) :
    require_attributes \
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

def find_or_create_contact (db, mail, rn, customer = None) :
    cemail = db.contact_type.lookup ('Email')
    sdict  = dict (contact_type = cemail, contact = mail)
    for c in db.contact.filter (None, sdict) :
        # filter uses substring match for strings
        if db.contact.get (c, 'contact') == mail :
            return c
    rn   = header_utf8 (rn)
    if not customer :
        customer = db.customer.create (name = ' '.join ((rn, mail)))
    c    = db.contact.create \
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

#               # Parse To and CC headers to find more customer email
#               # addresses. Check if these contain the same domain
#               # part as the From.
#               ccs = get_all ('CC')
#               tos = get_all ('To')
#               dom = mail.split ('@', 1) [-1]
#               for rn, mail in getaddresses (ccs + tos) :
#                   rn = decode_header (rn)
#                   d  = mail.split ('@', 1) [-1]
#                   if d == dom and not in_nosy (db, new_values, mail) :
#                       c = find_or_create_contact (db, mail)

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
    for m in newmsgs.difference (oldmsgs) :
        msg    = db.msg.getnode (m)
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
                sdict = dict (contact_type = cemail, contact = mail)
                c     = find_or_create_contact (db, mail, rn)
                new_values ['customer'] = db.contact.get (c, 'customer')
                new_values ['emails']   = [c]
        else :
            if send_to_customer :
                mails = None
                if 'emails' in new_values :
                    mails = new_values ['emails']
                elif nodeid :
                    mails = cl.get (nodeid, 'emails')
                if mails :
                    mails = (db.contact.get (x, 'contact') for x in mails)
                    h.add_header ('X-ROUNDUP-CC', ','.join (mails))
        h = h.as_string ()
        if h != '\n' and h != msg.header :
            db.msg.set (m, header = h)
# end def header_check

def check_require_message (db, cl, nodeid, new_values) :
    if 'messages' in new_values :
        return
    for prop in ('responsible',) :
        if prop in new_values :
            raise Reject, _ ("Change of %s requires a message") % _ (prop)
# end def check_require_message

def init (db) :
    if 'support' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.support.audit ("create", new_support,            priority = 50)
    db.support.audit ("set",    check_support,          priority = 40)
    db.support.audit ("create", audit_superseder)
    db.support.audit ("set",    audit_superseder)
    db.support.audit ("set",    check_closed,           priority = 200)
    db.support.audit ("set",    check_require_message,  priority = 200)
    db.support.audit ("create", header_check,           priority = 200)
    db.support.audit ("set",    header_check,           priority = 200)
# end def init
