# -*- coding: iso-8859-1 -*-
# Copyright (C) 2015 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    org_min
#
# Purpose
#    Schema definitions minimal organisation info
#
#--
#

from schemacfg       import schemadef

def init (db, Ext_Class, Link, Boolean, String, ** kw) :
    export = {}

    User_Ancestor = kw.get ('User_Class', Ext_Class)
    class User_Class (User_Ancestor) :
        """ create the user class with some default attributes
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( supervisor             = Link      ("user")
                , substitute             = Link      ("user")
                , clearance_by           = Link      ("user")
                )
            User_Ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Class
    export.update (dict (User_Class = User_Class))

    Dep_Ancestor = kw ['Department_Class']
    class Department_Class (Dep_Ancestor) :
        """ Add some attributes to department """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( manager               = Link      ("user")
                , deputy                = Link      ("user")
                )
            Dep_Ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Department_Class
    export.update (dict (Department_Class = Department_Class))

    Org_Ancestor = kw ['Organisation_Class']
    class Organisation_Class (Org_Ancestor) :
        """ Add some attributes to organisation """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( may_purchase          = Boolean   ()
                , company_code          = String    ()
                )
            Org_Ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Organisation_Class
    export.update (dict (Organisation_Class = Organisation_Class))

    return export
# end def init
