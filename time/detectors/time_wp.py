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
#    time_wp
#
# Purpose
#    Detectors for 'time_wp'
#

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

_      = lambda x : x
common = None

def check_duplicate_field_value (cl, project, field, value) :
    ids     = cl.filter (None, {field : value, 'project' : project})
    if ids :
        assert (len (ids) == 1)
        raise Reject, _ ('Duplicate %(field)s "%(value)s"') % locals ()
# end def check_duplicate_field_value

def check_time_wp (db, cl, nodeid, new_values) :
    for i in 'wp_no', 'project' :
        if i in new_values and cl.get (nodeid, i) :
            raise Reject, "%(attr)s may not be changed" % {'attr' : _ (i)}
    common.check_name_len (_, new_values.get ('name', cl.get (nodeid, 'name')))
    project = cl.get (nodeid, 'project')
    for i in 'name', 'wp_no' :
        if i in new_values :
            check_duplicate_field_value (cl, project, i, new_values [i])
# end def check_time_wp

def new_time_wp (db, cl, nodeid, new_values) :
    for i in 'name', 'responsible', 'project', 'planned_effort', 'cost_center' :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
    if 'durations_allowed' not in new_values :
        new_values ['durations_allowed'] = False
    common.check_name_len (_, new_values ['name'])
    project = new_values  ['project']
    for i in 'name', 'wp_no' :
        if i in new_values :
            check_duplicate_field_value (cl, project, i, new_values [i])
# end def new_time_wp

def init (db) :
    import sys, os
    global common, _
    sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
    common = __import__ ('common', globals (), locals ())
    del (sys.path [0])
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.time_wp.audit  ("create", new_time_wp)
    db.time_wp.audit  ("set",    check_time_wp)
# end def init

### __END__ time_wp
