# Copyright (C) 2020 Dr. Ralf Schlatterbeck Open Source Consulting.
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

from roundup.hyperdb import Class
from schemacfg       import schemadef

def init (db, Class, String, Date, ** kw) :
    job_log = Class \
        ( db, "job_log"
        , job_key             = String    (indexme = 'no')
        , timestamp           = Date      ()
        , comment             = String    (indexme = 'no')
        )
    job_log.setkey ("job_key")
    job_log.setlabelprop ("job_key")
# end def init

def security (db, ** kw) :
    roles = \
        [ ("Dom-User-Edit-GTT", "Edit/Create users with specific AD domain")
        ]
    #     classname             allowed to view   /  edit
    classes = \
        [ ("job_log",           ["User"],        ["Dom-User-Edit-GTT"])
        ]

    schemadef.register_roles                 (db, roles)
    schemadef.register_class_permissions     (db, classes, ())
# end def security
