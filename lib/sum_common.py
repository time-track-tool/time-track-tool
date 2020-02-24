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
#    summary
#
# Purpose
#    Utility functions for summary reports -- permission checks etc.
#
#--
#

import common
import user_dynamic

def time_project_viewable (db, userid, itemid) :
    """User may view time category if user is owner or deputy of time
       category or on nosy list of time category or if user is
       department manager of time category
    """
    project = db.time_project.getnode (itemid)
    p_nosy  = {}
    if 'nosy' in db.time_project.properties :
        p_nosy = dict.fromkeys (project.nosy)
    dep     = None
    if project.department :
        dep = db.department.getnode (project.department)
    mgr = None
    if 'manager' in db.department.properties and dep :
        mgr = dep.manager
    return \
        (  userid == project.responsible
        or userid == project.deputy
        or dep and userid == mgr
        or userid in p_nosy
        )
# end def time_project_viewable

def time_wp_viewable (db, userid, itemid) :
    """User may view work package if responsible for it, if user is
       owner or deputy of time category or on nosy list of time category
       or if user is department manager of time category
    """
    wp       = db.time_wp.getnode (itemid)
    return \
        (  userid == wp.responsible
        or time_project_viewable (db, userid, wp.project)
        or common.user_has_role (db, userid, 'Summary_View')
        )
# end def time_wp_viewable

def supervised_users (db, uid = None, use_sv = True) :
    """ Recursively compute the users for which the given uid is
        supervisor. If uid in not given (None), the current database
        user is taken.
    """
    if not uid :
        uid = db.getuid ()
    try :
        if uid in db.sup_cache :
            return db.sup_cache [uid]
    except AttributeError :
        def sup_cache_clear (db) :
            db.sup_cache = {}
        db.registerClearCacheCallback (sup_cache_clear, db)
        db.sup_cache = {}
    if use_sv :
        sv            = dict ((u, 1) for u in db.user.find (substitute = uid))
    else :
        sv            = {}
    sv [uid]          = 1
    users             = db.user.find (supervisor = sv)
    trans_users       = []
    for u in users :
        if u != uid :
            trans_users.extend (supervised_users (db, u, False))
    db.sup_cache [uid] = dict ((u, 1) for u in users + trans_users)
    return db.sup_cache [uid]
# end def supervised_users

def daily_record_viewable (db, userid, itemid) :
    """User may view a daily_record (and time_records that are attached
       to that daily_record) if the user owns the daily_record or has
       role 'HR' or 'Controlling', or the user is supervisor or
       substitute supervisor of the owner of the daily record (the
       supervisor relationship is transitive) or the user is the
       department manager of the owner of the daily record.
       If user has role HR-Org-Location and is in the same Org-Location
       as the record, it may also be seen.
    """
    if common.user_has_role (db, userid, 'HR', 'Controlling') :
        return True
    dr = db.daily_record.getnode (itemid)
    if userid == dr.user :
        return True
    if user_dynamic.hr_olo_role_for_this_user (db, userid, dr.user, dr.date) :
        return True
    # find departments managed by userid
    # FIXME: This needs a cache of users in departments
    # For now no access by department is granted
    # deps = db.department.filter (None, dict (manager = userid))
    # # find all users which are member of above departments:
    depusers = {}
    # if deps :
    #     depusers = dict.fromkeys \
    #         (db.user.filter (None, dict (department = deps)))
    return \
        (  dr.user in depusers
        or dr.user in supervised_users (db, userid)
        )
# end def daily_record_viewable

def get_users (db, filterspec, start, end) :
    """ Get all users in filterspec (including department, organisation,
        etc. where the user belongs to the given entity via a valid dyn
        user record between start and end)
    """
    users = filterspec.get ('user', [])
    sv    = dict ((i, 1) for i in filterspec.get ('supervisor', []))
    svu   = []
    if sv :
        svu = db.user.find (supervisor = sv)
    users = dict ((u, 1) for u in users + svu)
    found = bool (users)
    olo   = None
    if 'organisation' in filterspec :
        olo = db.org_location.filter \
            (None, dict (organisation = filterspec ['organisation']))
    for cl in 'department', 'org_location', 'org' :
        if cl == 'org' :
            cl = 'org_location'
            spec = olo
        else :
            spec = filterspec.get (cl, [])
        if spec :
            found = True
            for i in db.user_dynamic.filter \
                ( None
                , {cl : spec, 'valid_from' : end.pretty (';%Y-%m-%d')}
                ) :
                ud = db.user_dynamic.getnode (i)
                if  (   ud.valid_from <= end
                    and (not ud.valid_to or ud.valid_to > start)
                    ) :
                    users [ud.user] = 1
    if not found :
        users = dict ((i, 1) for i in db.user.getnodeids (retired = False))
    return users
# end def get_users
