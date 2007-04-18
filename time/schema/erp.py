#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
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
#++
# Name
#    erp
#
# Purpose
#    Schema definitions for ERP

from roundup.hyperdb import Class
import schemadef

def init \
    ( db
    , Class
    , Ext_Class
    , String
    , Date
    , Link
    , Multilink
    , Boolean
    , Number
    , IssueClass
    , Address_Class
    , Letter_Class
    , ** kw
    ) :

    do_index = "no"
    export   = {}

    bank_account = Class \
        ( db, ''"bank_account"
        , bank                  = String    ()
        , description           = String    ()
        , act_number            = String    ()
        , bank_code             = String    ()
        , iban                  = String    ()
        , bic                   = String    ()
        )

    customer = IssueClass \
        ( db, ''"customer"
        , name                  = String    ()
        , description           = String    ()
        , shipping_address      = Link      ("address")
        , invoice_address       = Link      ("address")
        , contact_person        = Multilink ("contact_person")
        , tax_id                = String    ()
        , status                = Link      ("customer_status")
        , customer_group        = Link      ("customer_group")
        , attendant             = Link      ("user")
        , credit_limit          = Number    ()
        , credit_limit_cur      = Link      ("currency")
        , discount_group        = Link      ("discount_group")
        , invoice_dispatch      = Link      ("invoice_dispatch")
        , dispatch_type         = Link      ("dispatch_type")
        , pharma_ref            = Link      ("pharma_ref")
        , invoice_text          = String    ()
        , bank_account          = Multilink ("bank_account")
        , sales_conditions      = Link      ("sales_conditions")
        , messages              = Multilink ("msg")
        )
    customer.setkey (''"name")

    customer_group = Class \
        ( db, ''"customer_group"
        , name                  = String    ()
        , description           = String    ()
        , discount_group        = Link      ("discount_group")
        )
    customer_group.setkey ("name")

    customer_status = Class \
        ( db, ''"customer_status"
        , name                  = String    ()
        , description           = String    ()
        , order                 = Number    ()
        )
    customer_status.setkey ("name")

    discount_group = Class \
        ( db, ''"discount_group"
        , name                  = String    ()
        , description           = String    ()
        , currency              = Link      ("currency")
        , group_discount        = Multilink ("group_discount")
        , overall_discount      = Multilink ("overall_discount")
        )
    discount_group.setkey ("name")

    dispatch_type = Class \
        ( db, ''"dispatch_type"
        , name                  = String    ()
        , description           = String    ()
        )
    dispatch_type.setkey ("name")

    group_discount = Class \
        ( db, ''"group_discount"
        , product_group         = Link      ("product_group")
        , discount              = Number    ()
        )

    invoice_dispatch = Class \
        ( db, ''"invoice_dispatch"
        , name                  = String    ()
        , description           = String    ()
        )
    invoice_dispatch.setkey ("name")

    overall_discount = Class \
        ( db, ''"overall_discount"
        , price                 = Number    ()
        , discount              = Number    ()
        )

    # Pharmareferenzbezirk
    pharma_ref = Class \
        ( db, ''"pharma_ref"
        , name                  = String    ()
        , description           = String    ()
        )
    pharma_ref.setkey ("name")

    product_group = Class \
        ( db, ''"product_group"
        , name                  = String    ()
        , description           = String    ()
        )
    product_group.setkey ("name")

    sales_conditions = Class \
        ( db, ''"sales_conditions"
        , name                  = String    ()
        , description           = String    ()
        , discount_percent      = Number    ()
        , discount_days         = Number    ()
        , payment_days          = Number    ()
        )
    sales_conditions.setkey ("name")

    Address_Class \
        ( db, ''"address"
        )

    Letter_Class \
        ( db, ''"letter"
        )

    return export
# end def init


def security (db, ** kw) :
    roles = \
        [ ("Contact"       , "Allowed to add/change customer contact data")
        , ("Discount"      , "Allowed to add/change discounts")
        , ("Letter"        , "Allowed to add/change templates and letters")
        , ("Product"       , "Allowed to add/change product data")
        ]

    classes = \
        [ ("address"           , ["User"],    ["Contact"])
        , ("bank_account"      , ["User"],    ["Contact"])
        , ("customer"          , ["User"],    ["Contact"])
        , ("customer_group"    , ["User"],    ["Admin"])
        , ("customer_status"   , ["User"],    ["Admin"])
        , ("dispatch_type"     , ["User"],    ["Admin"])
        , ("group_discount"    , ["User"],    ["Discount"])
        , ("invoice_dispatch"  , ["User"],    ["Admin"])
        , ("letter"            , ["User"],    ["Letter"])
        , ("pharma_ref"        , ["User"],    ["Admin"])
        , ("product_group"     , ["User"],    ["Product"])
        , ("sales_conditions"  , ["User"],    ["Admin"])
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, [])
# end def security
