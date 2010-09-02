#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007-10 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    adr_ext
#
# Purpose
#    Schema definitions for extended address

import schemadef

def init (db, Person_Class, Date, ** kw) :
    export   = {}

    class Ext_Person_Class (Person_Class) :
        """ Create person class with additional default attributes from
            standard Person Class.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( birthdate           = Date      ()
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class Ext_Person_Class

    export ['Person_Class'] = Ext_Person_Class
    return export
# end def init
