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
#    adr_perm
#
# Purpose
#    Permissions for addresses common for some projects

import schemadef

def init (db, Address_Class, Link, ** kw) :
    pass
# end def init

def security (db, ** kw) :
    classes = \
        [ ("file",          ["User", "Adr_Readonly"],            ["User"])
        , ("msg",           ["User", "Adr_Readonly"],            ["User"])
        , ("address",       ["Contact", "Adr_Readonly", "User"], ["User"])
        , ("contact",       ["Contact", "Adr_Readonly", "User"], ["Contact"])
        , ("weekday",       ["Contact", "Adr_Readonly", "User"], [])
        , ("opening_hours", ["Contact", "Adr_Readonly", "User"], ["User"])
        ]

    prop_perms = \
        [ ( "user", "View", ["User"]
          , ( "activity", "actor", "address", "alternate_addresses"
            , "clearance_by", "creation", "creator", "department"
            , "external_phone", "firstname", "job_description", "lastname"
            , "lunch_duration", "lunch_start", "nickname", "password", "phone"
            , "pictures", "position", "queries", "realname", "room", "sex"
            , "status", "subst_active", "substitute", "supervisor", "timezone"
            , "title", "username", "home_directory", "login_shell"
            , "samba_home_drive", "samba_home_path"
            )
          )
        , ( "user", "View", ["Adr_Readonly"]
          , ( "username", "realname", "phone")
          )
        ]

    schemadef.register_class_permissions (db, classes, prop_perms)
    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'user'
        , check       = schemadef.own_user_record
        , description = \
            "User is allowed to edit (some of) their own user details"
        , properties  = ('password', 'phone', 'csv_delimiter'
                        , 'timezone', 'address', 'alternate_addresses'
                        )
        )
    db.security.addPermissionToRole ('User', p)
    db.security.addPermissionToRole ('Adr_Readonly', p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'user'
        , check       = schemadef.own_user_record
        , description = \
            "User is allowed to view (some of) their own user details"
        , properties  = ('username', 'realname')
        )
    db.security.addPermissionToRole ('User', p)
    db.security.addPermissionToRole ('Adr_Readonly', p)
# end def security
