#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#
#++
# Name
#    schema-it
#
# Purpose
#    Specify the DB-Schema for a simple IT issue tracker.
#    Link this file to schema.py
#--
#

import sys, os

sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
sys.path.insert (0, os.path.join (db.config.HOME, 'schema'))
from common import clearance_by
import schemadef

# sub-schema definitins to include
# Note: order matters, core is always last.
schemas = \
    ( 'address'
    , 'adr_ext'
    , 'adr_ptr'
    , 'core'
    )

importer = schemadef.Importer (globals (), schemas)

del sys.path [0:1]

Letter_Class  (db, ''"letter")
Address_Class (db, ''"address")

importer.update_security ()

# SECURITY SETTINGS
#
# See the configuration and customisation document for information
# about security setup.
# Assign the access and edit Permissions for issue, file and message
# to regular users now

#     classname        allowed to view   /  edit
classes = \
    [ ("file",               ["User"],    ["User"])
    , ("msg",                ["User"],    ["User"])
    , ("address",            ["Contact"], ["Contact"])
    ]

prop_perms = \
    [ ( "user", "Edit", []
      , ( "address"
        , "alternate_addresses"
        , "nickname"
        , "password"
        , "timezone"
        , "username"
        )
      )
    , ( "user", "Edit", []
      , ( "clearance_by", "external_phone", "firstname"
        , "job_description", "lastname", "lunch_duration", "lunch_start"
        , "phone", "pictures", "position", "private_phone", "realname"
        , "room", "sex", "status", "subst_active", "substitute", "supervisor"
        , "title", "roles"
        )
      )
    , ( "user", "View", ["User"]
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
    ]

schemadef.register_class_permissions (db, classes, prop_perms)
p = db.security.addPermission \
    ( name        = 'Edit'
    , klass       = 'user'
    , check       = schemadef.own_user_record
    , description = \
        "User is allowed to edit (some of) their own user details"
    , properties  = ('password', 'phone')
    )
db.security.addPermissionToRole('User', p)

# oh, g'wan, let anonymous access the web interface too
# NOT really !!!
db.security.addPermissionToRole('Anonymous', 'Web Access')

