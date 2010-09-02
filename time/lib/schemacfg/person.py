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
#    Schema definitions for person

import schemadef

def init (db, Ext_Class, Person_Class, String, Link, Multilink, Number, ** kw) :
    do_index = "yes"
    export   = {}

    class E_Person_Class (Person_Class) :
        """ Create person class with default attributes, may be
            extended by other definitions.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( title               = String    (indexme = "no")
                , lettertitle         = String    (indexme = "no")
                , firstname           = String    (indexme = do_index)
                , initial             = String    (indexme = "no")
                , lastname            = String    (indexme = do_index)
                , affix               = String    (indexme = do_index)
                , function            = String    (indexme = do_index)
                , salutation          = String    (indexme = "no")
                , lookalike_lastname  = String    (indexme = do_index)
                , lookalike_firstname = String    (indexme = do_index)
                , lookalike_function  = String    (indexme = do_index)
                , contacts            = Multilink ("contact")
                )
            self.__super.__init__ (db, classname, ** properties)
            self.setlabelprop ('lastname')
        # end def __init__
    # end class Person_Class
    export.update (dict (Person_Class = E_Person_Class))

    return export
# end def init
