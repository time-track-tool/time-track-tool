#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-16 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    prlib
#
# Purpose
#    Common library functions for purchase request tracker
#
#--
#

import common
from   roundup.cgi.TranslationService import get_translation
from   roundup.exceptions             import Reject

def pr_offer_item_sum (db, pr) :
    pr    = db.purchase_request.getnode (pr)
    total = 0.0
    for id in pr.offer_items :
        item  = db.pr_offer_item.getnode (id)
        if item.price_per_unit is not None and item.units is not None :
            total += item.price_per_unit * item.units
    if pr.total_cost is not None :
        assert abs (pr.total_cost - total) < 0.0001
    return total
# end def pr_offer_item_sum

def gen_pr_approval (db, do_create, ** values) :
    """ If do_create is set, create a new approval with the given
        values. If unset we only return a dict of the given values.
    """
    if do_create :
        return db.pr_approval.create (** values)
    else :
        if values.get ('deputy') :
            values ['deputy'] = db.user.get (values ['deputy'], 'username')
        if values.get ('user') :
            values ['user']   = db.user.get (values ['user'], 'username')
        return values
# end def gen_pr_approval

def add_approval_with_role (db, do_create, prid, appr_order_id) :
    ord   = db.pr_approval_order.getnode (appr_order_id)
    return gen_pr_approval \
        ( db, do_create
        , order            = ord.order
        , purchase_request = prid
        , role             = ord.role.lower ()
        , role_id          = ord.id
        , description      = ord.role
        )
# end def add_approval_with_role

def supplier_is_approved (db, pr, sup_id) :
    if not sup_id :
        return False
    ratings = db.pr_supplier_rating.filter \
        (None, dict (supplier = sup_id, organisation = pr.organisation))
    assert len (ratings) <= 1
    if len (ratings) :
        sr = db.pr_supplier_rating.getnode (ratings [0])
        rating = db.pr_rating_category.getnode (sr.rating)
        if rating.order > 2 :
            return False
        return True
    return False
# end def supplier_is_approved

def in_las (db, pr) :
    pr    = db.purchase_request.getnode (pr)
    for id in pr.offer_items :
        item  = db.pr_offer_item.getnode (id)
        if not item.pr_supplier :
            return False
        d = dict (supplier = item.pr_supplier, organisation = pr.organisation)
        r = db.pr_supplier_rating.filter (None, d)
        if not r :
            return False
        assert len (r) == 1
        try :
            good = db.pr_rating_category.lookup ('good impression')
        except KeyError :
            good = 1
        if db.pr_supplier_rating.get (r [0], 'rating') != good :
            return False
    return True
# end def in_las

def _app_cfgs (db, pr, ids) :
    acs = []
    for id in ids :
        ac = db.pr_approval_config.getnode (id)
        if ac.if_not_in_las :
            continue
        if  (   ac.organisations and pr.organisation
            and pr.organisation not in ac.organisations
            ) :
            continue
        acs.append (ac)
    return acs
# end def _app_cfgs

def risk_type (db, offer_item_id, pr_supplier = None) :
    """ Note that an *empty* pr_supplier (one that isn't in LAS) is
        possible and will typically get a bad security rating.
        If pr_supplier is specified explicitly, it should be set to '-1'
        for explicitly searching for an empty supplier.
    """
    oi  = db.pr_offer_item.getnode (offer_item_id)
    pg  = db.product_group.getnode (oi.product_group)
    prs = db.purchase_request.filter (None, dict (offer_items = offer_item_id))
    assert len (prs) == 1
    pr  = db.purchase_request.getnode (prs [0])

    if not oi.infosec_level or not pr.organisation :
        return None
    if pr_supplier is None :
        pr_supplier = oi.pr_supplier
    if pr_supplier :
        sr = db.pr_supplier_risk.filter \
            ( None, dict
                ( supplier           = pr_supplier
                , organisation       = pr.organisation
                , security_req_group = pg.security_req_group
                )
            )
        assert len (sr) <= 1
        if sr :
            sr = db.pr_supplier_risk.getnode (sr [0])
            risk_cat = sr.supplier_risk_category
        else :
            risk_cat = '-1'
    else :
        risk_cat = '-1'
    risk = db.purchase_security_risk.filter \
        ( None, dict
            ( infosec_level          = oi.infosec_level
            , supplier_risk_category = risk_cat
            )
        )
    assert len (risk) == 1
    return db.purchase_security_risk.get (risk [0], 'purchase_risk_type')
# end def risk_type

