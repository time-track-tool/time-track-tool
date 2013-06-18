# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-13 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    company
#
# Purpose
#    Schema definitions for a company.
#
#--
#

from roundup.hyperdb import Class
from schemacfg       import schemadef


def init \
    ( db
    , Class
    , Ext_Class
    , String
    , Password
    , Date
    , Link
    , Multilink
    , Boolean
    , Number
    , ** kw
    ) :
    export = {}
    class Department_Class (Ext_Class) :
        """ create a department class with some default attributes
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( name                  = String    ()
                , description           = String    ()
                , manager               = Link      ("user")
                , part_of               = Link      ("department")
                , valid_from            = Date      ()
                , valid_to              = Date      ()
                , messages              = Multilink ("msg")
                )
            Ext_Class.__init__ (self, db, classname, ** properties)
            self.setkey ('name')
        # end def __init__
    # end class Department_Class
    export.update (dict (Department_Class = Department_Class))

    class Location_Class (Ext_Class) :
        """ create a department class with some default attributes
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( name                  = String    ()
                , address               = String    ()
                , country               = String    ()
                , domain_part           = String    ()
                )
            Ext_Class.__init__ (self, db, classname, ** properties)
            self.setkey ('name')
        # end def __init__
    # end class Location_Class
    export.update (dict (Location_Class = Location_Class))

    class Org_Location_Class (Ext_Class) :
        """ create a org_location class with some default attributes
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( name                  = String    ()
                , phone                 = String    ()
                , organisation          = Link      ("organisation")
                , location              = Link      ("location")
                )
            Ext_Class.__init__ (self, db, classname, ** properties)
            self.setkey ('name')
        # end def __init__
    # end class Org_Location_Class
    export.update (dict (Org_Location_Class = Org_Location_Class))

    class Organisation_Class (Ext_Class) :
        """ create a organisation class with some default attributes
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( name                  = String    ()
                , description           = String    ()
                # get automatically appended to the users mail address
                # upon creation of a new user.
                , mail_domain           = String    ()
                , valid_from            = Date      ()
                , valid_to              = Date      ()
                , messages              = Multilink ("msg")
                )
            Ext_Class.__init__ (self, db, classname, ** properties)
            self.setkey ('name')
        # end def __init__
    # end class Organisation_Class
    export.update (dict (Organisation_Class = Organisation_Class))

    User_Ancestor = kw.get ('User_Class', Ext_Class)
    class User_Class (User_Ancestor) :
        """ create the user class with some default attributes
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( firstname              = String    ()
                , lastname               = String    ()
                , supervisor             = Link      ("user")
                , substitute             = Link      ("user")
                , subst_active           = Boolean   ()
                , clearance_by           = Link      ("user")
                , room                   = Link      ("room")
                , title                  = String    ()
                , position               = Link      ("position")
                , job_description        = String    ()
                , pictures               = Multilink ("file")
                , lunch_start            = String    ()
                , lunch_duration         = Number    ()
                , tt_lines               = Number    ()
                , sex                    = Link      ("sex")
                , org_location           = Link      ("org_location")
                , department             = Link      ("department")
                )
            User_Ancestor.__init__ (self, db, classname, ** properties)
            self.setkey ('username')
        # end def __init__
    # end class User_Class
    export.update (dict (User_Class = User_Class))

    position = Class \
        ( db
        , ''"position"
        , position              = String    ()
        )
    position.setkey ("position")

    class Room_Class (Ext_Class) :
        """ Create room class with default attributes, may be
            extended by other definitions.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( name                = String    ()
                , location            = Link      ("location")
                )
            self.__super.__init__ (db, classname, ** properties)
            self.setkey (''"name")
        # end def __init__
    # end class Room_Class
    export.update (dict (Room_Class = Room_Class))

    sex = Class \
        ( db
        , ''"sex"
        , name                  = String    ()
        )
    sex.setkey ("name")

    return export
# end def init

def security (db, ** kw) :
    """ See the configuration and customisation document for information
        about security setup. Assign the access and edit Permissions for
        issue, file and message to regular users now
    """

    roles = \
        [ ("HR",              "Human Resources team")
        , ("HR-Org-Location", "Human Resources team in this Org-Location")
        , ("Controlling",     "Controlling")
        , ("Office",          "Member of Office")
        ]

    #     classname        allowed to view   /  edit

    classes = \
        [ ("department",   ["User"],  ["Controlling"])
        , ("location",     ["User"],  ["HR"])
        , ("organisation", ["User"],  ["HR", "Controlling"])
        , ("org_location", ["User"],  ["HR"])
        , ("position",     ["User"],  ["HR"])
        , ("room",         ["User"],  ["HR", "Office"])
        , ("sex",          ["User"],  [])
    #   , ("user", See below -- individual fields)
        ]

    prop_perms = \
        [ ( "user", "View", ["Controlling"], ("roles",))
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

    # HR should be able to create new users:
    db.security.addPermissionToRole ("HR", "Create", "user")

# end def security
