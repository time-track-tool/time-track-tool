#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    hamlog
#
# Purpose
#    Schema definitions for Ham radio logging

from roundup.hyperdb import Class
from schemacfg       import schemadef

def init \
    ( db
    , Class
    , String
    , Date
    , Link
    , Multilink
    , Boolean
    , Number
    , Min_Issue_Class
    , Nosy_Issue_Class
    , Address_Class
    , Letter_Class
    , ** kw
    ) :

    export   = {}

    ham_mode = Class \
        ( db, ''"ham_mode"
        , name                  = String    ()
        )
    ham_mode.setkey (''"name")

    ham_band = Class \
        ( db, ''"ham_band"
        , name                  = String    ()
        )
    ham_band.setkey (''"name")

    qso = Class \
        ( db, ''"qso"
        , freq                  = String    (indexme = "no")
        , call                  = String    ()
        , mode                  = Link      ("ham_mode", do_journal = "no")
        , name                  = String    ()
        , qso_start             = Date      ()
        , qso_end               = Date      ()
        , rst_rcvd              = String    (indexme = "no")
        , rst_sent              = String    (indexme = "no")
        , band                  = Link      ("ham_band", do_journal = "no")
        , qth                   = String    ()
        , gridsquare            = String    ()
        , messages              = Multilink ("msg")
        )

    return export
# end def init


def security (db, ** kw) :

    classes = \
        [ ("ham_mode",   ["User"],    ["User"])
        , ("ham_band",   ["User"],    ["User"])
        , ("qso",        ["User"],    ["User"])
        ]

    schemadef.register_class_permissions (db, classes, [])
# end def security

