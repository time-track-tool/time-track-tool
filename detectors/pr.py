# -*- coding: iso-8859-1 -*-
# Copyright (C) 2015-18 Ralf Schlatterbeck. All rights reserved
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
import prlib
from   roundup.date                   import Date, Interval
from   roundup.exceptions             import Reject
from   roundup.cgi.TranslationService import get_translation

def prjust (db, cl, nodeid, new_values) :
    """ Field pr_justification must be edited when signing
    """
    pjn = 'pr_justification'
    fn  = _ (pjn)
    pj  = new_values.get (pjn, cl.get (nodeid, pjn))
    if pj :
        for k, v in prlib.pr_justification :
            if v in pj :
                raise Reject (_ ("You must edit %(fn)s") % locals ())
# end def prjust

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
        if  (   not org
            and tp.organisation
            and db.organisation.get (tp.organisation, 'may_purchase')
            ) :
            new_values ['organisation'] = org = tp.organisation
    if new_values.get ('sap_cc', None) :
        sc  = db.sap_cc.getnode (new_values ['sap_cc'])
        if  (   not org
            and sc.organisation
            and db.organisation.get (sc.organisation, 'may_purchase')
            ) :
            new_values ['organisation'] = org = sc.organisation
    if new_values.get ('requester', None) :
        rq = db.user.getnode (new_values ['requester'])
        # FIXME: At some point we want to re-enable department
        #if not dep and rq.department :
        #    new_values ['department'] = dep = rq.department
        if not org and rq.org_location :
            org = db.org_location.get (rq.org_location, 'organisation')
            if db.organisation.get (org, 'may_purchase') :
                new_values ['organisation'] = org
        if nodeid :
            apps = db.pr_approval.filter \
                (None, dict (purchase_request = nodeid))
            assert len (apps) == 1
            db.pr_approval.set (apps [0], user = rq.id)
    if 'organisation' in new_values :
        org = db.organisation.getnode (new_values ['organisation'])
        if not org.may_purchase :
            o = _ ('organisation')
            oname = org.name
            raise Reject (_ ("%(o)s %(oname)s may not purchase") % locals ())
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

def reopen (db, cl, nodeid, new_values) :
    """ Must happen before change_pr below, to correctly retire old
        approvals.
    """
    ost = cl.get (nodeid, 'status')
    if ost == db.pr_status.lookup ('rejected') and 'status' not in new_values :
        new_values ['status'] = db.pr_status.lookup ('open')
# end def reopen

def check_io (db, cl, nodeid, new_values) :
    """ Check that internal_order isn't specified together with time
        category, but only if the PR isn't in status open (not yet
        submitted with sign&send).
    """
    st = new_values.get ('status', cl.get (nodeid, 'status'))
    if st == db.pr_status.lookup ('open') :
        return
    if 'internal_order' in new_values :
        io = new_values ['internal_order']
        tc = new_values.get ('time_project', cl.get (nodeid, 'time_project'))
        if tc and io :
            raise Reject \
                (_ ("Specify %(cc)s not %(tp)s with %(io)s")
                % dict
                    ( tp = _ ('time_project')
                    , cc = _ ('sap_cc')
                    , io = _ ('internal_order')
                    )
                )
# end def check_io

def check_input_len (db, cl, nodeid, new_values) :
    """ Check that some fields don't become too long
    """
    if len (new_values.get ('supplier', '')) > 55 :
        raise Reject (_ ("Supplier too long (max 55)"))
# end def check_input_len

def namelen (db, cl, nodeid, new_values) :
    """ Check that name field doesn't become too long
    """
    if len (new_values.get ('name', '')) > 55 :
        raise Reject (_ ("Supplier name too long (max 55)"))
# end def namelen

