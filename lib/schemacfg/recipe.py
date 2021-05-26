# Copyright (C) 2020-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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

def init (db, Link, Multilink, Number, String, Boolean, Class, ** kw) :
    export = {}

    substance = Class \
        ( db, ''"substance"
        , name                  = String    ()
        , identifier            = String    ()
        , is_raw_material       = Boolean   ()
        )
    substance.setkey ("identifier")

    ingredient_used_by_substance = Class \
        ( db, ''"ingredient_used_by_substance"
        , substance        = Link      ('substance'
                                       , rev_multilink = 'ingredients'
                                       )
        , ingredient       = Link      ('substance'
                                       , rev_multilink = 'part_of'
                                       )
        , quantity         = Number    ()
        )
    ingredient_used_by_substance.setlabelprop ('substance')

    rc_product_type = Class \
        ( db, ''"rc_product_type"
        , name             = String    ()
        , description      = String    ()
        )
    rc_product_type.setkey ("name")

    rc_application = Class \
        ( db, ''"rc_application"
        , name             = String    ()
        , description      = String    ()
        )
    rc_application.setkey ("name")

    rc_substrate = Class \
        ( db, ''"rc_substrate"
        , name             = String    ()
        , description      = String    ()
        )
    rc_substrate.setkey ("name")

    rc_suitability = Class \
        ( db, ''"rc_suitability"
        , name             = String    ()
        , description      = String    ()
        )
    rc_suitability.setkey ("name")

    rc_brand = Class \
        ( db, ''"rc_brand"
        , name             = String    ()
        , description      = String    ()
        )
    rc_brand.setkey ("name")

    rc_capability = Class \
        ( db, ''"rc_capability"
        , name             = String    ()
        , description      = String    ()
        )
    rc_capability.setkey ("name")

    rc_product = Class \
        ( db, ''"rc_product"
        , number           = String    ()
        , rc_product_type  = Link      ("rc_product_type", do_journal = 'no')
        , rc_application   = Link      ("rc_application",  do_journal = 'no')
        , rc_substrate     = Link      ("rc_substrate",    do_journal = 'no')
        , rc_suitability   = Link      ("rc_suitability",  do_journal = 'no')
        , rc_brand         = Link      ("rc_brand",        do_journal = 'no')
        , rc_capability    = Multilink ("rc_capability",   do_journal = 'no')
        , substance        = Link      ("substance")
        )
    rc_product.setkey ("number")

# end def init

def security (db, ** kw) :
    classes = \
        [ ("substance",                    ["User"], ["User"])
        , ("ingredient_used_by_substance", ["User"], ["User"])
        , ("rc_product_type",              ["User"], ["User"])
        , ("rc_application",               ["User"], ["User"])
        , ("rc_substrate",                 ["User"], ["User"])
        , ("rc_suitability",               ["User"], ["User"])
        , ("rc_brand",                     ["User"], ["User"])
        , ("rc_capability",                ["User"], ["User"])
        , ("rc_product",                   ["User"], [])
        ]
    schemadef.register_class_permissions (db, classes, [])
    # Allow creation but not modification
    db.security.addPermissionToRole ('User', 'Create', 'rc_product')
# end def security
