#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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
import ldap
import textwrap

from io                 import StringIO
from rsclib.autosuper   import autosuper
from rsclib.IP_Address  import IP4_Address
from roundup.date       import Date
from roundup            import instance
from roundup.hyperdb    import Link, Multilink
from ldap               import modlist
from ldap               import filter as ldapfilter

escape = ldapfilter.escape_filter_chars

class Roundup_Access (object) :
    """ Wrapper class that gets a handle to the roundup instance and
        includes code and classes from there.
    """

    def __init__ (self, path, basedn, user = 'admin') :
        global ymd, get_user_dynamic, common
        self.tracker = instance.open (path)
        self.db      = self.tracker.open (user)
        self.basedn  = basedn
        sys.path.insert (1, os.path.join (path, 'lib'))
        from user_dynamic import get_user_dynamic
        import common
        ymd = common.ymd
        self.common  = common
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
        return '_'.join (r [0].upper () + r [1:] for r in rupname.split ('_'))
    # end def _classname

    def class_from_rupname (self, rupname) :
        return getattr (self, self._classname (rupname))
    # end def class_from_rupname

    class Roundup (autosuper) :
        """
            Base class to encapsulate a roundup Class. With access functions
            for roundup and ldif export.
        """

        zero       = 0
        endofepoch = 0x7FFFFFFF

        def _label (self) :
            return getattr (self, self.cl.labelprop ())
        # end def _label
        label    = ldif_key = property (_label)

        def _now (self) :
            return Date ('.')
        # end def _now
        now = property (_now)

        def __init__ (self, id_or_key) :
            try :
                self.id = str (int (id_or_key))
            except ValueError :
                self.id = self.cl.lookup (id_or_key)
            self.node   = self.cl.getnode (self.id)
        # end def __init__

        def as_ldap_entry (self) :
            entry  = { 'objectClass' : self.object_class }
            for ldn in self.ldif_map :
                name = self.ldif_map [ldn]
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
            return entry
        # end def as_ldap_entry

        def as_ldif (self) :
            return self._ldif (self.dn (), self.as_ldap_entry ())
        # end def as_ldif

        def as_replog (self, url, basedn, binddn, bindpw) :
            ld = ldap.initialize (url)
            ld.simple_bind_s (binddn, bindpw)
            sk = self.ldap_search_key ()
            lu = ld.search_s \
                ( basedn
                , ldap.SCOPE_SUBTREE
                , sk
                , list (self.ldif_map) + self.object_class
                )
            print lu
            if len (lu) > 1 :
                raise ValueError, "More than one entry found for %s" % sk
            if not lu :
                return self._ldif \
                    (self.dn (), modlist.addModlist (self.as_ldap_entry ()))
            ret = []
            dn  = self.dn ().split (',')
            if self.dn () != lu[0][0] :
                ret.append ('dn: %s' % lu[0][0])
                ret.append ('changetype: modrdn')
                ret.append ('newrdn: %s' % dn [0])
                ret.append ('deleteoldrdn: 1')
                ret.append ('newSuperior: %s' % ','.join (dn [1:]))
                ret.append ('')
            ret.append \
                ( self._ldif 
                    ( self.dn ()
                    , modlist.modifyModlist (lu [0][1], self.as_ldap_entry ())
                    )
                )
            return '\n'.join (ret)
        # end def as_replog

        def dnname_ou (self, ou = None) :
            if ou is None :
                ou = ''
                if self.ou :
                    ou = ",ou=%s" % self.ou
            return "%s=%s%s" % (self.dnname, self.ldif_key, ou)
        # end def dnname_ou

        def dn (self) :
            op     = self.org_location.orgpath
            org_dn = ["ou=%s" % p for p in op [:-1]]
            org_dn.append ("o=%s" % op [-1])
            return "%s,%s,%s" \
                % (self.dnname_ou (), ','.join (org_dn), self.basedn)
        # end def dn

        def filter (cls, *args, **kw) :
            return (cls (i) for i in cls.cl.filter (*args, **kw))
        filter = classmethod (filter)

        def find (cls, *args, **kw) :
            return (cls (i) for i in cls.cl.find (*args, **kw))
        find = classmethod (find)

        def ldap_search_key (self) :
            return ldapfilter.filter_format \
                ( '(&(%s)(objectClass=%%s))' % escape (self.dnname_ou (''))
                , (self.object_class [0],)
                )
        # end def ldap_search_key

        def _ldif (self, dn, entry) :
            strio  = StringIO ()
            writer = ldif.LDIFWriter (strio)
            writer.unparse (dn, entry)
            return strio.getvalue ()
        # end def _ldif

        def __getattr__ (self, name) :
            try :
                value = self.node [name]
            except KeyError, cause :
                raise AttributeError, "%s%s: %s" \
                    % (self.node.cl.classname, self.id, cause)
            if value is None : return value
            prop = self.node.cl.properties [name]
            if prop.__class__ == Link :
                value = self.master.class_from_rupname (prop.classname) (value)
                setattr (self, name, value)
            elif prop.__class__ == Multilink :
                newval = []
                cls    = self.master.class_from_rupname (prop.classname)
                for v in value :
                    newval.append (cls (v))
                value = newval
            return value
        # end def __getattr__

    # end class Roundup

    class Org_Location (Roundup) :
        """
            Encapsulate the roundup org_location class.
            Include dn orgpath computation needed for dn computation in
            other classes.
            Include DHCP and DNS generation (the latter produces forward
            DNS records).
        """

        def _orgpath (self) :
            return sum \
                ( [x.domain_part.split ('.') for x in
                    (self.location, self.organisation)
                  ]
                , []
                )
        # end def _orgpath
        orgpath = property (_orgpath)

        def _ip_subnet (self) :
            sn = self.master.Ip_Subnet.find (org_location = self.id)
            return sn
        # end def _ip_subnet
        ip_subnet = property (_ip_subnet)

        def _domain (self) :
            return '.'.join (self.orgpath)
        # end def _domain
        domain = property (_domain)

        def dhcp_header (self) :
            return textwrap.dedent \
                (("""
                     #####################################################
                     # dhcpd.conf created: %s
                     # Configuration file for ISC dhcpd
                     # THIS FILE WAS AUTOMATICALLY GENERATED - DO NOT EDIT
                     #####################################################
                     
                     authoritative;
                     option domain-name "%s";
                     server-name "%s.%s";
                     
                  """)
                % ( self.now.pretty ('%Y-%m-%d %H:%M:%S')
                  , self.domain
                  , self.dhcp_server.name
                  , self.domain
                  )
                )
        # end def dhcp_header

        def as_dhcp (self) :
            dhcp = [self.dhcp_header ()]
            for sn in self.ip_subnet :
                dhcp.append (sn.as_dhcp ())
            return '\n'.join (dhcp)
        # end def as_dhcp

        def as_dns (self) :
            na  = self.master.Network_Address.find (org_location = self.id)
            dns = []
            for n in na :
                if not n.machine_name : continue
                dns.append (n.machine_name.as_dns (self))
            return "\n".join (d for d in dns if d)
        # end def as_dns

    # end class Org_Location

    class User (Roundup) :
        """
            Encapsulate the roundup user class. Includes LDIF export.
            uid=..,ou=Users,ou=vie,ou=at,ou=company,o=org,BASEDN
        """

        ldif_map = dict \
            (( ('cn',                   'username')
            ,  ('description',          'realname')
            ,  ('displayName',          'realname')
            ,  ('gecos',                'gecos')
            ,  ('homeDirectory',        'home_directory')
            ,  ('initials',             'nickname')
            ,  ('loginShell',           'login_shell')
            ,  ('mail',                 'address')
            ,  ('mailHost',             'mail_host')
            ,  ('mailLocalAddress',     'mail_addresses')
            ,  ('mailRoutingAddress',   'mail_routing_address')
            ,  ('sambaAcctFlags',       'samba_acct_flags')
            ,  ('sambaHomeDrive',       'samba_home_drive')
            ,  ('sambaHomePath',        'samba_home_path')
            ,  ('sambaKickoffTime',     'samba_kickoff_time')
            ,  ('sambaLMPassword',      'samba_lm_password')
            ,  ('sambaLogoffTime',      'endofepoch')
            ,  ('sambaLogonScript',     'samba_logon_script')
            ,  ('sambaLogonTime',       'zero')
            ,  ('sambaNTPassword',      'samba_nt_password')
            ,  ('sambaPrimaryGroupSID', 'group_sid')
            ,  ('sambaProfilePath',     'samba_profile_path')
            ,  ('sambaPwdCanChange',    'samba_pwd_can_change')
            ,  ('sambaPwdLastSet',      'samba_pwd_last_set')
            ,  ('sambaPwdMustChange',   'samba_pwd_must_change')
            ,  ('sambaSID',             'sid')
            ,  ('shadowExpire',         'shadow_expire')
            ,  ('shadowFlag',           'shadow_used')
            ,  ('shadowInactive',       'shadow_inactive')
            ,  ('shadowLastChange',     'shadow_last_change')
            ,  ('shadowMax',            'shadow_max')
            ,  ('shadowMin',            'shadow_min')
            ,  ('shadowWarning',        'shadow_warning')
            ,  ('sn',                   'realname')
            ,  ('uidNumber',            'uid')
            ,  ('uid',                  'username')
            ,  ('userPassword',         'user_password')
            ))

        samba_acct_flags = '[U]'

        object_class = \
            [ 'posixAccount'
            , 'inetLocalMailRecipient'
            , 'inetOrgPerson'
            , 'sambaSamAccount'
            , 'shadowAccount'
            , 'top'
            ]

        ou           = 'Users'
        dnname       = 'uid'

        def _gecos (self) :
            return self.realname
        # end def _gecos
        gecos = property (_gecos)

        def _mail_addresses (self) :
            return [self.address.split ('@')[0], self.username, self.nickname]
        # end def _mail_addresses
        mail_addresses = property (_mail_addresses)

        def _mail_host (self) :
            return self.address.split ('@')[1]
        # end def _mail_host
        mail_host = property (_mail_host)

        def _mail_routing_address (self) :
            return '@'.join ((self.username, self.mail_host))
        # end def _mail_routing_address
        mail_routing_address = property (_mail_routing_address)

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
            self._cache_ud = self.master.User_Dynamic (dyn.id)
            return self._cache_ud
        # end def _user_dynamic
        user_dynamic = property (_user_dynamic)

        def _org_location (self) :
            return self.user_dynamic.org_location
        # end def _org_location
        org_location = property (_org_location)

    # end class User

# end class Roundup_Access
