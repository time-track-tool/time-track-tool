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
from common    import clearance_by
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
        , "pictures", "position", "realname"
        , "room", "sex", "status", "subst_active", "substitute", "supervisor"
        , "title", "roles", "tt_lines"
        )
      )
    , ( "user", "Edit", ["Office"]
      , ( "title", "room", "position"
        )
      )
    , ( "user", "Edit", ["IT"]
      , ( "is_lotus_user", "sync_with_ldap", "group"
        , "secondary_groups", "uid", "home_directory", "login_shell"
        , "samba_home_drive", "samba_home_path", "samba_kickoff_time"
        , "samba_lm_password", "samba_logon_script", "samba_nt_password"
        , "samba_profile_path", "samba_pwd_can_change", "samba_pwd_last_set"
        , "samba_pwd_must_change", "user_password", "shadow_last_change"
        , "shadow_min", "shadow_max", "shadow_warning", "shadow_inactive"
        , "shadow_expire", "shadow_used"
        )
      )
    , ( "user", "View", ["Controlling"], ("roles",))
    , ( "user", "View", ["User"]
      , ( "activity", "actor", "address", "alternate_addresses"
        , "clearance_by", "creation", "creator", "department"
        , "firstname", "job_description", "lastname"
        , "id", "lunch_duration", "lunch_start", "nickname"
        , "pictures", "position", "queries", "realname", "room", "sex"
        , "status", "subst_active", "substitute", "supervisor", "timezone"
        , "title", "username", "home_directory", "login_shell"
        , "samba_home_drive", "samba_home_path", "tt_lines"
        )
      )
    ]

schemadef.register_class_permissions (db, classes, prop_perms)
schemadef.allow_user_details         (db, 'User', 'Edit')
# the following is further checked in an auditor:
db.security.addPermissionToRole ('User', 'Create', 'time_wp')

# editing of roles:
for r in "HR", "IT" :
    db.security.addPermissionToRole (r, 'Web Roles')

# oh, g'wan, let anonymous access the web interface too
# NOT really !!!
db.security.addPermissionToRole('Anonymous', 'Web Access')
