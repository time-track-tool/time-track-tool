#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2012-13 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    extuser
#
# Purpose
#    Role and access rights for external user
#    Include this last, *after* core as it extends the permissions
#    defined in core.

from roundup.hyperdb import Class
from schemacfg       import schemadef, core
from linking         import linkclass_iter

def security (db, ** kw) :
    roles = \
        [ ("External"      , "External user with less access")
        ]

    classes = \
        [ ("area",              ["External"],    [])
        , ("doc_issue_status",  ["External"],    [])
        , ("keyword",           ["External"],    [])
        , ("kind",              ["External"],    [])
        , ("msg_keyword",       ["External"],    [])
        , ("severity",          ["External"],    [])
        , ("status",            ["External"],    [])
        , ("status_transition", ["External"],    [])
        , ("ext_tracker_state", ["External"],    [])
        ]
    if 'fault_frequency' in db.classes :
        classes.append \
         (("fault_frequency",   ["External"],    []))
    if 'kpm' in db.classes :
        classes.append \
         (("kpm",               ["External"],    ["External"]))
    if 'kpm_function' in db.classes :
        classes.append \
         (("kpm_function",      ["External"],    []))
    if 'kpm_hw_variant' in db.classes :
        classes.append \
         (("kpm_hw_variant",    ["External"],    []))
    if 'kpm_occurrence' in db.classes :
        classes.append \
         (("kpm_occurrence",    ["External"],    []))
    if 'kpm_release' in db.classes :
        classes.append \
         (("kpm_release",       ["External"],    []))
    if 'kpm_tag' in db.classes :
        classes.append \
         (("kpm_tag",           ["External"],    []))
    if 'ext_tracker_type' in db.classes :
        classes.append \
         (("ext_tracker_type",  ["External"],    []))
    prop_perms = \
        [ ( "user",        "View", ["External"]
          , ("username", "nickname", "status")
          )
        , ( "category",    "View", ["External"]
          , ("name", )
          )
        , ( "user_status", "View", ["External"]
          , ("name", )
          )
        ]
    linkperms = \
        [ ("file", ["External"], ['View', 'Edit'], linkclass_iter (db, "file"))
        , ("msg",  ["External"],         ['View'], linkclass_iter (db, "msg"))
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)
    core.register_linkperms              (db, linkperms)

    # don't allow external_company or External for some issue attributes
    exceptions = dict.fromkeys \
        (('external_company', 'confidential', 'external_users', 'inherit_ext'))
    issue_props = [p for p in db.issue.getprops ().iterkeys ()
                   if p not in exceptions
                  ]

    if 'external_company' in db.issue.properties :
        def ext_company_access (db, userid, itemid) :
            """ Users are allowed to access issue
                if their external company has access
            """
            ec = db.user.get (userid, 'external_company')
            ecs = db.issue.get (itemid, 'external_company')
            return ecs and ec in ecs
        # end def ext_company_access

        for perm in ('View', 'Edit') :
            p = db.security.addPermission \
                ( name        = perm
                , klass       = 'issue'
                , check       = ext_company_access
                , description = schemadef.security_doc_from_docstring
                    (ext_company_access.__doc__)
                , properties  = issue_props
                )
            db.security.addPermissionToRole ('External', p)

    if 'external_users' in db.issue.properties :
        issue_props.append ('external_users')
        def ext_user_access (db, userid, itemid) :
            """ External users are allowed to access issue
                if they are on the list of allowed external users or
                there is a transitive permission via containers.
            """
            issue = db.issue.getnode (itemid)
            while True :
                if issue.external_users and userid in issue.external_users :
                    return True
                if not issue.part_of :
                    break
                # check parent permissions for non-container or if the
                # container defines inherit_ext
                if issue.composed_of and not issue.inherit_ext :
                    break
                issue = db.issue.getnode (issue.part_of)
            return False
        # end def ext_user_access

        for perm in ('View', 'Edit') :
            p = db.security.addPermission \
                ( name        = perm
                , klass       = 'issue'
                , check       = ext_user_access
                , description = schemadef.security_doc_from_docstring
                    (ext_user_access.__doc__)
                , properties  = issue_props
                )
            db.security.addPermissionToRole ('External', p)

    # Currently *never* allow any rights from being on nosy list
    if False :
        def is_on_nosy (db, userid, itemid) :
            "User is allowed to access issue if on nosy list"
            item = db.issue.getnode (itemid)
            return userid in item.nosy
        # end def is_on_nosy

        for perm in ('View', 'Edit') :
            p = db.security.addPermission \
                ( name        = perm
                , klass       = 'issue'
                , check       = is_on_nosy
                , description = schemadef.security_doc_from_docstring
                    (is_on_nosy.__doc__)
                , properties  = issue_props
                )
            db.security.addPermissionToRole ('External', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'user'
        , check       = schemadef.own_user_record
        , description = "Users are allowed to edit some of their details"
        , properties  = ( "password", "timezone", "csv_delimiter"
                        , "hide_message_files"
                        )
        )
    db.security.addPermissionToRole ('External', p)
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
    db.security.addPermissionToRole ('External', p)

    p = db.security.getPermission   ('Create', 'file')
    db.security.addPermissionToRole ('External', p)
    p = db.security.getPermission   ('Search', 'file')
    db.security.addPermissionToRole ('External', p)
    p = db.security.getPermission   ('View', 'file', check = core.view_file)
    db.security.addPermissionToRole ('External', p)

    p = db.security.getPermission   ('Create', 'issue')
    db.security.addPermissionToRole ('External', p)
    p = db.security.getPermission   ('Search', 'issue')
    db.security.addPermissionToRole ('External', p)
    # need search permission on username + id if we want to search for
    # user Link/Multilink properties on issue (e.g. responsible, nosy, ..)
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'user'
        , properties  = ("username", "nickname", "id")
        )
    db.security.addPermissionToRole ('External', p)
    # Need search-permission on ext_tracker_state
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'ext_tracker_state'
        , properties  = ("issue", "id")
        )
    db.security.addPermissionToRole ('External', p)

    p = db.security.getPermission   ('View', 'ext_tracker')
    db.security.addPermissionToRole ('External', p)

    p = db.security.getPermission   ('Create', 'msg')
    db.security.addPermissionToRole ('External', p)
    p = db.security.getPermission   ('Search', 'msg')
    db.security.addPermissionToRole ('External', p)

    p = db.security.getPermission   ('Create', 'query')
    db.security.addPermissionToRole ('External', p)
    p = db.security.getPermission   ('Edit', 'query', check = core.edit_query)
    db.security.addPermissionToRole ('External', p)
    p = db.security.getPermission   ('Retire', 'query', check = core.edit_query)
    db.security.addPermissionToRole ('External', p)
    p = db.security.getPermission   ('Search', 'query')
    db.security.addPermissionToRole ('External', p)
    p = db.security.getPermission   ('View', 'query', check = core.view_query)
    db.security.addPermissionToRole ('External', p)

    db.security.addPermissionToRole ('External', 'Web Access')
    db.security.addPermissionToRole ('External', 'Email Access')
# end def security
