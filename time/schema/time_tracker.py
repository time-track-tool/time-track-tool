# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    company
#
# Purpose
#    Schema definitions for a company.
#
#--
#

from roundup.hyperdb import Class
from common          import clearance_by
import schemadef

def init (db, Class, String, Date, Link, Multilink, Boolean, Number, ** kw) :
    cost_center = Class \
        ( db
        , ''"cost_center"
        , name                  = String    ()
        , description           = String    ()
        , status                = Link      ("cost_center_status")
        , cost_center_group     = Link      ("cost_center_group")
        , organisation          = Link      ("organisation")
        )
    cost_center.setkey ("name")

    cost_center_group = Class \
        ( db
        , ''"cost_center_group"
        , name                  = String    ()
        , description           = String    ()
        , responsible           = Link      ("user")
        , active                = Boolean   ()
        )
    cost_center_group.setkey ("name")

    cost_center_status = Class \
        ( db
        , ''"cost_center_status"
        , name                  = String    ()
        , description           = String    ()
        , active                = Boolean   ()
        )
    cost_center_status.setkey ("name")

    daily_record = Class \
        ( db
        , ''"daily_record"
        , user                  = Link      ("user",          do_journal = "no")
        , date                  = Date      (offset = 0)
        , status                = Link      ( "daily_record_status"
                                            , do_journal = "no"
                                            )
        , time_record           = Multilink ("time_record",   do_journal = "no")
        )

    daily_record_status = Class \
        ( db
        , ''"daily_record_status"
        , name                  = String    ()
        , description           = String    ()
        )
    daily_record_status.setkey ("name")

    public_holiday = Class \
        ( db
        , ''"public_holiday"
        , name                  = String    ()
        , description           = String    ()
        , date                  = Date      (offset = 0)
        , locations             = Multilink ("location")
        , is_half               = Boolean   ()
        )

    summary_report = Class \
        ( db
        , ''"summary_report"
        , date                  = Date      (offset = 0)
        , user                  = Link      ("user")
        , department            = Link      ("department")
        , supervisor            = Link      ("user")
        , org_location          = Link      ("org_location")
        , time_wp               = Link      ("time_wp")
        , time_wp_group         = Link      ("time_wp_group")
        , cost_center           = Link      ("cost_center")
        , cost_center_group     = Link      ("cost_center_group")
        , time_project          = Link      ("time_project")
        , summary_type          = Link      ("summary_type")
        , summary               = Boolean   ()
        , status                = Link      ("daily_record_status")
        , show_empty            = Boolean   ()
        , planned_effort        = Number    ()
        )

    summary_type = Class \
        ( db
        , ''"summary_type"
        , name                  = String    ()
        , order                 = Number    ()
        )
    summary_type.setkey ("name")

    time_activity = Class \
        ( db
        , ''"time_activity"
        , name                  = String    ()
        , description           = String    ()
        , travel                = Boolean   ()
        )
    time_activity.setkey ("name")

    time_project = Class \
        ( db
        , ''"time_project"
        , name                  = String    ()
        , description           = String    ()
        , responsible           = Link      ("user")
        , deputy                = Link      ("user")
        , organisation          = Link      ("organisation")
        , department            = Link      ("department")
        , planned_effort        = Number    ()
        , status                = Link      ("time_project_status")
        , work_location         = Link      ("work_location")
        , max_hours             = Number    ()
        , nosy                  = Multilink ("user")
        , op_project            = Boolean   ()
        )
    time_project.setkey ("name")

    time_project_status = Class \
        ( db
        , ''"time_project_status"
        , name                  = String    ()
        , description           = String    ()
        , active                = Boolean   ()
        )
    time_project_status.setkey ("name")

    time_record = Class \
        ( db
        , ''"time_record"
        , daily_record          = Link      ("daily_record",  do_journal = "no")
        , start                 = String    (indexme = "no")
        , end                   = String    (indexme = "no")
        , start_generated       = Boolean   ()
        , end_generated         = Boolean   ()
        , duration              = Number    ()
        , tr_duration           = Number    ()
        , wp                    = Link      ("time_wp",       do_journal = "no")
        , time_activity         = Link      ("time_activity", do_journal = "no")
        , work_location         = Link      ("work_location", do_journal = "no")
        , comment               = String    (indexme = "no")
        , dist                  = Number    ()
        )

    time_wp = Class \
        ( db
        , ''"time_wp"
        , name                  = String    ()
        , wp_no                 = String    ()
        , description           = String    ()
        , responsible           = Link      ("user")
        , project               = Link      ("time_project")
        , time_start            = Date      (offset = 0)
        , time_end              = Date      (offset = 0)
        , planned_effort        = Number    ()
        , bookers               = Multilink ("user")
        , durations_allowed     = Boolean   ()
        , cost_center           = Link      ("cost_center")
        , travel                = Boolean   ()
        )

    time_wp_group = Class \
        ( db
        , ''"time_wp_group"
        , name                  = String    ()
        , description           = String    ()
        , wps                   = Multilink ("time_wp")
        )
    time_wp_group.setkey ("name")

    user_dynamic = Class \
        ( db
        , ''"user_dynamic"
        , user                  = Link      ("user")
        , valid_from            = Date      (offset = 0)
        , valid_to              = Date      (offset = 0)
        , booking_allowed       = Boolean   ()
        , travel_full           = Boolean   ()
        , durations_allowed     = Boolean   ()
        , weekend_allowed       = Boolean   ()
        , vacation_remaining    = Number    ()
        , vacation_yearly       = Number    ()
        , daily_worktime        = Number    ()
        , weekly_hours          = Number    ()
        , supp_weekly_hours     = Number    ()
        , hours_mon             = Number    ()
        , hours_tue             = Number    ()
        , hours_wed             = Number    ()
        , hours_thu             = Number    ()
        , hours_fri             = Number    ()
        , hours_sat             = Number    ()
        , hours_sun             = Number    ()
        , org_location          = Link      ("org_location")
        , department            = Link      ("department")
        )

    work_location = Class \
        ( db
        , ''"work_location"
        , code                  = String    ()
        , description           = String    ()
        )
    work_location.setkey ("code")
