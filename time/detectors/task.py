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
#    task
#
# Purpose
#    detectors for task
#
# Revision Dates
#     8-Nov-2004 (MPH) Creation
#     9-Nov-2004 (MPH) Factored `update_features_status` to `common.py`
#    ««revision-date»»···
#--
#
from roundup import roundupdb, hyperdb
from roundup.exceptions import Reject

import common

def add_task (db, cl, nodeid, new_values) :
    """auditor for task.create:

    checks if both task.kind and task.title are set"""
    title = new_values.get ("title")
    kind  = new_values.get ("kind" )

    if not title :
        raise Reject, "Required task property title not supplied"
    if not kind :
        raise Reject, "Required task property kind not supplied"
# end def add_task

def update_feature_status (db, cl, nodeid, old_values) :
    """reactor on task.set:

    set the features status according to the linked tasks's status.

    - when only one task is in status `started`, set the feature's
      status to `open`
    - when all tasks are in status 'accepted', set the feature's
      status to `completed`. XXX: what about the defects ????
    """
    feature = cl.get (nodeid, "feature")
    new_values = {}
    common.update_feature_status (db, db.feature, feature, new_values)
    new_status = new_values.get ("status")
    if new_status :
        db.feature.set (feature, status = new_status)
# end def update_feature_status

def audit_task_status (db, cl, nodeid, new_values) :
    """auditor on task.set

    checks if the pending defects are open/closed
    if status accepted/accepted-but-defects:
        if sum (defects).status < closed :
            self.status = accepted-but-defects
        else :
            self.status = accepted
    """
    task_accepted    = db.task_status.lookup ("accepted")
    task_acc_but_def = db.task_status.lookup ("accepted-but-defects")
    task_status      = new_values.get ("status") or cl.get (nodeid, "status")
    if task_status in [task_accepted, task_acc_but_def] :
        defects = cl.get (nodeid, "defects")
        open_defects = False
        defect_closed = db.defect_status.lookup ("closed")
        for defect in defects :
            if db.defect.get (defect, "status") < defect_closed :
                open_defects = True
                break
        if open_defects and (task_status == task_accepted) :
            new_values ["status"] = task_acc_but_def
        elif not open_defects and (task_status == task_acc_but_def) :
            new_values ["status"] = task_accepted
# end def audit_task_status

def update_feature_test_ok (db, cl, nodeid, old_values) :
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
# end def update_feature_test_ok

def init (db) :
    db.task.audit ("create", add_task              )
    db.task.audit ("set"   , audit_task_status     )
    db.task.react ("set"   , update_feature_status )
    db.task.react ("set"   , update_feature_test_ok)
# end def init

### __END__ task


