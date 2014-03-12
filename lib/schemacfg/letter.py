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
#    letter
#
# Purpose
#    Schema definitions for letter

from schemacfg import schemadef

def init \
    ( db
    , Class
    , Min_Issue_Class
    , Boolean
    , Date
    , Link
    , Multilink
    , Number
    , String
    , ** kw
    ) :
    export   = {}

    class Letter_Class (Min_Issue_Class) :
        """ Create letter class with default attributes, may be
            extended by other definitions.
            The file types are either PDF (from old imported data) or an
            OpenOffice.org document which is cusomized using info
            pointed to with invoice and/or address.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( subject             = String    ()
                , address             = Link      ("address")
                , date                = Date      ()
                )
            self.__super.__init__ (db, classname, ** properties)
            self.setlabelprop ('subject')
        # end def __init__
    # end class Letter_Class
    export.update (dict (Letter_Class = Letter_Class))

    tmplate_status = Class \
        ( db, ''"tmplate_status"
        , name                = String    ()
        , order               = Number    ()
        , description         = String    ()
        , use_for_invoice     = Boolean   ()
        , use_for_letter      = Boolean   ()
        )
    tmplate_status.setkey (''"name")

    tmplate = Class \
        ( db, ''"tmplate"
        , name                = String    ()
        # version control, use latest:
        , files               = Multilink ("file", do_journal='no')
        , tmplate_status      = Link      ("tmplate_status")
        )
    tmplate.setkey (''"name")

    return export
# end def init

def security (db, ** kw) :
    roles = \
        [ ("Letter"        , "Allowed to add/change templates and letters")
        ]

    classes = \
        [ ("tmplate"           , ["User"],                    ["Letter"])
        , ("tmplate_status"    , ["User"],                    [])
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, [])
# end def security
