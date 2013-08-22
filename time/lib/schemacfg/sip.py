#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2013 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    sip
#
# Purpose
#    Schema definitions for sip device

from schemacfg import schemadef

def init (db, Class, Link, String, ** kw) :
    export   = {}

    sip_device = Class \
        ( db, ''"sip_device"
        , name                = String    ()
        , mac_address         = String    ()
        , http_username       = String    ()
        , http_password       = String    ()
        , pbx_username        = String    ()
        , pbx_password        = String    ()
        , pbx_hostname        = String    ()
        )
    sip_device.setkey (''"mac_address")

    class User_Class (kw ['User_Class']) :
        """ add sip_device to user class
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( sip_device             = Link      ("sip_device")
                )
            kw ['User_Class'].__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Class
    export ['User_Class'] = User_Class

    return export
# end def init

def security (db, ** kw) :
    roles = \
        [ ("PBX", "Allowed to edit pbx data")
        ]
    classes = \
        [ ("sip_device", ["PBX"], ["PBX"])
        ]
    prop_perms = \
        [ ("sip_device", "View", ["User"]
          , ("name", "id")
          )
        , ("user",       "View", ["PBX", "User"]
          , ("sip_device",)
          )
        , ("user",       "Edit", ["PBX"]
          , ("sip_device",)
          )
        ]
    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, [])
# end def security
