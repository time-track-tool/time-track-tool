#! /usr/bin/python
# Copyright (C) 2004-25 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    schema-itadr
#
# Purpose
#    Specify the DB-Schema for a simple IT issue tracker.
#    Also include address information (e.g. for customers)
#    Link this file to schema.py
#--
#

import sys, os

sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
from schemacfg import schemadef

# sub-schema definitins to include
# Note: order matters, core is always last.
schemas = \
    ( 'user'
    , 'it_tracker'
    , 'msg_header'
    , 'address'
    , 'uid_adr'
    , 'contact'
    , 'callerid'
    , 'adr_ext'
    , 'adr_ptr'
    , 'adr_perm'
    , 'person_adr'
    , 'person'
    , 'pers_ext'
    , 'pers_prov'
    , 'sip'
    , 'contact_sec'
    , 'core'
    )

importer = schemadef.Importer (globals (), schemas)

del sys.path [0:1]

Person_Class (db, ''"address")

prop_perms = \
    [ ( "user", "View", ["IT"]
      , ( "roles",
        )
      )
    , ( "user", "Edit", ["IT"]
      , ( "realname", "csv_delimiter", "roles"
        )
      )
    ]

importer.update_security ()
schemadef.register_class_permissions (db, [], prop_perms)
# allow search of users for IT
p = db.security.addPermission \
    ( name        = 'Search'
    , klass       = 'user'
    )
db.security.addPermissionToRole ('IT', p)

# Let anonymous users access the web interface. Note that almost all
# trackers will need this Permission. The only situation where it's not
# required is in a tracker that uses an HTTP Basic Authenticated front-end.
db.security.addPermissionToRole('Anonymous', 'Web Access')
db.security.addPermission \
    ( name='Password-Reset'
    , description='User is allowed to request a password reset'
    )
db.security.addPermissionToRole('Anonymous', 'Password-Reset')
