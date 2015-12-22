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
        # FIXME: At some point we want to re-enable department
        #if not dep and tp.department :
        #    new_values ['department'] = dep = tp.department
        if not org and tp.organisation :
            new_values ['organisation'] = org = tp.organisation
    if new_values.get ('requester', None) :
        rq = db.user.getnode (new_values ['requester'])
        # FIXME: At some point we want to re-enable department
        #if not dep and rq.department :
        #    new_values ['department'] = dep = rq.department
        if not org and rq.org_location :
            org = db.org_location.get (rq.org_location, 'organisation')
            new_values ['organisation'] = org
        if nodeid :
            apps = db.pr_approval.filter \
                (None, dict (purchase_request = nodeid))
            assert len (apps) == 1
            db.pr_approval.set (apps [0], user = rq.id)
# end def check_tp_rq

def create_pr_approval (db, cl, nodeid, old_values) :
    user = cl.get (nodeid, 'requester')
    db.pr_approval.create \
        ( order            = 1
        , purchase_request = nodeid
        , user             = user
        , deputy           = cl.get (nodeid, 'creator')
        , description      = "Requester or Creator"
        )
# end def create_pr_approval

def check_requester (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'requester')
# end def check_requester

def currency (db, pr) :
    pr    = db.purchase_request.getnode (pr)
    cur   = None
    for id in pr.offer_items :
        item  = db.pr_offer_item.getnode (id)
        assert item.pr_currency
        if cur and cur != item.pr_currency :
            raise Reject (_ ("All offer items must have same currency"))
        cur = item.pr_currency
    assert cur
    return cur
# end def currency

def change_pr (db, cl, nodeid, new_values) :
    oitems    = new_values.get ('offer_items', cl.get (nodeid, 'offer_items'))
    approvals = db.pr_approval.filter (None, dict (purchase_request = nodeid))
    approvals = [db.pr_approval.getnode (a) for a in approvals]
    ap_appr   = db.pr_approval_status.lookup ('approved')
    ap_rej    = db.pr_approval_status.lookup ('rejected')
    requester = new_values.get ('requester', cl.get (nodeid, 'requester'))
    creator   = cl.get (nodeid, 'creator')
    ost       = cl.get (nodeid, 'status')
    if 'status' in new_values and new_values ['status'] != ost :
        if new_values ['status'] == db.pr_status.lookup ('approving') :
            tc = new_values.get \
                ('time_project', cl.get (nodeid, 'time_project'))
            cc = new_values.get \
                ('sap_cc',  cl.get (nodeid, 'sap_cc'))
            if not tc and not cc :
                raise Reject \
                    (_ ("Need to specify %(tp)s or %(cc)s")
                    % dict (tp = _ ('time_project'), cc = _ ('sap_cc'))
                    )
            if tc and cc :
                raise Reject \
                    (_ ("Either specify %(tp)s or %(cc)s, not both")
                    % dict (tp = _ ('time_project'), cc = _ ('sap_cc'))
                    )
            common.require_attributes \
                ( _, cl, nodeid, new_values
                , 'department',  'organisation'
                , 'offer_items', 'delivery_deadline', 'purchase_type'
                , 'part_of_budget', 'terms_conditions', 'frame_purchase'
                )
            fp = new_values.get \
                ( 'frame_purchase'
                , cl.get (nodeid, 'frame_purchase')
                )
            if fp :
                common.require_attributes \
                    (_, cl, nodeid, new_values, 'frame_purchase_end')
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
                    , 'index'
                    , 'price_per_unit'
                    , 'units'
                    , 'description'
                    , 'pr_currency'
                    , 'vat'
                    )
                oitem = db.pr_offer_item.getnode (oi)
                if oitem.sap_cc and oitem.time_project :
                    raise Reject \
                        (_ ("Either specify %(tp)s or %(cc)s, not both")
                        % dict (tp = _ ('time_project'), cc = _ ('sap_cc'))
                        )
            # Check that approval of requester exists
            for ap in approvals :
                if  (   ap.status == ap_appr
                    and (ap.by == requester or ap.by == creator)
                    ) :
                    break
            else :
                raise Reject ( _ ("No approval by requester found"))
            new_values ['total_cost']  = common.pr_offer_item_sum (db, nodeid)
            new_values ['pr_currency'] = currency (db, nodeid)

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
        elif new_values ['status'] == db.pr_status.lookup ('open') :
            # If setting status to open again we need to retire *all*
            # approvals and re-create the (pending) approval of the
            # requester
            for ap in approvals :
                db.pr_approval.retire (ap.id)
            create_pr_approval (db, cl, nodeid, {})
# end def change_pr