def check_tp_cc_consistency (db, cl, nodeid, new_values) :
    """ Check that the organisation in tp or cc is correct and
        consistent with the organisation stored in the PR.
    """
    pr = cl.getnode (nodeid)
    tc = new_values.get ('time_project', pr.time_project)
    cc = new_values.get ('sap_cc', pr.sap_cc)
    if tc :
        node = db.time_project.getnode (tc)
    else :
        node = db.sap_cc.getnode (cc)
    if node.organisation != pr.organisation :
        o1 = db.organisation.get (pr.organisation, 'name')
        if not node.organisation :
            raise Reject (_ ("Organisation of CC/TC is empty"))
        o2 = db.organisation.get (node.organisation, 'name')
        raise Reject \
            ( _("Organisation must be consistent with CC/TC: got %s expect %s")
            % (o1, o2)
            )
# end def check_tp_cc_consistency

def update_nosy (db, cl, nodeid, new_values) :
    """ On sign&send of a PR we update the nosy list with the nosy list
        from the purchase_type
    """
    nosy = set (new_values.get ('nosy', cl.get (nodeid, 'nosy')))
    pt   = new_values.get ('purchase_type', cl.get (nodeid, 'purchase_type'))
    nosy.update (db.purchase_type.get (pt, 'nosy'))
    new_values ['nosy'] = nosy
# end def update_nosy

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
            # check that pr_justification is given
            prjust (db, cl, nodeid, new_values)
            io = new_values.get \
                ('internal_order', cl.get (nodeid, 'internal_order'))
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
            if tc and io :
                raise Reject \
                    (_ ("Specify %(cc)s not %(tp)s with %(io)s")
                    % dict
                        ( tp = _ ('time_project')
                        , cc = _ ('sap_cc')
                        , io = _ ('internal_order')
                        )
                    )
            common.require_attributes \
                ( _, cl, nodeid, new_values
                , 'department',  'organisation'
                , 'offer_items', 'delivery_deadline', 'purchase_type'
                , 'part_of_budget', 'terms_conditions', 'frame_purchase'
                , 'pr_currency'
                )
            dep = new_values.get ('department', cl.get (nodeid, 'department'))
            if dep and db.department.is_retired (dep) :
                raise Reject (_ ("Department no longer valid"))
            sapcc = new_values.get ('sap_cc', cl.get (nodeid, 'sap_cc'))
            if sapcc and db.sap_cc.is_retired (sapcc) :
                raise Reject (_ ("SAP Cost-Center no longer valid"))
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
                    , 'contract_term', 'intended_duration'
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
                    , 'vat'
                    )
                oitem = db.pr_offer_item.getnode (oi)
                if oitem.sap_cc and oitem.time_project :
                    raise Reject \
                        (_ ("Either specify %(tp)s or %(cc)s, not both")
                        % dict (tp = _ ('time_project'), cc = _ ('sap_cc'))
                        )
                if oitem.time_project and io :
                    raise Reject \
                        (_ ("Specify %(cc)s not %(tp)s with %(io)s")
                        % dict
                            ( tp = _ ('time_project')
                            , cc = _ ('sap_cc')
                            , io = _ ('internal_order')
                            )
                        )
            # Check that approval of requester exists
            for ap in approvals :
                if  (   ap.status == ap_appr
                    and (ap.by == requester or ap.by == creator)
                    ) :
                    break
                # Allow approval by procurement-admin instead of
                # requester/creator
                if  (   ap.status == ap_appr
                    and common.user_has_role (db, ap.by, 'Procurement-Admin')
                    ) :
                    break
            else :
                raise Reject ( _ ("No approval by requester found"))
            new_values ['total_cost']  = prlib.pr_offer_item_sum (db, nodeid)
            check_tp_cc_consistency (db, cl, nodeid, new_values)
            update_nosy (db, cl, nodeid, new_values)

        elif new_values ['status'] == db.pr_status.lookup ('approved') :
            for ap in approvals :
                if ap.status != ap_appr :
                    raise Reject (_ ("Not all approvals in status approved"))
        elif new_values ['status'] == db.pr_status.lookup ('rejected') :
            for ap in approvals :
                if ap.status == ap_rej :
                    break
            else :
                uid = db.getuid ()
                if not common.user_has_role (db, uid, 'Procurement-Admin') :
                    raise Reject (_ ("No rejected approval-record found"))
        elif new_values ['status'] == db.pr_status.lookup ('open') :
            # If setting status to open again we need to retire *all*
            # approvals and re-create the (pending) approval of the
            # requester
            if ost != db.pr_status.lookup ('rejected') :
                raise Reject ("Invalid status change to open")
            for ap in approvals :
                db.pr_approval.retire (ap.id)
            create_pr_approval (db, cl, nodeid, {})
            # We also need to set the total cost to None
            new_values ['total_cost'] = None
