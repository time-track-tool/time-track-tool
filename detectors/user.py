#! /usr/bin/python
# Copyright (C) 2006-19 Dr. Ralf Schlatterbeck Open Source Consulting.
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


from roundup.date                   import Date
from roundup.exceptions             import Reject
from domain_perm                    import check_domain_permission

import common
import user_dynamic

maxlen = dict \
    ( firstname = 64
    , lastname  = 64
    , nickname  = 6
    , address   = 256
    )

def common_user_checks (db, cl, nodeid, new_values) :
    ''' Make sure user properties are valid.
        - email address has no spaces in it
        - roles specified exist
    '''
    _ = db.i18n.gettext
    if  (   'address' in new_values
        and new_values ['address']
        and ' ' in new_values['address']
        ) :
        raise ValueError, 'Email address must not contain spaces'
    common.check_roles (db, cl, nodeid, new_values)
    # automatic setting of realname
    if 'firstname' in cl.properties :
        n = 'firstname'
        fn = new_values.get (n, None) or cl.get (nodeid, n) or ''
        n = 'lastname'
        ln = new_values.get (n, None) or cl.get (nodeid, n) or ''
        if  (  new_values.has_key ("firstname")
            or new_values.has_key ("lastname")
            ) :
            realname = " ".join ((fn, ln))
            new_values ["realname"] = realname
    if 'lunch_duration' in new_values :
        ld = new_values ['lunch_duration']
        if ld * 3600 % 900 :
            raise Reject, _ ("Times must be given in quarters of an hour")
        new_values ['lunch_duration'] = int (ld * 4) / 4.
        if ld > 8 :
            raise Reject, _ ("Lunchbreak of more than 8 hours? Sure?")
        if ld < .5 :
            raise Reject, _ ("Lunchbreak must be at least half an hour.")
    if 'lunch_start' in new_values :
        ls = new_values ['lunch_start']
        ls = Date (ls) # trigger date-spec error if this fails.
    if 'tt_lines' in new_values :
        ttl = new_values ['tt_lines']
        if ttl < 1 :
            new_values ['tt_lines'] = 1
        if ttl > 5 :
            new_values ['tt_lines'] = 5
    if 'supervisor' in new_values :
        common.check_loop \
            (_, cl, nodeid, 'supervisor', new_values ['supervisor'])
    # Allow nickname to be empty
    # Nick must be unique and must not collide with a username
    # This is checked in both directions
    if 'nickname' in new_values and new_values ['nickname'] :
        v = new_values ['nickname']
        common.check_unique (_, cl, nodeid, nickname = v)
        common.check_unique (_, cl, nodeid, username = v)
    if 'nickname' in cl.properties and 'username' in new_values :
        common.check_unique (_, cl, nodeid, nickname = new_values ['username'])
    for k in maxlen :
        if k in new_values :
            if new_values [k] is None :
                continue
            if len (new_values [k]) > maxlen [k] :
                fn = _ (k)
                l  = maxlen [k]
                raise Reject (_ ('%(fn)s too long: > %(l)s' % locals ()))
# end def common_user_checks

def is_valid_user_status (db, new_values) :
    """ Get all stati with 'timetracking_allowed' set if property exists
        Otherwise simply use 'valid' status
        If no user_status class exists, always return True
    """
    if 'user_dynamic' in db.classes and 'user_status' in db.classes :
        if 'status' not in new_values :
            return False
        status = new_values ['status']
        return user_dynamic.is_tt_user_status (db, status)
    return True
# end def is_valid_user_status

