# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-13 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    support
#
# Purpose
#    Schema definitions for a customer support tracker
#
#--
#

from roundup.hyperdb import Class
from schemacfg       import schemadef

def init \
    ( db
    , Class
    , Person_Class
    , Full_Issue_Class
    , Superseder_Issue_Class
    , Boolean
    , String
    , Date
    , Link
    , Multilink
    , Number
    , ** kw
    ) :

    business_unit = Class \
        ( db
        , ''"business_unit"
        , name             = String    ()
        , valid            = Boolean   ()
        )
    business_unit.setkey ("name")

    customer = Person_Class \
        ( db
        , ''"customer"
        , name             = String    ()
        , is_valid         = Boolean   ()
        , nosy             = Multilink ("user")
        , nosygroups       = Multilink ("mailgroup")
        , maildomain       = String    ()
        , fromaddress      = String    ()
        , rmafrom          = String    ()
        , suppclaimfrom    = String    ()
        , confidential     = Boolean   ()
        , responsible      = Link      ("user")
        , business_unit    = Link      ("business_unit")
        , is_customer      = Boolean   ()
        , is_supplier      = Boolean   ()
        , customer_code    = String    ()
        )
    customer.setkey ("name")

    customer_agreement = Class \
        ( db
        , ''"customer_agreement"
        , customer         = Link      ("customer")
        , product          = Link      ("product", try_id_parsing='no')
        , description      = String    ()
        )
    customer_agreement.setlabelprop ("customer")
    customer_agreement.setorderprop ("description")

    mailgroup = Class \
        ( db
        , ''"mailgroup"
        , name             = String    ()
        , nosy             = Multilink ("user")
        , default_nosy     = Boolean   ()
        )
    mailgroup.setkey ("name")

    product = Class \
        ( db
        , ''"product"
        , name             = String    ()
        , description      = String    ()
        , product_family   = Link      ("prodcat")
        , product_use_case = Link      ("prodcat")
        , product_line     = Link      ("prodcat")
        , business_unit    = Link      ("business_unit")
        , sap_material     = String    ()
        , is_series        = Boolean   ()
        , valid            = Boolean   ()
        )
    product.setkey ("sap_material")

    sup_warranty = Class \
        ( db
        , ''"sup_warranty"
        , name             = String    ()
        , order            = Number    ()
        )

    sup_classification = Class \
        ( db
        , ''"sup_classification"
        , name             = String    ()
        , valid            = Boolean   ()
        , description      = String    ()
        , sup_warranty     = Link      ('sup_warranty')
        , examples         = String    ()
        )
    sup_classification.setkey ("name")

    sup_execution = Class \
        ( db
        , ''"sup_execution"
        , name             = String    ()
        , order            = Number    ()
        )
    sup_execution.setkey ("name")

    sup_prio = Class \
        ( db
        , ''"sup_prio"
        , name             = String    ()
        , order            = Number    ()
        )
    sup_prio.setkey ("name")

    sup_status = Class \
        ( db
        , ''"sup_status"
        , name             = String    ()
        , description      = String    ()
        , transitions      = Multilink ("sup_status")
        , order            = Number    ()
	, relaxed          = Boolean   ()
        )
    sup_status.setkey ("name")

    sup_type = Class \
        ( db
        , ''"sup_type"
        , name             = String    ()
        , order            = Number    ()
        )
    sup_type.setkey ("name")

    analysis_result = Class \
        ( db
        , ''"analysis_result"
        , name             = String    ()
        , description      = String    ()
        )
    analysis_result.setkey ("name")

    return_type = Class \
        ( db
        , ''"return_type"
        , name             = String    ()
        , order            = Number    ()
        )
    return_type.setkey ("name")

    Superseder_Issue_Class \
        ( db
        , ''"support"
        , category         = Link      ("category",   do_journal='no')
        , closed           = Date      ()
        , satisfied        = Date      ()
        , first_reply      = Date      ()
        , set_first_reply  = Boolean   () # only used for setting above
        , analysis_start   = Date      ()
        , analysis_end     = Date      ()
        , goods_received   = Date      ()
        , goods_sent       = Date      ()
        , confidential     = Boolean   ()
        , numeric_effort   = Number    ()
        , prio             = Link      ("sup_prio",   do_journal='no')
        , release          = String    ()
        , status           = Link      ("sup_status", do_journal='no')
        , serial_number    = String    ()
        , related_issues   = Multilink ("issue")
        , related_support  = Multilink ("support")
        , customer         = Link      ("customer",   do_journal='no')
        , emails           = Multilink ("contact",    do_journal='no')
        , cc_emails        = Multilink ("contact",    do_journal='no')
        , send_to_customer = Boolean   ()
        , classification   = Link      ("sup_classification", do_journal='no')
        , cc               = String    ()
        , bcc              = String    ()
        , type             = Link      ("sup_type")
        , execution        = Link      ("sup_execution")
        , number_effected  = Number    ()
        , warranty         = Boolean   ()
        , lot              = String    ()
        , product          = Link      ("product", try_id_parsing='no')
        , prodcat          = Link      ("prodcat")
        , external_ref     = String    ()
        , sap_ref          = String    ()
        , analysis_result  = Link      ("analysis_result", do_journal='no')
        , return_type      = Link      ("return_type", do_journal='no')
        , business_unit    = Link      ("business_unit")
        )

# end def init

    #
    # SECURITY SETTINGS
    #
    # See the configuration and customisation document for information
    # about security setup.

def security (db, ** kw) :
    roles = [ ("SupportAdmin", "Customer support department") ]

    #     classname        allowed to view   /  edit
    classes = \
        [ ("sup_status",     ["User"],                 [])
        , ("sup_prio",       ["User"],                 [])
        , ("sup_type",       ["User"],                 [])
        , ("sup_warranty",   ["User"],                 [])
        , ("sup_execution",  ["User"],                 [])
        , ("business_unit",  ["User"],                 [])
        , ("product",        ["User"],                 [])
        , ("support",        ["SupportAdmin"],         ["SupportAdmin"])
        , ("customer",       ["User", "SupportAdmin"], ["SupportAdmin"])
        , ("contact",        ["User", "SupportAdmin"], ["SupportAdmin"])
        , ("mailgroup",      ["User", "SupportAdmin"], ["SupportAdmin"])
        , ("sup_classification",
                             ["User", "SupportAdmin"], ["SupportAdmin"])
        , ("customer_agreement",
                             ["User", "SupportAdmin"], ["SupportAdmin"])
        , ("analysis_result",
                             ["User", "SupportAdmin"], ["SupportAdmin"])
        , ("return_type",
                             ["User", "SupportAdmin"], ["SupportAdmin"])
        ]
    if 'adr_type' in db.classes :
        classes.append (( "adr_type"
                        , ["User", "SupportAdmin"]
                        , ["SupportAdmin"]
                       ))
        classes.append (( "adr_type_cat"
                        , ["User", "SupportAdmin"]
                        , ["SupportAdmin"]
                       ))

    prop_perms = []

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

    db.security.addPermissionToRole ('User',         'Create', 'support')
    db.security.addPermissionToRole ('SupportAdmin', 'Create', 'support')
    schemadef.register_confidentiality_check \
        (db, 'User', 'support',   ('View',))
    exc_props = dict.fromkeys (('first_reply', 'satisfied'))
    props = dict (db.support.properties)
    for p in exc_props :
        del props [p]
    schemadef.register_confidentiality_check \
        (db, 'User', 'support',   ('Edit',), * props.keys ())
    schemadef.register_nosy_classes (db, ['support'])
    schemadef.add_search_permission (db, 'support', 'User')
# end def security
