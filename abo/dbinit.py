#! /usr/bin/python
# Copyright (C) 2004 Ralf Schlatterbeck. All rights reserved
# Reichergasse 131, A-3411 Weidling. office@runtux.com
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

    abo_type = Class \
        ( db, "abo_type"
        , name                = String    ()
        , description         = String    ()
        )
    abo_type.setkey ("name")

    currency = Class \
        ( db, "currency"
        , name                = String    ()
        , description         = String    ()
        )
    currency.setkey ("name")

    abo_price = Class \
        ( db, "abo_price"
        , abotype             = Link      ('abo_type')
        , currency            = Link      ('currency')
        , amount              = Number    ()
        , name                = String    ()
        )

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
        , phone_home          = String    ()
        , phone_office        = String    ()
        , phone_mobile        = String    ()
        , fax                 = String    ()
        , salutation          = String    ()
        , messages            = Multilink ("msg")
        , email               = String    ()
        , abos                = Multilink ("abo")
        , payed_abos          = Multilink ("abo")
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
    user.create(username="admin", password=adminpw,
        address=config.ADMIN_EMAIL, roles='Admin')
    user.create(username="anonymous", roles='Anonymous')

    # add any additional database create steps here - but only if you
    # haven't initialised the database with the admin "initialise" command

    db.commit()

# vim: set filetype=python ts=4 sw=4 et si

#SHA: 3214e7d7760b31bdabc7afcb6a4a088e334ef782
