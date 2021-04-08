# Copyright (C) 2021 Ralf Schlatterbeck. All rights reserved
# Reichergasse 131, A-3411 Weidling
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

import os
import sys
import unittest
import pytest
import logging
import shutil

from ldap3.utils.ciDict import CaseInsensitiveDict

from roundup.test          import memorydb
from roundup.test.mocknull import MockNull
from roundup.configuration import Option, UserConfig
from roundup               import backends
from roundup.date          import Date
# Inject memorydb
backends.memorydb = memorydb

# Monkey-patch Database
# Some trackers inject sql for generating indices or unique constraints
def sql (self, s, *args) :
    t = ('alter table', 'create index')
    for x in t :
        if s.lower ().startswith (t) :
            break
    else :
        assert False, "Unfakeable sql encountered"
memorydb.Database.sql = sql

from roundup       import instance, configuration, init, password, date
from roundup.cgi   import templating
sys.path.insert (0, os.path.abspath ('lib'))
sys.path.insert (0, os.path.abspath ('extensions'))

from ldap_sync import LDAP_Roundup_Sync
import common
import summary

class LDAP_Property :

    def __init__ (self, *args) :
        self.args = args
    # end def __init__

    def __len__ (self) :
        return len (self.args)
    # end def __len__

    def __repr__ (self) :
        if len (self.args) == 1 :
            return self.args [0]
        return self.args
    # end def __repr__
    __str__ = __repr__

    def __getitem__ (self, idx) :
        return self.args [idx]
    # end def __getitem__

# end class LDAP_Property

class default_dict (dict) :
    def __getitem__ (self, name) :
        try :
            return dict.__getitem__ (self, name)
        except KeyError :
            pass
        return MockNull ()
    # end def __getitem__
# end class default_dict

