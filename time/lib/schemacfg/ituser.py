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
#    ituser
#
# Purpose
#    Role and access rights for IT helpdesk client user

from roundup.hyperdb import Class
from schemacfg       import schemadef, core
from linking         import linkclass_iter
from common          import user_has_role

def security (db, ** kw) :
    roles = \
        [ ("ITuser", "IT-Helpdesk user with less access")
        ]

    classes   = [('it_issue_status', ["ITuser"], [])]
    linkperms = \
        [ ("file", ["ITuser"], ['View'], linkclass_iter (db, "file"))
        , ("msg",  ["ITuser"], ['View'], linkclass_iter (db, "msg"))
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, ())
    core.register_linkperms              (db, linkperms)

    def is_on_nosy (db, userid, itemid) :
        "User is allowed to access it_issue if on nosy list"
        item = db.it_issue.getnode (itemid)
        return userid in item.nosy
    # end def is_on_nosy

    def is_it_staff (db, userid, itemid) :
        "User is allowed to see other IT users"
        return user_has_role (db, itemid, "IT")
    # end def is_it_staff

    it_r_props = \
        ( 'status', 'responsible', 'stakeholder', 'creation', 'creator'
        , 'activity', 'actor', 'messages', 'files'
        )
    it_rw_props = \
        ('title', 'deadline', 'confidential')

    for perm, props in (('View', it_r_props), ('Edit', it_rw_props)) :
        p = db.security.addPermission \
            ( name        = perm
            , klass       = 'it_issue'
            , check       = is_on_nosy
            , description = is_on_nosy.__doc__
            , properties  = props
            )
        db.security.addPermissionToRole ('ITuser', p)


    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'user'
        , check       = schemadef.own_user_record
        , description = "Users are allowed to edit some of their properties"
        , properties  =
            ("password", "realname", "alternate_addresses", "csv_delimiter")
        )
    db.security.addPermissionToRole ('ITuser', p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'user'
        , check       = schemadef.own_user_record
        , description = "Users are allowed to see some of their attributes"
        , properties  = ("username", "address")
        )
    db.security.addPermissionToRole ('ITuser', p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'user'
        , check       = is_it_staff
        , description = is_it_staff.__doc__
        , properties  = ("username", "realname")
        )
    db.security.addPermissionToRole ('ITuser', p)

    p = db.security.getPermission   ('Create', 'file')
    db.security.addPermissionToRole ('ITuser', p)
    for klass in ('file', 'it_issue', 'msg', 'query') :
        try :
            p = db.security.getPermission   ('Search', klass)
        except ValueError :
            p = db.security.addPermission \
                ( name  = 'Search'
                , klass = klass
                )
        db.security.addPermissionToRole ('ITuser', p)
    db.security.addPermissionToRole ('ITuser', p)
    try :
        p = db.security.getPermission   ('View', 'file', check = core.view_file)
    except ValueError :
        p = db.security.addPermission \
            ( name  = 'Search'
            , klass = 'file'
            , check = core.view_file
            , description = core.view_file.__doc__
            )
    db.security.addPermissionToRole ('ITuser', p)

    p = db.security.getPermission   ('Create', 'it_issue')
    db.security.addPermissionToRole ('ITuser', p)

    p = db.security.getPermission   ('Create', 'msg')
    db.security.addPermissionToRole ('ITuser', p)

    p = db.security.getPermission   ('Create', 'query')
    db.security.addPermissionToRole ('ITuser', p)
    for perm in 'Edit', 'Retire' :
        try :
            p = db.security.getPermission \
                (perm, 'query', check = core.edit_query)
        except ValueError :
            p = db.security.addPermission \
                ( name  = perm
                , klass = 'query'
                , check = core.edit_query
                , description = core.edit_query.__doc__
                )
        db.security.addPermissionToRole ('ITuser', p)
    try :
        p = db.security.getPermission ('View', 'query', check = core.view_query)
    except ValueError :
        p = db.security.addPermission \
            ( name  = perm
            , klass = 'query'
            , check = core.view_query
            , description = core.view_query.__doc__
            )
    db.security.addPermissionToRole ('ITuser', p)

    db.security.addPermissionToRole ('ITuser', 'Web Access')
    db.security.addPermissionToRole ('ITuser', 'Email Access')
# end def security
