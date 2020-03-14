#! /usr/bin/python
# Copyright (C) 2015 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    schema-pr
#
# Purpose
#    Specify the DB-Schema for a Purchase-Request tool
#--
#

import sys, os

sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
from schemacfg import schemadef

# sub-schema definitins to include
# Note: order matters, core is always last
# -- except for modules that extend the standard permission scheme in
# core (e.g. extuser)
schemas = \
    ( 'company'
    , 'time_project'
    , 'org_min'
    , 'sync_id'
    , 'user'
    , 'ldap'
    , 'pr'
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
    [ ("file",                 [],               [])
    , ("msg",                  [],               [])
    , ("query",                ["Controlling"],  ["Controlling"])
    , ("department",           [],               ["Procurement-Admin"])
    ]


prop_perms = []

# For PGP-Processing we need a role
schemadef.register_roles             (db, [('PGP', 'Roles that require PGP')])
schemadef.register_class_permissions (db, classes, prop_perms)
schemadef.allow_user_details         \
    ( db, 'User', 'View', 'address'
    , 'alternate_addresses', 'creation', 'activity'
    )
schemadef.allow_user_details         (db, 'User', 'Edit')

# oh, g'wan, let anonymous access the web interface too
# NOT really !!!
db.security.addPermissionToRole('Anonymous', 'Web Access')
