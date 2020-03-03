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


from roundup.cgi.TranslationService import get_translation
from roundup.date                   import Date
from roundup.exceptions             import Reject

import common
import rup_utils
import user_dynamic
try :
    import ldap_sync
except ImportError :
    ldap_sync = None

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
    """ Get all stati with 'timetracking_allowed' set it property exists
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
        valid = db.user_status.lookup ('valid')
        if 'status' not in new_values :
            new_values ['status'] = valid
        if not is_valid_user_status (db, new_values) :
            return
        status = new_values ['status']
    common.require_attributes \
        ( _
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

def audit_user_fields(db, cl, nodeid, new_values):
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

def update_userlist_html (db, cl, nodeid, old_values) :
    """newly create user_list.html macro page
    """
    changed    = False
    for i in 'username', 'status', 'roles' :
        if  (  not old_values
            or i not in old_values
            or old_values [i] != cl.get (nodeid, i)
            ) :
            changed = True
    if not changed :
        return
    rup_utils.update_userlist_html (db)
# end def update_userlist_html

def check_retire (db, cl, nodeid, old_values) :
    if db.getuid () != '1' :
        raise Reject, _ ("Not allowed to retire a user")
# end def check_retire

def obsolete_action (db, cl, nodeid, new_values) :
    obsolete = db.user_status.lookup ('obsolete')
    status   = new_values.get ('status', cl.get (nodeid, 'status'))
    if status == obsolete :
        new_values ['roles'] = ''
# end def obsolete_action

def sync_to_ldap (db, cl, nodeid, old_values) :
    user = cl.getnode (nodeid)
    ld   = ldap_sync.LDAP_Roundup_Sync (db, verbose = 0)
    if user.status not in ld.status_sync :
        return
    # Don't sync obsolete users back to ldap
    if user.status == ld.status_obsolete :
        return
    ld.sync_user_to_ldap (user.username)
# end def sync_to_ldap

def sync_to_ldap_ud (db, cl, nodeid, old_values) :
    ud = cl.getnode (nodeid)
    props = ('sap_cc', 'department', 'org_location')
    for p in props :
        if p in old_values and old_values [p] != getattr (ud, p, '-1') :
            break
    else :
        # Nothing to do, none of the props changed
        return
    sync_to_ldap (db, db.user, ud.user, {})
# end def sync_to_ldap_ud

def check_pictures (db, cl, nodeid, new_values) :
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
            (_, cl, nodeid, ldap_group = new_values ['ldap_group'])
# end def check_user_status

def deny_system_user (db, cl, nodeid, new_values) :
    """ Deny user creation by system users
    """
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
    if not _domain_user_role_check (db) :
        return
    uid = db.getuid ()
    # Find entries in domain_permission
    dpids = db.domain_permission.filter (None, dict (users = uid))
    if not dpids :
        raise Reject (_ ("No permission to edit/create users with any domain"))
    ad_domain = new_values.get ('ad_domain', None)
    if not ad_domain and nodeid :
        ad_domain = cl.get (nodeid, 'ad_domain')
    if ad_domain or nodeid :
        for d in dpids :
            dp = db.domain_permission.getnode (d)
            if dp.ad_domain == ad_domain :
                break
        else :
            raise Reject \
                (_ ('No permission for user with AD-Domain: "%s"' % ad_domain))
    else :
        if len (dpids) == 1 :
            dp = db.domain_permission.getnode (dpids [0])
            ad_domain = dp.ad_domain
        else :
            raise Reject (_ ("AD-Domain must be specified"))
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
        for user_dynamic and user_contact classes.
    """
    if not _domain_user_role_check (db) :
        return
    uid = db.getuid ()
    # Find entries in domain_permission
    dpids = db.domain_permission.filter (None, dict (users = uid))
    if not dpids :
        raise Reject (_ ("No permission to edit/create users with any domain"))
    uid = new_values.get ('user', None)
    if nodeid and not uid :
        uid = cl.get (nodeid, 'user')
    if not uid :
        classname = _ (cl.classname)
        raise Reject \
            (_ ("No permission to edit/create %(classname)s") % locals ())
    ad_domain =  db.user.get (uid, 'ad_domain')
    for d in dpids :
        dp = db.domain_permission.getnode (d)
        if dp.ad_domain == ad_domain :
            break
    else :
        raise Reject \
            (_ ('No permission for user with AD-Domain: "%s"' % ad_domain))
# end def domain_user_check

def fix_domain_username (db, cl, nodeid, new_values) :
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

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.user.audit ("set",    audit_user_fields)
    db.user.audit ("create", new_user)
    db.user.react ("create", update_userlist_html)
    if 'external_company' in db.classes :
        db.user.audit ("create", check_ext_company)
        db.user.audit ("set",    check_ext_company)
    db.user.react ("set",    update_userlist_html)
    db.user.audit ("retire", check_retire)
    db.user.audit ("set",    obsolete_action)
    db.user.audit ("set",    check_pictures)
    # ldap sync only on set not create (!)
    if ldap_sync and ldap_sync.check_ldap_config (db) :
        db.user.react ("set", sync_to_ldap, priority = 200)
        if 'user_dynamic' in db.classes :
            db.user_dynamic.react ("set", sync_to_ldap_ud, priority = 200)
    if 'user_status' in db.classes :
        db.user_status.audit ("create", check_user_status)
        db.user_status.audit ("set",    check_user_status)
        db.user.audit        ("create", deny_system_user)
    if 'domain_permission' in db.classes :
        db.user.audit ("create", domain_user_edit)
        db.user.audit ("set",    domain_user_edit)
        db.user.audit ("create", fix_domain_username)
        db.user.audit ("set",    fix_domain_username)
    if 'user_dynamic' in db.classes :
        db.user_dynamic.audit ("create", domain_user_check)
        db.user_dynamic.audit ("set",    domain_user_check)
    if 'user_contact' in db.classes :
        db.user_contact.audit ("create", domain_user_check)
        db.user_contact.audit ("set",    domain_user_check)
