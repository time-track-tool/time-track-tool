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
#    defect
#
# Purpose
#    Detectors for 'defect's
#
# Revision Dates
#    11-Oct-2004 (MPH) Creation
#     2-Nov-2004 (MPH) Added `audit_superseder`
#     8-Nov-2004 (MPH) Added `update_defects_task`, major cleanup
#     9-Nov-2004 (MPH) Removed some debug output, refactoring
#     8-Jun-2005 (RSC) Hack for import of common
#    ««revision-date»»···
#--
#
from roundup import roundupdb, hyperdb, date
from roundup.exceptions import Reject
common = None

def check_new_defect (db, cl, nodeid, new_values) :
    """auditor for defect's create

    check the `found_in_release` value of new defect reports.
    if it points to a release whose status is
     >= M500: clear any `solved_in_release` -> defect container.
     between
     M0 and M500: set `solved_in_release` to `found_in_release`, so that it
                  gets appended to the release's bug's property.
    """
    release_id     = new_values ["found_in_release"]
    milestone_id   = db.release.get   (release_id  , "status")
    milestone_name = db.milestone.get (milestone_id, "name"  )
    ms_value       = int (milestone_name [1:]) # cut away the `M` from e.g.
                                               # "M100"
    if ms_value >= 500 :
        # clear solved_in_release - shouldn't be set anyway
        if new_values.has_key ("solved_in_release") :
            del new_values ["solved_in_release"]
    else :
        # release free for bug reports -> set solved_in_release to
        # found_in_release
        new_values ["solved_in_release"] = release_id
# end def check_new_defect

def check_defect (db, cl, nodeid, new_values) :
    """auditor for defect's set

    basically the same checks as in 'check_new_defect'.

    if `found_in_release` and `solved_in_release` are equal, than we have
    nothing to do.
    if `solved_in_release` is changed, (user wants to put this defect
    to another release), we have to check wheter it's allowed to add this
    defect (from a different release) to this relese (i.e. release planning
    milestone has not been reached already)
    """
    release_id         = new_values.get ("solved_in_release", None)
    if release_id :
        # check if found_in_release matches solved_in_release, then we can go
        # on, otherwise we have to check for the release beeing allowed to
        # attach defects to it's planned_fixes prperty.
        found_in_release = cl.get (nodeid, "found_in_release")
        if release_id != found_in_release :
            # check if the current reached milestone allows for attaching this
            # defect
            milestone_id   = db.release.get   (release_id  , "status")
            milestone_name = db.milestone.get (milestone_id, "name"  )
            ms_value       = int (milestone_name [1:]) # cut away the `M`
                                                       # from e.g. "M100"
            if ms_value >= 100 :
                rel_title = db.release.get (release_id, "title")
                raise Reject, "Release %r planning has been finished, you " \
                              "are not allowed to attach defects " \
                              "anymore !" % rel_title
# end def check_defect

def update_defects_task (db, cl, nodeid, old_values) :
    """reactor on defect.set

    if the defect was attached to a task - or detached from a task, we have
    to take care that the task's status is updated accordingly:

    if the task is in accepted or accepted-but-defects, we need to toggle
    between these two states according to the defect's status which are
    attached to this task.

    if task is in accepted and there are defects attached which are not
    closed or suspended we need to change the status of the task to
    accepted-but-defects.

    other way around we need to change from accepted-but-defects to accepted
    if the last defect gets closed.
    """
    old_task = old_values.get ("belongs_to_task")
    new_task = cl.get (nodeid, "belongs_to_task")
    defect_closed = db.defect_status.lookup ("closed")
    task_acc_def_status  = db.task_status.lookup ("accepted-but-defects")
    task_accepted_status = db.task_status.lookup ("accepted")
    tasks = []
    if old_task :
        tasks.append (old_task)
    if new_task :
        tasks.append (new_task)
    for task in tasks :
        defects = db.task.get (task, "defects")
        all_closed = True
        for defect in defects :
            if db.defect.get (defect, "status") < defect_closed :
                all_closed = False
                break
        if all_closed :
            if db.task.get (task, "status") == task_acc_def_status :
                db.task.set (task, status = task_accepted_status)
        elif not all_closed :
            if db.task.get (task, "status") == task_accepted_status :
                db.task.set (task, status = task_acc_def_status)
