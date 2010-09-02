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
#    person
#
# Purpose
#    Schema definitions for person and other contact information

from schemacfg import schemadef

def init (db, Ext_Class, String, Link, Number, ** kw) :
    do_index = "yes"
    export   = {}

    class Contact_Class (Ext_Class) :
        """ Create contact class with default attributes, may be
            extended by other definitions.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( contact             = String    ()
                , description         = String    ()
                , contact_type        = Link      ("contact_type")
                )
            self.__super.__init__ (db, classname, ** properties)
            self.setlabelprop ('contact')
        # end def __init__
    # end class Contact_Class
    export.update (dict (Contact_Class = Contact_Class))

    class Contact_Type_Class (Ext_Class) :
        """ Create contact_type class with default attributes, may be
            extended by other definitions.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( name                = String    ()
                , description         = String    ()
                , url_template        = String    ()
                , order               = Number    ()
                )
            self.__super.__init__ (db, classname, ** properties)
            self.setkey (''"name")
        # end def __init__
    # end class Contact_Type_Class
    export.update (dict (Contact_Type_Class = Contact_Type_Class))

    contact_type = Contact_Type_Class (db, ''"contact_type")

    return export
# end def init

def security (db, ** kw) :
    roles = \
        [ ("Contact"       , "Allowed to add/change address data")
        ]

    classes = \
        [ ("contact_type"      , ["User", "Adr_Readonly"],    [])
        , ("contact"           , ["User", "Adr_Readonly"],    ["Contact"])
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, [])
# end def security
