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
# Purpose
#    it_issue extension for part_of/composed_of
#
#--
#

from schemacfg       import schemadef

def init \
    ( db
    , Ext_Mixin
    , Link
    , Multilink
    , ** kw
    ) :

    export = {}

    IT_Base = kw ['IT_Issue_Baseclass']
    class IT_Issue_Baseclass (IT_Base) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( part_of             = Link      ('it_issue')
                , composed_of         = Multilink ('it_issue')
                )
            IT_Base.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class IT_Issue_Baseclass
    export ['IT_Issue_Baseclass'] = IT_Issue_Baseclass

    return export
# end def init
