#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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

import common

def check_time_project (db, cl, nodeid, new_values) :
    for i in 'wp_no', 'project' :
        if i in new_values and cl.get (nodeid, i) :
            raise Reject, "%(attr)s may not be changed" % {'attr' : _ (i)}
    common.check_name_len (_, new_values.get ('name', cl.get (nodeid, 'name')))
    wl  = new_values.get ('work_location', cl.get (nodeid, 'work_location'))
    if not wl :
        common.require_attributes (_, cl, nodeid, new_values, 'organisation')
    common.require_attributes (_, cl, nodeid, new_values, 'cost_center')
# end def check_time_project

def new_time_project (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'name', 'responsible')
    if 'work_location' not in new_values :
        common.require_attributes (_, cl, nodeid, new_values, 'organisation')
    common.check_name_len (_, new_values ['name'])
    if 'status' not in new_values :
        try :
            new_values ['status'] = db.time_project_status.lookup ('New')
        except KeyError :
            new_values ['status'] = '1'
    if 'op_project' not in new_values :
        new_values ['op_project'] = True
    common.require_attributes (_, cl, nodeid, new_values, 'cost_center')
# end def new_time_project

def fix_wp (db, cl, nodeid, old_values) :
    """ Copy cost_center of time_project to time_wp if changed in
        time_project.
    """
    ccn = 'cost_center'
    cc  = cl.getnode (nodeid)
    if  (  not old_values
        or ccn not in old_values
        or old_values [ccn] == cc.cost_center
        ) :
        return
    for wp in db.time_wp.filter (None, dict (project = nodeid)) :
        db.time_wp.set (wp, cost_center = cc.cost_center)
# end def fix_wp

def init (db) :
    if 'time_project' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.time_project.audit  ("create", new_time_project)
    db.time_project.audit  ("set",    check_time_project)
    db.time_project.react  ("create", fix_wp)
    db.time_project.react  ("set",    fix_wp)
# end def init

### __END__ time_project