def max_risk_type (db, prid) :
    """ Loop over all offer items and compute maximum risk type.
        Sort order is the order property.
        Note that if the pr already has a purchase_risk_type set, this
        also gets into the maximum. So once set, the maximum will never
        be smaller.
    """
    pr = db.purchase_request.getnode (prid)
    rtmax = None
    if pr.purchase_risk_type :
        rtmax = db.purchase_risk_type.getnode (pr.purchase_risk_type)
    for oi in pr.offer_items :
        rtid = risk_type (db, oi)
        if not rtid :
            continue
        rt = db.purchase_risk_type.getnode (rtid)
        if rtmax is None or rtmax.order < rt.order :
            rtmax = rt
    return rtmax
# end def max_risk_type

def infosec_level_lowered (db, prid) :
    """ Check if the user specified a lower infosec_level than would be
        computed automagically
    """
    pr = db.purchase_request.getnode (prid)
    for oid in pr.offer_items :
        oi = db.pr_offer_item.getnode (oid)
        pg = db.product_group.getnode (oi.product_group)
        if pg.infosec_level :
            if oi.infosec_level is None :
                return True
            pg_il = db.infosec_level.getnode (pg.infosec_level)
            oi_il = db.infosec_level.getnode (oi.infosec_level)
            if oi_il.order < pg_il.order :
                return True
    return False
# end def infosec_level_lowered

def need_payment_type_approval (db, pr, new = None) :
    pt_default = new or pr.payment_type or '1'
    for id in pr.offer_items :
        item  = db.pr_offer_item.getnode (id)
        ptid  = item.payment_type or pt_default
        if ptid :
            pt = db.payment_type.getnode (ptid)
            if pt.need_approval :
                return True
    return False
# end def need_payment_type_approval