# end def init

    #
    # SECURITY SETTINGS
    #
    # See the configuration and customisation document for information
    # about security setup.
    # Assign the access and edit Permissions for issue, file and message
    # to regular users now

def security (db, ** kw) :
    roles = \
        [ ("Project"       , "Project Office"                )
        ]

    #     classname        allowed to view   /  edit
    # For daily_record, time_record, additional restrictions apply
    classes = \
        [ ("cost_center"         , ["User"],             ["Controlling"     ])
        , ("cost_center_group"   , ["User"],             ["Controlling"     ])
        , ("cost_center_status"  , ["User"],             ["Controlling"     ])
        , ("daily_record"        , ["HR","Controlling"], ["HR","Controlling"])
        , ("daily_record_status" , ["User"],             ["Admin"           ])
        , ("public_holiday"      , ["User"],             ["HR","Controlling"])
        , ("summary_report"      , ["User"],             [                  ])
        , ("summary_type"        , ["User"],             ["Admin"           ])
        , ("time_activity"       , ["User"],             ["Controlling"     ])
        , ("time_project_status" , ["User"],             ["Project"         ])
        , ("time_project"        , ["User"],             ["Project"         ])
        , ("time_record"         , ["HR","Controlling"], ["HR","Controlling"])
        , ("time_wp_group"       , ["User"],             ["Project"         ])
        , ("time_wp"             , ["User"],             ["Project"         ])
        , ("user_dynamic"        , ["HR"],               ["HR"              ])
        , ("work_location"       , ["User"],             ["Controlling"     ])
        ]

    prop_perms = \
        [ ( "time_wp", "Edit", ["Controlling"], ( "project",))
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

    # For the following the use is regulated by auditors.
    db.security.addPermissionToRole ('User', 'Create', 'time_record')
    db.security.addPermissionToRole ('User', 'Create', 'daily_record')

    def ok_daily_record (db, userid, itemid) :
        """Determine if the user owns the daily record, a negative itemid
           indicates that the record doesn't exits yet -- we allow creation
           in this case. Modification is also allowed by the supervisor or
           the person to whom approvals are delegated.
        """
        if int (itemid) < 0 : # allow creation
            return True
        ownerid   = db.daily_record.get (itemid, 'user')
        if not ownerid :
            return False
        clearance = clearance_by (db, ownerid)
        return userid == ownerid or userid in clearance
    # end def ok_daily_record

    def own_time_record (db, userid, itemid) :
        """Determine if the user owns the daily record, a negative itemid
           indicates that the record doesn't exits yet -- we allow creation
           in this case.
        """
        if int (itemid) < 0 : # allow creation
            return True
        dr      = db.time_record.get  (itemid, 'daily_record')
        ownerid = db.daily_record.get (dr, 'user')
        return userid == ownerid
    # end def own_time_record

    def is_project_owner_of_wp (db, userid, itemid) :
        """ Check if user is owner of wp """
        if int (itemid) < 0 :
            return False
        prid    = db.time_wp.get (itemid, 'project')
        project = db.time_project.getnode (prid)
        return userid == project.responsible
    # end def is_project_owner_of_wp

    def ok_work_package (db, userid, itemid) :
        """ Check if user is responsible for wp or if user is responsible
            for project or is the deputy for project
        """
        if int (itemid) < 0 :
            return False
        ownerid = db.time_wp.get (itemid, 'responsible')
        if ownerid == userid :
            return True
        prid    = db.time_wp.get (itemid, 'project')
        project = db.time_project.getnode (prid)
        return userid == project.responsible or userid == project.deputy
    # end def ok_work_package

    def approval_for_time_record (db, userid, itemid) :
        """Viewing is allowed by the supervisor or the person to whom
           approvals are delegated.
        """
        dr        = db.time_record.get  (itemid, 'daily_record')
        ownerid   = db.daily_record.get (dr, 'user')
        clearance = clearance_by (db, ownerid)
        return userid in clearance
    # end def approval_for_time_record

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'time_wp'
        , check       = ok_work_package
        , description = "User is allowed to edit (some of) their own user wps"
        , properties  = \
            ( 'responsible', 'description', 'cost_center'
            , 'time_start', 'time_end', 'bookers', 'planned_effort'
            )
        )
    db.security.addPermissionToRole('User', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'time_wp'
        , check       = is_project_owner_of_wp
        , description = "User is allowed to edit name and wp_no"
        , properties  = ('name', 'wp_no')
        )
    db.security.addPermissionToRole('User', p)

    for perm in 'View', 'Edit' :
        p = db.security.addPermission \
            ( name        = perm
            , klass       = 'daily_record'
            , check       = ok_daily_record
            , description = 'User and approver may edit daily_records'
            )
        db.security.addPermissionToRole('User', p)

        p = db.security.addPermission \
            ( name        = perm
            , klass       = 'time_record'
            , check       = own_time_record
            , description = 'User may edit own time_records'
            )
        db.security.addPermissionToRole('User', p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_record'
        , check       = approval_for_time_record
        , description = 'Supervisor may see time record'
        )
    db.security.addPermissionToRole('User', p)
# end def security
