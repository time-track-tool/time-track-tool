#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-10 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    time_wp
#
# Purpose
#    Detectors for 'time_wp'
#

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

import common

def check_duplicate_field_value (cl, project, field, value) :
    ids     = cl.filter (None, {field : value, 'project' : project})
    # filter for exact match!
    ids     = [i for i in ids if cl.get (i, field) == value]
    if ids :
        assert (len (ids) == 1)
        raise Reject, _ ('Duplicate %(field)s "%(value)s"') % locals ()
# end def check_duplicate_field_value

def check_time_wp (db, cl, nodeid, new_values) :
    common.require_attributes \
        ( _
        , cl
        , nodeid
        , new_values
        , 'name'
        , 'project'
        , 'is_public'
        )
    common.check_name_len (_, new_values.get ('name', cl.get (nodeid, 'name')))
    prj = new_values.get ('project', cl.get (nodeid, 'project'))
    for i in 'name', 'wp_no' :
        if i in new_values :
            check_duplicate_field_value (cl, prj, i, new_values [i])
    if 'project' in new_values :
        new_values ['cost_center'] = db.time_project.get (prj, 'cost_center')
# end def check_time_wp

def new_time_wp (db, cl, nodeid, new_values) :
    if 'is_public' not in new_values :
        new_values ['is_public'] = False
    common.require_attributes \
        ( _
        , cl
        , nodeid
        , new_values
        , 'name'
        , 'responsible'
        , 'project'
        , 'is_public'
        )
    prid = new_values ['project']
    uid  = db.getuid ()
    prj  = db.time_project.getnode (prid)
    if  (  uid != prj.responsible
        and uid != prj.deputy
        and not common.user_has_role (db, uid, 'Project')
        and uid != '1'
        ) :
        raise Reject, ("You may only create WPs for your own projects")
    act  = db.time_project_status.get (prj.status, 'active')
    if not act and uid != '1' :
        raise Reject, ("You may only create WPs for active projects")
    if 'durations_allowed' not in new_values :
        new_values ['durations_allowed'] = False
    common.check_name_len (_, new_values ['name'])
    project = new_values  ['project']
    if 'wp_no' in new_values and not new_values ['wp_no'] :
        del new_values ['wp_no']
    for i in 'name', 'wp_no' :
        if i in new_values :
            check_duplicate_field_value (cl, project, i, new_values [i])
    status = db.time_project.get (project, 'status')
    new_values ['cost_center'] = prj.cost_center
# end def new_time_wp

def init (db) :
    if 'time_wp' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.time_wp.audit  ("create", new_time_wp)
    db.time_wp.audit  ("set",    check_time_wp)
# end def init

### __END__ time_wp
