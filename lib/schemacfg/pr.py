# -*- coding: iso-8859-1 -*-
# Copyright (C) 2015 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    pr
#
# Purpose
#    Schema definitions for Purchase Requests
#
#--
#

from roundup.hyperdb import Class
from schemacfg       import schemadef


def init (db, Organisation_Class, ** kw) :
    Organisation_Class (db, ''"organisation")
    Department_Class (db, ''"department")
# end def init

def security (db, ** kw) :
    """ See the configuration and customisation document for information
        about security setup. Assign the access and edit Permissions for
        issue, file and message to regular users now
    """

    roles = \
        [ ("Controlling",     "Controlling")
        ]

    #     classname        allowed to view   /  edit

    classes = \
        [ ("organisation", ["User"],  ["Controlling"])
        ]

    prop_perms = []

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

    tp_properties = \
        ( 'name', 'description', 'responsible', 'deputy', 'organisation'
        , 'status', 'id', 'cost_center'
        , 'creation', 'creator', 'activity', 'actor'
        )
    # Search permission
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'time_project'
        , properties  = tp_properties
        )
    db.security.addPermissionToRole ('User', p)

# end def security
