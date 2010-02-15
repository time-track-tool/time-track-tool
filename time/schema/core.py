# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
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
#    core
#
# Purpose
#    Schema definitions needed in any case by every tracker
#
#--
#

import schemadef
from linking import linkclass_iter

def init \
    ( db
    , Class
    , FileClass
    , Msg_Class
    , String
    , Password
    , Date
    , Link
    , Multilink
    , ** kw
    ) :
    # FileClass automatically gets these properties:
    #   content = String()    [saved to disk in <tracker home>/db/files/]
    #   (it also gets the Class properties creation, activity and creator)
    FileClass \
        ( db
        , ''"file"
        , name                  = String    (indexme = 'no')
        , type                  = String    (indexme = 'no')
        , content               = String    (indexme = 'no')
        )

    msg = Msg_Class  (db , ''"msg")
    msg.setorderprop ('creation')

    query = Class \
        ( db
        , ''"query"
        , klass                 = String    ()
        , name                  = String    ()
        , url                   = String    ()
        , private_for           = Link      ('user')
        , tmplate               = String    ()
        )

    User_Class = kw.get ('User_Class', Class)
    user = User_Class \
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
        , status                = Link      ("user_status")
        , timezone              = String    ()
        )
    user.setkey ('username')

    user_status = Class \
        ( db
        , ''"user_status"
        , name                  = String    ()
        , description           = String    ()
        )
    user_status.setkey ("name")
# end def init

def security (db, ** kw) :
    """ See the configuration and customisation document for information
        about security setup. Assign the access and edit Permissions for
        issue, file and message to regular users now
    """

    # Will have special handling for queries, see below
    #     classname        allowed to view   /  edit
    classes = \
        [ ("user_status", ["User"],  [])
        , ("query",       [],        [])
        ]

    linkperms = \
        [ ("file", ['User'],      ['View', 'Edit'], linkclass_iter (db, "file"))
        , ("msg",  ['User'],              ['View'], linkclass_iter (db, "msg"))
        , ("msg",  ['Issue_Admin', 'IT'], ['Edit'], linkclass_iter (db, "msg"))
        ]

    schemadef.register_class_permissions (db, classes, [])
    # Allow creation of file and msg for normal users:
    db.security.addPermissionToRole ('User', 'Create', 'file')
    db.security.addPermissionToRole ('User', 'Create', 'msg')

    def view_msg(db, userid, itemid):
        return userid == db.msg.get(itemid, 'creator')
    # end def view_msg

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'msg'
        , check       = view_msg
        , description = "User is allowed to view their own messages"
        )
    db.security.addPermissionToRole('User', p)

    def view_file(db, userid, itemid):
        return userid == db.file.get(itemid, 'creator')
    # end def view_file

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'file'
        , check       = view_file
        , description = "User is allowed to view their own files"
        )
    db.security.addPermissionToRole('User', p)
    for cls, roles, perms, classprops in linkperms :
        for role in roles :
            if role.lower () not in db.security.role :
                continue
            for perm in perms :
                schemadef.register_permission_by_link \
                    (db, role, perm, cls, * classprops)

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
        ( name        = 'Retire'
        , klass       = 'query'
        , check       = edit_query
        , description = "User is allowed to retire their queries"
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

# end def security
