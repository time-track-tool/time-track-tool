# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
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

def register_nosy_classes (db, nosy_classes) :
    for klass in nosy_classes :
        p = db.security.addPermission \
            ( name        = "Nosy"
            , klass       = klass
            , description = \
                "User may get nosy messages for %(klass)s" % locals ()
            )
        db.security.addPermissionToRole ("Nosy", p)
# end def register_nosy_classes

def register_confidentiality_check (db, cls, perms, * properties) :
    """ Register a check for confidentiality, allow access with perms if
        - confidential flag for item of cls is not set
        - user is in nosy list of item
    """
    klass = db.getclass (cls)
    def check_confidential (db, userid, itemid) :
        if not itemid :
            return True
        item = klass.getnode (itemid)
        try :
            if not item.confidential :
                return True
        except IndexError :
            return False
        if userid in item.nosy :
            return True
        return False
    # end def check_confidential
    for perm in perms :
        params = dict \
            ( name        = perm
            , klass       = cls
            , check       = check_confidential
            , description = \
                ''"User is allowed %(perm)s on %(cls)s if %(cls)s is "
                "non-confidential or user is on nosy list" % locals ()
            )
        if properties :
            params ['properties'] = properties
        p = db.security.addPermission (** params)
        db.security.addPermissionToRole ('User', p)
# end register_confidentiality_check

def register_permission_by_link (db, role, perm, linkclass, * classprops) :
    """ Install permission check methods for a given linkclass (e.g.
        msg, file) linked by other classes (e.g. issue) from a
        Multilink. The parameter classprops is a list of 2-tuple of
        classname and property name.
    """
    if linkclass not in db.classes :
        return
    classprops = [(c, p) for c, p in classprops
                  if c in db.classes and p in db.classes [c].getprops ()
                 ]
    def is_linked (db, uid, itemid) :
        if not itemid :
            return False
        for cls, prop in classprops :
            if cls not in db.classes :
                continue
            ids = db.getclass (cls).filter (None, {prop : itemid})
            for id in ids :
                if db.security.hasPermission \
                    (perm, uid, cls, itemid = id, property = prop) :
                    return True
        return False
    # end def is_linked
    p = db.security.addPermission \
        ( name        = perm
        , klass       = linkclass
        , check       = is_linked
        , description = \
            ''"User is allowed %(perm)s on %(linkclass)s"
            " if %(linkclass)s is linked from an item with %(perm)s"
            " permission" % locals ()
        )
    db.security.addPermissionToRole (role, p)
# end def register_permission_by_link

def own_user_record (db, userid, itemid) :
    """Determine whether the userid matches the item being accessed"""
    return userid == itemid
# end def own_user_record

def add_search_permission (db, klass, role, properties = None) :
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = klass
        , description = "search %s" % klass
        , properties  = properties
        )
    db.security.addPermissionToRole (role, p)
# end add_search_permission

def allow_user_details (db, role, permission, *additional_props) :
    """ Allow editing some user details -- depending on the properties
        the user class has
    """
    default_props = \
        [ 'csv_delimiter'
        , 'lunch_duration'
        , 'lunch_start'
        , 'password'
        , 'queries'
        , 'realname'
        , 'room'
        , 'subst_active'
        , 'substitute'
        , 'timezone'
        , 'title'
        , 'tt_lines'
        ]
    props = []
    allprops = dict.fromkeys (default_props)
    allprops.update (dict.fromkeys (additional_props))
    for p in sorted (allprops.iterkeys ()) :
        if p in db.user.properties :
            props.append (p)
    p = db.security.addPermission \
        ( name        = permission
        , klass       = 'user'
        , check       = own_user_record
        , description = \
            "User is allowed to %s (some of) their own user details"
            % permission.lower ()
        , properties  = tuple (props)
        )
    db.security.addPermissionToRole(role, p)
# end def allow_user_details

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
        IssueClass   = globals ['IssueClass']
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

        class Min_Issue_Class (Ext_Class, IssueClass) :
            """ Minimal issue class with messages and files.
            
                Note that we inherit from IssueClass for handling of
                nosy messages, message sending (in reactors) etc., *not*
                for the attributes of IssueClass (that's why we don't
                call the constructor).
            """
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
        # end class Nosy_Issue_Class

        class Full_Issue_Class (Nosy_Issue_Class) :
            def __init__ (self, db, classname, ** properties) :
                self.update_properties \
                    ( title       = String    (indexme = "yes")
                    , responsible = Link      ("user")
                    )
                self.__super.__init__ (db, classname, ** properties)
            # end def __init__
        # end class Full_Issue_Class

        class Superseder_Issue_Class (Full_Issue_Class) :
            def __init__ (self, db, classname, ** properties) :
                self.update_properties \
                    (superseder  = Multilink (classname))
                self.__super.__init__ (db, classname, ** properties)
            # end def __init__
        # end class Superseder_Issue_Class

        Optional_Doc_Issue_Class = Superseder_Issue_Class

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
                    , content              = String    (indexme = 'yes')
                    )
                Ext_Mixin.__init__ (self, db, properties)
                FileClass.__init__ (self, db, classname, ** properties)
            # end def __init__
        # end class Msg_Class

        globals ['Ext_Class']                = Ext_Class
        globals ['Msg_Class']                = Msg_Class
        globals ['Ext_Mixin']                = Ext_Mixin
        globals ['Min_Issue_Class']          = Min_Issue_Class
        globals ['Nosy_Issue_Class']         = Nosy_Issue_Class
        globals ['Full_Issue_Class']         = Full_Issue_Class
        globals ['Superseder_Issue_Class']   = Superseder_Issue_Class
        globals ['Optional_Doc_Issue_Class'] = Optional_Doc_Issue_Class

        for s in schemas :
            m = __import__ ('.'.join (('schemacfg', s)))
            m = getattr (m, s)
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
