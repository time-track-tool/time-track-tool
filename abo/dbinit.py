#! /usr/bin/python
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
# $Id$

import os

import config
from select_db import Database, Class, FileClass, IssueClass
from rup_utils import uni

def open(name=None):
    ''' as from the roundupdb method openDB 
    ''' 
    from roundup.hyperdb import String, Password, Date, Link, Multilink
    from roundup.hyperdb import Interval, Boolean, Number

    # open the database
    db = Database(config, name)

    #
    # Now initialise the schema. Must do this each time the database is
    # opened.
    #

    # Class automatically gets these properties:
    #   creation = Date ()
    #   activity = Date ()
    #   creator  = Link ('user')

    abo = Class \
        ( db, "abo"
        , begin               = Date      ()
        , end                 = Date      ()
        , aboprice            = Link      ('abo_price')
        , payer               = Link      ('address')
        , subscriber          = Link      ('address')
        , amount              = Number    ()
        , messages            = Multilink ("msg")
        )

    abo_price = Class \
        ( db, "abo_price"
        , abotype             = Link      ('abo_type')
        , currency            = Link      ('currency')
        , amount              = Number    ()
        , name                = String    ()
        )

    abo_type = Class \
        ( db, "abo_type"
        , name                = String    ()
        , description         = String    ()
        , order               = Number    ()
        )
    abo_type.setkey ("name")

    address = Class \
        ( db, "address"
        , title               = String    ()
        , firstname           = String    ()
        , lastname            = String    ()
        , function            = String    ()
        , street              = String    ()
        , country             = String    ()
        , postalcode          = String    ()
        , city                = String    ()
        , phone               = String    ()
        , fax                 = String    ()
        , salutation          = String    ()
        , messages            = Multilink ("msg")
        , email               = String    ()
        , abos                = Multilink ("abo")
        , payed_abos          = Multilink ("abo")
        , adr_type            = Multilink ("adr_type")
        , valid               = Link      ("valid")
        )

    adr_type = Class \
        ( db, "adr_type"
        , code                = String    ()
        , description         = String    ()
        )
    adr_type.setkey ("code")

    currency = Class \
        ( db, "currency"
        , name                = String    ()
        , description         = String    ()
        )
    currency.setkey ("name")

    # Define codes for (in)valid addresses, e.g., "verstorben"
    valid = Class \
        ( db, "valid"
        , name                = String    ()
        , description         = String    ()
        )
    valid.setkey ("name")

    query = Class \
        ( db, "query"
        , klass               = String    ()
        , name                = String    ()
        , url                 = String    ()
        , private_for         = Link      ('user')
        )
    query.setkey("name")


    # Note: roles is a comma-separated string of Role names
    user = Class \
        ( db, "user"
        , username            = String    ()
        , password            = Password  ()
        # used by email gateway:
        , address             = String    ()
        , realname            = String    ()
        , alternate_addresses = String    ()
        # other framework parts in rup
        , queries             = Multilink ('query')
        , roles               = String    ()
        , timezone            = String    ()
        # optional
        , nickname            = String    ()
        )
    user.setkey("username")

    # FileClass automatically gets these properties:
    #   content = String()    [saved to disk in <tracker home>/db/files/]
    #   (it also gets the Class properties creation, activity and creator)
    msg = FileClass \
        ( db
        , "msg"
        , date                  = Date      ()
        # Note: below fields are used by roundup internally (obviously by the
        #       mail-gateway)
        , author                = Link      ("user", do_journal='no')
        , recipients            = Multilink ("user", do_journal='no')
        , summary               = String    ()
        , messageid             = String    ()
        , inreplyto             = String    ()
        )

    #
    # SECURITY SETTINGS
    #

    # Assign the access and edit permissions
    # to regular users now
    for cl in \
        'abo', 'abo_type', 'currency', 'msg', 'abo_price', 'query', 'address' :
        p = db.security.getPermission('View', cl)
        db.security.addPermissionToRole('User', p)
        p = db.security.getPermission('Edit', cl)
        db.security.addPermissionToRole('User', p)

    # Access permissions for the other classes for regular users
