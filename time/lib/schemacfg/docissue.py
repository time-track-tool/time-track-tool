# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    docissue
#
# Purpose
#    Schema definition for issue tracker with doc_issue_status
#
#--
#

from roundup.hyperdb import Class
from schemacfg       import schemadef

def init (db, Class, String, Link, Multilink, ** kw) :
    export   = {}
    docstat = Class \
        ( db, "doc_issue_status"
        , name                = String    (indexme = 'no')
        , description         = String    (indexme = 'no')
        , order               = String    (indexme = 'no')
        , transitions         = Multilink ("doc_issue_status")
        , nosy                = Multilink ("user")
        )
    docstat.setkey ("name")

    class Optional_Doc_Issue_Class (kw ['Optional_Doc_Issue_Class']) :
        """ extends the normal Optional_Doc_Issue_Class with doc_issue_status
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( doc_issue_status = Link      ("doc_issue_status")
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class Optional_Doc_Issue_Class
    export ['Optional_Doc_Issue_Class'] = Optional_Doc_Issue_Class
    return export
# end def init

def security (db, ** kw) :
    roles = \
        [ ("Issue_Admin", "Admin for issue tracker")
        ]
    #     classname             allowed to view   /  edit
    classes = \
        [ ("doc_issue_status",        ["User"], ["Issue_Admin"])
        ]

    schemadef.register_roles                 (db, roles)
    schemadef.register_class_permissions     (db, classes, ())
# end def security
