# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    dbinit
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
#     8-Nov-2004 (MPH) Cleanup, removed `accepted-but-defects` from `document_status`
#    ««revision-date»»···
#--
#
import os

import config
from   select_db import Database, Class, FileClass, IssueClass
from   roundup   import hyperdb, password, roundupdb

class TTT_Issue_Class (Class, roundupdb.IssueClass) :
    """extends the IssueClass with some parameters common to all issues here
    at TTTech.
    Note: inheritance methodology stolen from roundup/backends/back_anydbm.py's
          IssueClass ;-)
    """
    def __init__ (self, db, classname, ** properties) :
        if not properties.has_key ("title") :
            properties ["title"]       = hyperdb.String    (indexme = "yes")
        if not properties.has_key ("responsible") :
            properties ["responsible"] = hyperdb.Link      ("user")
        if not properties.has_key ("nosy") :
            properties ["nosy"]        = hyperdb.Multilink ( "user"
                                                           , do_journal = "no"
                                                           )
        if not properties.has_key ("messages") :
            properties ["messages"]    = hyperdb.Multilink ("msg")
        Class.__init__ (self, db, classname, ** properties)
    # end def __init__
# end class TTT_Issue_Class

def open (name = None):
    ''' as from the roundupdb method openDB
    '''
    from roundup.hyperdb import String, Password, Date, Link, Multilink
    from roundup.hyperdb import Interval, Boolean, Number

    # open the database
    db = Database (config, name)

    # Helper classes
    # Class automatically gets these properties:
    #   creation = Date ()
    #   activity = Date ()
    #   creator  = Link ('user')
    # Note: without "order" they get sorted by the key, "name" or "title" or
    #       the alphabetically "first" attribute.
    query = Class \
        ( db
        , "query"
        , klass                 = String    ()
        , name                  = String    ()
        , url                   = String    ()
        , private_for           = Link      ('user')
        )

    room = Class \
        ( db
        , "room"
        , name                  = String    ()
        # XXX: or more specific, but without a key
        #, building              = String    ()
        #, floor                 = String    ()
        #, room_number           = String    ()
        )
    room.setkey ("name")

    milestone_class = Class \
        ( db
        , "milestone"
        , name                  = String    ()
        , description           = String    ()
        , planned               = Date      ()
        , reached               = Date      ()
        , order                 = Number    ()
        , release               = Link      ("release") # the release this
                                        # milestone belongs to - needed for
                                        # reactors updating the releases
                                        # "status" field,  which represents
                                        # the last reached milestone.
        )

    task_status = Class \
        ( db
        , "task_status"
        , name                  = String    ()
        , description           = String    ()
        , abbreviation          = String    ()
        , transitions           = Multilink ("task_status")
        , order                 = String    ()
        )
    task_status.setkey ("name")

    task_kind = Class \
        ( db
        , "task_kind"
        , name                  = String    ()
        , description           = String    ()
        , order                 = String    ()
        )
    task_kind.setkey ("name")

    feature_status = Class \
        ( db
        , "feature_status"
        , name                  = String    ()
        , description           = String    ()
        , abbreviation          = String    ()
        , transitions           = Multilink ("feature_status")
        , order                 = String    ()
        )
    feature_status.setkey ("name")

    defect_status = Class \
        ( db
        , "defect_status"
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
        , "action_item_status"
        , name                  = String    ()
        , description           = String    ()
        , order                 = String    ()
        )
    action_item_status.setkey ("name")

    document_status = Class \
        ( db
        , "document_status"
        , name                  = String    ()
        , description           = String    ()
        , abbreviation          = String    ()
        , transitions           = Multilink ("document_status")
        , order                 = String    ()
        )
    document_status.setkey ("name")

    document_type = Class \
        ( db
        , "document_type"
        , name                  = String    ()
        , description           = String    ()
        , order                 = String    ()
        )
    document_type.setkey ("name")

    severity = Class \
        ( db
        , "severity"
        , name                  = String    ()
        , order                 = String    ()
        )
    severity.setkey ("name")

    product = Class \
        ( db
        , "product"
        , name                  = String    ()
        , description           = String    ()
        , responsible           = Link      ("user")
        , nosy                  = Multilink ("user")
        , certifiable           = Boolean   () # needs to be set, to let the
                                        # "defect report" mechanism allow to
                                        # mark some defect against a specific
                                        # product as belonging to "cert".
        # XXX: no "order", gets sorted by "name" automatically.
        )
    product.setkey ("name")

    organisation = Class \
        ( db
        , "organisation"
        , name                  = String    ()
        , address               = String    () # XXX: should be more
                                               # specific, but would require
                                               # much more classes ...
        , phone                 = String    ()
        , mail_domain           = String    () # get automatically appended
                                               # to the users mail address upon
                                               # creation of a new user.
        )
    organisation.setkey ("name")

    department = Class \
        ( db
        , "department"
        , name                  = String    ()
        )
    department.setkey ("name")

    title = Class \
        ( db
        , "title"
        , title                 = String    ()
        )
    title.setkey ("title")

    position = Class \
        ( db
        , "position"
        , position              = String    ()
        )
    position.setkey ("position")

    # Note: roles is a comma-separated string of Role names
    user = Class \
        ( db
        , "user"
        , username              = String    () # e.g. goller
        , nickname              = String    () # e.g. ago
        , password              = Password  ()
        , address               = String    () # email address
        , alternate_addresses   = String    () # other email adresses
        , firstname             = String    () # e.g. alois
        , lastname              = String    () # e.g. goller
        , realname              = String    () # gets automatically set from
                                               # firstname and lastname - is
                                               # needed by roundupdp.py's
                                               # send_message - which is used
                                               # e.g. by the nosyreactor
        , phone                 = String    () # shortcut: e.g. 42
        , external_phone        = String    () # mobile_short: e.g. 6142
        , private_phone         = String    () # whatever
        , organisation          = Link      ("organisation") # e.g. TTTech
        , location              = String    () # e.g. Vienna HQ, XXX: Link ???
        , department            = Link      ("department")   # e.g. SW, Sales
        , superior              = Link      ("user")
        , substitutes           = Multilink ("user")
        , room                  = Link      ("room")
        , title                 = Link      ("title")    # e.g. Dipl. Ing.
        , position              = Link      ("position") # e.g. SW Developer
        , job_description       = String    ()
        , queries               = Multilink ("query")
        , roles                 = String    ()
        , timezone              = String    ()
        , pictures              = Multilink ("file")
        # XXX: add wiki page url in the web-template based on firstname &
        #      lastname
        # Note: email adresses could get set automatically by a detector on
        #       creation of a new user, as its always <nickname>@tttech.com,
        #       <username>@tttech.com and <firstname>.<lastname>@tttech.com.
        #       However the "tttech.com" part should be part of the
        #       "organisation" ???
        )
    user.setkey ("username")

    # FileClass automatically gets these properties:
    #   content = String()    [saved to disk in <tracker home>/db/files/]
    #   (it also gets the Class properties creation, activity and creator)
    msg = FileClass \
        ( db
        , "msg"
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
        , "file"
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
        , "meeting"
        , files                 = Multilink ("file")
        )

    action_item = TTT_Issue_Class \
        ( db
        , "action_item"
        , files                 = Multilink ("file")
        , meeting               = Link      ("meeting")
        , status                = Link      ("action_item_status")
        , deadline              = Date      ()
        )

    document = TTT_Issue_Class \
        ( db
        , "document"
        , files                 = Multilink ("file")
        , status                = Link      ("document_status")
        , release               = Link      ("release")
        , type                  = Link      ("document_type")
        )

    release = TTT_Issue_Class \
        ( db
        , "release"
        , status                = Link      ("milestone") # just to show
                                                          # something in the
                                                          # pop-up, gets set
                                                          # to the last
                                                          # reached milestone
        , documents             = Multilink ("document")
        , features              = Multilink ("feature")
        , planned_fixes         = Multilink ("defect")
        , bugs                  = Multilink ("defect")
        , milestones            = Multilink ("milestone") # Note: they get
                                        # added automatically on creation of
                                        # a new release (by the auditor -
        )

    feature = TTT_Issue_Class \
        ( db
        , "feature"
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
        , test_ok               = Boolean   () # gets set automatically by a
                                               # detector depending on the
                                               # testcases test_ok switch.
        , tasks                 = Multilink ("task")
        , depends               = Multilink ("feature")
        , needs                 = Multilink ("feature")
        , release               = Link      ("release")
        , defects               = Multilink ("defect")
        , planned_begin         = Date      () # automatically by import
        , planned_end           = Date      () # automatically by import
        , actual_begin          = Date      () # automatically by status
        , actual_end            = Date      () # change of workpackages
        )

    task = TTT_Issue_Class \
        ( db
        , "task"
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
        , "defect"
        , status                = Link      ("defect_status")
        , superseder            = Link      ("defect")
        , cert                  = Boolean   ()
        , solved_in_release     = Link      ("release") # in which "release"
                                                        # it gets repaired.
                                                        # i.e. it is in the
                                                        # "planned_fixes" of
                                                        # that release.
        , found_in_release      = Link      ("release") # where it was
                                                        # initially found.
                                                        # "solved_in_release"
                                                        # is initially set to
                                                        # "found_in_release"
        , estimated_effort      = Number    ()
        , fixed_until           = Date      () # currently optional, but the
                                        # opinions differ if it is generally
                                        # good to only say how long does it
                                        # take, or to give some point in time
                                        # where it is actually fixed... mph
                                        # thinks that the estimated_effort is
                                        # best - and gives some rough
                                        # estimation on how much time we
                                        # actually need to add for
                                        # big-fixing. in tal's opinion it is
                                        # important to know when it will be
                                        # ready. but the past showed that
                                        # "deadlines" in general are a bad
                                        # idea - as they always point to some
                                        # point back in time ;)
        , severity              = Link      ("severity")
        , product               = Link      ("product")
        , version               = String    ()
        , files                 = Multilink ("file")
        , fixed_in              = String    ()
        , files_affected        = String    () # XXX only cert ???
        , closed                = Date      ()
        , closer                = Link      ("user") # if it opens again,
                                        # than we have a shortcut to who
                                        # actually closed it last time. as we
                                        # are also setting the "closed" date
                                        # for this, we can also set the
                                        # "closer" here.
        , belongs_to_feature    = Link      ("feature") # if known
        , belongs_to_task       = Link      ("task")    # if known
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
        , ("document_type"     , ["User"], ["Admin"           ])
        , ("severity"          , ["User"], ["Admin"           ])
        , ("product"           , ["User"], ["Admin"           ])
        , ("organisation"      , ["User"], ["Admin"           ])
        , ("department"        , ["User"], ["Admin"           ])
        , ("title"             , ["User"], ["Admin"           ])
        , ("position"          , ["User"], ["Admin"           ])
        , ("user"              , ["User"], ["Admin", "Office" ])
        , ("msg"               , ["User"], ["User"            ])
        , ("file"              , ["User"], ["User"            ])
        , ("document"          , ["User"], ["User"            ])
        , ("release"           , ["User"], ["Releasemanager"  ])
        , ("feature"           , ["User"], ["Releasemanager"  ])
        , ("task"              , ["User"], ["User"            ])
        , ("defect"            , ["User"], ["User"            ])
        , ("meeting"           , ["User"], ["Admin"           ])
        , ("action_item"       , ["User"], ["User"            ])
        ]

    roles = \
        [ ("Nosy"          , "Allowed on nosy list"          )
        , ("CCB"           , "Member of Change Control Board")
        , ("Office"        , "Member of Office"              )
        , ("Releasemanager", "Allowed to manage a SW Release")
        , ("IV&V"          , "Member of the IV&V Team."      )
        ]

    for name, desc in roles :
        db.security.addRole (name = name, description = desc)

    for cl, view_list, edit_list in classes :
        for viewer in view_list :
            p = db.security.getPermission ("View", cl)
            db.security.addPermissionToRole (viewer, p)
        for editor in edit_list :
            p = db.security.getPermission ("Edit", cl)
            db.security.addPermissionToRole (editor, p)

    # add permission "May Change Status" to role "CCB" and "Admin"
    p = db.security.addPermission (name="May Change Status", klass="defect")
    db.security.addPermissionToRole("CCB", p)
    db.security.addPermissionToRole("Admin", p)

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
                   ]
    for klass in nosy_classes :
        db.security.addPermission \
            ( name        = "Nosy"
            , klass       = klass
            , description = "User may get nosy messages for %s" % klass
            )
        p = db.security.getPermission   ("Nosy", klass)
        db.security.addPermissionToRole ("Nosy", p)

    # and give the regular users access to the web and email interface
    p = db.security.getPermission('Web Access')
    db.security.addPermissionToRole('User', p)
    p = db.security.getPermission('Email Access')
    db.security.addPermissionToRole('User', p)

    # Anonymous may view other users profiles - required for intranet pages.
    p = db.security.getPermission('View', 'user')
    db.security.addPermissionToRole('Anonymous', p)


    # oh, g'wan, let anonymous access the web interface too
    # XXX: really ???
