#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2013 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    callerid
#
# Purpose
#    Extend Contact_Class with callerid dialling information for asterisk

from schemacfg import schemadef

def init (db, Class, Contact_Type_Class, Boolean, Link, String, ** kw) :
    export   = {}

    class CI_Contact_Type_Class (Contact_Type_Class) :
        """ Add callerid attribute (direct inbound dial) number
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( use_callerid        = Boolean   ()
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class CI_Contact_Type_Class
    export.update (dict (Contact_Type_Class = CI_Contact_Type_Class))

    callerid = Class \
        ( db, ''"callerid"
        , number   = String ()
        , contact  = Link   ("contact")
        )
    callerid.setkey (''"number") 

    return export
# end def init

def security (db, ** kw) :
    classes = \
        [ ("callerid", ["User"], [])
        ]
    schemadef.register_class_permissions (db, classes, [])
# end def security
