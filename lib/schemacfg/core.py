# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
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

from schemacfg import schemadef
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
    msg.setorderprop ('date')

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
        , queries               = Multilink ("query")
        , roles                 = String    ()
        , status                = Link      ("user_status", do_journal='no')
        , timezone              = String    ()
        )
    user.setkey ('username')

    if 'User_Status_Class' in kw :
        user_status = kw ['User_Status_Class'] (db, ''"user_status")

    if 'Room_Class' in kw :
        room = kw ['Room_Class'] (db, ''"room")
# end def init

def register_linkperms (db, linkperms) :
    for cls, roles, perms, classprops in linkperms :
        for role in roles :
            if role.lower () not in db.security.role :
                continue
            for perm in perms :
                schemadef.register_permission_by_link \
                    (db, role, perm, cls, * classprops)
# end def register_linkperms

def view_file(db, userid, itemid):
    """ Users are allowed to view their files """
    return userid == db.file.get(itemid, 'creator')
# end def view_file

def edit_query(db, userid, itemid):
    """ Users are allowed to edit their queries """
    return userid == db.query.get(itemid, 'creator')
# end def edit_query

def view_query (db, userid, itemid) :
    """ Users are allowed to view their own and public queries for
        classes where they have search permission
    """
    q = db.query.getnode (itemid)
    if not q.private_for :
        if not q.klass :
            return False
        prop = db.getclass (q.klass).labelprop ()
        return db.security.hasSearchPermission (userid, q.klass, prop)
    return userid == q.private_for
# end def view_query

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
        , ("file", ['IT'],        ['View', 'Edit'], linkclass_iter (db, "file"))
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

    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'msg'
        , description = "User is allowed to search for their own messages"
        )
    db.security.addPermissionToRole('User', p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'file'
        , check       = view_file
        , description = "User is allowed to view their own files"
        )
    db.security.addPermissionToRole('User', p)

    register_linkperms (db, linkperms)
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'file'
        , description = "User is allowed to search for their own files"
        )
    db.security.addPermissionToRole('User', p)


    ### Query permissions ###

    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'query'
        , description = "User is allowed to search for their queries"
        )
    db.security.addPermissionToRole('User', p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'query'
        , check       = view_query
        , description = schemadef.security_doc_from_docstring
            (view_query.__doc__)
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
    db.security.addPermissionToRole ('User', 'Rest Access')
    db.security.addPermissionToRole ('User', 'Xmlrpc Access')

# end def security
