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
#
#++
# Name
#    pr
#
# Purpose
#    Schema definitions for Purchase Requests
#
#--
#

import common
from   schemacfg import schemadef
from   roundup   import date

def init \
    ( db
    , Boolean
    , Date
    , Link
    , Multilink
    , Number
    , String
    , Class
    , Department_Class
    , Ext_Class
    , Full_Issue_Class
    , Location_Class
    , Organisation_Class
    , Org_Location_Class
    , Time_Project_Class
    , ** kw
    ) :
    export = {}
    p_o_b = Class \
        ( db, ''"part_of_budget"
        , name                  = String    ()
        , order                 = Number    ()
        , description           = String    ()
        )
    p_o_b.setkey ('name')

    pr_currency = Class \
        ( db, ''"pr_currency"
        , name                  = String    ()
        , order                 = Number    ()
        , max_sum               = Number    ()
        , min_sum               = Number    ()
        )
    pr_currency.setkey ('name')

    pr_approval_status = Class \
        ( db, ''"pr_approval_status"
        , name                  = String    ()
        , order                 = Number    ()
        , transitions           = Multilink ("pr_approval_status")
        )
    pr_approval_status.setkey ('name')

    pr_approval = Class \
        ( db, ''"pr_approval"
        , role                  = String    ()
        , user                  = Link      ("user")
        , deputy                = Link      ("user")
        , by                    = Link      ("user")
        , status                = Link      ("pr_approval_status")
        , date                  = Date      ()
        , purchase_request      = Link      ("purchase_request")
        , order                 = Number    ()
        , description           = String    ()
        , msg                   = Link      ("msg")
        )

    pr_approval_order = Class \
        ( db, ''"pr_approval_order"
        , role                  = String    ()
        , order                 = Number    ()
        )
    pr_approval_order.setkey ('role')

    pr_offer_item = Class \
        ( db, ''"pr_offer_item"
        , index                 = Number    ()
        , description           = String    ()
        , units                 = Number    ()
        , price_per_unit        = Number    ()
        , pr_currency           = Link      ("pr_currency")
        , supplier              = String    ()
        , add_to_las            = Boolean   ()
        , pr_supplier           = Link      ("pr_supplier")
        , offer_number          = String    ()
        , vat                   = Number    ()
        , sap_cc                = Link      ("sap_cc")
        , time_project          = Link      ("time_project")
        , purchase_type         = Link      ("purchase_type")
        , is_asset              = Boolean   ()
        )

    pr_status = Class \
        ( db, ''"pr_status"
        , name                  = String    ()
        , order                 = Number    ()
        , transitions           = Multilink ("pr_status")
        , relaxed               = Boolean   ()
        )
    pr_status.setkey ('name')

    pr_supplier_rating = Class \
        ( db, ''"pr_supplier_rating"
        , name                  = String    ()
        , order                 = Number    ()
        )
    pr_supplier_rating.setkey ('name')

    pr_supplier = Class \
        ( db, ''"pr_supplier"
        , name                  = String    ()
        , sap_ref               = String    ()
        , ratings               = Multilink ("pr_supplier_rating_by_org")
        )
    pr_supplier.setkey ('name')

    pr_supplier_rating_by_org = Class \
        ( db, ''"pr_supplier_rating_by_org"
        , name                  = String    ()
        , rating                = Link      ("pr_supplier_rating")
        , organisation          = Link      ("organisation")
        )
    pr_supplier_rating_by_org.setkey ('name')

    purchase_type = Class \
        ( db, ''"purchase_type"
        , name                  = String    ()
        , order                 = Number    ()
        , roles                 = String    ()
        , view_roles            = String    ()
        , description           = String    ()
        , valid                 = Boolean   ()
        )
    purchase_type.setkey ('name')

    t_c = Class \
        ( db, ''"terms_conditions"
        , name                  = String    ()
        , order                 = Number    ()
        , description           = String    ()
        )
    t_c.setkey ('name')

    class PR (Full_Issue_Class) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( organisation          = Link      ("organisation")
                , department            = Link      ("department")
                , requester             = Link      ("user")
                , purchase_type         = Link      ("purchase_type")
                , safety_critical       = Boolean   ()
                , time_project          = Link      ("time_project")
                , part_of_budget        = Link      ("part_of_budget")
                , frame_purchase        = Boolean   ()
                , frame_purchase_end    = Date      ()
                , continuous_obligation = Boolean   ()
                , contract_term         = String    ()
                , termination_date      = Date      ()
                , intended_duration     = String    ()
                , terms_conditions      = Link      ("terms_conditions")
                , delivery_deadline     = Date      ()
                , renegotiations        = Boolean   ()
                , offer_items           = Multilink ("pr_offer_item")
                , status                = Link      ("pr_status")
                , total_cost            = Number    ()
                , pr_currency           = Link      ("pr_currency")
                , sap_cc                = Link      ("sap_cc")
                , sap_reference         = String    ()
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class PR
    pr = PR (db, ''"purchase_request")

    # Protect against dupe instantiation during i18n template generation
    if 'organisation' not in db.classes :
        Organisation_Class (db, ''"organisation")
    if 'location' not in db.classes :
        Location_Class (db, ''"location")
    if 'org_location' not in db.classes :
        Org_Location_Class (db, ''"org_location")
    if 'department' not in db.classes :
        Department_Class   (db, ''"department")
    if 'time_project' not in db.classes :
        Time_Project_Class (db, ''"time_project")
    return export
# end def init

def security (db, ** kw) :
    """ See the configuration and customisation document for information
        about security setup. Assign the access and edit Permissions for
        issue, file and message to regular users now
    """

    roles = \
        [ ("Board",             "Approvals over certain limits")
        , ("Nosy",              "Nosy list")
        , ("Finance",           "Finance-related approvals")
        , ("HR",                "Approvals for staff/subcontracting")
        , ("IT-Approval",       "Approve IT-Related PRs")
        , ("Procurement",       "Procurement department")
        , ("Procurement-Admin", "Procurement administration")
        , ("Procure-Approval",  "Procurement approvals")
        , ("Quality",           "Approvals for Safety issues")
        , ("Subcontract",       "Approvals for staff/subcontracting")
        , ("PR-View",           "See all Purchase Requests")
        ]

    #     classname        allowed to view   /  edit

    classes = \
        [ ("department",         ["User"],              [])
        , ("location",           ["User"],              [])
        , ("organisation",       ["User"],              [])
        , ("org_location",       ["User"],              [])
        , ("part_of_budget",     ["User"],              [])
        , ("pr_approval_order",  ["Procurement"],       ["Procurement-Admin"])
        , ("pr_approval",        ["Procurement","PR-View"], [])
        , ("pr_approval_status", ["User"],              [])
        , ("pr_currency",        ["User"],              ["Procurement-Admin"])
        , ("pr_status",          ["User"],              [])
        , ("pr_supplier",        ["User"],              ["Procurement-Admin"])
        , ("pr_supplier_rating", ["User"],              [])
        , ("pr_supplier_rating_by_org", ["User"],       ["Procurement-Admin"])
        , ("purchase_type",      ["User"],              ["Procurement-Admin"])
        , ("terms_conditions",   ["User"],              [])
        , ("time_project",       ["User"],              [])
        , ("user",               ["Procurement-Admin"], [])
        , ("purchase_request",   ["PR-View"],           [])
        , ("pr_offer_item",      ["PR-View"],           [])
        ]

    prop_perms = \
        [ ( "user", "Edit", ["Procurement-Admin"]
          , ("roles", "password")
          )
        , ( "user", "View", ["User"]
          , ("username", "id", "realname", "status")
          )
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

    tp_properties = \
        ( 'name', 'description', 'responsible', 'deputy', 'organisation'
        , 'status', 'id'
        , 'creation', 'creator', 'activity', 'actor'
        )
    # Search permission
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'time_project'
        , properties  = tp_properties
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'user'
        )
    db.security.addPermissionToRole ('Procurement-Admin', p)

    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'purchase_request'
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'pr_approval'
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'pr_offer_item'
        )
    db.security.addPermissionToRole ('User', p)

    db.security.addPermissionToRole ('User', 'Create', 'pr_offer_item')
    db.security.addPermissionToRole ('User', 'Create', 'purchase_request')

    fixdoc = schemadef.security_doc_from_docstring

    def view_role_pr (db, userid, itemid) :
        """ Users are allowed if they have one of the view roles
            of the purchase type
        """
        if not itemid or itemid < 1 :
            return False
        pr = db.purchase_request.getnode (itemid)
        if not pr.purchase_type :
            return False
        roles = db.purchase_type.get (pr.purchase_type, 'view_roles')
        roles = common.role_list (roles)
        if roles and common.user_has_role (db, userid, * roles) :
            return True
        return False
    # end def view_role_pr

    p = db.security.addPermission \
        ( name = 'View'
        , klass = 'purchase_request'
        , check = view_role_pr
        , description = fixdoc (view_role_pr.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = view_role_pr
        , description = fixdoc (view_role_pr.__doc__)
        , properties =
            ( 'sap_reference', 'terms_conditions', 'frame_purchase'
            , 'frame_purchase_end', 'nosy'
            )
        )
    db.security.addPermissionToRole ('User', p)

    def view_role_pr_offer (db, userid, itemid) :
        """ Users are allowed to view if they have one of the view roles
            of the purchase type
        """
        pr  = get_pr (db, itemid)
        if pr is None :
            return False
        return view_role_pr (db, userid, pr.id)
    # end def view_role_pr_offer

    p = db.security.addPermission \
        ( name = 'View'
        , klass = 'pr_offer_item'
        , check = view_role_pr_offer
        , description = fixdoc (view_role_pr_offer.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'pr_offer_item'
        , check = view_role_pr_offer
        , description = fixdoc (view_role_pr_offer.__doc__)
        , properties =
            ( 'add_to_las', 'supplier', 'pr_supplier', 'is_asset')
        )
    db.security.addPermissionToRole ('User', p)

    def approver_non_finance (db, userid, itemid) :
        """ Approvers are allowed if not finance and PR not yet approved
            by finance.
        """
        if not itemid or itemid < 1 :
            return False
        # User may not change
        if own_pr (db, userid, itemid) :
            return False
        # Finance may not change
        if common.user_has_role (db, userid, 'finance') :
            return False
        pr = db.purchase_request.getnode (itemid)
        st_approving = db.pr_status.lookup ('approving')
        if pr.status != st_approving :
            return False
        un = db.pr_approval_status.lookup ('undecided')
        ap = db.pr_approval.filter (None, dict (purchase_request = itemid))
        for id in ap :
            a = db.pr_approval.getnode (id)
            # already signed by finance?
            if a.status != un and a.role and a.role.lower () == 'finance' :
                return False
        return linked_pr (db, userid, itemid)
    # end def approver_non_finance

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = approver_non_finance
        , description = fixdoc (approver_non_finance.__doc__)
        , properties =
            ( 'continuous_obligation', 'termination_date', 'contract_term')
        )
    db.security.addPermissionToRole ('User', p)

    def approver_non_finance_offer (db, userid, itemid) :
        """ Approvers are allowed if not finance and PR not yet approved
            by finance.
        """
        pr  = get_pr (db, itemid)
        if pr is None :
            return False
        return approver_non_finance (db, userid, pr.id)
    # end def approver_non_finance_offer

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'pr_offer_item'
        , check = approver_non_finance_offer
        , description = fixdoc (approver_non_finance_offer.__doc__)
        , properties = ( 'vat',)
        )
    db.security.addPermissionToRole ('User', p)

    def own_pr (db, userid, itemid) :
        """ User is allowed permission on their own PRs if either creator or
            requester.
        """
        if not itemid or itemid < 1 :
            return False
        pr = db.purchase_request.getnode (itemid)
        if pr.creator == userid or pr.requester == userid :
            return True
        return False
    # end def own_pr

    p = db.security.addPermission \
        ( name = 'View'
        , klass = 'purchase_request'
        , check = own_pr
        , description = fixdoc (own_pr.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = own_pr
        , description = fixdoc (own_pr.__doc__)
        , properties = ('messages', 'nosy', 'files')
        )
    db.security.addPermissionToRole ('User', p)

    def open_or_approving (db, userid, itemid) :
        st_open      = db.pr_status.lookup ('open')
        st_approving = db.pr_status.lookup ('approving')
        pr           = db.purchase_request.getnode (itemid)
        if pr.status in (st_open, st_approving) :
            return True
        return False
    # end def open_or_approving

    def cancel_own_pr (db, userid, itemid) :
        """ User is allowed to cancel their own PR.
        """
        if not own_pr (db, userid, itemid) :
            return False
        return open_or_approving (db, userid, itemid)
    # end def cancel_own_pr

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = cancel_own_pr
        , description = fixdoc (cancel_own_pr.__doc__)
        , properties = ('status', 'messages', 'nosy')
        )
    db.security.addPermissionToRole ('User', p)

    def reopen_rejected_pr (db, userid, itemid) :
        """ User is allowed to reopen their own rejected PR.
        """
        if not own_pr (db, userid, itemid) :
            return False
        st_rejected  = db.pr_status.lookup ('rejected')
        pr           = db.purchase_request.getnode (itemid)
        if pr.status == st_rejected :
            return True
        return False
    # end def reopen_rejected_pr

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = reopen_rejected_pr
        , description = fixdoc (reopen_rejected_pr.__doc__)
        , properties = ('status', 'messages', 'nosy')
        )
    db.security.addPermissionToRole ('User', p)

    def own_pr_and_open (db, userid, itemid) :
        """ User is allowed to edit their own PRs (creator or requester)
            while PR is open.
        """
        if not own_pr (db, userid, itemid) :
            return False
        open = db.pr_status.lookup ('open')
        pr = db.purchase_request.getnode (itemid)
        if pr.status == open :
            return True
        return False
    # end def own_pr_and_open

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = own_pr_and_open
        , description = fixdoc (own_pr_and_open.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    def linked_pr (db, userid, itemid) :
        """ Users are allowed if an approval from them is
            linked to the PR.
        """
        if not itemid or itemid < 1 :
            return False
        pr = db.purchase_request.getnode (itemid)
        ap = db.pr_approval.filter (None, dict (purchase_request = itemid))
        for id in ap :
            a = db.pr_approval.getnode (id)
            if a.user == userid or a.deputy == userid :
                return True
            if a.role and common.user_has_role (db, userid, a.role) :
                return True
        return False
    # end def linked_pr

    p = db.security.addPermission \
        ( name = 'View'
        , klass = 'purchase_request'
        , check = linked_pr
        , description = fixdoc (linked_pr.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = linked_pr
        , description = fixdoc (linked_pr.__doc__)
        , properties  = ('messages', 'nosy', 'files')
        )
    db.security.addPermissionToRole ('User', p)

    def pending_approval (db, userid, itemid) :
        """ Users are allowed to edit message if a pending
            approval from them is linked to the PR.
        """
        if not linked_pr (db, userid, itemid) :
            return False
        if open_or_approving (db, userid, itemid) :
            return True
        # Also allow for reject because message is tried to attach twice
        # We allow this only for some time (5 min after last change)
        st_reject = db.pr_status.lookup ('rejected')
        pr        = db.purchase_request.getnode (itemid)
        if pr.status != st_reject :
            return False
        now = date.Date ('.')
        if pr.activity + date.Interval ('00:05:00') > now :
            return True
        return False
    # end def pending_approval

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = pending_approval
        , description = fixdoc (pending_approval.__doc__)
        , properties  = ('messages', 'nosy', 'files')
        )
    db.security.addPermissionToRole ('User', p)

    def linked_to_pr (db, userid, itemid) :
        """ Users are allowed to view if approval is linked to viewable PR.
        """
        if not itemid or itemid < 1 :
            return False
        ap = db.pr_approval.getnode (itemid)
        pr = ap.purchase_request
        if own_pr (db, userid, pr) :
            return True
        if linked_pr (db, userid, pr) :
            return True
        return False
    # end def linked_to_pr

    p = db.security.addPermission \
        ( name = 'View'
        , klass = 'pr_approval'
        , check = linked_to_pr
        , description = fixdoc (linked_to_pr.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    def approval_undecided (db, userid, itemid) :
        """ User is allowed to change status of undecided approval if
            they are the owner/deputy or have appropriate role.
        """
        if not itemid or itemid < 1 :
            return False
        ap           = db.pr_approval.getnode (itemid)
        pr           = db.purchase_request.getnode (ap.purchase_request)
        und          = db.pr_approval_status.lookup ('undecided')
        st_open      = db.pr_status.lookup ('open')
        st_approving = db.pr_status.lookup ('approving')
        if  (   ap.status == und
            and (  ap.user   == userid
                or ap.deputy == userid
                or (ap.role and common.user_has_role (db, userid, ap.role))
                )
            and pr.status in (st_open, st_approving)
            ) :
            return True
        return False
    # end def approval_undecided

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'pr_approval'
        , check = approval_undecided
        , description = fixdoc (approval_undecided.__doc__)
        , properties = ('status', 'msg')
        )
    db.security.addPermissionToRole ('User', p)

    def get_pr (db, itemid) :
        prs = db.purchase_request.filter (None, dict (offer_items = itemid))
        if len (prs) == 0 :
            return None
        assert len (prs) == 1
        return db.purchase_request.getnode (prs [0])
    # end def get_pr

    def linked_from_pr (db, userid, itemid) :
        """ Users are allowed to view if offer is linked from PR.
        """
        if not itemid or itemid < 1 :
            return True
        off = db.pr_offer_item.getnode (itemid)
        pr  = get_pr (db, itemid)
        if pr is None :
            return False
        if own_pr (db, userid, pr.id) :
            return True
        if linked_pr (db, userid, pr.id) :
            return True
        return False
    # end def linked_from_pr

    p = db.security.addPermission \
        ( name = 'View'
        , klass = 'pr_offer_item'
        , check = linked_from_pr
        , description = fixdoc (linked_from_pr.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    def add_to_las_false (db, userid, itemid) :
        """ Allow setting add_to_las from 'None' for orphanes offer items.
        """
        if itemid is None :
            return False
        oi = db.pr_offer_item.getnode (itemid)
        pr = get_pr (db, itemid)
        if pr is not None :
            return False
        if oi.add_to_las is None :
            return True
        return False
    # end def add_to_las_false

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'pr_offer_item'
        , check = add_to_las_false
        , description = fixdoc (add_to_las_false.__doc__)
        , properties = ('add_to_las',)
        )
    db.security.addPermissionToRole ('User', p)

    def linked_and_editable (db, userid, itemid) :
        """ Users are allowed to edit if offer is linked from PR and PR
            is editable.
        """
        if not itemid or itemid < 1 :
            return True
        if not linked_from_pr (db, userid, itemid) :
            return False
        pr  = get_pr (db, itemid)
        if pr is None :
            return False
        return own_pr_and_open (db, userid, pr.id)
    # end def linked_and_editable

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'pr_offer_item'
        , check = linked_and_editable
        , description = fixdoc (linked_and_editable.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    def approved_or_ordered (db, userid, itemid) :
        """ User with view role is allowed editing if status
            is 'approved' or 'ordered'
        """
        if not view_role_pr (db, userid, itemid) :
            return False
        pr = db.purchase_request.getnode (itemid)
        stati = []
        for n in ('approved', 'ordered') :
            try :
                st = db.pr_status.lookup (n)
                stati.append (st)
            except KeyError :
                pass
        if pr.status in stati :
            return True
        return False
    # end def approved_or_ordered

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'purchase_request'
        , check       = approved_or_ordered
        , description = fixdoc (approved_or_ordered.__doc__)
        , properties  = ('status', 'messages', 'files', 'nosy')
        )
    db.security.addPermissionToRole ('User', p)

    schemadef.register_nosy_classes (db, ['purchase_request'])

    def user_on_nosy (db, userid, itemid) :
        """ User is allowed if on the nosy list
        """
        pr = db.purchase_request.getnode (itemid)
        if userid in pr.nosy :
            return True
    # end def user_on_nosy

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'purchase_request'
        , check       = user_on_nosy
        , description = fixdoc (user_on_nosy.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'purchase_request'
        , check       = user_on_nosy
        , description = fixdoc (user_on_nosy.__doc__)
        , properties  = ('messages', 'files', 'nosy')
        )
    db.security.addPermissionToRole ('User', p)

    def user_on_nosy_approval (db, userid, itemid) :
        """ User is allowed if on the nosy list of the PR
        """
        ap = db.pr_approval.getnode (itemid)
        return user_on_nosy (db, userid, ap.purchase_request)
    # end def user_on_nosy

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'pr_approval'
        , check       = user_on_nosy_approval
        , description = fixdoc (user_on_nosy_approval.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    def user_on_nosy_offer (db, userid, itemid) :
        """ User is allowed if on the nosy list of the PR
        """
        if not itemid or itemid < 1 :
            return True
        prs = db.purchase_request.filter (None, dict (offer_items = itemid))
        assert len (prs) <= 1
        if prs :
            return user_on_nosy (db, userid, prs [0])
        return False
    # end def user_on_nosy

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'pr_offer_item'
        , check       = user_on_nosy_offer
        , description = fixdoc (user_on_nosy_offer.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

# end def security
