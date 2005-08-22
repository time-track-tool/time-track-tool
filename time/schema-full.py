# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@mexx.mobile
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
#    schema
#
# Purpose
#    Specify the DB-Schema for the tttech2 issue tracker.
#
# Revision Dates
#    22-Jun-2004 (MPH) Creation
#     5-Jul-2004 (MPH) Work in progress.
#     6-Jul-2004 (MPH) Added `closed-obsolete` to `work_package_status`.
#    23-Jul-2004 (MPH) Removed `automatic` status changes from `feature_status`
#     5-Oct-2004 (MPH) Split `work_package` into `implementation_task` and
#                      `documentation_task`
#    14-Oct-2004 (pr) Major changes
#                      - `task` with `task_kind` instead of `*_task` and
#                        `testcase`
#                      - added `estimated_[begin|end]` to task
#                      - added `task` link to `defect` and vice versa, to
#                        have to possibility to add defects also to tasks
#                      - added `defects` multilink to `feature` (was missing)
#                      - cleanup of unused classes
#     4-Nov-2004 (MPH) Effort: `Interval` -> `Number`
#     8-Nov-2004 (MPH) Cleanup, removed `accepted-but-defects` from
#                      `document_status`
#     9-Nov-2004 (MPH) Added `completed-but-defects` to `feature_status`
#    16-Nov-2004 (MPH) Added `May Public Queries` permission to `query`
#     1-Dec-2004 (MPH) Added `is_alias` to Class `user`
#     5-Apr-2005 (MPH) Added `composed_of` and `part_of` to `feature`, added
#                      support for Online Peer Reviews
#     6-Apr-2005 (RSC) Factored from dbinit.py for roundup 0.8.2
#                      "May Public Queries"->"May publish Queries"
#    11-Apr-2005 (MPH) Fixed Multilink in `review` and `announcement` to link
#                      to `file` instead of `files`
#     6-Jun-2005 (RSC) Incorporate changes from dbinit.py
#     8-Jun-2005 (RSC) time_record and time_wp added.
#                      IssueClass used directly
#    15-Jun-2005 (RSC) i18n stuff for name translations
#    22-Jun-2005 (RSC) schema additions for time-tracking
#    22-Jun-2005 (RSC) schema additions for time-tracking
#                      moved some comments in the class definition into
#                      the extensions/help.py
#    ««revision-date»»···
#--
#

class TTT_Issue_Class (Class, IssueClass) :
    """extends the IssueClass with some parameters common to all issues here
    at TTTech.
    Note: inheritance methodology stolen from roundup/backends/back_anydbm.py's
          IssueClass ;-)
    """
    def __init__ (self, db, classname, ** properties) :
        if not properties.has_key ("title") :
            properties ["title"]       = String    (indexme = "yes")
        if not properties.has_key ("responsible") :
            properties ["responsible"] = Link      ("user")
        if not properties.has_key ("nosy") :
            properties ["nosy"]        = Multilink ("user", do_journal = "no")
        if not properties.has_key ("messages") :
            properties ["messages"]    = Multilink ("msg")
        Class.__init__ (self, db, classname, ** properties)
    # end def __init__
# end class TTT_Issue_Class

# Helper classes
# Class automatically gets these properties:
#   creation = Date ()
#   activity = Date ()
#   creator  = Link ('user')
# Note: without "order" they get sorted by the key, "name" or "title" or
#       the alphabetically "first" attribute.
query = Class \
    ( db
    , ''"query"
    , klass                 = String    ()
    , name                  = String    ()
    , url                   = String    ()
    , private_for           = Link      ('user')
    )

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

severity = Class \
    ( db
    , ''"severity"
    , name                  = String    ()
    , order                 = String    ()
    )
severity.setkey ("name")

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

organisation = Class \
    ( db
    , ''"organisation"
    , name                  = String    ()
    , description           = String    ()
    # get automatically appended to the users mail address upon creation
    # of a new user.
    , mail_domain           = String    ()
    , valid_from            = Date      ()
    , valid_to              = Date      ()
    , messages              = Multilink ("msg")
    )
