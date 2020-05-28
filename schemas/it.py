#! /usr/bin/python
# Copyright (C) 2004-16 Dr. Ralf Schlatterbeck Open Source Consulting.
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

from schemacfg import schemadef

# sub-schema definitins to include
# Note: order matters, core is always last.
schemas = \
    ( 'it_tracker'
    , 'msg_header'
    , 'user'
    , 'core'
    , 'ituser'
    )

importer = schemadef.Importer (globals (), schemas)

#
# SECURITY SETTINGS
#
# See the configuration and customisation document for information
# about security setup.
# Assign the access and edit Permissions for issue, file and message
# to regular users now

#     classname        allowed to view   /  edit
classes = \
    [ ("file"                , ["User"],  ["User"            ])
    , ("msg"                 , ["User"],  ["User"            ])
    ]

prop_perms = \
    [ ( "user", "View", ["User"]
      , ( "activity", "actor", "address", "alternate_addresses"
        , "creation", "creator", "id", "queries", "realname"
        , "status", "timezone", "username"
        )
      )
    , ( "user", "View", ["IT"]
      , ( "roles",
        )
      )
    , ( "user", "Edit", ["IT"]
      , ( "realname", "csv_delimiter", "roles"
        )
      )
    ]

importer.update_security ()
schemadef.register_class_permissions (db, classes, prop_perms)
schemadef.allow_user_details \
    (db, 'User', 'Edit', 'address', 'alternate_addresses')

# oh, g'wan, let anonymous access the web interface too
# NOT really !!!
db.security.addPermissionToRole('Anonymous', 'Web Access')

# allow search of users for IT
p = db.security.addPermission \
    ( name        = 'Search'
    , klass       = 'user'
    )
db.security.addPermissionToRole ('IT', p)
