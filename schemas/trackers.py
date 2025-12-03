#! /usr/bin/python
# Copyright (C) 2004-25 Dr. Ralf Schlatterbeck Open Source Consulting.
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
from schemacfg import schemadef

# sub-schema definitins to include
# Note: order matters, core is always last
# -- except for modules that extend the standard permission scheme in
# core (e.g. extuser, rouser)
schemas = \
    ( 'user'
    , 'nickname'
    , 'external_users'
    , 'docissue'
    , 'keyword'
    , 'kpm'
    , 'ext_tracker'
    , 'msg_header'
    , 'issue'
    , 'contact'
    , 'person_cust'
    , 'support'
    , 'ldap'
    , 'core'
    , 'extuser'
    , 'rouser'
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
        , "status", "timezone", "title", "username", "ad_domain"
        )
      )
    ]
roles = \
    [ ('PGP',       'Roles that require PGP')
    , ('Sub-Login', 'Allow to login as another user')
    ]

schemadef.register_roles             (db, roles)
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

# Let anonymous users access the web interface. Note that almost all
# trackers will need this Permission. The only situation where it's not
# required is in a tracker that uses an HTTP Basic Authenticated front-end.
db.security.addPermissionToRole('Anonymous', 'Web Access')