organisation.setkey ("name")

location = Class \
    ( db
    , ''"location"
    , name                  = String    ()
    , address               = String    ()
    , country               = String    ()
    )
location.setkey ("name")

org_location = Class \
    ( db
    , ''"org_location"
    , name                  = String    ()
    , phone                 = String    ()
    , organisation          = Link      ("organisation")
    , location              = Link      ("location")
    )
org_location.setkey ("name")

room = Class \
    ( db
    , ''"room"
    , name                  = String    ()
    , org_location          = Link      ("org_location")
    )
room.setkey ("name")

meeting_room = Class \
    ( db
    , ''"meeting_room"
    , name                  = String    ()
    , room                  = Link      ("room")
    )
meeting_room.setkey ("name")

cost_center_group = Class \
    ( db
    , ''"cost_center_group"
    , name                  = String    ()
    , description           = String    ()
    , responsible           = Link      ("user")
    , active                = Boolean   ()
    )
cost_center_group.setkey ("name")

department = Class \
    ( db
    , ''"department"
    , name                  = String    ()
    , description           = String    ()
    , manager               = Link      ("user")
    , part_of               = Link      ("department")
    , doc_num               = String    ()
    , valid_from            = Date      ()
    , valid_to              = Date      ()
    , messages              = Multilink ("msg")
    )
department.setkey ("name")

position = Class \
    ( db
    , ''"position"
    , position              = String    ()
    )
position.setkey ("position")

time_project_status = Class \
    ( db
    , ''"time_project_status"
    , name                  = String    ()
    , description           = String    ()
    , only_controlling      = Boolean   ()
    )
time_project_status.setkey ("name")

time_project = Class \
    ( db
    , ''"time_project"
    , name                  = String    ()
    , description           = String    ()
    , responsible           = Link      ("user")
    , deputy                = Link      ("user")
    , team_members          = Multilink ("user")
    , organisation          = Link      ("organisation")
    , department            = Link      ("department")
    , time_start            = Date      (offset = 0)
    , time_end              = Date      (offset = 0)
    , planned_effort        = Number    ()
    , status                = Link      ("time_project_status")
    )
time_project.setkey ("name")

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
    )

work_location = Class \
    ( db
    , ''"work_location"
    , code                  = String    ()
    , description           = String    ()
    )
work_location.setkey ("code")

daily_record_status = Class \
    ( db
    , ''"daily_record_status"
    , name                  = String    ()
    , description           = String    ()
    )
daily_record_status.setkey ("name")

daily_record = Class \
    ( db
    , ''"daily_record"
    , user                  = Link      ("user")
    , date                  = Date      (offset = 0)
    , status                = Link      ("daily_record_status")
    , time_record           = Multilink ("time_record")
    )

time_record = Class \
    ( db
    , ''"time_record"
    , daily_record          = Link      ("daily_record")
    , start                 = String    ()
    , end                   = String    ()
    , duration              = Number    ()
    , wp                    = Link      ("time_wp")
    , time_activity         = Link      ("time_activity")
    , work_location         = Link      ("work_location")
    , comment               = String    ()
    )

time_activity = Class \
    ( db
    , ''"time_activity"
    , name                  = String    ()
    , description           = String    ()
    )
time_activity.setkey ("name")

time_wp_group = Class \
    ( db
    , ''"time_wp_group"
    , name                  = String    ()
    , description           = String    ()
    , wps                   = Multilink ("time_wp")
    )
time_wp_group.setkey ("name")

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

cost_center_status = Class \
    ( db
    , ''"cost_center_status"
    , name                  = String    ()
    , description           = String    ()
    , active                = Boolean   ()
    )
cost_center_status.setkey ("name")

sex = Class \
    ( db
    , ''"sex"
    , name                  = String    ()
    )
sex.setkey ("name")

user_status = Class \
    ( db
    , ''"user_status"
    , name                  = String    ()
    , description           = String    ()
    )
user_status.setkey ("name")

