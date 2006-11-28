# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    complex
#
# Purpose
#    Schema definitions for a complex tracker with many classes
#
#--
#

import schemadef
import ext_issue

def init \
    ( db
    , Class
    , Ext_Issue_Class
    , String
    , Date
    , Link
    , Multilink
    , Boolean
    , Number
    , ** kw
    ) :

    severity = Class \
        ( db
        , ''"severity"
        , name                  = String    ()
        , order                 = String    ()
        )
    severity.setkey ("name")

    milestone_class = Class \
        ( db
        , ''"milestone"
        , name                  = String    ()
        , description           = String    ()
        , planned               = Date      ()
        , reached               = Date      ()
        , order                 = Number    ()
        # the release this milestone belongs to - needed for reactors
        # updating the releases "status" field,  which represents the last
        # reached milestone.
        , release               = Link      ("release")
        )

    task_status = Class \
        ( db
        , ''"task_status"
        , name                  = String    ()
        , description           = String    ()
        , abbreviation          = String    ()
        , transitions           = Multilink ("task_status")
        , order                 = String    ()
        )
    task_status.setkey ("name")

    task_kind = Class \
        ( db
        , ''"task_kind"
        , name                  = String    ()
        , description           = String    ()
        , order                 = String    ()
        )
    task_kind.setkey ("name")

    feature_status = Class \
        ( db
        , ''"feature_status"
        , name                  = String    ()
        , description           = String    ()
        , abbreviation          = String    ()
        , transitions           = Multilink ("feature_status")
        , order                 = String    ()
        )
    feature_status.setkey ("name")

    defect_status = Class \
        ( db
        , ''"defect_status"
        , name                  = String    ()
        , description           = String    ()
        , abbreviation          = String    ()
        , cert                  = Boolean   ()
        , cert_transitions      = Multilink ("defect_status")
        , transitions           = Multilink ("defect_status")
        , order                 = String    ()
        )
    defect_status.setkey ("name")

    action_item_status = Class \
        ( db
        , ''"action_item_status"
        , name                  = String    ()
        , description           = String    ()
        , order                 = String    ()
        )
    action_item_status.setkey ("name")

    review_status = Class \
        ( db
        , ''"review_status"
        , name                  = String    ()
        , description           = String    ()
        , order                 = String    ()
        )
    review_status.setkey ("name")

    comment_status = Class \
        ( db
        , ''"comment_status"
        , name                  = String    ()
        , description           = String    ()
        , transitions           = Multilink ("comment_status")
        , order                 = String    ()
        )
    comment_status.setkey ("name")

    document_status = Class \
        ( db
        , ''"document_status"
        , name                  = String    ()
        , description           = String    ()
        , abbreviation          = String    ()
        , transitions           = Multilink ("document_status")
        , order                 = String    ()
        )
    document_status.setkey ("name")

    document_type = Class \
        ( db
        , ''"document_type"
        , name                  = String    ()
        , description           = String    ()
        , order                 = String    ()
        )
    document_type.setkey ("name")

    product = Class \
        ( db
        , ''"product"
        , name                  = String    ()
        , description           = String    ()
        , responsible           = Link      ("user")
        , nosy                  = Multilink ("user")
        # needs to be set, to let the "defect report" mechanism allow to
        # mark some defect against a specific product as belonging to
        # "cert".
        , certifiable           = Boolean   ()
        # XXX: no "order", gets sorted by "name" automatically.
        )
    product.setkey ("name")

    # Ext_Issue_Class automatically gets these properties:
    #   title       = String    ()
    #   responsible = Link      ("user")
    #   nosy        = Multilink ("user")
    #   messages    = Multilink ("msg")
    #   (it also gets the Class properties creation, activity and creator)

    meeting = Ext_Issue_Class \
        ( db
        , ''"meeting"
        , files                 = Multilink ("file")
        )

    action_item = Ext_Issue_Class \
        ( db
        , ''"action_item"
        , files                 = Multilink ("file")
        , meeting               = Link      ("meeting")
        , status                = Link      ("action_item_status")
        , deadline              = Date      ()
        )

    document = Ext_Issue_Class \
        ( db
        , ''"document"
        , files                 = Multilink ("file")
        , status                = Link      ("document_status")
        , release               = Link      ("release")
        , type                  = Link      ("document_type")
        )

    release = Ext_Issue_Class \
        ( db
        , ''"release"
        # just to show something in the pop-up, gets set to the last reached
        # milestone
        , status                = Link      ("milestone")
        , documents             = Multilink ("document")
        , features              = Multilink ("feature")
        , planned_fixes         = Multilink ("defect")
        , bugs                  = Multilink ("defect")
        # Note: they get added automatically on creation of a new release
        # (by the auditor -
        , milestones            = Multilink ("milestone")
        )

    feature = Ext_Issue_Class \
        ( db
        , ''"feature"
        , stakeholder           = String    () # some freeform text
        # note: "status" is simplified to be only one of "raised",
        #       "suspended", "open" and "completed", all other *.accepted
        #       states can be computed directly from the status of the
        #       attached issues.
        #       There is now a seperate flag "test_ok" which covers the state
        #       of the testcases, and gets set automatically by a detector
        #       when the "test_ok" flag of some attached "testcase" changes.
        #       Changes to the "testcase"s "test_ok" are only allowed by the
        #       iv&v team, and are set manually at begin and later on this
        #       should be automatically, based on the success of a given
        #       testcase (identified by the issue no.).
        , status                = Link      ("feature_status")
        # gets set automatically by a detector depending on the testcases
        # test_ok switch:
        , test_ok               = Boolean   ()
        , tasks                 = Multilink ("task")
        , depends               = Multilink ("feature")
        , needs                 = Multilink ("feature")
        , release               = Link      ("release")
        , defects               = Multilink ("defect")
        , composed_of           = Multilink ("feature")
        , part_of               = Link      ("feature")
        , planned_begin         = Date      () # automatically by import
        , planned_end           = Date      () # automatically by import
        , actual_begin          = Date      () # automatically by status
        , actual_end            = Date      () # change of workpackages
        )

    task = Ext_Issue_Class \
        ( db
        , ''"task"
        , status                = Link      ("task_status")
        , kind                  = Link      ("task_kind")
        , effort                = Number    () # not Interval, as it's
                                               # actually in workingdays
        , depends               = Multilink ("task")
        , needs                 = Multilink ("task")
        , files                 = Multilink ("file")
        , feature               = Link      ("feature")
        , defects               = Multilink ("defect")
        , test_ok               = Boolean   () # if kind == "testcase"
        , planned_begin         = Date      () #
        , planned_end           = Date      () # == durchlaufzeit 5d
        , actual_begin          = Date      () #
        , actual_end            = Date      () # == tatsächliche dauer 2h
        , estimated_begin       = Date      () #
        , estimated_end         = Date      () # == geschätze dauer 8w
        )

    defect = Ext_Issue_Class \
        ( db
        , ''"defect"
        , status                = Link      ("defect_status")
        , superseder            = Link      ("defect")
        , cert                  = Boolean   ()
        # in which "release" it gets repaired.  i.e. it is in the
        # "planned_fixes" of that release:
        , solved_in_release     = Link      ("release")
        # where it was initially found.  "solved_in_release" is initially
        # set to "found_in_release":
        , found_in_release      = Link      ("release")
        , estimated_effort      = Number    ()
        # currently optional, but the opinions differ if it is generally
        # good to only say how long does it take, or to give some point in
        # time where it is actually fixed... mph thinks that the
        # estimated_effort is best - and gives some rough estimation on how
        # much time we actually need to add for big-fixing. in tal's opinion
        # it is important to know when it will be ready. but the past showed
        # that "deadlines" in general are a bad idea - as they always point
        # to some point back in time ;):
        , fixed_until           = Date      ()
        , severity              = Link      ("severity")
        , product               = Link      ("product")
        , version               = String    ()
        , files                 = Multilink ("file")
        , fixed_in              = String    ()
        , files_affected        = String    () # XXX only cert ???
        , closed                = Date      ()
        # if it opens again, than we have a shortcut to who actually closed
        # it last time. as we are also setting the "closed" date for this,
        # we can also set the "closer" here:
        , closer                = Link      ("user")
        , belongs_to_feature    = Link      ("feature") # if known
        , belongs_to_task       = Link      ("task")    # if known
        )

    Ext_Issue_Class \
        ( db
        , ''"review"
        # `moderator` is implemented with `responsible`
        , status                = Link      ("review_status")
        , authors               = Multilink ("user")
        , qa_representative     = Link      ("user")
        , recorder              = Link      ("user")
        , peer_reviewers        = Multilink ("user")
        , opt_reviewers         = Multilink ("user")
        , cut_off_date          = Date      ()
        , final_meeting_date    = Date      ()
        , files                 = Multilink ("file")
        , announcements         = Multilink ("announcement")
        )

    Ext_Issue_Class \
        ( db
        , ''"announcement"
        , version               = String    ()
        , meeting_room          = Link      ("meeting_room")
        , comments              = Multilink ("comment")
        , review                = Link      ("review")
        , status                = Link      ("review_status")
        , files                 = Multilink ("file")
        )

    Ext_Issue_Class \
        ( db
        , ''"comment"
        , severity              = Link      ("severity")
        , status                = Link      ("comment_status")
        , review                = Link      ("review")
        , announcement          = Link      ("announcement")
        , file_name             = String    ()
        , line_number           = String    ()
        )

