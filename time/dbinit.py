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
        , order                 = String    ()
        )
    milestone_class.setkey ("name")

    work_package_status = Class \
        ( db
        , "work_package_status"
        , name                  = String    ()
        , description           = String    ()
        , transitions           = Multilink ("work_package_status")
        , order                 = String    ()
        )
    work_package_status.setkey ("name")

    feature_status = Class \
        ( db
        , "feature_status"
        , name                  = String    ()
        , description           = String    ()
        , transitions           = Multilink ("feature_status")
        , order                 = String    ()
        )
    feature_status.setkey ("name")

    defect_status = Class \
        ( db
        , "defect_status"
        , name                  = String    ()
        , description           = String    ()
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

    # XXX: needs to get clarified with OIT - regarding the LDAP Tree they are
    #      building up right now ...
    #      Acc to the meeting from 1.7.04 they have some properties already
    #      in ldap,  but dont care about a db backend right now, maybe some
    #      day the ldap info will be created out of roundup.
    #      RSC: has the current ldap spec, and will investigate further
    #      properties needed here in roundup
    #
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
        , phone                 = String    () # shortcut: e.g. 42
        , ext_phone             = String    () # mobile_short: e.g. 6142
        , priv_phone            = String    () # whatever
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
        , picture               = Link      ("file")
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

    pdf_file = FileClass \
        ( db
        , "pdf_file"
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
        , files                 = Multilink ("pdf_file")
        , status                = Link      ("work_package_status")
        , type                  = Link      ("document_type")
        )

    ### XXX: "Software" Container is a singleton and was eliminated, instead
    ###      of this one or more global queries will be created to hold all
    ###      the information found in the "Software" container.
    ###      Namely these queries would filter :
    ###        * all release containers
    ###        * all defects not connected to a release == known defects
    ###        * all features not connected to a release == new features.
    ###
    ###      Further filtering capabilities can be implemented as needed.
    ###      This information solely is of importance for SW Head and/or
    ###      Teamleaders.

    release = TTT_Issue_Class \
        ( db
        , "release"
        # XXX: instead of:
        #, eval_sheet            = Link      ("pdf_file")
        #, configuration_plan    = Link      ("pdf_file")
        #, test_plan             = Link      ("pdf_file")
        ## XXX: add the .ppt presentation of the release here ???
        ##, release_plan          = Link      ("pdf_file")
        # we have only one Multilink on "planning_document" - so we can
        # easily adapt to the number of documents we want here. the type of
        # the document can be set in the individual "planning_document"'s
        # instaces. the presence of some document types can be checked by an
        # auditor, all documents and their corresponding types are displayed
        # on the web page.
        , documents             = Multilink ("document")
        , features              = Multilink ("feature")
        , planned_fixes         = Multilink ("defect")
        , bugs                  = Multilink ("defect")
        , milestones            = Multilink ("milestone") # Note: they get
                                        # added automatically on creation of
                                        # a new release (by the reactor -
                                        # XXX: what if creation fails, or
                                        # there is some error during creation
                                        # of the multilink properties ??? -
                                        # how to clean up ???).
        )

    feature = TTT_Issue_Class \
        ( db
        , "feature"
        , stakeholder           = String    () # some freeform text
        # XXX: "status" is simplified to be only one of "raised",
        #      "suspended", "open" and "completed", all other *.accepted
        #      states can be computed directly from the status of the
        #      attached issues.
        #      There is now a seperate flag "test_ok" which covers the state
        #      of the testcases, and gets set automatically by a detector
        #      when the "test_ok" flag of some attached "testcase" changes.
        #      Changes to the "testcase"s "test_ok" are only allowed by the
        #      iv&v team, and are set manually at begin and later on this
        #      should be automatically, based on the success of a given
        #      testcase (identified by the issue no.).
        , status                = Link      ("feature_status")
        , test_ok               = Boolean   () # gets set automatically by a
                                               # detector depending on the
                                               # testcases test_ok switch.
        , documents             = Multilink ("document") # SRD, SDD, etc.
        , implementation_tasks  = Multilink ("work_package")
        , testcases             = Multilink ("testcase")
        , documentation_tasks   = Multilink ("work_package")
        , depends               = Multilink ("feature")
        , needs                 = Multilink ("feature")
        , release               = Link      ("release")
        , planned_begin         = Date      () # automatically by import
        , planned_end           = Date      () # automatically by import
        , actual_begin          = Date      () # automatically by status
        , actual_end            = Date      () # change of workpackages
        )

    work_package = TTT_Issue_Class \
        ( db
        , "work_package"
        , status                = Link      ("work_package_status")
        , effort                = Interval  () # XXX: was: Number, but
                                               # Interval is better suited
        , depends               = Multilink ("work_package")
        , needs                 = Multilink ("work_package")
        , files                 = Multilink ("file")
        , feature               = Link      ("feature")
        , planned_begin         = Date      ()
        , planned_end           = Date      ()
        , actual_begin          = Date      ()
        , actual_end            = Date      ()
        )

    testcase = TTT_Issue_Class \
        ( db
        , "testcase"
        , status                = Link      ("work_package_status")
        , effort                = Number    () # days only
        , depends               = Multilink ("work_package")
        , needs                 = Multilink ("work_package")
        , files                 = Multilink ("file")
        , feature               = Link      ("feature")
        , planned_begin         = Date      ()
        , planned_end           = Date      ()
        , actual_begin          = Date      ()
        , actual_end            = Date      ()
        , test_ok               = Boolean   () # only difference to the
                                        # "work_package", but we need it in a
                                        # seperate class to give permissions,
                                        # and let the detectors only fire
                                        # here.
                                        # This gets set by the iv&v team when
                                        # the particular test case failed. a
                                        # detector sets also the "test_ok"
                                        # field in the feature this testcase
                                        # belongs to.
        )

    defect = TTT_Issue_Class \
        ( db
        , "defect"
        , status                = Link      ("defect_status")
        , superseder            = Link      ("defect")
        , cert                  = Boolean   ()
        , part_of_release       = Link      ("release") # in which "release"
                                                        # it gets repaired.
                                                        # i.e. it is in the
                                                        # "planned_fixes" of
                                                        # that release.
        , found_in_release      = Link      ("release") # where it was
                                                        # initially found.
                                                        # "part_of_release"
                                                        # is initially set to
                                                        # "found_in_release"
        , estimated_effort      = Interval  ()
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
        , fixed_in              = String    ()
        , files_affected        = String    () # XXX only cert ???
        , closed                = Date      ()
        , closer                = Link      ("user") # if it opens again,
                                        # than we have a shortcut to who
                                        # actually closed it last time. as we
                                        # are also setting the "closed" date
                                        # for this, we can also set the
                                        # "closer" here.
        , feature               = Link      ("feature") # if known
        )

## XXX: acc to AGO/RSC/MPH there should be no legacy "issue" class - if
##      somebody wants something with this tracker, we define and implement
##      what he/she needs.
##
##     # XXX: should we provide a legacy issue class ???
##     #      needs also the companion classes (keyword, status, category,
##     #      kind and area)
##     issue = TTT_Issue_Class \
##         ( db, "issue"
##         # , responsible          = Link      ("user")
##         # , stakeholder          = String    () # unformatted
##         , keywords             = Multilink ("keyword")
##         , priority             = Number    ()
##         , effective_prio       = Number    ()
##         , status               = Link      ("status")
##         , closed               = Date      ()
##         , release              = String    ()
##         , fixed_in             = String    () # was Release-Note in gnats
##         , files_affected       = String    ()
##         # , needs_files_affected = Boolean   ()
##         , category             = Link      ("category")
##         , kind                 = Link      ("kind")
##         , area                 = Link      ("area")
##         , depends              = Multilink ("issue")
##         , needs                = Multilink ("issue")
##         , effort               = String    ()
##         # , accumulated_effort   = String    () # `(c, t, o)`
##         , deadline             = Date      ()
##         , earliest_start       = Date      ()
##         , planned_begin        = Date      ()
##         , planned_end          = Date      ()
##         , cur_est_begin        = Date      () # current estimate
##         , cur_est_end          = Date      () # current estimate
##         , candidates           = Multilink ("user")
##         , composed_of          = Multilink ("issue") # should be read only
##         , part_of              = Link      ("issue") # should set composed_of
##         )

# XXX: to be defined
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
        [ ("query"                 , ["User"], ["User"            ])
        , ("room"                  , ["User"], ["Admin"           ])
        , ("milestone"             , ["User"], ["Teamleader"      ])
        , ("work_package_status"   , ["User"], ["Admin"           ])
        , ("defect_status"         , ["User"], ["Admin"           ])
        , ("document_type"         , ["User"], ["Admin"           ])
        , ("severity"              , ["User"], ["Admin"           ])
        , ("product"               , ["User"], ["Admin"           ])
        , ("organisation"          , ["User"], ["Admin"           ])
        , ("department"            , ["User"], ["Admin"           ])
        , ("title"                 , ["User"], ["Admin"           ])
        , ("position"              , ["User"], ["Admin"           ])
        , ("user"                  , ["User"], ["Admin", "Office" ])
        , ("msg"                   , ["User"], ["User"            ])
        , ("file"                  , ["User"], ["User"            ])
        , ("pdf_file"              , ["User"], ["User"            ])
        , ("document"              , ["User"], ["User"            ])
## XXX: this behaviour has to be checked via tal on the page.
##         , ("planning_document"     , ["User"], [ "Teamleader"
##                                                , "Releasemanager"
##                                                ]
##           )
        , ("release"               , ["User"], [ "Teamleader"
                                               , "Releasemanager"
                                               ]
          )
        , ("feature"               , ["User"], [ "Teamleader"
                                               , "Releasemanager"
                                               ]
          )
        , ("work_package"          , ["User"], [ "User"           ])
        , ("defect"                , ["User"], [ "User"           ])
        , ("meeting"               , ["User"], [ "Admin"          ])
        , ("action_item"           , ["User"], [ "User"           ])
        ]

    roles = \
        [ ("Nosy"          , "Allowed on nosy list"          )
        , ("Teamleader"    , "Is Teamleader"                 )
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

    # Add special permission for receiving nosy msgs. In this way we may
    # spare in-house people from receiving notifications from roundup,
    # more importantly we can add external listeners for nosy messages.
    nosy_classes = [ "document"
                   , "release"
                   , "feature"
                   , "work_package"
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

##     for cl in 'issue', 'file', 'msg', 'query':
##         p = db.security.getPermission('View', cl)
##         db.security.addPermissionToRole('User', p)
##         p = db.security.getPermission('Edit', cl)
##         db.security.addPermissionToRole('User', p)
##     for cl in 'priority', 'status':
##         p = db.security.getPermission('View', cl)
##         db.security.addPermissionToRole('User', p)

    # and give the regular users access to the web and email interface
    p = db.security.getPermission('Web Access')
    db.security.addPermissionToRole('User', p)
    p = db.security.getPermission('Email Access')
    db.security.addPermissionToRole('User', p)

    # Anonymous may view other users profiles - required for intranet pages.
    p = db.security.getPermission('View', 'user')
    db.security.addPermissionToRole('Anonymous', p)

##     # Assign the appropriate permissions to the anonymous user's Anonymous
##     # Role. Choices here are:
##     # - Allow anonymous users to register through the web
##     p = db.security.getPermission('Web Registration')
##     db.security.addPermissionToRole('Anonymous', p)
##     # - Allow anonymous (new) users to register through the email gateway
##     p = db.security.getPermission('Email Registration')
##     db.security.addPermissionToRole('Anonymous', p)
##     # - Allow anonymous users access to view issues (which implies being
##     #   able to view all linked information too
##     for cl in 'issue', 'file', 'msg', 'priority', 'status':
##         p = db.security.getPermission('View', cl)
##         db.security.addPermissionToRole('Anonymous', p)
##     # - Allow anonymous users access to edit the "issue" class of data
##     #   Note: this also grants access to create related information like
##     #         files and messages etc that are linked to issues
##     #p = db.security.getPermission('Edit', 'issue')
##     #db.security.addPermissionToRole('Anonymous', p)

    # oh, g'wan, let anonymous access the web interface too
    p = db.security.getPermission('Web Access')
    db.security.addPermissionToRole('Anonymous', p)

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

    # work_package_status
    # order, name, transitions, description
    wps = [ ("1", "issued"   , ("started", )
            , "Waiting to get started")
          , ("2", "started"  , ("available", "suspended")
            , "Someone is working on it.")
          , ("3", "available", ("accepted", "suspended")
            , "It is ready for review.")
          , ("4", "accepted" , ()
            , "It is reviewed and found to be correct.")
          , ("5", "suspended", ("issued",)
            , "We plan to do it later.")
          , ("6", "closed-obsolete", ()
            , "We agreed to not do it anymore")
          ]

    work_package_status = db.getclass ("work_package_status")
    for order, name, trans, desc in wps :
        work_package_status.create ( name        = name
                                   , order       = order
                                   , description = desc
                                   )
    for order, name, trans, desc in wps :
        if trans :
            id        = work_package_status.lookup (name)
            trans_ids = [work_package_status.lookup (t) for t in trans]
            work_package_status.set (id, transitions = trans_ids)

    # feature_status
    # order, name, transitions, description
    fss = [ ("1", "raised"   , ("suspended", "open", "rejected")
            , "We should start working on it.")
          , ("2", "open"     , ("suspended", "completed")
            , "We are currently working on it.")
          , ("3", "completed", ()
            , "It is completed.")
          , ("4", "rejected" , ("raised", )
            , "We wont do it.")
          , ("5", "suspended", ("raised", )
            , "We will do it later.")
          ]
    feature_status = db.getclass ("feature_status")
    for order, name, trans, desc in fss :
        feature_status.create (name = name, order = order, description = desc)

    for order, name, trans, desc in fss :
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

##     feature_status = db.getclass ("feature_status")
##     # XXX: need the order to be 01, 02, 03, 04 to get sorted properly ???
##     feature_status.create (name = "raised"                 , order = "1")
##     feature_status.create (name = "SRD accepted"           , order = "2")
##     feature_status.create (name = "SDD accepted"           , order = "3")
##     feature_status.create (name = "Testcases accepted"     , order = "4")
##     feature_status.create (name = "Implementation accepted", order = "5")
##     feature_status.create (name = "Testc. & Impl. accepted", order = "6")
##     feature_status.create (name = "Integrationtest OK"     , order = "7")
##     feature_status.create (name = "Integrationtest FAILED" , order = "8")
##     feature_status.create (name = "completed"              , order = "9")
##     feature_status.create (name = "suspended"              , order = "10")
##     feature_status.create (name = "rejected"               , order = "11")

    # defect_status:
    # order, name, cert, description, cert_trans, trans
    dss = [ ("1", "assigned"        , False
            , "Has just been reported"
            , ("analyzed", "closed")
            , ( "resolved"       , "closed-duplicate"
              , "closed-mistaken", "suspended"
              )
            )
          , ("2", "analyzed"        , True
            , "We know what caused the defect"
            , ( "implemented"    , "closed-duplicate"
              , "closed-rejected", "suspended"
              )
            , ()
            )
          , ("3", "implemented"     , True
            , "The fix is implemented"
            , ("analyzed", "resolved", "suspended")
            , ()
            )
          , ("4", "resolved"        , False
            , "The defect is ready for testing"
            , ("closed", )
            , ("closed", "assigned")
            )
          , ("5", "closed"          , False, "Rest in peace"      , (), ())
          , ("6", "closed-duplicate", False, "Is a duplicate"     , (), ())
          , ("7", "closed-mistaken" , False, "Originator went mad", (), ())
          , ("8", "closed-rejected" , True , "We dont do it"      , (), ())
          , ("8", "suspended"       , False
            , "We will fix this later"
            , ("assigned", )
            , ("assigned", )
            )
          ]
    defect_status = db.getclass ("defect_status")
    for order, name, cert, desc, c_trans, trans in dss :
        defect_status.create ( name        = name
                             , cert        = cert
                             , order       = order
                             , description = desc
                             )
    for order, name, cert, desc, c_trans, trans in dss :
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
          , ("4", "SRD", "Software Requirements Document")
          , ("5", "SDD", "Software Design Document")
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

    # create TTTech users:
    # XXX: we should import this from somewhere ;-)
    # but it should reside here - or not ???
    user.create ( username = "priesch"
                , password = password.Password ("priesch")
                , address  = "priesch@tttech.com"
                , roles    = "Admin, User, Nosy"
                )

    user.create ( username = "pr"
                , password = password.Password ("pr")
                , address  = "priesch@tttech.com"
                , roles    = "Admin, User, Nosy"
                )

    # products:
    # name, responsible, description, nosy
    ps = [ ("TTPPlan"     , "priesch", "desc", [])
         , ("TTPCalibrate", "priesch", "desc", [])
         # XXX: add products here
         ]
    product = db.getclass ("product")
    for name, resp, desc, nosy in ps :
        nosy_ids = [user.lookup (u) for u in nosy]
        product.create ( name        = name
                       , responsible = resp
                       , nosy        = nosy_ids
                       , description = desc
                       )

    # meetings
    # title, responsible, nosy
    meetings = \
        [ ("Tools-Meeting", "admin", ["priesch", ])
        , ("SAFT-Meeting",  "pr"   , ["priesch", ])
        # XXX: add other meetings
        ]
    meeting = db.getclass ("meeting")
    for title, resp, nosy in meetings :
        nosy_ids = [user.lookup (u) for u in nosy]
        meeting.create (title = title, responsible = resp,  nosy = nosy_ids)

    # add any additional database create steps here - but only if you
    # haven't initialised the database with the admin "initialise" command

    db.commit()
    db.close()

# vim: set filetype=python ts=4 sw=4 et si

#SHA: 92c54c05ba9f59453dc74fa9fdbbae34f7a9c077
### __END__ dbinit