# Note: roles is a comma-separated string of Role names
user = Class \
    ( db
    , ''"user"
    , username              = String    ()
    , nickname              = String    ()
    , password              = Password  ()
    , address               = String    ()
    , alternate_addresses   = String    ()
    , status                = Link      ("user_status")
    , firstname             = String    ()
    , lastname              = String    ()
    , realname              = String    ()
    , phone                 = String    ()
    , external_phone        = String    ()
    , private_phone         = String    ()
    , department            = Link      ("department")
    , supervisor            = Link      ("user")
    , substitutes           = Multilink ("user")
    , subst_active          = Boolean   ()
    , clearance_by          = Link      ("user")
    , room                  = Link      ("room")
    , title                 = String    ()
    , position              = Link      ("position") # e.g. SW Developer
    , job_description       = String    ()
    , queries               = Multilink ("query")
    , roles                 = String    ()
    , timezone              = String    ()
    , pictures              = Multilink ("file")
    , lunch_start           = String    ()
    , lunch_duration        = Number    ()
    , sex                   = Link      ("sex")
    # XXX: add wiki page url in the web-template based on firstname &
    #      lastname -> why not compute this on the fly (RSC)
    # Note: email adresses could get set automatically by a detector on
    #       creation of a new user, as its always <nickname>@tttech.com,
    #       <username>@tttech.com and <firstname>.<lastname>@tttech.com.
    #       However the "tttech.com" part should be part of the
    #       "organisation" ???
    )
user.setkey ("username")

user_dynamic = Class \
    ( db
    , ''"user_dynamic"
    , user                  = Link      ("user")
    , valid_from            = Date      (offset = 0)
    , valid_to              = Date      (offset = 0)
    , durations_allowed     = Boolean   ()
    , long_worktime         = Boolean   ()
    , weekly_hours          = Number    ()
    , hours_mon             = Number    ()
    , hours_tue             = Number    ()
    , hours_wed             = Number    ()
    , hours_thu             = Number    ()
    , hours_fri             = Number    ()
    , hours_sat             = Number    ()
    , hours_sun             = Number    ()
    , holidays              = Number    ()
    , org_location          = Link      ("org_location")
    )

# FileClass automatically gets these properties:
#   content = String()    [saved to disk in <tracker home>/db/files/]
#   (it also gets the Class properties creation, activity and creator)
msg = FileClass \
    ( db
    , ''"msg"
    , date                  = Date      ()
    , files                 = Multilink ("file")
    # Note: below fields are used by roundup internally (obviously by the
    #       mail-gateway)
    , author                = Link      ("user", do_journal='no')
    , recipients            = Multilink ("user", do_journal='no')
    , summary               = String    ()
    , messageid             = String    ()
    , inreplyto             = String    ()
    )

file = FileClass \
    ( db
    , ''"file"
    , name                  = String    ()
    , type                  = String    ()
    )

# TTT_Issue_Class automatically gets these properties:
#   title       = String    ()
#   responsible = Link      ("user")
#   nosy        = Multilink ("user")
#   messages    = Multilink ("msg")
#   (it also gets the Class properties creation, activity and creator)

meeting = TTT_Issue_Class \
    ( db
    , ''"meeting"
    , files                 = Multilink ("file")
    )

action_item = TTT_Issue_Class \
    ( db
    , ''"action_item"
    , files                 = Multilink ("file")
    , meeting               = Link      ("meeting")
    , status                = Link      ("action_item_status")
    , deadline              = Date      ()
    )

document = TTT_Issue_Class \
    ( db
    , ''"document"
    , files                 = Multilink ("file")
    , status                = Link      ("document_status")
    , release               = Link      ("release")
    , type                  = Link      ("document_type")
    )

release = TTT_Issue_Class \
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

feature = TTT_Issue_Class \
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

task = TTT_Issue_Class \
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

defect = TTT_Issue_Class \
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

TTT_Issue_Class \
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

