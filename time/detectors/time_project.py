#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
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

_      = lambda x : x
common = None

def check_time_project (db, cl, nodeid, new_values) :
    for i in 'wp_no', 'project' :
        if i in new_values and cl.get (nodeid, i) :
            raise Reject, "%(attr)s may not be changed" % {'attr' : _ (i)}
    common.check_name_len (_, new_values.get ('name', cl.get (nodeid, 'name')))
    wl  = new_values.get ('work_location', cl.get (nodeid, 'work_location'))
    for n in 'department', :
        if not new_values.get (n, cl.get (nodeid, n)) :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (n)}
    if not wl :
        for n in 'organisation', :
            if not new_values.get (n, cl.get (nodeid, n)) :
                raise Reject, "%(attr)s must be specified" % {'attr' : _ (n)}
# end def check_time_project

def new_time_project (db, cl, nodeid, new_values) :
    for i in ( 'name', 'responsible', 'department') :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
    for i in ('organisation', ) :
        if i not in new_values and 'work_location' not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
    common.check_name_len (_, new_values ['name'])
    if 'status' not in new_values :
        new_values ['status'] = db.time_project_status.lookup ('New')
    if 'op_project' not in new_values :
        new_values ['op_project'] = True
# end def new_time_project

def init (db) :
    if 'time_project' not in db.classes :
        return
    import sys, os
    global common, _
    sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
    common = __import__ ('common', globals (), locals ())
    del (sys.path [0])
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.time_project.audit  ("create", new_time_project)
    db.time_project.audit  ("set",    check_time_project)
# end def init

### __END__ time_project
