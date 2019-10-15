# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-14 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    company
#
# Purpose
#    Schema definitions for a company.
#
#--
#

from roundup.hyperdb import Class
from common          import tt_clearance_by
from freeze          import frozen
from roundup.date    import Interval
from schemacfg       import schemadef
import sum_common
import common
import user_dynamic

def init \
    ( db
    , Class
    , String
    , Date
    , Link
    , Multilink
    , Boolean
    , Number
    , Department_Class
    , Location_Class
    , Organisation_Class
    , Time_Project_Status_Class
    , SAP_CC_Class
    , ** kw
    ) :
    export = {}
    cost_center = Class \
        ( db
        , ''"cost_center"
        , name                  = String    ()
        , description           = String    ()
        , status                = Link      ("cost_center_status")
        , cost_center_group     = Link      ("cost_center_group")
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
        , required_overtime     = Boolean   ()
        , weekend_allowed       = Boolean   ()
        , time_record           = Multilink ("time_record",   do_journal = "no")
        , tr_duration_ok        = Number    ()
        )
    daily_record.setlabelprop ('date')

    daily_record_freeze = Class \
        ( db
        , ''"daily_record_freeze"
        , user                  = Link      ("user",          do_journal = "no")
        , date                  = Date      (offset = 0)
        , frozen                = Boolean   ()
	, achieved_hours        = Number    ()
	, balance               = Number    ()
	, validity_date         = Date      ()
        , week_balance          = Number    ()
        , month_balance         = Number    ()
        , month_validity_date   = Date      (offset = 0)
        )
    daily_record_freeze.setlabelprop ('date')

    overtime_correction = Class \
        ( db
        , ''"overtime_correction"
        , user                  = Link      ("user",          do_journal = "no")
        , date                  = Date      (offset = 0)
        , value                 = Number    ()
        , comment               = String    ()
        )
    overtime_correction.setlabelprop ('date')

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
        , organisation          = Link      ("organisation")
        , time_wp               = Link      ("time_wp")
        , time_wp_group         = Link      ("time_wp_group")
        , cost_center           = Link      ("cost_center")
        , cost_center_group     = Link      ("cost_center_group")
        , time_project          = Link      ("time_project")
        , summary_type          = Link      ("summary_type")
        , summary               = Boolean   ()
        , status                = Link      ("daily_record_status")
        , show_empty            = Boolean   ()
        , show_all_users        = Boolean   ()
        , planned_effort        = Number    ()
        , show_missing          = Boolean   ()
        , all_in                = Boolean   ()
        , op_project            = Boolean   ()
        , reporting_group       = Link      ("reporting_group")
        , product_family        = Link      ("product_family")
        , project_type          = Link      ("project_type")
        , sap_cc                = Link      ("sap_cc")
        , time_wp_summary_no    = Link      ("time_wp_summary_no")
        )

    reporting_group = Class \
        ( db
        , ''"reporting_group"
        , name                  = String    ()
        , description           = String    ()
        , responsible           = Link      ("user")
        )
    reporting_group.setkey ("name")

    product_family = Class \
        ( db
        , ''"product_family"
        , name                  = String    ()
        , description           = String    ()
        , responsible           = Link      ("user")
        )
    product_family.setkey ("name")

    project_type = Class \
        ( db
        , ''"project_type"
        , name                  = String    ()
        , order                 = Number    ()
        )
    project_type.setkey ("name")

    summary_type = Class \
        ( db
        , ''"summary_type"
        , name                  = String    ()
        , is_staff              = Boolean   ()
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

    time_report = Class \
        ( db
        , ''"time_report"
        , file                  = Link      ("file")
        , time_project          = Link      ("time_project")
        , last_updated          = Date      ()
        )

    class Time_Project_Class (kw ['Time_Project_Class']) :
        """Add attributes to existing Time_Project_Class class."""

        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( approval_hr           = Boolean   ()
                , approval_required     = Boolean   ()
                , is_public_holiday     = Boolean   ()
                , is_special_leave      = Boolean   ()
                , is_vacation           = Boolean   ()
                , max_hours             = Number    ()
                , nosy                  = Multilink ("user")
                , no_overtime           = Boolean   ()
                , no_overtime_day       = Boolean   ()
                , overtime_reduction    = Boolean   ()
                , planned_effort        = Number    ()
                , product_family        = Multilink ("product_family")
                , project_type          = Link      ("project_type")
                , reporting_group       = Multilink ("reporting_group")
                , work_location         = Link      ("work_location")
                , cost_center           = Link      ("cost_center")
                , only_hours            = Boolean   ()
                , op_project            = Boolean   ()
                )
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class Time_Project_Class
    Time_Project_Class (db, ''"time_project")

    Time_Project_Status_Class (db, ''"time_project_status")

    SAP_CC_Class (db, ''"sap_cc")

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
        , is_public             = Boolean   ()
        , has_expiration_date   = Boolean   ()
        , time_wp_summary_no    = Link      ("time_wp_summary_no")
        , epic_key              = String    ()
        )

    time_wp_summary_no = Class \
        ( db, ''"time_wp_summary_no"
        , name                  = String    ()
        , order                 = Number    ()
        )
    time_wp_summary_no.setkey ("name")

    time_wp_group = Class \
        ( db
        , ''"time_wp_group"
        , name                  = String    ()
        , description           = String    ()
        , wps                   = Multilink ("time_wp")
        )
    time_wp_group.setkey ("name")

    overtime_period = Class \
        ( db
        , ''"overtime_period"
        , name                  = String    ()
        , order                 = Number    ()
        , weekly                = Boolean   ()
        , months                = Number    ()
        , required_overtime     = Boolean   ()
        )
    overtime_period.setkey ("name")

    vac_aliq = Class \
        ( db
        , ''"vac_aliq"
        , name                  = String    ()
        )
    vac_aliq.setkey ("name")

    ud = Class \
        ( db
        , ''"user_dynamic"
        , user                  = Link      ("user")
        , valid_from            = Date      (offset = 0)
        , valid_to              = Date      (offset = 0)
        , booking_allowed       = Boolean   ()
        , travel_full           = Boolean   ()
        , durations_allowed     = Boolean   ()
        , weekend_allowed       = Boolean   ()
        , vacation_yearly       = Number    ()
        , vacation_month        = Number    ()
        , vacation_day          = Number    ()
        , contract_type         = Link      ('contract_type', do_journal = "no")
        , daily_worktime        = Number    ()
        , weekly_hours          = Number    ()
        , supp_weekly_hours     = Number    ()
        , supp_per_period       = Number    ()
        , hours_mon             = Number    ()
        , hours_tue             = Number    ()
        , hours_wed             = Number    ()
        , hours_thu             = Number    ()
        , hours_fri             = Number    ()
        , hours_sat             = Number    ()
        , hours_sun             = Number    ()
        , org_location          = Link      ("org_location", do_journal = "no")
        , department            = Link      ("department",   do_journal = "no")
        , all_in                = Boolean   ()
        , additional_hours      = Number    ()
        , overtime_period       = Link      ( "overtime_period"
                                            , do_journal = "no"
                                            )
        , sap_cc                = Link      ("sap_cc")
        , max_flexitime         = Number    ()
        , vac_aliq              = Link      ("vac_aliq",     do_journal = "no")
        )

    leave_status = Class \
        ( db
        , ''"leave_status"
        , name                  = String ()
        , order                 = Number ()
        , transitions           = Multilink ("leave_status")
        )
    leave_status.setkey ("name")

    contract_type = Class \
        ( db
        , ''"contract_type"
        , name                  = String ()
        , order                 = Number ()
        , description           = String ()
        )

    leave_submission = Class \
        ( db
        , ''"leave_submission"
        , user                  = Link      ("user")
        , first_day             = Date      (offset = 0)
        , last_day              = Date      (offset = 0)
        , status                = Link      ("leave_status")
        , time_wp               = Link      ("time_wp")
        , comment               = String    ()
        , comment_cancel        = String    ()
        , approval_hr           = Boolean   () # only for queries
        )

    # Remaining vacation starting with given date if absolute is True,
    # Interpreted as relative correction if absolute = False, relative
    # to last vacation. Note that to start vacation reporting at least
    # one starting vacation_correction record with absolute = True must
    # exist.  Vacation reporting is started with that date. Note that
    # the date does *not* belong to the computation, to start reporting
    # with 2014-01-01 a vacation_correction record with exactly that
    # date must exist and the carry-over from the last year is in
    # 'days'.
    vacation_correction = Class \
        ( db
        , ''"vacation_correction"
        , user                  = Link      ("user")
        , date                  = Date      (offset = 0)
        , absolute              = Boolean   ()
        , days                  = Number    ()
        , contract_type         = Link      ('contract_type')
        , comment               = String    ()
        )

    # Only for reporting mask, no records will ever be created
    vacation_report = Class \
        ( db
        , ''"vacation_report"
        , user                  = Link      ("user")
        , supervisor            = Link      ("user")
        , department            = Link      ("department")
        , organisation          = Link      ("organisation")
        , org_location          = Link      ("org_location")
        , time_project          = Link      ("time_project")
        , date                  = Date      (offset = 0)
        , additional_submitted  = String    ()
        , approved_submissions  = String    ()
        , flexi_time            = String    ()
        , flexi_sub             = String    ()
        , flexi_max             = String    ()
        , flexi_rem             = String    ()
        , special_leave         = String    ()
        , special_sub           = String    ()
        , show_obsolete         = Boolean   ()
        )

    absence_type = Class \
        ( db
        , ''"absence_type"
        , code                  = String    ()
        , description           = String    ()
        , cssclass              = String    ()
        )
    absence_type.setkey ("code")

    absence = Class \
        ( db
        , ''"absence"
        , absence_type          = Link      ("absence_type")
        , first_day             = Date      (offset = 0)
        , last_day              = Date      (offset = 0)
        , user                  = Link      ("user")
        )

    # Only for queries
    timesheet = Class \
        ( db
        , ''"timesheet"
        , first_day             = Date      (offset = 0)
        , last_day              = Date      (offset = 0)
        , user                  = Link      ("user")
        , department            = Link      ("department")
        , supervisor            = Link      ("user")
        )

    work_location = Class \
        ( db
        , ''"work_location"
        , code                  = String    ()
        , description           = String    ()
        )
    work_location.setkey ("code")

    class User_Class (kw ['User_Class']) :
        """ add some attrs to user class
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( timing_info            = Boolean   ()
                , timetracking_by        = Link      ("user")
                , aux_username           = String    ()
                )
            kw ['User_Class'].__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Class
    export.update (dict (User_Class = User_Class))

    class Org_Location_Class (kw ['Org_Location_Class']) :
        """ Add some attributes needed for time tracker
        """
        def __init__ (self, db, classname, ** properties) :
            ancestor = kw ['Org_Location_Class']
            self.update_properties \
                ( vacation_legal_year        = Boolean   ()
                , vacation_yearly            = Number    ()
                , do_leave_process           = Boolean   ()
                , vac_aliq                   = Link      ("vac_aliq")
                )
            ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Org_Location_Class
    export.update (dict (Org_Location_Class = Org_Location_Class))
    Org_Location_Class (db, ''"org_location")

    # Some classes defined elsewhere which are required (and possibly
    # extended in several other include files)
    Department_Class   (db, ''"department")
    Location_Class     (db, ''"location")
    Organisation_Class (db, ''"organisation")

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
        , ("HR-vacation",       "May approve vacation and special leave")
        , ("HR-leave-approval", "Approve paid vacation beyond normal vacation")
        , ("staff-report",      "May view staff report")
        , ("Controlling",       "Controlling")
        , ("Summary_View",      "View full summary report and all WPs")
        , ("Office",            "Office")
        , ("Time-Report",       "External time reports")
        ]

    #     classname
    # allowed to view   /  edit
    # For daily_record, time_record, additional restrictions apply
    classes = \
        [ ( "absence"
          , ["User"]
          , ["Office"]
          )
        , ( "absence_type"
          , ["User"]
          , ["Office"]
          )
        , ( "contract_type"
          , ["HR", "HR-vacation", "HR-leave-approval", "controlling"]
          , ["HR-vacation"]
          )
        , ( "cost_center"
          , ["User"]
          , ["Controlling"]
          )
        , ( "cost_center_group"
          , ["User"]
          , ["Controlling"]
          )
        , ( "cost_center_status"
          , ["User"]
          , ["Controlling"]
          )
        , ( "daily_record"
          , ["HR", "Controlling"]
          , []
          )
        , ( "daily_record_freeze"
          , ["HR", "Controlling"]
          , []
          )
        , ( "daily_record_status"
          , ["User"]
          , []
          )
        , ( "leave_status"
          , ["User"]
          , []
          )
        , ( "timesheet"
          , ["User"]
          , []
          )
        , ( "leave_submission"
          , ["HR", "HR-vacation", "HR-leave-approval", "controlling"]
          , ["HR-vacation"]
          )
        , ( "overtime_correction"
          , ["HR", "Controlling"]
          , []
          )
        , ( "overtime_period"
          , ["User"]
          , []
          )
        , ( "public_holiday"
          , ["User"]
          , ["HR", "Controlling"]
          )
        , ( "product_family"
          , ["User"]
          , ["HR", "Controlling"]
          )
        , ( "project_type"
          , ["User"]
          , ["HR", "Controlling"]
          )
        , ( "reporting_group"
          , ["User"]
          , ["HR", "Controlling"]
          )
        , ( "sap_cc"
          , ["User"]
          , ["HR", "Controlling"]
          )
        , ( "summary_report"
          , ["User"]
          , []
          )
        , ( "summary_type"
          , ["User"]
          , []
          )
        , ( "time_activity"
          , ["User"]
          , ["Controlling"]
          )
        , ( "time_record"
          , ["HR", "Controlling"]
          , ["HR", "Controlling"]
          )
        , ( "time_wp_group"
          , ["User"]
          , ["Project"]
          )
        , ( "time_wp"
          , ["Project_View", "Project", "Controlling"]
          , ["Project"]
          )
        , ( "time_wp_summary_no"
          , ["User"]
          , []
          )
        , ( "user_dynamic"
          , ["HR"]
          , []
          )
        , ( "vac_aliq"
          , ["User"]
          , []
          )
        , ( "vacation_correction"
          , ["HR", "HR-vacation", "HR-leave-approval", "controlling"]
          , ["HR-vacation"]
          )
        , ( "vacation_report"
          , ["User"]
          , []
          )
        , ( "work_location"
          , ["User"]
          , ["Controlling"]
          )
        , ( "time_report"
          , ["Time-Report", "Controlling", "Project", "Project_View"]
          , ["Time-Report"]
          )
        ]

    prop_perms = \
        [ ( "daily_record", "Edit", ["HR", "Controlling"]
          , ("status", "time_record")
          )
        , ( "daily_record", "Edit", ["HR"]
          , ("required_overtime", "weekend_allowed")
          )
        , ( "leave_submission", "Edit", ["HR-leave-approval"]
          , ("status",)
          )
        , ( "time_project", "Edit", ["Project"]
          , ( "max_hours", "op_project", "planned_effort"
            , "product_family", "project_type", "reporting_group"
            , "work_location", "infosec_req"
            )
          )
        , ( "time_project", "Edit", ["HR"]
          , ( "is_public_holiday", "is_vacation", "is_special_leave"
            , "no_overtime", "no_overtime_day"
            , "overtime_reduction", "approval_required", "approval_hr"
            )
          )
        , ( "time_wp",      "Edit", ["Controlling"]
          , ( "project",)
          )
        , ( "user_dynamic", "View", ["Controlling"]
          , ( "id", "sap_cc", "user", "valid_from", "valid_to")
          )
        , ( "user",         "View", ["User"]
          , ( "timetracking_by",)
          )
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)

    # For the following the use is regulated by auditors.
    db.security.addPermissionToRole ('User', 'Create', 'time_record')
    db.security.addPermissionToRole ('User', 'Create', 'daily_record')
    db.security.addPermissionToRole ('User', 'Create', 'leave_submission')
    schemadef.add_search_permission (db, 'leave_submission', 'User')
    schemadef.add_search_permission (db, 'daily_record', 'User')
    schemadef.add_search_permission (db, 'time_record', 'User')

    fixdoc = schemadef.security_doc_from_docstring

    def approver_daily_record (db, userid, itemid) :
        """User is allowed to edit daily record if he is supervisor.

           A negative itemid indicates that the record doesn't exist
           yet -- we allow creation in this case. Modification is only
           allowed by the supervisor.
        """
        if int (itemid) < 0 : # allow creation
            return True
        ownerid   = db.daily_record.get (itemid, 'user')
        if not ownerid :
            return False
        clearance = tt_clearance_by (db, ownerid)
        return userid in clearance
    # end def approver_daily_record

    def ok_daily_record (db, userid, itemid) :
        """User is allowed to access daily record if he is owner or
           supervisor or timetracking-by user.

           Determine if the user owns the daily record, a negative itemid
           indicates that the record doesn't exist yet -- we allow creation
           in this case. Modification is also allowed by the supervisor or
           the person to whom approvals are delegated.
        """
        ownerid   = db.daily_record.get (itemid, 'user')
        ttby      = db.user.get (ownerid, 'timetracking_by')
        if userid == ttby :
            return True
        return userid == ownerid or approver_daily_record (db, userid, itemid)
    # end def ok_daily_record

    def own_time_record (db, userid, itemid) :
        """User may edit own time_records.

           Determine if the user owns the daily record, a negative itemid
           indicates that the record doesn't exist yet -- we allow creation
           in this case.
        """
        if int (itemid) < 0 : # allow creation
            return True
        dr      = db.time_record.get  (itemid, 'daily_record')
        ownerid = db.daily_record.get (dr, 'user')
        return userid == ownerid
    # end def own_time_record

    def own_leave_submission (db, userid, itemid) :
        """ User may edit own leave submissions. """
        ownerid = db.leave_submission.get (itemid, 'user')
        return userid == ownerid
    # end def own_leave_submission

    def approval_for_leave_submission (db, userid, itemid) :
        """User is allowed to view leave submission if he is the supervisor
           or the person to whom approvals are delegated.

           Viewing is allowed by the supervisor or the person to whom
           approvals are delegated.
        """
        ownerid   = db.leave_submission.get (itemid, 'user')
        clearance = tt_clearance_by (db, ownerid)
        return userid in clearance
    # end def approval_for_time_record


    def may_see_time_record (db, userid, itemid) :
        # docstring is used to create composite doc for given check
        # function it is intended that it ends with "or"
        """User is allowed to see time record if he is allowed to see
           all details on work package or
        """
        dr = db.time_record.get (itemid, 'daily_record')
        wp = db.time_record.get (itemid, 'wp')
        if sum_common.daily_record_viewable (db, userid, dr) :
            return True
        if wp is None :
            return False
        return sum_common.time_wp_viewable (db, userid, wp)
    # end def may_see_time_record

    def may_see_daily_record (db, userid, itemid) :
        """ Users may see daily record if they may see one of the
            time_records for that day.
        """
        if int (itemid) < 0 :
            return False
        trs = db.time_record.filter (None, dict (daily_record = itemid))
        for tr in trs :
            if may_see_time_record (db, userid, tr) :
                return True
        return False
    # end def may_see_daily_record

    def is_project_owner_or_deputy (db, userid, itemid) :
        """User is allowed to edit workpackage if he is time category
           owner or deputy.
        """
        if int (itemid) < 0 :
            return False
        prid    = db.time_wp.get (itemid, 'project')
        project = db.time_project.getnode (prid)
        return userid == project.responsible or userid == project.deputy
    # end def is_project_owner_of_wp

    def ok_work_package (db, userid, itemid) :
        """User is allowed to view/edit workpackage if he is owner or project
           responsible/deputy.

           Check if user is responsible for wp or if user is responsible
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

    def time_project_responsible_and_open (db, userid, itemid) :
        """ User is allowed to edit time category if the status is
            "Open" and he is responsible for the time category.

            Check if the user is responsible for the given time_project
            if yes *and* the time_project is in status open, the user
            may edit several fields.
        """
        if int (itemid) < 0 :
            return False
        ownerid = db.time_project.get (itemid, 'responsible')
        open    = db.time_project_status.lookup ('Open')
        status  = db.time_project.get (itemid, 'status')
        if ownerid == userid and status == open :
            return True
        return False
    # end def time_project_responsible_and_open

    def approval_for_time_record (db, userid, itemid) :
        """User is allowed to view time record if he is the supervisor
           or the person to whom approvals are delegated.

           Viewing is allowed by the supervisor or the person to whom
           approvals are delegated.
        """
        dr        = db.time_record.get  (itemid, 'daily_record')
        ownerid   = db.daily_record.get (dr, 'user')
        clearance = tt_clearance_by (db, ownerid)
        return userid in clearance
    # end def approval_for_time_record

    def overtime_thawed (db, userid, itemid) :
        """User is allowed to edit overtime correction if the overtime
           correction is not frozen.

           Check that no daily_record_freeze is active at date
        """
        oc = db.overtime_correction.getnode (itemid)
        return not frozen (db, oc.user, oc.date)
    # end def overtime_thawed

    def dr_freeze_last_frozen (db, userid, itemid) :
        """User is allowed to edit freeze record if not frozen at the
           given date.

           Check that no daily_record_freeze is active after date
        """
        df = db.daily_record_freeze.getnode (itemid)
        return not frozen (db, df.user, df.date + Interval ('1d'))
    # end def dr_freeze_last_frozen

    def dynuser_thawed (db, userid, itemid) :
        """User is allowed to edit dynamic user data if not frozen in
           validity span of dynamic user record
        """
        dyn = db.user_dynamic.getnode (itemid)
        return not frozen (db, dyn.user, dyn.valid_from)
    # end def dynuser_thawed

    def wp_admitted (db, userid, itemid) :
        """User is allowed to view selected fields in work package if
           booking is allowed for this user
        """
        wp = db.time_wp.getnode (itemid)
        if wp.is_public or userid in wp.bookers :
            return True
        # Get all users for which *this* user is in timetracking_by
        users = db.user.filter (None, dict (timetracking_by = userid))
        for u in users :
            if u in wp.bookers :
                return True
        return False
    # end def wp_admitted

    def project_admitted (db, userid, itemid) :
        """User is allowed to view selected fields if booking is allowed
           for at least one work package for this user
        """
        wps = db.time_wp.filter (None, dict (project = itemid))
        for wp in wps :
            if wp_admitted (db, userid, wp) :
                return True
        return False
    # end def project_admitted

    def project_or_wp_name_visible (db, userid, itemid) :
        """User is allowed to view work package and time category names
           if he/she is department manager or supervisor or has role HR
           or HR-Org-Location.
        """
        if common.user_has_role (db, userid, 'HR', 'HR-Org-Location') :
            return True
        if db.department.filter (None, dict (manager = userid)) :
            return True
        if db.user.filter (None, dict (supervisor = userid)) :
            return True
    # end def project_or_wp_name_visible

    def time_record_visible_for_hr_olo (db, userid, itemid) :
        """User is allowed to view time record data if he/she
           is in group HR-Org-Location and in the same Org-Location as
           the given user
        """
        did = db.time_record.get (itemid, 'daily_record')
        dr  = db.daily_record.getnode (did)
        return user_dynamic.hr_olo_role_for_this_user \
            (db, userid, dr.user, dr.date)
    # end def time_record_visible_for_hr_olo

    def user_dynamic_visible_for_hr_olo (db, userid, itemid) :
        """User is allowed to view dynamic user data if he/she
           is in group HR-Org-Location and in the same Org-Location as
           the given user
        """
        dyn = db.user_dynamic.getnode (itemid)
        return user_dynamic.hr_olo_role_for_this_user_dyn (db, userid, dyn)
    # end def user_dynamic_visible_for_hr_olo

    def overtime_corr_visible_for_hr_olo (db, userid, itemid) :
        """User is allowed to view overtime information if he/she
           is in group HR-Org-Location and in the same Org-Location as
           the given user
        """
        ot = db.overtime_correction.getnode (itemid)
        return user_dynamic.hr_olo_role_for_this_user \
            (db, userid, ot.user, ot.date)
    # end def overtime_corr_visible_for_hr_olo

    def overtime_corr_visible_for_user (db, userid, itemid) :
        """User is allowed to view their own overtime information
        """
        ot = db.overtime_correction.getnode (itemid)
        if ot.user == userid :
            return True
    # end def overtime_corr_visible_for_user

    def dr_freeze_visible_for_hr_olo (db, userid, itemid) :
        """User is allowed to view freeze information if he/she
           is in group HR-Org-Location and in the same Org-Location as
           the given user
        """
        df = db.daily_record_freeze.getnode (itemid)
        return user_dynamic.hr_olo_role_for_this_user \
            (db, userid, df.user, df.date)
    # end def dr_freeze_visible_for_hr_olo

    def time_report_visible (db, userid, itemid) :
        """ User may see time report if reponsible or deputy of time
            project or on nosy list of time project.
        """
        trep = db.time_report.getnode (itemid)
        if not trep.time_project :
            return False
        tp   = db.time_project.getnode (trep.time_project)
        if userid == tp.responsible or userid == tp.deputy :
            return True
        if userid in tp.nosy :
            return True
        return False
    # end def time_report_visible

    def own_file (db, userid, itemid) :
        """ User may edit own file (file created by user)
        """
        f = db.file.getnode (itemid)
        if userid == f.creator :
            return True
        return False
    # end def own_file

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'file'
        , check       = own_file
        , description = fixdoc (own_file.__doc__)
        )
    db.security.addPermissionToRole ('Time-Report', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'time_wp'
        , check       = ok_work_package
        , description = fixdoc (ok_work_package.__doc__)
        , properties  = \
            ( 'description'
            , 'time_start', 'time_end', 'bookers', 'planned_effort'
            , 'time_wp_summary_no', 'epic_key'
            )
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_wp'
        , check       = sum_common.time_wp_viewable
        , description = fixdoc (sum_common.time_wp_viewable.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'time_wp'
        , check       = is_project_owner_or_deputy
        , description = fixdoc (is_project_owner_or_deputy.__doc__)
        , properties  = \
            ( 'name', 'responsible', 'wp_no', 'cost_center'
            , 'time_wp_summary_no', 'is_public'
            )
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'time_project'
        , check       = time_project_responsible_and_open
        , description = fixdoc (time_project_responsible_and_open.__doc__)
        , properties  = ('deputy', 'planned_effort', 'nosy')
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'daily_record'
        , check       = ok_daily_record
        , description = fixdoc (ok_daily_record.__doc__)
        , properties  = ('status', 'time_record')
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'daily_record'
        , check       = ok_daily_record
        , description = fixdoc (ok_daily_record.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    for perm in 'View', 'Edit' :

        p = db.security.addPermission \
            ( name        = perm
            , klass       = 'daily_record'
            , check       = approver_daily_record
            , description = fixdoc (approver_daily_record.__doc__)
            , properties  = ('required_overtime',)
            )
        #db.security.addPermissionToRole ('User', p)

        p = db.security.addPermission \
            ( name        = perm
            , klass       = 'time_record'
            , check       = own_time_record
            , description = fixdoc (own_time_record.__doc__)
            )
        db.security.addPermissionToRole ('User', p)

        p = db.security.addPermission \
            ( name        = perm
            , klass       = 'leave_submission'
            , check       = own_leave_submission
            , description = fixdoc (own_leave_submission.__doc__)
            , properties  = \
                ( 'user', 'first_day', 'last_day', 'status', 'time_wp'
                , 'comment', 'comment_cancel'
                )
            )
        db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'leave_submission'
        , check       = approval_for_leave_submission
        , description = fixdoc (approval_for_leave_submission.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'leave_submission'
        , check       = approval_for_leave_submission
        , description = fixdoc (approval_for_leave_submission.__doc__)
        , properties  = ('status',)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_record'
        , check       = approval_for_time_record
        , description = fixdoc (approval_for_time_record.__doc__)
        )
    db.security.addPermissionToRole ('User', p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'daily_record'
        , check       = sum_common.daily_record_viewable
        , description = fixdoc (sum_common.daily_record_viewable.__doc__)
        )
    db.security.addPermissionToRole ('User', p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_record'
        , check       = may_see_time_record
        , description = ' '.join
            (( fixdoc (may_see_time_record.__doc__)
             , fixdoc (sum_common.daily_record_viewable.__doc__)
            ))
        )
    db.security.addPermissionToRole ('User', p)
    schemadef.add_search_permission (db, 'time_record', 'User')
    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'overtime_correction'
        , check       = overtime_thawed
        , description = fixdoc (overtime_thawed.__doc__)
        )
    db.security.addPermissionToRole ('HR', p)
    db.security.addPermissionToRole ('HR', 'Create', 'overtime_correction')
    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'daily_record_freeze'
        , check       = dr_freeze_last_frozen
        , description = fixdoc (dr_freeze_last_frozen.__doc__)
        , properties  = ('frozen',)
        )
    db.security.addPermissionToRole ('HR', p)
    db.security.addPermissionToRole ('HR', 'Create', 'daily_record_freeze')
    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'user_dynamic'
        , check       = dynuser_thawed
        , description = fixdoc (dynuser_thawed.__doc__)
        )
    db.security.addPermissionToRole ('HR', p)
    db.security.addPermissionToRole ('HR', 'Create', 'user_dynamic')
    wp_properties = \
        ( 'name', 'wp_no', 'description', 'responsible', 'project'
        , 'time_start', 'time_end', 'durations_allowed', 'travel'
        , 'cost_center', 'creation', 'creator', 'activity', 'actor', 'id'
        , 'has_expiration_date', 'time_wp_summary_no', 'epic_key'
        , 'is_public'
        )
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_wp'
        , check       = wp_admitted
        , description = fixdoc (wp_admitted.__doc__)
        , properties  = wp_properties
        )
    db.security.addPermissionToRole ('User', p)
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'time_wp'
        , properties  = wp_properties + ('bookers',)
        )
    db.security.addPermissionToRole ('User', p)
    schemadef.add_search_permission (db, 'time_wp', 'User', wp_properties)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_project'
        , check       = sum_common.time_project_viewable
        , description = fixdoc (sum_common.time_project_viewable.__doc__)
        )
    db.security.addPermissionToRole ('User', p)
    tp_properties = \
        ( 'name', 'description', 'responsible', 'deputy', 'organisation'
        , 'status', 'work_location', 'op_project', 'id'
        , 'is_public_holiday', 'is_vacation', 'is_special_leave'
        , 'creation', 'creator', 'activity', 'actor'
        , 'cost_center', 'overtime_reduction'
        , 'product_family', 'project_type', 'reporting_group'
        )
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_project'
        , check       = project_admitted
        , description = fixdoc (project_admitted.__doc__)
        , properties  = tp_properties
        )
    db.security.addPermissionToRole ('User', p)
    # Search permission
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'time_project'
        , properties  = tp_properties
        )
    db.security.addPermissionToRole ('User', p)

    for klass in 'time_project', 'time_wp' :
        p = db.security.addPermission \
            ( name        = 'View'
            , klass       = klass
            , check       = project_or_wp_name_visible
            , description = fixdoc (project_or_wp_name_visible.__doc__)
            , properties  = ('name', 'project')
            )
        db.security.addPermissionToRole ('User', p)
    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'overtime_period'
        , properties  = ('name', 'order')
        )
    db.security.addPermissionToRole ('HR', p)
    db.security.addPermissionToRole ('HR', 'Create', 'overtime_period')

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_record'
        , check       = time_record_visible_for_hr_olo
        , description = fixdoc (time_record_visible_for_hr_olo.__doc__)
        )
    db.security.addPermissionToRole ('HR-Org-Location', p)
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'time_record'
        )
    db.security.addPermissionToRole ('HR-Org-Location', p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'user_dynamic'
        , check       = user_dynamic_visible_for_hr_olo
        , description = fixdoc (user_dynamic_visible_for_hr_olo.__doc__)
        )
    db.security.addPermissionToRole ('HR-Org-Location', p)
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'user_dynamic'
        )
    db.security.addPermissionToRole ('HR-Org-Location', p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'overtime_correction'
        , check       = overtime_corr_visible_for_user
        , description = fixdoc (overtime_corr_visible_for_user.__doc__)
        )
    db.security.addPermissionToRole ('User', p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'overtime_correction'
        , check       = overtime_corr_visible_for_hr_olo
        , description = fixdoc (overtime_corr_visible_for_hr_olo.__doc__)
        )
    db.security.addPermissionToRole ('HR-Org-Location', p)
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'overtime_correction'
        )
    db.security.addPermissionToRole ('HR-Org-Location', p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'daily_record_freeze'
        , check       = dr_freeze_visible_for_hr_olo
        , description = fixdoc (dr_freeze_visible_for_hr_olo.__doc__)
        )
    db.security.addPermissionToRole ('HR-Org-Location', p)
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'daily_record_freeze'
        )
    db.security.addPermissionToRole ('HR-Org-Location', p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'daily_record'
        , check       = may_see_daily_record
        , description = fixdoc (may_see_daily_record.__doc__)
        )
    db.security.addPermissionToRole ('User', p)
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'time_report'
        , check       = time_report_visible
        , description = fixdoc (time_report_visible.__doc__)
        )
    db.security.addPermissionToRole ('User', p)
# end def security
