# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    initial_data
#
# Purpose
#    Specify the initial initialisation for the tttech2 issue tracker.
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
#     9-Nov-2004 (MPH) Added `completed-but-defects` to `feature_status`
#    16-Nov-2004 (MPH) Added `May Public Queries` permission to `query`
#     1-Dec-2004 (MPH) Added `is_alias` to Class `user`
#     5-Apr-2005 (MPH) Added `composed_of` and `part_of` to `feature`, added
#                      support for Online Peer Reviews
#     6-Apr-2005 (RSC) Factored from dbinit.py
#    11-Apr-2005 (MPH) Fixed Multilink in `review` and `announcement` to link
#                      to `file` instead of `files`
#     6-Jun-2005 (RSC) Incorporate changes from dbinit.py
#    22-Jun-2005 (RSC) time recording stuff added.
#    ««revision-date»»···
#--
#


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
      , ("3", "completed", "comp", ("completed-but-defects",)
        , "It is completed.")
      , ("4", "completed-but-defects", "cdef", ("completed",)
        , "It is completed, but has pending defects.")
      , ("5", "rejected" , "reje", ("raised", )
        , "We wont do it.")
      , ("6", "suspended", "susp", ("raised", )
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

# review_status
# order, name, description
rs = [ ("1", "open"  , "The Review is open"  )
     , ("2", "closed", "The Review is closed")
     ]
r = db.getclass ("review_status")
for order, name, desc in rs :
    r.create (name = name, description = desc, order = order)

# comment_status
# order, name, description, transitions
cs = [ ("1", "assigned", "The Comment just got reported"
       , ("resolved", "rejected")
       )
     , ("2", "resolved", "The Comment got resolved from the author"
       , ("accepted", "assigned")
       )
     , ("3", "accepted", "The Fix is accepted by the reviewer"
       , ()
       )
     , ("4", "rejected", "The Comment got rejected"
       , ()
       )
     ]
comment_status = db.getclass ("comment_status")

for order, name, desc, trans in cs :
    comment_status.create (name = name, description = desc, order = order)

for order, name, desc, trans in cs :
    id = comment_status.lookup (name)
    if trans :
        trans_ids = [comment_status.lookup (t) for t in trans]
        comment_status.set (id, transitions = trans_ids)

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
            , address  = db.config.ADMIN_EMAIL
            , roles    = "Admin"
            )
user.create ( username = "anonymous"
            , roles    = "Anonymous"
            )

daily_record_status = db.getclass ('daily_record_status')
daily_record_status.create \
    ( name        = "open"
    , description = "Open for editing"
    )
daily_record_status.create \
    ( name        = "submitted"
    , description = "Submitted to supervisor"
    )
daily_record_status.create \
    ( name        = "accepted"
    , description = "Accepted by supervisor"
    )

work_location = db.getclass ('work_location')
work_location.create \
    ( code = "on site"
    , description = "Person working at office"
    )
