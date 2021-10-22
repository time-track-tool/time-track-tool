#! /usr/bin/python
# Copyright (C) 2015-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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

import prlib
import common
import cgi
try :
    from urllib.parse import urlencode
except ImportError :
    from urllib import urlencode
from   rsclib.autosuper       import autosuper
from   roundup.cgi.exceptions import Redirect
from   roundup.cgi.actions    import EditItemAction, NewItemAction, EditCommon
from   roundup.cgi.templating import HTMLClass, _HTMLItem

class PR_Submit (EditCommon, autosuper) :
    """ Remove items that should not create a new offer item from the
        list of offer items. In particular this is done for boolean
        attributes with a yes/no choice.
        Also remove all changes to pr_approval that *only* have a
        message.
    """

    def _editnodes (self, props, links) :
        for (cl, id), val in props.items () :
            if cl == 'pr_offer_item' :
                if int (id) < 0 and list (val) == ['is_asset'] :
                    del props [(cl, id)]
            if cl == 'pr_approval' :
                if list (val) == ['msg'] or list (val) == [] :
                    del props [(cl, id)]
                    # find it in links
                    for n, (c, i, p, r) in enumerate (links [:]) :
                        if c == cl and i == id and p == 'msg' :
                            del links [n]
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
        assert len (ap) <= 1
        if len (ap) < 1 :
            assert common.user_has_role (self.db, uid, 'Procurement-Admin')
            del d ['deputy']
            d ['user'] = pr.requester
            ap = dict.fromkeys (self.db.pr_approval.filter (None, d))
        assert len (ap) == 1
        for a in ap :
            pr_ap = self.db.pr_approval.getnode (a)
            assert \
                (  pr_ap.user == uid
                or pr_ap.creator == uid
                or common.user_has_role (self.db, uid, 'Procurement-Admin')
                )
            assert pr_ap.status == st_ud
            self.db.pr_approval.set (a, status = st_ap)
            self.db.commit ()
            break
        if red is not None :
            raise red
    # end def handle

# end class Sign_Purchase_Request


def supplier_approved (db, context, supplier) :
    """ Return rating string with link to rating if supplier is approved
        for given organisation. Otherwise 'not approved for
        organisation' is returned.
    """
    if not context.organisation :
        return ''
    orgid   = context.organisation.id
    orgname = context.organisation.name
    r = db.pr_supplier_rating.filter \
        (None, dict (supplier = supplier.id, organisation = orgid))
    assert len (r) <= 1
    if len (r) == 1 :
        s = ( 'Rating: %s (<a title="%s" href="pr_supplier_rating%s">Scope</a>)'
            % ( cgi.escape (str (r [0].rating))
              , cgi.escape (str (r [0].scope))
              , r [0].id
              )
            )
        return s
    else :
        return 'not approved for %(orgname)s' % locals ()
# end def supplier_approved

def pr_edit_button (context) :
    if isinstance (context, _HTMLItem) :
        return 'pr_edit'
    elif isinstance (context, HTMLClass) :
        return 'pr_new'
    assert None
# end def pr_edit_button

def pr_filter_status_transitions (db, context) :
    try :
        db = db._db
    except AttributeError :
        pass
    uid   = db.getuid ()
    stati = ['approving', 'approved']
    if not common.user_has_role (db, uid, *prlib.reject_roles) :
        stati.append ('rejected')
    # This filters the stati *out* of the list.
    return common.filter_status_transitions (context, * stati)
# end def pr_filter_status_transitions

def pr_justification () :
    r = []
    for k, v in prlib.pr_justification :
        r.append (': '.join ((k, '(' + v + ')')))
    q = {'@template': 'item', 'pr_justification' : '\r\n'.join (r)}
    return '?' + urlencode (q)
# end def pr_justification

def pr_type_valid_agents (db, pr_type_id) :
    try :
        db = db._db
    except AttributeError :
        pass
    pt = db.purchase_type.getnode (pr_type_id)
    users = set ()
    for rid in pt.pr_view_roles :
        r = db.pr_approval_order.getnode (rid)
        users.update (r.users)
    return list (users)
# end def pr_type_valid_agents

def risk_type (db, offer_item) :
    rid = prlib.risk_type (db._db, offer_item.id)
    if rid :
        return db._db.purchase_risk_type.get (rid, 'name')
    return ''
# end def risk_type

def orig_infosec_level (offer_item) :
    db = offer_item._db
    oi = db.pr_offer_item.getnode (offer_item.id)
    if not oi.product_group :
        return ''
    pg = db.product_group.getnode (oi.product_group)
    if not pg.infosec_level :
        return ''
    il = db.infosec_level.getnode (pg.infosec_level)
    return il.name
# end def orig_infosec_level

def need_psp (context) :
    if not context or not context.id :
        return True
    if context.status.id == context._db.pr_status.lookup ('open') :
        return True
    if context.psp_element :
        return True
    has_sap = bool (context.sap_cc)
    has_tc  = bool (context.time_project)
    for oi in context.offer_items :
        if oi.psp_element :
            return True
        if oi.sap_cc :
            has_sap = True
        if oi.time_project :
            has_tc = True
    if not has_tc :
        #assert (has_sap)
        return True
    return False
# end def need_psp

def init (instance) :
    act = instance.registerAction
    act ('pr_sign', Sign_Purchase_Request)
    act ('pr_edit', Edit_Purchase_Request)
    act ('pr_new',  New_Purchase_Request)
    reg = instance.registerUtil
    reg ('pr_offer_item_sum',            prlib.pr_offer_item_sum)
    reg ('compute_approvals',            prlib.compute_approvals)
    reg ('supplier_approved',            supplier_approved)
    reg ('pr_edit_button',               pr_edit_button)
    reg ('pr_filter_status_transitions', pr_filter_status_transitions)
    reg ('pr_justification',             pr_justification)
    reg ('pr_type_valid_agents',         pr_type_valid_agents)
    reg ('risk_type',                    risk_type)
    reg ('orig_infosec_level',           orig_infosec_level)
    reg ('need_psp',                     need_psp)
# end def init
