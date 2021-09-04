#! /usr/bin/python
# Copyright (C) 2012-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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
    , Integer
    , ** kw
    ) :

    export   = {}

    antenna = Class \
        ( db, ''"antenna"
        , name                  = String    ()
        , description           = String    ()
        , order                 = Number    ()
        )
    antenna.setkey (''"name")

    continent = Class \
        ( db, ''"continent"
        , code                  = String    ()
        , name                  = String    ()
        )
    continent.setkey (''"code")

    # Entities may have multiple cq and itu zones but we provide them
    # here only if unique.
    dxcc_entity = Class \
        ( db, ''"dxcc_entity"
        , code                  = String    ()
        , name                  = String    ()
        , continent             = Multilink ("continent")
        , cq_zone               = Integer   ()
        , itu_zone              = Integer   ()
        )
    dxcc_entity.setkey (''"code")
    dxcc_entity.setlabelprop ('name')

    ham_call = Class \
        ( db, ''"ham_call"
        , call                  = String    ()
        , name                  = String    ()
        , qth                   = String    ()
        , gridsquare            = String    ()
        , iota                  = String    ()
        , eqsl_nickname         = String    ()
        , cq_zone               = Integer   ()
        , itu_zone              = Integer   ()
        , owner                 = Link      ("user", rev_multilink = 'call')
        , cardname              = String    ()
        )
    ham_call.setkey (''"name")

    ham_mode = Class \
        ( db, ''"ham_mode"
        , name                  = String    ()
        , order                 = Number    ()
        , adif_mode             = String    ()
        , adif_submode          = String    ()
        )
    ham_mode.setkey (''"name")

    ham_band = Class \
        ( db, ''"ham_band"
        , name                  = String    ()
        , order                 = Number    ()
        )
    ham_band.setkey (''"name")

    qsl_type = Class \
        ( db, ''"qsl_type"
        , name                  = String    ()
        , order                 = Number    ()
        , code                  = Number    ()
        )
    qsl_type.setkey (''"name")

    qsl_status = Class \
        ( db, ''"qsl_status"
        , name                  = String    ()
        , code                  = Number    ()
        )
    qsl_status.setkey       (''"name")
    qsl_status.setorderprop (''"code")

    qsl = Class \
        ( db, ''"qsl"
        , qsl_type              = Link      ("qsl_type", do_journal = "no")
        , qso                   = Link      ("qso")
        , date_recv             = Date      ()
        , date_sent             = Date      ()
        )

    qso = Class \
        ( db, ''"qso"
        , freq                  = String    (indexme = "no")
        , tx_pwr                = String    ()
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
        , country               = String    ()
        , state                 = String    ()
        , owner                 = Link      ("ham_call", do_journal = "no")
        , messages              = Multilink ("msg")
        , antenna               = Link      ("antenna",  do_journal = "no")
        , swl                   = Link      ("qso")
        , qsl_via               = String    ()
        , qso2                  = Link      ("qso")
        , wont_qsl_via          = Multilink ("qsl_type",   do_journal = "no")
        , qsl_r_status          = Link      ("qsl_status", do_journal = "no")
        , qsl_s_status          = Link      ("qsl_status", do_journal = "no")
        , no_qsl_status         = Link      ("qsl_status", do_journal = "no")
        , reject                = Boolean   ()
        , cq_zone               = Integer   ()
        , itu_zone              = Integer   ()
        , iota                  = String    ()
        , german_dok            = String    ()
        , dxcc_entity           = Link      ("dxcc_entity")
        , remarks               = String    ()
        )
    qso.setlabelprop ('call')

    return export
# end def init


def security (db, ** kw) :

    roles = [('Nosy', 'Nosy list')]
    classes = \
        [ ("ham_call",    ["User"],    ["User"])
        , ("ham_mode",    ["User"],    ["User"])
        , ("ham_band",    ["User"],    ["User"])
        , ("qsl_type",    ["User"],    ["User"])
        , ("qsl_status",  ["User"],    ["User"])
        , ("antenna",     ["User"],    ["User"])
        , ("continent",   ["User"],    ["User"])
        , ("dxcc_entity", ["User"],    ["User"])
        , ("qsl",         ["User"],    ["User"])
        , ("qso",         ["User"],    ["User"])
        , ("user",        ["User"],    ["Admin"])
        ]
    prop_perms = \
        [ ( "user", "View", ["User"], ("call",))
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)
# end def security

