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

def create_defaults (db, cl, nodeid, new_values) :
    if not new_values.has_key ("status") :
        new_values ["status"] = "raised"
# end def create_defaults

def add_feature_to_release (db, cl, nodeid, oldvalues) :
    """reactor on feature.set:

    update links to and from releases
    """
    old_release = oldvalues.get  ("release", None)
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

def update_features_status (db, cl, nodeid, oldvalues) :
    """reactor on task.set:

    set the features status according to the linked tasks's status.

    - when only one task is in status `started`, set the feature's
      status to `open`
    - when all tasks are in status 'accepted', set the feature's
      status to `completed`
    """
    old_status = oldvalues ["status"]
    new_status = cl.get (nodeid, "status")
    if old_status != new_status :
        # status changed, we should investigate further
        t_id_started = db.task_status.lookup    ("started")
        f_id_open    = db.feature_status.lookup ("open")
        f_id         = cl.get (nodeid, "feature") # new value, because it could
                                                  # also have changed !
        f_id_status  = db.feature.get (f_id, "status")
        if new_status == t_id_started and f_id_status != f_id_open :
            # status changed to status, we can safely set the feature's
            # status to `open` if not already done so.
            db.feature.set (f_id, status = f_id_open)
        else :
            # we need to iterate over all tasks of the feature, to
            # find out if we can close the feature now
            t_id_accepted = db.task_status.lookup ("accepted")
            can_close     = True
            tasks         = db.feature.get (f_id, "tasks")
            for task in tasks :
                if db.task.get (task, "status") != t_id_accepted :
                    can_close = False
                    break
            if can_close :
                f_id_completed = db.feature_status.lookup ("completed")
                db.feature.set (f_id, status = f_id_completed)
# end def update_features_status

def update_features_test_ok (db, cl, nodeid, oldvalues) :
    """reactor of task.set:
    if this task is of kind `testcase` we should propagate the `test_ok`
    value to the feature.
    """
    k_id_testcase = db.task_kind.lookup ("testcase")
    s_id_accepted = db.task_status.lookup ("accepted")
    if cl.get (nodeid, "kind")   == k_id_testcase and \
       cl.get (nodeid, "status") == s_id_accepted :
        f_id      = cl.get (nodeid, "feature")
        f_test_ok = db.feature.get (f_id, "test_ok")
        # if our `test_ok` is False, we can safely set the feature's test_ok
        # to False, if it's not already
        my_test_ok = cl.get (nodeid, "test_ok")
        if not my_test_ok and f_test_ok == True :
            # safe to set feature's test_ok to False
            db.feature.set (f_id, test_ok = False)
        elif my_test_ok :
            # my test is ok, check if there are other testcases attached to
            # this feature which have a `test_ok` which is False. If we find
            # none, we can safely set the feature's test_ok to True.
            all_testcases = \
                db.task.filter ( None
                               , { "feature" : f_id
                                 , "kind"    : k_id_testcase
                                 }
                               )
            closed_ok_testcases = \
                db.task.filter ( None
                               , { "feature" : f_id
                                 , "kind"    : k_id_testcase
                                 , "status"  : s_id_accepted
                                 , "test_ok" : True
                                 }
                               )
            if len (all_testcases) == len (closed_ok_testcases) :
                # all testcases are `accepted` and the test has passed
                db.feature.set (f_id, test_ok = True)
# end def update_features_test_ok

def suspend_tasks_and_defects (db, cl, nodeid, oldvalues) :
    """reactor on feature.set:

    if the feature's state changed to `suspended` or `rejected` all it's
    task's and defect's status should also change to `suspended`
    """
    old_status = oldvalues ["status"]
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

def add_task (db, cl, nodeid, newvalues) :
    """auditor for task.create:

    checks if both task.kind and task.title are set"""
    title = newvalues.get ("title")
    kind  = newvalues.get ("kind" )

    if not title :
        raise Reject, "Required task property title not supplied"
    if not kind :
        raise Reject, "Required task property kind not supplied"
# end def add_task

def backlink_task (db, cl, nodeid, oldvalues) :
    """reactor feature.set

    sets the `feature` backlink in the newly created task.
    """
    old_tasks = oldvalues.get ("tasks", [])
    new_tasks = cl.get (nodeid, "tasks")
    new_task = [t for t in new_tasks if t not in old_tasks]
    if new_task :
        feature_id  = nodeid
        new_task_id = new_task [0]
        db.task.set (new_task_id, feature = feature_id)
# end def backlink_task

def move_defects (db, cl, nodeid, oldvalues) :
    """reactor on feature.set

    move the feature's defects from the release to the 'new' release when the
    `release` attribute changes. i.e. this feature gets moved from one
    release to another or gets detached from a release back into the pool of
    features.

    note: this code could be merged in the `add_feature_to_release` function
          but for clarity it's a seperate function.
    """
    old_release = oldvalues.get ("release", None)
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
    db.feature.audit             ("create", create_defaults          )
    db.feature.react             ("set"   , add_feature_to_release   )
    db.feature.react             ("set"   , move_defects             )
    db.feature.react             ("set"   , suspend_tasks_and_defects)
    db.feature.react             ("set"   , backlink_task            )
    db.task.react                ("set"   , update_features_status   )
    db.task.react                ("set"   , update_features_test_ok  )
    db.task.audit                ("create", add_task                 )
# end def init

# TODO: feature.audit:
#       - disable adding new stuff when the feature is in state 'completed'
#         (at least)
#       - you cant start when it's not connected to a release ??
### __END__ feature


