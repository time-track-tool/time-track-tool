# -*- coding: iso-8859-1 -*-
# Copyright (C) 2015 Ralf Schlatterbeck. All rights reserved
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

import common
from   roundup.date                   import Date, Interval
from   roundup.exceptions             import Reject
from   roundup.cgi.TranslationService import get_translation

def new_pr (db, cl, nodeid, new_values) :
    if 'requester' not in new_values :
        new_values ['requester'] = db.getuid ()
    new_values ['status'] = db.pr_status.lookup ('open')
# end def new_pr

def check_tp_rq (db, cl, nodeid, new_values) :
    dep = new_values.get ('department',   None)
    org = new_values.get ('organisation', None)
    if nodeid :
        if not dep :
            dep = cl.get (nodeid, 'department')
        if not org :
            org = cl.get (nodeid, 'organisation')
    if new_values.get ('time_project', None) :
        tp  = db.time_project.getnode (new_values ['time_project'])
        if not dep and tp.department :
            new_values ['department'] = dep = tp.department
        if not org and tp.organisation :
            new_values ['organisation'] = org = tp.organisation
    if new_values.get ('requester', None) :
        rq = db.user.getnode (new_values ['requester'])
        if not dep and rq.department :
            new_values ['department'] = dep = rq.department
        if not org and rq.org_location :
            org = db.org_location.get (rq.org_location, 'organisation')
            new_values ['organisation'] = org
        if nodeid :
            apps = db.pr_approval.filter \
                (None, dict (purchase_request = nodeid))
            assert len (apps) <= 1
            if len (apps) == 0 :
                db.pr_approval.create \
                    ( order            = 1
                    , purchase_request = nodeid
                    , user             = rq.id
                    , description      = "Requester"
                    )
            else :
                db.pr_approval.set (apps [0], user = rq.id)
# end def check_tp_rq

def create_pr_approval (db, cl, nodeid, old_values) :
    user = cl.get (nodeid, 'requester')
    db.pr_approval.create \
        ( order            = 1
        , purchase_request = nodeid
        , user             = user
        , description      = "Requester"
        )
# end def create_pr_approval

def check_requester (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'requester')
# end def check_requester

def change_pr (db, cl, nodeid, new_values) :
    oitems    = new_values.get ('offer_items', cl.get (nodeid, 'offer_items'))
    approvals = db.pr_approval.filter (None, dict (purchase_request = nodeid))
    approvals = [db.pr_approval.getnode (a) for a in approvals]
    ap_appr   = db.pr_approval_status.lookup ('approved')
    ap_rej    = db.pr_approval_status.lookup ('rejected')
    requester = new_values.get ('requester', cl.get (nodeid, 'requester'))
    if 'status' in new_values :
        if new_values ['status'] == db.pr_status.lookup ('approving') :
            common.require_attributes \
                ( _, cl, nodeid, new_values
                , 'time_project', 'department',  'organisation'
                , 'offer_items', 'delivery_deadline', 'purchase_type'
                , 'part_of_budget', 'terms_conditions'
                )
            co = new_values.get \
                ( 'continuous_obligation'
                , cl.get (nodeid, 'continuous_obligation')
                )
            if co :
                common.require_attributes \
                    ( _, cl, nodeid, new_values
                    , 'contract_term', 'termination_date'
                    )
            if not oitems :
                raise Reject (_ ("Need at least one offer item"))
            for oi in oitems :
                fix_pr_offer_item (db, db.pr_offer_item, oi, {})
            for oi in oitems :
                common.require_attributes \
                    (_, db.pr_offer_item, oi, {}
                    , 'index', 'offer_number', 'price_per_unit'
                    , 'units', 'description'
                    )
            # Check that approval of requester exists
            for ap in approvals :
                if ap.status == ap_appr and ap.by == requester :
                    break
            else :
                raise Reject ( _ ("No approval by requester found"))
            new_values ['total_cost'] = common.pr_offer_item_sum (db, nodeid)

        elif new_values ['status'] == db.pr_status.lookup ('approved') :
            for ap in approvals :
                if ap.status != ap_appr :
                    raise Reject (_ ("Not all approvals in status approved"))
        elif new_values ['status'] == db.pr_status.lookup ('rejected') :
            for ap in approvals :
                if ap.status == ap_rej :
                    break
            else :
                raise Reject (_ ("No rejected approval-record found"))
# end def change_pr

def changed_pr (db, cl, nodeid, old_values) :
    pr  = cl.getnode (nodeid)
    ost = old_values.get ('status', None)
    nst = pr.status
    st_op = db.pr_status.lookup ('open')
    st_ag = db.pr_status.lookup ('approving')
    if ost == st_op and nst == st_ag :
        tp = db.time_project.getnode (pr.time_project)
        d  = _ ('%(tp)s responsible') % dict (tp = _ ('time_project'))
        db.pr_approval.create \
            ( order            = 10
            , purchase_request = pr.id
            , user             = tp.responsible
            , description      = d
            )
        add_approval_with_role (db, pr.id, 'Finance')
        pob = db.part_of_budget.getnode (pr.part_of_budget)
        if  (  pob.name.lower () == 'no'
            or common.pr_offer_item_sum (db, pr.id) >= 10000
            ) :
            add_approval_with_role (db, pr.id, 'Board')
        pt    = db.purchase_type.getnode (pr.purchase_type)
        roles = common.role_list (pt.roles)
        for role in roles :
            add_approval_with_role (db, pr.id, role)
# end def changed_pr

def new_pr_approval (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'purchase_request', 'order')
    if  (   not new_values.get ('user', None)
        and not new_values.get ('role', None)
        ) :
        raise Reject (_ ("user or role required"))
    new_values ['status'] = db.pr_approval_status.lookup ('undecided')