def compute_approvals (db, pr, do_create) :
    """ Compute approvals for current PR settings
        do_create specifies if the approvals are created or just a
        would-be list is computed.
    """
    _ = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    # Compute board and finance approval configs for this pr
    board_roles   = db.pr_approval_order.filter (None, dict (is_board = True))
    finance_roles = db.pr_approval_order.filter (None, dict (is_finance = True))
    # Check if there are any pr_approval_config entries with board or
    # finance roles
    ids = db.pr_approval_config.filter (None, dict (role = board_roles))
    bac = _app_cfgs (db, pr, ids)
    board_roles = set (ac.role for ac in bac)

    ids = db.pr_approval_config.filter (None, dict (role = finance_roles))
    fac = _app_cfgs (db, pr, ids)
    finance_roles = set (ac.role for ac in fac)

    if do_create and not board_roles :
        raise Reject (_ ("Configuration error: No board roles for this PR"))
    if do_create and not finance_roles :
        raise Reject (_ ("Configuration error: No finance roles for this PR"))
    board_approval = False

    assert not do_create or pr.organisation
    assert not do_create or pr.pr_currency
    cur = None
    if pr.pr_currency :
        cur = db.pr_currency.getnode (pr.pr_currency)
    apr_by_r_d  = {}
    apr_by_role = {}
    assert not do_create or pr.time_project or pr.sap_cc
    d = None
    if pr.time_project :
        pcc = db.time_project.getnode (pr.time_project)
        d   = _ ('%(tp)s responsible/deputy') \
            % dict (tp = _ ('time_project'))
    elif pr.sap_cc :
        pcc = db.sap_cc.getnode (pr.sap_cc)
        d   = _ ('%(cc)s responsible/deputy') % dict (cc = _ ('sap_cc'))
    if d :
        apr = gen_pr_approval \
            ( db, do_create
            , order            = 10
            , purchase_request = pr.id
            , user             = pcc.responsible
            , deputy           = pcc.deputy
            , deputy_gets_mail = pcc.deputy_gets_mail or False
            , description      = d
            )
        apr_by_r_d [(pcc.responsible, pcc.deputy)] = apr
    for u in pr.special_approval :
        apr = gen_pr_approval \
            ( db, do_create
            , order            = 15
            , purchase_request = pr.id
            , user             = u
            , deputy           = u
            , description      = _ ("Special approval")
            )
        apr_by_r_d [(u, u)] = apr

    max_risk = max_risk_type (db, pr.id)
    prc_ids  = db.pr_approval_config.filter (None, dict (valid = True))
    if cur :
        s  = pr_offer_item_sum (db, pr.id)
        s  = s * 1.0 / cur.exchange_rate
        for prcid in prc_ids :
            prc = db.pr_approval_config.getnode (prcid)
            if prc.if_not_in_las and in_las (db, pr.id) :
                continue
            if prc.purchase_type and pr.purchase_type not in prc.purchase_type :
                continue
            if  (   prc.pr_ext_resource
                and pr.pr_ext_resource != prc.pr_ext_resource
                ) :
                continue
            if  (   prc.organisations and pr.organisation
                and pr.organisation not in prc.organisations
                ) :
                continue
            if  (      prc.amount         is not None and s > prc.amount
                or (   prc.infosec_amount is not None and s > prc.infosec_amount
                   and max_risk
                   and (  'High' in max_risk.name
                       or max_risk.order >= 30
                       or infosec_level_lowered (db, pr.id)
                       )
                   )
                or (   prc.payment_type_amount is not None
                   and s > prc.payment_type_amount
                   and need_payment_type_approval (db, pr)
                   )
                ) :
                apr_by_role [prc.role] = add_approval_with_role \
                    (db, do_create, pr.id, prc.role)
                r = db.pr_approval_order.getnode (prc.role)
                # prevent double board-approval if this is also not part
                # of budget.
                if r.is_board :
                    board_approval = True
    if cur and pr_offer_item_sum (db, pr.id) > cur.min_sum :
        assert not do_create or pr.department
        if pr.department :
            dep = db.department.getnode (pr.department)
            apr = gen_pr_approval \
                ( db, do_create
                , order            = 55
                , purchase_request = pr.id
                , user             = dep.manager
                , deputy           = dep.deputy
                , description      = "Department Head"
                )
            apr_by_r_d [(dep.manager, dep.deputy)] = apr
        # Loop over order items and check if any is not on the approved
        # suppliers list
        supplier_approved = True
        for id in pr.offer_items :
            oi = db.pr_offer_item.getnode (id)
            if not supplier_is_approved (db, pr, oi.pr_supplier) :
                supplier_approved = False
        if pr.safety_critical and not supplier_approved :
            quality = db.pr_approval_order.lookup ('quality')
            apr_by_role [quality] = add_approval_with_role \
                (db, do_create, pr.id, quality)
        assert not do_create or pr.part_of_budget
        if pr.part_of_budget :
            pob = db.part_of_budget.getnode (pr.part_of_budget)
        else :
            pob = None
        # Board approval if not part of budget but only if we don't
        # already *have* a board approval
        if pob and pob.name.lower () == 'no' and not board_approval :
            for board in board_roles :
                apr_by_role [board] = add_approval_with_role \
                    (db, do_create, pr.id, board)
        assert not do_create or pr.purchase_type

    if pr.purchase_type :
        pt    = db.purchase_type.getnode (pr.purchase_type)
        roles = []
        if cur and pr_offer_item_sum (db, pr.id) > cur.min_sum :
            roles.extend (pt.pr_roles)
        roles.extend (pt.pr_forced_roles)
        # Make them unique
        roles = dict.fromkeys (roles).keys ()
        for role in roles :
            apr_by_role [role] = add_approval_with_role \
                (db, do_create, pr.id, role)
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
        if (   pcc
           and (pcc.responsible, pcc.deputy) not in apr_by_r_d
           and cur
           and pr_offer_item_sum (db, pr.id) > cur.min_sum
           ) :
            idx = oi.index or 0
            apr = gen_pr_approval \
                ( db, do_create
                , order            = 10 + idx * 0.001
                , purchase_request = pr.id
                , user             = pcc.responsible
                , deputy           = pcc.deputy
                , description      = d
                )
            apr_by_r_d [(pcc.responsible, pcc.deputy)] = apr
        if oi.purchase_type :
            pt    = db.purchase_type.getnode (oi.purchase_type)
            roles = []
            if cur and pr_offer_item_sum (db, pr.id) > cur.min_sum :
                roles.extend (pt.pr_roles)
            roles.extend (pt.pr_forced_roles)
            for role in roles :
                if role not in apr_by_role :
                    apr_by_role [role] = add_approval_with_role \
                        (db, do_create, pr.id, role)
    if not do_create :
        vals = apr_by_r_d.values () + apr_by_role.values ()
        vals.sort (key = lambda x : x ['order'])
        return vals
# end def compute_approvals

def has_pr_role (db, uid, roleid) :
    r = db.pr_approval_order.getnode (roleid)
    # For speed reasons check direct user
    if uid in r.users :
        return True
    # Check including delegated and substituted approvals
    for u in r.users :
        if uid in common.approval_by (db, u) :
            return True
    return False
# end def has_pr_role

pr_justification = \
    ( ( 'Related item (in PES)'
      , 'please indicate how it is covered'
      )
    , ( 'Purchase explanation'
      , 'please explain the reasons why do we need this purchase'
      )
    , ( 'Possible alternatives'
      , 'please specify what other solutions you see'
      )
    , ( 'Impact on the project in case of rejection'
      , 'please state possible consequences of rejecting the purchase'
      )
    )

reject_roles = ('Procurement-Admin', 'Procurement')