def supplier_is_approved (db, pr, sup_id) :
    if not sup_id :
        return False
    supplier = db.pr_supplier.getnode (sup_id)
    if pr.organisation in supplier.organisation :
        if not supplier.rating :
            return False
        rating = db.pr_supplier_rating.getnode (supplier.rating)
        if rating.order > 2 :
            return False
        return True
    return False
# end def supplier_is_approved

def changed_pr (db, cl, nodeid, old_values) :
    pr  = cl.getnode (nodeid)
    ost = old_values.get ('status', None)
    nst = pr.status
    st_op = db.pr_status.lookup ('open')
    st_ag = db.pr_status.lookup ('approving')
    if ost == st_op and nst == st_ag :
        cur = db.pr_currency.getnode (currency (db, pr.id))
        apr_by_r_d  = {}
        apr_by_role = {}
        if common.pr_offer_item_sum (db, pr.id) > cur.min_sum :
            if pr.time_project :
                pcc = db.time_project.getnode (pr.time_project)
                d   = _ ('%(tp)s responsible/deputy') \
                    % dict (tp = _ ('time_project'))
            else :
                pcc = db.sap_cc.getnode (pr.sap_cc)
                d   = _ ('%(cc)s responsible/deputy') % dict (cc = _ ('sap_cc'))
            apr = db.pr_approval.create \
                ( order            = 10
                , purchase_request = pr.id
                , user             = pcc.responsible
                , deputy           = pcc.deputy
                , description      = d
                )
            apr_by_r_d [(pcc.responsible, pcc.deputy)] = apr
            dep = db.department.getnode (pr.department)
            apr = db.pr_approval.create \
                ( order            = 55
                , purchase_request = pr.id
                , user             = dep.manager
                , deputy           = dep.deputy
                , description      = "Department Head"
                )
            apr_by_r_d [(dep.manager, dep.deputy)] = apr
            add_approval_with_role (db, pr.id, 'Finance')
            pob = db.part_of_budget.getnode (pr.part_of_budget)
            # Loop over order items and check if any is not on the approved
            # suppliers list
            supplier_approved = True
            for id in pr.offer_items :
                oi = db.pr_offer_item.getnode (id)
                if not supplier_is_approved (db, pr, oi.pr_supplier) :
                    supplier_approved = False
            if pr.safety_critical and not supplier_approved :
                add_approval_with_role (db, pr.id, 'Quality')
                apr_by_role ['quality'] = True
            if  (  pob.name.lower () == 'no'
                or common.pr_offer_item_sum (db, pr.id) >= cur.max_sum
                ) :
                add_approval_with_role (db, pr.id, 'Board')
                apr_by_role ['board'] = True
            pt    = db.purchase_type.getnode (pr.purchase_type)
            roles = common.role_list (pt.roles)
            for role in roles :
                add_approval_with_role (db, pr.id, role)
                apr_by_role [role.lower ()] = True
            # Loop over offer items and add additional approvals if
            # needed by specified sap_cc, time_project, or purchase_type
            for id in pr.offer_items :
                oi = db.pr_offer_item.getnode (id)
                pcc = None
                if oi.time_project :
                    pcc = db.time_project.getnode (oi.time_project)
                    d   = _ ('%(tp)s responsible/deputy') \
                        % dict (tp = _ ('time_project'))
                elif oi.sap_cc :
                    pcc = db.sap_cc.getnode (oi.sap_cc)
                    d   = _ ('%(cc)s responsible/deputy') \
                            % dict (cc = _ ('sap_cc'))
                if pcc and (pcc.responsible, pcc.deputy) not in apr_by_r_d :
                    apr = db.pr_approval.create \
                        ( order            = 10 + oi.index * 0.001
                        , purchase_request = pr.id
                        , user             = pcc.responsible
                        , deputy           = pcc.deputy
                        , description      = d
                        )
                    apr_by_r_d [(pcc.responsible, pcc.deputy)] = apr
                if oi.purchase_type :
                    pt    = db.purchase_type.getnode (oi.purchase_type)
                    roles = common.role_list (pt.roles)
                    for role in roles :
                        if role.lower () not in apr_by_role :
                            add_approval_with_role (db, pr.id, role)
                            apr_by_role [role.lower ()] = True
        else :
            req = db.user.getnode (pr.requester)
            sup = db.user.getnode (req.supervisor)
            db.pr_approval.create \
                ( order            = 10
                , purchase_request = pr.id
                , user             = sup.id
                , deputy           = sup.supervisor
                , description      = 'Supervisor'
                )
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

def nosy_for_approval (db, app) :
    nosy = {}
    if app.user :
        nosy [app.user] = 1
    # Don't add deputy to nosy
    if app.role :
        nosy.update (dict.fromkeys (common.get_uids_with_role (db, app.role)))
    return nosy
