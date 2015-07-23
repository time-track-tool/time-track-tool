#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-13 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    schema-trackers
#
# Purpose
#    Specify the DB-Schema for several trackers in one
#    Link this file to schema.py
#--
#

import sys, os

sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
from common    import clearance_by
from schemacfg import schemadef

# sub-schema definitins to include
# Note: order matters, core is always last
# -- except for modules that extend the standard permission scheme in
# core (e.g. extuser)
schemas = \
    ( 'user'
    , 'nickname'
    , 'external_users'
    , 'docissue'
    , 'keyword'
    , 'ext_tracker'
    , 'issue'
    , 'it_part_of'
    , 'it_tracker'
    , 'min_adr'
    , 'contact'
    , 'person_cust'
    , 'support'
    , 'ldap'
    , 'core'
    , 'extuser'
    )

importer = schemadef.Importer (globals (), schemas)
del sys.path [0:1]

#
# SECURITY SETTINGS
#
# See the configuration and customisation document for information
# about security setup.
# Assign the access and edit Permissions for issue, file and message
# to regular users now

importer.update_security ()

#     classname        allowed to view   /  edit
classes = \
    [ ("file",         [],               [])
    , ("msg",          [],               [])
    , ("query",        ["Issue_Admin"],  ["Issue_Admin"])
    , ("contact",      ["User"],         ["SupportAdmin"])
    , ("contact_type", ["User"],         ["SupportAdmin"])
    ]

prop_perms = \
    [ ( "user", "Edit", ["IT"]
      , ( "address", "alternate_addresses", "nickname", "password"
        , "timezone", "username"
        )
      )
    , ( "user", "View", ["IT"]
      , ( "roles"
        ,
        )
      )
    , ( "user", "Edit", ["IT"]
      , ( "firstname", "lastname", "realname", "status", "roles"
        )
      )
    , ( "user", "View", ["User"]
      , ( "activity", "actor", "address", "alternate_addresses", "creation"
        , "creator", "firstname", "lastname", "id", "nickname", "realname"
        , "status", "timezone", "title", "username"
        )
      )
    ]

# For PGP-Processing we need a role
schemadef.register_roles             (db, [('PGP', 'Roles that require PGP')])
schemadef.register_class_permissions (db, classes, prop_perms)
schemadef.allow_user_details         (db, 'User', 'Edit')

# editing of roles:
db.security.addPermissionToRole ('IT', 'Web Roles')

# allow search of users for normal users
p = db.security.addPermission \
    ( name        = 'Search'
    , klass       = 'user'
    , properties  = ('realname', )
    )
db.security.addPermissionToRole ('User', p)

# oh, g'wan, let anonymous access the web interface too
# NOT really !!!
db.security.addPermissionToRole('Anonymous', 'Web Access')
