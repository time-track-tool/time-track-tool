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
#    cost_center
#
# Purpose
#    Detectors for cost_center
#
#--
#

from roundup                        import roundupdb, hyperdb
from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation
common = None


def new_cc (db, cl, nodeid, new_values) :
    for i in 'cost_center_group', 'organisation' :
        if i not in new_values :
            raise Reject, _ ("New %s requires a %s") % (_ (cl.classname), _ (i))
    if 'status' not in new_values :
        new_values ['status'] = db.cost_center_status.lookup ('New')
# end def new_cc

def check_cc (db, cl, nodeid, new_values) :
    for i in 'cost_center_group', 'organisation', 'status' :
        if  (  i in new_values and not new_values [i]
            or not cl.get (nodeid, i) and not i in new_values
            ) :
            raise Reject, _ ("%(attr)s may not be undefined") % {'attr' : _ (i)}
# end def check_cc

def init (db) :
    if 'cost_center' not in db.classes :
        return
    global _, common
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    import common
    db.cost_center.audit     ("create", new_cc)
    db.cost_center.audit     ("set",    check_cc)
# end def init