# end def new_pr_approval

def change_pr_approval (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'purchase_request', 'order')
    app = cl.getnode (nodeid)
    if 'status' in new_values :
        pr_open      = db.pr_status.lookup ('open')
        pr_approving = db.pr_status.lookup ('approving')
        os = app.status
        ns = new_values ['status']
        if os != ns :
            pr = db.purchase_request.getnode (app.purchase_request)
            if pr.status not in (pr_open, pr_approving) :
                raise Reject (_ ("No change of approvals for this PR"))
            new_values ['by']   = db.getuid ()
            new_values ['date'] = Date ('.')
            approvals = cl.filter (None, dict (purchase_request = pr.id))
            assert nodeid in approvals
    elif app.status != db.pr_approval_status.lookup ('undecided') :
        raise Reject (_ ("May not change approval status parameters"))
# end def change_pr_approval

def add_approval_with_role (db, prid, role) :
    oid = db.pr_approval_order.lookup (role.lower ())
    ord = db.pr_approval_order.getnode (oid)
    db.pr_approval.create \
        ( order            = ord.order
        , purchase_request = prid
        , role             = role.lower ()
        , description      = role
        )
# end def add_approval_with_role

def approved_pr_approval (db, cl, nodeid, old_values) :
    app = cl.getnode (nodeid)
    os  = old_values.get ('status', None)
    ns  = app.status
    apr = db.pr_approval_status.lookup ('approved')
    rej = db.pr_approval_status.lookup ('rejected')
    und = db.pr_approval_status.lookup ('undecided')
    pr_open      = db.pr_status.lookup ('open')
    pr_approving = db.pr_status.lookup ('approving')
    if os != ns :
        pr = db.purchase_request.getnode (app.purchase_request)
        if ns == apr :
            if pr.status == pr_open :
                db.purchase_request.set (pr.id, status = pr_approving)
            apps = cl.filter (None, dict (purchase_request = pr.id))
            for a in apps :
                ap = cl.getnode (a)
                if ap.status != apr :
                    assert ap.status == und
                    break
            else :
                db.purchase_request.set \
                    (pr.id, status = db.pr_status.lookup ('approved'))
        elif ns == rej :
            d = dict (status = db.pr_status.lookup ('rejected'))
            msg = app.msg
            prm = dict.fromkeys (pr.messages)
            if msg :
                # Depending on form evaluation order msg may already
                # have been set in the same transaction. Remove it
                # to set it together with state-change otherwise we
                # get a reject due to missing msg later on.
                if msg in prm :
                    del prm [msg]
                    db.purchase_request.set (pr.id, messages = prm.keys ())
                prm [msg] = 1
                d ['messages'] = prm.keys ()
            db.purchase_request.set (pr.id, ** d)
# end def approved_pr_approval

def new_pr_offer_item (db, cl, nodeid, new_values) :
    if 'units' not in new_values :
        new_values ['units'] = 1
# end def check_pr_offer_item

def fix_pr_offer_item (db, cl, nodeid, new_values) :
    """ Fix missing info of offer_item from previous lines
    """
    item = db.pr_offer_item.getnode (nodeid)
    prs  = db.purchase_request.filter (None, dict (offer_items = nodeid))
    assert len (prs) == 1
    pr   = db.purchase_request.getnode (prs [0])
    d    = {}
    idx  = new_values.get ('index', item.index)
    if idx is None :
        idx = 0
        for id in pr.offer_items :
            it = db.pr_offer_item.getnode (id)
            if it.index :
                idx = max (idx, it.index)
        d ['index'] = idx + 1
        idx = d ['index']
    p_s = new_values.get ('pr_supplier', item.pr_supplier)
    s   = new_values.get ('supplier',    item.supplier)
    if p_s is None and not s :
        midx = 0
        for id in pr.offer_items :
            it = db.pr_offer_item.getnode (id)
            if it.index is None or it.index > idx or it.index < midx :
                continue
            if it.pr_supplier :
                p_s = it.pr_supplier
                max = it.index
            if it.supplier :
                s = it.supplier
                max = it.index
        if p_s :
            d ['pr_supplier'] = p_s
        if s :
            d ['supplier'] = s
    if d :
        db.pr_offer_item.set (nodeid, **d)
# end def fix_pr_offer_item

def check_supplier (db, cl, nodeid, new_values) :
    if 'supplier' in new_values :
        prsup = None
        try :
            prsup = db.pr_supplier.lookup (new_values ['supplier'])
            new_values ['pr_supplier'] = prsup
        except KeyError :
            new_values ['pr_supplier'] = None
            pass
        if prsup :
            vc = db.pr_supplier.get (prsup, 'vat_country')
            if vc :
                new_values ['vat_country'] = vc
# end def check_supplier

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    if 'purchase_request' not in db.classes :
        return
    db.purchase_type.audit    ("create", common.check_roles)
    db.purchase_type.audit    ("set",    common.check_roles)
    db.purchase_request.audit ("create", new_pr,          priority = 50)
    db.purchase_request.audit ("set",    check_requester, priority = 50)
    db.purchase_request.audit ("create", check_tp_rq,     priority = 80)
    db.purchase_request.audit ("set",    check_tp_rq,     priority = 80)
    db.purchase_request.audit ("set",    change_pr)
    db.purchase_request.react ("set",    changed_pr)
    db.purchase_request.react ("create", create_pr_approval)
    db.pr_approval.audit      ("create", new_pr_approval)
    db.pr_approval.audit      ("set",    change_pr_approval)
    db.pr_approval.react      ("set",    approved_pr_approval)
    db.pr_offer_item.audit    ("create", new_pr_offer_item)
    db.pr_offer_item.audit    ("create", check_supplier)
    db.pr_offer_item.audit    ("set",    check_supplier)
# end def init
