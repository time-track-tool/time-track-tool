#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    min_adr
#
# Purpose
#    Minimal address class without any properties

def init (db, Ext_Class, Multilink, ** kw) :
    export   = {}
    class Address_Class (Ext_Class) :
        """ Create address class with minimum default attributes
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( contacts            = Multilink ("contact")
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class Address_Class

    export ['Address_Class'] = Address_Class
    return export
# end def init
