# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@mexx.mobile
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
#
#++
# Name
#    release
#
# Purpose
#    Detectors for the 'release' class
#
# Revision Dates
#    22-Jul-2004 (MPH) Creation
#    ««revision-date»»···
#--
#

from roundup import roundupdb, hyperdb
from roundup.exceptions import Reject

def add_milestones (db, cl, nodeid, new_values) :
    milestones = \
        [ ("M0"  , "Release Planning has started")
        , ("M50" , "Release Planning ready for start of Design")
        , ("M100", "Release Planning completed, Feature Freeze")
        , ("M150", "Design ready for start of Implementation")
        , ("M200", "Desgin completed")
        , ("M250", "Implementation ready for start of Integration Test")
        , ("M300", "Implementation completed")
        , ("M310", "TC Spec & TC Implementation completed")
        , ("M350", "Integration Test ready for start of Test by Services; "
                   "Alpha Release")
        , ("M400", "Integration Test completed; Beta Release")
        , ("M500", "Test by Services completed; Production Release")
        , ("M600", "Shipment completed")
        ]
    order  = 1
    ms_ids = []
    for name, desc in milestones :
        ms = db.milestone.create ( name        = name
                                 , description = desc
                                 , order       = order
                                 )
        ms_ids.append (ms)
        order += 1
    ms_ids.sort ()
    new_values ["milestones"] = ms_ids
    print new_values
# end def add_milestones

def init (db) :
    db.release.audit ("create", add_milestones)
# end def init

### __END__ release


