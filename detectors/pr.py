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

import re
import common
import prlib
from   roundup.date                   import Date, Interval
from   roundup.exceptions             import Reject
from   roundup.cgi.TranslationService import get_translation
from   roundup                        import roundupdb

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
    if 'payment_type' not in new_values :
        new_values ['payment_type'] = '1'
# end def new_pr

def check_psp_cc (db, cl, nodeid, new_values) :
    """ Check concerning psp_element, sap_cc, organisation
    """
    dep = new_values.get ('department',   None)
    org = new_values.get ('organisation', None)
    if nodeid :
        if not dep :
            dep = cl.get (nodeid, 'department')
        if not org :
            org = cl.get (nodeid, 'organisation')
    if new_values.get ('psp_element', None) :
        psp = db.psp_element.getnode (new_values ['psp_element'])
        if  (   not org
            and db.organisation.get (psp.organisation, 'may_purchase')
            ) :
            new_values ['organisation'] = org = psp.organisation
        new_values ['time_project'] = psp.project
    elif new_values.get ('time_project', None) :
        # Change of time_project without psp change
        if not nodeid or not cl.get (nodeid, 'psp_element') :
            raise Reject ("Need PSP element not Time Category")
        psp = cl.get (nodeid, "psp_element")
        new_values ["time_project"] = psp.project
    if new_values.get ('sap_cc', None) :
        sc  = db.sap_cc.getnode (new_values ['sap_cc'])
        if  (   not org
            and sc.organisation
            and db.organisation.get (sc.organisation, 'may_purchase')
            ) :
            new_values ['organisation'] = org = sc.organisation
        # Legacy: If no psp element but we *do* have a time_project, reset it
        if  (   'time_project' not in new_values
            and 'psp_element' not in new_values
            and nodeid
            and cl.get (nodeid, 'time_project')
            and not cl.get (nodeid, 'psp_element')
            ) :
            new_values ['time_project'] = None
    if new_values.get ('requester', None) :
        rq = db.user.getnode (new_values ['requester'])
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
# end def check_psp_cc

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
        Note that we ignore some attribute changes that do *not* cause a
        reopen of an issue.
    """
    changed   = set (new_values.keys ())
    no_reopen = set (('messages', 'nosy'))
    if not (changed - no_reopen) :
        return
    ost = cl.get (nodeid, 'status')
    rej = db.pr_status.lookup ('rejected')
    opn = db.pr_status.lookup ('open')
    if ost == rej and 'status' not in new_values :
        new_values ['status'] = opn
    if ost == rej and new_values ['status'] == opn :
        new_values ['date_ordered']       = None
        new_values ['date_approved']      = None
        new_values ['infosec_level']      = None
        new_values ['purchase_risk_type'] = None
# end def reopen

def check_io_pr (db, cl, nodeid, new_values) :
    """ Check that internal_order isn't specified together with time
        category and psp_element, but only if the PR isn't in status
        open (not yet submitted with sign&send).
    """
    st = new_values.get ('status', cl.get (nodeid, 'status'))
    if st == db.pr_status.lookup ('open') :
        return
    if 'internal_order' in new_values :
        pr  = cl.getnode (nodeid)
        io  = new_values ['internal_order']
        tc  = new_values.get ('time_project', pr.time_project)
        psp = new_values.get ('psp_element',  pr.psp_element)
        if tc and io or psp and io :
            raise Reject \
                (_ ("Specify %(cc)s not %(psp)s with %(io)s")
                % dict
                    ( psp = _ ('psp_element')
                    , cc  = _ ('sap_cc')
                    , io  = _ ('internal_order')
                    )
                )
# end def check_io_pr

def check_io_oi (db, cl, nodeid, new_values) :
    pr  = get_pr_from_offer_item (db, nodeid)
    if not pr :
        return
    if pr.status == db.pr_status.lookup ('open') :
        return
    if  (   'internal_order' not in new_values
        and 'time_project'   not in new_values
        and 'psp_element'    not in new_values
        ) :
        return
    oi  = cl.getnode (nodeid)
    io  = new_values.get ('internal_order', oi.internal_order)
    tc  = new_values.get ('time_project',   oi.time_project)
    psp = new_values.get ('psp_element',    oi.psp_element)
    if  (  (tc  or pr.time_project) and (io or pr.internal_order)
        or (psp or pr.psp_element)  and (io or pr.internal_order)
        ) :
        raise Reject \
            (_ ("Specify %(cc)s not %(tp)s with %(io)s")
            % dict
                ( tp = _ ('time_project')
                , cc = _ ('sap_cc')
                , io = _ ('internal_order')
                )
            )
# end def check_io_oi

def check_psp_tc (db, cl, nodeid, new_values) :
    """ If psp changes, also update tc
    """
    node = None
    if nodeid :
        node = cl.getnode (nodeid)
    pspid = new_values.get ('psp_element')
    if pspid is None and node :
        pspid = node.psp_element
    if not pspid :
        return
    psp = db.psp_element.getnode (pspid)
    if 'time_project' in new_values or node and node.time_project is None :
        new_values ['time_project'] = psp.project
# end def check_psp_tc

def check_supplier_change (db, cl, nodeid, new_values) :
    """ Allow change of supplier unconditionally if not yet approving
        Later we check that the maximum risk type will not change.
        We compute the maximum risk type over all offer items.
        Then we compute the risk type that would result from the change.
        If this is below the computed maximum risk type we allow the
        change.
    """
    if 'supplier' not in new_values :
        return
    pr  = get_pr_from_offer_item (db, nodeid)
    if not pr :
        return
    if pr.status == db.pr_status.lookup ('open') :
        return
    # Compute the new risk-type and check if it's allowed
    # Return immediately if no risk
    supplier = new_values ['pr_supplier']
    # So the appropriate risk is computed we need to specify an unknown
    # supplier if None was found
    if supplier is None :
        supplier = '-1'
    nrt = prlib.risk_type (db, nodeid, supplier)
    if not nrt :
        return
    nrt = db.purchase_risk_type.getnode (nrt)
    if nrt.name == 'Do not purchase' :
        raise Reject ( _ ('Purchasing risk would be "%s"') % nrt.name)

    # Search for an infosec approval, if we find one and it is not yet
    # approved we allow all supplier changes.
    ap_approved = db.pr_approval_status.lookup ('approved')
    infosec_roles = []
    cur  = db.pr_currency.getnode (pr.pr_currency)
    cost = pr.total_cost * 1.0 / cur.exchange_rate
    prc_ids = db.pr_approval_config.filter (None, dict (valid = True))
    for prcid in prc_ids :
        prc = db.pr_approval_config.getnode (prcid)
        if prc.infosec_amount is None :
            continue
        # Only if we expect an approval due to costs
        if cost >= prc.infosec_amount :
            infosec_roles.append (prc.role)
    if not infosec_roles :
        return

    # Loop over approvals and check if we find an unapproved infosec
    # approval
    aps = db.pr_approval.filter (None, dict (purchase_request = pr.id))
    for apid in aps :
        ap = db.pr_approval.getnode (apid)
        if ap.role_id in infosec_roles :
            # If we find an infosec approval which is still unapproved
            # we do not need to check further
            if ap.status != ap_approved :
                return
    # We either found only approved infosec approvals or none.
    # In both cases we need to check.
    # If no approval was found, a change in purchasing risk might
    # require an approval. We're currently not prepared to add one.

    mrt = prlib.max_risk_type (db, pr.id)
    if nrt.order > mrt.order :
        raise Reject \
            ( _ ('Supplier change would increase purchasing risk '
                 'from "%s" to "%s"'
                )
            % (mrt.name, nrt.name)
            )
# end def check_supplier_change

def check_input_len (db, cl, nodeid, new_values) :
    """ Check that some fields don't become too long
    """
    if len (new_values.get ('supplier', '') or '') > 55 :
        raise Reject (_ ("Supplier too long (max 55)"))
# end def check_input_len

def get_pr_from_offer_item (db, nodeid) :
    ids = db.purchase_request.filter (None, dict (offer_items = nodeid))
    # Happens on retire or unlink
    if len (ids) < 1 :
        return None
    assert len (ids) == 1
    id  = ids [0]
    pr  = db.purchase_request.getnode (id)
    return pr
# end def get_pr_from_offer_item

def update_payment_approval (db, pr) :
    cur = db.pr_currency.getnode (pr.pr_currency)
    s = prlib.pr_offer_item_sum (db, pr.id)
    s = s * 1.0 / cur.exchange_rate
    prc_ids = db.pr_approval_config.filter (None, dict (valid = True))
    for prcid in prc_ids :
        prc = db.pr_approval_config.getnode (prcid)
        if  (   prc.payment_type_amount is not None
            and s > prc.payment_type_amount
            ) :
            # Search this role in approvals
            aps = db.pr_approval.filter (None, dict (purchase_request = pr.id))
            for apid in aps :
                ap = db.pr_approval.getnode (apid)
                if ap.role_id == prc.role :
                    break
            else :
                prlib.add_approval_with_role (db, True, pr.id, prc.role)
                break
# end def update_payment_approval

def check_payment_type (db, cl, nodeid, new_values) :
    """ When payment type changes:
        - Do nothing if not in state approving (state open is handled
          elsewhere)
        - Do not allow if in state >= approved
        - If already approving, check if we need to add new approval
    """
    if 'payment_type' not in new_values :
        return
    pr  = get_pr_from_offer_item (db, nodeid)
    if not pr :
        return
    ptdefault = pr.payment_type or '1'
    # Allow change for open and approving
    opn = db.pr_status.lookup ('open')
    ap  = db.pr_status.lookup ('approving')
    if pr.status not in (opn, ap) :
        raise Reject (_ ("Change of payment type not allowed"))
    if pr.status == opn :
        return
    ptid = new_values.get ('payment_type', ptdefault)
    pt = db.payment_type.getnode (new_values ['payment_type'])
    # If we're already in status approving and there is no approval yet
    # for payment type and the new payment type needs approval we need
    # to add an approval
    if not pt.need_approval :
        return
    update_payment_approval (db, pr)
# end def check_payment_type

def pr_check_payment_type (db, cl, nodeid, new_values) :
    if 'payment_type' not in new_values :
        return
    pr  = cl.getnode (nodeid)
    # Allow change for open and approving
    opn = db.pr_status.lookup ('open')
    ap  = db.pr_status.lookup ('approving')
    if pr.status not in (opn, ap) :
        raise Reject (_ ("Change of payment type not allowed"))
    if pr.status == opn :
        return
    need = prlib.need_payment_type_approval \
        (db, pr, new_values ['payment_type'])
    if need :
        update_payment_approval (db, pr)
# end def pr_check_payment_type

def namelen (db, cl, nodeid, new_values) :
    """ Check that name field doesn't become too long
    """
    if len (new_values.get ('name', '') or '') > 55 :
        raise Reject (_ ("Supplier name too long (max 55)"))
# end def namelen

def check_psp_cc_consistency (db, cl, nodeid, new_values, org = None) :
    """ Check that the organisation in psp or cc is correct and
        consistent with the organisation stored in the PR.
        Also check that the psp or cc is valid.
        Note: This is called with a valid nodeid.
    """
    proi = cl.getnode (nodeid) # Can be offer item or pr
    tc   = new_values.get ('time_project', proi.time_project)
    psp  = new_values.get ('psp_element', proi.psp_element)
    cc   = new_values.get ('sap_cc', proi.sap_cc)
    # Can happen only for offer item:
    if not psp and not cc :
        return
    # Needs to be specified for offer_item
    org = org or proi.organisation
    if psp :
        assert tc # Timecat *must be defined if psp element is defined
        node = db.psp_element.getnode (psp)
        tp   = db.time_project.getnode (tc)
        st   = db.time_project_status.getnode (tp.status)
        if not node.valid or not st.active :
            d = dict \
            ( psp_element  = _ ('psp_element')
            , time_project = _ ('time_project')
            , name = tc.name + ' ' + tc.description
            , pspn = node.name
            )
            raise Reject \
                (_ ("Non-active %(psp_element)s: %(pspn)s or "
                    "%(time_project)s: %(name)s"
                   ) % locals ()
                )
    else :
        node = db.sap_cc.getnode (cc)
        if not node.valid :
            sap_cc = _ ('sap_cc')
            name   = node.name
            raise Reject (_ ("Invalid %(sap_cc)s: %(name)s") % locals ())
    if node.organisation != org :
        o1 = db.organisation.get (org, 'name')
        if not node.organisation :
            raise Reject (_ ("Organisation of CC/TC is empty"))
        o2 = db.organisation.get (node.organisation, 'name')
        raise Reject \
            ( _("Organisation must be consistent with CC/TC: got %s expect %s")
            % (o1, o2)
            )
# end def check_psp_cc_consistency

def update_nosy (db, cl, nodeid, new_values) :
    """ On sign&send of a PR we update the nosy list with the nosy list
        from purchase_type, department, sap_cc, and time_project
        Note that we don't need the psp_element because time_project is
        updated consistently.
    """
    nosy = set (new_values.get ('nosy', cl.get (nodeid, 'nosy')))
    pt   = new_values.get ('purchase_type', cl.get (nodeid, 'purchase_type'))
    nosy.update (db.purchase_type.get (pt, 'nosy'))
    tc   = new_values.get ('time_project', cl.get (nodeid, 'time_project'))
    if tc :
        nosy.update (db.time_project.get (tc, 'nosy'))
    sap  = new_values.get ('sap_cc', cl.get (nodeid, 'sap_cc'))
    if sap :
        nosy.update (db.sap_cc.get (sap, 'nosy'))
    dep  = new_values.get ('department', cl.get (nodeid, 'department'))
    nosy.update (db.department.get (dep, 'nosy'))
    new_values ['nosy'] = list (nosy)
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
    now       = Date ('.')
    if 'status' in new_values and new_values ['status'] != ost :
        if new_values ['status'] == db.pr_status.lookup ('approving') :
            # check that pr_justification is given
            prjust (db, cl, nodeid, new_values)
            io  = new_values.get \
                ('internal_order', cl.get (nodeid, 'internal_order'))
            psp = new_values.get ('psp_element', cl.get (nodeid, 'psp_element'))
            tc  = new_values.get \
                ('time_project', cl.get (nodeid, 'time_project'))
            cc  = new_values.get \
                ('sap_cc',  cl.get (nodeid, 'sap_cc'))
            if not psp and not cc :
                raise Reject \
                    (_ ("Need to specify %(psp)s or %(cc)s")
                    % dict (psp = _ ('psp_element'), cc = _ ('sap_cc'))
                    )
            if psp and cc :
                raise Reject \
                    (_ ("Either specify %(psp)s or %(cc)s, not both")
                    % dict (psp = _ ('psp_element'), cc = _ ('sap_cc'))
                    )
            if psp and io :
                raise Reject \
                    (_ ("Specify %(cc)s not %(psp)s with %(io)s")
                    % dict
                        ( psp = _ ('psp_element')
                        , cc  = _ ('sap_cc')
                        , io  = _ ('internal_order')
                        )
                    )
            common.require_attributes \
                ( _, cl, nodeid, new_values
                , 'department',  'organisation'
                , 'offer_items', 'delivery_deadline', 'purchase_type'
                , 'part_of_budget', 'terms_conditions', 'frame_purchase'
                , 'pr_currency', 'purchasing_agents', 'pr_ext_resource'
                )
            org = new_values.get \
                ('organisation', cl.get (nodeid, 'organisation'))
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
                if oitem.sap_cc and oitem.psp_element :
                    raise Reject \
                        (_ ("Either specify %(psp)s or %(cc)s, not both")
                        % dict (psp = _ ('psp_element'), cc = _ ('sap_cc'))
                        )
                if (psp or oitem.psp_element) and (io or oitem.internal_order) :
                    raise Reject \
                        (_ ("Specify %(cc)s not %(psp)s with %(io)s")
                        % dict
                            ( psp = _ ('psp_element')
                            , cc  = _ ('sap_cc')
                            , io  = _ ('internal_order')
                            )
                        )
                nv = dict \
                    ( time_project = oitem.time_project
                    , sap_cc       = oitem.sap_cc
                    , psp_element  = oitem.psp_element
                    )
                check_psp_cc_consistency (db, db.pr_offer_item, oi, nv, org)
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
            check_psp_cc_consistency (db, cl, nodeid, new_values)
            update_nosy (db, cl, nodeid, new_values)

        elif new_values ['status'] == db.pr_status.lookup ('approved') :
            for ap in approvals :
                if ap.status != ap_appr :
                    raise Reject (_ ("Not all approvals in status approved"))
            new_values ['date_approved'] = now
        elif new_values ['status'] == db.pr_status.lookup ('rejected') :
            for ap in approvals :
                if ap.status == ap_rej :
                    break
            else :
                uid = db.getuid ()
                if not common.user_has_role (db, uid, *prlib.reject_roles) :
                    raise Reject (_ ("No rejected approval-record found"))
            new_values ['date_approved'] = None
            new_values ['date_ordered']  = None
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
            new_values ['total_cost']    = None
            new_values ['date_approved'] = None
            new_values ['date_ordered']  = None
        elif new_values ['status'] == db.pr_status.lookup ('ordered') :
            new_values ['date_ordered'] = now
        elif new_values ['status'] == db.pr_status.lookup ('cancelled') :
            new_values ['date_approved'] = None
            new_values ['date_ordered']  = None
# end def change_pr

def agent_in_approval_order_users (db, uid, ptid) :
    pt = db.purchase_type.getnode (ptid)
    for aoid in pt.pr_view_roles :
        ao = db.pr_approval_order.getnode (aoid)
        if uid in ao.users :
            return True
    return False
# end def agent_in_approval_order_users

def compute_agents (db, paset, pts) :
    pa = set ()
    for uid in paset :
        # Add only if allowed by *all* pts
        for pt in pts :
            if not agent_in_approval_order_users (db, uid, pt) :
                break
        else :
            pa.add (uid)
    return pa
# end def compute_agents

def set_agents (db, cl, nodeid, new_values) :
    """ Set purchasing agents if agents empty (or would become empty)
        or the sap_cc or time_project changed
        *and* we can set the agent from the tc or cc.
        We also update the nosy list whenever purchasing_agents changes.
        Note that we do a check that the agents in sap_cc or
        time_project do have the necessary view roles of the
        purchase_type. Only if this check succeeds are agents added to
        purchasing_agents and nosy.
    """
    force = False
    pr = None
    if nodeid :
        pr = cl.getnode (nodeid)
    pa = new_values.get ('purchasing_agents', [])
    if pa == ['2'] :
        pa = []
        force = True
    opa = set ()
    if pr and 'purchasing_agents' not in new_values :
        pa  = pr.purchasing_agents
    if pr :
        opa = set (pr.purchasing_agents)
    pt = new_values.get ('purchase_type')
    if pr and 'purchase_type' not in new_values :
        pt = pr.purchase_type
    pts = set ()
    if pt :
        pts.add (pt)
    if force :
        paset = set ()
    else :
        paset = set (new_values.get ('purchasing_agents', []))
    # Loop over offer items and add pt if any, also add purchase agents
    ois = new_values.get ('offer_items', [])
    if pr and 'offer_items' not in new_values :
        ois = pr.offer_items
    for oid in ois :
        oi = db.pr_offer_item.getnode (oid)
        if oi.purchase_type :
            pts.add   (oi.purchase_type)
            ptyp = db.purchase_type.getnode (oi.purchase_type)
            paset.update (ptyp.purchasing_agents)
        for cn in 'sap_cc', 'time_project' :
            a = getattr (oi, cn)
            if a :
                paset.update (db.getclass (cn).get (a, 'purchasing_agents'))
    # If agents edited by user, check they all have necessary
    # permissions and keep only the ones that do
    # This also means that if the list gets empty here we will compute
    # the default below.
    if 'purchasing_agents' in new_values and not force :
        pa = compute_agents (db, pa, pts)
        if pa :
            new_values ['purchasing_agents'] = list (pa)
    if  (  not pa
        or force
        or 'time_project'      in new_values
        or 'sap_cc'            in new_values
        or 'purchase_type'     in new_values
        or 'offer_items'       in new_values
        ) :
        cc = tc = None
        if 'time_project' in new_values :
            tc = new_values ['time_project']
        elif pr :
            tc = pr.time_project
        if 'sap_cc' in new_values :
            cc = new_values ['sap_cc']
        elif pr :
            cc = pr.sap_cc
        if tc :
            tc = db.time_project.getnode (tc)
        if cc :
            cc = db.sap_cc.getnode (cc)
        item = tc or cc
        if item :
            paset.update (item.purchasing_agents)
        if pt :
            paset.update (db.purchase_type.get (pt, 'purchasing_agents'))
        # Only put those agents into 'purchasing_agents' that have
        # necessary role from all the purchase_types in pts
        pa = compute_agents (db, paset, pts)
        new_values ['purchasing_agents'] = list (pa)
    # Add agents to nosy list
    if set (new_values.get ('purchasing_agents', [])) != opa :
        nosy = new_values.get ('nosy', [])
        if not nosy and pr :
            nosy = pr.nosy
        nosy = set (nosy)
        # Remove old agents from nosy
        nosy.difference_update (opa)
        # Add new agents
        for i in new_values.get ('purchasing_agents', []) :
            nosy.add (i)
        new_values ['nosy'] = list (nosy)
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

def set_approval_pr (db, cl, nodeid, new_values) :
    """ Do not allow change of PR, but we *need* to allow this input in
        the web-interface for ordering actions.
    """
    common.require_attributes \
        (_, cl, nodeid, new_values, 'purchase_request')

    if 'date' in new_values and 'status' not in new_values :
        del new_values ['date']
    if 'purchase_request' in new_values and 'status' not in new_values :
        del new_values ['purchase_request']
    if 'purchase_request' not in new_values :
        return
    npr = new_values ['purchase_request']
    opr = cl.get (nodeid, 'purchase_request')
    if npr != opr :
        raise Reject (_ ("Purchase request cannot be changed"))
# end def set_approval_pr

def nosy_for_approval (db, app, add = False) :
    """ Used for adding/removing users from nosy list prior to/after
        approval
    """
    nosy = {}
    if app.user :
        for k in common.approval_by (db, app.user) :
            nosy [k] = 1
    # Don't add deputy to nosy unless deputy_gets_mail is set
    if app.deputy and app.deputy_gets_mail :
        for k in common.approval_by (db, app.deputy) :
            nosy [k] = 1
    nosy_dd = {}
    if app.role_id :
        ao = db.pr_approval_order.getnode (app.role_id)
        subst = []
        if not ao.want_no_messages :
            for u in ao.users :
                # Do not include user replaced by clearance_by (delegation)
                # in the mailing list, common.see approval_by.
                subst.extend (common.approval_by (db, u))
        nosy_dd = subst
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
    """ At the end of all nosy-list manipulations make sure that some
        users *stay* on the nosy list even if they were removed for some
        reason previously.
    """
    nosy  = set (new_values.get ('nosy', cl.get (nodeid, 'nosy')))
    onosy = set (nosy)
    rq    = new_values.get ('requester', cl.get (nodeid, 'requester'))
    if rq not in nosy :
        nosy.add (rq)
    # Allow creator to remove her/himself after initial sign&send
    pr_approving = db.pr_status.lookup ('approving')
    if 'status' in new_values and new_values ['status'] == pr_approving :
        cr = cl.get (nodeid, 'creator')
        if cr not in nosy :
            nosy.add (cr)
    # Agent should always be kept on nosy list, might vanish due to
    # removal by nosy_for_approval
    pan = 'purchasing_agents'
    agents = new_values.get (pan, cl.get (nodeid, pan))
    nosy.update (agents)
    # All users from roles configured as 'only_nosy' in approval_order
    # should be kept on the nosy list, but only while approving
    status = new_values.get ('status', cl.get (nodeid, 'status'))
    if status == pr_approving :
        pr = db.purchase_request.getnode (nodeid)
        users = prlib.compute_approvals (db, pr, email_only = True)
        nosy.update (users)
    if onosy != nosy :
        new_values ['nosy'] = list (nosy)
# end def fix_nosy

def set_infosec (db, cl, nodeid, new_values) :
    """ When going from open->approving, set the infosec attributes on
        the PR
    """
    apr = db.pr_status.lookup ('approving')
    opn = db.pr_status.lookup ('open')
    ost = cl.get (nodeid, 'status')
    nst = new_values.get ('status', ost)
    if ost != opn or nst != apr :
        return
    mrt = prlib.max_risk_type (db, nodeid)
    # Can happen if none of the product groups has a security level
    if not mrt :
        return
    new_values ['purchase_risk_type'] = mrt.id
    if mrt.order > 40 :
        raise Reject (_ ('Risk is too high: "%s"') % mrt.name)
    ois = new_values.get ('offer_items', cl.get (nodeid, 'offer_items'))
    ilm = None
    for oid in ois :
        oi = db.pr_offer_item.getnode (oid)
        if oi.infosec_level :
            il = db.infosec_level.getnode (oi.infosec_level)
            if ilm is None or il.order > ilm.order :
                ilm = il
    if ilm is not None :
        new_values ['infosec_level'] = ilm.id
# end def set_infosec

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
    msgs = set (pr.messages)
    msgs.add (msg)
    d = kw
    d.update (nosy = list (nosy), messages = list (msgs))
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
    if 'units' not in new_values or new_values ['units'] <= 0 :
        new_values ['units'] = 1
    if 'vat' not in new_values :
        new_values ['vat'] = 0
# end def new_pr_offer_item

def check_pr_offer_item (db, cl, nodeid, new_values) :
    common.require_attributes \
        ( _, cl, nodeid, new_values, 'units'
        , 'price_per_unit', 'product_group', 'supplier'
        )
    units = new_values.get ('units', None)
    price = new_values.get ('price_per_unit', None)
    oi    = None
    if nodeid :
        oi = cl.getnode (nodeid)
    if units is None :
        assert oi
        units = oi.units
    if price is None :
        assert oi
        price = oi.price_per_unit
    if units <= 0 :
        raise Reject ("Units must not be <= 0")
    if price <= 0 :
        raise Reject ("Price must not be <= 0")
    pgid = new_values.get ('product_group')
    if not pgid and nodeid :
        pgid = cl.get (nodeid, 'product_group')
    if pgid :
        pg = db.product_group.getnode (pgid)
    else :
        pg = None
    if 'infosec_level' in new_values :
        if new_values ['infosec_level'] is None and pg :
            new_values ['infosec_level'] = pg.infosec_level
    elif 'product_group' in new_values :
        new_values ['infosec_level'] = pg.infosec_level
    ilid = new_values.get ('infosec_level')
    if nodeid and not ilid :
        ilid = cl.get (nodeid, 'infosec_level')
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
    """ Set pr_supplier to correct value if supplier (text-input field)
        is changed. Note that this must come *before* the method
        check_supplier_change, therefore we have prio 90.
    """
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
    pr  = get_pr_from_offer_item (db, nodeid)
    if not pr :
        return
    if pr.status == rej :
        db.purchase_request.set (pr.id, status = opn)
# end def check_pr_update

def check_agent_change (db, cl, nodeid, old_values) :
    do_check = False
    for k in 'purchase_type', 'sap_cc', 'time_project' :
        if cl.get (nodeid, k) != old_values.get (k, None) :
            do_check = True
            break
    if do_check :
        prs = db.purchase_request.filter (None, dict (offer_items = nodeid))
        assert len (prs) == 1
        # Setting the agent to 2 (anonymous) will force a recomputation
        db.purchase_request.set (prs [0], purchasing_agents = ['2'])
# end def check_agent_change

def check_currency (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'min_sum', 'order', 'exchange_rate')
    if new_values.get ('key_currency') :
        for id in db.pr_currency.getnodeids () :
            if id == nodeid :
                continue
            if cl.get (id, 'key_currency') :
                raise Reject (_ ("Duplicate key currency"))
    tmax = new_values.get ('max_team')
    if tmax is None and nodeid :
        tmax = cl.get (nodeid, 'max_team')
    gmax = new_values.get ('max_group')
    if gmax is None and nodeid :
        gmax = cl.get (nodeid, 'max_group')
    # If both, max_group and max_team are specified, max_team must be
    # lower than max_group
    if tmax and gmax :
        if gmax <= tmax :
            mg = _ ("max_group")
            mt = _ ("max_team")
            raise Reject (_ ("%(mt)s must be < %(mg)s") % locals ())
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
    # Ensure that all purchasing_agents have one of the view roles
    if 'purchasing_agents' in new_values :
        if 'pr_view_roles' in new_values :
            roles = new_values ['pr_view_roles']
        elif nodeid :
            roles = cl.get (nodeid, 'pr_view_roles')
        users = set ()
        for rid in roles :
            role = db.pr_approval_order.getnode (rid)
            users.update (role.users)
        for id in new_values ['purchasing_agents'] :
            if id not in users :
                un = db.user.get (id, 'username')
                raise Reject (_ ("User doesn't have a View-Role: %s") % un)
# end def pt_check_roles

def pao_check_roles (db, cl, nodeid, new_values) :
    """ Now allow the role-name to not be a roundup role anymore
        Also check that only_nosy is set to a boolean value.
    """
    if 'role' in new_values and ',' in new_values ['role'] :
        raise Reject (_ ("No commas allowed in role name"))
    nosyflag   = new_values.get ('only_nosy')
    is_board   = new_values.get ('is_board')
    is_finance = new_values.get ('is_finance')
    if nodeid :
        if nosyflag is None :
            nosyflag   = cl.get (nodeid, 'only_nosy')
        if is_board is None :
            is_board   = cl.get (nodeid, 'is_board')
        if is_finance is None :
            is_finance = cl.get (nodeid, 'is_finance')
    if nosyflag is None :
        new_values ['only_nosy'] = False
    if nosyflag and (is_board or is_finance) :
        raise Reject ('Finance or Board may not be set only nosy')
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

def check_supplier_risk (db, cl, nodeid, new_values) :
    """ Check risk entries of supplier: each combination
        organisation+security_req_group may occur only once
    """
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'organisation'
        , 'supplier'
        , 'security_req_group'
        , 'supplier_risk_category'
        )
    org = new_values.get ('organisation')
    sup = new_values.get ('supplier')
    srg = new_values.get ('security_req_group')
    if not org :
        org = cl.get (nodeid, 'organisation')
    if not sup :
        sup = cl.get (nodeid, 'supplier')
    if not srg :
        srg = cl.get (nodeid, 'security_req_group')
    common.check_unique \
        ( _, cl, nodeid
        , supplier           = sup
        , organisation       = org
        , security_req_group = srg
        )
# end def check_supplier_risk

def check_psr (db, cl, nodeid, new_values) :
    """ Check purchase_security_risk entries: each combination
        infosec_level+supplier_risk_category may occur only once
    """
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'infosec_level'
        , 'purchase_risk_type'
        )
    il  = new_values.get ('infosec_level')
    src = new_values.get ('supplier_risk_category')
    if not il :
        il  = cl.get (nodeid, 'infosec_level')
    if not src and nodeid :
        src = cl.get (nodeid, 'supplier_risk_category')
    common.check_unique \
        ( _, cl, nodeid
        , infosec_level          = il
        , supplier_risk_category = src
        )
# end def check_psr

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

def check_issue_nums (db, cl, nodeid, new_values) :
    issue_ids = new_values.get ('issue_ids', None)
    # Allow empty value, also exits if not changed
    if issue_ids is None :
        return
    minl = int (getattr (db.config.ext, 'LINK_MINID', 0))
    maxl = int (getattr (db.config.ext, 'LINK_MAXID', 100))
    ids  = [x.strip () for x in issue_ids.split (',')]
    for id in ids :
        if not (minl <= len (id) <= maxl) or not id.isdigit () :
            raise Reject (_ ("Invalid Issue-Number: %s") % id)
# end def check_issue_nums

def check_pg (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'sap_ref', 'pg_category')
# end def check_pg

def check_pgc (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'sap_ref')
# end def check_pgc

def send_las_email (db, cl, nodeid, old_values) :
    oi = cl.getnode (nodeid)
    if not oi.add_to_las :
        return
    try :
        las_email = getattr (db.config.ext, 'MAIL_LAS_EMAIL', None)
        las_text  = getattr (db.config.ext, 'MAIL_LAS_TEXT', None)
        las_subj  = getattr (db.config.ext, 'MAIL_LAS_SUBJECT', None)
    except InvalidOptionError :
        return
    if not las_email or not las_text or not las_subj :
        return
    pr = get_pr_from_offer_item (db, nodeid)
    # Changed?
    if not old_values or not old_values.get ('add_to_las') :
        r      = re.compile (r'\s+\n')
        mailer = roundupdb.Mailer (db.config)
        sender = None
        try :
            sname = getattr (db.config.ext, 'MAIL_SENDER_NAME', None)
            smail = getattr (db.config.ext, 'MAIL_SENDER_ADDR', None)
            if sname and smail :
                sender = (sname, smail)
        except InvalidOptionError :
            pass
        title    = pr.title
        supplier = oi.supplier
        prid     = pr.id
        url      = db.config.TRACKER_WEB
        user     = db.user.getnode (db.getuid ())
        realname = user.realname
        address  = user.address
        d = dict (locals ())
        txt = r.sub ('\n', las_text)
        txt = txt.replace ('$', '%') % d
        try :
            mailer.standard_message ((las_email,), las_subj, txt, sender)
        except roundupdb.MessageSendError as message :
            raise roundupdb.DetectorError (message)
# end def send_las_email

def check_psp (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'name', 'number', 'organisation', 'project')
    if not nodeid and 'valid' not in new_values :
        new_values ['valid'] = True
# end def check_psp

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
    db.purchase_request.audit   ("create", check_psp_cc,    priority = 80)
    db.purchase_request.audit   ("set",    check_psp_cc,    priority = 80)
    db.purchase_request.audit   ("set",    requester_chg,   priority = 70)
    db.purchase_request.audit   ("set",    reopen,          priority = 90)
    db.purchase_request.audit   ("set",    change_pr)
    db.purchase_request.audit   ("set",    check_late_changes)
    db.purchase_request.audit   ("create", check_dd)
    db.purchase_request.audit   ("set",    check_dd)
    db.purchase_request.audit   ("create", set_agents,      priority = 150)
    db.purchase_request.audit   ("set",    set_agents,      priority = 150)
    db.purchase_request.audit   ("set",    approvalchange)
    db.purchase_request.react   ("set",    changed_pr)
    db.purchase_request.react   ("create", create_pr_approval)
    db.purchase_request.audit   ("set",    check_io_pr)
    db.purchase_request.audit   ("set",    fix_nosy,        priority = 200)
    db.purchase_request.audit   ("set",    set_infosec,     priority = 250)
    db.purchase_request.audit   ("create", check_issue_nums)
    db.purchase_request.audit   ("set",    check_issue_nums)
    db.purchase_request.audit   ("set",    pr_check_payment_type)
    db.pr_approval.audit        ("create", new_pr_approval)
    db.pr_approval.audit        ("set",    change_pr_approval)
    db.pr_approval.audit        ("set",    set_approval_pr, priority = 90)
    db.pr_approval.react        ("set",    approved_pr_approval)
    db.pr_offer_item.audit      ("create", new_pr_offer_item)
    db.pr_offer_item.audit      ("create", check_pr_offer_item, priority = 110)
    db.pr_offer_item.audit      ("set",    check_pr_offer_item, priority = 110)
    db.pr_offer_item.audit      ("create", check_supplier, priority = 90)
    db.pr_offer_item.audit      ("set",    check_supplier, priority = 90)
    db.pr_offer_item.audit      ("set",    check_supplier_change)
    db.pr_offer_item.react      ("set",    check_pr_update)
    db.pr_offer_item.react      ("set",    check_agent_change)
    db.pr_offer_item.audit      ("create", check_input_len, priority = 150)
    db.pr_offer_item.audit      ("set",    check_input_len, priority = 150)
    db.pr_offer_item.audit      ("set",    check_payment_type)
    db.pr_offer_item.audit      ("set",    check_io_oi)
    db.pr_offer_item.audit      ("create", check_psp_tc, priority = 50)
    db.pr_offer_item.audit      ("set",    check_psp_tc, priority = 50)
    db.pr_offer_item.react      ("create", send_las_email, priority = 150)
    db.pr_offer_item.react      ("set",    send_las_email, priority = 150)
    db.pr_currency.audit        ("create", check_currency)
    db.pr_currency.audit        ("set",    check_currency)
    db.pr_approval_order.audit  ("create", pao_check_roles)
    db.pr_approval_order.audit  ("set",    pao_check_roles)
    db.pr_supplier_rating.audit ("create", check_supplier_rating)
    db.pr_supplier_rating.audit ("set",    check_supplier_rating)
    db.pr_supplier.audit        ("create", namelen)
    db.pr_supplier.audit        ("set",    namelen)
    db.pr_supplier_risk.audit   ("create", check_supplier_risk)
    db.pr_supplier_risk.audit   ("set",    check_supplier_risk)
    db.purchase_security_risk.audit ("create", check_psr)
    db.purchase_security_risk.audit ("set",    check_psr)
    db.product_group.audit      ("create", check_pg)
    db.product_group.audit      ("set",    check_pg)
    db.pg_category.audit        ("create", check_pgc)
    db.pg_category.audit        ("set",    check_pgc)
    db.psp_element.audit        ("create", check_psp)
    db.psp_element.audit        ("set",    check_psp)
# end def init
