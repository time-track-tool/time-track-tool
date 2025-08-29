#! /usr/bin/python
# Copyright (C) 2010-25 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    person_cust
#
# Purpose
#    Schema definitions for extending customer with person attributes

def init (db, Address_Class, Contact_Class, Contact_Type_Class, Link, ** kw) :
    export   = {}

    contact = Contact_Class \
        ( db, ''"contact"
        , customer            = Link      ( 'customer'
                                          , rev_multilink = 'contacts'
                                          )
        , contact_type        = Link      ("contact_type")
        )
    contact_type = Contact_Type_Class (db, ''"contact_type")

    export ['Person_Class'] = Address_Class
    return export
# end def init