#    p = db.security.getPermission('Web Access')
#    db.security.addPermissionToRole('Anonymous', p)

    import detectors
    detectors.init(db)

    # schema is set up - run any post-initialisation
    db.post_init()
    return db

def init(adminpw):
    '''Invoked by the "roundup-admin initialise" command to set up the
    initial state of the hyperdb.

    If you wish to change the hyperdb *after* running that command, see
    the customisation doc "Database Content" section.
    '''
    dbdir = os.path.join (config.DATABASE, 'files')
    if not os.path.isdir (dbdir):
        os.makedirs (dbdir)

    db = open ("admin")
    db.clear  ()

    # init values
    # room
    room = db.getclass ("room")
    room.create        (name = "SW Dept.")
    # add rooms here

    # task_status
    # order, name, abbreviation, transitions, description
    tasks = [ ("1", "issued"              , "issu", ("started", )
              , "Waiting to get started")
            , ("2", "started"             , "star", ("available", "suspended")
              , "Someone is working on it.")
            , ("3", "available"           , "avai", ("accepted", "suspended")
              , "It is ready for review.")
            , ("4", "accepted"            , "acce", ("accepted-but-defects", )
              , "It is reviewed and found to be correct.")
            , ("5", "accepted-but-defects", "acbd", ("accepted", )
              , "It is accepted, but has defects reported.")
            , ("6", "suspended"           , "susp", ("issued", )
              , "We plan to do it later.")
            , ("7", "closed-obsolete"     , "obso", ()
              , "We agreed to not do it anymore")
            ]

    task_status = db.getclass ("task_status")
    for order, name, abbr, trans, desc in tasks :
        task_status.create ( name         = name
                           , order        = order
                           , description  = desc
                           , abbreviation = abbr
                           )
    for order, name, abbr, trans, desc in tasks :
        if trans :
            id        = task_status.lookup (name)
            trans_ids = [task_status.lookup (t) for t in trans]
            task_status.set (id, transitions = trans_ids)

    # document_status
    # order, name, abbr, transitions, description
    docs = [ ("1", "issued"              , "issu", ("started", )
             , "Waiting to get started")
           , ("2", "started"             , "star", ("available")
             , "Someone is working on it.")
           , ("3", "available"           , "avai", ("accepted")
             , "It is ready for review.")
           , ("4", "accepted"            , "acce", ()
              , "It is reviewed and found to be correct.")
           ]

    document_status = db.getclass ("document_status")
    for order, name, abbr, trans, desc in tasks :
        document_status.create ( name         = name
                               , order        = order
                               , description  = desc
                               , abbreviation = abbr
                               )
    for order, name, abbr, trans, desc in tasks :
        if trans :
            id        = document_status.lookup (name)
            trans_ids = [document_status.lookup (t) for t in trans]
            document_status.set (id, transitions = trans_ids)

    # task_kind
    kinds = [ ("1", "srd"                  , "Software Requirements Document")
            , ("2", "sdd"                  , "Software Design Document"      )
            , ("3", "implementation_task"  , "Implementation Task"           )
            , ("4", "testcase"             , "Testcase"                      )
            , ("5", "product_documentation", "Product Documentation Task"    )
            ]
    task_kind = db.getclass ("task_kind")
    for order, name, desc in kinds :
        task_kind.create ( name        = name
                         , order       = order
                         , description = desc
                         )

    # feature_status
    # order, name, abbreviation, transitions, description
    fss = [ ("1", "raised"   , "rais", ("suspended", "rejected") # "open" automatically
            , "We should start working on it.")
          , ("2", "open"     , "open", ("suspended", ) # "completed" automatically
            , "We are currently working on it.")
          , ("3", "completed", "comp", ()
            , "It is completed.")
          , ("4", "rejected" , "reje", ("raised", )
            , "We wont do it.")
          , ("5", "suspended", "susp", ("raised", )
            , "We will do it later.")
          ]
    feature_status = db.getclass ("feature_status")
    for order, name, abbr, trans, desc in fss :
        feature_status.create ( name         = name
                              , order        = order
                              , description  = desc
                              , abbreviation = abbr
                              )

    for order, name, abbr, trans, desc in fss :
        if trans :
            id        = feature_status.lookup (name)
            trans_ids = [feature_status.lookup (t) for t in trans]
            feature_status.set (id, transitions = trans_ids)

    # action_item_status
    # order, name, description
    ais = [ ("1", "open"  , "The Action-Item is open"  )
          , ("2", "closed", "The Action-Item is closed")
          ]
    ai = db.getclass ("action_item_status")
    for order, name, desc in ais :
        ai.create (name = name, description = desc, order = order)

    # defect_status:
    # order, name, abbreviation, cert, description, cert_trans, trans
    dss = [ ("1", "assigned"        , "assi", False
            , "Has just been reported"
            , ("analyzed", "closed")
            , ( "resolved"       , "closed-duplicate"
              , "closed-mistaken", "suspended"
              )
            )
          , ("2", "analyzed"        , "ana ", True
            , "We know what caused the defect"
            , ( "implemented"    , "closed-duplicate"
              , "closed-rejected", "suspended"
              )
            , ()
            )
          , ("3", "implemented"     , "impl", True
            , "The fix is implemented"
            , ("analyzed", "resolved", "suspended")
            , ()
            )
          , ("4", "resolved"        , "res ", False
            , "The defect is ready for testing"
            , ("closed", "suspended")
            , ("closed", "assigned", "suspended")
            )
          , ("5", "closed"          , "clos", False, "Rest in peace"  , (), ())
          , ("6", "closed-duplicate", "dupl", False, "Is a duplicate" , (), ())
          , ("7", "closed-mistaken" , "mist", False, "Originator "
                                                     "misunderstood "
                                                     "something"      , (), ())
          , ("8", "closed-rejected" , "rej ", True , "We dont do it"  , (), ())
          , ("9", "suspended"       , "susp", False
            , "We will fix this later"
            , ("assigned", )
            , ("assigned", )
            )
          ]
    defect_status = db.getclass ("defect_status")
    for order, name, abbr, cert, desc, c_trans, trans in dss :
        defect_status.create ( name         = name
                             , cert         = cert
                             , order        = order
                             , description  = desc
                             , abbreviation = abbr
                             )
    for order, name, abbr, cert, desc, c_trans, trans in dss :
        id        = defect_status.lookup (name)
        if c_trans :
            trans_ids = [defect_status.lookup (t) for t in c_trans]
            defect_status.set (id, cert_transitions = trans_ids)
        if trans :
            trans_ids = [defect_status.lookup (t) for t in trans]
            defect_status.set (id, transitions = trans_ids)

    # document_type
    # order, name, description
    dts = [ ("1", "ES" , "Evaluation Sheet"             )
          , ("2", "CMP", "Configuration Management Plan")
          , ("3", "HTP", "High-Level Test Plan"         )
          ]
    doc_type = db.getclass ("document_type")
    for order, name, desc in dts :
        doc_type.create (name = name, description = desc, order = order)

    # severity
    # order, name
    ss = [ ("1", "showstopper")
         , ("2", "major")
         , ("3", "minor")
         ]
    severity = db.getclass ("severity")
    for order, name in ss :
        severity.create (name = name, order = order)

    # organisation
    # name, address, phone
    orgs = [ ("TTTech Vienna"        , "addr", "phone")
           , ("TTTech Germany"       , "addr", "phone")
           , ("TTTech Japan"         , "addr", "phone")
           , ("TTTech North America" , "addr", "phone")
           , ("TTTChip"              , "addr", "phone")
           , ("TTControl"            , "addr", "phone")
           # XXX: add other companies name, address & phone
           ]
    org = db.getclass ("organisation")
    for name, address, phone in orgs :
        org.create (name = name, address = address, phone = phone)

    # departments
    # name
    depts = [ "Software"
            , "Hardware"
            , "Office"
            , "Service"
            , "Sales"
            , "Marketing"
            , "Executive Board"
            # XXX: add departments
            ]
    dept = db.getclass ("department")
    for name in depts :
        dept.create (name = name)

    # titles
    # title
    titles = [ "Dipl. Ing."
             , "Dr."
             , "DI Dr."
             , "DDr."
             # XXX: add titles (notably the international (english)
             #      counterparts)
             ]
    title = db.getclass ("title")
    for _title in titles :
        title.create (title = _title)

    # positions
    # position
    positions = [ "Software Developer"
                , "Senior Software Developer"
                , "Marketing Director"
                # XXX: Add positions
                ]
    position = db.getclass ("position")
    for _position in positions :
        position.create (position = _position)

    # users
    # create the two default users
    user = db.getclass ('user')
    user.create ( username = "admin"
                , password = adminpw
                , address  = config.ADMIN_EMAIL
                , roles    = "Admin"
                )
    user.create ( username = "anonymous"
                , roles    = "Anonymous"
                )

