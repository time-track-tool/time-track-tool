# -*- coding: iso-8859-1 -*-
# Copyright (C) 2015 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    kpm
#
# Purpose
#    Additional attributes for KPM sync for issue tracker
#
#--
#

from schemacfg import schemadef

def init \
    ( db
    , Class
    , Ext_Mixin
    , String
    , Date
    , Link
    , Multilink
    , Number
    , Boolean
    , ** kw
    ) :

    export = {}

    kpm = Class \
        ( db, "kpm"
        , issue               = Link      ("issue")
        , analysis            = Link      ("msg")
        , description         = Link      ("msg")
        , supplier_answer     = Link      ("msg")
        , kpm_function        = Link      ("kpm_function")
        , reproduceable       = Boolean   ()
        , fault_frequency     = Link      ("fault_frequency")
        , hardware_version    = String    ()
        , ready_for_sync      = Boolean   ()
        , kpm_hw_variant      = Multilink ("kpm_hw_variant")
        , problem_description = Link      ("msg")
        , kpm_occurrence      = Link      ("kpm_occurrence")
        , customer_effect     = Link      ("msg")
        , workaround          = Link      ("msg")
        , problem_solution    = Link      ("msg")
        , safety_relevant     = Boolean   ()
        , kpm_tag             = Multilink ("kpm_tag")
        , planned_correction  = Multilink ("kpm_release")
        , tested_with         = Multilink ("kpm_release")
        )
    kpm.setlabelprop ('kpm_function')

    kpm_function = Class \
        ( db, "kpm_function"
        , name                = String    ()
        , kpm_key             = String    ()
        , kpm_group           = String    ()
        , order               = Number    ()
        )
    kpm_function.setkey ('kpm_key')

    fault_frequency = Class \
        ( db, "fault_frequency"
        , name                = String    ()
        , order               = Number    ()
        )
    fault_frequency.setkey ('name')

    kpm_hw_variant = Class \
        ( db, "kpm_hw_variant"
        , name                = String    ()
        , order               = Number    ()
        )
    kpm_hw_variant.setkey ('name')

    kpm_occurrence = Class \
        ( db, "kpm_occurrence"
        , name                = String    ()
        , order               = Number    ()
        )
    kpm_occurrence.setkey ('name')

    kpm_tag = Class \
        ( db, "kpm_tag"
        , name                = String    ()
        , order               = Number    ()
        , valid               = Boolean   ()
        )
    kpm_tag.setkey ('name')

    kpm_release = Class \
        ( db, "kpm_release"
        , name                = String    ()
        , order               = Number    ()
        , valid               = Boolean   ()
        )
    kpm_release.setkey ('name')

    return export

# end def init

def security (db, ** kw) :
    roles = \
        [ ("KPM-Admin", "Admin for KPM multiselect fields")
        ]
    #     classname             allowed to view   /  edit
    classes = \
        [ ("fault_frequency",    ["User"], [])
        , ("kpm_function",       ["User"], ["KPM-Admin"])
        , ("kpm_hw_variant",     ["User"], ["KPM-Admin"])
        , ("kpm_occurrence",     ["User"], ["KPM-Admin"])
        , ("kpm_release",        ["User"], ["KPM-Admin"])
        , ("kpm_tag",            ["User"], ["KPM-Admin"])
        , ("kpm",                ["User"], ["User"])
        ]
    prop_perms = []

    schemadef.register_roles                 (db, roles)
    schemadef.register_class_permissions     (db, classes, prop_perms)
# end def security
