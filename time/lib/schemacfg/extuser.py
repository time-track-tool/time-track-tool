#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck Open Source Consulting.
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
        , ("user_status",       ["External"],    [])
        ]
    prop_perms = \
        [ ( "user",     "View", ["External"]
          , ( "username", "lastname", "firstname", "realname", "status"
            , "creation", "creator", "activity", "actor"
            )
          )
        , ( "category", "View", ["External"]
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
            , description = is_on_nosy.__doc__
            )
        db.security.addPermissionToRole ('External', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'user'
        , check       = schemadef.own_user_record
        , description = "Users are allowed to edit their password"
        , properties  = ("password",)
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
