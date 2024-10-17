#! /usr/bin/python
# Copyright (C) 2004-19 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    schema-full
#
# Purpose
#    Specify the DB-Schema for a tracker including most parts,
#    time-tracking, it-issue tracking, ...
#    Link this file to schema.py
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
    ( 'nickname'
    , 'company'
    , 'org_min'
    , 'org_loc'
    , 'user'
    , 'external_users'
    , 'docissue'
    , 'keyword'
    , 'ext_tracker'
    , 'msg_header'
    , 'issue'
    , 'doc'
    , 'it_tracker'
    , 'min_adr'
    , 'contact'
    , 'user_contact'
    , 'person_cust'
    , 'support'
    , 'time_project'
    , 'time_tracker'
    , 'ldap'
    , 'contact_sec'
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
    [ ("file"                , [],               [])
    , ("msg"                 , [],               [])
    , ("query"               , ["Controlling"],  ["Controlling"])
    ]

prop_perms = \
    [ ( "user", "Edit", ["IT"]
      , ( "nickname", "pictures", "password", "roles", "timezone"
        , "timetracking_by", "username", "ad_domain"
        )
      )
    , ( "user", "View", ["User"]
      , ( "activity", "actor", "address", "alternate_addresses"
        , "clearance_by", "creation", "creator"
        , "firstname", "job_description", "lastname"
        , "id", "lunch_duration", "lunch_start", "nickname"
        , "pictures", "position_text", "queries", "realname", "room", "sex"
        , "status", "subst_active", "substitute", "supervisor", "timezone"
        , "title", "username", "tt_lines", "ad_domain", "business_responsible"
        )
      )
    ]

# For PGP-Processing we need a role
schemadef.register_roles             (db, [('PGP', 'Roles that require PGP')])
schemadef.register_class_permissions (db, classes, prop_perms)
schemadef.allow_user_details         (db, 'User', 'Edit')
# the following is further checked in an auditor:
db.security.addPermissionToRole ('User', 'Create', 'time_wp')

# editing of roles:
db.security.addPermissionToRole ('IT', 'Web Roles')

# oh, g'wan, let anonymous access the web interface too
# NOT really !!!
db.security.addPermissionToRole('Anonymous', 'Web Access')