# end def update_defects_task

def add_defect_to_release (db, cl, nodeid, old_values) :
    """reactor on defect's create and set

    attach the newly generated defect automatically to a release, or not.

    we distinguish three different things to do:

    - the defect was found during development of a release, then both
      found_in_release and solved_in_release point to the same release and
      we attach this defect to this release's 'bugs' property.

    - the defect gets removed from a release, so it's solved_in_release was
      cleared during the previous action, and it now floats in space. we have
      to take care that it gets removed from the release pointed to by the
      possible old_values ['solved_in_release'] - afterwards this defect is
      floating around in free space and can easily be queried by requesting
      the 'solved_in_release' property to be 'unset' (i.e. filtering it by
      '-1')

    - the defect comes from outer space and will be solved in some new
      release, so it's solved_in_release field was unset and gets now set to
      some real release. in this case the defect is attached to the release's
      'planned_fixes' property. optionally it has to be removed from the
      old_value's 'solved_in_release' release, in case it gets moved on the
      fly from one release to another.

    note: found_in_release can only be set when reporting a defect.
    """
    if old_values == None :
        old_values = {}

    old_solved_in_release = old_values.get ("solved_in_release", None)
    new_solved_in_release = cl.get         (nodeid, "solved_in_release")
    found_in_release      = cl.get         (nodeid, "found_in_release")
    if old_solved_in_release and (old_solved_in_release != new_solved_in_release) :
        # remove this defect from the old release
        # from the bugs
        defs = db.release.get (old_solved_in_release, "bugs")
        while nodeid in defs : # just to be really on the safe side, this
                               # should not be iterated over more than once
                               # ever, thus we can also live with the
                               # 'non-performant' db.release.set () call
                               # every time.
            defs.remove (nodeid)
            db.release.set (old_solved_in_release, bugs = defs)
        # and/or from the planned_fixes
        defs = db.release.get (old_solved_in_release, "planned_fixes")
        while nodeid in defs :
            defs.remove (nodeid)
            db.release.set (old_solved_in_release, planned_fixes = defs)

    if (found_in_release == new_solved_in_release) and \
       (new_solved_in_release != old_solved_in_release) :
        # newly generated "bug" report, attach to 'bugs' of found_in_release
        defs = db.release.get (found_in_release, "bugs")
        defs.append (nodeid)
        db.release.set (found_in_release, bugs = defs)

    elif new_solved_in_release and (new_solved_in_release != old_solved_in_release) :
        # we have a new solved_in_release, attach to 'planned_fixes' of
        # new_solved_in_release, if it was a bug, it got cought by the if
        # above.
        defs = db.release.get (new_solved_in_release, "planned_fixes")
        defs.append (nodeid)
        db.release.set (new_solved_in_release, planned_fixes = defs)
# end def add_defect_to_release

def belongs_to_feature_auditor (db, cl, nodeid, new_values) :
    """auditor on defect.set

    clears the `belongs_to_task` attribute if `belongs_to_feature` has
    changed.
    """
    new_btf = new_values.get ("belongs_to_feature", None)
    if new_btf :
        new_values ["belongs_to_task"] = None
# end def belongs_to_feature_auditor

