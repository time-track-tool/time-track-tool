#! /usr/bin/python
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
# Note: order matters, core is always last.
schemas = \
    ( 'nickname'
    , 'company'
    , 'org_min'
    , 'org_loc'
    , 'docissue'
    , 'keyword'
    , 'ext_tracker'
    , 'msg_header'
    , 'issue'
    , 'doc'
    , 'it_tracker'
    , 'address'
    , 'contact'
    , 'person_cust'
    , 'person'
    , 'support'
    , 'time_project'
    , 'time_tracker'
    , 'contact_sec'
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
    [ ("file"                , [],               [])
    , ("msg"                 , [],               [])
    , ("query"               , ["Controlling"],  ["Controlling"])
    ]

prop_perms = \
    [ ( "user", "Edit", ["HR", "IT"]
      , ( "address"
        , "alternate_addresses"
        , "nickname"
        , "password"
        , "timezone"
        , "username"
        )
      )
    , ( "user", "Edit", ["HR"]
      , ( "clearance_by", "firstname"
        , "job_description", "lastname", "lunch_duration", "lunch_start"
        , "pictures", "position_text", "realname"
        , "room", "sex", "status", "subst_active", "substitute", "supervisor"
        , "title", "roles", "tt_lines"
        )
      )
    , ( "user", "Edit", ["Office"]
      , ( "title", "room", "position_text"
        )
      )
    , ( "user", "View", ["User"]
      , ( "activity", "actor", "address", "alternate_addresses"
        , "clearance_by", "creation", "creator"
        , "firstname", "job_description", "lastname"
        , "id", "lunch_duration", "lunch_start", "nickname"
        , "pictures", "position_text", "queries", "realname", "room", "sex"
        , "status", "subst_active", "substitute", "supervisor", "timezone"
        , "title", "username", "tt_lines", "business_responsible"
        )
      )
    ]

schemadef.register_class_permissions (db, classes, prop_perms)
schemadef.allow_user_details         (db, 'User', 'Edit')
# the following is further checked in an auditor:
db.security.addPermissionToRole ('User', 'Create', 'time_wp')

# editing of roles:
db.security.addPermissionToRole ('IT', 'Web Roles')

# oh, g'wan, let anonymous access the web interface too
# NOT really !!!
db.security.addPermissionToRole('Anonymous', 'Web Access')
