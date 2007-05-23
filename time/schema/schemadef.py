# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
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
# Name
#    schemadef
#
# Purpose
#    Common routines for roundup schema definition
#--
#

import re
from rsclib.autosuper import autosuper

# Common routines for registration of roles classes and permissions
def register_roles (db, roles) :
    """Loop over given roles and register them -- each role consists of
       a two-element sequence with rolename and description.
    """
    for name, desc in roles :
        if name.lower () not in db.security.role :
            db.security.addRole (name = name, description = desc)
# end def register_roles

def register_class_permissions (db, class_perms, prop_perms) :
    """Register permissions for classes. Two sequences are expected:
       - class_perms contains sequences with the class, a list of roles
         that have permission to view the class, and a list of roles
         that may edit (Edit, Create) the class.
       - prop_perms contains a sequence with the following items: the
         class for which the permissions apply, the permission (one of
         "Edit", "Create", "View"), a sequence of roles, a sequence of
         properties of the given class for which the permissions apply.
    """
    for cl, view_list, edit_list in class_perms :
        for viewer in view_list :
            db.security.addPermissionToRole (viewer, 'View', cl)
        for editor in edit_list :
            db.security.addPermissionToRole (editor, 'Edit',   cl)
            db.security.addPermissionToRole (editor, 'Create', cl)
    for cl, perm, roles, props in prop_perms :
        p = db.security.addPermission \
            ( name        = perm
            , klass       = cl
            , description = ''"User is allowed %(perm)s on" % locals ()
            , properties  = props
            )
        for r in roles :
            db.security.addPermissionToRole (r, p)
# end def register_class_permissions

def own_user_record (db, userid, itemid) :
    """Determine whether the userid matches the item being accessed"""
    return userid == itemid
# end def own_user_record

whitespace = re.compile ('(\s+)')

def security_doc_from_docstring (doc) :
    """ Take given docstring (from security function) and use first
        paragraph (up to empty line) for security doc.
    """
    d = doc.split ('\n\n', 1) [0]
    d = whitespace.sub (' ', d)
    return d.strip ().strip ('.')
# end def security_doc_from_docstring

class Importer (object) :
    def __init__ (self, globals, schemas) :
        self.modules = {}
        self.globals = globals
        self.schemas = schemas
        Class        = globals ['Class']
        FileClass    = globals ['FileClass']
        Date         = globals ['Date']
        Multilink    = globals ['Multilink']
        Link         = globals ['Link']
        String       = globals ['String']

        class Ext_Mixin (autosuper) :
            """ create a class with some default attributes
                Note: inheritance methodology stolen from
                roundup/backends/back_anydbm.py's IssueClass ;-)
            """

            def __init__ (self, db, properties) :
                for k, v in self.default_properties.iteritems () :
                    properties.setdefault (k, v)
            # end def __init__

            def update_properties (self, ** properties) :
                """ We expect this method to be called *after* having
                    initialised all objects of derived classes. So we may
                    already have an initialised self.default_properties and
                    we only update those properties that are not already
                    present (it's more efficient to update the properties
                    parameter with the already existing default_properties).
                """
                props = getattr (self, 'default_properties', {})
                properties.update       (props)
                self.default_properties = properties
            # end def update_properties
        # end class Ext_Mixin

        class Ext_Class (Class, Ext_Mixin) :
            def __init__ (self, db, classname, ** properties) :
                Ext_Mixin.__init__ (self, db, properties)
                Class.__init__     (self, db, classname, ** properties)
            # end def __init__
        # end class Ext_Class

        class Min_Issue_Class (Ext_Class) :
            def __init__ (self, db, classname, ** properties) :
                self.update_properties \
                    ( messages             = Multilink ("msg")
                    , files                = Multilink ("file")
                    )
                self.__super.__init__ (db, classname, ** properties)
            # end def __init__
        # end class Min_Issue_Class

        class Nosy_Issue_Class (Min_Issue_Class) :
            def __init__ (self, db, classname, ** properties) :
                self.update_properties \
                    (nosy = Multilink ("user", do_journal = "no"))
                self.__super.__init__ (db, classname, ** properties)
            # end def __init__
        # end class Min_Issue_Class

        class Msg_Class (FileClass, Ext_Mixin) :
            def __init__ (self, db, classname, ** properties) :
                self.update_properties \
                    ( date                 = Date      ()
                    , files                = Multilink ("file")
                    # Note: fields below are used by roundup internally
                    # (obviously by the mail-gateway)
                    , author               = Link      ("user", do_journal='no')
                    , recipients           = Multilink ("user", do_journal='no')
                    , summary              = String    (indexme = 'no')
                    , messageid            = String    (indexme = 'no')
                    , inreplyto            = String    (indexme = 'no')
                    , content              = String    (indexme = 'no')
                    )
                Ext_Mixin.__init__ (self, db, properties)
                FileClass.__init__ (self, db, classname, ** properties)
            # end def __init__
        # end class Msg_Class

        globals ['Ext_Class']        = Ext_Class
        globals ['Msg_Class']        = Msg_Class
        globals ['Ext_Mixin']        = Ext_Mixin
        globals ['Min_Issue_Class']  = Min_Issue_Class
        globals ['Nosy_Issue_Class'] = Nosy_Issue_Class

        for s in schemas :
            m = __import__ (s)
            globals [s] = m
            if hasattr (m, 'init') :
                v = m.init (** globals)
                if v :
                    globals.update (v)
            self.modules [s] = m
    # end def __init__

    def update_security (self) :
        for s in self.schemas :
            m = self.modules [s]
            if hasattr (m, 'security') :
                m.security (** self.globals)
    # end def update_security
# end class Importer
