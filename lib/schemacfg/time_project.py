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
#    time_project
#
# Purpose
#    Schema definitions for PSP-elements (time-project or time-category)
#
#--
#

from roundup.hyperdb import Class
from roundup.date    import Interval
from schemacfg       import schemadef
import sum_common
import common

def init \
    ( db
    , Boolean
    , Date
    , Link
    , Multilink
    , Number
    , String
    , Class
    , Ext_Class
    , ** kw
    ) :
    export = {}

    class Time_Project_Class (Ext_Class) :
        """ Create a time_project class with some default properties
        """

        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( name                  = String    ()
                , description           = String    ()
                , responsible           = Link      ("user")
                , organisation          = Link      ("organisation")
                , deputy                = Link      ("user")
                , status                = Link      ("time_project_status")
                , purchasing_agents     = Multilink ("user")
                , group_lead            = Link      ("user")
                , team_lead             = Link      ("user")
                , infosec_req           = Boolean   ()
                , nosy                  = Multilink ("user")
                )
            Ext_Class.__init__ (self, db, classname, ** properties)
            self.setkey ("name")
        # end def __init__
    # end class Time_Project_Class
    export.update (dict (Time_Project_Class = Time_Project_Class))

    class Time_Project_Status_Class (Ext_Class) :
        """ Create a time_project_status class with some default properties
        """

        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( name                  = String    ()
                , description           = String    ()
                , active                = Boolean   ()
                )
            Ext_Class.__init__ (self, db, classname, ** properties)
            self.setkey ("name")
        # end def __init__
    # end class Time_Project_Status_Class
    export.update (dict (Time_Project_Status_Class = Time_Project_Status_Class))

    class SAP_CC_Class (Ext_Class) :
        """ Create a sap_cc class with some default properties
        """

        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( name                  = String    ()
                , description           = String    ()
                , responsible           = Link      ("user")
                , deputy                = Link      ("user")
                , purchasing_agents     = Multilink ("user")
                , group_lead            = Link      ("user")
                , team_lead             = Link      ("user")
                , nosy                  = Multilink ("user")
                , valid                 = Boolean   ()
                , organisation          = Link      ("organisation")
                )
            Ext_Class.__init__ (self, db, classname, ** properties)
            self.setkey ("name")
        # end def __init__
    # end class SAP_CC_Class
    export.update (dict (SAP_CC_Class = SAP_CC_Class))

    return export
# end def init

    #
    # SECURITY SETTINGS
    #
    # See the configuration and customisation document for information
    # about security setup.

def security (db, ** kw) :
    roles = \
        [ ("Project",           "Project Office")
        , ("Project_View",      "May view project data")
        , ("Controlling",       "Controlling")
        , ("Procurement",       "Purchasing/Procurement")
        ]

    #     classname
    # allowed to view   /  edit
    # For daily_record, time_record, additional restrictions apply
    classes = \
        [ ( "time_project_status"
          , ["User"]
          , ["Project"]
          )
        , ( "time_project"
          , ["Project_View", "Project", "Controlling"]
          , []
          )
        , ( "sap_cc"
          , ["User"]
          , []
          )
        ]

    prop_perms = \
        [ ( "time_project", "Edit", ["Project"]
          , ( "cost_center", "deputy", "description", "name"
            , "nosy", "organisation", "responsible", "status"
            )
          )
        , ( "time_project", "Edit", ["Procurement"]
          , ("purchasing_agents", "group_lead", "team_lead", "nosy")
          )
        , ( "sap_cc", "Edit", ["Procurement"]
          , ("purchasing_agents", "group_lead", "team_lead", "nosy")
          )
        , ( "time_project", "Edit", ["Controlling"]
          , ("group_lead", "team_lead", "nosy")
          )
        , ( "sap_cc", "Edit", ["Controlling"]
          , ("group_lead", "team_lead", "nosy")
          )
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

    fixdoc = schemadef.security_doc_from_docstring

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_project'
        , check       = sum_common.time_project_viewable
        , description = fixdoc (sum_common.time_project_viewable.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_project'
        )
    db.security.addPermissionToRole ('Procurement', p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'sap_cc'
        )
    db.security.addPermissionToRole ('Procurement', p)

    db.security.addPermissionToRole ('Project', 'Create', 'time_project')

# end def security
