#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    abo
#
# Purpose
#    Schema definitions for abo

from roundup.hyperdb import Class
import schemadef

def init \
    ( db
    , Class
    , Address_Class
    , Invoice_Class
    , Letter_Class
    , String
    , Date
    , Link
    , Multilink
    , Boolean
    , Number
    , ** kw
    ) :

    abo = Class \
        ( db, ''"abo"
        , begin               = Date      (offset = 0)
        , end                 = Date      (offset = 0)
        , aboprice            = Link      ('abo_price')
        , payer               = Link      ('address')
        , subscriber          = Link      ('address')
        , amount              = Number    ()
        , messages            = Multilink ("msg")
        , invoices            = Multilink ("invoice")
        )
    abo.setlabelprop (''"aboprice")

    abo_price = Class \
        ( db, ''"abo_price"
        , abotype             = Link      ('abo_type')
        , currency            = Link      ('currency')
        , amount              = Number    ()
        , name                = String    ()
        , invoice_template    = Multilink ('invoice_template')
        , invoice_group       = Link      ('invoice_group')
        , valid               = Boolean   ()
        )
    abo_price.setkey (''"name")

    abo_type = Class \
        ( db, ''"abo_type"
        , name                = String    ()
        , description         = String    ()
        , period              = Number    () # subscription period in months
        , order               = Number    ()
        , adr_type            = Link      ('adr_type')
        )
    abo_type.setkey (''"name")

    Address_Class \
        ( db, ''"address"
        , abos                = Multilink ("abo")
        , payed_abos          = Multilink ("abo")
        , invoices            = Multilink ("invoice")
        )

    Invoice_Class \
        ( db, ''"invoice"
        , period_start        = Date      (offset = 0)
        , period_end          = Date      (offset = 0)
        , payer               = Link      ("address")
        , subscriber          = Link      ("address")
        , abo                 = Link      ("abo")
        , invoice_group       = Link      ("invoice_group", do_journal='no')
        )

    invoice_group = Class \
        ( db, ''"invoice_group"
        , name                = String    ()
        , description         = String    ()
        )
    invoice_group.setkey (''"name")

    # Add invoice link -- this is optional, not every letter is related
    # to an invoice.
    Letter_Class \
        ( db, ''"letter"
        , invoice             = Link      ("invoice")
        )

# end def init

def security (db, ** kw) :
    roles = \
        [ ("Abo"           , "Allowed to modify subscriptions")
        , ("Invoice"       , "Allowed to change financial data")
        , ("Letter"        , "Allowed to add/change templates and letters")
        , ("Product"       , "Allowed to create/edit products")
        , ("Type"          , "Allowed to add/change type codes")
        ]

    classes = \
        [ ("abo_price"         , ["User"],    ["Product"])
        , ("abo_type"          , ["Abo", "Product", "Invoice"],
                                              ["Product", "Abo", "Invoice"])
        , ("abo"               , ["Abo", "Product", "Invoice"],
                                              ["Abo"])
        , ("address"           , ["User"],    ["User"])
        , ("adr_type"          , ["User"],    ["Type"])
        , ("adr_type_cat"      , ["User"],    ["Type"])
        , ("contact"           , ["User"],    ["Contact"])
        , ("contact_type"      , ["User"],    [])
        , ("currency"          , ["User"],    ["Product"])
        , ("invoice_group"     , ["Invoice"], ["Invoice"])
        , ("invoice_template"  , ["Invoice"], ["Invoice"])
        , ("invoice"           , ["Invoice"], ["Invoice"])
        , ("letter"            , ["User"],    ["Abo", "Letter"])
        , ("query"             , ["User"],    ["User"])
        , ("tmplate"           , ["User"],    ["Abo", "Invoice", "Letter"])
        , ("valid"             , ["User"],    [])
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, [])
# end def security
