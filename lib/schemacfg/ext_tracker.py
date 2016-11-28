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

from schemacfg       import schemadef

def init \
    ( db
    , Class
    , Ext_Tracker_Class
    , String
    , Link
    , Multilink
    , Number
    , ** kw
    ) :
    export = {}

    # These need to be set for supported implementations.
    # Currently we have Jira and KPM.
    ext_tracker_type = Class \
        ( db, "ext_tracker_type"
        , name                = String    (indexme = 'no')
        , order               = Number    ()
        )
    ext_tracker_type.setkey("name")

    ext_tracker = Ext_Tracker_Class \
        ( db, "ext_tracker"
        , name                = String    (indexme = 'no')
        , description         = String    (indexme = 'no')
        , url_template        = String    (indexme = 'no')
        , type                = Link      ('ext_tracker_type')
        )
    ext_tracker.setkey("name")

    # Needed to mark synced messages for some external tracker
    # implementations. Similar to ext_tracker_state for issues below.
    ext_msg = Class \
        ( db, "ext_msg"
        , ext_tracker         = Link      ("ext_tracker")
        , msg                 = Link      ("msg")
        , ext_id              = String    (indexme = 'no')
        , key                 = String    (indexme = 'no')
        )
    ext_msg.setkey ("key")

    ext_tracker_state = Class \
        ( db, "ext_tracker_state"
        , ext_id              = String    ()
        , ext_status          = String    ()
        , ext_attributes      = Link      ("msg")
        , ext_tracker         = Link      ("ext_tracker")
        , issue               = Link      ("issue")
        )
    ext_tracker_state.setlabelprop ('ext_id')

    Cat_Cl = kw ['Category_Class']
    class Category_Class (Cat_Cl) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( ext_trackers        = Multilink ("ext_tracker")
                )
            Cat_Cl.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Category_Class
    export ['Category_Class'] = Category_Class

    return export
# end def init

def security (db, ** kw) :
    roles = \
        [ ("MsgEdit",     "Allowed to edit message properties")
        , ("MsgSync",     "Allowed to sync message with ext. tracker")
        , ("Issue_Admin", "Admin for issue tracker")
        ]
    #     classname             allowed to view
    #                           allowed to edit
    classes = \
        [ ("ext_tracker",       ["User"],
                                ["Issue_Admin"]
          )
        , ("ext_msg",           ["MsgEdit", "MsgSync"],
                                ["MsgSync"]
          )
        , ("ext_tracker_type",  ["MsgEdit", "MsgSync", "User"],
                                []
          )
        , ("ext_tracker_state", ["MsgEdit", "MsgSync", "User"],
                                ["MsgSync"]
          )
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