TTT_Issue_Class \
    ( db
    , ''"announcement"
    , version               = String    ()
    , meeting_room          = Link      ("meeting_room")
    , comments              = Multilink ("comment")
    , review                = Link      ("review")
    , status                = Link      ("review_status")
    , files                 = Multilink ("file")
    )

TTT_Issue_Class \
    ( db
    , ''"comment"
    , severity              = Link      ("severity")
    , status                = Link      ("comment_status")
    , review                = Link      ("review")
    , announcement          = Link      ("announcement")
    , file_name             = String    ()
    , line_number           = String    ()
    )

#
# SECURITY SETTINGS
#
# See the configuration and customisation document for information
# about security setup.
# Assign the access and edit Permissions for issue, file and message
# to regular users now

# roles: user, admin, nosy, teamleader, ccb, office (to edit the users
#        only)
#     classname        allowed to view   /  edit
classes = \
    [ ("query"             , ["User"], ["User"            ])
    , ("room"              , ["User"], ["Admin"           ])
    , ("milestone"         , ["User"], ["Releasemanager"  ])
    , ("task_status"       , ["User"], ["Admin"           ])
    , ("task_kind"         , ["User"], ["Admin"           ])
    , ("action_item_status", ["User"], ["Admin"           ])
    , ("defect_status"     , ["User"], ["Admin"           ])
    , ("feature_status"    , ["User"], ["Admin"           ])
    , ("review_status"     , ["User"], ["Admin"           ])
    , ("comment_status"    , ["User"], ["Admin"           ])
    , ("document_type"     , ["User"], ["Admin"           ])
    , ("severity"          , ["User"], ["Admin"           ])
    , ("product"           , ["User"], ["Admin"           ])
    , ("organisation"      , ["User"], ["Admin"           ])
    , ("department"        , ["User"], ["Admin"           ])
    , ("position"          , ["User"], ["Admin"           ])
#    , ("user"              , ["User"], ["Admin", "Office" ])
    , ("msg"               , ["User"], ["User"            ])
    , ("file"              , ["User"], ["User"            ])
    , ("document"          , ["User"], ["User"            ])
    , ("release"           , ["User"], ["Releasemanager"  ])
    , ("feature"           , ["User"], ["Releasemanager"  ])
    , ("task"              , ["User"], ["User"            ])
    , ("defect"            , ["User"], ["User"            ])
    , ("meeting"           , ["User"], ["Admin"           ])
    , ("action_item"       , ["User"], ["User"            ])
    , ("review"            , ["User"], ["User"            ])
    , ("announcement"      , ["User"], ["User"            ])
    , ("comment"           , ["User"], ["User"            ])
    ]

roles = \
    [ ("Nosy"          , "Allowed on nosy list"          )
    , ("CCB"           , "Member of Change Control Board")
    , ("Office"        , "Member of Office"              )
    , ("Releasemanager", "Allowed to manage a SW Release")
    , ("IV&V"          , "Member of the IV&V Team."      )
    , ("halfweek"      , "User works only the half week" )
    ]

for name, desc in roles :
    db.security.addRole (name = name, description = desc)

for cl, view_list, edit_list in classes :
    for viewer in view_list :
        db.security.addPermissionToRole (viewer, 'View', cl)
    for editor in edit_list :
        db.security.addPermissionToRole (editor, 'Edit',   cl)
        db.security.addPermissionToRole (editor, 'Create', cl)

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
for klass in nosy_classes :
    db.security.addPermission \
        ( name        = "Nosy"
        , klass       = klass
        , description = "User may get nosy messages for %s" % klass
        )
    db.security.addPermissionToRole ("Nosy", "Nosy", klass)

# and give the regular users access to the web and email interface
db.security.addPermissionToRole('User', 'Web Access')
db.security.addPermissionToRole('User', 'Email Access')

# Anonymous may view other users profiles - required for intranet pages.
db.security.addPermissionToRole('Anonymous', 'View', 'user')

# oh, g'wan, let anonymous access the web interface too
# NOT really !!!
db.security.addPermissionToRole('Anonymous', 'Web Access')
# db.security.addPermissionToRole('Anonymous', 'Email Access')

