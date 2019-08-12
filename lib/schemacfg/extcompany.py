# -*- coding: iso-8859-1 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    external_company
#
# Purpose
#    Schema definitions for an external company for access control.
#
#--
#

from roundup.hyperdb import Class
from schemacfg       import schemadef


def init (db, Class, String, Link, Multilink, ** kw) :

    export = {}

    external_company = Class \
        ( db
        , ''"external_company"
        , name                  = String    ()
        )
    external_company.setkey ("name")

    class User_Class (kw ['User_Class']) :
        """ add some default attributes to User_Class
        """
        def __init__ (self, db, classname, ** properties) :
            ancestor = kw ['User_Class']
            self.update_properties \
                ( external_company      = Link      ("external_company")
                )
            ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Class
    export.update (dict (User_Class = User_Class))

    class EC_Optional_Doc_Issue_Class (kw ['Optional_Doc_Issue_Class']) :
        """ extends the normal Optional_Doc_Issue_Class with external_company
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( external_company = Multilink ("external_company")
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class EC_Optional_Doc_Issue_Class
    export ['Optional_Doc_Issue_Class'] = EC_Optional_Doc_Issue_Class

    return export
# end def init

def security (db, ** kw) :
    """ See the configuration and customisation document for information
        about security setup.
    """

    roles = \
        [ ("HR",        "Human Resources team")
        , ("External",  "External user with less access")
        , ("IT",        "IT-Department")
        ]

    #     classname        allowed to view   /  edit

    classes = \
        [ ("external_company",   ["User"],  ["HR", "IT"])
        ]

    prop_perms = \
        [ ( "user", "Edit", ["HR", "IT"], ("external_company",))
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

    def own_ext_company (db, userid, itemid) :
        ''"Users are allowed to access their own external company"
        return itemid == db.user.get (userid, 'external_company')
    # end def own_ext_company

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'external_company'
        , check       = own_ext_company
        , description = own_ext_company.__doc__
        )
    db.security.addPermissionToRole ('External', p)

# end def security