# end def nosy_for_approval

def fix_nosy (db, cl, nodeid, new_values) :
    nosy = dict.fromkeys (new_values.get ('nosy', cl.get (nodeid, 'nosy')))
    rq   = new_values.get ('requester', cl.get (nodeid, 'requester'))
    chg  = False
    if rq not in nosy :
        nosy [rq] = 1
        chg = True
    # Allow creator to remove her/himself after initial sign&send
    pr_approving = db.pr_status.lookup ('approving')
    if 'status' in new_values and new_values ['status'] == pr_approving :
        cr = cl.get (nodeid, 'creator')
        if cr not in nosy :
            nosy [cr] = 1
            chg = True
    if chg :
        new_values ['nosy'] = nosy.keys ()
# end def fix_nosy

def update_pr (db, pr, ap, nosy, txt, ** kw) :
    uor = ''
    if ap :
        if ap.user :
            uor = db.user.get (ap.user, 'realname')
        if ap.deputy :
            uor += '/' + db.user.get (ap.deputy, 'realname')
        if ap.role :
            if uor :
                uor += ' and role %s' % ap.role
            else :
                uor = 'role %s' % ap.role
    txt = (txt.replace ('$', '%') % dict (title = pr.title, user_or_role = uor))
    # Note: We can't use the current db user as the
    # author of the message, otherwise the nosy auditor
    # will prevent the user from being removed from the
    # nosy list (!)
    msg = db.msg.create \
        ( content = txt
        , author  = '1' # admin
        , date    = Date ('.')
        )
    msgs = dict.fromkeys (pr.messages)
    msgs [msg] = 1
    d = kw
    d.update (nosy = nosy.keys (), messages = msgs.keys ())
    db.purchase_request.set (pr.id, ** d)
# end def update_pr

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
            is_new = False
            if pr.status == pr_open :
                db.purchase_request.set (pr.id, status = pr_approving)
                is_new = True
            srt  = [('+', 'order')]
            apps = cl.filter (None, dict (purchase_request = pr.id), sort = srt)
            nosy = dict.fromkeys (pr.nosy)
            for n in nosy_for_approval (db, app) :
                if n in nosy :
                    del nosy [n]
            if is_new :
                if pr.time_project :
                    id = pr.time_project
                    agent = db.time_project.get (id, 'purchasing_agent')
                else :
                    assert pr.sap_cc
                    agent = db.sap_cc.get (pr.sap_cc, 'purchasing_agent')
                if agent :
                    nosy [agent] = 1
            for a in apps :
                ap = cl.getnode (a)
                if ap.status != apr :
                    assert ap.status == und
                    nosy.update (nosy_for_approval (db, ap))
                    uor = ''
                    update_pr \
                        (db, pr, ap, nosy, db.config.ext.MAIL_PR_APPROVAL_TEXT)
                    break
            else :
                update_pr \
                    ( db
                    , pr
                    , None
                    , nosy
                    , db.config.ext.MAIL_PR_APPROVED_TEXT
                    , status = db.pr_status.lookup ('approved')
                    )
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
    if 'pr_currency' not in new_values :
        # get first currency by 'order' attribute:
        c = db.pr_currency.filter (None, {}, sort = [('+', 'order')])
        if c :
            new_values ['pr_currency'] = c [0]
# end def new_pr_offer_item

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
                p_s  = it.pr_supplier
                midx = it.index
            if it.supplier :
                s    = it.supplier
                midx = it.index
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
# end def check_supplier

def check_currency (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'max_sum', 'order')
# end def check_currency

def requester_chg (db, cl, nodeid, new_values) :
    if 'requester' in new_values :
        st_open = db.pr_status.lookup ('open')
        ost = cl.get (nodeid, 'status')
        if ost != open :
            raise Reject (_ ("Requester may not be changed"))
# end def requester_chg

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
    db.purchase_request.audit ("set",    requester_chg,   priority = 70)
    db.purchase_request.audit ("set",    change_pr)
    db.purchase_request.audit ("set",    fix_nosy)
    db.purchase_request.react ("set",    changed_pr)
    db.purchase_request.react ("create", create_pr_approval)
    db.pr_approval.audit      ("create", new_pr_approval)
    db.pr_approval.audit      ("set",    change_pr_approval)
    db.pr_approval.react      ("set",    approved_pr_approval)
    db.pr_offer_item.audit    ("create", new_pr_offer_item)
    db.pr_offer_item.audit    ("create", check_supplier)
    db.pr_offer_item.audit    ("set",    check_supplier)
    db.pr_currency.audit      ("create", check_currency)
    db.pr_currency.audit      ("set",    check_currency)
# end def init
