#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-11 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#++
# Name
#    user_contact
#
# Purpose
#    Schema definitions for optional user_contact

from schemacfg import schemadef

def init \
    ( db
    , Address_Class
    , Contact_Class
    , Contact_Type_Class
    , Boolean
    , Number
    , Link
    , Multilink
    , ** kw
    ) :
    export   = {}

    contact = Contact_Class \
        ( db, ''"user_contact"
        , user                = Link      ('user',    do_journal = "no")
        , contact_type        = Link      ("uc_type", do_journal = "no")
        , order               = Number    ()
        , visible             = Boolean   ()
        )
    uc_type = Contact_Type_Class \
        (db, ''"uc_type"
        , visible             = Boolean   ()
        # Sync to user address/alternate_addresses if this is set
        , is_email            = Boolean   ()
        )

    class User_Class (kw ['User_Class']) :
        """ add contacts to user class
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( contacts               = Multilink ("user_contact")
                )
            kw ['User_Class'].__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Class
    export ['User_Class'] = User_Class

    return export
# end def init

def security (db, ** kw) :
    user_roles = ["HR", "Office"]
    if 'it' in db.security.role :
        user_roles.append ("IT")
    classes    = \
        ( ("uc_type",      ("User",),        ("HR", "Office"))
        , ("user_contact", ("HR", "Office"), ())
        )
    prop_perms = \
        [ ( "user",         "View", ["User", "HR", "Office"]
          , ("contacts",)
          )
        ]
    if 'it' in db.security.role :
        p = db.security.addPermission \
            ( name        = 'Create'
            , klass       = 'user_contact'
            , description = 'Create'
            )
        db.security.addPermissionToRole ('IT', p)
    schemadef.register_class_permissions (db, classes, prop_perms)
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'user_contact'
        , description = 'Search'
        )
    db.security.addPermissionToRole ('User', p)

    def contact_visible (db, userid, itemid) :
        """User is allowed to view contact if he's the owner of the contact
           or the contact is marked visible
        """
        if not itemid or itemid < 1 :
            return False
        c = db.user_contact.getnode (itemid)
        if userid == c.user :
            return True
        return c.visible
    # end def contact_visible

    def contact_visible_editable (db, userid, itemid) :
        """User is allowed to edit if he's the owner of the contact
        """
        if not itemid or itemid < 1 :
            return False
        c = db.user_contact.getnode (itemid)
        if userid == c.user :
            return True
        return False
    # end def contact_visible_editable

    fixdoc = schemadef.security_doc_from_docstring
    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'user_contact'
        , check       = contact_visible
        , description = fixdoc (contact_visible.__doc__)
        )
    db.security.addPermissionToRole ('User', p)

    p = db.security.addPermission \
        ( name        = 'Edit'
        , klass       = 'user_contact'
        , check       = contact_visible_editable
        , description = fixdoc (contact_visible_editable.__doc__)
        , properties  = ('visible',)
        )
    db.security.addPermissionToRole ('User', p)

# end def security

