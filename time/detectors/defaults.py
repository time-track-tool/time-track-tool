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
#    defaults
#
# Purpose
#    Auditors for 'default values'
#
# Revision Dates
#    22-Jul-2004 (MPH) Creation
#    5-Oct-2004 (MPH) Added implementation_task.create and
#                     documentation_task.create and testcase.create
#    ««revision-date»»···
#--
#
from roundup import roundupdb, hyperdb
from roundup.exceptions import Reject

def default_responsible (db, cl, nodeid, new_values) :
    if not new_values.has_key ("responsible") :
        new_values ["responsible"] = db.getuid()
# end def set_defaults

def default_defect_status (db, cl, nodeid, new_values) :
    if not new_values.has_key ("status") \
        or new_values ["status"] != "assigned" :
        new_values ["status"] = "assigned"
# end def default_defect_status


def init (db) :
    db.document.audit            ("create", default_responsible)
    db.release.audit             ("create", default_responsible)
    db.action_item.audit         ("create", default_responsible)
    db.feature.audit             ("create", default_responsible)
    db.design_document.audit     ("create", default_responsible)
    db.implementation_task.audit ("create", default_responsible)
    db.documentation_task.audit  ("create", default_responsible)
    db.testcase.audit            ("create", default_responsible)
    db.defect.audit              ("create", default_responsible)
    db.defect.audit              ("create", default_defect_status)
# end def init

### __END__ defaults


