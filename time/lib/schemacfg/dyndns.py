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
#    dyndns
#
# Purpose
#    Schema definitions for ddclient (dyndns update daemon) configuration

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

    """ Everything here is only editable by Admin """
    dyndns_protocol = Class \
        ( db, ''"dyndns_protocol"
        , name                = String    ()
        , order               = Number    ()
        , default_server      = String    ()
        , description         = String    ()
        )
    dyndns_protocol.setkey (''"name")

    dyndns_service = Class \
        ( db, ''"dyndns_service"
        , dyndns              = Link      ('dyndns')
        , server              = String    ()
        , protocol            = Link      ('dyndns_protocol')
        , login               = String    ()
        , password            = String    ()
        )
    dyndns_service.setlabelprop (''"server")

    dyndns_host = Class \
        ( db, ''"dyndns_host"
        , dyndns_service      = Link      ('dyndns_service')
        , hostname            = String    ()
        , description         = String    ()
        )
    dyndns_host.setkey (''"hostname")

    # currently a singleton -- may be more for different hosts
    dyndns = Class \
        ( db, ''"dyndns"
        , local_hostname      = String    ()
        , syslog              = Boolean   ()
        , interface           = String    ()
        , interface_skip      = String    ()
        , web_url             = String    ()
        , web_skip            = String    ()
        , fw_login            = String    ()
        , fw_password         = String    ()
        , fw_url              = String    ()
        , fw_skip             = String    ()
        )
    dyndns.setkey (''"local_hostname")

# end def init