def belongs_to_feature_reactor (db, cl, nodeid, old_values) :
    """reactor on defect.set

    clears `feature` and `task` references to this defect if
    `belongs_to_feature` and/or `belongs_to_task` has changed.
    """
    old_btf = old_values.get ("belongs_to_feature")
    new_btf = cl.get (nodeid, "belongs_to_feature")
    if old_btf != new_btf :
        if old_btf :
            # remove us from the old feature's list of defects
            l = db.feature.get (old_btf, "defects")
            if nodeid in l :
                l.remove (nodeid)
            db.feature.set (old_btf, defects = l)
            # possibly update status of the feature from "completed-but-defects"
            # to "completed", if no more open defects are attached to this
            # feature
        if new_btf :
            # append us to the new feature's list of defects
            l = db.feature.get (new_btf, "defects")
            l.append (nodeid)
            db.feature.set (new_btf, defects = l)
            # possibly update status of the feature from "completed"
            # to "completed-but-defects", if it was "completed", as this defect
            # surely is not accepted
    # same now for belongs_to_task
    old_btt = old_values.get ("belongs_to_task")
    new_btt = cl.get (nodeid, "belongs_to_task")
    if old_btt != new_btt :
        if old_btt :
            # remove from the old task's list of defects
            l = db.task.get (old_btt, "defects")
            if nodeid in l :
                l.remove (nodeid)
            db.task.set (old_btt, defects = l)
        if new_btt :
            # append us to the new task's list of defects
            l = db.task.get (new_btt, "defects")
            l.append (nodeid)
            db.task.set (new_btt, defects = l)
# end def belongs_to_feature_reactor

def audit_superseder (db, cl, nodeid, new_values) :
    """auditor on defect's set

      * ensure that superseder gets not set to itself
      * automatically set status to closed-duplicate
      * ensure that superseder, once set can not be removed again
    """
    new_sup = new_values.get ("superseder")
    cd_id   = db.defect_status.lookup ("closed-duplicate")
    if new_sup == nodeid :
        raise Reject, "Can't set superseder to yourself"
    if not new_sup and cl.get (nodeid, "superseder") :
        raise Reject, "You are not allowed to remove the superseder"
    if new_values.get ("status", None) == cd_id and not new_sup :
        raise Reject, "You need to specify a superseder, when setting "\
                      "to 'closed-duplicate'"
    if new_sup :
        new_values ["status"] = cd_id
# end def audit_superseder

def set_closer (db, cl, nodeid, new_values) :
    """auditor on defect's set

    when status changes to one of closed-*:
     - `closer` is set to the current user
     - `closed` is set to current time
    """
    status_id = new_values.get ("status")
    if status_id :
        id_min = db.defect_status.lookup ("closed")
        id_max = db.defect_status.lookup ("closed-rejected")
        if status_id >= id_min and status_id <= id_max :
            new_values ["closer"] = db.getuid ()
            new_values ["closed"] = date.Date (".")
# end def set_closer

def react_on_closed (db, cl, nodeid, old_values) :
    """reactor on defect.set

    if the defect got closed (anything between and including `closed` and
    `closed-rejected`) we need to update the feature's status this defect is
    connected to.
    """
    closed          = db.defect_status.lookup ("closed")
    closed_rejected = db.defect_status.lookup ("closed-rejected")
    status          = cl.get                  (nodeid, "status")
    if status >= closed and \
       status <= closed_rejected :
        feature = cl.get (nodeid, "belongs_to_feature")
        if feature :
            new_values = {}
            common.update_feature_status (db, db.feature, feature, new_values)
            new_status = new_values.get ("status")
            if new_status :
                db.feature.set (feature, status = new_status)
# end def react_on_closed

def init (db) :
    if 'defect' not in db.classes :
        return
    import sys, os
    sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
    common = __import__ ('common', globals (), locals ())
    del (sys.path [0])

    db.defect.audit ("create", check_new_defect          )
    db.defect.audit ("set"   , check_defect              )
    db.defect.react ("create", add_defect_to_release     )
    db.defect.react ("set"   , add_defect_to_release     )
    db.defect.audit ("set"   , belongs_to_feature_auditor)
    db.defect.react ("set"   , belongs_to_feature_reactor)
    db.defect.audit ("set"   , audit_superseder          )
    db.defect.audit ("set"   , set_closer                )
    db.defect.react ("set"   , update_defects_task       )
    db.defect.react ("set"   , react_on_closed           )
# end def init

### __END__ defaults
