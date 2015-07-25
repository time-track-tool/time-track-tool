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

    Ext_TC = kw ['Ext_Tracker_Class']
    class Ext_Tracker_Class (Ext_TC) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( is_kpm              = Boolean   ()
                )
            Ext_TC.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Ext_Tracker_Class
    export ['Ext_Tracker_Class'] = Ext_Tracker_Class

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

    return export

# end def init

def security (db, ** kw) :
    #     classname             allowed to view   /  edit
    classes = \
        [ ("fault_frequency",    ["User"], [])
        , ("kpm_function",       ["User"], [])
        , ("kpm",                ["User"], ["User"])
        ]
    prop_perms = []

    schemadef.register_class_permissions     (db, classes, prop_perms)
# end def security
