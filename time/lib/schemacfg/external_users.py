# -*- coding: iso-8859-1 -*-
# Copyright (C) 2013 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    external_users
#
# Purpose
#    Schema definitions for list of external users in issue for access control.
#
#--
#

from roundup.hyperdb import Class
from schemacfg       import schemadef


def init (db, Class, Boolean, String, Link, Multilink, ** kw) :

    export = {}

    class EC_Optional_Doc_Issue_Class (kw ['Optional_Doc_Issue_Class']) :
        """ extends the normal Optional_Doc_Issue_Class with external_users
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( external_users   = Multilink ("user")
                , inherit_ext      = Boolean   ()
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class EC_Optional_Doc_Issue_Class
    export ['Optional_Doc_Issue_Class'] = EC_Optional_Doc_Issue_Class

    return export
# end def init

# security defs see extuser module
