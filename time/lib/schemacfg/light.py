# -*- coding: iso-8859-1 -*-
# Copyright (C) 2013 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    light
#
# Purpose
#    Schema definitions for lightweight issue tracker
#
#--
#

from roundup.hyperdb import Class
from schemacfg       import schemadef

def init \
    ( db
    , Class
    , Optional_Doc_Issue_Class
    , Ext_Mixin
    , String
    , Date
    , Link
    , Multilink
    , Number
    , Boolean
    , ** kw
    ) :
    stat = Class \
        ( db, "status"
        , name                = String    (indexme = 'no')
        , description         = String    (indexme = 'no')
        , transitions         = Multilink ("status")
        , order               = String    (indexme = 'no')
        )
    stat.setkey ("name")

    prio = Class \
        ( db
        , ''"prio"
        , name                  = String    ()
        , order                 = Number    ()
        )
    prio.setkey ("name")

    Optional_Doc_Issue_Class \
        ( db, "issue"
        , keywords              = Multilink ("keyword", do_journal = 'no')
        , priority              = Link      ("prio",    do_journal = 'no')
        , status                = Link      ("status",  do_journal = 'no')
        , closed                = Date      ()
        )
# end def init

def security (db, ** kw) :
    roles = \
        [ ("Issue_Admin", "Admin for issue tracker")
        , ("Nosy",        "Allowed on nosy list")
        ]
    #     classname             allowed to view   /  edit
    classes = \
        [ ("issue",             ["Issue_Admin"], ["Issue_Admin"])
        , ("status",            ["User"],        ["Issue_Admin"])
        , ("prio",              ["User"],        ["Issue_Admin"])
        ]

    schemadef.register_roles                 (db, roles)
    schemadef.register_class_permissions     (db, classes, ())
    schemadef.register_nosy_classes          (db, ['issue'])
    db.security.addPermissionToRole          ('User', 'Create', 'issue')
    schemadef.add_search_permission (db, 'issue', 'User')
# end def security
