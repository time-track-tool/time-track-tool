# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Dr. Ralf Schlatterbeck Open Source Consulting.
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

    sup_prio = Class \
        ( db
        , ''"sup_prio"
        , name             = String    ()
        , order            = Number    ()
        )
    sup_prio.setkey ("name")

    Superseder_Issue_Class \
        ( db
        , ''"support"
        , category         = Link      ("category",   do_journal='no')
        , closed           = Date      ()
        , confidential     = Boolean   ()
        , numeric_effort   = Number    ()
        , prio             = Link      ("sup_prio",   do_journal='no')
        , release          = String    ()
        , severity         = Link      ("severity",   do_journal='no')
        , status           = Link      ("sup_status", do_journal='no')
        , serial_number    = String    ()
        , related_issues   = Multilink ("issue")
        , customer         = Link      ("customer",   do_journal='no')
        )

    customer = Person_Class \
        ( db
        , ''"customer"
        , name             =  String   ()
        )
    customer.setkey ("name")

# end def init

    #
    # SECURITY SETTINGS
    #
    # See the configuration and customisation document for information
    # about security setup.
    # Assign the access and edit Permissions for issue, file and message
    # to regular users now

def security (db, ** kw) :
    roles = [ ("Support",    "Customer support department") ]

    #     classname        allowed to view   /  edit
    classes = \
        [ ("sup_status",     ["User"],            [])
        , ("sup_prio",       ["User"],            [])
        , ("support",        ["Support"],         ["Support"])
        , ("customer",       ["User", "Support"], ["Support"])
        , ("contact",        ["User", "Support"], ["Support"])
        , ("adr_type",       ["User", "Support"], ["Support"])
        , ("adr_type_cat",   ["User", "Support"], ["Support"])
        ]

    prop_perms = \
        [
#       , ( "user", "View", ["User"]
#         , ( "activity", "actor", "address", "alternate_addresses"
#           , "clearance_by", "creation", "creator", "department"
#           , "external_phone", "firstname", "job_description", "lastname"
#           , "lunch_duration", "lunch_start", "nickname", "password", "phone"
#           , "pictures", "position", "queries", "realname", "room", "sex"
#           , "status", "subst_active", "substitute", "supervisor", "timezone"
#           , "title", "username", "home_directory", "login_shell"
#           , "samba_home_drive", "samba_home_path"
#           )
#         )
        ]


    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

    db.security.addPermissionToRole ('User',    'Create', 'support')
    db.security.addPermissionToRole ('Support', 'Create', 'support')
    schemadef.register_confidentiality_check \
        (db, 'support',   ('View',))
    schemadef.register_confidentiality_check \
        (db, 'support',   ('Edit',))
    schemadef.register_nosy_classes (db, ['support'])
# end def security
