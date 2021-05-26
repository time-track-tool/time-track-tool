#! /usr/bin/python
# Copyright (C) 2021 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    currency
#
# Purpose
#    Schema definitions for money currency

from schemacfg       import schemadef

def init (db, Ext_Class, String, Boolean, Number, ** kw) :

    export   = {}

    class Currency_Class (Ext_Class) :
        """ Create a currency class that can be extended in later
            definitions. The exchange_rate is relative to the
            key_currency, only one of the currencies is the
            key_currency.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( name                = String    ()
                , description         = String    ()
                , order               = Number    ()
                , exchange_rate       = Number    ()
                , key_currency        = Boolean   ()
                )
            self.__super.__init__ (db, classname, ** properties)
            self.setkey (''"name")
        # end def __init__
    # end class Invoice_Class
    export.update (dict (Currency_Class = Currency_Class))

    return export
# end def init