##     # create TTTech users:
##     # XXX: we should import this from somewhere ;-)
##     # but it should reside here - or not ???
##     user.create ( username = "priesch"
##                 , password = password.Password ("")
##                 , address  = "priesch@tttech.com"
##                 , roles    = "Admin, User, Nosy"
##                 )

##     user.create ( username = "pr"
##                 , password = password.Password ("")
##                 , address  = "priesch@tttech.com"
##                 , roles    = "Admin, User, Nosy"
##                 )

##     # products:
##     # name, responsible, description, nosy
##     ps = [ ("TTPPlan"     , "priesch", "desc", [])
##          , ("TTPCalibrate", "pr"     , "desc", [])
##          # XXX: add products here
##          ]
##     product = db.getclass ("product")
##     for name, resp, desc, nosy in ps :
##         nosy_ids = [user.lookup (u) for u in nosy]
##         product.create ( name        = name
##                        , responsible = resp
##                        , nosy        = nosy_ids
##                        , description = desc
##                        )

##     # meetings
##     # title, responsible, nosy
##     meetings = \
##         [ ("Tools-Meeting", "admin", ["priesch", ])
##         , ("SAFT-Meeting",  "pr"   , ["priesch", ])
##         # XXX: add other meetings
##         ]
##     meeting = db.getclass ("meeting")
##     for title, resp, nosy in meetings :
##         nosy_ids = [user.lookup (u) for u in nosy]
##         meeting.create (title = title, responsible = resp,  nosy = nosy_ids)

    # add any additional database create steps here - but only if you
    # haven't initialised the database with the admin "initialise" command

    db.commit()
    db.close()

# vim: set filetype=python ts=4 sw=4 et si

#SHA: 92c54c05ba9f59453dc74fa9fdbbae34f7a9c077
### __END__ dbinit
