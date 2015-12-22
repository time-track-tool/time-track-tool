#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2015 Dr. Ralf Schlatterbeck Open Source Consulting.
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

import common
from   rsclib.autosuper       import autosuper
from   roundup.cgi.exceptions import Redirect
from   roundup.cgi.actions    import EditItemAction

class Sign_Purchase_Request (EditItemAction, autosuper) :
    """ Sign own purchase request
        Note: This handles all newly-submitted attributes first, then
        the current PR is signed.
    """

    name = 'pr_sign'

    def handle (self) :
        red = None
        try :
            r = self.__super.handle ()
        except Redirect as red :
            pass
        assert self.classname == 'purchase_request'
        cl    = self.db.getclass (self.classname)
        pr    = cl.getnode (self.nodeid)
        uid   = self.db.getuid ()
        st_ud = self.db.pr_approval_status.lookup ('undecided')
        st_ap = self.db.pr_approval_status.lookup ('approved')
        d     = dict (purchase_request = pr.id, status = st_ud, user = uid)
        ap    = dict.fromkeys (self.db.pr_approval.filter (None, d))
        del d ['user']
        d ['deputy'] = uid
        ap.update (dict.fromkeys (self.db.pr_approval.filter (None, d)))
        assert len (ap) == 1
        for a in ap :
            pr_ap = self.db.pr_approval.getnode (a)
            assert pr_ap.user == uid or pr_ap.creator == uid
            assert pr_ap.status == st_ud
            self.db.pr_approval.set (a, status = st_ap)
            self.db.commit ()
            break
        if red is not None :
            raise red
    # end def handle
# end class Sign_Purchase_Request

def supplier_approved (db, context, supplier) :
    """ Return 'approved' if supplier is approved for given organisation.
        If we cannot determine the current status we return an empty
        string. Otherwise 'not approved for organisation' is returned.
    """
    if not context.organisation :
        return ''
    orgname = context.organisation.name
    for org in supplier.organisation :
        if org.id == context.organisation.id :
            if supplier.rating :
                return 'Rating: %s' % str (supplier.rating)
            return 'unknown status'
    return 'not approved for %(orgname)s' % locals ()
# end def supplier_approved

def init (instance) :
    act = instance.registerAction
    act ('pr_sign', Sign_Purchase_Request)
    reg = instance.registerUtil
    reg ('pr_offer_item_sum', common.pr_offer_item_sum)
    reg ('supplier_approved', supplier_approved)
# end def init
