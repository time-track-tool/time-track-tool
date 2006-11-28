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
#    feature
#
# Purpose
#    Detectors for the 'feature'
#
# Revision Dates
#    23-Jul-2004 (MPH) Creation
#     5-Oct-2004 (MPH) Added `set_composed_ofs_feature`
#     8-Nov-2004 (MPH) Moved `task` related to `task.py`, major cleanup
#     9-Nov-2004 (MPH) Some refactoring on `update_feature_status`
#     8-Jun-2005 (RSC) Hack for import of common
#    ««revision-date»»···
#--
#

from roundup import roundupdb, hyperdb
from roundup.exceptions import Reject

common = None

def is_feature_completed (db, cl, nodeid, new_values) :
    """auditor on feature.set

    does not allow any changes when the feture is in state `completed`
    """
    completed = db.feature_status.lookup ("completed")
    if cl.get (nodeid, "status") == completed :
        raise Reject, "You are not allowed to change a 'completed' feature"
# end def is_feature_completed

def add_feature_to_release (db, cl, nodeid, old_values) :
    """reactor on feature.set:

    update links to and from releases
    """
    old_release = old_values.get ("release", None)
    new_release = cl.get         (nodeid, "release")

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

def suspend_tasks_and_defects (db, cl, nodeid, old_values) :
    """reactor on feature.set:

    if the feature's state changed to `suspended` or `rejected` all it's
    task's and defect's status should also change to `suspended`
    """
    old_status = old_values ["status"]
    new_status = cl.get (nodeid, "status")
    suspend_ids = ( db.feature_status.lookup ("suspended")
                  , db.feature_status.lookup ("rejected")
                  )
    if old_status != new_status and new_status in suspend_ids :
        tasks = cl.get (nodeid, "tasks")
        if tasks :
            t_id_suspended = db.task_status.lookup ("suspended")
            for task in tasks :
                db.task.set (task, status = t_id_suspended)
        defects = cl.get (nodeid, "defects")
        if defects :
            d_id_suspended = db.defect_status.lookup ("suspended")
            for defect in defects :
                d_status = db.defect.get (defect, "status")
                if int (d_status) < 4 :
                    # all that are not closed or suspended
                    db.defect.set (defect, status = d_id_suspended)
# end def suspend_workpackages

def backlink_task (db, cl, nodeid, old_values) :
    """reactor feature.set

    sets the `feature` backlink in the newly created task.
    """
    old_tasks = old_values.get ("tasks", [])
    new_tasks = cl.get (nodeid, "tasks")
    new_task = [t for t in new_tasks if t not in old_tasks]
    if new_task :
        feature_id  = nodeid
        new_task_id = new_task [0]
        db.task.set (new_task_id, feature = feature_id)
# end def backlink_task

def move_defects (db, cl, nodeid, old_values) :
    """reactor on feature.set

    move the feature's defects from the release to the 'new' release when the
    `release` attribute changes. i.e. this feature gets moved from one
    release to another or gets detached from a release back into the pool of
    features.

    note: this code could be merged in the `add_feature_to_release` function
          but for clarity it's a seperate function.
    """
    old_release = old_values.get ("release", None)
    new_release = cl.get        (nodeid, "release")

    if new_release != old_release :
        my_defects = cl.get (nodeid, "defects")
        if old_release and my_defects :
            # remove `my_defects` from `old_release`'s lists of defects
            rel_bugs = db.release.get (old_release, "bugs")
            new_bugs = [d for d in rel_bugs if d not in my_defects]
            db.release.set (old_release, bugs = new_bugs)
            rel_fixes = db.release.get (old_release, "planned_fixes")
            new_fixes = [d for d in rel_fixes if d not in my_defects]
            db.release.set (old_release, planned_fixes = new_fixes)
        # update the defect's `solved_in_release`
        if old_release and not new_release :
            for id in my_defects :
                db.defect.set (id, solved_in_release = None)
        elif new_release :
            for id in my_defects :
                db.defect.set (id, solved_in_release = new_release)
            # append defects to `new_release`'s `planned_fixes`
            rel_fixes = db.release.get (new_release, "planned_fixes")
            rel_fixes.extend (my_defects)
            db.release.set (new_release, planned_fixes = rel_fixes)
        else :
            raise "Error: not old_release and not new_release ?!?!?"
# end def move_defects

def init (db) :
    if 'feature' not in db.classes :
        return
    import sys, os
    sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
    common = __import__ ('common', globals (), locals ())
    del (sys.path [0])

#    db.feature.audit             ("set"   , is_feature_completed        )
    db.feature.audit             ("set"   , common.update_feature_status)
    db.feature.react             ("set"   , add_feature_to_release      )
    db.feature.react             ("set"   , move_defects                )
    db.feature.react             ("set"   , suspend_tasks_and_defects   )
    db.feature.react             ("set"   , backlink_task               )
# end def init

### __END__ feature
