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
    , String
    , Date
    , Link
    , Multilink
    , Boolean
    , Number
    , Min_Issue_Class
    , Nosy_Issue_Class
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

    cust_supp = Nosy_Issue_Class \
        ( db, ''"cust_supp"
        , name                  = String    ()
        , lookalike_name        = String    ()
        , description           = String    ()
        , tax_id                = String    ()
        , pharma_ref            = Link      ("pharma_ref")
        , bank_account          = Multilink ("bank_account")
        , currency              = Link      ("currency")
        , invoice_dispatch      = Link      ("invoice_dispatch")
        , dispatch_type         = Link      ("dispatch_type")
        # customer-specific:
        , customer_status       = Link      ("customer_status")
        , customer_group        = Link      ("customer_group")
        , customer_type         = Multilink ("customer_type")
        , attendant             = Link      ("user")
        , credit_limit          = Number    ()
        , discount_group        = Link      ("discount_group")
        , invoice_text          = String    ()
        , sales_conditions      = Link      ("sales_conditions")
        # supplier-specific:
        , supplier_status       = Link      ("supplier_status")
        , supplier_group        = Link      ("supplier_group")
        , order_text            = String    ()
        )
    cust_supp.setkey (''"name")

    customer_type = Class \
        ( db, ''"customer_type"
        , code                = String    ()
        , description         = String    ()
        )
    customer_type.setkey ("code")

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
        , valid                 = Boolean   ()
        , display               = Boolean   ()
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

    measuring_unit = Class \
        ( db, ''"measuring_unit"
        , name                  = String    ()
        , description           = String    ()
        )
    measuring_unit.setkey ("name")

    overall_discount = Class \
        ( db, ''"overall_discount"
        , price                 = Number    ()
        , discount              = Number    ()
        )

    packaging_unit = Class \
        ( db, ''"packaging_unit"
        , name                  = String    ()
        , description           = String    ()
        )
    packaging_unit.setkey ("name")

    # Pharmareferenzbezirk
    pharma_ref = Class \
        ( db, ''"pharma_ref"
        , name                  = String    ()
        , description           = String    ()
        )
    pharma_ref.setkey ("name")

    proceeds_group = Class \
        ( db, ''"proceeds_group"
        , name                  = String    ()
        , description           = String    ()
        )
    proceeds_group.setkey ("name")

    product = Min_Issue_Class \
        ( db, ''"product"
        , name                  = String    ()
        , description           = String    ()
        , status                = Link      ("product_status")
        , product_group         = Link      ("product_group")
        , measuring_unit        = Link      ("measuring_unit")
        , packaging_unit        = Link      ("packaging_unit")
        , minimum_inventory     = Number    ()
        , shelf_life_code       = Link      ("shelf_life_code")
        , proceeds_group        = Link      ("proceeds_group")
        , use_lot               = Boolean   ()
        , product_price         = Multilink ("product_price")
        )
    product.setkey ("name")

    product_group = Class \
        ( db, ''"product_group"
        , name                  = String    ()
        , description           = String    ()
        )
    product_group.setkey ("name")

    product_price = Class \
        ( db, ''"product_price"
        , price                 = Number    ()
        , vat_percent           = Number    ()
        , currency              = Link      ("currency")
        )

    product_status = Class \
        ( db, ''"product_status"
        , name                  = String    ()
        , description           = String    ()
        , order                 = Number    ()
        , valid                 = Boolean   ()
        )
    product_status.setkey ("name")

    sales_conditions = Class \
        ( db, ''"sales_conditions"
        , name                  = String    ()
        , description           = String    ()
        , discount_percent      = Number    ()
        , discount_days         = Number    ()
        , payment_days          = Number    ()
        )

    shelf_life_code = Class \
        ( db, ''"shelf_life_code"
        , name                  = String    ()
        , description           = String    ()
        , shelf_life            = Number    ()
        )
    shelf_life_code.setkey ("name")

    storage = Class \
        ( db, ''"storage"
        , name                  = String    ()
        , description           = String    ()
        , storage_locations     = Multilink ("storage_location")
        )
    storage.setkey ("name")

    storage_location = Class \
        ( db, ''"stock"
        , name                  = String    ()
        , description           = String    ()
        , storage               = Link      ("storage")
        )

    stocked_product = Class \
        ( db, ''"stocked_product"
        , product               = Link      ("product")
        , storage_location      = Link      ("storage_location")
        , on_stock              = Number    ()
        , lot                   = String    ()
        # Wareneingang
        # Verfall
        # Quarantänestatus
        )

    supplier_group = Class \
        ( db, ''"supplier_group"
        , name                  = String    ()
        , description           = String    ()
        )
    supplier_group.setkey ("name")

    supplier_status = Class \
        ( db, ''"supplier_status"
        , name                  = String    ()
        , description           = String    ()
        , order                 = Number    ()
        , valid                 = Boolean   ()
        , display               = Boolean   ()
        )
    supplier_status.setkey ("name")

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
        [ ("Discount"      , "Allowed to add/change discounts")
        , ("Letter"        , "Allowed to add/change templates and letters")
        , ("Product"       , "Allowed to add/change product data")
        ]

    classes = \
        [ ("address",          ["User"],    ["Contact"])
        , ("bank_account",     ["User"],    ["Contact"])
        , ("cust_supp",        ["User"],    ["Contact"])
        , ("customer_group",   ["User"],    [])
        , ("customer_status",  ["User"],    [])
        , ("discount_group",   ["User"],    ["Discount"])
        , ("dispatch_type",    ["User"],    [])
        , ("group_discount",   ["User"],    ["Discount"])
        , ("invoice_dispatch", ["User"],    [])
        , ("letter",           ["User"],    ["Letter"])
        , ("measuring_unit",   ["User"],    [])
        , ("overall_discount", ["User"],    ["Discount"])
        , ("packaging_unit",   ["User"],    [])
        , ("pharma_ref",       ["User"],    [])
        , ("proceeds_group",   ["User"],    [])
        , ("product",          ["User"],    ["Product"])
        , ("product_group",    ["User"],    ["Product"])
        , ("product_status",   ["User"],    [])
        , ("sales_conditions", ["User"],    [])
        , ("shelf_life_code",  ["User"],    [])
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, [])
# end def security
