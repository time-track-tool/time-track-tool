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
#    document
#
# Purpose
#    Auditors / Reactors for the 'document' class.
#
# Revision Dates
#    22-Jul-2004 (MPH) Creation
#     5-Oct-2004 (MPH) Factored set_default_wp_status and added to
#                      work_package.create and testcase.create
#    ««revision-date»»···
#--
#

from roundup import roundupdb, hyperdb
from roundup.exceptions import Reject

def set_default_wp_status (db, cl, nodeid, new_values) :
    if not new_values.has_key ("status") :
        new_values ["status"] = "issued"
# end def set_default_wp_status

def set_document_defaults (db, cl, nodeid, new_values) :
    set_default_wp_status (db, cl, nodeid, new_values)
    if not new_values.has_key ("title") :
        # if type specified
        if new_values.has_key ("type") :
            desc = db.document_type.get (new_values ["type"], "description")
            new_values ["title"] = desc
        else :
            new_values ["title"] = "Automatically generated"
# end def set_document_defaults

def set_design_doc_defaults (db, cl, nodeid, new_values) :
    set_default_wp_status (db, cl, nodeid, new_values)
    if not new_values.has_key ("title") :
        # if type specified
        if new_values.has_key ("type") :
            desc = db.design_document_type.get ( new_values ["type"]
                                               , "description"
                                               )
            new_values ["title"] = desc
        else :
            new_values ["title"] = "Automatically generated"
# end def set_design_doc_defaults


def init (db) :
    db.document.audit            ("create", set_document_defaults)
    db.design_document.audit     ("create", set_design_doc_defaults)
    db.implementation_task.audit ("create", set_default_wp_status)
    db.documentation_task.audit  ("create", set_default_wp_status)
    db.testcase.audit            ("create", set_default_wp_status)
# end def init

### __END__ status


