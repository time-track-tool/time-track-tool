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
#
#++
# Name
#    Roundup_Access classes
#
# Purpose
#    Classes encapsulating roundup objects. With access functions and
#    export to LDIF. All classes live in a Roundup_Access object.
#

import os
import sys
import ldif

from cStringIO        import StringIO
from roundup.date     import Date
from roundup          import instance
from roundup.hyperdb  import Link, Multilink

class Roundup_Access (object) :
    """ Wrapper class that gets a handle to the roundup instance and
        includes code and classes from there.
    """

    def __init__ (self, basedn, path, user = 'admin') :
        global ymd, get_user_dynamic
        self.tracker = instance.open (path)
        self.db      = self.tracker.open (user)
        self.basedn  = basedn
        sys.path.insert (1, os.path.join (path, 'lib'))
        from common       import ymd
        from user_dynamic import get_user_dynamic
        del sys.path [1]
        for rupname in self.db.getclasses () :
            classname = self._classname (rupname)
            if not hasattr (self, classname) :
                # create a derived class dynamically
                setattr (self, classname, type (classname, (self.Roundup,), {}))
            cls = getattr (self, classname)
            setattr (cls, 'db',     self.db)
            setattr (cls, 'cl',     self.db.getclass (rupname))
            setattr (cls, 'basedn', self.basedn)
            setattr (cls, 'master', self)
    # end def __init__

    def _classname (self, rupname) :
        return rupname [0].upper () + rupname [1:]
    # end def _classname

    def class_from_rupname (self, rupname) :
        return getattr (self, self._classname (rupname))
    # end def class_from_rupname

    class Roundup (object) :
        """
            Base class to encapsulate a roundup Class. With access functions
            for roundup and ldif export.
        """

        def __init__ (self, id) :
            self.node   = self.cl.getnode (id)
            self.id     = id
        # end def __init__

        def __getattr__ (self, name) :
            try :
                value = self.node [name]
            except KeyError, cause :
                raise AttributeError, "%s%s: %s" \
                    % (self.node.cl.classname, self.id, cause)
            prop = self.node.cl.properties [name]
            if prop.__class__ == Link :
                value = self.master.class_from_rupname (prop.classname) (value)
                setattr (self, name, value)
            elif prop.__class__ == Multilink :
                newval = []
                cls    = self.master.class_from_rupname (prop.classname)
                for v in value :
                    newvalue.append (cls (v))
                value = newvalue
            return value
        # end def __getattr__

        def as_ldif (self) :
            strio  = StringIO ()
            entry  = { 'objectClass' : self.object_class }
            writer = ldif.LDIFWriter (strio)
            for ldn, name in self.ldif_map :
                try :
                    attr = getattr (self, name)
                except AttributeError, cause :
                    attr = None
                if isinstance (attr, Date) :
                    attr = attr.timestamp ()
                if isinstance (attr, float) :
                    attr = long (attr)
                if isinstance (attr, list) :
                    entry [ldn] = attr
                elif attr is not None :
                    entry [ldn] = [str (attr)]
            writer.unparse (self.dn (), entry)
            return strio.getvalue ()
        # end def as_ldif

        zero       = 0
        endofepoch = 0x7FFFFFFF

    # end class Roundup

    class Alias (Roundup) :
        """
            Encapsulate the roundup alias class. Includes LDIF export.
        """

        ldif_map = \
            [ ('cn',                   'name')
            , ('mailLocalAddress',     'name')
            , ('description',          'description')
            #, ('mailHost',             'tttech.com')
            #, ('mailRoutingAddress',   'name@domino01.vie.at.tttech.ttt')
            ]

        object_class = \
            [ 'organizationalRole'
            , 'inetLocalMailRecipient'
            ]
        """
        dn =
        cn=root,ou=MailGroups,ou=vie,ou=at,ou=TTTech,o=ttt,dc=tttech,dc=com
        """

    # end class Alias

    class Group (Roundup) :
        """
            Encapsulate the roundup group class. Includes LDIF export.
        """

        ldif_map = \
            [ ('cn',                   'name')
            , ('description',          'description')
            , ('displayName',          'name')
            , ('gidNumber',            'gid')
            , ('memberUid',            'members')
            , ('sambaGroupType',       'samba_group_type')
            , ('sambaSID',             'sid')
            ]

        object_class = \
            [ 'posixGroup'
            , 'sambaGroupMapping'
            ]

        def _sid (self) :
            return ''.join \
                (( self.org_location.smb_domain.sid
                 , '-'
                 , str (int (self.gid * 2 + 1001))
                ))
        # end def _sid
        sid = property (_sid)

        samba_group_type = 2

        def dn (self) :
            op     = self.org_location.orgpath ()
            org_dn = ["ou=%s" % p for p in op [:-1]]
            org_dn.append ("o=%s" % op [-1])
            return "cn=%s,ou=Groups,%s,%s" \
                % (self.name, ','.join (org_dn), self.basedn)
        # end def dn

        def _members (self) :
            users = dict \
                ([(i, 1) for i in self.db.user.find (group = self.id)])
            aux = self.db.user.find (secondary_groups = self.id)
            if aux :
                users.update ([(i, 1) for i in aux])
            return [self.db.user.get (u, 'username') for u in users.iterkeys ()]
        # end def _members
        members = property (_members)

    # end class Group

    class User (Roundup) :
        """
            Encapsulate the roundup user class. Includes LDIF export.
        """

        ldif_map = \
            [ ('cn',                   'username')
            , ('sn',                   'realname')
            , ('telephoneNumber',      'phone')
            , ('description',          'realname')
            , ('displayName',          'realname')
            , ('initials',             'nickname')
            , ('mail',                 'address')
            , ('uid',                  'username')
            , ('uidNumber',            'uid')
            , ('gidNumber',            'gid')
            , ('homeDirectory',        'home_directory')
            , ('loginShell',           'login_shell')
            , ('gecos',                'gecos')
            , ('mailLocalAddress',     'mail_addresses')
            , ('sambaAcctFlags',       'samba_acct_flags')
            , ('sambaHomeDrive',       'samba_home_drive')
            , ('sambaHomePath',        'samba_home_path')
            , ('sambaKickoffTime',     'samba_kickoff_time')
            , ('sambaLMPassword',      'samba_lm_password')
            , ('sambaLogoffTime',      'endofepoch')
            , ('sambaLogonScript',     'samba_logon_script')
            , ('sambaLogonTime',       'zero')
            , ('sambaNTPassword',      'samba_nt_password')
            , ('sambaPrimaryGroupSID', 'group_sid')
            , ('sambaProfilePath',     'samba_profile_path')
            , ('sambaPwdCanChange',    'samba_pwd_can_change')
            , ('sambaPwdLastSet',      'samba_pwd_last_set')
            , ('sambaPwdMustChange',   'samba_pwd_must_change')
            , ('sambaSID',             'sid')
            , ('shadowExpire',         'shadow_expire')
            , ('shadowFlag',           'shadow_used')
            , ('shadowInactive',       'shadow_inactive')
            , ('shadowLastChange',     'shadow_last_change')
            , ('shadowMax',            'shadow_max')
            , ('shadowMin',            'shadow_min')
            , ('shadowWarning',        'shadow_warning')
            ]

        samba_acct_flags = '[U]'

        object_class = \
            [ 'top'
            , 'inetOrgPerson'
            , 'posixAccount'
            , 'inetLocalMailRecipient'
            , 'sambaSamAccount'
            , 'shadowAccount'
            ]

        def _gecos (self) :
            return ','.join ((self.realname, self.phone))
        # end def _gecos
        gecos = property (_gecos)

        def _gid (self) :
            return int (self.group.gid)
        # end def _gid
        gid = property (_gid)

        def _mail_addresses (self) :
            return [self.username, self.nickname]
        # end def _mail_addresses
        mail_addresses = property (_mail_addresses)

        def _sid (self) :
            return ''.join \
                (( self.user_dynamic.org_location.smb_domain.sid
                 , '-'
                 , str (int (self.uid * 2 + 1000))
                ))
        # end def _sid
        sid = property (_sid)

        def _group_sid (self) :
            return self.group.sid
        # end def _group_sid
        group_sid = property (_group_sid)

        _cache_ud = None

        def _user_dynamic (self) :
            if self._cache_ud : return self._cache_ud
            date = '.'
            dyn  = get_user_dynamic (self.db, self.id, date)
            if not dyn :
                raise AttributeError, "No valid dynamic user record for %s %s" \
                    % (self.username, date.pretty (ymd))
            self._cache_ud = self.master.User_dynamic (dyn.id)
            return self._cache_ud
        # end def _user_dynamic

        user_dynamic = property (_user_dynamic)

        def dn (self) :
            op     = self.user_dynamic.org_location.orgpath ()
            org_dn = ["ou=%s" % p for p in op [:-1]]
            org_dn.append ("o=%s" % op [-1])
            return "uid=%s,%s,ou=Users,%s" \
                % (self.username, ','.join (org_dn), self.basedn)
        # end def dn

    # end class User

    class Org_location (Roundup) :
        """
            Encapsulate the roundup org_location class.
            Include dn orgpath computation needed for dn computation in
            other classes.
        """

        def orgpath (self) :
            return sum \
                ( [x.domain_part.split ('.') for x in
                    (self.location, self.organisation)
                  ]
                , []
                )
        # end def orgpath

    # end class Org_location