# end def change_pr

def set_agents (db, cl, nodeid, new_values) :
    """ Set purchasing agents if agents empty (or would become empty)
        or the sap_cc or time_project changed
        *and* we can set the agent from the tc or cc.
        We also update the nosy list whenever purchasing_agents changes.
    """
    pr = None
    if nodeid :
        pr = cl.getnode (nodeid)
    pa = new_values.get ('purchasing_agents', None)
    if pr and not pa :
        pa = pr.purchasing_agents
    if not pa or 'time_project' in new_values or 'sap_cc' in new_values :
        tc = new_values.get ('time_project')
        cc = new_values.get ('sap_cc')
        if not tc and not cc and pr :
            tc = pr.time_project
            cc = pr.sap_cc
        if tc :
            tc = db.time_project.getnode (tc)
        if cc :
            cc = db.sap_cc.getnode (cc)
        item = tc or cc
        if item :
            new_values ['purchasing_agents'] = item.purchasing_agents
            # Add agent to nosy list
    if new_values.get ('purchasing_agents') :
        nosy = new_values.get ('nosy')
        if not nosy and pr :
            nosy = pr.nosy
        nosy = dict.fromkeys (nosy or [])
        for i in new_values ['purchasing_agents'] :
            nosy [i] = 1
        new_values ['nosy'] = nosy.keys ()
# end def set_agents

def approvalchange (db, cl, nodeid, new_values) :
    if 'special_approval' not in new_values :
        return
    status = new_values.get ('status', cl.get (nodeid, 'status'))
    # In state open we do nothing at this point, the special approvals
    # will be processed later, in other states change of approvals is no
    # longer possible.
    if status == db.pr_status.lookup ('open') :
        return
    if status != db.pr_status.lookup ('approving') :
        raise Reject (_ ("Approval change only in state open and approving"))
    sa  = set (new_values ['special_approval'])
    osa = set (cl.get (nodeid, 'special_approval'))
    if osa - sa :
        raise Reject (_ ("Cannot remove users from approval list"))
    for uid in sa - osa :
        prlib.gen_pr_approval \
            ( db, True
            , purchase_request = nodeid
            , user             = uid
            , order            = 15
            , description      = _ ("Special approval")
            )
# end def approvalchange

def check_late_changes (db, cl, nodeid, new_values) :
    """ Check that attributes changed late in the process are consistent
    """
    if 'continuous_obligation' in new_values :
        co = new_values ['continuous_obligation']
        if co :
            common.require_attributes \
                ( _, cl, nodeid, new_values
                , 'contract_term', 'intended_duration'
                )
    if 'frame_purchase' in new_values :
        fp = new_values ['frame_purchase']
        if fp :
            common.require_attributes \
                (_, cl, nodeid, new_values, 'frame_purchase_end')
# end def check_late_changes

def changed_pr (db, cl, nodeid, old_values) :
    pr  = cl.getnode (nodeid)
    ost = old_values.get ('status', None)
    nst = pr.status
    st_op = db.pr_status.lookup ('open')
    st_ag = db.pr_status.lookup ('approving')
    if ost == st_op and nst == st_ag :
        prlib.compute_approvals (db, pr, True)
