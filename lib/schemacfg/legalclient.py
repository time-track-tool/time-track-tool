# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    legalclient
#
# Purpose
#    Schema definitions for a simple client database
#
#--
#

from roundup.hyperdb import Class
from schemacfg       import schemadef

def init (db, Class, String, Date, Link, Multilink, Number, ** kw) :
    client = Class \
        ( db
        , ''"legalclient"
        , lastname              = String    ()
        , firstname             = String    ()
        , born                  = Date      ()
        , first_date            = Date      ()
        , last_date             = Date      ()
        , messages              = Multilink ("msg")
        )
    client.setlabelprop ("lastname")

# end def init

def security (db, ** kw) :
    #     classname        allowed to view   /  edit
    classes = [("legalclient", ["User"], ["User"])]
    schemadef.register_class_permissions (db, classes, [])
# end def security