def new_user (db, cl, nodeid, new_values) :
    # No checks for special accounts:
    if new_values.get ('username', None) in ['admin', 'anonymous'] :
        return
    # status set to a value different from valid: no checks
    if 'user_status' in db.classes :
        try :
            valid = db.user_status.lookup ('valid')
        except KeyError :
            valid = db.user_status.filter (None, dict (name = 'valid')) [0]
        if 'status' not in new_values :
            new_values ['status'] = valid
    common.require_attributes \
        ( db.i18n.gettext
        , cl
        , nodeid
        , new_values
        , 'firstname'
        , 'lastname'
        , 'username'
        )
    if 'tt_lines' in cl.properties and 'tt_lines' not in new_values :
        new_values ['tt_lines'] = 1
    common_user_checks (db, cl, nodeid, new_values)
# end def new_user

def audit_user_fields (db, cl, nodeid, new_values):
    _ = db.i18n.gettext
    for n in \
        ( 'firstname'
        , 'lastname'
        , 'lunch_duration'
        , 'lunch_start'
        , 'shadow_inactive'
        , 'shadow_max'
        , 'shadow_min'
        , 'shadow_warning'
        , 'uid'
        ) :
        if n in new_values and new_values [n] is None and cl.get (nodeid, n) :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (n)}
    common_user_checks (db, cl, nodeid, new_values)
# end def audit_user_fields

def check_retire (db, cl, nodeid, old_values) :
    _ = db.i18n.gettext
    if db.getuid () != '1' :
        raise Reject, _ ("Not allowed to retire a user")
# end def check_retire

def obsolete_action (db, cl, nodeid, new_values) :
    obsolete = db.user_status.lookup ('obsolete')
    status   = new_values.get ('status', cl.get (nodeid, 'status'))
    if status == obsolete :
        if 'nickname' in cl.properties :
            new_values ['nickname'] = ''
        new_values ['roles'] = ''
# end def obsolete_action

