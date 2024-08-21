# -*- coding: iso-8859-1 -*-
# Copyright (C) 2015-22 Dr. Ralf Schlatterbeck Open Source Consulting.
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
import prlib
import o_permission
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
    , Ext_Class
    , Full_Issue_Class
    , Location_Class
    , Organisation_Class
    , Org_Location_Class
    , Time_Project_Status_Class
    , Currency_Class
    , O_Permission_Class
    , ** kw
    ):
    export = {}

    # Infosec data structures
    infosec_level = Class \
        ( db, ''"infosec_level"
        , name                  = String    ()
        , order                 = Number    ()
        , is_consulting         = Boolean   ()
        )
    infosec_level.setkey ('name')

    security_req_group = Class \
        ( db, ''"security_req_group"
        , name                  = String    ()
        , is_consulting         = Boolean   ()
        )
    security_req_group.setkey ('name')

    pg_category = Class \
        ( db, ''"pg_category"
        , name                  = String    ()
        , sap_ref               = String    ()
        )
    pg_category.setkey ('name')
    pg_category.setorderprop ('sap_ref')

    product_group = Class \
        ( db, ''"product_group"
        , name                  = String    ()
        , security_req_group    = Link      ('security_req_group')
        , infosec_level         = Link      ('infosec_level')
        , sap_ref               = String    ()
        , pg_category           = Link      ('pg_category')
        )
    product_group.setkey ('name')
    product_group.setorderprop ('sap_ref')

    supplier_risk_category = Class \
        ( db, ''"supplier_risk_category"
        , name                  = String    ()
        , order                 = Number    ()
        )
    supplier_risk_category.setkey ('name')

    purchase_risk_type = Class \
        ( db, ''"purchase_risk_type"
        , name                  = String    ()
        , order                 = Number    ()
        )
    purchase_risk_type.setkey ('name')

    purchase_security_risk = Class \
        ( db, ''"purchase_security_risk"
        , supplier_risk_category = Link      ('supplier_risk_category')
        , infosec_level          = Link      ('infosec_level')
        , purchase_risk_type     = Link      ('purchase_risk_type')
        )

    pr_supplier_risk = Class \
        ( db, ''"pr_supplier_risk"
        , supplier               = Link      ("pr_supplier")
        , organisation           = Link      ("organisation")
        , security_req_group     = Link      ("security_req_group")
        , supplier_risk_category = Link      ("supplier_risk_category")
        )

    # PR-Tracker data
    p_o_b = Class \
        ( db, ''"part_of_budget"
        , name                  = String    ()
        , order                 = Number    ()
        , description           = String    ()
        )
    p_o_b.setkey ('name')

    payment_type = Class \
        ( db, ''"payment_type"
        , name                  = String    ()
        , order                 = Number    ()
        , need_approval         = Boolean   ()
        )
    payment_type.setkey ('name')

    pr_currency = Currency_Class \
        ( db, ''"pr_currency"
        , min_sum               = Number    ()
        , max_team              = Number    ()
        , max_group             = Number    ()
        )

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
        , role_id               = Link      ( "pr_approval_order"
                                            , do_journal = 'no'
                                            )
        , user                  = Link      ("user", do_journal = 'no')
        , deputy                = Link      ("user", do_journal = 'no')
        , deputy_gets_mail      = Boolean   ()
        , by                    = Link      ("user", do_journal = 'no')
        , status                = Link      ("pr_approval_status")
        , date                  = Date      ()
        , purchase_request      = Link      ( "purchase_request"
                                            , rev_multilink='approvals'
                                            )
        , order                 = Number    ()
        , description           = String    ()
        , msg                   = Link      ("msg")
        )

    pr_approval_config = Class \
        ( db, ''"pr_approval_config"
        , role                  = Link      ("pr_approval_order")
        , amount                = Number    ()
        , if_not_in_las         = Boolean   ()
        , valid                 = Boolean   ()
        , organisations         = Multilink ("organisation")
        , pr_ext_resource       = Link      ("pr_ext_resource")
        , purchase_type         = Multilink ("purchase_type")
        , infosec_amount        = Number    ()
        , payment_type_amount   = Number    ()
        , oob_amount            = Number    ()
        , departments           = Multilink ("department")
        )

    pr_approval_order = Class \
        ( db, ''"pr_approval_order"
        , role                  = String    ()
        , order                 = Number    ()
        , users                 = Multilink ("user")
        , is_finance            = Boolean   ()
        , is_board              = Boolean   ()
        , want_no_messages      = Boolean   ()
        , only_nosy             = Boolean   ()
        )
    pr_approval_order.setkey ('role')

    pr_ext_resource = Class \
        ( db, ''"pr_ext_resource"
        , name                  = String    ()
        )
    pr_ext_resource.setkey ('name')

    pr_offer_item = Class \
        ( db, ''"pr_offer_item"
        , index                 = Number    ()
        , description           = String    ()
        , units                 = Number    ()
        , price_per_unit        = Number    ()
        , pr_currency           = Link      ("pr_currency", do_journal = 'no')
        , supplier              = String    ()
        , add_to_las            = Boolean   ()
        , pr_supplier           = Link      ("pr_supplier")
        , offer_number          = String    ()
        , vat                   = Number    ()
        , sap_cc                = Link      ("sap_cc")
        , time_project          = Link      ("time_project")
        , psp_element           = Link      ("psp_element")
        , purchase_type         = Link      ("purchase_type")
        , is_asset              = Boolean   ()
        , product_group         = Link      ("product_group", do_journal = 'no')
        , infosec_level         = Link      ("infosec_level", do_journal = 'no')
        , payment_type          = Link      ("payment_type",  do_journal = 'no')
        , internal_order        = Link      ( "internal_order"
                                            , try_id_parsing = 'no'
                                            , do_journal     = 'no'
                                            )
        , gl_account            = String    ()
        )

    pr_status = Class \
        ( db, ''"pr_status"
        , name                  = String    ()
        , order                 = Number    ()
        , transitions           = Multilink ("pr_status")
        , relaxed               = Boolean   ()
        )
    pr_status.setkey ('name')

    pr_rating_category = Class \
        ( db, ''"pr_rating_category"
        , name                  = String    ()
        , order                 = Number    ()
        )
    pr_rating_category.setkey ('name')

    pr_supplier = Class \
        ( db, ''"pr_supplier"
        , name                  = String    ()
        , sap_ref               = String    ()
        )
    pr_supplier.setkey ('name')

    pr_supplier_rating = Class \
        ( db, ''"pr_supplier_rating"
        , rating                = Link      ("pr_rating_category")
        , organisation          = Link      ("organisation")
        , supplier              = Link      ("pr_supplier")
        , scope                 = String    ()
        )

    purchase_type = Class \
        ( db, ''"purchase_type"
        , name                  = String    ()
        , order                 = Number    ()
        , description           = String    ()
        , valid                 = Boolean   ()
        , confidential          = Boolean   ()
        , pr_roles              = Multilink ("pr_approval_order")
        , pr_forced_roles       = Multilink ("pr_approval_order")
        , pr_view_roles         = Multilink ("pr_approval_order")
        , nosy                  = Multilink ("user")
        , purchasing_agents     = Multilink ("user")
        , allow_gl_account      = Boolean   ()
        , organisations         = Multilink ("organisation")
        )
    purchase_type.setkey ('name')

    t_c = Class \
        ( db, ''"terms_conditions"
        , name                  = String    ()
        , order                 = Number    ()
        , description           = String    ()
        )
    t_c.setkey ('name')

    io = Class \
        ( db, ''"internal_order"
        , order_number          = String    ()
        , name                  = String    ()
        , valid                 = Boolean   ()
        )
    io.setkey ('order_number')

    psp = Class \
        ( db, ''"psp_element"
        , number                = String    ()
        , name                  = String    ()
        , valid                 = Boolean   ()
        , project               = Link      ("time_project")
        , organisation          = Link      ("organisation")
        , project_org           = String    ()
        )
    psp.setkey ('number')
    psp.setorderprop ('project_org')

    class PR (Full_Issue_Class):
        def __init__ (self, db, classname, ** properties):
            self.update_properties \
                ( organisation          = Link      ( "organisation"
                                                    , do_journal = 'no'
                                                    )
                , department            = Link      ( "department"
                                                    , do_journal = 'no'
                                                    )
                , requester             = Link      ( "user"
                                                    , do_journal = 'no'
                                                    )
                , purchase_type         = Link      ( "purchase_type"
                                                    , do_journal = 'no'
                                                    )
                , safety_critical       = Boolean   ()
                , time_project          = Link      ( "time_project"
                                                    , do_journal = 'no'
                                                    )
                , psp_element           = Link      ( "psp_element"
                                                    , do_journal = 'no'
                                                    )
                , part_of_budget        = Link      ( "part_of_budget"
                                                    , do_journal = 'no'
                                                    )
                , frame_purchase        = Boolean   ()
                , frame_purchase_end    = Date      ()
                , continuous_obligation = Boolean   ()
                , contract_term         = String    ()
                , termination_date      = Date      ()
                , intended_duration     = String    ()
                , terms_conditions      = Link      ( "terms_conditions"
                                                    , do_journal = 'no'
                                                    )
                , delivery_deadline     = Date      ()
                , renegotiations        = Boolean   ()
                , offer_items           = Multilink ("pr_offer_item")
                , status                = Link      ( "pr_status"
                                                    , do_journal = 'no'
                                                    )
                , total_cost            = Number    ()
                , pr_currency           = Link      ( "pr_currency"
                                                    , do_journal = 'no'
                                                    )
                , sap_cc                = Link      ("sap_cc"
                                                    , do_journal = 'no'
                                                    )
                , sap_reference         = String    ()
                , purchasing_agents     = Multilink ("user"
                                                    , do_journal = 'no'
                                                    )
                , pr_justification      = String    ()
                , pr_risks              = String    ()
                , internal_order        = Link
                                          ( "internal_order"
                                          , try_id_parsing = 'no'
                                          , do_journal     = 'no'
                                          )
                , special_approval      = Multilink ("user", do_journal = 'no')
                , pr_ext_resource       = Link      ("pr_ext_resource")
                , issue_ids             = String    ()
                # Currently not used, but keep it in the DB:
                , infosec_project       = Boolean   ()
                , infosec_level         = Link      ( "infosec_level"
                                                    , do_journal = 'no'
                                                    )
                , purchase_risk_type    = Link      ( "purchase_risk_type"
                                                    , do_journal = 'no'
                                                    )
                , date_approved         = Date      ()
                , date_ordered          = Date      ()
                , renew_until           = Date      ()
                , payment_type          = Link      ( "payment_type"
                                                    , do_journal = 'no'
                                                    )
                , gl_account            = String    ()
                , charge_to             = Link      ('organisation'
                                                    , do_journal = 'no'
                                                    )
                , delivery_address      = Link      ('location'
                                                    , do_journal = 'no'
                                                    )
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class PR
    pr = PR (db, ''"purchase_request")

    assert 'time_project' not in db.classes
    class PR_Time_Project_Class (kw ['Time_Project_Class']):
        def __init__ (self, db, classname, ** properties):
            self.update_properties \
                ( deputy_gets_mail      = Boolean   ()
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class PR_Time_Project_Class
    PR_Time_Project_Class (db, ''"time_project")

    assert 'sap_cc' not in db.classes
    class PR_SAP_CC_Class (kw ['SAP_CC_Class']):
        def __init__ (self, db, classname, ** properties):
            self.update_properties \
                ( deputy_gets_mail      = Boolean   ()
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class PR_SAP_CC_Class
    PR_SAP_CC_Class (db, ''"sap_cc")

    Dep_Ancestor = kw ['Department_Class']
    class Department_Class (Dep_Ancestor):
        """ Add some attributes to department """
        def __init__ (self, db, classname, ** properties):
            self.update_properties \
                ( nosy                  = Multilink ("user")
                , deputy_gets_mail      = Boolean   ()
                , no_approval           = Boolean   ()
                )
            Dep_Ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Department_Class
    export.update (dict (Department_Class = Department_Class))
    assert 'department' not in db.classes
    Department_Class (db, ''"department")

    # Protect against dupe instantiation during i18n template generation
    if 'organisation' not in db.classes:
        Organisation_Class (db, ''"organisation")
    assert 'location' not in db.classes

    class LC (Location_Class):
        """ Add some attributes to Location
        """
        def __init__ (self, db, classname, ** properties):
            self.update_properties (order = Number ())
            Location_Class.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class LC

    LC (db, ''"location")
    if 'org_location' not in db.classes:
        Org_Location_Class (db, ''"org_location")
    if 'time_project_status' not in db.classes:
        Time_Project_Status_Class (db, ''"time_project_status")

    User_Ancestor = kw.get ('User_Class', Ext_Class)
    class User_Class (User_Ancestor):
        """ add some attrs to user class
        """
        def __init__ (self, db, classname, ** properties):
            self.update_properties \
                ( want_no_messages       = Boolean   ()
                , subst_until            = Date      ()
                , organisation           = Link      ("organisation")
                )
            User_Ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Class
    export.update (dict (User_Class = User_Class))

    o_perm = O_Permission_Class \
        ( db, ''"o_permission"
        , organisation = Multilink ("organisation")
        )

    return export
# end def init

def security (db, ** kw):
    """ See the configuration and customisation document for information
        about security setup.
    """

    roles = \
        [ ("Board",                "Approvals over certain limits")
        , ("Nosy",                 "Nosy list")
        , ("Finance",              "Finance-related approvals")
        , ("HR",                   "Approvals for staff/subcontracting")
        , ("HR-Approval",          "Approvals for HR-related issues")
        , ("IT-Approval",          "Approve IT-Related PRs")
        , ("Procurement-Admin",    "Procurement administration")
        , ("Procure-Approval",     "Procurement approvals")
        , ("Quality",              "Approvals for Safety issues")
        , ("Subcontract",          "Approvals for staff/subcontracting")
        , ("Measurement-Approval", "Responsible for Measurement-Equipment")
        , ("Training-Approval",    "Approvals for Training")
        , ("Subcontract-Org",      "Approvals for Subcontracting")
        , ("CISO",                 "Editing of Security Tables")
        # LAS is 'List of Approved Suppliers'
        , ("LAS",                  "Supplier management")
        ]

    #     classname        allowed to view   /  edit

    classes = \
        [ ("department",         ["User"],              [])
        , ("infosec_level",      ["User"],              ["Procurement-Admin"])
        , ("location",           ["User"],              ["Procurement-Admin"])
        , ("organisation",       ["User"],              [])
        , ("org_location",       ["User"],              [])
        , ("part_of_budget",     ["User"],              [])
        , ("pr_approval_config", [],                    ["Procurement-Admin"])
        , ("pr_approval_order",  ["User"],              ["Procurement-Admin"])
        , ("pr_approval_status", ["User"],              [])
        , ("pr_currency",        ["User"],              ["Procurement-Admin"])
        , ("pr_status",          ["User"],              [])
        , ("pr_supplier",        ["User"],       ["Procurement-Admin", "LAS"])
        , ("pr_rating_category", ["User"],       ["Procurement-Admin", "LAS"])
        , ("pr_supplier_rating", [],                    ["Procurement-Admin"])
        , ("purchase_type",      [],                    ["Procurement-Admin"])
        , ("terms_conditions",   ["User"],              [])
        , ("user",               ["Procurement-Admin"], [])
        , ("internal_order",     ["User"],              [])
        , ("pr_ext_resource",    ["User"],              [])
        , ("security_req_group", ["User"],      ["Procurement-Admin", "CISO"])
        , ("product_group",      ["User"],              ["Procurement-Admin"])
        , ("pg_category",        ["User"],              ["Procurement-Admin"])
        , ("supplier_risk_category", ["User"],          [])
        , ("purchase_risk_type", ["User"],              [])
        , ("pr_supplier_risk",   [],                    ["Procurement-Admin"])
        , ("payment_type",       ["User"],              [])
        , ("purchase_security_risk", ["User"],          [])
        ]

    prop_perms = \
        [ ( "user", "Edit", ["Procurement-Admin"]
          , ("roles", "password", "substitute", "subst_until", "clearance_by")
          )
        , ( "user", "View", ["User"]
          , ("username", "id", "realname", "status", "address")
          )
        , ( "user", "Edit", ["Procurement-Admin"]
          , ("want_no_messages",)
          )
        # Allow anybody to edit purchase_request but do not allow change
        # (in reactor): This is used for ordering actions in the web
        # interface via links (!)
        , ( "pr_approval", "Edit", ["User"]
          , ("purchase_request", "date")
          )
        , ( "purchase_request", "Edit", ["Procurement-Admin"]
          , ("renew_until",)
          )
        , ( "time_project", "Edit", ["Procurement-Admin"]
          , ("deputy_gets_mail",)
          )
        , ( "sap_cc", "Edit", ["Procurement-Admin"]
          , ("deputy_gets_mail",)
          )
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

    # Retire/Restore permission for pr_approval_order
    for n in 'Retire', 'Restore':
        p = db.security.addPermission \
            ( name        = n
            , klass       = 'pr_approval_order'
            )
        db.security.addPermissionToRole ('Procurement-Admin', p)
    tp_properties = \
        ( 'name', 'description', 'responsible', 'deputy', 'organisation'
        , 'status', 'id'
        , 'creation', 'creator', 'activity', 'actor'
        )
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

    def pr_pt_role (db, userid, itemid):
        """ Users are allowed if they have one of the view roles
            of the purchase type or one of the (forced) approval roles.
        """
        if not itemid or int (itemid) < 1:
            return False
        pr = db.purchase_request.getnode (itemid)
        if not o_permission.purchase_request_allowed_by_org \
            (db, userid, itemid):
            return False
        if not pr.purchase_type:
            return False
        pt = db.purchase_type.getnode (pr.purchase_type)
        roles = set (pt.pr_view_roles)
        roles.update (pt.pr_roles)
        roles.update (pt.pr_forced_roles)
        for r in roles:
            if prlib.has_pr_role (db, userid, r):
                return True
        return False
    # end def pr_pt_role

    p = db.security.addPermission \
        ( name = 'View'
        , klass = 'purchase_request'
        , check = pr_pt_role
        , description = fixdoc (pr_pt_role.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = pr_pt_role
        , description = fixdoc (pr_pt_role.__doc__)
        , properties =
            ( 'sap_reference', 'terms_conditions', 'frame_purchase'
            , 'frame_purchase_end', 'nosy', 'messages', 'purchasing_agents'
            , 'internal_order', 'special_approval', 'payment_type'
            , 'delivery_address'
            )
        )
    db.security.addPermissionToRole ('User', p)

    def pt_role_offer_item (db, userid, itemid):
        """ Users are allowed to view if they have one of the view roles
            of the purchase type
        """
        pr  = get_pr_from_offer_item (db, itemid)
        if pr is None:
            return False
        return pr_pt_role (db, userid, pr.id)
    # end def pt_role_offer_item

    p = db.security.addPermission \
        ( name = 'View'
        , klass = 'pr_offer_item'
        , check = pt_role_offer_item
        , description = fixdoc (pt_role_offer_item.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'pr_offer_item'
        , check = pt_role_offer_item
        , description = fixdoc (pt_role_offer_item.__doc__)
        , properties =
            ( 'add_to_las'
            , 'supplier'
            , 'pr_supplier'
            , 'is_asset'
            , 'payment_type'
            , 'internal_order'
            )
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'pr_offer_item'
        , properties =
            ( 'add_to_las'
            ,
            )
        )
    db.security.addPermissionToRole ('CISO', p)
    db.security.addPermissionToRole ('LAS', p)
    p = db.security.addPermission \
        ( name = 'View'
        , klass = 'pr_offer_item'
        , properties =
            ( 'add_to_las'
            , 'supplier'
            , 'pr_supplier'
            , 'creation'
            , 'creator'
            , 'activity'
            , 'actor'
            )
        )
    db.security.addPermissionToRole ('CISO', p)
    db.security.addPermissionToRole ('LAS', p)

    def view_role_approval (db, userid, itemid):
        """ Users are allowed to view if they have one of the view roles
            of the purchase type
        """
        sp = db.pr_approval.getnode (itemid)
        pr = db.purchase_request.getnode (sp.purchase_request)
        if pr is None:
            return False
        return pr_pt_role (db, userid, pr.id)
    # end def view_role_approval

    p = db.security.addPermission \
        ( name = 'View'
        , klass = 'pr_approval'
        , check = view_role_approval
        , description = fixdoc (view_role_approval.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    def approver_non_finance (db, userid, itemid):
        """ Approvers are allowed if not finance and PR not yet approved
            by finance.
        """
        if not itemid or int (itemid) < 1:
            return False
        # User may not change
        if own_pr (db, userid, itemid):
            return False
        # Finance may not change
        if common.user_has_role (db, userid, 'finance'):
            return False
        pr = db.purchase_request.getnode (itemid)
        st_approving = db.pr_status.lookup ('approving')
        if pr.status != st_approving:
            return False
        un = db.pr_approval_status.lookup ('undecided')
        ap = db.pr_approval.filter (None, dict (purchase_request = itemid))
        for id in ap:
            a = db.pr_approval.getnode (id)
            # already signed by finance?
            finance = db.pr_approval_order.filter \
                (None, dict (is_finance = True))
            if a.status != un and a.role_id in finance:
                return False
        return linked_pr (db, userid, itemid)
    # end def approver_non_finance

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = approver_non_finance
        , description = fixdoc (approver_non_finance.__doc__)
        , properties =
            ( 'continuous_obligation', 'intended_duration', 'contract_term')
        )
    db.security.addPermissionToRole ('User', p)

    def approver_non_finance_offer (db, userid, itemid):
        """ Approvers are allowed if not finance and PR not yet approved
            by finance.
        """
        pr  = get_pr_from_offer_item (db, itemid)
        if pr is None:
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

    def own_pr (db, userid, itemid):
        """ User is allowed permission on their own PRs if either creator or
            requester or supervisor of requester.
        """
        if not itemid or int (itemid) < 1:
            return False
        pr = db.purchase_request.getnode (itemid)
        if pr.creator == userid or pr.requester == userid:
            return True
        sup = db.user.get (pr.requester, 'supervisor')
        if sup and sup == userid:
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
        , properties = ('messages', 'nosy', 'files', 'renew_until')
        )
    db.security.addPermissionToRole ('User', p)

    def open_or_approving (db, userid, itemid):
        st_open      = db.pr_status.lookup ('open')
        st_approving = db.pr_status.lookup ('approving')
        pr           = db.purchase_request.getnode (itemid)
        if pr.status in (st_open, st_approving):
            return True
        return False
    # end def open_or_approving

    def until_ordered (db, userid, itemid):
        if open_or_approving (db, userid, itemid):
            return True
        pr          = db.purchase_request.getnode (itemid)
        stati = []
        unwanted = ('ordered', 'rejected', 'cancelled')
        for st in db.pr_status.getnodeids (retired = False):
            status = db.pr_status.getnode (st)
            if status.name in unwanted:
                continue
            stati.append (st)
        if pr.status in stati:
            return True
        return False
    # end def until_ordered

    def until_ordered_oi (db, userid, itemid):
        pr  = get_pr_from_offer_item (db, itemid)
        if pr is None:
            return False
        return until_ordered (db, userid, pr.id)
    # def until_ordered_oi

    def cancel_own_pr (db, userid, itemid):
        """ User is allowed to cancel their own PR.
        """
        if not own_pr (db, userid, itemid):
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

    def edit_pr_justification (db, userid, itemid):
        """ User is allowed to edit PR Justification
            if the PR has appropriate status
            and the user is creator or owner of the PR or has one of the
            view roles.
        """
        st_open      = db.pr_status.lookup ('open')
        st_approving = db.pr_status.lookup ('approving')
        st_rejected  = db.pr_status.lookup ('rejected')
        st_approved  = db.pr_status.lookup ('approved')
        stati        = (st_open, st_approving, st_rejected, st_approved)
        pr           = db.purchase_request.getnode (itemid)
        if pr.status not in stati:
            return False
        if own_pr (db, userid, itemid):
            return True
        if pr_pt_role (db, userid, itemid):
            return True
        return False
    # end def edit_pr_justification

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = edit_pr_justification
        , description = fixdoc (edit_pr_justification.__doc__)
        , properties = ('pr_justification',)
        )
    db.security.addPermissionToRole ('User', p)

    def cancel_open_pr (db, userid, itemid):
        """ User is allowed to cancel a PR if it is open
        """
        st_open      = db.pr_status.lookup ('open')
        pr           = db.purchase_request.getnode (itemid)
        if pr.status == st_open:
            return True
        return False
    # end def cancel_open_pr

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = cancel_open_pr
        , description = fixdoc (cancel_open_pr.__doc__)
        , properties = ('status', 'messages')
        )
    db.security.addPermissionToRole ('Procurement-Admin', p)

    def approving_or_approved (db, userid, itemid):
        """ User is allowed to reject PR in state approving or approved
        """
        st_approving = db.pr_status.lookup ('approving')
        st_approved  = db.pr_status.lookup ('approved')
        pr           = db.purchase_request.getnode (itemid)
        if pr.status in (st_approving, st_approved):
            return True
        return False
    # end def approving_or_approved

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = approving_or_approved
        , description = fixdoc (approving_or_approved.__doc__)
        , properties = ('status', 'messages')
        )
    for r in prlib.reject_roles:
        db.security.addPermissionToRole (r, p)

    def reopen_rejected_pr (db, userid, itemid):
        """ User is allowed to reopen their own rejected PR.
        """
        if not own_pr (db, userid, itemid):
            return False
        st_rejected  = db.pr_status.lookup ('rejected')
        pr           = db.purchase_request.getnode (itemid)
        if pr.status == st_rejected:
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

    def own_pr_and_open_or_rej (db, userid, itemid):
        """ User is allowed to edit their own PRs (creator or requester
            or supervisor of requester) while PR is open or rejected.
        """
        if not own_pr (db, userid, itemid):
            return False
        open = db.pr_status.lookup ('open')
        rej  = db.pr_status.lookup ('rejected')
        pr = db.purchase_request.getnode (itemid)
        if pr.status == open or pr.status == rej:
            return True
        return False
    # end def own_pr_and_open_or_rej

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = own_pr_and_open_or_rej
        , description = fixdoc (own_pr_and_open_or_rej.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    def linked_pr (db, userid, itemid):
        """ Users are allowed if an approval from them is
            linked to the PR.
        """
        if not itemid or int (itemid) < 1:
            return False
        pr = db.purchase_request.getnode (itemid)
        ap = db.pr_approval.filter (None, dict (purchase_request = itemid))
        for id in ap:
            a = db.pr_approval.getnode (id)
            # User or deputy or delegated?
            if userid in common.approval_by (db, a.user):
                return True
            if userid in common.approval_by (db, a.deputy):
                return True
            if a.role_id and prlib.has_pr_role (db, userid, a.role_id):
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

    def pending_approval (db, userid, itemid):
        """ Users are allowed to edit message if a pending
            approval from them is linked to the PR.
        """
        if not linked_pr (db, userid, itemid):
            return False
        if open_or_approving (db, userid, itemid):
            return True
        # Also allow for reject because message is tried to attach twice
        # We allow this only for some time (5 min after last change)
        st_reject = db.pr_status.lookup ('rejected')
        pr        = db.purchase_request.getnode (itemid)
        if pr.status != st_reject:
            return False
        now = date.Date ('.')
        if pr.activity + date.Interval ('00:05:00') > now:
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

    def linked_to_pr (db, userid, itemid):
        """ Users are allowed to view if approval is linked to viewable PR.
        """
        if not itemid or int (itemid) < 1:
            return False
        ap = db.pr_approval.getnode (itemid)
        pr = ap.purchase_request
        if own_pr (db, userid, pr):
            return True
        if linked_pr (db, userid, pr):
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

    def approval_undecided (db, userid, itemid):
        """ User is allowed to change status of undecided approval if
            they are the owner/deputy or have appropriate role.
            In addition this is allowed if they have a delegated
            approval or are an active substitute.
            We also allow pr.status to be 'rejected': This cannot change
            the outcome (once approved or rejected the pr.status cannot
            change) but allows for race condition when someone has
            several approvals in a single mask and one of that approvals
            changed the PR to rejected before the others were processed.
        """
        if not itemid or int (itemid) < 1:
            return False
        ap           = db.pr_approval.getnode (itemid)
        pr           = db.purchase_request.getnode (ap.purchase_request)
        und          = db.pr_approval_status.lookup ('undecided')
        st_open      = db.pr_status.lookup ('open')
        st_approving = db.pr_status.lookup ('approving')
        st_reject    = db.pr_status.lookup ('rejected')
        if  (   ap.status == und
            and (  userid in common.approval_by (db, ap.user)
                or userid in common.approval_by (db, ap.deputy)
                or (ap.role_id and prlib.has_pr_role (db, userid, ap.role_id))
                )
            and pr.status in (st_open, st_approving, st_reject)
            ):
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

    def get_pr_from_offer_item (db, itemid):
        prs = db.purchase_request.filter (None, dict (offer_items = itemid))
        if len (prs) == 0:
            return None
        assert len (prs) == 1
        return db.purchase_request.getnode (prs [0])
    # end def get_pr_from_offer_item

    def linked_from_pr (db, userid, itemid):
        """ Users are allowed to view if offer is linked from PR.
        """
        if not itemid or int (itemid) < 1:
            return True
        off = db.pr_offer_item.getnode (itemid)
        pr  = get_pr_from_offer_item (db, itemid)
        if pr is None:
            return False
        if own_pr (db, userid, pr.id):
            return True
        if linked_pr (db, userid, pr.id):
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

    def add_to_las_false (db, userid, itemid):
        """ Allow setting add_to_las from 'None' for orphanes offer items.
        """
        if itemid is None:
            return False
        oi = db.pr_offer_item.getnode (itemid)
        pr = get_pr_from_offer_item (db, itemid)
        if pr is not None:
            return False
        if oi.add_to_las is None:
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

    def linked_and_editable (db, userid, itemid):
        """ Users are allowed to edit if offer is linked from PR and PR
            is editable.
        """
        if not itemid or int (itemid) < 1:
            return True
        if not linked_from_pr (db, userid, itemid):
            return False
        pr  = get_pr_from_offer_item (db, itemid)
        if pr is None:
            return False
        return own_pr_and_open_or_rej (db, userid, pr.id)
    # end def linked_and_editable

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'pr_offer_item'
        , check = linked_and_editable
        , description = fixdoc (linked_and_editable.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    def after_approval (db, userid, itemid):
        """ User with view role is allowed editing if status
            is not one of the in-progress stati
        """
        if not pr_pt_role (db, userid, itemid):
            return False
        pr = db.purchase_request.getnode (itemid)
        unwanted = ('open', 'approving', 'rejected', 'cancelled')
        stati = []
        for st in db.pr_status.getnodeids (retired = False):
            status = db.pr_status.getnode (st)
            if status.name in unwanted:
                continue
            stati.append (st)
        if pr.status in stati:
            return True
        return False
    # end def after_approval

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'purchase_request'
        , check       = after_approval
        , description = fixdoc (after_approval.__doc__)
        , properties  = ('status', 'messages', 'files', 'nosy')
        )
    db.security.addPermissionToRole ('User', p)

    schemadef.register_nosy_classes (db, ['purchase_request'])

    def user_on_nosy (db, userid, itemid):
        """ User is allowed if on the nosy list
        """
        pr = db.purchase_request.getnode (itemid)
        if userid in pr.nosy:
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

    def user_on_nosy_approval (db, userid, itemid):
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

    def user_on_nosy_offer (db, userid, itemid):
        """ User is allowed if on the nosy list of the PR
        """
        if not itemid or int (itemid) < 1:
            return True
        prs = db.purchase_request.filter (None, dict (offer_items = itemid))
        assert len (prs) <= 1
        if prs:
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

    def view_pr_risks (db, userid, itemid):
        """ User is allowed to view special risks
            if the PR has appropriate status
            and the user is creator or owner of the PR or has one of the
            view roles.
        """
        st_open      = db.pr_status.lookup ('open')
        pr           = db.purchase_request.getnode (itemid)
        if pr.status == st_open:
            return False
        if own_pr (db, userid, itemid):
            return True
        if pr_pt_role (db, userid, itemid):
            return True
        return False
    # end def view_pr_risks

    p = db.security.addPermission \
        ( name = 'View'
        , klass = 'purchase_request'
        , check = view_pr_risks
        , description = fixdoc (view_pr_risks.__doc__)
        , properties = ('pr_risks',)
        )
    db.security.addPermissionToRole ('User', p)

    def edit_pr_risks (db, userid, itemid):
        """ User is allowed to edit special risks
            if the PR has appropriate status.
        """
        if not pr_pt_role (db, userid, itemid):
            return False
        st_open      = db.pr_status.lookup ('open')
        pr           = db.purchase_request.getnode (itemid)
        if pr.status == st_open:
            return False
        return True
    # end def edit_pr_risks

    p = db.security.addPermission \
        ( name = 'Edit'
        , klass = 'purchase_request'
        , check = edit_pr_risks
        , description = fixdoc (edit_pr_risks.__doc__)
        , properties = ('pr_risks',)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'user'
        , check       = schemadef.own_user_record
        , description = "Users are allowed to view some of their details"
        , properties  = ('supervisor', 'clearance_by', 'want_no_messages')
        )
    db.security.addPermissionToRole ('User', p)

    def until_ordered_and_purchasing (db, userid, itemid):
        st = until_ordered (db, userid, itemid)
        if not st:
            return False
        return pr_pt_role (db, userid, itemid)
    # end def until_ordered_and_purchasing

    def until_ordered_and_purchasing_oi (db, userid, itemid):
        pr  = get_pr_from_offer_item (db, itemid)
        if pr is None:
            return False
        return until_ordered_and_purchasing (db, userid, pr.id)
    # end def until_ordered_and_purchasing_oi

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'purchase_request'
        , check       = until_ordered_and_purchasing
        , description = "Allowed to edit until ordered"
        , properties  = ('gl_account',)
        )
    db.security.addPermissionToRole ('User', p)
    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'pr_offer_item'
        , check       = until_ordered_and_purchasing_oi
        , description = "Allowed to edit until ordered"
        , properties  = ('gl_account',)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'purchase_request'
        , check       = until_ordered
        , description = "Allowed to edit until ordered"
        , properties  = ('gl_account',)
        )
    db.security.addPermissionToRole ('Controlling', p)
    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'pr_offer_item'
        , check       = until_ordered_oi
        , description = "Allowed to edit until ordered"
        , properties  = ('gl_account',)
        )
    db.security.addPermissionToRole ('Controlling', p)

    tp_props = ('name', 'responsible', 'deputy', 'status', 'organisation')
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_project'
        , properties  = tp_props
        , check       = o_permission.time_project_allowed_by_org
        , description = fixdoc
            (o_permission.time_project_allowed_by_org.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    schemadef.add_search_permission (db, 'psp_element', 'User')
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'psp_element'
        , check       = o_permission.psp_element_allowed_by_org
        , description = fixdoc (o_permission.psp_element_allowed_by_org.__doc__)
        )
    db.security.addPermissionToRole ("User", p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'pr_supplier_risk'
        , check       = o_permission.supplier_risk_allowed_by_org
        , description = fixdoc \
            (o_permission.supplier_risk_allowed_by_org.__doc__)
        )
    db.security.addPermissionToRole ("User", p)
    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'pr_supplier_risk'
        , check       = o_permission.supplier_risk_allowed_by_org
        , description = fixdoc \
            (o_permission.supplier_risk_allowed_by_org.__doc__)
        )
    db.security.addPermissionToRole ("CISO", p)
    db.security.addPermissionToRole ('CISO', 'Create', 'pr_supplier_risk')

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'pr_supplier_rating'
        , check       = o_permission.supplier_rating_allowed_by_org
        , description = fixdoc \
            (o_permission.supplier_rating_allowed_by_org.__doc__)
        )
    db.security.addPermissionToRole ("User", p)
    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'pr_supplier_rating'
        , check       = o_permission.supplier_rating_allowed_by_org
        , description = fixdoc \
            (o_permission.supplier_rating_allowed_by_org.__doc__)
        )
    db.security.addPermissionToRole ("LAS", p)
    db.security.addPermissionToRole ('LAS', 'Create', 'pr_supplier_rating')

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'purchase_type'
        , check       = o_permission.purchase_type_allowed_by_org
        , description = fixdoc \
            (o_permission.purchase_type_allowed_by_org.__doc__)
        )
    db.security.addPermissionToRole ("User", p)

# end def security
