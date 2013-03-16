#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2013 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    light
#
# Purpose
#    Specify a lightweight DB-Schema for a tracker
#    Link this file to schema.py
#--
#

import sys, os

sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
from schemacfg      import schemadef
from schemacfg.core import view_query

# sub-schema definitins to include
# Note: order matters, core is always last
# -- except for modules that extend the standard permission scheme in
# core (e.g. extuser)
schemas = \
    ( 'user'
    , 'keyword'
    , 'light'
    , 'core'
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
    [ ("file"                , [],  [])
    , ("msg"                 , [],  [])
    , ("query"               , [],  [])
    ]

prop_perms = \
    [ ( "user", "View", ["User"]
      , ( "firstname", "lastname", "id"
        , "pictures", "realname", "username", "status"
        )
      )
    ]

schemadef.register_class_permissions (db, classes, prop_perms)
schemadef.allow_user_details \
    (db, 'User', 'Edit', 'address', 'alternate_addresses', 'timezone')
schemadef.allow_user_details \
    (db, 'User', 'View', 'creator', 'creation', 'activity', 'actor')

db.security.addPermission \
    ( name='Register'
    , klass='user'
    , description='User is allowed to register new user'
    )
db.security.addPermissionToRole('Anonymous', 'Web Access')
db.security.addPermissionToRole('Anonymous', 'Register', 'user')
for cl in 'issue', 'file', 'msg', 'keyword', 'prio', 'status':
    db.security.addPermissionToRole('Anonymous', 'View', cl)
    db.security.addPermissionToRole('User', 'View', cl)
db.security.addPermissionToRole('User', 'Edit', 'issue')

# Allow anonymous to see public queries
p = db.security.getPermission   ('View', 'query', check = view_query)
db.security.addPermissionToRole ('Anonymous', p)
p = db.security.getPermission   ('Search', 'query')
db.security.addPermissionToRole ('Anonymous', p)