def check_pictures (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    limit = common.Size_Limit (db, 'LIMIT_PICTURE_SIZE')
    if not limit :
        return
    pictures = new_values.get ('pictures')
    if not pictures :
        return
    p = list ( sorted ( pictures
                      , reverse = 1
                      , key = lambda x : db.file.get (x, 'activity')
                      )
             ) [0]
    pict = db.file.getnode (p)
    length = len (pict.content)
    if length > limit.limit :
        raise Reject, _ \
            ("Maximum picture size %(limit)s exceeded: %(length)s") % locals ()
# end def check_pictures

def check_ext_company (db, cl, nodeid, new_values) :
    try :
        st_ext = db.user_status.lookup ('external')
    except KeyError :
        st_ext = None
    if 'status' in new_values :
        if st_ext and new_values ['status'] == st_ext :
            roles = db.user_status.get (st_ext, 'roles')
            if not roles :
                roles = 'External,Nosy'
            new_values ['roles'] = roles
    st = new_values.get ('status')
    if not st and nodeid :
        st = cl.get (nodeid, 'status')
    if 'external_company' in new_values or 'status' in new_values :
        if st != st_ext :
            new_values ['external_company'] = None
# end def check_ext_company

def check_user_status (db, cl, nodeid, new_values) :
    if 'ldap_group' in new_values and new_values ['ldap_group'] :
        common.check_unique \
            ( db.i18n.gettext, cl, nodeid
            , ldap_group = new_values ['ldap_group']
            )
# end def check_user_status

def deny_system_user (db, cl, nodeid, new_values) :
    """ Deny user creation by system users
    """
    _ = db.i18n.gettext
    # admin *may* create users
    uid = db.getuid ()
    if int (uid) <= 1 :
        return
    system = db.user_status.lookup ('system')
    status = db.user.get (uid, 'status')
    if status == system :
        raise Reject, _ ("System users may not create users")
# end def deny_system_user

def _domain_user_role_check (db) :
    # Get role of user and check permission
    uid  = db.getuid ()
    # Allow admin user
    if uid == '1' :
        return False
    roles = ("Dom-User-Edit-GTT", "Dom-User-Edit-HR", "Dom-User-Edit-Office")
    if not common.user_has_role (db, uid, * roles) :
        return False
    return True
# end def _domain_user_role_check

def domain_user_edit (db, cl, nodeid, new_values) :
    """ If a user change/create happens and the user doing the
        modification has the 'Domain-User-Edit' role, we need to perform
        additional checks.
    """
    _ = db.i18n.gettext
    if not _domain_user_role_check (db) :
        return
    uid = db.getuid ()
    ad_domain = new_values.get ('ad_domain', None)
    if not ad_domain and nodeid :
        ad_domain = cl.get (nodeid, 'ad_domain')
    if not ad_domain :
        raise Reject (_ ("AD-Domain must be specified"))
    dp = check_domain_permission (db, uid, ad_domain)
    if not dp :
        raise Reject \
            (_ ('No permission for user with AD-Domain: "%s"' % ad_domain))
    perm = db.security.hasPermission
    # Force this to valid value
    if not nodeid or ad_domain in new_values :
        new_values ['ad_domain'] = ad_domain
    if  (   not nodeid or 'roles' in new_values
        and not perm ('Edit', uid, 'user', 'roles')
        ) :
        new_values ['roles'] = dp.default_roles
    if not nodeid or 'timetracking_by' in new_values :
        new_values ['timetracking_by'] = dp.timetracking_by
    if not nodeid and 'clearance_by' not in new_values :
        new_values ['clearance_by'] = dp.clearance_by
    if  (   'clearance_by' in new_values
        and not perm ('Edit', uid, 'user', 'clearance_by')
        ) :
        new_values ['clearance_by'] = dp.clearance_by
    obsolete = db.user_status.lookup ('obsolete')
    if not nodeid or 'status' in new_values :
        nstatus = new_values.get ('status', None)
        if (nstatus and nstatus != obsolete) or not nodeid :
            new_values ['status'] = dp.status
# end def domain_user_edit

def domain_user_check (db, cl, nodeid, new_values) :
    """ This checks for items that are editable if the linked user (in
        the property 'user') has the correct ad_domain. Currently used
        for user_dynamic user_contact classes. For user_contact we check
        this only on modify not on creation because user_contact items
        are first created without a user and later added to the user.
    """
    _ = db.i18n.gettext
    if not _domain_user_role_check (db) :
        return
    uid = new_values.get ('user', None)
    if nodeid and not uid :
        uid = cl.get (nodeid, 'user')
    # Allow creation of empty user
    if not uid :
        return
    ad_domain = db.user.get (uid, 'ad_domain')
    if not check_domain_permission (db, db.getuid (), ad_domain) :
        raise Reject \
            (_ ('No permission for user with AD-Domain: "%s"' % ad_domain))
# end def domain_user_check

def fix_domain_username (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    if 'username' not in new_values and 'ad_domain' not in new_values :
        return
    ad_domain = new_values.get ('ad_domain', None)
    username  = new_values.get ('username', None)
    if not username :
        username = cl.get (nodeid, 'username')
    if not ad_domain and nodeid :
        ad_domain = cl.get (nodeid, 'ad_domain')
    if not ad_domain :
        if username and '@' in username :
            raise Reject (_ ("No domain allowed for username"))
        return
    assert username
    if '@' in username :
        username = username.split ('@') [0]
    new_values ['username'] = '@'.join ((username, ad_domain))
# end def fix_domain_username

def default_reduced_activity_list (db, cl, nodeid, new_values) :
    """ This is the cut-off date where every new user should have the
        value set.
    """
    if 'reduced_activity_list' not in new_values :
        new_values ['reduced_activity_list'] = Date ('2020-04-01')
# end def default_reduced_activity_list

def check_room_on_restore (db, cl, nodeid, new_values) :
    """ If a user is restored (status set from obsolete to something
        other than obsolete) and has a retired room, set the room to
        None
    """
    if 'status' not in new_values :
        return
    user = cl.getnode (nodeid)
    ostatus  = user.status
    obsolete = db.user_status.lookup ('obsolete')
    if ostatus != obsolete or new_values ['status'] == obsolete :
        return
    room = new_values.get ('room', user.room)
    if room and db.room.is_retired (room) :
        new_values ['room'] = None
# end def check_room_on_restore

def check_dp_role (db, cl, nodeid, new_values) :
    """ We ensure that the given role is lowercase: The lookup will be
        performed using exact string match later, so the domain needs to
        be in a defined case. For all role-fields we check the role names
        given are valid.
    """
    if new_values.get ('roles_enabled', None) :
        common.check_roles (db, cl, nodeid, new_values, rname = 'roles_enabled')
        new_values ['roles_enabled'] = new_values ['roles_enabled'].lower ()
    if new_values.get ('default_roles', None) :
        common.check_roles (db, cl, nodeid, new_values, rname = 'default_roles')
# end def check_dp_role

def vie_backlink_check (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    if 'vie_user_bl_override' not in new_values :
        return
    # Not allowed on creation!
    if not nodeid and new_values ['vie_user_bl_override'] :
        raise Reject \
            (_ ("Not allowed on creation: %s") % _ ('vie_user_bl_override'))
    if not nodeid :
        return
    allowed_ids = cl.get (nodeid, 'vie_user_ml')
    allowed_ids.append (nodeid)
    blo = new_values ['vie_user_bl_override']
    if blo and blo not in allowed_ids :
        raise Reject \
            (_ ('"%s" must match own ID or one in "%s"')
            % (_ ('vie_user_bl_override'), _ ('vie_user_ml'))
            )
# end def vie_backlink_check

def business_responsible_check (db, cl, nodeid, new_values) :
    """ Check the field business_responsible
        Setting business_responsible for a user who has a
        vie_user_ml is not allowed. Likewise setting the
        business_responsible *to* a user who has a vie_user_ml is not
        allowed.
    """
    # Either not in new_values or changed to None
    if not new_values.get ('business_responsible', None) :
        return
    resp = cl.getnode (new_values ['business_responsible'])
    if resp.vie_user_ml :
        raise Reject ('Business responsible must be a source user')
    if nodeid :
        user = cl.getnode (nodeid)
        if user.vie_user_ml :
            raise Reject ('Business responsible must not be set for this user')
# end def business_responsible_check

def init (db) :
    db.user.audit ("set",    audit_user_fields)
    db.user.audit ("create", new_user)
    if 'external_company' in db.classes :
        db.user.audit ("create", check_ext_company)
        db.user.audit ("set",    check_ext_company)
    db.user.audit ("retire", check_retire)
    db.user.audit ("set",    obsolete_action)
    db.user.audit ("set",    check_pictures)
    if 'room' in db.user.properties :
        db.user.audit ("set",    check_room_on_restore)
    if 'user_status' in db.classes :
        db.user_status.audit ("create", check_user_status)
        db.user_status.audit ("set",    check_user_status)
        db.user.audit        ("create", deny_system_user)
    if 'domain_permission' in db.classes :
        db.user.audit ("create", domain_user_edit)
        db.user.audit ("set",    domain_user_edit)
        db.user.audit ("create", fix_domain_username)
        db.user.audit ("set",    fix_domain_username)
        db.domain_permission.audit ("set",    check_dp_role)
        db.domain_permission.audit ("create", check_dp_role)
    if 'user_dynamic' in db.classes :
        db.user_dynamic.audit ("create", domain_user_check)
        db.user_dynamic.audit ("set",    domain_user_check)
    if 'user_contact' in db.classes :
        db.user_contact.audit ("set",    domain_user_check)
    if 'reduced_activity_list' in db.user.properties :
        db.user.audit ("create", default_reduced_activity_list)
    if 'vie_user_bl_override' in db.user.properties :
        db.user.audit ("create", vie_backlink_check)
        db.user.audit ("set",    vie_backlink_check)
        db.user.audit ("create", business_responsible_check, priority = 150)
        db.user.audit ("set",    business_responsible_check, priority = 150)
