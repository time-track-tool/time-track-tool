# Copyright (C) 2015-23 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    And for permission management
#
#--
#

from roundup.hyperdb import Class
from roundup.date    import Interval
from schemacfg       import schemadef
import sum_common
import common
import o_permission

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
    ):
    export = {}

    class Time_Project_Class (Ext_Class):
        """ Create a time_project class with some default properties
        """

        def __init__ (self, db, classname, ** properties):
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

    class Time_Project_Status_Class (Ext_Class):
        """ Create a time_project_status class with some default properties
        """

        def __init__ (self, db, classname, ** properties):
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

    class SAP_CC_Class (Ext_Class):
        """ Create a sap_cc class with some default properties
        """

        def __init__ (self, db, classname, ** properties):
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

    class O_Permission_Class (Ext_Class):
        """ Create a o_permission class with some default properties
        """

        def __init__ (self, db, classname, ** properties):
            self.update_properties \
                ( user                  = Link      ("user")
                )
            Ext_Class.__init__ (self, db, classname, ** properties)
            self.setlabelprop ("user")
        # end def __init__
    # end class O_Permission_Class
    export.update (dict (O_Permission_Class = O_Permission_Class))

    return export
# end def init

    #
    # SECURITY SETTINGS
    #
    # See the configuration and customisation document for information
    # about security setup.

def security (db, ** kw):
    roles = \
        [ ("Project",           "Project Office")
        , ("Project_View",      "May view project data")
        , ("Controlling",       "Controlling")
        , ("O-Permission",      "Allowed org-location/organisation per user")
        , ("View-Roles",        "Allow to view user roles")
        ]

    #     classname
    # allowed to view   /  edit
    # For daily_record, time_record, additional restrictions apply
    classes = \
        [ ( "time_project_status"
          , ["User"]
          , ["Project"]
          )
        # Note that the role 'O-Permission' has additional checks that
        # do not allow changing org locations that are not in the
        # permission set of that user.
        , ( "o_permission"
          , ["User"]
          , ["Admin", "O-Permission"]
          )
        ]

    prop_perms = \
        [ ( "user",         "View", ["View-Roles"]
          , ( "roles"
            ,
            )
          )
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

    fixdoc = schemadef.security_doc_from_docstring

    schemadef.add_search_permission (db, 'sap_cc', 'User')
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'sap_cc'
        , check       = o_permission.sap_cc_allowed_by_org
        , description = fixdoc (o_permission.sap_cc_allowed_by_org.__doc__)
        )
    db.security.addPermissionToRole ("User", p)

    schemadef.add_search_permission (db, 'time_project', 'User')
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_project'
        , check       = o_permission.time_project_allowed_by_org
        , description = fixdoc
            (o_permission.time_project_allowed_by_org.__doc__)
        )
    for role in ("Project_View", "Project", "Controlling"):
        db.security.addPermissionToRole (role, p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_project'
        , check       = sum_common.time_project_viewable
        , description = fixdoc (sum_common.time_project_viewable.__doc__)
        )
    db.security.addPermissionToRole ('User', p)
    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'time_project'
        , check       = o_permission.time_project_allowed_by_org
        , properties  = ( "cost_center", "deputy", "description", "name"
                        , "nosy", "organisation", "responsible", "status"
                        )
        , description = fixdoc
            (o_permission.time_project_allowed_by_org.__doc__)
        )
    db.security.addPermissionToRole ("Project", p)
    db.security.addPermissionToRole ('Project', 'Create', 'time_project')

# end def security
