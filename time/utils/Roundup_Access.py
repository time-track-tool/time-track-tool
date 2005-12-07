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
from roundup.hyperdb  import Date, Link, Multilink

class Roundup_Access (object) :
    """ Wrapper class that gets a handle to the roundup instance and
        includes code and classes from there.
    """

    def __init__ (self, basedn, path, user = 'admin') :
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
                raise AttributeError, cause
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
            for ldn, name in self.ldif_map.iteritems () :
                attr = getattr (self, name)
                entry [ldn] = [attr]
            writer.unparse (self.dn (), entry)
            return strio.getvalue ()
        # end def as_ldif

    # end class Roundup

    class User (Roundup) :
        """
            Encapsulate the roundup user class. Includes LDIF export.
        """

        ldif_map = \
            [ ('cn',              'username')
            , ('sn',              'realname')
            , ('telephoneNumber', 'phone')
            , ('description',     'realname')
            , ('displayName',     'realname')
            , ('initials',        'nickname')
            , ('mail',            'address')
            , ('uid',             'username')
            , ('uidNumber',       'uid')
            , ('gidNumber',       'gid')
            , ('homeDirectory',   'home_directory')
            , ('loginShell',      'login_shell')
            , ('gecos',           'gecos')
            ]

        object_class = \
            [ 'top'
            , 'inetOrgPerson'
            , 'posixAccount'
            , 'inetLocalMailRecipient'
            , 'sambaSamAccount'
            , 'shadowAccount'
            ]

        def gid (self) :
            return self.db.group.get (self.group, 'gid')
        # end def gid

        def gecos (self) :
            return ','.join (self.realname, self.phone)
        # end def gecos

        def _cache_dynuser (self, date = Date ('.')) :
            if hasattr (self, '_user_dynamic') :
                return
            date = Date ('.')
            dyn  = self._user_dynamic = get_user_dynamic (self.db, self.id, date)
            if not dyn :
                raise KeyError, "No valid dynamic user record for %s %s" \
                    % (self.username, date.pretty (ymd))
            olo = self.db.org_location.getnode (dyn.org_location)
            org = self.db.organisation.getnode (olo.organisation)
            loc = self.db.org_location.getnode (olo.location)
            self._org_location = olo
            self._organisation = org
            self._location     = loc
        # end def _cache_dynuser

        def orgpath (self) :
            self.organisation
        # end def orgpath

        def dn (self) :
            return "uid=%s,ou=Users,ou=%s,ou=%s,ou=%s,o=%s,%s" \
                % (self.username, self.basedn)
        # end def dn

    # end class User
