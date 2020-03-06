# -*- coding: iso-8859-1 -*-
# Copyright (C) 2012-15 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#++
# Name
#    ldap
#
# Purpose
#    LDAP specific attributes used for syncing with LDAP.
#
#--
#

from schemacfg import schemadef

def init \
    ( db
    , String
    , Link
    , Multilink
    , Ext_Class
    , Class
    , ** kw
    ) :
    export = {}

    User_Status_Ancestor = kw.get ('User_Status_Class', Ext_Class)
    class User_Status_Class (User_Status_Ancestor) :
        """ Add some attrs for tracking ldap behaviour
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( ldap_group             = String    ()
                , roles                  = String    ()
                )
            User_Status_Ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Status_Class
    export.update (dict (User_Status_Class = User_Status_Class))

    User_Ancestor = kw.get ('User_Class', Ext_Class)
    class User_Class (User_Ancestor) :
        """ Add some attrs to user class: We need the active directory
            guid for matching users when syncing users with ldap.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( guid                   = String    ()
                , ad_domain              = String    ()
                )
            User_Ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Class
    export.update (dict (User_Class = User_Class))

    # add_properties specifies properties that may be edited although
    # normally restricted.
    domain_permission = Class \
        ( db
        , ''"domain_permission"
        , ad_domain       = String    ()
        , users           = Multilink ("user")
        , default_roles   = String    ()
        , timetracking_by = Link      ("user")
        , clearance_by    = Link      ("user")
        , status          = Link      ("user_status")
        )
    domain_permission.setkey ('ad_domain')

    return export
# end def init

def security (db, ** kw) :
    roles = \
        [ ("Dom-User-Edit-GTT", "Edit/Create users with specific AD domain")
        , ("Dom-User-Edit-HR",  "Edit users with specific AD domain")
        , ("Dom-User-Edit-Office",   "Edit users with specific AD domain")
        , ("Dom-User-Edit-Facility", "Edit users with specific AD domain")
        , ("IT", "IT-Department")
        ]
    schemadef.register_roles (db, roles)
    db.security.addPermissionToRole ('Dom-User-Edit-GTT', 'Create', 'user')
    # Editable user fields for the Domain-User-Edit roles
    user_props = \
        [ 'contacts'
        , 'csv_delimiter'
        , 'firstname'
        , 'hide_message_files'
        , 'job_description'
        , 'lastname'
        , 'lunch_duration'
        , 'lunch_start'
        , 'nickname'
        , 'pictures'
        , 'position'
        , 'room'
        , 'sex'
        , 'status'
        , 'subst_active'
        , 'substitute'
        , 'supervisor'
        , 'timezone'
        , 'title'
        , 'tt_lines'
        , 'scale_role'
        , 'scale_seniority'
        , 'vie_user'
	]
    user_props_hr  = user_props + ['clearance_by', 'roles', 'reduced_activity_list']
    user_props_gtt = user_props + ['username']
    user_props_office = ['contacts', 'position', 'room', 'title']
    user_props_facility = ['room']
    role_perms = \
        [ ("Dom-User-Edit-GTT",      user_props_gtt)
        , ("Dom-User-Edit-HR",       user_props_hr)
        , ("Dom-User-Edit-Office",   user_props_office)
        , ("Dom-User-Edit-Facility", user_props_facility)
        ]
    classes = \
        [ ( "domain_permission"
          , ["IT"]
          , ["IT"]
          )
        ]
    if 'user_contact' in db.classes :
        for role, x in role_perms [:3] :
            classes.append \
                ( ( "user_contact"
                  , []
                  , [role]
                  )
                )
            db.security.addPermissionToRole (role, 'Create', 'user_contact')
    if 'user_dynamic' in db.classes :
        for role in ("Dom-User-Edit-GTT", "Dom-User-Edit-HR") :
            classes.append \
                ( ( "user_dynamic"
                  , []
                  , [role]
                  )
                )
            db.security.addPermissionToRole (role, 'Create', 'user_dynamic')
    prop_perms = []
    schemadef.register_class_permissions (db, classes, prop_perms)
    fixdoc = schemadef.security_doc_from_docstring

    def domain_access_user (db, userid, itemid) :
        """ Users may view/edit user records for ad_domain for which they
            are in the domain_permission for the user.
        """
        dpids = db.domain_permission.filter (None, dict (users = userid))
        if not dpids :
            return False
        u = db.user.getnode (itemid)
        for dpid in dpids :
            dp = db.domain_permission.getnode (dpid)
            if dp.ad_domain == u.ad_domain :
                return True
        return False
    # end def domain_access_user

    for role, props in role_perms :
        for perm in 'Edit', 'View' :
            p = db.security.addPermission \
                ( name        = perm
                , klass       = 'user'
                , check       = domain_access_user
                , description = fixdoc (domain_access_user.__doc__)
                , properties  = props
                )
            db.security.addPermissionToRole (role, p)

    def domain_view_user_dynamic (db, userid, itemid) :
        """ Users may view user_dynamic records for ad_domain for which
            they are in the domain_permission for the user
        """
        dpids = db.domain_permission.filter (None, dict (users = userid))
        if not dpids :
            return False
        ud = db.user_dynamic.getnode (itemid)
        u  = db.user.getnode (ud.user)
        for dpid in dpids :
            dp = db.domain_permission.getnode (dpid)
            if dp.ad_domain == u.ad_domain :
                return True
        return False
    # end def domain_view_user_dynamic

    p = db.security.addPermission \
        ( name        = 'View'
        , klass       = 'user_dynamic'
        , check       = domain_view_user_dynamic
        , description = fixdoc (domain_view_user_dynamic.__doc__)
        )
    db.security.addPermissionToRole ('Dom-User-Edit-GTT', p)
    db.security.addPermissionToRole ('Dom-User-Edit-HR', p)
    p = db.security.addPermission \
        ( name        = 'Search'
        , klass       = 'user_dynamic'
        )
    db.security.addPermissionToRole ('Dom-User-Edit-GTT', p)
    db.security.addPermissionToRole ('Dom-User-Edit-HR', p)
# end def security
