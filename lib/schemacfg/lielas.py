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
from schemacfg       import schemadef

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
        , tty                 = String    ()
        , name                = String    ()
        , sint                = Number    ()
        , sint_pending        = Boolean   ()
        , mint                = Number    ()
        , mint_pending        = Boolean   ()
        )
    transceiver.setkey (''"name")

    device_group = Class \
        ( db, ''"device_group"
        , name                = String    ()
        , description         = String    ()
        , order               = Number    ()
        )
    device_group.setlabelprop (''"name")

    device = Class \
        ( db, ''"device"
        , transceiver         = Link      ("transceiver")
        , adr                 = String    ()
        , dev                 = String    ()
        , cls                 = String    ()
        , name                = String    ()
        , surrogate           = String    ()
        , device_group        = Link      ("device_group")
        , sint                = Number    ()
        , sint_pending        = Boolean   ()
        , mint                = Number    ()
        , mint_pending        = Boolean   ()
        , gapint              = Number    ()
        , rec                 = Link      ("logstyle")
        , version             = String    ()
        , order               = Number    ()
        )
    device.setkey       (''"surrogate")
    device.setorderprop (''"surrogate")

    sensor = Class \
        ( db, ''"sensor"
        , device              = Link      ("device")
        , adr                 = String    ()
        , type                = String    ()
        , name                = String    ()
        , surrogate           = String    ()
        , almin               = Number    ()
        , almax               = Number    ()
        , unit                = String    ()
        , do_logging          = Boolean   ()
        , is_actuator         = Boolean   ()
        , is_app_sensor       = Boolean   ()
        , order               = Number    ()
        )
    sensor.setkey       (''"surrogate")
    sensor.setorderprop (''"surrogate")

    logstyle = Class \
        ( db, ''"logstyle"
        , name                = String    ()
        , description         = String    ()
        , order               = Number    ()
        )
    logstyle.setkey (''"name")

    measurement = Class \
        ( db, ''"measurement"
        , sensor              = Link      ("sensor", do_journal = "no")
        , val                 = Number    ()
        , date                = Date      ()
        )

    alarm = Class \
        ( db, ''"alarm"
        , sensor              = Link      ("sensor", do_journal = "no")
        , val                 = Number    ()
        , last_triggered      = Date      ()
        , timeout             = Number    ()
        , is_lower            = Boolean   ()
        )

# end def init

def security (db, ** kw) :
    roles = \
        [ ("Guest",  "Allowed to view everything")
        , ("Logger", "Allowed to add and change measurements")
        ]

    classes = \
        [ ("device",       ["User", "Guest", "Logger"], ["Logger"])
        , ("device_group", ["User", "Guest", "Logger"], ["User"])
        , ("logstyle",     ["User", "Guest", "Logger"], [])
        , ("measurement",  ["User", "Guest", "Logger"], ["Logger"])
        , ("sensor",       ["User", "Guest", "Logger"], ["Logger"])
        , ("transceiver",  ["User", "Guest", "Logger"], ["Logger"])
        , ("alarm",        ["User", "Guest", "Logger"], ["User", "Logger"])
        ]

    prop_perms = \
        [ ( "device",      "Edit", ["User"]
          , ( "name", "sint", "mint", "gapint", "rec", "device_group"
            , "mint_pending", "sint_pending"
            )
          )
        , ( "sensor",      "Edit", ["User"]
          , ("almin", "almax", "do_logging"
            )
          )
        , ( "transceiver", "Edit", ["User"]
          , ("name", "tty", "sint", "mint", "mint_pending", "sint_pending")
          )
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)
# end def security