# end def changed_pr

def new_pr_approval (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'purchase_request', 'order')
    if  (   not new_values.get ('user', None)
        and not new_values.get ('role', None)
        ) :
        raise Reject (_ ("user or role required"))
    if 'role' in new_values and 'role_id' not in new_values :
        raise Reject (_ ("No role id"))
    new_values ['status'] = db.pr_approval_status.lookup ('undecided')
# end def new_pr_approval

def change_pr_approval (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'purchase_request', 'order')
    app = cl.getnode (nodeid)
    rol = new_values.get ('role',    cl.get (nodeid, 'role'))
    rid = new_values.get ('role_id', cl.get (nodeid, 'role_id'))
    if rol and not rid :
        new_values ['role_id'] = db.pr_approval_order.lookup (rol)
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
    elif new_values.keys () == ['role_id'] :
        n = db.pr_approval_order.get (new_values ['role_id'], 'role')
        if cl.get (nodeid, 'role') != n :
            raise Reject ("Inconsistent role_id")
    elif app.status != db.pr_approval_status.lookup ('undecided') :
        raise Reject (_ ("May not change approval status parameters"))
    elif 'msg' in new_values and new_values ['msg'] is not None :
        # Don't link random message to approval if status isn't changing
        del new_values ['msg']
# end def change_pr_approval

def nosy_for_approval (db, app, add = False) :
    nosy = {}
    if app.user :
        nosy [app.user] = 1
    # Don't add deputy to nosy
    nosy_dd = {}
    if app.role_id :
        ao = db.pr_approval_order.getnode (app.role_id)
        nosy_dd = ao.users
    elif app.role :
        nosy_dd = common.get_uids_with_role (db, app.role)
        # If we're adding users, filter by unwanted messages
    if add and nosy_dd :
        nosy_dd = dict.fromkeys \
            (u for u in nosy_dd if not db.user.get (u, 'want_no_messages'))
    nosy.update (dict.fromkeys (nosy_dd))
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
            pt = db.purchase_type.getnode (pr.purchase_type)
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
                agents = pr.purchasing_agents
                if agents and not pt.confidential :
                    nosy.update (dict.fromkeys (agents))
            for a in apps :
                ap = cl.getnode (a)
                if ap.status != apr :
                    assert ap.status == und
                    nosy.update (nosy_for_approval (db, ap, add = True))
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
    if 'vat' not in new_values :
        new_values ['vat'] = 0
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

def check_pr_update (db, cl, nodeid, old_values) :
    """ When changing an offer item check if the PR is in status
        'rejected', if so, set it to 'open'. This will trigger some
        actions including resetting the total_cost to None.
    """
    rej = db.pr_status.lookup ('rejected')
    opn = db.pr_status.lookup ('open')
    ids = db.purchase_request.filter (None, dict (offer_items = nodeid))
    assert len (ids) == 1
    id  = ids [0]
    pr  = db.purchase_request.getnode (id)
    if pr.status == rej :
        db.purchase_request.set (id, status = opn)
# end def check_pr_update

def check_currency (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'min_sum', 'order', 'exchange_rate')
    if new_values.get ('key_currency') :
        for id in db.pr_currency.getnodeids () :
            if id == nodeid :
                continue
            if cl.get (id, 'key_currency') :
                raise Reject (_ ("Duplicate key currency"))
# end def check_currency

def requester_chg (db, cl, nodeid, new_values) :
    if 'requester' in new_values :
        st_rej  = db.pr_status.lookup ('rejected')
        st_open = db.pr_status.lookup ('open')
        ost = cl.get (nodeid, 'status')
        if ost != st_open and ost != st_rej :
            raise Reject (_ ("Requester may not be changed"))
# end def requester_chg

def pt_check_roles (db, cl, nodeid, new_values) :
    common.check_roles (db, cl, nodeid, new_values)
    common.check_roles (db, cl, nodeid, new_values, 'view_roles')
    common.check_roles (db, cl, nodeid, new_values, 'forced_roles')
