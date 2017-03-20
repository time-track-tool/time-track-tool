#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2017 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#++
# Name
#    rouser
#
# Purpose
#    Role and access rights for read-only user
#    Include this last, *after* core as it extends the permissions
#    defined in core. Needs external_users module.

from roundup.hyperdb import Class
from schemacfg       import schemadef, core
from linking         import linkclass_iter

def security (db, ** kw) :
    roles = \
        [ ("Readonly-User"      , "User with less access")
        ]

    classes = \
        [ ("area",              ["Readonly-User"],    [])
        , ("doc_issue_status",  ["Readonly-User"],    [])
        , ("keyword",           ["Readonly-User"],    [])
        , ("kind",              ["Readonly-User"],    [])
        , ("msg_keyword",       ["Readonly-User"],    [])
        , ("severity",          ["Readonly-User"],    [])
        , ("status",            ["Readonly-User"],    [])
        , ("status_transition", ["Readonly-User"],    [])
        , ("ext_tracker_state", ["Readonly-User"],    [])
        , ("safety_level",      ["Readonly-User"],    [])
        , ("test_level",        ["Readonly-User"],    [])
        ]
    if 'fault_frequency' in db.classes :
        classes.append \
         (("fault_frequency",   ["Readonly-User"],    []))
    if 'kpm' in db.classes :
        classes.append \
         (("kpm",               ["Readonly-User"],    []))
    if 'kpm_function' in db.classes :
        classes.append \
         (("kpm_function",      ["Readonly-User"],    []))
    if 'kpm_hw_variant' in db.classes :
        classes.append \
         (("kpm_hw_variant",    ["Readonly-User"],    []))
    if 'kpm_occurrence' in db.classes :
        classes.append \
         (("kpm_occurrence",    ["Readonly-User"],    []))
    if 'kpm_release' in db.classes :
        classes.append \
         (("kpm_release",       ["Readonly-User"],    []))
    if 'kpm_tag' in db.classes :
        classes.append \
         (("kpm_tag",           ["Readonly-User"],    []))
    if 'ext_tracker_type' in db.classes :
        classes.append \
         (("ext_tracker_type",  ["Readonly-User"],    []))
    prop_perms = \
        [ ( "user",        "View", ["Readonly-User"]
          , ("username", "nickname", "status")
          )
        , ( "category",    "View", ["Readonly-User"]
          , ("name", "id")
          )
        , ( "user_status", "View", ["Readonly-User"]
          , ("name", )
          )
        ]
    linkperms = \
        [ ("file", ["Readonly-User"], ['View'], linkclass_iter (db, "file"))
        , ("msg",  ["Readonly-User"], ['View'], linkclass_iter (db, "msg"))
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)
    core.register_linkperms              (db, linkperms)

    # don't allow Readonly-User for some issue attributes
    exceptions = dict.fromkeys \
        (('external_company', 'confidential'))
    issue_props = [p for p in db.issue.getprops ().iterkeys ()
                   if p not in exceptions
                  ]

    if 'external_users' in db.issue.properties :
        def ro_user_access (db, userid, itemid) :
            """ Read-only users are allowed to view issue
                if they are on the list of allowed external users or
                there is a transitive permission via containers.
            """
            issue = db.issue.getnode (itemid)
            while True :
                if issue.external_users and userid in issue.external_users :
                    return True
                if not issue.part_of :
                    break
                issue = db.issue.getnode (issue.part_of)
            return False
        # end def ext_user_access

        p = db.security.addPermission \
            ( name        = 'View'
            , klass       = 'issue'
            , check       = ro_user_access
            , description = schemadef.security_doc_from_docstring
                (ro_user_access.__doc__)
            , properties  = issue_props
            )
        db.security.addPermissionToRole ('Readonly-User', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'user'
        , check       = schemadef.own_user_record
        , description = "Users are allowed to edit some of their details"
        , properties  = ("timezone", "csv_delimiter", "hide_message_files")
        )
    db.security.addPermissionToRole ('Readonly-User', p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'user'
        , check       = schemadef.own_user_record
        , description = "Users are allowed to view some of their details"
        , properties  =
            ( "username", "realname", "firstname", "lastname"
            , "creation", "creator", "activity", "actor"
            )
        )
    db.security.addPermissionToRole ('Readonly-User', p)

    p = db.security.getPermission   ('Search', 'file')
    db.security.addPermissionToRole ('Readonly-User', p)
    p = db.security.getPermission   ('View', 'file', check = core.view_file)
    db.security.addPermissionToRole ('Readonly-User', p)

    p = db.security.getPermission   ('Search', 'issue')
    db.security.addPermissionToRole ('Readonly-User', p)
    # need search permission on username + id if we want to search for
    # user Link/Multilink properties on issue (e.g. responsible, nosy, ..)
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'user'
        , properties  = ("username", "nickname", "id")
        )
    db.security.addPermissionToRole ('Readonly-User', p)
    # Need search-permission on ext_tracker_state
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'ext_tracker_state'
        , properties  = ("issue", "id")
        )
    db.security.addPermissionToRole ('Readonly-User', p)

    p = db.security.getPermission   ('View', 'ext_tracker')
    db.security.addPermissionToRole ('Readonly-User', p)

    p = db.security.getPermission   ('Search', 'msg')
    db.security.addPermissionToRole ('Readonly-User', p)

    db.security.addPermissionToRole ('Readonly-User', 'Web Access')
    db.security.addPermissionToRole ('Readonly-User', 'Email Access')
# end def security
