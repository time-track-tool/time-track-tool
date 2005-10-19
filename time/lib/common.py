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
#    common
#
# Purpose
#    Common detectors used more often
#
# Revision Dates
#     9-Nov-2004 (MPH) Creation
#     6-Apr-2005 (RSC) minor comment correction
#                      moved to lib
#    ««revision-date»»···
#--
#
from roundup import roundupdb, hyperdb
from roundup.exceptions import Reject
from roundup.date       import Date, Interval
from time               import gmtime

ymd = '%Y-%m-%d'

def update_feature_status (db, cl, nodeid, new_values) :
    """auditor on feature.set

    update feature's status according to attached tasks/defects status.

    if single task is 'started' -> feature becomes 'open'
    if all tasks are 'accepted' -> feature becomes 'completed'
    if all tasks are 'accepted', but feature has open defects ->
                                   feature becomes 'completed-but-defects'
    """
    tasks   = new_values.get ("tasks")   or db.feature.get (nodeid, "tasks")
    defects = new_values.get ("defects") or db.feature.get (nodeid, "defects")
    open      = False
    completed = False
    task_started  = int (db.task_status.lookup ("started"))
    task_accepted = int (db.task_status.lookup ("accepted"))
    for task in tasks :
        task_status = int (db.task.get (task, "status"))
        if task_status == task_started :
            open = True
            break
        elif task_status >= task_accepted :
            completed = True
        elif task_status < task_started :
            completed = False
    if open :
        status = "open"
    elif completed :
        status = "completed"
    else :
        status = None

    if status == "completed" :
        # check if there are pending defects
        defect_closed = db.defect_status.lookup ("closed")
        has_defects = False
        for defect in defects :
            defect_status = db.defect.get (defect, "status")
            if defect_status < defect_closed :
                has_defects = True
                break
        if has_defects :
            status = "completed-but-defects"
    # set status
    if status :
        curr_status = new_values.get ("status") or \
                      db.feature.get (nodeid, "status")
        if status != curr_status :
            new_values ["status"] = db.feature_status.lookup (status)
# end def update_feature_status

def check_name_len (_, name) :
    if len (name) > 25 :
        raise Reject, \
            _ ('Name "%(name)s" too long (> 25 characters)') % locals ()
# end def name_len

def user_has_role (db, uid, * role) :
    roles = db.user.get (uid, 'roles')
    roles = dict ([(r.lower ().strip (), 1) for r in roles.split (',')])
    role  = [r.lower ().strip () for r in role]
    print role, roles
    for r in role :
        if r in roles : return True
    return False
# end def user_has_role

def clearance_by (db, userid, only_subs = False) :
    assert (userid)
    sv = db.user.get (userid, 'supervisor')
    if not sv :
        return []
    ap = db.user.get (sv, 'clearance_by') or sv
    su = db.user.get (ap, 'substitute')
    clearance = [ap]
    if su and db.user.get (ap, 'subst_active') :
        if only_subs :
            return [su]
        clearance.append (su)
    return clearance
# end def clearance_by

def week_from_date (date) :
    wday  = gmtime (date.timestamp ())[6]
    start = date + Interval ("%sd" % -wday)
    end   = date + Interval ("%sd" % (6 - wday))
    return start, end
# end def week_from_date

def pretty_range (start, end) :
    return ';'.join ([x.pretty (ymd) for x in (start, end)])
# end def pretty_range

### __END__
