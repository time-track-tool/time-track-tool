#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    release
#
# Purpose
#    Detectors for the 'release' class
#
# Revision Dates
#    22-Jul-2004 (MPH) Creation
#     4-Nov-2004 (MPH) Changed Milestones
#     8-Nov-2004 (MPH) Cleanup
#     9-Nov-2004 (MPH) Removed debug output, fixed `update_release_status`
#    ««revision-date»»···
#--
#

from roundup import roundupdb, hyperdb, date
from roundup.exceptions import Reject

def add_milestones (db, cl, nodeid, new_values) :
    """auditor on release.create

    XXX: not sure if this should be in an auditor ???

    - creates the milestones and attaches them to the newly created release.
    - set release's `status` to M000
    """
    milestones = \
        [ ("M000", "+     0d", "Release Planning has started")
        , ("M100", "+ 2m 15d", "Release Planning completed, Feature Freeze")
        , ("M200", "+ 3m 20d", "Design completed")
        , ("M210", "+ 3m 30d", "Check for Customer Appslications to be "
                               "used as Testcases")
        , ("M300", "+ 6m 20d", "Implementation completed")
        , ("M310", "+ 7m    ", "TC Spec & TC Implementation completed")
        , ("M400", "+ 8m 15d", "Integration Test completed; Beta Release")
        , ("M410", "+ 8m 20d", "Documentation Completed")
        , ("M490", "+ 9m    ", "Bugfixing completed")
        , ("M500", "+ 9m 10d", "Test by Services completed; Production "
                               "Release")
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
    """reactor on release.create

    set the 'release' property of the attached milestones
    """
    mss = cl.get (nodeid, "milestones")
    for ms in mss :
        db.milestone.set (ms, release = nodeid)
# end def update_milestones

def update_release_status (db, cl, nodeid, old_values) :
    """reactor on milestone.set

    link the release's status field to the last reached milestone.
    """
    release_id = cl.get         (nodeid, "release")
    milestones = db.release.get (release_id, "milestones")
    milestones.reverse ()
    last = milestones.pop (0)
    for ms in milestones :
        reached = cl.get (ms, "reached")
        if reached :
            last = ms
            break
    db.release.set (release_id, status = last)
# end def update_release_status

def backlink_documents (db, cl, nodeid, old_values) :
    """reactor on release.set

    when the contents of the `documents` property chenges, the newly attached
    docuemnts get their `release` property set accordingly.
    """
    old_docs = old_values.get ("documents", [])
    new_docs = db.release.get (nodeid, "documents")
    if new_docs != old_docs and new_docs != [] :
        new_docs = [d for d in new_docs if d not in old_docs]
        for d in new_docs :
            db.document.set (d, release = nodeid)
# end def backlink_documents

def init (db) :
    if 'release' not in db.classes :
        return
    db.release.audit   ("create", add_milestones)
    db.release.react   ("create", update_milestones)
    db.release.react   ("set"   , backlink_documents)
    db.milestone.react ("set"   , update_release_status)
# end def init

### __END__ release
