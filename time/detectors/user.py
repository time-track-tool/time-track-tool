#! /usr/bin/python
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


from roundup.cgi.TranslationService import get_translation
from roundup.date                   import Date
from roundup.exceptions             import Reject

import common
import rup_utils
from user_dynamic                   import get_user_dynamic

def common_user_checks (db, cl, nodeid, new_values) :
    ''' Make sure user properties are valid.
        - email address has no spaces in it
        - roles specified exist
    '''
    if 'org_location' in cl.properties :
        olo = new_values.get ('org_location') or cl.get (nodeid, 'org_location')
        if not olo :
            dyn = get_user_dynamic (db, nodeid, Date ('.'))
            if dyn :
                olo = new_values ['org_location'] = dyn.org_location
                new_values ['department']         = dyn.department
    if new_values.has_key('address') and ' ' in new_values['address'] :
        raise ValueError, 'Email address must not contain spaces'
    if new_values.has_key('roles') :
        roles = new_values ['roles']
        if roles :
            roles = roles.strip ()
        if roles :
            roles = [x.lower().strip() for x in roles.split(',')]
            for rolename in roles:
                if not db.security.role.has_key (rolename):
                    raise ValueError, 'Role "%s" does not exist' % rolename
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
    for a in 'uid', 'nickname' :
        if a in new_values :
            v = new_values [a]
            common.check_unique (_, cl, nodeid, ** {a : v})
            if a == 'nickname' :
                common.check_unique (_, cl, nodeid, username = v)
    if 'nickname' in cl.properties and 'username' in new_values :
        common.check_unique (_, cl, nodeid, nickname = new_values ['username'])
    if 'uid' in new_values and new_values ['uid'] :
        if not olo :
            raise Reject, _("%s specified for user without %s") \
                % (_('uid'), _('org_location'))
        uid     = new_values ['uid']
        uidname = _ ('uid')
        id  = db.org_location.get (olo, 'smb_domain')
        if id :
            sd  = db.smb_domain.getnode (id)
            if not common.uid_or_gid_in_range (uid, sd.uid_range) :
                raise Reject, _("Invalid %(uidname)s: %(uid)s") % locals ()
            db.smb_domain.set (sd.id, last_uid = max (uid, sd.last_uid))
        else :
            raise Reject, _ \
                ("%(uidname)s specified but no samba domain configured")
# end def common_user_checks

def create_dynuser (db, cl, nodeid, new_values) :
    u = db.user.getnode (nodeid)
    s = None
    if 'user_status' in db.classes :
	s = db.user_status.lookup ('valid')
    if nodeid > 2 and (not s or u.status == s) :
	db.user_dynamic.create \
	    ( user         = nodeid
	    , valid_from   = Date ('.')
	    , org_location = cl.get (nodeid, 'org_location')
	    , department   = cl.get (nodeid, 'department')
	    )
# end def create_dynuser

def new_user (db, cl, nodeid, new_values) :
    # No checks for special accounts:
    if new_values.get ('username', None) in ['admin', 'anonymous'] :
        return
    # status set to a value different from valid: no checks
    if 'user_status' in db.classes :
        valid = db.user_status.lookup ('valid')
        if new_values.get ('status', valid) != valid :
            return
        if 'status' not in new_values :
            new_values ['status'] = valid
        status = new_values ['status']
    common.require_attributes \
        ( _
        , cl
        , nodeid
        , new_values
        , 'firstname'
        , 'lastname'
        , 'org_location'
        , 'department'
        , 'username'
        )
    if 'tt_lines' in cl.properties and 'tt_lines' not in new_values :
        new_values ['tt_lines'] = 1

    id = nodeid
    sd = None
    if 'nickname' in cl.properties :
        nickname = new_values ['nickname']
    if 'firstname' in cl.properties :
        fn    = new_values ['firstname']
        ln    = new_values ['lastname']
        lfn   = common.tolower_ascii (fn)
        lln   = common.tolower_ascii (ln)
        if  ('nickname' not in new_values and status == valid) :
            nick = common.new_nickname (_, cl, nodeid, lfn, lln)
            if nick :
                new_values ['nickname'] = nick
                nickname = new_values ['nickname']
            else :
                nickname = None
    if 'org_location' in db.classes :
        olo   = new_values ['org_location']
        org        = db.org_location.get   (olo, 'organisation')
        maildomain = db.organisation.get   (org, 'mail_domain')
        if 'smb_domain' in db.classes :
            id = db.org_location.get (olo, 'smb_domain')
            if id :
                sd = db.smb_domain.getnode (id)

    username   = new_values ['username']
    # defaults:
    if new_values ['status'] == valid :
        if 'contacts' in cl.properties :
            try :
                email = db.uc_type.lookup ('Email')
            except KeyError :
                email = None
            contacts = []
            c = db.user_contact.create \
                ( contact      = '@'.join (('.'.join ((lfn, lln)), maildomain))
                , contact_type = email
                , order        = 1
                )
            contacts.append (c)
            for n, i in enumerate ((nickname, username)) :
                if not i :
                    continue
                c = db.user_contact.create \
                    ( contact      = '@'.join ((i, maildomain))
                    , contact_type = email
                    , order        = 2 + n
                    )
                contacts.append (c)
            if 'contacts' not in new_values :
                new_values ['contacts'] = []
            new_values ['contacts'].extend (contacts)
        elif 'nickname' in cl.properties :
            if 'address' not in new_values :
                new_values ['address'] = \
                    '@'.join (('.'.join ((lfn, lln)), maildomain))
            if 'alternate_addresses' not in new_values :
                new_values ['alternate_addresses'] = '\n'.join \
                    ('@'.join ((i, maildomain))
                     for i in (nickname, username) if i
                    )
        if 'lunch_duration' in cl.properties :
            if 'lunch_duration' not in new_values :
                new_values ['lunch_duration'] = .5
            if 'lunch_start'    not in new_values :
                new_values ['lunch_start'] = '12:00'
        if sd and 'uid' in cl.properties and 'uid' not in new_values :
            new_values ['uid'] = common.next_uid_or_gid \
                (sd.last_uid, sd.uid_range)
            uid = new_values ['uid']
            if 'group' not in new_values :
                new_values ['group'] = db.group.create \
                    ( name         = username
                    , gid          = uid
                    , org_location = olo
                    )
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
    if 'status' in cl.properties :
        status = new_values.get ('status', cl.get (nodeid, 'status'))
        if status == db.user_status.lookup ('valid') :
            for n in \
                ( 'org_location'
                , 'department'
                ) :
                if n in new_values and new_values [n] is None :
                    raise Reject, "%(attr)s may not be undefined" \
                        % {'attr' : _ (n)}
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
    raise Reject, _ ("Not allowed to retire a user")
# end def check_retire

def obsolete_action (db, cl, nodeid, new_values) :
    obsolete = db.user_status.lookup ('obsolete')
    status   = new_values.get ('status', None)
    if status == obsolete :
        new_values ['roles'] = ''
# end def obsolete_action

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    # fire before changes are made
    db.user.audit("set"   , audit_user_fields)
    db.user.audit("create", new_user)
    db.user.react("create", update_userlist_html)
    if 'user_dynamic' in db.classes :
        db.user.react("create", create_dynuser)
    db.user.react("set"   , update_userlist_html)
    db.user.audit("retire", check_retire)
    db.user.audit("set"   , obsolete_action)
