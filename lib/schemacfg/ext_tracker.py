# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-15 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    issue extension
#
# Purpose
#    Schema definitions for issue tracker with external sync
#
#--
#

from roundup.hyperdb import Class
from schemacfg       import schemadef

def init \
    ( db
    , Class
    , Ext_Mixin
    , String
    , Date
    , Link
    , Multilink
    , Number
    , Boolean
    , ** kw
    ) :
    export = {}

    ext_tracker = Class \
        ( db, "ext_tracker"
        , name                = String    (indexme = 'no')
        , description         = String    (indexme = 'no')
        , url_template        = String    (indexme = 'no')
        )
    ext_tracker.setkey("name")

    ext_msg = Class \
        ( db, "ext_msg"
        , ext_tracker         = Link      ("ext_tracker")
        , msg                 = Link      ("msg")
        , ext_id              = String    (indexme = 'no')
        , key                 = String    (indexme = 'no')
        )
    ext_msg.setkey ("key")

    Opt_Doc = kw ['Optional_Doc_Issue_Class']
    class Optional_Doc_Issue_Class (Opt_Doc) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( ext_id              = String    ()
                , ext_status          = String    ()
                , ext_attributes      = Link      ("msg")
                , ext_tracker         = Link      ("ext_tracker")
                )
            Opt_Doc.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Optional_Doc_Issue_Class
    export ['Optional_Doc_Issue_Class'] = Optional_Doc_Issue_Class

    return export
# end def init

def security (db, ** kw) :
    roles = \
        [ ("MsgEdit",     "Allowed to edit message properties")
        , ("MsgSync",     "Allowed to sync message with ext. tracker")
        , ("Issue_Admin", "Admin for issue tracker")
        ]
    #     classname             allowed to view   /  edit
    classes = \
        [ ("ext_tracker",       ["User"],               ["Issue_Admin"])
        , ("ext_msg",           ["MsgEdit", "MsgSync"], ["MsgSync"])
        ]
    prop_perms = []

    schemadef.register_roles                 (db, roles)
    schemadef.register_class_permissions     (db, classes, prop_perms)

    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'msg'
        , properties  = ("date", "id")
        )
    db.security.addPermissionToRole ('MsgEdit', p)
    db.security.addPermissionToRole ('MsgSync', p)
# end def security
