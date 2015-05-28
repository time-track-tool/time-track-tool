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

    class Organisation_Class (Ext_Class) :
        """ create a organisation class with some default attributes
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( name                  = String    ()
                , description           = String    ()
                , valid_from            = Date      ()
                , valid_to              = Date      ()
                )
            Ext_Class.__init__ (self, db, classname, ** properties)
            self.setkey ('name')
        # end def __init__
    # end class Organisation_Class
    export.update (dict (Organisation_Class = Organisation_Class))

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
                )
            Ext_Class.__init__ (self, db, classname, ** properties)
            self.setkey ('name')
        # end def __init__
    # end class Department_Class
    export.update (dict (Department_Class = Department_Class))

    User_Ancestor = kw.get ('User_Class', Ext_Class)
    class User_Class (User_Ancestor) :
        """ create the user class with some default attributes
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( department             = Link      ("department")
                )
            User_Ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Class
    export.update (dict (User_Class = User_Class))

    return export
# end def init

def security (db, ** kw) :
    """ See the configuration and customisation document for information
        about security setup. Assign the access and edit Permissions for
        issue, file and message to regular users now
    """

    roles = \
        [ ("Controlling",     "Controlling")
        ]

    #     classname        allowed to view   /  edit

    classes = \
        [ ("organisation", ["User"],  ["Controlling"])
        ]

    prop_perms = []

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

# end def security
