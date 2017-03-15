#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-15 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
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
#    time_project
#
# Purpose
#    Detectors for 'time_project'
#

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation
from roundup.date                   import Date

import common

def check_time_project (db, cl, nodeid, new_values) :
    for i in 'wp_no', 'project' :
        if i in new_values and cl.get (nodeid, i) :
            raise Reject, "%(attr)s may not be changed" % {'attr' : _ (i)}
    common.check_prop_len (_, new_values.get ('name', cl.get (nodeid, 'name')))
    if 'work_location' in cl.properties :
        wl  = new_values.get ('work_location', cl.get (nodeid, 'work_location'))
        if not wl :
            common.require_attributes \
                (_, cl, nodeid, new_values, 'organisation')
    common.require_attributes \
        ( _, cl, nodeid, new_values
        , 'cost_center', 'approval_hr', 'approval_required'
        )
# end def check_time_project

def new_time_project (db, cl, nodeid, new_values) :
    defaults = \
        ( ('approval_required', False)
        , ('approval_hr',       False)
        , ('op_project',        True)
        )
    common.require_attributes (_, cl, nodeid, new_values, 'name', 'responsible')
    if 'work_location' in cl.properties and 'work_location' not in new_values :
        common.require_attributes (_, cl, nodeid, new_values, 'organisation')
    for k, v in defaults :
        if k in cl.properties and k not in new_values :
            new_values [k] = v
    common.check_prop_len (_, new_values ['name'])
    if 'status' not in new_values :
        try :
            new_values ['status'] = db.time_project_status.lookup ('New')
        except KeyError :
            new_values ['status'] = '1'
    common.require_attributes (_, cl, nodeid, new_values, 'cost_center')
# end def new_time_project

def fix_wp (db, cl, nodeid, old_values) :
    """ Copy cost_center of time_project to time_wp if changed in
        time_project. Close WPs if not an active status.
    """

    ccn = 'cost_center'
    tp  = cl.getnode (nodeid)
    act = db.time_project_status.get (tp.status, 'active')
    if not old_values :
        return
    now = Date ('.')
    for wp in db.time_wp.filter (None, dict (project = nodeid)) :
        d = {}
        if ccn in old_values and old_values [ccn] == tp.cost_center :
            d [ccn] = tp.cost_center
        if not act :
            te = db.time_wp.get (wp, 'time_end')
            if not te or te > now :
                d ['time_end'] = now
        if d :
            db.time_wp.set (wp, ** d)
# end def fix_wp

def init (db) :
    if 'time_project' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.time_project.audit  ("create", new_time_project)
    db.time_project.audit  ("set",    check_time_project)
    if 'time_wp' in db.classes :
        db.time_project.react  ("set", fix_wp)
# end def init

### __END__ time_project
