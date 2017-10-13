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

def compute_approvals (db, pr, do_create) :
    """ Compute approvals for current PR settings
        do_create specifies if the approvals are created or just a
        would-be list is computed.
    """
    _ = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
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

    prc_ids = db.pr_approval_config.filter (None, dict (valid = True))
    if cur :
        s  = pr_offer_item_sum (db, pr.id)
        s  = s * cur.exchange_rate
        for prcid in prc_ids :
            prc = db.pr_approval_config.getnode (prcid)
            if prc.if_not_in_las and in_las (db, pr.id) :
                continue
            if s > prc.amount :
                apr_by_role [prc.role] = add_approval_with_role \
                    (db, do_create, pr.id, prc.role)
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
        finance = db.pr_approval_order.lookup ('finance')
        apr_by_role [finance] = add_approval_with_role \
            (db, do_create, pr.id, finance)
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
        if  (  (pob and pob.name.lower () == 'no')
            or (cur and pr_offer_item_sum (db, pr.id) >= cur.max_sum)
            ) :
            board = db.pr_approval_order.lookup ('board')
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
    if uid in r.users :
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
