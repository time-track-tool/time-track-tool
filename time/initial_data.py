#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-10 Dr. Ralf Schlatterbeck Open Source Consulting.
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
from rup_utils                      import uni

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
    user_status.create (name = "valid",    description = "Valid user")
    user_status.create (name = "obsolete", description = "No longer valid")
    user_status.create (name = "system",   description = "Needed by system")

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
user = db.getclass ('user')
user.create \
    ( username = "admin"
    , password = adminpw
    , address  = db.config.ADMIN_EMAIL
    , roles    = "Admin"
    )
user.create \
    ( username = "anonymous"
    , roles    = "Anonymous"
    )
if 'it_issue' in db.classes :
    user.create \
        ( username = "helpdesk"
        , address  = db.config.ADMIN_EMAIL
        , status   = db.user_status.lookup ('system')
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
    db.it_category.create (name = 'helpdesk', description = 'Helpdesk Issues')

if 'it_prio' in db.classes :
    db.it_prio.create (name = "nice to have",                        order = 1)
    db.it_prio.create (name = "assistance",                          order = 2)
    db.it_prio.create (name = "one person, important for project",   order = 3)
    db.it_prio.create (name = "many persons, important for project", order = 4)
    db.it_prio.create (name = "showstopper for one person",          order = 5)
    db.it_prio.create (name = "showstopper for many persons",        order = 6)
    db.it_prio.create (name = "unknown",                             order = 7)

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

if 'status' in db.classes :
    ### Since status refers to status_transition and status_transition refers to
    ### status, this needs to be done in three steps

    assert "status_transition" in db.classes, "status needs status_transition"

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

if 'doc_issue_status' in db.classes :
    di1 = db.doc_issue_status.create \
        ( name        = 'undecided'
        , description = 'Unknown if this issue need documentation'
        , order       = 1
        , nosy        = []
        , may_close   = False
        , need_msg    = False
        )
    di2 = db.doc_issue_status.create \
        ( name        = 'needs documentation'
        , description = 'This issue needs documentation (not done yet)'
        , order       = 2
        , nosy        = []
        , may_close   = True
        , need_msg    = True
        )
    di3 = db.doc_issue_status.create \
        ( name        = 'no documentation'
        , description = 'This issue needs no documentation (or already done)'
        , order       = 3
        , nosy        = []
        , may_close   = True
        , need_msg    = True
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
        ( name = uni ('gültig')
        , description = uni ('Gültige Adresse')
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
        ( name         = uni ('gültig')
        , description  = uni ('Gültiger Kunde')
        , order        = 1
        , valid        = True
        )
    db.customer_status.create \
        ( name         = uni ('ungültig')
        , description  = 'Kein Kunde'
        , order        = 2
        , valid        = False
        )

if 'supplier_status' in db.classes :
    db.supplier_status.create \
        ( name         = uni ('gültig')
        , description  = uni ('Gültiger Lieferant')
        , order        = 1
        , valid        = True
        )
    db.supplier_status.create \
        ( name         = uni ('ungültig')
        , description  = 'Kein Lieferant'
        , order        = 2
        , valid        = False
        )

if 'product_status' in db.classes :
    db.product_status.create \
        ( name         = uni ('gültig')
        , description  = uni ('Gültiger Artikel')
        , order        = 1
        , valid        = True
        )
    db.product_status.create \
        ( name         = uni ('ungültig')
        , description  = uni ('Kein gültiger Artikel')
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
        ( name            = uni ('Brief')
        , order           = 1
        , description     = uni ('Vorlage für Briefe')
        , use_for_invoice = False
        , use_for_letter  = True
        )
    db.tmplate_status.create \
        ( name            = uni ('Rechnung')
        , order           = 2
        , description     = uni ('Vorlage für Rechnungen')
        , use_for_invoice = True
        , use_for_letter  = False
        )
    db.tmplate_status.create \
        ( name            = uni ('Ungültig')
        , order           = 1
        , description     = uni ('Vorlage derzeit nicht in Verwendung')
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
        ( tty  = '/dev/ttyUSB0'
        , name = 'USB0'
        , mint = 10
        , sint = 10
        )
    db.user.create \
        ( username = "user"
        , password = adminpw
        , address  = db.config.ADMIN_EMAIL
        , roles    = 'User'
        , timezone = 'Europe/Vienna'
        )
    db.user.create \
        ( username = "guest"
        , password = adminpw
        , address  = db.config.ADMIN_EMAIL
        , roles    = 'Guest'
        , timezone = 'Europe/Vienna'
        )
    db.user.create \
        ( username = "logger"
        , password = adminpw
        , address  = db.config.ADMIN_EMAIL
        , roles    = 'Logger'
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
        , description = 'New or open supprt issue'
        , order       = 1
        )
    closed = db.sup_status.create \
        ( name        = 'closed'
        , description = 'Done support issue'
        , order       = 2
        )
    db.sup_status.set (open,   transitions = [closed])
    db.sup_status.set (closed, transitions = [open])

if 'sup_prio' in db.classes :
    db.sup_prio.create (name = "assistance",                          order = 2)
    db.sup_prio.create (name = "one person, important for project",   order = 3)
    db.sup_prio.create (name = "many persons, important for project", order = 4)
    db.sup_prio.create (name = "showstopper for one person",          order = 5)
    db.sup_prio.create (name = "showstopper for many persons",        order = 6)
    db.sup_prio.create (name = "unknown",                             order = 7)

