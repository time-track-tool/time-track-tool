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
#    keyword
#
# Purpose
#    Schema definition for keyword class
#
#--
#

from roundup.hyperdb import Class
from schemacfg       import schemadef

def init (db, Class, String, ** kw) :
    keyword = Class \
        ( db, "keyword"
        , name                = String    (indexme = 'no')
        , description         = String    (indexme = 'no')
        )
    keyword.setkey ("name")
# end def init

def security (db, ** kw) :
    roles = \
        [ ("Issue_Admin", "Admin for issue tracker")
        , ("Nosy",        "Allowed on nosy list")
        ]
    #     classname             allowed to view   /  edit
    classes = \
        [ ("keyword",           ["User"],        ["Issue_Admin"])
        ]

    schemadef.register_roles                 (db, roles)
    schemadef.register_class_permissions     (db, classes, ())
# end def security
