#! /usr/bin/python
# Copyright (C) 2011-21 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
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
#    Support-Tracker related utilities
#
#--
#

try :
    # fail at runtime if these are used
    from email.parser import Parser
except ImportError :
    pass

def has_x_roundup_header (db, msg) :
    try :
        db = db._db
    except AttributeError :
        pass
    if 'header' in db.msg.properties and msg.header :
        h = Parser ().parsestr (str (msg.header), headersonly = True)
        rcc = h.get_all ('X-ROUNDUP-CC')
        if rcc :
            return True
        rto = h.get_all ('X-ROUNDUP-TO')
        if rto :
            return True
    return False
# end def has_x_roundup_header

def prodcat_parents (db, utils, prodcat) :
    x = []
    parent = prodcat
    for n in range (int (prodcat.level or 0), 0, -1) :
        ep = utils.ExtProperty (utils, parent.name, item = parent)
        x.append (ep.formatlink ())
        parent = getattr (parent, 'parent', None)
        if not parent :
            break
    return '&raquo;'.join (x)
# end def prodcat_parents

def serial_match (sn, serials) :
    sns = (s.strip () for s in str (serials).split ('\n'))
    sns = dict.fromkeys (s for s in sns if s)
    return sn in sns
# end def serial_match

def serial (db, node, sn) :
    ser = db.support.filter (None, dict (serial_number = sn))
    ser = [s for s in ser
           if s.id != node.id and serial_match (sn, s.serial_number)
          ]
    return ser
# end def serial

def serials (db, node) :
    if not node.serial_number :
        return []
    tpl = \
        ("support?"
         ":columns=id,title,type,status,responsible,customer&:sort=id"
         "&:filter=id&:pagesize=20&:startwith=0&id=%s"
        )
    serials = (s.strip () for s in str (node.serial_number).split ('\n'))
    sns     = dict ((s, serial (db, node, s)) for s in serials if s)
    serials = dict ((s, len (sns [s])) for s in sns)
    r   = []
    for s in serials :
        l = serials [s]
        if not l :
            continue
        r.append \
            (""'Serial <a href="%s">%s</a> '
               'occurs %s times in other support issues'
            % (tpl % ','.join (k.id for k in sns [s]), s, l)
            )
    return r
# end def serials

# The lower part removes 'business_unit' from the required attributes
mark_spam = """
function mark_spam_js() {
    frm = document.forms.itemSynopsis;
    frm.status.value = "%(status)s";
    frm.customer.value = "%(customername)s";
    frm.responsible.value = "%(username)s";
    frm.nosy.value = "";
    frm ['@note'].value = "spam --> closed";
    var req = frm ['@required'].value.split (',');
    var nrq = [];
    for (var i=0; i<req.length; i++) {
        var r = req [i].trim ();
        if (r != 'business_unit') {
            nrq.push (r);
        }
    }
    frm ['@required'].value = nrq.join ();
}
"""

def mark_spam_js (db) :
    try :
        db = db._db
    except AttributeError :
        pass
    status = db.sup_status.lookup ('closed')
    try :
        cust   = db.customer.lookup ('SPAM')
        cust   = db.customer.getnode (cust)
    except KeyError :
        return ''
    customername = cust.name
    username = db.user.get (db.getuid (), 'username')
    return mark_spam % locals ()
#end def mark_spam_js

def init (instance) :
    reg = instance.registerUtil
    reg ('has_x_roundup_header',    has_x_roundup_header)
    reg ('prodcat_parents',         prodcat_parents)
    reg ('serials',                 serials)
    reg ('mark_spam_js',            mark_spam_js)
# end def init
