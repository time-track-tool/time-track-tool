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
#    Auditors for 'defect's
#
# Revision Dates
#    11-Oct-2004 (MPH) Creation
#    ««revision-date»»···
#--
#
from roundup import roundupdb, hyperdb
from roundup.exceptions import Reject

def add_defect_to_release (db, cl, nodeid, old_values) :
    old_release = old_values.get ("solved_in_release")
    new_release = cl.get         (nodeid, "solved_in_release")

    if old_release != new_release :
        if old_release :
            # remove from old release
            fs = db.release.get (old_release, "defects")
            fs.remove (nodeid)
            db.release.set (old_release, features = fs)
        if new_release :
            # add this feature to selected release's features
            fs = db.release.get (new_release, "features")
            fs.append (nodeid)
            db.release.set (new_release, features = fs)
# end def add_defect_to_release

def check_new_defect (db, cl, nodeid, new_values) :
    """check the `found_in_release` value of new defect reports.
    if it points to a release whose status is
     >= M500: clear any `solved_in_release` -> defect container.
     <  M150: print Error message that this release has not been started.
     between
     M150 and M500: set `solved_in_release` to `found_in_release`, so that it
                    gets appended to the release's bug's property.
    """
    release_id     = new_values ["found_in_release"]
    milestone_id   = db.release.get   (release_id  , "status")
    milestone_name = db.milestone.get (milestone_id, "name"  )
    ms_value       = int (milestone_name [1:]) # cut away the `M` from e.g.
                                               # "M100"
    if ms_value < 50 :
        rel_title = db.release.get (release_id, "title")
        raise Reject, "Release %r is not open for reporting bugs - " \
                      "wait until 'M50' is reached !"% rel_title
    elif ms_value >= 500 :
        # clear solved_in_release - shouldn't be set anyway
        if new_values.has_key ("solved_in_release") :
            del new_values ["solved_in_release"]
    else :
        # release free for bug reports -> set solved_in_release to
        # found_in_release
        new_values ["solved_in_release"] = release_id
# end def check_new_defect

def check_defect (db, cl, nodeid, new_values) :
    """basically the same checks as in 'check_new_defect', but with
    potentially different properties and impacts ;)

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

def add_defect_to_release (db, cl, nodeid, old_values) :
    """attach the newly generated defect automatically to a release, or not.

    we distinguish two different things to do:

    - the defect was found during development of a release, then both
      found_in_release and solved_in_release point to the same release and
      we attach this defect to this release's 'bugs' property.

    - the defect gets removed from a release, so it's solved_in_release was
      cleared during the previous action, and it now floats in space. we have
      to take care that it gets removed from the release pointed to by the
      possible old_values ['solved_in_release'] - afterwards this defect is
      floating around in free space and can easily be queried by requesting
      the 'solved_in_release' property to be 'unset' (i.e. setting it to '-1')

    - the defect comes from outer space and will be solved in some new
      release, so it's solved_in_release field was unset and gets now set to
      some real release. in this case the defect is attached to the release's
      'planned_fixes' property. optionally it has to be removed from the
      old_value's 'solved_in_release' - in case it gets moved on the fly from
      one release to another.

    note: found_in_release can only be set when reporting a defect.
    """
    if old_values == None :
        old_values = {}

    old_solved_in_release = old_values.get ("solved_in_release", None)
    new_solved_in_release = cl.get         (nodeid, "solved_in_release")
    found_in_release    = cl.get (nodeid, "found_in_release")
    if old_solved_in_release and (old_solved_in_release != new_solved_in_release) :
        # remove this defect from the old release
        # from the bugs
        defs = db.release.get (old_solved_in_release, "bugs")
        print "old bugs:", defs
        while nodeid in defs : # just to be really on the safe side, this
                               # should not be iterated over more than once
                               # ever, thus we can also live with the
                               # 'non-performant' db.release.set () call
                               # every time.
            defs.remove (nodeid)
            print "set", defs
            db.release.set (old_solved_in_release, bugs = defs)
        # and/or from the planned_fixes
        defs = db.release.get (old_solved_in_release, "planned_fixes")
        print "old planned_fixes:", defs
        while nodeid in defs :
            defs.remove (nodeid)
            print "set", defs
            db.release.set (old_solved_in_release, planned_fixes = defs)

    if found_in_release == new_solved_in_release :
        # newly generated "bug" report, attach to 'bugs' of found_in_release
        defs = db.release.get (found_in_release, "bugs")
        print "append to ", found_in_release, defs
        defs.append (nodeid)
        print "set", defs
        db.release.set (found_in_release, bugs = defs)

    elif new_solved_in_release and (new_solved_in_release != old_solved_in_release) :
        # we have a new solved_in_release, attach to 'planned_fixes' of
        # new_solved_in_release, if it was a bug, it got cought by the if
        # above.
        defs = db.release.get (new_solved_in_release, "planned_fixes")
        print "append to new", new_solved_in_release, defs
        defs.append (nodeid)
        print "set", defs
        db.release.set (new_solved_in_release, planned_fixes = defs)
# end def add_defect_to_release

def belongs_to_auditor (db, cl, nodeid, newvalues) :
    """auditor on defect.set

    clears the `belongs_to_task` attribute if `belongs_to_feature` has
    changed.

    removes self from the corresponding task's `defects` list.
    """
    new_btf = newvalues.get ("belongs_to_feature", None)
    if new_btf :
        newvalues ["belongs_to_task"] = None
# end def belongs_to_auditor

def belongs_to_reactor (db, cl, nodeid, oldvalues) :
    """reactor on defect.set

    clears `feature` and `task` references to this defect if
    `belongs_to_feature` and/or `belongs_to_task` has changed.
    """
    old_btf = oldvalues.get ("belongs_to_feature")
    new_btf = cl.get (nodeid, "belongs_to_feature")
    if old_btf != new_btf :
        if old_btf :
            # remove us from the old feature's list of defects
            l = db.feature.get (old_btf, "defects")
            if nodeid in l :
                l.remove (nodeid)
            db.feature.set (old_btf, defects = l)
        if new_btf :
            # append us to the new feature's list of defects
            l = db.feature.get (new_btf, "defects")
            l.append (nodeid)
            db.feature.set (new_btf, defects = l)
    # same now for belongs_to_tasks
    old_btt = oldvalues.get ("belongs_to_task")
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
# end def belongs_to_reactor

def init (db) :
    pass
    db.defect.audit ("create", check_new_defect     )
    db.defect.audit ("set"   , check_defect         )
    db.defect.react ("create", add_defect_to_release)
    db.defect.react ("set"   , add_defect_to_release)
    db.defect.audit ("set"   , belongs_to_auditor   )
    db.defect.react ("set"   , belongs_to_reactor   )
# end def init

### __END__ defaults


