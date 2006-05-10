# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@mexx.mobile
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
#    schema
#
# Purpose
#    Specify the DB-Schema for the tttech2 issue tracker.
#
# Revision Dates
#    22-Jun-2004 (MPH) Creation
#     5-Jul-2004 (MPH) Work in progress.
#     6-Jul-2004 (MPH) Added `closed-obsolete` to `work_package_status`.
#    23-Jul-2004 (MPH) Removed `automatic` status changes from `feature_status`
#     5-Oct-2004 (MPH) Split `work_package` into `implementation_task` and
#                      `documentation_task`
#    14-Oct-2004 (pr) Major changes
#                      - `task` with `task_kind` instead of `*_task` and
#                        `testcase`
#                      - added `estimated_[begin|end]` to task
#                      - added `task` link to `defect` and vice versa, to
#                        have to possibility to add defects also to tasks
#                      - added `defects` multilink to `feature` (was missing)
#                      - cleanup of unused classes
#     4-Nov-2004 (MPH) Effort: `Interval` -> `Number`
#     8-Nov-2004 (MPH) Cleanup, removed `accepted-but-defects` from
#                      `document_status`
#     9-Nov-2004 (MPH) Added `completed-but-defects` to `feature_status`
#    16-Nov-2004 (MPH) Added `May Public Queries` permission to `query`
#     1-Dec-2004 (MPH) Added `is_alias` to Class `user`
#     5-Apr-2005 (MPH) Added `composed_of` and `part_of` to `feature`, added
#                      support for Online Peer Reviews
#     6-Apr-2005 (RSC) Factored from dbinit.py for roundup 0.8.2
#                      "May Public Queries"->"May publish Queries"
#    11-Apr-2005 (MPH) Fixed Multilink in `review` and `announcement` to link
#                      to `file` instead of `files`
#     6-Jun-2005 (RSC) Incorporate changes from dbinit.py
#     8-Jun-2005 (RSC) time_record and time_wp added.
#                      IssueClass used directly
#    15-Jun-2005 (RSC) i18n stuff for name translations
#    22-Jun-2005 (RSC) schema additions for time-tracking
#    22-Jun-2005 (RSC) schema additions for time-tracking
#                      moved some comments in the class definition into
#                      the extensions/help.py
#    ««revision-date»»···
#--
#

import sys, os

sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
sys.path.insert (0, os.path.join (db.config.HOME, 'schema'))
from common import clearance_by

# sub-schema definitins to include
schemas = \
    ( 'schemadef'
    , 'ext_issue'
    , 'company'
    , 'complex'
    , 'it_tracker'
    , 'nwm'
    , 'severity'
    , 'time_tracker'
    )

# Class automatically gets these properties:
#   creation = Date ()
#   activity = Date ()
#   creator  = Link ('user')

query = Class \
    ( db
    , ''"query"
    , klass                 = String    ()
    , name                  = String    ()
    , url                   = String    ()
    , private_for           = Link      ('user')
    )

# FileClass automatically gets these properties:
#   content = String()    [saved to disk in <tracker home>/db/files/]
#   (it also gets the Class properties creation, activity and creator)
FileClass \
    ( db
    , ''"msg"
    , date                  = Date      ()
    , files                 = Multilink ("file")
    # Note: below fields are used by roundup internally (obviously by the
    #       mail-gateway)
    , author                = Link      ("user", do_journal='no')
    , recipients            = Multilink ("user", do_journal='no')
    , summary               = String    ()
    , messageid             = String    ()
    , inreplyto             = String    ()
    )

FileClass \
    ( db
    , ''"file"
    , name                  = String    ()
    , type                  = String    ()
    )

vars = \
    { 'Class'      : Class
    , 'FileClass'  : FileClass
    , 'IssueClass' : IssueClass
    , 'String'     : String
    , 'Password'   : Password
    , 'Date'       : Date
    , 'Link'       : Link
    , 'Multilink'  : Multilink
    , 'Interval'   : Interval
    , 'Boolean'    : Boolean
    , 'Number'     : Number
    , 'db'         : db
    }
modules = {}
for s in schemas :
    m = __import__ (s)
    globals ().update (((s, m),))
    if hasattr (m, 'init') :
        v = m.init (** vars)
        if v :
            vars.update (v)
    modules [s] = m

del sys.path [0:1]

Department_Class = vars ['Department_Class']
Department_Class (db, ''"department")

User_Class = vars ['User_Class']
User_Class \
    ( db
    , ''"user"
    , username              = String    ()
    , password              = Password  ()
    , address               = String    ()
    , alternate_addresses   = String    ()
    , realname              = String    ()
    , phone                 = String    ()
    , queries               = Multilink ("query")
    , roles                 = String    ()
    , timezone              = String    ()
    )

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
# Will have special handling for queries, see below
    , ("query"               , ["Admin"], ["Admin"           ])
    ]

prop_perms = \
    [ ( "user", "Edit", ["Admin", "HR", "IT"]
      , ( "address"
        , "alternate_addresses"
        , "nickname"
        , "password"
        , "timezone"
        , "username"
        )
      )
    , ( "user", "Edit", ["Admin", "HR"]
      , ( "clearance_by", "external_phone", "firstname"
        , "job_description", "lastname", "lunch_duration", "lunch_start"
        , "phone", "pictures", "position", "private_phone", "realname"
        , "room", "sex", "status", "subst_active", "substitute", "supervisor"
        , "title", "roles"
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

### Query permissions ###
def view_query (db, userid, itemid) :
    private_for = db.query.get (itemid, 'private_for')
    if not private_for : return True
    return userid == private_for
# end def view_query

def edit_query(db, userid, itemid):
    return userid == db.query.get(itemid, 'creator')
# end def edit_query

p = db.security.addPermission \
    ( name        = 'View'
    , klass       = 'query'
    , check       = view_query
    , description = "User is allowed to view their own and public queries"
    )
db.security.addPermissionToRole('User', p)
p = db.security.addPermission \
    ( name        = 'Edit'
    , klass       = 'query'
    , check       = edit_query
    , description = "User is allowed to edit their queries"
    )
db.security.addPermissionToRole('User', p)
p = db.security.addPermission \
    ( name        = 'Create'
    , klass       = 'query'
    , description = "User is allowed to create queries"
    )
db.security.addPermissionToRole('User', p)

# and give the regular users access to the web and email interface
db.security.addPermissionToRole ('User', 'Web Access')
db.security.addPermissionToRole ('User', 'Email Access')

# editing of roles:
for r in "Admin", "HR", "IT" :
    db.security.addPermissionToRole (r, 'Web Roles')

# oh, g'wan, let anonymous access the web interface too
# NOT really !!!
db.security.addPermissionToRole('Anonymous', 'Web Access')

for s in schemas :
    m = modules [s]
    if hasattr (m, 'security') :
        m.security (** vars)
