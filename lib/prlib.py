#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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
from   roundup.exceptions import Reject

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
        id = db.pr_approval.create (** values)
        return db.pr_approval.getnode (id)
    else :
        if values.get ('deputy') :
            values ['deputy'] = db.user.get (values ['deputy'], 'username')
        if values.get ('user') :
            values ['user']   = db.user.get (values ['user'], 'username')
        return values
# end def gen_pr_approval

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
        if  (   ac.departments and pr.department
            and pr.department not in ac.departments
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

class Approval_Logic :

    def __init__ (self, db, pr, do_create, email_only) :
        self.db          = db
        self.pr          = pr
        self.do_create   = do_create
        self.email_only  = email_only
        self.apr_by_r_d  = {}
        self.apr_by_role = {}
        # These do not go together
        assert not (do_create and email_only)
    # end def __init__

    def _add_approval (self, key, value) :
        if self.email_only :
            return
        if key not in self.apr_by_r_d :
            self.apr_by_r_d [key] = []
        self.apr_by_r_d [key].append (value)
    # end def _add_approval

    def _lookup_approval (self, key, value = None) :
        if key not in self.apr_by_r_d :
            return None
        if value is None :
            return True
        for v in self.apr_by_r_d [key] :
            if v ['description'] == value :
                return True
        return False
    # end def _lookup_approval

    def add_approval_with_role (self, appr_order_id) :
        ord   = self.db.pr_approval_order.getnode (appr_order_id)
        # MUST be set
        assert ord.only_nosy is not None
        if ord.only_nosy and not self.email_only :
            return
        if not ord.only_nosy and self.email_only :
            return
        apr   = gen_pr_approval \
            ( self.db, self.do_create
            , order            = ord.order
            , purchase_request = self.pr.id
            , role             = ord.role.lower ()
            , role_id          = ord.id
            , description      = ord.role
            )
        self.apr_by_role [appr_order_id] = apr
    # end def add_approval_with_role

    def compute_approvals (self) :
        """ Compute approvals for current PR settings
            do_create specifies if the approvals are created or just a
            would-be list is computed. If email_only is specified we
            return a list of user ids *only* of the approval order
            entries with the only_nosy flag set. For normal approvals we
            do *not* return the entries with only_nosy set.
        """
        db = self.db
        _  = db.i18n.gettext
        pr = self.pr
        # Compute board and finance approval configs for this pr
        board_roles   = db.pr_approval_order.filter \
            (None, dict (is_board = True))
        finance_roles = db.pr_approval_order.filter \
            (None, dict (is_finance = True))
        # Check if there are any pr_approval_config entries with board or
        # finance roles
        ids = db.pr_approval_config.filter (None, dict (role = board_roles))
        bac = _app_cfgs (db, pr, ids)
        board_roles = set (ac.role for ac in bac)

        ids = db.pr_approval_config.filter (None, dict (role = finance_roles))
        fac = _app_cfgs (db, pr, ids)
        finance_roles = set (ac.role for ac in fac)

        if self.do_create and not board_roles :
            raise Reject \
                (_ ("Configuration error: No board roles for this PR"))
        if self.do_create and not finance_roles :
            raise Reject \
                (_ ("Configuration error: No finance roles for this PR"))
        board_approval = False

        assert not self.do_create  or pr.organisation
        assert not self.do_create  or pr.pr_currency
        assert not self.email_only or pr.organisation
        assert not self.email_only or pr.pr_currency
        cur = None
        if pr.pr_currency :
            cur = db.pr_currency.getnode (pr.pr_currency)
        assert not self.do_create  or pr.time_project or pr.sap_cc
        assert not self.email_only or pr.time_project or pr.sap_cc
        d = None
        pcc = None
        if pr.time_project :
            pcc = db.time_project.getnode (pr.time_project)
            d   = _ ('%(tp)s responsible/deputy') \
                % dict (tp = _ ('time_project'))
        elif pr.sap_cc :
            pcc = db.sap_cc.getnode (pr.sap_cc)
            d   = _ ('%(cc)s responsible/deputy') \
                % dict (cc = _ ('sap_cc'))
        if d :
            apr = gen_pr_approval \
                ( db, self.do_create
                , order            = 10
                , purchase_request = pr.id
                , user             = pcc.responsible
                , deputy           = pcc.deputy
                , deputy_gets_mail = pcc.deputy_gets_mail or False
                , description      = d
                )
            self._add_approval ((pcc.responsible, pcc.deputy), apr)
        for u in pr.special_approval :
            apr = gen_pr_approval \
                ( db, self.do_create
                , order            = 15
                , purchase_request = pr.id
                , user             = u
                , deputy           = u
                , description      = _ ("Special approval")
                )
            self._add_approval ((u, u), apr)

        max_risk = max_risk_type (db, pr.id)
        prc_ids  = db.pr_approval_config.filter (None, dict (valid = True))
        if cur :
            assert not self.do_create or pr.part_of_budget
            if pr.part_of_budget :
                pob = db.part_of_budget.getnode (pr.part_of_budget)
            else :
                pob = None
            s  = pr_offer_item_sum (db, pr.id)
            s  = s * 1.0 / cur.exchange_rate
            for prcid in prc_ids :
                prc = db.pr_approval_config.getnode (prcid)
                if prc.if_not_in_las and in_las (db, pr.id) :
                    continue
                if  (   prc.purchase_type
                    and pr.purchase_type not in prc.purchase_type
                    ) :
                    continue
                if  (   prc.pr_ext_resource
                    and pr.pr_ext_resource != prc.pr_ext_resource
                    ) :
                    continue
                if  (   prc.organisations and pr.organisation
                    and pr.organisation not in prc.organisations
                    ) :
                    continue
                if  (   prc.departments and pr.department
                    and pr.department not in prc.departments
                    ) :
                    continue
                if  (      prc.amount         is not None and s > prc.amount
                    or (   prc.infosec_amount is not None
                       and s > prc.infosec_amount
                       and max_risk
                       and (  'High' in max_risk.name
                           or max_risk.order >= 30
                           or self.infosec_level_lowered ()
                           )
                       )
                    or (   prc.payment_type_amount is not None
                       and s > prc.payment_type_amount
                       and need_payment_type_approval (db, pr)
                       )
                    or (   prc.oob_amount is not None
                       and pob
                       and pob.name.lower () == 'no'
                       and s > prc.oob_amount
                       )
                    ) :
                    self.add_approval_with_role (prc.role)
                    r = db.pr_approval_order.getnode (prc.role)
        oisum = pr_offer_item_sum (db, pr.id)
        if cur :
            min_head = self.team_group_head_approval (cur, oisum, pcc)
            if oisum > min_head :
                assert not self.do_create or pr.department
                if pr.department :
                    dep = db.department.getnode (pr.department)
                    if not dep.no_approval :
                        if not dep.manager and not dep.deputy :
                            raise Reject \
                                (_ ("Configuration error: No "
                                    "department manager and deputy"
                                   )
                                )
                        apr = gen_pr_approval \
                            ( db, self.do_create
                            , order            = 55
                            , purchase_request = pr.id
                            , user             = dep.manager
                            , deputy           = dep.deputy
                            , description      = "Department Head"
                            , deputy_gets_mail = dep.deputy_gets_mail or False
                            )
                        self._add_approval ((dep.manager, dep.deputy), apr)
        if cur and oisum > cur.min_sum :
            # Loop over order items and check if any is not on the approved
            # suppliers list
            supplier_approved = True
            for id in pr.offer_items :
                oi = db.pr_offer_item.getnode (id)
                if not self.supplier_is_approved (oi.pr_supplier) :
                    supplier_approved = False
            if pr.safety_critical and not supplier_approved :
                quality = db.pr_approval_order.lookup ('quality')
                self.add_approval_with_role (quality)

        assert not self.do_create or pr.purchase_type
        if pr.purchase_type :
            pt    = db.purchase_type.getnode (pr.purchase_type)
            roles = []
            if cur and pr_offer_item_sum (db, pr.id) > cur.min_sum :
                roles.extend (pt.pr_roles)
            roles.extend (pt.pr_forced_roles)
            # Make them unique
            roles = list (set (roles))
            for role in roles :
                self.add_approval_with_role (role)
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
            if cur :
                self.team_group_head_approval (cur, oisum, pcc)
            if (   pcc
               and not self._lookup_approval ((pcc.responsible, pcc.deputy))
               and cur
               ) :
                idx = oi.index or 0
                apr = gen_pr_approval \
                    ( db, self.do_create
                    , order            = 10 + idx * 0.001
                    , purchase_request = pr.id
                    , user             = pcc.responsible
                    , deputy           = pcc.deputy
                    , description      = d
                    )
                self._add_approval ((pcc.responsible, pcc.deputy), apr)
            if oi.purchase_type :
                pt    = db.purchase_type.getnode (oi.purchase_type)
                roles = []
                if cur and pr_offer_item_sum (db, pr.id) > cur.min_sum :
                    roles.extend (pt.pr_roles)
                roles.extend (pt.pr_forced_roles)
                for role in roles :
                    if role not in self.apr_by_role :
                        self.add_approval_with_role (role)
        if self.email_only :
            return self.compute_nosy_users ()
        if not self.do_create :
            vals = []
            for k in self.apr_by_r_d :
                vals.extend (self.apr_by_r_d [k])
            vals.extend (self.apr_by_role.values ())
            vals.sort (key = lambda x : x ['order'])
            return vals
    # end def compute_approvals

    def compute_nosy_users (self) :
        users = set ()
        for aoid in self.apr_by_role :
            ao  = self.db.pr_approval_order.getnode (aoid)
            apr = self.apr_by_role [aoid]
            assert isinstance (apr, dict)
            assert ao.only_nosy
            users.update (ao.users)
        # We return a set here, can be used to compute new nosy list
        return users
    # end def compute_nosy_users

    def infosec_level_lowered (self) :
        """ Check if the user specified a lower infosec_level than would be
            computed automagically
        """
        for oid in self.pr.offer_items :
            oi = self.db.pr_offer_item.getnode (oid)
            pg = self.db.product_group.getnode (oi.product_group)
            if pg.infosec_level :
                if oi.infosec_level is None :
                    return True
                pg_il = self.db.infosec_level.getnode (pg.infosec_level)
                oi_il = self.db.infosec_level.getnode (oi.infosec_level)
                if oi_il.order < pg_il.order :
                    return True
        return False
    # end def infosec_level_lowered

    def supplier_is_approved (self, sup_id) :
        if not sup_id :
            return False
        org     = self.pr.organisation
        ratings = self.db.pr_supplier_rating.filter \
            (None, dict (supplier = sup_id, organisation = org))
        assert len (ratings) <= 1
        if len (ratings) :
            sr = self.db.pr_supplier_rating.getnode (ratings [0])
            rating = self.db.pr_rating_category.getnode (sr.rating)
            if rating.order > 2 :
                return False
            return True
        return False
    # end def supplier_is_approved

    def team_group_head_approval (self, cur, oisum, cc_or_tc) :
        if not cc_or_tc :
            return None
        min_team = min_group = None
        # Checked by auditor:
        assert cur.min_sum is not None
        min_head = cur.min_sum
        if cur.max_team is not None and cc_or_tc.team_lead :
            min_team = cur.min_sum
            min_head = cur.max_team
        if cur.max_group is not None and cc_or_tc.group_lead :
            min_group = cur.min_sum
            if min_team is not None :
                min_group = cur.max_team
            min_head = cur.max_group
        if min_team is not None and min_team < oisum :
            u    = cc_or_tc.team_lead
            desc = 'Team Lead'
            key  = (u, u)
            if not self._lookup_approval (key, desc) :
                apr = gen_pr_approval \
                    ( self.db, self.do_create
                    , order            = 53
                    , purchase_request = self.pr.id
                    , user             = u
                    , deputy           = u
                    , description      = desc
                    )
                self._add_approval (key, apr)
        if min_group is not None and min_group < oisum :
            u    = cc_or_tc.group_lead
            desc = 'Group Lead'
            key  = (u, u)
            if not self._lookup_approval (key, desc) :
                apr = gen_pr_approval \
                    ( self.db, self.do_create
                    , order            = 54
                    , purchase_request = self.pr.id
                    , user             = u
                    , deputy           = u
                    , description      = desc
                    )
                self._add_approval (key, apr)
        assert min_head is not None
        return min_head
    # end def team_group_head_approval

# end class Approval_Logic

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

def compute_approvals (db, pr, do_create = False, email_only = False) :
    al = Approval_Logic (db, pr, do_create, email_only)
    return al.compute_approvals ()
# end def compute_approvals
