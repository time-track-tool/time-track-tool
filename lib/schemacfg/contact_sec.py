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
#++
# Name
#    contact_sec
#
# Purpose
#    Security settings for contact classes

from schemacfg import schemadef

def security (db, ** kw) :
    roles = \
        [ ("Contact"       , "Allowed to add/change address data")
        ]

    classes = \
        [ ("contact_type", ["User"], [])
        , ("contact",      ["User"], ["Contact"])
        ]
    if 'adr_readonly' in db.security.role :
        classes [0][1].append ('Adr_Readonly')
        classes [1][1].append ('Adr_Readonly')

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, [])
    for perm in 'Retire', 'Restore':
        p = db.security.addPermission (name = perm, klass = 'contact')
        db.security.addPermissionToRole ('Contact', p)
# end def security
