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

from roundup import roundupdb, hyperdb, date
from roundup.exceptions import Reject

def add_milestones (db, cl, nodeid, new_values) :
    milestones = \
        [ ("M0"  , "+     0d", "Release Planning has started")
        , ("M50" , "+ 1m 20d", "Release Planning ready for start of Design")
        , ("M100", "+ 2m 15d", "Release Planning completed, Feature Freeze")
        , ("M150", "+ 3m"    , "Design ready for start of Implementation")
        , ("M200", "+ 3m 20d", "Desgin completed")
        , ("M250", "+ 4m 20d", "Implementation ready for start of "
                               "Integration Test")
        , ("M300", "+ 6m 20d", "Implementation completed")
        , ("M310", "+ 7m"    , "TC Spec & TC Implementation completed")
        , ("M350", "+ 7m 15d", "Integration Test ready for start of Test by "
                               "Services; Alpha Release")
        , ("M400", "+ 8m 15d", "Integration Test completed; Beta Release")
        , ("M500", "+ 9m 10d", "Test by Services completed; Production Release")
        , ("M600", "+10m"    , "Shipment completed")
        ]
    order  = 1
    ms_ids = []
    today  = date.Date (".").pretty (format="%Y-%m-%d")
    today  = date.Date (today) # to start today at 00:00 and not somewhere in
                               # the day
    for name, interval, desc in milestones :
        planned = today + date.Interval (interval)
        ms = db.milestone.create ( name        = name
                                 , description = desc
                                 , order       = order
                                 , planned     = planned
                                 , release     = nodeid
                                 )
        ms_ids.append (ms)
        order += 1
    new_values ["milestones"] = ms_ids
    # set status to M0
    new_values ["status"] = ms_ids [0]
# end def add_milestones

def update_milestones (db, cl, nodeid, old_values) :
    """update the 'release' property of the attached milestones
    """
    mss = cl.get (nodeid, "milestones")
    print mss
    for ms in mss :
        db.milestone.set (ms, release = nodeid)
# end def update_milestones

def update_release_status (db, cl, nodeid, old_values) :
    """link the release's status field to the last reached milestone.
    """
    release_id = cl.get         (nodeid, "release")
    milestones = db.release.get (release_id, "milestones")
    milestones.reverse ()
    last = milestones.pop (0)
    for ms in milestones :
        reached = cl.get (ms, "reached")
        if reached :
            last = ms
        else :
            break
    db.release.set (release_id, status = last)
# end def update_release_status

def backlink_documents (db, cl, nodeid, oldvalues) :
    """reactor on release:
    when the contents of the "documents" property chenges, the newly attached
    docuemnts get their "release" property set correctly.
    """
    old_docs = oldvalues.get ("documents", [])
    new_docs = db.release.get (nodeid, "documents")
    print old_docs
    print new_docs
    if new_docs != old_docs and new_docs != [] :
        new_docs = [d for d in new_docs if d not in old_docs]
        for d in new_docs :
            db.document.set (d, release = nodeid)
# end def backlink_documents

def init (db) :
    db.release.audit   ("create", add_milestones)
    db.release.react   ("create", update_milestones)
    db.release.react   ("set"   , backlink_documents)
    db.milestone.react ("set"   , update_release_status)
# end def init

### __END__ release