#    for cl in 'id_type' , 'artefact', 'department', 'product_type' :
#        p = db.security.getPermission('View', cl)
#        db.security.addPermissionToRole('User', p)

    # Maybe at some point in time we may want a different role for
    # administration of artefacts etc.

    # and give the regular users access to the web and email interface
    p = db.security.getPermission('Web Access')
    db.security.addPermissionToRole('User', p)
    p = db.security.getPermission('Email Access')
    db.security.addPermissionToRole('User', p)

    # May users view other user information? Comment these lines out
    # if you don't want them to
    p = db.security.getPermission('View', 'user')
    db.security.addPermissionToRole('User', p)

    # Assign the appropriate permissions to the anonymous user's Anonymous
    # Role. Choices here are:
    # - Allow anonymous users to register through the web
    # p = db.security.getPermission('Web Registration')
    # db.security.addPermissionToRole('Anonymous', p)
    # - Allow anonymous (new) users to register through the email gateway
    # p = db.security.getPermission('Email Registration')
    # db.security.addPermissionToRole('Anonymous', p)
    # - Allow anonymous users access to the "issue" class of data
    #   Note: this also grants access to related information like files,
    #         messages, statuses etc that are linked to issues
    for cl in ('user',) :
        p = db.security.getPermission('View', cl)
        db.security.addPermissionToRole('Anonymous', p)
    # Dont
    # - Allow anonymous users access to edit the "issue" class of data
    #   Note: this also grants access to create related information like
    #         files and messages etc that are linked to issues
    #p = db.security.getPermission('Edit', 'issue')
    #db.security.addPermissionToRole('Anonymous', p)

    # oh, g'wan, let anonymous access the web interface too
    # p = db.security.getPermission('Web Access')
    # db.security.addPermissionToRole('Anonymous', p)

    import detectors
    detectors.init(db)

    # schema is set up - run any post-initialisation
    db.post_init()
    return db
 
def init(adminpw): 
    ''' as from the roundupdb method initDB 
 
    Open the new database, and add new nodes - used for initialisation. You
    can edit this before running the "roundup-admin initialise" command to
    change the initial database entries.
    ''' 
    dbdir = os.path.join(config.DATABASE, 'files')
    if not os.path.isdir(dbdir):
        os.makedirs(dbdir)

    db = open("admin")
    db.clear()

    #
    # INITIAL VALUES
    #


    # create the two default users
    user = db.getclass('user')
    user.create \
        ( username="admin"
        , password=adminpw
        , address=config.ADMIN_EMAIL
        , roles='Admin'
        )
    user.create (username="anonymous", roles='Anonymous')

    # add any additional database create steps here - but only if you
    # haven't initialised the database with the admin "initialise" command

    currency = db.getclass ('currency')
    currency.create (name = 'CHF', description = 'Schweizer Franken')
    currency.create (name = 'EUR', description = 'Euro')
    currency.create (name = 'GBP', description = 'Britische Pfund')
    currency.create (name = 'USD', description = 'US-Dollar')

    abo_type = db.getclass ('abo_type')
    abo_type.create \
        ( name        = 'ZFW12norm'
        , description = uni ('Jahresabo Zeit-Fragen')
        , order       = 1
        )
    abo_type.create \
        ( name        = 'ZFW06norm'
        , description = uni ('Halbjahresabo Zeit-Fragen')
        , order       = 2
        )
    abo_type.create \
        ( name        = 'ZFW12gift'
        , description = uni ('Geschenkabo Zeit-Fragen')
        , order       = 3
        )
    abo_type.create \
        ( name        = 'CCM12norm'
        , description = uni ('Subscription Current Concerns')
        , order       = 4
        )
    abo_type.create \
        ( name        = 'HDM12norm'
        , description = uni ('abonnement Horizons et débats')
        , order       = 5
        )
    abo_type.create \
        ( name        = 'ZFM12norm'
        , description = uni ('Jahresabo Zeit-Fragen Monatsausgabe')
        , order       = 6
        )
    abo_type.create \
        ( name        = 'ZFM12gift'
        , description = uni ('Geschenkabo Zeit-Fragen Monatsausgabe')
        , order       = 7
        )
    abo_type.create \
        ( name        = 'ZFM12spon'
        , description = uni ('Förderabo Zeit-Fragen Monatsausgabe')
        , order       = 8
        )
    abo_type.create \
        ( name        = 'ZFW12free'
        , description = uni ('Gratisabo Zeit-Fragen')
        , order       = 9
        )
    abo_type.create \
        ( name        = 'ZFW12spec'
        , description = uni ('Spezialabo Zeit-Fragen')
        , order       = 10
        )
    abo_type.create \
        ( name        = 'CCM12gift'
        , description = uni ('Gift subscription Current Concerns')
        , order       = 11
        )
    abo_type.create \
        ( name        = 'CCM12free'
        , description = uni ('Free subscription Current Concerns')
        , order       = 12
        )
    abo_type.create \
        ( name        = 'HDM12gift'
        , description = uni ('abonnement-cadeau Horizons et débats')
        , order       = 13
        )
    abo_type.create \
        ( name        = 'ZFW12pate'
        , description = uni ('Patenschaftsabo Zeit-Fragen')
        , order       = 14
        )
    abo_type.create \
        ( name        = 'ZFW06gift'
        , description = uni ('Halbjahres-Geschenkabo Zeit-Fragen')
        , order       = 15
        )
    abo_type.create \
        ( name        = 'ZFW06spec'
        , description = uni ('Halbjahres-Spezialabo Zeit-Fragen')
        , order       = 16
        )

    valid = db.getclass ('valid')
    valid.create \
        ( name = uni ('gültig')
        , description = uni ('Gültige Adresse')
        )

    db.commit()

# vim: set filetype=python ts=4 sw=4 et si