# end def init

def security (db, **kw) :
    #
    # SECURITY SETTINGS
    #
    # See the configuration and customisation document for information
    # about security setup.
    # Assign the access and edit Permissions for issue, file and message
    # to regular users now

    #     classname        allowed to view   /  edit
    classes = \
        [
        # Issue Tracker classes:
        # no permission for now -- once we roll this out we want it enabled.
        #, ("action_item"         , ["User"],  ["User"            ])
        #, ("action_item_status"  , ["User"],  ["Admin"           ])
        #, ("announcement"        , ["User"],  ["User"            ])
        #, ("comment"             , ["User"],  ["User"            ])
        #, ("comment_status"      , ["User"],  ["Admin"           ])
        #, ("defect"              , ["User"],  ["User"            ])
        #, ("defect_status"       , ["User"],  ["Admin"           ])
        #, ("document"            , ["User"],  ["User"            ])
        #, ("document_status"     , ["User"],  ["Admin"           ])
        #, ("document_type"       , ["User"],  ["Admin"           ])
        #, ("feature"             , ["User"],  ["Releasemanager"  ])
        #, ("feature_status"      , ["User"],  ["Admin"           ])
        #, ("meeting"             , ["User"],  ["Admin"           ])
        #, ("milestone"           , ["User"],  ["Releasemanager"  ])
        #, ("product"             , ["User"],  ["Admin"           ])
        #, ("release"             , ["User"],  ["Releasemanager"  ])
        #, ("review"              , ["User"],  ["User"            ])
        #, ("review_status"       , ["User"],  ["Admin"           ])
        #, ("severity"            , ["User"],  ["Admin"           ])
        #, ("task"                , ["User"],  ["User"            ])
        #, ("task_kind"           , ["User"],  ["Admin"           ])
        #, ("task_status"         , ["User"],  ["Admin"           ])
        # Time-Tracking classes
        # For daily_record, time_record, additional restrictions apply
        ]

    roles = \
        [ ("CCB"           , "Member of Change Control Board")
        , ("Releasemanager", "Allowed to manage a SW Release")
        , ("IV&V"          , "Member of the IV&V Team."      )
        , ("halfweek"      , "User works only the half week" )
        ]


    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, ())

    # add permission "May Change Status" to role "CCB" and "Admin"
    p = db.security.addPermission (name="May Change Status", klass="defect")
    db.security.addPermissionToRole("CCB",   "May Change Status", "defect")
    db.security.addPermissionToRole("Admin", "May Change Status", "defect")

    # add permission "May publish Queries" to role "Releasemanager and "Admin"
    p = db.security.addPermission (name="May publish Queries", klass="query")
    db.security.addPermissionToRole \
        ("Releasemanager", "May publish Queries", "query")
    db.security.addPermissionToRole \
        ("Admin",          "May publish Queries", "query")

    # Add special permission for receiving nosy msgs. In this way we may
    # spare in-house people from receiving notifications from roundup,
    # more importantly we can add external listeners for nosy messages.
    nosy_classes = [ "document"
                   , "release"
                   , "feature"
                   , "task"
                   , "defect"
                   , "meeting"
                   , "action_item"
                   , "review"
                   , "announcement"
                   , "comment"
                   ]

    ext_issue.register_nosy_classes (db, nosy_classes)
# end def security
