#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
    , String
    , Date
    , Link
    , Multilink
    , Boolean
    , Number
    , ** kw
    ) :

    do_index = "no"
    export   = {}

    class Address_Class (Ext_Class) :
        """ Create address class with default attributes, may be
            extended by other definitions.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( title               = String    ()
                , lettertitle         = String    ()
                , firstname           = String    (indexme = do_index)
                , initial             = String    ()
                , lastname            = String    (indexme = do_index)
                , function            = String    (indexme = do_index)
                , street              = String    (indexme = do_index)
                , country             = String    ()
                , postalcode          = String    ()
                , city                = String    (indexme = do_index)
                , phone               = String    ()
                , fax                 = String    ()
                , salutation          = String    ()
                , messages            = Multilink ("msg")
                , email               = String    (indexme = do_index)
                , adr_type            = Multilink ("adr_type")
                , valid               = Link      ("valid")
                , letters             = Multilink ("letter")
                , lookalike_name      = String    (indexme = do_index)
                )
            self.__super.__init__ (db, classname, ** properties)
            self.setlabelprop ('lastname')
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
        )
    adr_type_cat.setkey (''"code")

    class Letter_Class (Ext_Class) :
        """ Create letter class with default attributes, may be
            extended by other definitions.
            The file types are either PDF (from old imported data) or an
            OpenOffice.org document which is cusomized using info
            pointed to with invoice and/or address.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( subject             = String    ()
                , address             = Link      ("address")
                , date                = Date      ()
                , files               = Multilink ("file", do_journal='no')
                , messages            = Multilink ("msg")
                )
            self.__super.__init__ (db, classname, ** properties)
            self.setlabelprop ('subject')
        # end def __init__
    # end class Letter_Class
    export.update (dict (Letter_Class = Letter_Class))

    tmplate = Class \
        ( db, ''"tmplate"
        , name                = String    ()
        # version control, use latest:
        , files               = Multilink ("file", do_journal='no')
        )
    tmplate.setkey (''"name")

    # Define codes for (in)valid addresses, e.g., "verstorben"
    valid = Class \
        ( db, ''"valid"
        , name                = String    ()
        , description         = String    ()
        )
    valid.setkey (''"name")

    contact_type = Class \
        ( db, ''"contact_type"
        , name                = String    ()
        , description         = String    ()
        , url_template        = String    ()
        )
    contact_type.setkey (''"name")

    contact = Class \
        ( db, ''"contact"
        , contact             = String    ()
        , description         = String    ()
        , contact_type        = Link      ("contact_type")
        , address             = Link      ("address")
        )

    return export
# end def init


def security (db, ** kw) :
    roles = \
        [ ("Type"          , "Allowed to add/change type codes")
        , ("Letter"        , "Allowed to add/change templates and letters")
        ]

    classes = \
        [ ("address"           , ["User"],    ["User"])
        , ("adr_type"          , ["User"],    ["Type"])
        , ("adr_type_cat"      , ["User"],    ["Type"])
        , ("letter"            , ["User"],    ["Letter"])
        , ("tmplate"           , ["User"],    ["Letter"])
        , ("valid"             , ["User"],    ["Admin"])
        , ("contact_type"      , ["User"],    ["Admin"])
        , ("contact"           , ["User"],    ["User"])
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, [])
# end def security
