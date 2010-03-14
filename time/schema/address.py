#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-10 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    address
#
# Purpose
#    Schema definitions for address and other contact information

from roundup.hyperdb import Class
import schemadef

def init \
    ( db
    , Class
    , Ext_Class
    , Min_Issue_Class
    , String
    , Date
    , Link
    , Multilink
    , Boolean
    , Number
    , ** kw
    ) :

    do_index = "yes"
    export   = {}

    class Address_Class (Min_Issue_Class) :
        """ Create address class with default attributes, may be
            extended by other definitions.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( street              = String    (indexme = do_index)
                , country             = String    (indexme = "no")
                , postalcode          = String    (indexme = "no")
                , city                = String    (indexme = do_index)
                , adr_type            = Multilink ("adr_type")
                , valid               = Link      ("valid")
                , lookalike_city      = String    (indexme = do_index)
                , lookalike_street    = String    (indexme = do_index)
                )
            self.__super.__init__ (db, classname, ** properties)
            self.setlabelprop ('country')
        # end def __init__
    # end class Address_Class
    export.update (dict (Address_Class = Address_Class))

    adr_type = Class \
        ( db, ''"adr_type"
        , code                = String    ()
        , description         = String    ()
        , typecat             = Link      ("adr_type_cat")
        )
    adr_type.setkey ("code")

    adr_type_cat = Class \
        ( db, ''"adr_type_cat"
        , code                = String    ()
        , description         = String    ()
        , type_valid          = Boolean   ()
        )
    adr_type_cat.setkey (''"code")

    # Define codes for (in)valid addresses, e.g., "verstorben"
    valid = Class \
        ( db, ''"valid"
        , name                = String    ()
        , description         = String    ()
        )
    valid.setkey (''"name")

    return export
# end def init

def security (db, ** kw) :
    roles = \
        [ ("Type"          , "Allowed to add/change type codes")
        , ("Contact"       , "Allowed to add/change address data")
        , ("Adr_Readonly"  , "Allowed to read address and contact data")
        ]

    classes = \
        [ ("adr_type"          , ["User", "Adr_Readonly"],    ["Type"])
        , ("adr_type_cat"      , ["User", "Adr_Readonly"],    ["Type"])
        , ("valid"             , ["User", "Adr_Readonly"],    [])
        , ("address"           , ["Adr_Readonly"],            [])
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, [])
    db.security.addPermissionToRole ('Adr_Readonly', 'Web Access')
# end def security
