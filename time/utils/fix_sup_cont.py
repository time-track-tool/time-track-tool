#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

phone = None
try :
    phone = db.contact_type.lookup ('Phone')
except KeyError :
    pass
if not phone :
    db.contact_type.create \
        ( name         = 'Phone'
        , description  = 'Phone number'
        , order        = 1
        )
    db.contact_type.create \
        ( name         = 'Mobile-phone'
        , description  = 'Phone number mobile'
        , order        = 2
        )
    db.contact_type.create \
        ( name         = 'Fax'
        , description  = 'Fax-number'
        , order        = 3
        )
    db.contact_type.create \
        ( name         = 'Email'
        , description  = 'Email Address'
        , url_template = 'mailto:%(contact)s'
        , order        = 4
        )
    db.contact_type.create \
        ( name         = 'Web'
        , description  = 'Internet Home Page'
        , url_template = 'http://%(contact)s'
        , order        = 5
        )
open = None
try :
    open = db.sup_status.lookup ('open')
except KeyError :
    pass

if not open :
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
    db.sup_status.set (open,   transitions = [closed])
    db.sup_status.set (closed, transitions = [open])


assist = None
try :
    assist = db.sup_prio.lookup ('assistance')
except KeyError :
    pass
if not assist :
    db.sup_prio.create (name = "assistance",                          order = 2)
    db.sup_prio.create (name = "one person, important for project",   order = 3)
    db.sup_prio.create (name = "many persons, important for project", order = 4)
    db.sup_prio.create (name = "showstopper for one person",          order = 5)
    db.sup_prio.create (name = "showstopper for many persons",        order = 6)
    db.sup_prio.create (name = "unknown",                             order = 7)

valid = None
try :
    valid = db.valid.lookup ('valid')
except KeyError :
    pass
except AttributeError :
    valid = 1
if not valid :
    db.valid.create \
        ( name = 'valid'
        , description = 'Valid Customer'
        )
    db.valid.create \
        ( name = 'invalid'
        , description = 'No longer valid Customer'
        )

doc_issue_status = None
try :
    doc_issue_status = db.doc_issue_status.lookup ('undecided')
except KeyError :
    pass
if not doc_issue_status :
    users = [db.user.lookup (u) for u in 'macher', 'keitel']
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
        , nosy        = users
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

for sid in db.status.getnodeids () :
    s  = db.status.getnode (sid)
    t  = s.transitions
    t.sort ()
    tn = dict.fromkeys (t).keys ()
    tn.sort ()
    if t != tn :
        db.status.set (sid, transitions = [])
        db.status.set (sid, transitions = tn)

uc_type = db.uc_type.filter (None, {})
if not uc_type :
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
uc_type = db.uc_type.filter (None, dict (order = 5))
if not uc_type :
    x = db.uc_type.lookup ('private Phone')
    db.uc_type.set (x, order = 5)
    db.uc_type.create \
        ( name         = 'external Phone'
        , description  = 'External (non-mobile) Phone number'
        , order        = 4
        , visible      = True
        )
user_contact = db.user_contact.filter (None, {})
if not user_contact :
    for u in db.user.getnodeids () :
        n    = 0
        contacts = []
        user = db.user.getnode (u)
        internal = {}
        mobile   = {}
        private  = {}
        external = {}
        if user.phone :
            internal.setdefault (user.phone, (n, True))
            n += 1
        if user.quick_dialling :
            internal.setdefault (user.quick_dialling, (n, True))
            n += 1
        if user.internal_phone :
            x = user.internal_phone
            if len (x) <= 4 :
                internal.setdefault (x, (n, True))
                n += 1
            else :
                mobile.setdefault (x, (n, True))
                n += 1
        if user.external_phone :
            x = user.external_phone
            if len (x) <= 4 :
                internal.setdefault (x, (n, True))
                n += 1
            else :
                external.setdefault (x, (n, True))
                n += 1
        if user.private_phone :
            x = user.private_phone
            if len (x) <= 4 :
                internal.setdefault (x, (n, True))
                n += 1
            else :
                private.setdefault (x, (n, user.private_phone_visible))
                n += 1
        if user.private_mobile :
            private.setdefault \
                (user.private_mobile, (n, user.private_mobile_visible))

        for k, (n, vi) in internal.iteritems () :
            x = db.user_contact.create \
                ( contact      = k
                , contact_type = db.uc_type.lookup ('internal Phone')
                , order        = n
                , visible      = vi
                , user         = u
                )
            contacts.append (x)
        for k, (n, vi) in mobile.iteritems () :
            x = db.user_contact.create \
                ( contact      = k
                , contact_type = db.uc_type.lookup ('mobile Phone')
                , order        = n
                , visible      = vi
                , user         = u
                )
            contacts.append (x)
        for k, (n, vi) in private.iteritems () :
            x = db.user_contact.create \
                ( contact      = k
                , contact_type = db.uc_type.lookup ('private Phone')
                , order        = n
                , visible      = vi
                , user         = u
                )
            contacts.append (x)
        for k, (n, vi) in external.iteritems () :
            x = db.user_contact.create \
                ( contact      = k
                , contact_type = db.uc_type.lookup ('external Phone')
                , order        = n
                , visible      = vi
                , user         = u
                )
            contacts.append (x)
        if user.address :
            x = db.user_contact.create \
                ( contact      = user.address
                , contact_type = db.uc_type.lookup ('Email')
                , order        = 1
                , visible      = True
                , user         = u
                )
            contacts.append (x)
        if user.alternate_addresses :
            for n, a in enumerate (user.alternate_addresses.split ('\n')) :
                a = a.strip ()
                if not a :
                    continue
                x = db.user_contact.create \
                    ( contact      = a
                    , contact_type = db.uc_type.lookup ('Email')
                    , order        = n + 2
                    , visible      = True
                    , user         = u
                    )
                contacts.append (x)
        db.user.set (u, contacts = contacts)


db.commit ()