# end def pt_check_roles

def pao_check_roles (db, cl, nodeid, new_values) :
    """ Now allow the role-name to not be a roundup role anymore """
    if 'role' in new_values and ',' in new_values ['role'] :
        raise Reject (_ ("No commas allowed in role name"))
# end def pao_check_roles

def check_supplier_rating (db, cl, nodeid, new_values) :
    """ Check ratings of supplier: each organisation may occur only once
    """
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'rating', 'organisation', 'supplier', 'scope'
        )
    org = new_values.get ('organisation')
    sup = new_values.get ('supplier')
    if not org :
        org = cl.get (nodeid, 'organisation')
    if not sup :
        sup = cl.get (nodeid, 'supplier')
    common.check_unique \
        ( _, cl, nodeid
        , supplier     = sup
        , organisation = org
        )
# end def check_supplier_rating

def check_no_change (db, cl, nodeid, new_values) :
    if new_values and new_values.keys () != ['name'] :
        classname = cl.classname
        raise Reject (_ ("%(classname)s may not be changed" % locals ()))
# end def check_no_change

def check_dd (db, cl, nodeid, new_values) :
    if 'delivery_deadline' in new_values :
        now = Date ('.')
        if new_values ['delivery_deadline'] < now :
            d = dict (deadline = _ ('delivery_deadline'))
            raise Reject (_ ("%(deadline)s may not be in the past") % d)
# end def check_dd

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    if 'purchase_request' not in db.classes :
        return
    db.purchase_type.audit      ("create", pt_check_roles)
    db.purchase_type.audit      ("set",    pt_check_roles)
    db.purchase_request.audit   ("create", new_pr,          priority = 50)
    db.purchase_request.audit   ("set",    check_requester, priority = 50)
    db.purchase_request.audit   ("create", check_tp_rq,     priority = 80)
    db.purchase_request.audit   ("set",    check_tp_rq,     priority = 80)
    db.purchase_request.audit   ("set",    requester_chg,   priority = 70)
    db.purchase_request.audit   ("set",    reopen,          priority = 90)
    db.purchase_request.audit   ("set",    change_pr)
    db.purchase_request.audit   ("set",    fix_nosy)
    db.purchase_request.audit   ("set",    check_late_changes)
    db.purchase_request.audit   ("create", check_dd)
    db.purchase_request.audit   ("set",    check_dd)
    db.purchase_request.audit   ("create", set_agents,      priority = 150)
    db.purchase_request.audit   ("set",    set_agents,      priority = 150)
    db.purchase_request.audit   ("set",    approvalchange)
    db.purchase_request.react   ("set",    changed_pr)
    db.purchase_request.react   ("create", create_pr_approval)
    db.purchase_request.audit   ("set",    check_io)
    db.pr_approval.audit        ("create", new_pr_approval)
    db.pr_approval.audit        ("set",    change_pr_approval)
    db.pr_approval.react        ("set",    approved_pr_approval)
    db.pr_offer_item.audit      ("create", new_pr_offer_item)
    db.pr_offer_item.audit      ("create", check_supplier)
    db.pr_offer_item.audit      ("set",    check_supplier)
    db.pr_offer_item.react      ("set",    check_pr_update)
    db.pr_offer_item.audit      ("create", check_input_len, priority = 150)
    db.pr_offer_item.audit      ("set",    check_input_len, priority = 150)
    db.pr_currency.audit        ("create", check_currency)
    db.pr_currency.audit        ("set",    check_currency)
    db.pr_approval_order.audit  ("create", pao_check_roles)
    db.pr_approval_order.audit  ("set",    pao_check_roles)
    db.pr_supplier_rating.audit ("set",    check_supplier_rating)
    db.pr_supplier.audit        ("create", namelen)
    db.pr_supplier.audit        ("set",    namelen)
# end def init
