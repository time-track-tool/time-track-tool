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
#    user_contact
#
# Purpose
#    Schema definitions for optional user_contact

def init (db, Address_Class, Contact_Class, Contact_Type_Class, Link, ** kw) :
    export   = {}

    params = {}
    if 'room' in db.classes :
        params ['room'] = Link ('room')
    contact = Contact_Class \
        ( db, ''"contact"
        , user                = Link      ('user')
        , contact_type        = Link      ("uc_type")
        , **params
        )
    uc_type = Contact_Type_Class (db, ''"uc_type")

    return export
# end def init
