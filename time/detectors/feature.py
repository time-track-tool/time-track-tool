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
#     5-Oct-2004 (MPH) Added `set_composed_ofs_feature`
#    ««revision-date»»···
#--
#

from roundup import roundupdb, hyperdb
from roundup.exceptions import Reject

def workpackage_iter (db) :
    """yields a feature.attribute_name, db.klass tuple for all feature's
    attributes which correspond to workpackages.
    """
    for attr, klass in ( ( "documents"           , db.design_document    )
                       , ( "implementation_tasks", db.implementation_task)
                       , ( "testcases"           , db.testcase           )
                       , ( "documentation_tasks" , db.documentation_task )
                       ) :
        yield attr, klass
# end def workpackage

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

def set_composed_ofs_feature (db, cl, nodeid, old_values) :
    """set the 'feature' link (pointing to myself) in the newly generated
    issues which are now part of me
    """
    # we check the following attributes (which are multilinks to other
    # issue classes)
    for attr, klass in workpackage_iter (db) :
        old = old_values [attr]
        new = cl.get (nodeid, attr)
        for new in [k for k in new if k not in old] :
            k = klass.set (new, feature = nodeid)
# end def set_composed_ofs_feature

def update_status (db, cl, nodeid, old_values) :
    """set the features status according to what the linked workpackages are
    doing.
    - when only one workpackage is in status `started`, set it's feature's
      status to `open`
    - when all workpackages are in status 'accepted', set the feature's
      status to `completed`
    """
    old_status = old_values ["status"]
    new_status = cl.get (nodeid, "status")
    if old_status != new_status :
        id_started = db.work_package_status.lookup ("started")
        id_open    = db.feature_status.lookup      ("open")
        # status changed
        feature = cl.get (nodeid, "feature") # new value, because it could
                                             # also have changed !
        if new_status == id_started :
            db.feature.set (feature, status = id_open)
        else :
            # we need to iterate over all workpackages of the feature, to
            # find out if we can close the feature now
            id_accepted = db.work_package_status.lookup ("accepted")
            can_close = True
            for attr, klass in workpackage_iter (db) :
                wps = db.feature.get (feature, attr)
                for wp in wps :
                    if klass.get (wp, "status") != id_accepted :
                        can_close = False
                        break
            if can_close :
                id_completed = db.feature_status.lookup ("completed")
                db.feature.set (feature, status = id_completed)
    # check test_ok of all testcases and set the feature's test_ok
    # accordingly
    feature = cl.get (nodeid, "feature")
    tcs     = db.feature.get (feature, "testcases")
    test_ok = True
    id_accepted = db.work_package_status.lookup ("accepted")
    for tc in tcs :
        if ( (db.testcase.get (tc, "status") == id_accepted)
            and not db.testcase.get (tc, "test_ok")
           ) :
            test_ok = False
            break
    db.feature.set (feature, test_ok = test_ok)
# end def update_status

def suspend_workpackages (db, cl, nodeid, old_values) :
    """if the feature's state changed to `suspended` or `rejected` all it's
    workpackages status should change to `suspended`
    """
    old_status = old_values ["status"]
    new_status = cl.get (nodeid, "status")
    suspend_ids = ( db.feature_status.lookup ("suspended")
                  , db.feature_status.lookup ("rejected")
                  )
    if old_status != new_status and new_status in suspend_ids :
        id_suspended = db.work_package_status.lookup ("suspended")
        for attr, klass in workpackage_iter (db) :
            wps = cl.get (nodeid, attr)
            for wp in wps :
                klass.set (wp, status = id_suspended)
# end def suspend_workpackages

def init (db) :
    db.feature.audit             ("create", create_defaults         )
    db.feature.react             ("set"   , add_feature_to_release  )
    db.feature.react             ("create", add_feature_to_release  )
    db.feature.react             ("set"   , set_composed_ofs_feature)
    db.feature.react             ("set"   , suspend_workpackages    )
    db.implementation_task.react ("set"   , update_status           )
    db.testcase.react            ("set"   , update_status           )
    db.documentation_task.react  ("set"   , update_status           )
    db.design_document.react     ("set"   , update_status           )
# end def init

# TODO: feature.audit:
#       - disable adding new stuff when the feature is in state 'completed'
#         (at least)
#       - you cant start when it's not connected to a release ??
### __END__ feature