class _Test_Base :
    count = 0
    db = None
    backend = 'memorydb'
    schemaname = 'time'
    schemafile = 'time_ldap'
    verbose = 0
    log = ldap = None

    def setup_tracker (self, backend = None) :
        """ Install and initialize tracker in dirname, return tracker instance.
            If directory exists, it is wiped out before the operation.
        """
        self.__class__.count += 1
        self.dirname = '_test_init_%s' % self.count
        if backend :
            self.backend = backend
        self.config  = config = configuration.CoreConfig ()
        config.DATABASE       = 'db'
        config.RDBMS_NAME     = "rounduptestttt"
        config.RDBMS_HOST     = "localhost"
        if 'RDBMS_HOST' in os.environ :
            config.RDBMS_HOST     = os.environ ['RDBMS_HOST']
        config.RDBMS_USER     = "rounduptest"
        if 'RDBMS_USER' in os.environ :
            config.RDBMS_USER = os.environ ['RDBMS_USER']
        config.RDBMS_PASSWORD = "rounduptest"
        if 'RDBMS_PASSWORD' in os.environ :
            config.RDBMS_PASSWORD = os.environ ['RDBMS_PASSWORD']
        config.MAIL_DOMAIN    = "your.tracker.email.domain.example"
        config.TRACKER_WEB    = "http://localhost:4711/ttt/"
        config.RDBMS_TEMPLATE = "template0"
        config.MAIL_DEBUG     = "maildebug"
        config.init_logging ()
        self.tearDown ()
        srcdir = os.path.join (os.path.dirname (__file__), '..')
        os.mkdir (self.dirname)
        for f in ( 'detectors', 'extensions', 'html', 'initial_data.py'
                 , 'lib', 'locale', 'schema'
                 , 'schemas/%s.py' % self.schemafile
                 , 'TEMPLATE-INFO.txt', 'utils'
                 ) :
            ft = f
            if f.startswith ('schemas') :
                ft = 'schema.py'
            os.symlink \
                ( os.path.abspath (os.path.join (srcdir, f))
                , os.path.join (self.dirname, ft)
                )
        config.RDBMS_BACKEND = self.backend
        self.config.save (os.path.join (self.dirname, 'config.ini'))
        tracker = instance.open (self.dirname)
        if tracker.exists () :
            tracker.nuke ()
        tracker.init (password.Password (self.config.RDBMS_PASSWORD))
        self.tracker = tracker
        # LDAP Config
        config = self.tracker.config
        ldap_settings = dict \
            ( uri            = 'ldap://do.not.care:389'
            , bind_dn        = 'CN=system,OU=test'
            , password       = 'verysecret: this is not used'
            , base_dn        = 'OU=example,DC=example,DC=com'
            , update_ldap    = 'True'
            , update_roundup = 'True'
            , objectclass    = 'user'
            , ad_domains     = 'ds1.internal'
            , no_starttls    = 'False'
            , allowed_dn_suffix_by_domain = \
                'ext1.internal:OU=External'
            )
        config.ext = UserConfig ()
        for k in ldap_settings :
            o = Option (config.ext, 'LDAP', k)
            config.ext.add_option (o)
            config.ext ['LDAP_' + k.upper ()] = ldap_settings [k]
    # end def setup_tracker

    def setUp (self) :
        self.setup_tracker ()
    # end def setUp

    def setup_ldap (self) :
        # Create user-stati for ldap sync
        self.db = self.tracker.open ('admin')
        for g in self.ldap_groups :
            self.db.user_status.create (ldap_group = g, ** self.ldap_groups [g])
        self.ustatus_valid_ad = self.db.user_status.lookup ('valid-ad')
        self.ustatus_valid = self.db.user_status.lookup ('valid')
        for n, name in enumerate (('external Phone', 'Mobile short')) :
            self.db.uc_type.create (name = name, order = n + 5)
        # Create a test-user
        self.testuser1 = self.db.user.create \
            ( username  = 'testuser1@ds1.internal'
            , firstname = 'Test'
            , lastname  = 'User'
            , status    = self.ustatus_valid_ad
            , ad_domain = 'ds1.internal'
            , guid      = '31' # hex ('1')
            )
        self.organisation1 = self.db.organisation.create \
            ( name = 'testorganisation1'
            )
        self.location1 = self.db.location.create \
            ( name = 'testcity'
            , room_prefix = 'ASD.'
            )
        self.org_location1 = self.db.org_location.create \
            ( name = 'testorglocation1'
            , location = self.location1
            , organisation = self.organisation1
            )
        self.department1 = self.db.department.create \
            ( name = 'testdepartment'
            )
        self.room1 = self.db.room.create \
            ( name = 'ASD.OIZ.501'
            , location = self.location1
            )
        self.testuser2 = self.db.user.create \
            ( username  = 'testuser2@ds1.internal'
            , firstname = 'Test2'
            , lastname  = 'User2'
            , status    = self.ustatus_valid_ad
            , ad_domain = 'ds1.internal'
            , guid      = '32' # hex ('2')
            )
        self.user_dynamic2_1 = self.db.user_dynamic.create \
            ( user = self.testuser2
            , org_location = self.org_location1
            , department = self.department1
            , valid_from  = Date('2021-01-01')
            , vacation_yearly = 25
            )
        self.testuser102 = self.db.user.create \
            ( username  = 'testuser2@ext1.internal'
            , firstname = 'Test2'
            , lastname  = 'User2_differ'
            , status    = self.ustatus_valid
            , ad_domain = 'ext1.internal'
            , vie_user  = self.testuser2
            )
        if not self.log :
            self.log = MockNull ()
        if not self.ldap :
            sv = MockNull
            sv.single_value = True
            self.ldap = MockNull ()
            self.ldap.Connection = self.mock_connection
            self.ldap.Server     = self.mock_connection
            self.ldap.search     = self.mock_ldap_search
            self.ldap.modify     = self.mock_ldap_modify
            self.ldap.modify_dn  = self.mock_ldap_modify_dn
            # These are single values in AD and must be treated
            # accordingly during sync
            self.ldap.schema.attribute_types = default_dict \
                ( mail   = sv
                , mobile = sv
                , pager  = sv
                )
        self.ldap_sync = LDAP_Roundup_Sync \
            (self.db, verbose = self.verbose, ldap = self.ldap, log = self.log)
        self.ldap_modify_result    = {}
        self.ldap_modify_dn_result = {}
    # end def setup_ldap

    def mock_connection (self, *args, **kw) :
        """ Called when a new ldap connection or server object is created
            We just return our mock ldap object
        """
        return self.ldap
    # end def mock_connection

    def mock_ldap_search (self, dn, s, attributes = None) :
        """ Emulate an ldap search. We get a Mock object as the first
            parameter, then the base dn (which is currently not used) and
            the query string. Depending on the query string we return
            something in self.entries.
        """
        self.ldap.entries = []
        # Searching for groups
        for g in self.ldap_groups :
            t  = '(&(sAMAccountName=%s)(objectclass=group))' % g
            # We don't care about dn syntax, we're parsing our own
            # output later on.
            dn = g
            if s == t :
                m = MockNull ()
                m.entry_dn = dn
                self.ldap.entries = [m]
                return
        # Searching for members of a group including groups in groups
        if s.startswith ('(&(memberOf:1.2.840.113556.1.4.1941:=') :
            if s.endswith ('objectclass=group))') :
                return
            assert s.endswith ('objectclass=person))')
            g = s [37:].split (')') [0]
            for udn in self.person_dn_by_group.get (g, []) :
                m = MockNull ()
                m.entry_dn = udn
                self.ldap.entries.append (m)
            return
        if  (   s.startswith ('(&(UserPrincipalName=')
            and s.endswith (')(objectclass=user))')
            ) :
            username = s [21:-20]
            entry = self.mock_users_by_username [username]
            m = {}
            m ['attributes'] = entry [1]
            m ['dn'] = entry [0]
            self.ldap.entries = [m]
            return
    # end def mock_ldap_search

    def mock_ldap_modify (self, dn, moddict) :
        self.ldap_modify_result [dn] = moddict
    # end def mock_ldap_modify

    def mock_ldap_modify_dn (self, dn, newdn) :
        self.ldap_modify_dn_result [dn] = newdn
    # end def mock_ldap_modify_dn

    def tearDown (self) :
        for k in 'db', 'db1', 'db2' :
            db = getattr (self, k, None)
            if db :
                db.clearCache ()
                db.close ()
        self.db = self.db1 = self.db2 = None
        if os.path.exists (self.dirname) :
            shutil.rmtree (self.dirname)
    # end def tearDown
