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

def init (db, Class, String, Date, Link, Multilink, Boolean, Number, ** kw) :

    do_index = "yes"
    do_index = "no"

    abo = Class \
        ( db, ''"abo"
        , begin               = Date      ()
        , end                 = Date      ()
        , aboprice            = Link      ('abo_price')
        , payer               = Link      ('address')
        , subscriber          = Link      ('address')
        , amount              = Number    ()
        , messages            = Multilink ("msg")
        , invoices            = Multilink ("invoice")
        )

    abo_price = Class \
        ( db, ''"abo_price"
        , abotype             = Link      ('abo_type')
        , currency            = Link      ('currency')
        , amount              = Number    ()
        , name                = String    ()
        , invoice_group       = Link      ('invoice_group')
        )
    abo_price.setkey (''"name")

    abo_type = Class \
        ( db, ''"abo_type"
        , name                = String    ()
        , description         = String    ()
        , period              = Number    () # subscription period in months
        , order               = Number    ()
        , invoice_template    = Multilink ('invoice_template')
        , adr_type            = Link      ('adr_type')
        )
    abo_type.setkey (''"name")

    address = Class \
        ( db, ''"address"
        , title               = String    ()
        , lettertitle         = String    ()
        , firstname           = String    (indexme = do_index)
        , initial             = String    ()
        , lastname            = String    (indexme = do_index)
        , function            = String    (indexme = do_index)
        , street              = String    (indexme = do_index)
        , country             = String    ()
        , postalcode          = String    ()
        , city                = String    (indexme = do_index)
        , phone               = String    ()
        , fax                 = String    ()
        , salutation          = String    ()
        , messages            = Multilink ("msg")
        , email               = String    (indexme = do_index)
        , abos                = Multilink ("abo")
        , payed_abos          = Multilink ("abo")
        , adr_type            = Multilink ("adr_type")
        , valid               = Link      ("valid")
        , letters             = Multilink ("letter")
        , invoices            = Multilink ("invoice")
        )
    address.setlabelprop ('lastname')

    adr_type = Class \
        ( db, ''"adr_type"
        , code                = String    ()
        , description         = String    ()
        , typecat             = Link      ("adr_type_cat")
        )
    adr_type.setkey ("code")

    adr_type_cat = Class \
        ( db, ''"adr_type_cat"
        , code                = String    ()
        , description         = String    ()
        )
    adr_type_cat.setkey (''"code")

    currency = Class \
        ( db, ''"currency"
        , name                = String    ()
        , description         = String    ()
        )
    currency.setkey (''"name")

    invoice = Class \
        ( db, ''"invoice"
        , invoice_no          = String    ()
        , period_start        = Date      ()
        , period_end          = Date      ()
        , amount              = Number    ()
        , currency            = Link      ("currency")
        , balance_open        = Number    ()
        , open                = Boolean   ()
        , n_sent              = Number    ()
        , last_sent           = Date      ()
        , payer               = Link      ("address")
        , subscriber          = Link      ("address")
        , abo                 = Link      ("abo")
        , date_payed          = Date      ()
        , bookentry           = Date      ()
        , receipt_no          = String    ()
        , send_it             = Boolean   ()
        , payment             = Number    ()
        , invoice_group       = Link      ("invoice_group", do_journal='no')
        , letters             = Multilink ("letter")
        )
    invoice.setkey (''"invoice_no")

    invoice_group = Class \
        ( db, ''"invoice_group"
        , name                = String    ()
        , description         = String    ()
        )
    invoice_group.setkey (''"name")

    # The invoice_level number decides for which invoice level we use
    # which template.
    invoice_template = Class \
        ( db, ''"invoice_template"
        , tmplate             = Link      ("tmplate")
        , invoice_level       = Number    ()
        , interval            = Number    ()
        , name                = String    ()
        )
    invoice_template.setkey (''"name")

    # The file types are either PDF (from old imported data) or an
    # OpenOffice.org document which is cusomized using info pointed to with
    # invoice and/or address. The invoice link is optional -- not every
    # letter is related to an invoice.
    letter = Class \
        ( db, ''"letter"
        , subject             = String    ()
        , address             = Link      ("address")
        , date                = Date      ()
        , files               = Multilink ("file", do_journal='no')
        , messages            = Multilink ("msg")
        , invoice             = Link      ("invoice")
        )

    tmplate = Class \
        ( db, ''"tmplate"
        , name                = String    ()
        # version control, use latest:
        , files               = Multilink ("file", do_journal='no')
        )
    tmplate.setkey (''"name")

    # Define codes for (in)valid addresses, e.g., "verstorben"
    valid = Class \
        ( db, ''"valid"
        , name                = String    ()
        , description         = String    ()
        )
    valid.setkey (''"name")

# end def init


def security (db, ** kw) :
    roles = \
        [ ("Abo"           , "Allowed to modify subscriptions")
        , ("Invoice"       , "Allowed to change financial data")
        , ("Product"       , "Allowed to create/edit products")
        , ("Type"          , "Allowed to add/change type codes")
        ]

    classes = \
        [ ("abo_price"         , ["User"],    ["Product"                  ])
        , ("abo_type"          , ["User"],    ["Product", "Abo", "Invoice"])
        , ("abo"               , ["User"],    ["Abo"                      ])
        , ("address"           , ["User"],    ["User"                     ])
        , ("adr_type"          , ["User"],    ["Type"                     ])
        , ("adr_type_cat"      , ["User"],    ["Type"                     ])
        , ("currency"          , ["User"],    ["Product"                  ])
        , ("file"              , ["User"],    ["User"                     ])
        , ("invoice_group"     , ["User"],    ["Invoice"                  ])
        , ("invoice_template"  , ["User"],    ["Invoice"                  ])
        , ("invoice"           , ["Invoice"], ["Invoice"                  ])
        , ("letter"            , ["User"],    ["Abo"                      ])
        , ("msg"               , ["User"],    ["User"                     ])
        , ("query"             , ["User"],    ["User"                     ])
        , ("tmplate"           , ["User"],    ["Abo", "Invoice"           ])
        , ("valid"             , ["User"],    ["Admin"                    ])
        ]
    prop_perms = [("user", "View", ["Anonymous"] , ("username",))]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)
# end def security
