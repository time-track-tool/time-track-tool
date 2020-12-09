# Copyright (C) 2020 Dr. Ralf Schlatterbeck Open Source Consulting.
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

import common
from   schemacfg import schemadef

def init (db, Link, Multilink, Number, String, Class, ** kw) :
    export = {}

    substance = Class \
        ( db, ''"substance"
        , name                  = String    ()
        , identifier            = String    ()
        )
    substance.setkey ("identifier")

    ingredient_used_by_substance = Class \
        ( db, ''"ingredient_used_by_substance"
        , substance             = Link      ('substance'
                                            , rev_multilink  = 'ingredients'
                                            , try_id_parsing = 'no'
                                            )
        , ingredient            = Link      ('substance'
                                            , rev_multilink  = 'part_of'
                                            , try_id_parsing = 'no'
                                            )
        , quantity              = Number    ()
        )

# end def init

def security (db, ** kw) :
    roles = \
        [ ("User", "Normal user of the system")
        ]
    classes = \
        [ ("substance",                    ["User"], ["User"])
        , ("ingredient_used_by_substance", ["User"], ["User"])
        ]
    schemadef.register_roles (db, roles)
    schemadef.register_class_permissions (db, classes, [])
# end def security
