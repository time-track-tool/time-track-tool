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
# Dual License:
# If you need a proprietary license that permits you to add your own
# software without the need to publish your source-code under the GNU
# General Public License above, contact
# Reder, Christian Reder, A-2560 Berndorf, Austria, christian@reder.eu
#++
# Name
#    lielas
#
# Purpose
#    Schema definitions for lielas data logger

from roundup.hyperdb import Class
import schemadef

def init \
    ( db
    , Class
    , String
    , Date
    , Link
    , Boolean
    , Number
    , ** kw
    ) :

    transceiver = Class \
        ( db, ''"transceiver"
        , adr                 = String    ()
        , name                = String    ()
        , sint                = Number    ()
        , mint                = Number    ()
        )
    transceiver.setlabelprop (''"name")

    device = Class \
        ( db, ''"device"
        , adr                 = String    ()
        , dev                 = String    ()
        , cls                 = String    ()
        , name                = String    ()
        , sint                = Number    ()
        , mint                = Number    ()
        , gapint              = Number    ()
        , rec                 = Link      ("logstyle")
        , version             = String    ()
        )
    device.setkey (''"adr")
    device.setlabelprop (''"name")

    sensor = Class \
        ( db, ''"sensor"
        , device              = Link      ("device")
        , type                = String    ()
        , name                = String    ()
        , almin               = Number    ()
        , almax               = Number    ()
        , unit                = String    ()
        , do_logging          = Boolean   ()
        , is_actuator         = Boolean   ()
        )
    sensor.setlabelprop (''"name")

    logstyle = Class \
        ( db, ''"logstyle"
        , name                = String    ()
        , description         = String    ()
        , order               = Number    ()
        )
    logstyle.setkey (''"name")

    measurement = Class \
        ( db, ''"measurement"
        , sensor              = Link      ("sensor")
        , val                 = Number    ()
        , date                = Date      ()
        )

# end def init

def security (db, ** kw) :
    roles = \
        [ ("Guest",  "Allowed to view everything")
        , ("Logger", "Allowed to add and change measurements")
        ]

    classes = \
        [ ("device",      ["User", "Guest", "Logger"], ["Logger"])
        , ("logstyle",    ["User", "Guest", "Logger"], [])
        , ("measurement", ["User", "Guest", "Logger"], ["Logger"])
        , ("sensor",      ["User", "Guest", "Logger"], ["Logger"])
        , ("transceiver", ["User", "Guest", "Logger"], ["Logger"])
        ]

    prop_perms = \
        [ ( "device",      "Edit", ["User"]
          , ("name", "sint", "mint", "gapint", "rec")
          )
        , ( "sensor",      "Edit", ["User"]
          , ("name", "type", "almin", "almax", "unit"
            , "do_logging", "is_actuator"
            )
          )
        , ( "transceiver", "Edit", ["User"]
          , ("name", "adr", "sint", "mint")
          )
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, [])
# end def security
