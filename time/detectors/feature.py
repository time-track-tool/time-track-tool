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
#    feature
#
# Purpose
#    Detectors for the 'feature'
#
# Revision Dates
#    23-Jul-2004 (MPH) Creation
#    ««revision-date»»···
#--
#

from roundup import roundupdb, hyperdb
from roundup.exceptions import Reject

def create_defaults (db, cl, nodeid, new_values) :
    if not new_values.has_key ("status") :
        new_values ["status"] = "raised"
# end def create_defaults

def add_feature_to_release (db, cl, nodeid, old_values) :
    try :
        old_release = old_values ["release"]
    except (KeyError, TypeError) :
        old_release = None

    try :
        new_release = cl.get (nodeid, "release")
    except IndexError : # no new release
        new_release = None

    if old_release != new_release :
        if old_release :
            # remove from old release
            fs = db.release.get (old_release, "features")
            fs.remove (nodeid)
            db.release.set (old_release, features = fs)
        if new_release :
            # add this feature to selected release's features
            fs = db.release.get (new_release, "features")
            fs.append (nodeid)
            db.release.set (new_release, features = fs)
# end def add_feature_to_release

def init (db) :
    db.feature.audit ("create", create_defaults)
    db.feature.react ("set"   , add_feature_to_release)
    db.feature.react ("create", add_feature_to_release)
# end def init

### __END__ feature


