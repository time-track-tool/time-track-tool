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
from   roundup.cgi.actions    import EditItemAction, NewItemAction, EditCommon
from   roundup.cgi.templating import HTMLClass, _HTMLItem

class PR_Submit (EditCommon, autosuper) :
    """ Remove items that should not create a new offer item from the
        list of offer items. In particular this is done for boolean
        attributes with a yes/no choice.
    """

    def _editnodes (self, props, links) :
        for (cl, id), val in props.items () :
            if cl == 'pr_offer_item' :
                if int (id) < 0 and val.keys () == ['is_asset'] :
                    del props [(cl, id)]
        return EditCommon._editnodes (self, props, links)
    # end def _editnodes

# end class PR_Submit

class Edit_Purchase_Request (EditItemAction, PR_Submit) :
    def _editnodes (self, props, links) :
        return PR_Submit._editnodes (self, props, links)
    # end def _editnodes
# end class Edit_Purchase_Request

class New_Purchase_Request (NewItemAction, PR_Submit) :
    def _editnodes (self, props, links) :
        return PR_Submit._editnodes (self, props, links)
    # end def _editnodes
# end class New_Purchase_Request

class Sign_Purchase_Request (Edit_Purchase_Request, autosuper) :
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
    for rating in supplier.ratings :
        if rating.organisation.id == context.organisation.id :
            return 'Rating: %s' % str (rating.rating)
    return 'not approved for %(orgname)s' % locals ()
# end def supplier_approved

def pr_edit_button (context) :
    if isinstance (context, _HTMLItem) :
        return 'pr_edit'
    elif isinstance (context, HTMLClass) :
        return 'pr_new'
    assert None
# end def pr_edit_button

def init (instance) :
    act = instance.registerAction
    act ('pr_sign',           Sign_Purchase_Request)
    act ('pr_edit',           Edit_Purchase_Request)
    act ('pr_new',            New_Purchase_Request)
    reg = instance.registerUtil
    reg ('pr_offer_item_sum', common.pr_offer_item_sum)
    reg ('supplier_approved', supplier_approved)
    reg ('pr_edit_button',    pr_edit_button)
# end def init
