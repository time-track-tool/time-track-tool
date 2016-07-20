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
#    issue
#
# Purpose
#    Schema definitions for issue tracker derived from gnats
#
#--
#

from schemacfg       import schemadef

def init (db, String, ** kw) :
    Cls = kw ['Msg_Class']
    class Msg_Class (Cls) :
        """ extends the normal FileClass with some attributes for message
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( header      = String    (indexme = 'no')
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class Msg_Class
    return dict (Msg_Class = Msg_Class)
# end def init