# end class _Test_Base

class Test_Case_LDAP_Sync (_Test_Base, unittest.TestCase) :

    # Used for creating user_status objects
    ldap_groups = \
        { 'roundup-users' : dict \
            ( name       = 'valid-ad'
            , ldap_prio  = 1
            , roles      = 'User,Nosy'
            , is_nosy    = True
            )
        , 's_ap_timetracker-system-users' : dict
            ( name       = 'system-ad'
            , ldap_prio  = 2
            , roles      = 'User,Nosy'
            , is_nosy    = True
            )
        , 's_or_ad-natural-user' : dict
            ( name       = 'valid-ad-nopermission'
            , ldap_prio  = 10
            , roles      = 'Anonymous'
            , is_nosy    = False
            )
        }
    person_dn_by_group = \
        { 'roundup-users' :
          [ 'CN=Test User,OU=internal'
          , 'CN=Test Middlename Usernameold,OU=internal'
          , 'CN=Test2 User2,OU=external'
          ]
        }

    # Note: things synced to user_contact must be a list or tuple
    mock_users_by_username = \
        { 'testuser1@ds1.internal' :
          ( 'CN=Test Middlename Usernameold,OU=internal', CaseInsensitiveDict
            ( objectGUID        = MockNull ( raw_values = ['1']
                                           , __len__ = lambda : 1)
            , UserPrincipalName = LDAP_Property ('testuser1@ds1.internal')
            , cn                = LDAP_Property ('Test Middlename Usernameold')
            , givenname         = LDAP_Property ('Test Middlename')
            , sn                = LDAP_Property ('Usernameold')
            , mail              = LDAP_Property ('testuser1@example.com')
            , otherTelephone    = LDAP_Property ('0815')
            , displayname       = LDAP_Property ('Test Middlename Usernameold')
            )
          )
        , 'testuser2@ds1.internal' :
          ( 'CN=Test2 User2,OU=external', CaseInsensitiveDict
            ( objectGUID        = MockNull ( raw_values = ['2']
                                           , __len__ = lambda : 1)
            , UserPrincipalName = LDAP_Property ('testuser2@ds1.internal')
            , cn                = LDAP_Property ('Test2 User2')
            , givenname         = LDAP_Property ('Test2')
            , sn                = LDAP_Property ('User2')
            , mail              = LDAP_Property ('testuser2@example.com')
            , displayname       = LDAP_Property ('Test2 User2')
            )
          )
        }

    def test_sync_contact_to_roundup (self) :
        """ Test that modification of firstname and lastname is synced
            to LDAP
        """
        # If different logging or ldap instrumentation is needed,
        # perform it here before calling setup_ldap, or modify self.ldap
        # and/or self.log afterwards.
        self.setup_ldap ()

        self.ldap_sync.sync_user_from_ldap ('testuser1@ds1.internal')

        user = self.db.user.getnode (self.testuser1)
        self.assertEqual (user.username,  'testuser1@ds1.internal')
        self.assertEqual (user.firstname, 'Test')
        self.assertEqual (user.lastname,  'User')
        self.assertEqual (user.status,    self.ustatus_valid_ad)
        self.assertEqual (user.guid,      '31')
        self.assertEqual (user.ad_domain, 'ds1.internal')
        self.assertEqual (user.contacts,  ['2', '3'])
        ct = self.db.user_contact.getnode ('2')
        self.assertEqual (ct.contact, '0815')
        ct = self.db.user_contact.getnode ('3')
        self.assertEqual (ct.contact, 'testuser1@example.com')
    # end def test_sync_contact_to_roundup

    def test_sync_realname_to_ldap (self) :
        self.setup_ldap ()
        self.ldap_sync.sync_user_to_ldap ('testuser1@ds1.internal')
        olddn = 'CN=Test Middlename Usernameold,OU=internal'
        newdn = 'CN=Test User,OU=internal'
        newcn = newdn.split (',')[0].lower ()
        self.assertEqual \
            (self.ldap_modify_result.keys (), [newdn])
        d = self.ldap_modify_result [newdn]
        self.assertEqual (len (d), 5)
        for k in d :
            self.assertEqual (len (d [k]), 1)
        self.assertEqual (d ['givenname'][0][0], 'MODIFY_REPLACE')
        self.assertEqual (d ['givenname'][0][1], [u'Test'])
        self.assertEqual (d ['displayname'][0][0], 'MODIFY_REPLACE')
        self.assertEqual (d ['displayname'][0][1], [u'Test User'])
        self.assertEqual (d ['employeenumber'][0][0], 'MODIFY_ADD')
        self.assertEqual (d ['employeenumber'][0][1], [u'3'])
        self.assertEqual (d ['sn'][0][0], 'MODIFY_REPLACE')
        self.assertEqual (d ['sn'][0][1], [u'User'])
        self.assertEqual (d ['otherTelephone'][0][0], 'MODIFY_DELETE')
        self.assertEqual (d ['otherTelephone'][0][1], [])
        self.assertEqual (self.ldap_modify_dn_result.keys (), [olddn])
        changed = self.ldap_modify_dn_result [olddn].lower ()
        self.assertEqual (changed, newcn)
    # end def test_sync_realname_to_ldap

    @pytest.mark.xfail
    def test_sync_room_to_ldap (self) :
        self.setup_ldap ()
        self.db.user.set (self.testuser1, room = self.room1)
        self.ldap_sync.sync_user_from_ldap ('testuser1@ds1.internal')
        self.ldap_sync.sync_user_to_ldap ('testuser1@ds1.internal')
        newdn = 'CN=Test User,OU=test'
        d = self.ldap_modify_result [newdn]
        office = d ['physicalDeliveryOfficeName'][0]
        self.assertEqual (office [0], 'MODIFY_ADD')
        self.assertEqual (office [1], [u'ASD.OIZ.501'])
    # end test_sync_room_to_ldap

    def test_dont_sync_if_vie_user_and_dyn_user (self) :
        self.setup_ldap ()
        messages = []
        def mock_log (*msg) :
            messages.append (msg)
        self.log.error = mock_log
        self.assertEqual \
            ( self.db.user.get (self.testuser2, 'vie_user_ml')
            , [self.testuser102]
            )
        self.ldap_sync.sync_user_to_ldap ('testuser2@ds1.internal')
        self.assertEqual (len (messages), 1)
        start_str = 'User testuser2@ds1.internal has a vie_user_ml link'
        self.assertTrue (messages[0][0].startswith (start_str))
        self.assertEqual (self.ldap_modify_result, {})
    # end test_dont_sync_if_vie_user_and_dyn_user

# end class Test_Case_LDAP_Sync

def test_suite () :
    suite = unittest.TestSuite ()
    suite.addTest (unittest.makeSuite (Test_Case_LDAP_Sync))
    return suite
# end def test_suite
