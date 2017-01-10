#! /usr/bin/python
# -*- coding: utf-8 -*-
# äöüÄÖÜß
# Copyright (C) 2004-12 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#++
# Name
#    initial_data
#
# Purpose
#    Specify the initial initialisation
#--
#

# init values
from roundup.cgi.TranslationService import get_translation

_ = get_translation (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext

# task_status
# order, name, abbreviation, transitions, description
if 'task_status' in db.classes :
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

if 'document_status' in db.classes :
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

if 'task_kind' in db.classes :
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

if 'feature_status' in db.classes :
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

if 'action_item_status' in db.classes :
    # action_item_status
    # order, name, description
    ais = [ ("1", "open"  , "The Action-Item is open"  )
          , ("2", "closed", "The Action-Item is closed")
          ]
    ai = db.getclass ("action_item_status")
    for order, name, desc in ais :
        ai.create (name = name, description = desc, order = order)

if 'review_status' in db.classes :
    # review_status
    # order, name, description
    rs = [ ("1", "open"  , "The Review is open"  )
         , ("2", "closed", "The Review is closed")
         ]
    r = db.getclass ("review_status")
    for order, name, desc in rs :
        r.create (name = name, description = desc, order = order)

if 'comment_status' in db.classes :
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

if 'defect_status' in db.classes :
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

if 'document_type' in db.classes :
    # document_type
    # order, name, description
    dts = [ ("1", "ES" , "Evaluation Sheet"             )
          , ("2", "CMP", "Configuration Management Plan")
          , ("3", "HTP", "High-Level Test Plan"         )
          ]
    doc_type = db.getclass ("document_type")
    for order, name, desc in dts :
        doc_type.create (name = name, description = desc, order = order)

if 'severity' in db.classes :
    # severity
    # order, name
    ss = ( (1, "Minor",       "m")
         , (2, "Major",       "M")
         , (3, "Showstopper", "S")
         )
    severity = db.getclass ("severity")
    for order, name, abbr in ss :
        severity.create (name = name, order = order, abbreviation = abbr)

if 'user_status' in db.classes :
    # user status must come first.
    user_status = db.getclass ('user_status')
    user_status.create \
        (name = "valid",    is_nosy = True,  description = "Valid user")
    user_status.create \
        (name = "obsolete", is_nosy = False, description = "No longer valid")
    user_status.create \
        (name = "system",   is_nosy = True,  description = "Needed by system")

if 'uc_type' in db.classes :
    db.uc_type.create \
        ( name         = 'Email'
        , description  = 'Email address'
        , order        = 1
        , url_template = 'mailto:%(contact)s'
        , visible      = True
        )
    db.uc_type.create \
        ( name         = 'internal Phone'
        , description  = 'Internal Phone number'
        , order        = 2
        , visible      = True
        )
    db.uc_type.create \
        ( name         = 'mobile Phone'
        , description  = 'Mobile Phone number'
        , order        = 3
        , visible      = True
        )
    db.uc_type.create \
        ( name         = 'private Phone'
        , description  = 'Private Phone number'
        , order        = 4
        , visible      = False
        )

# users
# create the two default users
admin = dict \
    ( username = "admin"
    , password = adminpw
    , roles    = "Admin"
    )

if 'transceiver' not in db.classes :
    admin ['address'] = db.config.ADMIN_EMAIL
db.user.create (**admin)
db.user.create \
    ( username = "anonymous"
    , roles    = "Anonymous"
    )
if 'it_issue' in db.classes :
    db.user.create \
        ( username = "helpdesk"
        , address  = db.config.ADMIN_EMAIL
        , status   = db.user_status.lookup ('system')
        )
    if hasattr (db, 'sql') :
        db.sql ('create index _it_issue_status_idx on _it_issue (_status);')
        db.sql ('create index _it_issue_it_prio_idx on _it_issue (_it_prio);')
        db.sql ('create index _it_issue_category_idx on _it_issue (_category);')
        db.sql ('create index _it_issue_it_project_idx '
                'on _it_issue (_it_project);'
               )
        db.sql ('create index _it_issue_responsible_idx '
                'on _it_issue (_responsible);'
               )
        db.sql ('create index _it_issue_stakeholder_idx '
                'on _it_issue (_stakeholder);'
               )

if 'daily_record' in db.classes and hasattr (db, 'sql') :
    db.sql ('create index _daily_record_date_idx on _daily_record ( _date );')
    db.sql ('create index _daily_record_user_idx on _daily_record ( _user );')

if 'time_record' in db.classes and hasattr (db, 'sql') :
    db.sql ('create index _time_record_wp_idx on _time_record (_wp);')
    db.sql ('create index _time_record_daily_record_idx '
            'on _time_record (_daily_record);'
           )
    db.sql ('create index _time_record_wp_daily_record_idx '
            'on _time_record (_wp, _daily_record);'
           )
    db.sql ('create index _time_record_time_activity_idx '
            'on _time_record (_time_activity);'
           )
    db.sql ('create index _time_record_time_activity_daily_record_idx '
            'on _time_record (_time_activity, _daily_record);'
           )

if 'daily_record_status' in db.classes :
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
    daily_record_status.create \
        ( name        = "leave"
        , description = "Accepted leave"
        )

if 'work_location' in db.classes :
    work_location = db.getclass ('work_location')
    work_location.create \
        ( code = "office"
        , description = "Abwesend"
        )
    work_location.create \
        ( code = "home"
        , description = "Zuhause / Home office"
        )
    work_location.create \
        ( code = "off-site/trav."
        , description =
          "Travel -- Unterwegs, Dienstgang, Dienstreise "
          "(reisend oder an einer fremden Location)"
        )
    work_location.create \
        ( code = "other"
        , description = "In einer anderen als der eigenen Org-Location"
        )
    work_location.create \
        ( code = "off"
        , description = "Abwesend"
        )
    work_location.create \
        ( code = "on site"
        , description = "Person working at customer site"
        )

if 'sex' in db.classes :
    sex = db.getclass ('sex')
    sex.create (name = "female")
    sex.create (name = "male")

if 'summary_type' in db.classes :
    summary_type = db.summary_type
    summary_type.create (name = "day",   is_staff = False, order = 1)
    summary_type.create (name = "week",  is_staff = True,  order = 2)
    summary_type.create (name = "month", is_staff = True,  order = 3)
    summary_type.create (name = "range", is_staff = True,  order = 4)

if 'dns_record_type' in db.classes :
    dns_record_type = db.dns_record_type
    dns_record_type.create (name = "invalid",   description = "don't use")
    dns_record_type.create (name = "A",         description = "A record")
    dns_record_type.create (name = "CNAME",     description = "CNAME record")

def gen_status (cls, list) :
    for order, name, desc, trans in list :
        cls.create \
            ( name         = name
            , order        = order
            , description  = desc
            )
    for order, name, desc, trans in list :
        id = cls.lookup (name)
        if trans :
            trans_ids = [cls.lookup (t) for t in trans]
            cls.set (id, transitions = trans_ids)

if 'it_issue_status' in db.classes :
    its = [ (1, "new",      "Has just been reported"
            , ("open", "feedback", "closed")
            )
          , (2, "open",     "Not resolved"
            , ("feedback", "closed")
            )
          , (3, "feedback", "Need feedback from another person"
            , ("open", "closed")
            )
          , (4, "closed",   "Closed"
            , ("feedback", "open")
            )
          ]
    gen_status (db.getclass ("it_issue_status"), its)

if 'it_project_status' in db.classes :
    its = [ (1, "open",      "Not yet resolved", ("closed", ))
          , (2, "closed",    "Resolved",         ("open", ))
          ]
    gen_status (db.getclass ("it_project_status"), its)

if 'it_category' in db.classes :
    db.it_category.create \
        (name = 'helpdesk', description = 'Helpdesk Issues', valid = True)

if 'it_prio' in db.classes :
    db.it_prio.create (name = "nice to have",                        order = 1)
    db.it_prio.create (name = "assistance",                          order = 2)
    db.it_prio.create (name = "one person, important for project",   order = 3)
    db.it_prio.create (name = "many persons, important for project", order = 4)
    db.it_prio.create (name = "showstopper for one person",          order = 5)
    db.it_prio.create (name = "showstopper for many persons",        order = 6)
    db.it_prio.create \
        (name = "unknown", must_change = True, default = True, order = 7)

if 'area' in db.classes :
    db.area.create (name = "SW",  description = "Software")
    db.area.create (name = "HW",  description = "Hardware")
    db.area.create (name = "Doc", description = "Documentation")
    db.area.create (name = "IT",  description = "Information Technology")

if 'category' in db.classes :
    db.category.create \
        ( name        = "pending"
        , responsible = "admin"
        , valid       = True
        , cert_sw     = False
        , description = "Category for faulty PRs"
        )

if 'kind' in db.classes :
    db.kind.create \
        ( name        = "Bug"
        , description = "A defect in the software"
        )
    db.kind.create \
        ( name        = "Change-Request"
        , description = "New functionality requested"
        )
    db.kind.create \
        ( name        = "Wart"
        , description = "Broken Window hindering development"
        )
    db.kind.create \
        ( name        = "Support"
        , description = "Support item"
        )
    db.kind.create \
        ( name        = "Mistaken"
        , description = "Misunderstanding on reporter's side"
        )
    db.kind.create \
        ( name        = "Obsolete"
        , description = "No longer relevant"
        )

if 'msg_keyword' in db.classes :
    db.msg_keyword.create \
        ( name        = "Reporting"
        , description = "Relevant for reporting to management"
        )
    db.msg_keyword.create \
        ( name        = "Design"
        , description = "Documentation of Design"
        )

if 'status' in db.classes and 'status_transition' in db.classes :
    ### Since status refers to status_transition and status_transition refers to
    ### status, this needs to be done in three steps

    status_lst = \
        ( ('analyzing', 'Require Analysis', ('o_wo_msg', 'e', 'c'))
        , ('open',      'Open to be implemented', 'acest')
        , ('feedback',  'Require Feedback', ('o_wo_msg', 'c_w_msg'))
        , ('escalated', 'Require Decision', 'acos')
        , ('testing',   'Independent Test', 'oc')
        , ('suspended', 'Will currently not be implemented', 'e')
        , ('closed',    'Done', 'o')
        )
    trans_lst = dict \
        ( a        = ('To analyzing',                     'analyzing', 1, 0)
        , f        = ('To feedback',                      'feedback',  1, 1)
        , t        = ('To testing',                       'testing',   1, 1)
        , s        = ('To suspended',                     'suspended', 1, 0)
        , o        = ('To open',                          'open',      1, 0)
        , o_wo_msg = ('To open without required message', 'open',      0, 0)
        , o_wo_ch  = ('To open with changed responsible', 'open',      1, 1)
        , e        = ('To escalated',                     'escalated', 1, 0)
        , c        = ('To closed',                        'closed',    0, 0)
        , c_w_msg  = ('To closed with message',           'closed',    1, 0)
        )

    for order, (name, desc, x) in enumerate (status_lst) :
        db.status.create (name = name, order = str (order), description = desc)

    for name, tgt, msg, resp in trans_lst.itervalues () :
        db.status_transition.create \
            ( name                = name
            , target              = tgt
            , require_msg         = msg
            , require_resp_change = resp
            )

    for name, x, trans in status_lst :
        status             = db.status.getnode (db.status.lookup (name))
        status.transitions = [trans_lst [t] [0] for t in trans]
elif 'status' in db.classes :
    st_o = db.status.create \
        ( name        = "open"
        , description = "Open Issue"
        , order       = 1
        , relaxed     = False
        )
    st_c = db.status.create \
        ( name        = "closed"
        , description = "Done"
        , order       = 2
        , relaxed     = False
        )
    st_p = db.status.create \
        ( name        = "postponed"
        , description = "Not currently being worked on"
        , order       = 3
        , relaxed     = False
        )
    db.status.set (st_o, transitions = [st_c, st_p])
    db.status.set (st_c, transitions = [st_o, st_p])
    db.status.set (st_p, transitions = [st_o, st_c])

if 'prio' in db.classes :
    db.prio.create (name = "nice to have", order =  10)
    db.prio.create (name = "high",         order =  20)
    db.prio.create (name = "showstopper",  order =  30)
    db.prio.create (name = "unknown",      order = 100)

if 'doc_issue_status' in db.classes :
    all_stati  = db.status.getnodeids ()
    testing    = db.status.lookup ("testing")
    no_testing = [s for s in all_stati if s != testing]
    di1 = db.doc_issue_status.create \
        ( name        = 'undecided'
        , description = 'Unknown if this issue need documentation'
        , order       = 1
        , nosy        = []
        , need_msg    = False
        , may_change_state_to = no_testing
        )
    di2 = db.doc_issue_status.create \
        ( name        = 'needs documentation'
        , description = 'This issue needs documentation (not done yet)'
        , order       = 2
        , nosy        = []
        , need_msg    = True
        , may_change_state_to = all_stati
        )
    di3 = db.doc_issue_status.create \
        ( name        = 'no documentation'
        , description = 'This issue needs no documentation (or already done)'
        , order       = 3
        , nosy        = []
        , need_msg    = True
        , may_change_state_to = all_stati
        )
    for k in di1, di2, di3 :
        db.doc_issue_status.set (k, transitions = [di1, di2, di3])

if 'overtime_period' in db.classes :
    db.overtime_period.create \
        (name = "week",  order = 0, months = 0,  weekly = True)
    db.overtime_period.create \
        (name = "month", order = 1, months = 1,  weekly = False)
    db.overtime_period.create \
        (name = "year",  order = 2, months = 12, weekly = False)

if 'currency' in db.classes :
    currency = db.getclass ('currency')
    currency.create (name = 'CHF', description = 'Schweizer Franken')
    currency.create (name = 'EUR', description = 'Euro')
    currency.create (name = 'GBP', description = 'Britische Pfund')
    currency.create (name = 'USD', description = 'US-Dollar')

if 'valid' in db.classes :
    valid = db.getclass ('valid')
    valid.create \
        ( name = 'gültig'
        , description = 'Gültige Adresse'
        )

if 'adr_type_cat' in db.classes :
    db.adr_type_cat.create (code = 'ABO', description = 'Laufende Abos')

if 'contact_type' in db.classes :
    db.contact_type.create \
        ( name         = 'Telefon'
        , description  = 'Telefonnummer privat/Firma'
        , order        = 1
        )
    db.contact_type.create \
        ( name         = 'Fax'
        , description  = 'Faxnummer'
        , order        = 3
        )
    db.contact_type.create \
        ( name         = 'Email'
        , description  = 'Email Adresse'
        , url_template = 'mailto:%(contact)s'
        , order        = 4
        )
    db.contact_type.create \
        ( name         = 'Web'
        , description  = 'Internet Home Page'
        , url_template = 'http://%(contact)s'
        , order        = 5
        )
    db.contact_type.create \
        ( name         = 'Mobiltelefon'
        , description  = 'Telefonnummer mobil'
        , order        = 2
        )
if 'customer_status' in db.classes :
    db.customer_status.create \
        ( name         = 'gültig'
        , description  = 'Gültiger Kunde'
        , order        = 1
        , valid        = True
        )
    db.customer_status.create \
        ( name         = 'ungültig'
        , description  = 'Kein Kunde'
        , order        = 2
        , valid        = False
        )

if 'supplier_status' in db.classes :
    db.supplier_status.create \
        ( name         = 'gültig'
        , description  = 'Gültiger Lieferant'
        , order        = 1
        , valid        = True
        )
    db.supplier_status.create \
        ( name         = 'ungültig'
        , description  = 'Kein Lieferant'
        , order        = 2
        , valid        = False
        )

if 'product_status' in db.classes :
    db.product_status.create \
        ( name         = 'gültig'
        , description  = 'Gültiger Artikel'
        , order        = 1
        , valid        = True
        )
    db.product_status.create \
        ( name         = 'ungültig'
        , description  = 'Kein gültiger Artikel'
        , order        = 2
        , valid        = False
        )

if 'weekday' in db.classes :
    for n, d in enumerate \
        (( 'Montag'
         , 'Dienstag'
         , 'Mittwoch'
         , 'Donnerstag'
         , 'Freitag'
         , 'Samstag'
         , 'Sonntag'
        )) :
        db.weekday.create (name = d, order = n + 1)

if 'product_type' in db.classes :
    db.product_type.create (name = "D", description = "Document")
    db.product_type.create (name = "S", description = "Software")
    db.product_type.create (name = "H", description = "Hardware")

if 'doc_status' in db.classes :
    lst = ("work in progress", "draft", "released", "obsolete")
    for nr, name in enumerate (lst) :
        db.doc_status.create (name = name, order = nr)

if 'tmplate_status' in db.classes :
    db.tmplate_status.create \
        ( name            = 'Brief'
        , order           = 1
        , description     = 'Vorlage für Briefe'
        , use_for_invoice = False
        , use_for_letter  = True
        )
    db.tmplate_status.create \
        ( name            = 'Rechnung'
        , order           = 2
        , description     = 'Vorlage für Rechnungen'
        , use_for_invoice = True
        , use_for_letter  = False
        )
    db.tmplate_status.create \
        ( name            = 'Ungültig'
        , order           = 1
        , description     = 'Vorlage derzeit nicht in Verwendung'
        , use_for_invoice = False
        , use_for_letter  = False
        )

if 'time_project_status' in db.classes :
    db.time_project_status.create (name = 'New',        active = False)
    db.time_project_status.create (name = 'Open',       active = True)
    db.time_project_status.create (name = 'Post-Prjct', active = True)
    db.time_project_status.create (name = 'Hold',       active = False)
    db.time_project_status.create (name = 'Closed',     active = False)

if 'cost_center_status' in db.classes :
    db.cost_center_status.create (name = 'New',    active = False)
    db.cost_center_status.create (name = 'Open',   active = True)
    db.cost_center_status.create (name = 'Closed', active = False)

if 'time_activity' in db.classes :
    db.time_activity.create (name = 'study',          travel = False)
    db.time_activity.create (name = 'info transfer',  travel = False)
    db.time_activity.create (name = 'sell',           travel = False)
    db.time_activity.create (name = 'plan',           travel = False)
    db.time_activity.create (name = 'review',         travel = False)
    db.time_activity.create (name = 'document',       travel = False)
    db.time_activity.create (name = 'execute',        travel = False)
    db.time_activity.create (name = 'test',           travel = False)
    db.time_activity.create (name = 'administer',     travel = False)
    db.time_activity.create (name = 'travel passive', travel = True)
    db.time_activity.create (name = 'travel active',  travel = False)

if 'person_type' in db.classes :
    db.person_type.create \
        ( name        = _ (""'invoice')
        , description = _ (""'Invoice Address')
        , order       = 1
        )
    db.person_type.create \
        ( name        = _ (""'shipping')
        , description = _ (""'Shipping Address')
        , order       = 2
        )
    db.person_type.create \
        ( name        = _ (""'supply')
        , description = _ (""'Address used for fetching supplies from supplier')
        , order       = 3
        )
    db.person_type.create \
        ( name        = _ (""'contact')
        , description = _ (""'Address of a personal contact')
        , order       = 4
        )

if 'logstyle' in db.classes :
    db.logstyle.create \
        ( name        = 'circ'
        , description = _ (""'Circular logging')
        , order       = 1
        )
    db.logstyle.create \
        ( name        = 'start'
        , order       = 2
        )
    db.logstyle.create \
        ( name        = 'stop'
        , order       = 3
        )
    db.logstyle.create \
        ( name        = 'full'
        , order       = 4
        )
if 'transceiver' in db.classes :
    db.transceiver.create \
        ( tty          = '/dev/ttyS0'
        , name         = 'S0'
        , mint         = 10
        , mint_pending = False
        , sint         = 60
        , sint_pending = False
        )
    db.user.create \
        ( username = "guest"
        , password = adminpw
        , roles    = 'Guest'
        , timezone = 'Europe/Vienna'
        )
    db.user.create \
        ( username = "logger"
        , password = adminpw
        , roles    = 'Logger'
        )
if 'measurement' in db.classes and hasattr (db, 'sql') :
    db.sql \
        ('create index _measurement_date_idx_ '
         'on _measurement using btree '
         '( _sensor'
         ', __retired__'
         ', (_measurement._date is not NULL) desc'
         ', _date desc'
         ', id'
         ');'
        )

if 'dyndns' in db.classes :
    db.dyndns.create \
        ( syslog         = True
        , web_url        = 'dyndns'
        , local_hostname = 'localhost'
        )
    db.dyndns_protocol.create \
        ( name           = 'dyndns2'
        , order          = 1
        , default_server = 'members.dyndns.org'
        , description    = "free dynamic DNS service offered by www.dyndns.org"
        )
# Dead
#   db.dyndns_protocol.create \
#       ( name           = 'concont'
#       , order          = 2
#       , default_server = 'www.dydns.za.net'
#       , description    = "used by the free dyndns service Tyrmida "
#                          "www.dydns.za.net"
#       )
    db.dyndns_protocol.create \
        ( name           = 'dnspark'
        , order          = 3
        , default_server = 'www.dnspark.com'
        , description    = "DNS service offered by www.dnspark.com"
        )
    db.dyndns_protocol.create \
        ( name           = 'dslreports1'
        , order          = 4
        , default_server = 'www.dslreports.com'
        , description    = "free DSL monitoring service www.dslreports.com"
        )
    db.dyndns_protocol.create \
        ( name           = 'easydns'
        , order          = 5
        , default_server = 'members.easydns.com'
        , description    = "for fee DNS service offered by www.easydns.com"
        )
# Dead
#   db.dyndns_protocol.create \
#       ( name           = 'hammernode1'
#       , order          = 6
#       , default_server = 'www.hn.org'
#       , description    = "free dynamic DNS service by Hammernode www.hn.org"
#       )
    db.dyndns_protocol.create \
        ( name           = 'namecheap'
        , order          = 7
        , default_server = 'dynamicdns.park-your-domain.com'
        , description    = "DNS service offered by www.namecheap.com"
        )
    db.dyndns_protocol.create \
        ( name           = 'sitelutions'
        , order          = 8
        , default_server = 'sitelutions.com'
        , description    = "DNS services offered by www.sitelutions.com"
        )
    db.dyndns_protocol.create \
        ( name           = 'zoneedit1'
        , order          = 9
        , default_server = 'www.zoneedit.com'
        , description    = 'DNS service offered by www.zoneedit.com'
        )

if 'sup_status' in db.classes :
    open = db.sup_status.create \
        ( name        = 'open'
        , description = 'New or open support issue'
        , order       = 1
        )
    closed = db.sup_status.create \
        ( name        = 'closed'
        , description = 'Done support issue'
        , order       = 2
        )
    satisfied = db.sup_status.create \
        ( name        = 'satisfied'
        , description = 'Customer is satisfied'
        , order       = 3
        )
    db.sup_status.set (open,      transitions = [closed, satisfied])
    db.sup_status.set (closed,    transitions = [open, satisfied])
    db.sup_status.set (satisfied, transitions = [open, closed])

if 'sup_prio' in db.classes :
    db.sup_prio.create (name = "assistance",                          order = 2)
    db.sup_prio.create (name = "one person, important for project",   order = 3)
    db.sup_prio.create (name = "many persons, important for project", order = 4)
    db.sup_prio.create (name = "showstopper for one person",          order = 5)
    db.sup_prio.create (name = "showstopper for many persons",        order = 6)
    db.sup_prio.create (name = "unknown",                             order = 7)

if 'umts' in db.classes :
    db.umts.create (tty = "/dev/ttyUSB0")

if 'email' in db.classes :
    db.email.create (server = "smtp.example.com")

if 'ham_band' in db.classes :
    db.ham_band.create (name = '6m',   order =  100)
    db.ham_band.create (name = '10m',  order =  200)
    db.ham_band.create (name = '12m',  order =  300)
    db.ham_band.create (name = '15m',  order =  400)
    db.ham_band.create (name = '17m',  order =  500)
    db.ham_band.create (name = '20m',  order =  600)
    db.ham_band.create (name = '30m',  order =  700)
    db.ham_band.create (name = '40m',  order =  800)
    db.ham_band.create (name = '80m',  order =  900)
    db.ham_band.create (name = '160m', order = 1000)

if 'ham_mode' in db.classes :
    db.ham_mode.create (name = 'PSK31',   order = 100)
    db.ham_mode.create (name = 'PSK63',   order = 110)
    db.ham_mode.create (name = 'PSK125',  order = 120)
    db.ham_mode.create (name = 'QPSK31',  order = 200)
    db.ham_mode.create (name = 'QPSK63',  order = 210)
    db.ham_mode.create (name = 'QPSK125', order = 220)
    db.ham_mode.create (name = 'MFSK16',  order = 300)
    db.ham_mode.create (name = 'RTTY',    order = 400)
    db.ham_mode.create (name = 'HELL',    order = 500)
    db.ham_mode.create (name = 'OLIVIA',  order = 600)

if 'qsl_type' in db.classes :
    db.qsl_type.create (name = 'eQSL',    order = 10, code = 1)
    db.qsl_type.create (name = 'LOTW',    order = 20, code = 2)
    db.qsl_type.create (name = 'Bureau',  order = 30, code = 4)
    db.qsl_type.create (name = 'Direct',  order = 40, code = 4)

if 'qsl_status' in db.classes :
    db.qsl_status.create (name = 'eQSL',            code = 1)
    db.qsl_status.create (name = 'LOTW',            code = 2)
    db.qsl_status.create (name = 'eQSL+LOTW',       code = 3)
    db.qsl_status.create (name = 'paper',           code = 4)
    db.qsl_status.create (name = 'eQSL+paper',      code = 5)
    db.qsl_status.create (name = 'LOTW+paper',      code = 6)
    db.qsl_status.create (name = 'eQSL+LOTW+paper', code = 7)
    db.qsl_status.create (name = 'none',            code = 0)
if 'external_company' in db.classes :
    user_status.create (name = "external", description = "External user")
if 'project_type' in db.classes :
    db.project_type.create (order = 1, name = 'Initial Development')
    db.project_type.create (order = 2, name = 'Further Development')
    db.project_type.create (order = 3, name = 'Maintenance')
    db.project_type.create (order = 4, name = 'Support')
    db.project_type.create (order = 5, name = 'Engineering')
if 'sup_type' in db.classes :
    db.sup_type.create (order = 1, name = 'Support Issue')
    db.sup_type.create (order = 2, name = 'RMA Issue')
    db.sup_type.create (order = 3, name = 'Supplier Claim')
    db.sup_type.create (order = 4, name = 'Other')
if 'sup_execution' in db.classes :
    db.sup_execution.create (order = 1, name = 'Repair')
    db.sup_execution.create (order = 2, name = 'Replace')
    db.sup_execution.create (order = 3, name = 'Refund')
    db.sup_execution.create (order = 4, name = 'Return')
if 'prodcat' in db.classes :
    db.sql ('ALTER TABLE _prodcat ADD UNIQUE (_name, _level);')
if 'leave_status' in db.classes :
    v1 = db.leave_status.create (name = 'open',             order = 1)
    v2 = db.leave_status.create (name = 'submitted',        order = 2)
    v3 = db.leave_status.create (name = 'accepted',         order = 3)
    v4 = db.leave_status.create (name = 'declined',         order = 4)
    v5 = db.leave_status.create (name = 'cancel requested', order = 5)
    v6 = db.leave_status.create (name = 'cancelled',        order = 6)
    db.leave_status.set (v1, transitions = [v2, v6, v3])
    db.leave_status.set (v2, transitions = [v1, v3, v4])
    db.leave_status.set (v3, transitions = [v5])
    db.leave_status.set (v5, transitions = [v3, v6])
if 'purchase_type' in db.classes :
    db.purchase_type.create \
        ( name       = 'Service'
        , order      = 10
        , view_roles = "Procurement"
        )
    db.purchase_type.create \
        ( name       = 'IT-Assett'
        , order      = 20
        , roles      = "IT-Approval"
        , view_roles = "Procurement"
        )
    db.purchase_type.create \
        ( name       = 'Assett'
        , order      = 25
        , roles      = "Procurement"
        , view_roles = "Procurement"
        )
    db.purchase_type.create \
        ( name       = 'IT-Hardware'
        , order      = 30
        , roles      = "IT-Approval"
        , view_roles = "Procurement"
        )
    db.purchase_type.create \
        ( name       = 'Hardware'
        , order      = 35
        , roles      = "Procurement"
        , view_roles = "Procurement"
        )
    db.purchase_type.create \
        ( name       = 'IT-Software'
        , order      = 40
        , roles      = "IT-Approval"
        , view_roles = "Procurement"
        )
    db.purchase_type.create \
        ( name       = 'Software'
        , order      = 45
        , roles      = "Procurement"
        , view_roles = "Procurement"
        )
    db.purchase_type.create \
        ( name       = 'Stock'
        , order      = 50
        , view_roles = "Procurement"
        )
    db.purchase_type.create \
        ( name       = 'Subcontracting'
        , order      = 60
        , roles      = "Subcontract,HR"
        , view_roles = "Procurement"
        )
    db.purchase_type.create \
        ( name       = 'Other'
        , order      = 70
        , roles      = "Procurement"
        , view_roles = "Procurement"
        )
    if hasattr (db, 'sql') :
        db.sql ('alter table _purchase_request alter column '
                '_total_cost type double precision;'
               )
        db.sql ('alter table _pr_offer_item alter column '
                '_price_per_unit type double precision;'
               )
if 'pr_status' in db.classes :
    s1 = db.pr_status.create (name = 'open',      order = 1)
    s2 = db.pr_status.create (name = 'approving', order = 2, relaxed = True)
    s3 = db.pr_status.create (name = 'approved',  order = 3, relaxed = True)
    s4 = db.pr_status.create (name = 'rejected',  order = 4)
    s5 = db.pr_status.create (name = 'cancelled', order = 5)
    s6 = db.pr_status.create (name = 'ordered',   order = 6)
    s7 = db.pr_status.create (name = 'delivered', order = 7)
    db.pr_status.set (s1, transitions = [s2, s5])
    db.pr_status.set (s2, transitions = [s3, s4, s5])
    db.pr_status.set (s3, transitions = [s6])
    db.pr_status.set (s6, transitions = [s7])
if 'pr_approval_status' in db.classes :
    s1 = db.pr_approval_status.create (name = 'undecided', order = 1)
    s2 = db.pr_approval_status.create (name = 'approved',  order = 2)
    s3 = db.pr_approval_status.create (name = 'rejected',  order = 3)
    db.pr_approval_status.set (s1, transitions = [s2, s3])
if 'pr_approval_order' in db.classes :
    db.pr_approval_order.create (role = '',            order = 10)
    db.pr_approval_order.create (role = 'procurement', order = 20)
    db.pr_approval_order.create (role = 'it-approval', order = 30)
    db.pr_approval_order.create (role = 'quality',     order = 35)
    db.pr_approval_order.create (role = 'subcontract', order = 40)
    db.pr_approval_order.create (role = 'hr',          order = 50)
    db.pr_approval_order.create (role = 'finance',     order = 60)
    db.pr_approval_order.create (role = 'board',       order = 70)
if 'pr_currency' in db.classes :
    db.pr_currency.create (name = '€', order = 10, max_sum = 10000)
    db.pr_currency.create (name = '$', order = 20, max_sum = 10000)
if 'it_request_type' in db.classes :
    db.it_request_type.create (name = 'Incident',       order = 1)
    db.it_request_type.create (name = 'Change Request', order = 2)
if 'ext_tracker_type' in db.classes :
    db.ext_tracker_type.create (name = 'Jira', order = 10)
    db.ext_tracker_type.create (name = 'KPM',  order = 20)
if 'absence_type' in db.classes :
    db.absence_type.create \
        ( code = 'A'
        , cssclass = 'absence'
        , description = 'Absence like Sick-leave, Comp Time, Special Leave ...'
        )
    db.absence_type.create \
        ( code = 'H'
        , cssclass = 'absence'
        , description = 'Home Office'
        )
    db.absence_type.create \
        ( code = 'T'
        , cssclass = 'absence'
        , description = 'Travel'
        )
    db.absence_type.create \
        ( code = 'TW'
        , cssclass = 'absence'
        , description = 'Training, Workshop, Conference'
        )
    db.absence_type.create \
        ( code = 'V'
        , cssclass = 'absence'
        , description = 'Vacation'
        )
if 'time_wp_summary_no' in db.classes :
    db.time_wp_summary_no.create \
        ( name  = 'Project management'
        , order = 100
        )
    db.time_wp_summary_no.create \
        ( name  = 'Configuration management'
        , order = 200
        )
    db.time_wp_summary_no.create \
        ( name  = 'Training'
        , order = 300
        )
    db.time_wp_summary_no.create \
        ( name  = 'Quality'
        , order = 400
        )
    db.time_wp_summary_no.create \
        ( name  = 'Requirements'
        , order = 500
        )
    db.time_wp_summary_no.create \
        ( name  = 'Design'
        , order = 600
        )
    db.time_wp_summary_no.create \
        ( name  = 'Implementation'
        , order = 700
        )
    db.time_wp_summary_no.create \
        ( name  = 'Module, Unit test'
        , order = 800
        )
    db.time_wp_summary_no.create \
        ( name  = 'Integration'
        , order = 900
        )
    db.time_wp_summary_no.create \
        ( name  = 'System test, Verification'
        , order = 1000
        )

if 'ext_tracker_state' in db.classes and hasattr (db, 'sql') :
    db.sql \
        ( 'alter table _ext_tracker_state add constraint '
          'issue_ext_tracker_uniq unique '
          '(_issue, _ext_tracker, __retired__);'
        )

if 'kpm' in db.classes and hasattr (db, 'sql') :
    db.sql \
        ( 'alter table _kpm add constraint issue_uniq unique '
          '(_issue, __retired__);'
        )

if 'daily_record' in db.classes and hasattr (db, 'sql') :
    db.sql \
        ( 'alter table _daily_record add constraint '
          'daily_record_user_date unique (_user, _date, __retired__);'
        )
