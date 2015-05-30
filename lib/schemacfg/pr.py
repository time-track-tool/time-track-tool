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

from schemacfg       import schemadef

def init \
    ( db
    , Boolean
    , Date
    , Link
    , Multilink
    , Number
    , String
    , Class
    , Department_Class
    , Ext_Class
    , Full_Issue_Class
    , Organisation_Class
    , Time_Project_Class
    , ** kw
    ) :
    export = {}
    p_o_b = Class \
        ( db, ''"part_of_budget"
        , name                  = String    ()
        , order                 = Number    ()
        , description           = String    ()
        )
    p_o_b.setkey ('name')

    t_c = Class \
        ( db, ''"terms_conditions"
        , name                  = String    ()
        , order                 = Number    ()
        , description           = String    ()
        )
    t_c.setkey ('name')

    purchase_type = Class \
        ( db, ''"purchase_type"
        , name                  = String    ()
        , order                 = Number    ()
        )
    purchase_type.setkey ('name')

    vat_country = Class \
        ( db, ''"vat_country"
        , country               = String    ()
        , vat                   = Number    ()
        )
    vat_country.setkey ('country')

    pr_offer = Class \
        ( db, ''"pr_offer"
        , index                 = Number    ()
        , description           = String    ()
        , supplier              = String    ()
        , offer_number          = String    ()
        , purchase_request      = Link      ("purchase_request")
        , vat_country           = Link      ("vat_country")
        , items                 = Multilink ("pr_offer_item")
        )

    pr_offer_item = Class \
        ( db, ''"pr_offer_item"
        , index                 = Number    ()
        , description           = String    ()
        , pr_offer              = Link      ("pr_offer")
        , units                 = Number    ()
        , price_per_unit        = Number    ()
        )

    class PR (Full_Issue_Class) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( organisation          = Link      ("organisation")
                , department            = Link      ("department")
                , requester             = Link      ("user")
                , purchase_type         = Link      ("purchase_type")
                , safety_critical       = Boolean   ()
                , time_project          = Link      ("time_project")
                , cost_center           = Link      ("cost_center")
                , approved_supplier     = Boolean   ()
                , add_to_las            = Boolean   ()
                #?, subcontracting        = Boolean   ()
                , part_of_budget        = Link      ("part_of_budget")
                , frame_purchase        = Boolean   ()
                , continuous_obligation = Boolean   ()
                , contract_term         = String    ()
                , termination_date      = Date      ()
                , terms_conditions      = Link      ("terms_conditions")
                , terms_identical       = Boolean   ()
                , delivery_deadline     = Date      ()
                , renegotiations        = Boolean   ()
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class PR
    pr = PR (db, ''"purchase_request")

    User_Ancestor = kw.get ('User_Class', Ext_Class)
    class User_Class (User_Ancestor) :
        """ Add organisation to user class
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( organisation           = Link      ("organisation")
                )
            User_Ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Class
    export.update (dict (User_Class = User_Class))

    # Protect against dupe instantiation during i18n template generation
    if 'organisation' not in db.classes :
        Organisation_Class (db, ''"organisation")
    if 'department' not in db.classes :
        Department_Class   (db, ''"department")
    if 'time_project' not in db.classes :
        Time_Project_Class (db, ''"time_project")
    return export
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
