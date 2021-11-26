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

from __future__ import unicode_literals

import os
import sys
import copy
import unittest
import pytest
import logging
import shutil

from hashlib            import md5
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

    @property
    def value (self) :
        return repr (self)
    # end def value

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

class Mock_Guid :

    def __init__ (self, value) :
        self.value = value
        self.raw_values = [value]
    # end def __init__

    def __len__ (self) :
        return 1
    # end def __len__

# end class Mock_Guid

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
        self.base_dn = 'OU=example,DC=example,DC=com'
        ldap_settings = dict \
            ( uri            = 'ldap://do.not.care:389'
            , bind_dn        = 'CN=system,OU=test'
            , password       = 'verysecret: this is not used'
            , base_dn        = self.base_dn
            , update_ldap    = 'True'
            , update_roundup = 'True'
            , objectclass    = 'user'
            , ad_domains     = 'ds1.internal'
            , no_starttls    = 'False'
            , do_not_sync_roundup_properties = ''
            , do_not_sync_ldap_properties = ''
            , allowed_dn_suffix_by_domain = \
                'ext1.internal:OU=External'
            )
        limit_settings = dict \
            ( picture_sync_size = '9k'
            #, picture_quality   = '80'
            )
        config.ext = UserConfig ()
        for k in ldap_settings :
            o = Option (config.ext, 'LDAP', k)
            config.ext.add_option (o)
            config.ext ['LDAP_' + k.upper ()] = ldap_settings [k]
        for k in limit_settings :
            o = Option (config.ext, 'LIMIT', k)
            config.ext.add_option (o)
            config.ext ['LIMIT_' + k.upper ()] = limit_settings [k]
        # Override before call to setup_ldap if necessary
        self.aux_ldap_parameters = {}
    # end def setup_tracker

    def setUp (self) :
        self.setup_tracker ()
    # end def setUp

    def setup_ldap (self) :
        # Create user-stati for ldap sync
        self.db = self.tracker.open ('admin')
        # This is used by mock_log which is not used by default
        self.messages = []
        for g in self.ldap_groups :
            self.db.user_status.create (ldap_group = g, ** self.ldap_groups [g])
        self.ustatus_valid_ad = self.db.user_status.lookup ('valid-ad')
        self.ustatus_valid = self.db.user_status.lookup ('valid')
        for n, name in enumerate (('external Phone', 'Mobile short')) :
            self.db.uc_type.create (name = name, order = n + 5)
        # Create a test-user
        self.testuser1 = self.db.user.create \
            ( username  = str ('testuser1@ds1.internal')
            , firstname = str ('Test')
            , lastname  = str ('User')
            , status    = self.ustatus_valid_ad
            , ad_domain = str ('ds1.internal')
            , guid      = '31' # hex ('1')
            )
        self.organisation1 = self.db.organisation.create \
            ( name = str ('testorganisation1')
            )
        self.location1 = self.db.location.create \
            ( name = str ('testcity')
            , room_prefix = str ('ASD.')
            )
        self.org_location1 = self.db.org_location.create \
            ( name = str ('testorglocation1')
            , location = self.location1
            , organisation = self.organisation1
            )
        self.room1 = self.db.room.create \
            ( name = str ('ASD.OIZ.501')
            , location = self.location1
            )
        self.room2 = self.db.room.create \
            ( name = str ('ASD.MJH.402')
            , location = self.location1
            )
        self.user_dynamic1_1 = self.db.user_dynamic.create \
            ( user            = self.testuser1
            , org_location    = self.org_location1
            , valid_from      = Date (str ('2021-01-01'))
            , vacation_yearly = 25
            )
        self.testuser2 = self.db.user.create \
            ( username  = str ('testuser2@ds1.internal')
            , firstname = str ('Test2')
            , lastname  = str ('User2')
            , status    = self.ustatus_valid_ad
            , ad_domain = str ('ds1.internal')
            , guid      = str ('32') # hex ('2')
            , room      = self.room1
            )
        self.user_dynamic2_1 = self.db.user_dynamic.create \
            ( user            = self.testuser2
            , org_location    = self.org_location1
            , valid_from      = Date (str ('2021-01-01'))
            , vacation_yearly = 25
            )
        self.testuser102 = self.db.user.create \
            ( username  = str ('testuser2@ext1.internal')
            , firstname = str ('Test2')
            , lastname  = str ('NewLastname')
            , status    = self.ustatus_valid
            , ad_domain = str ('ext1.internal')
            , vie_user  = self.testuser2
            )
        self.telephone_for_102 = self.db.user_contact.create \
            ( contact      = '08154711'
            , contact_type = self.db.uc_type.lookup ('mobile Phone')
            )
        self.db.user.set (self.testuser102, contacts = [self.telephone_for_102])
        self.user_dynamic102_1 = self.db.user_dynamic.create \
            ( user            = self.testuser102
            , org_location    = self.org_location1
            , valid_from      = Date (str ('2021-01-01'))
            , vacation_yearly = 25
            )
        self.testuser3 = self.db.user.create \
            ( username  = str ('rcase@ds1.internal')
            , firstname = str ('Roman')
            , lastname  = str ('Case')
            , status    = self.ustatus_valid_ad
            , ad_domain = str ('ds1.internal')
            , guid      = str ('33') # hex ('3')
            )
        self.user_dynamic3_1 = self.db.user_dynamic.create \
            ( user            = self.testuser3
            , org_location    = self.org_location1
            , valid_from      = Date (str ('2021-01-01'))
            , vacation_yearly = 25
            )
        self.testuser4 = self.db.user.create \
            ( username  = str ('jdoe@ds1.internal')
            , firstname = str ('Jane')
            , lastname  = str ('Doe')
            , status    = self.ustatus_valid_ad
            , ad_domain = str ('ds1.internal')
            , guid      = str ('34') # hex ('4')
            )
        self.testuser104 = self.db.user.create \
            ( username  = str ('jane.doe@ext1.internal')
            , firstname = str ('Jane')
            , lastname  = str ('Doe')
            , status    = self.ustatus_valid
            , ad_domain = str ('ext1.internal')
            , vie_user  = self.testuser4
            )
        self.testuser5 = self.db.user.create \
            ( username  = str ('vsuper@ds1.internal')
            , firstname = str ('Vincent')
            , lastname  = str ('Super')
            , status    = self.ustatus_valid_ad
            , ad_domain = str ('ds1.internal')
            , guid      = str ('35') # hex ('5')
            )
        self.testuser105 = self.db.user.create \
            ( username  = str ('vicent.super@ext1.internal')
            , firstname = str ('Vincent')
            , lastname  = str ('Super')
            , status    = self.ustatus_valid
            , ad_domain = str ('ext1.internal')
            , vie_user  = self.testuser5
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
            self.ldap.extend.standard.paged_search = self.mock_paged_search
            # These are single values in AD and must be treated
            # accordingly during sync
            self.ldap.schema.attribute_types = default_dict \
                ( mail   = sv
                , mobile = sv
                , pager  = sv
                )
        self.ldap_sync = LDAP_Roundup_Sync \
            ( self.db
            , verbose = self.verbose
            , ldap    = self.ldap
            , log     = self.log
            , ** self.aux_ldap_parameters
            )
        self.ldap_modify_result    = {}
        self.ldap_modify_dn_result = {}
    # end def setup_ldap

    def mock_connection (self, *args, **kw) :
        """ Called when a new ldap connection or server object is created
            We just return our mock ldap object
        """
        return self.ldap
    # end def mock_connection

    def mock_ldap_search (self, dn, s, attributes = None, search_scope = None) :
        """ Emulate an ldap search. We get a Mock object as the first
            parameter, then the base dn (which is currently not used) and
            the query string. Depending on the query string we return
            something in self.entries.
        """
        self.ldap.entries = []
        # Searching by DN
        if search_scope :
            username = self.person_username_by_dn [dn]
            entry = self.mock_users_by_username [username]
            m = {}
            m ['attributes'] = entry [1]
            m ['dn'] = entry [0]
            self.ldap.entries = [m]
            return

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

    def mock_paged_search (self, base_dn, filter, **d) :
        self.assertEqual (filter, '(objectclass=user)')
        self.assertIn ('attributes', d)
        self.assertEqual (base_dn, self.base_dn)
        self.assertEqual (d ['attributes'], ['UserPrincipalName'])
        # Loop over *all* ldap users
        l = []
        for username in self.mock_users_by_username :
            m = {}
            m ['attributes'] = CaseInsensitiveDict \
                (UserPrincipalName = username)
            m ['dn'] = self.mock_users_by_username [username][0]
            l.append (m)
        return l
    # end def mock_paged_search

    def mock_ldap_modify (self, dn, moddict) :
        self.ldap_modify_result [dn] = moddict
    # end def mock_ldap_modify

    def mock_ldap_modify_dn (self, dn, newdn) :
        self.ldap_modify_dn_result [dn] = newdn
    # end def mock_ldap_modify_dn

    def mock_log (self, *msg) :
        """ Not used by default, needs mockup in test
        """
        self.messages.append (msg)
    # end def mock_log

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
          , 'CN=Roman Case,OU=internal'
          , 'CN=Jane Doe,OU=external'
          , 'CN=Vincent Super,OU=external'
          , 'CN=Nonexisting Roundup,OU=internal'
          ]
        }

    # Note: things synced to user_contact must be a list or tuple
    mock_users_by_username = \
        { 'testuser1@ds1.internal' :
          ( 'CN=Test Middlename Usernameold,OU=internal', CaseInsensitiveDict
            ( objectGUID        = Mock_Guid ('1')
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
            ( objectGUID        = Mock_Guid ('2')
            , UserPrincipalName = LDAP_Property ('testuser2@ds1.internal')
            , cn                = LDAP_Property ('Test2 User2')
            , givenname         = LDAP_Property ('Test2')
            , sn                = LDAP_Property ('User2')
            , mail              = LDAP_Property ('testuser2@example.com')
            , displayname       = LDAP_Property ('Test2 User2')
            )
          )
        , 'rcase@ds1.internal' :
          ( 'CN=Roman Case,OU=internal', CaseInsensitiveDict
            ( objectGUID        = Mock_Guid ('3')
            , UserPrincipalName = LDAP_Property ('rcase@ds1.internal')
            , cn                = LDAP_Property ('Roman Case')
            , givenname         = LDAP_Property ('Roman')
            , sn                = LDAP_Property ('Case')
            , mail              = LDAP_Property ('roman.case@example.com')
            , displayname       = LDAP_Property ('Roman Case')
            , physicalDeliveryOfficeName = LDAP_Property ('ASD.MJH.402')
            , department = LDAP_Property ('original_department')
            )
          )
        , 'jdoe@ds1.internal' :
          ( 'CN=Jane Doe,OU=external', CaseInsensitiveDict
            ( objectGUID        = Mock_Guid ('4')
            , UserPrincipalName = LDAP_Property ('jdoe@ds1.internal')
            , cn                = LDAP_Property ('Jane Doe')
            , givenname         = LDAP_Property ('Jane')
            , sn                = LDAP_Property ('Doe')
            , mail              = LDAP_Property ('jane.doe@example.com')
            , displayname       = LDAP_Property ('Jane Doe')
            , physicalDeliveryOfficeName = LDAP_Property ('ASD.MJH.402')
            )
          )
        , 'vsuper@ds1.internal' :
          ( 'CN=Vincent Super,OU=external', CaseInsensitiveDict
            ( objectGUID        = Mock_Guid ('5')
            , UserPrincipalName = LDAP_Property ('vsuper@ds1.internal')
            , cn                = LDAP_Property ('Vincent Super')
            , givenname         = LDAP_Property ('Vincent')
            , sn                = LDAP_Property ('Super')
            , mail              = LDAP_Property ('vincent.super@example.com')
            , displayname       = LDAP_Property ('Vincent Super')
            , physicalDeliveryOfficeName = LDAP_Property ('ASD.MJH.402')
            )
          )
        , 'nonexistingrup@ds1.internal' :
          ( 'CN=Nonexisting Roundup,OU=internal', CaseInsensitiveDict
            ( objectGUID        = Mock_Guid ('6')
            , UserPrincipalName = LDAP_Property ('nonexistingrup@ds1.internal')
            , cn                = LDAP_Property ('Nonexisting Roundup')
            , givenname         = LDAP_Property ('Nonexisting')
            , sn                = LDAP_Property ('Roundup')
            , mail              = LDAP_Property ('nonexisting.rup@example.com')
            , displayname       = LDAP_Property ('Nonexisting Roundup')
            )
          )
        }

    person_username_by_dn = dict \
        ((v [0], k) for k, v in mock_users_by_username.items ())


    def set_testuser1_testpic (self) :
        with open ('test/240px-Bald_Man.svg.png', 'rb') as f :
            fid = self.db.file.create \
                ( name    = 'picture'
                , type    = 'image/png'
                , content = f.read ()
                )
            self.db.user.set (self.testuser1, pictures = [fid])
    # end def set_testuser1_testpic

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
        self.assertEqual (user.contacts,  ['3', '4'])
        ct = self.db.user_contact.getnode ('3')
        self.assertEqual (ct.contact, '0815')
        ct = self.db.user_contact.getnode ('4')
        self.assertEqual (ct.contact, 'testuser1@example.com')
    # end def test_sync_contact_to_roundup

    def test_sync_new_user_to_roundup (self) :
        self.setup_ldap ()
        self.ldap_sync.sync_user_from_ldap ('nonexistingrup@ds1.internal')
        newuser = self.db.user.lookup ('nonexistingrup@ds1.internal')
        user = self.db.user.getnode (newuser)
        self.assertEqual (user.username,  'nonexistingrup@ds1.internal')
        self.assertEqual (user.firstname, 'Nonexisting')
        self.assertEqual (user.lastname,  'Roundup')
        self.assertEqual (user.status,    self.ustatus_valid_ad)
        self.assertEqual (user.guid,      '36')
        self.assertEqual (user.ad_domain, 'ds1.internal')
    # end def test_sync_new_user_to_roundup

    def test_sync_to_roundup_all (self) :
        # Change behavior so that names are updated in roundup
        self.aux_ldap_parameters ['update_ldap'] = False
        self.setup_ldap ()
        self.log.info = self.mock_log
        self.ldap_sync.sync_all_users_from_ldap ()
        msg = 'Synced %s users from LDAP to roundup' \
              % (len (self.mock_users_by_username) - 1)
        self.assertEqual (self.messages [-2][0], msg)
        user = self.db.user.getnode (self.testuser1)
        self.assertEqual (user.firstname, 'Test Middlename')
        self.assertEqual (user.lastname,  'Usernameold')
    # end def test_sync_to_roundup_all

    def test_sync_to_roundup_all_dry (self) :
        # Change behavior so that names are updated in roundup
        self.aux_ldap_parameters ['update_ldap']     = False
        self.aux_ldap_parameters ['dry_run_roundup'] = True
        self.setup_ldap ()
        self.log.info = self.mock_log
        self.ldap_sync.sync_all_users_from_ldap ()
        msg = '(Dry Run): Synced %s users from LDAP to roundup' \
              % (len (self.mock_users_by_username) - 1)
        self.assertEqual (self.messages [-2][0], msg)
        user = self.db.user.getnode (self.testuser1)
        self.assertEqual (user.firstname, 'Test')
        self.assertEqual (user.lastname,  'User')
    # end def test_sync_to_roundup_all_dry

    def test_sync_to_roundup_all_limit (self) :
        # Change behavior so that names are updated in roundup
        self.aux_ldap_parameters ['update_ldap']     = False
        self.setup_ldap ()
        self.log.error = self.mock_log
        self.ldap_sync.sync_all_users_from_ldap (max_changes = 1)
        msg = ('Number of changes (%s) from LDAP to Roundup '
              'would exceed maximum 1, aborting') \
              % (len (self.mock_users_by_username) - 1)
        self.assertEqual (self.messages [-1][0], msg)
        user = self.db.user.getnode (self.testuser1)
        self.assertEqual (user.firstname, 'Test')
        self.assertEqual (user.lastname,  'User')
    # end def test_sync_to_roundup_all_dry

    def test_sync_realname_to_ldap (self) :
        self.setup_ldap ()
        self.ldap_sync.sync_user_to_ldap ('testuser1@ds1.internal')
        olddn = 'CN=Test Middlename Usernameold,OU=internal'
        newdn = 'CN=Test User,OU=internal'
        newcn = newdn.split (',') [0].lower ()
        self.assertEqual \
            (self.ldap_modify_result.keys (), [newdn])
        d = self.ldap_modify_result [newdn]
        self.assertEqual (len (d), 7)
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
        self.assertEqual (d ['company'][0][0], 'MODIFY_ADD')
        self.assertEqual (d ['company'][0][1][0], 'testorglocation1')
        self.assertEqual (self.ldap_modify_dn_result.keys (), [olddn])
        changed = self.ldap_modify_dn_result [olddn].lower ()
        self.assertEqual (changed, newcn)
    # end def test_sync_realname_to_ldap

    def test_dont_sync_cn_if_no_dynuser (self) :
        self.setup_ldap ()
        self.log.warn = self.mock_log
        self.db.user_dynamic.retire (self.user_dynamic1_1)
        self.ldap_sync.sync_user_to_ldap ('testuser1@ds1.internal')
        olddn = 'CN=Test Middlename Usernameold,OU=internal'
        self.assertEqual \
            (self.ldap_modify_result.keys (), [olddn])
        d = self.ldap_modify_result [olddn]
        self.assertEqual (len (d), 4)
        self.assertEqual (self.ldap_modify_dn_result.keys (), [])
        msg = 'Not syncing "realname"->"cn": no valid dyn. user for'
        self.assertTrue (self.messages [-1][0].startswith (msg))
    # end def test_dont_sync_cn_if_no_dynuser

    def test_sync_cn_if_no_dynuser_but_system (self) :
        self.setup_ldap ()
        self.log.error = self.mock_log
        self.db.user_dynamic.retire (self.user_dynamic1_1)
        self.db.user_status.set (self.ustatus_valid_ad, is_system = True)
        self.ldap_sync.sync_user_to_ldap ('testuser1@ds1.internal')
        newdn = 'CN=Test User,OU=internal'
        olddn = 'CN=Test Middlename Usernameold,OU=internal'
        newcn = newdn.split (',') [0].lower ()
        self.assertEqual \
            (self.ldap_modify_result.keys (), [newdn])
        d = self.ldap_modify_result [newdn]
        # The number differs from the test_sync_realname_to_ldap above
        # because we've retired the dynamic user record
        self.assertEqual (len (d), 5)
        self.assertEqual (self.ldap_modify_dn_result.keys (), [olddn])
        changed = self.ldap_modify_dn_result [olddn].lower ()
        self.assertEqual (changed, newcn)
    # end def test_sync_cn_if_no_dynuser_but_system

    def test_sync_no_cn (self) :
        self.tracker.config.ext.LDAP_DO_NOT_SYNC_LDAP_PROPERTIES = 'cn'
        self.setup_ldap ()
        self.ldap_sync.sync_user_to_ldap ('testuser1@ds1.internal')
        olddn = 'CN=Test Middlename Usernameold,OU=internal'
        self.assertEqual \
            (self.ldap_modify_result.keys (), [olddn])
        d = self.ldap_modify_result [olddn]
        self.assertEqual (len (d), 6)
        assert 'displayname' not in d
        self.assertEqual (d ['givenname'][0][0], 'MODIFY_REPLACE')
        self.assertEqual (d ['givenname'][0][1], [u'Test'])
        self.assertEqual (d ['sn'][0][0], 'MODIFY_REPLACE')
        self.assertEqual (d ['sn'][0][1], [u'User'])
        self.assertFalse (self.ldap_modify_dn_result)
        self.ldap_sync.sync_user_from_ldap ('testuser1@ds1.internal')
        u = self.db.user.getnode (self.testuser1)
        # firstname/lastname/realname *not* changed in roundup
        self.assertEqual (u.firstname, 'Test')
        self.assertEqual (u.lastname, 'User')
        self.assertEqual (u.realname, 'Test User')
    # end def test_sync_no_cn

    def test_sync_realname_to_ldap_all (self) :
        self.setup_ldap ()
        nusers = len (self.db.user.filter (None, {})) / 2 - 1
        self.log.info = self.mock_log
        self.ldap_sync.sync_all_users_to_ldap ()
        newdn = 'CN=Test User,OU=internal'
        self.assertEqual (len (self.ldap_modify_result), nusers)
        self.assertEqual (len (self.ldap_modify_result [newdn]), 7)
        msg = 'Synced %s users from roundup to LDAP' % nusers
        self.assertEqual (self.messages [-2][0], msg)
    # end def test_sync_realname_to_ldap_all

    def test_sync_realname_to_ldap_all_dryrun (self) :
        self.aux_ldap_parameters ['dry_run_ldap'] = True
        self.setup_ldap ()
        nusers = len (self.db.user.filter (None, {})) / 2 - 1
        self.log.info = self.mock_log
        self.ldap_sync.sync_all_users_to_ldap ()
        self.assertEqual (len (self.ldap_modify_result), 0)
        msg = '(Dry Run): Synced %s users from roundup to LDAP' % nusers
        self.assertEqual (self.messages [-2][0], msg)
    # end def test_sync_realname_to_ldap_all

    def test_sync_realname_to_ldap_all_limit (self) :
        self.setup_ldap ()
        nusers = len (self.db.user.filter (None, {})) / 2 - 1
        self.log.error = self.mock_log
        self.ldap_sync.sync_all_users_to_ldap (max_changes = 0)
        self.assertEqual (len (self.ldap_modify_result), 0)
        msg = ('Number of changes (%s) from Roundup to LDAP would exceed '
              'maximum 0, aborting') % nusers
        self.assertEqual (self.messages [-1][0], msg)
    # end def test_sync_realname_to_ldap_all

    def test_sync_room_to_ldap (self) :
        self.setup_ldap ()
        self.db.user.set (self.testuser1, room = self.room1)
        self.ldap_sync.sync_user_from_ldap ('testuser1@ds1.internal')
        self.ldap_sync.sync_user_to_ldap ('testuser1@ds1.internal')
        newdn = 'CN=Test User,OU=internal'
        d = self.ldap_modify_result [newdn]
        office = d ['physicalDeliveryOfficeName'][0]
        self.assertEqual (office [0], 'MODIFY_ADD')
        self.assertEqual (office [1], [u'ASD.OIZ.501'])
    # end test_sync_room_to_ldap

    def test_dont_sync_if_vie_user_and_dyn_user (self) :
        self.setup_ldap ()
        self.log.error = self.mock_log
        self.assertEqual \
            ( self.db.user.get (self.testuser2, 'vie_user_ml')
            , [self.testuser102]
            )
        self.ldap_sync.sync_user_to_ldap ('testuser2@ds1.internal')
        self.assertEqual (len (self.messages), 1)
        start_str = 'User testuser2@ds1.internal has a vie_user_ml link'
        self.assertTrue (self.messages [0][0].startswith (start_str))
        self.assertEqual (self.ldap_modify_result, {})
    # end test_dont_sync_if_vie_user_and_dyn_user

    def test_sync_if_vie_user_and_dyn_user_when_bl_override (self) :
        self.setup_ldap ()
        self.log.error = self.mock_log
        self.assertEqual \
            ( self.db.user.get (self.testuser2, 'vie_user_ml')
            , [self.testuser102]
            )
        self.ldap_sync.sync_user_to_ldap ('testuser2@ds1.internal')
        self.assertEqual (len (self.messages), 1)
        start_str = 'User testuser2@ds1.internal has a vie_user_ml link'
        self.assertTrue (self.messages [0][0].startswith (start_str))
        self.assertEqual (self.ldap_modify_result, {})
       
        # override with user itself
        self.db.user.set (self.testuser2, vie_user_bl_override = self.testuser2)
        self.ldap_sync.sync_user_to_ldap ('testuser2@ds1.internal')
        self.maxDiff = None
        dn = 'CN=Test2 User2,OU=external'
        self.assertEqual (len (self.ldap_modify_result), 1)
        self.assertEqual (len (self.ldap_modify_result [dn]), 4)
        self.assertEqual (self.ldap_modify_dn_result, {})

        # override with user external user
        self.db.user.set \
            (self.testuser2, vie_user_bl_override = self.testuser102)
        self.ldap_sync.sync_user_to_ldap ('testuser2@ds1.internal')
        cn = 'cn=Test2 NewLastname'
        self.assertEqual (self.ldap_modify_dn_result [dn], cn)
        dn = 'CN=Test2 NewLastname,OU=external'
        self.assertEqual (len (self.ldap_modify_result [dn]), 6)
        results = \
            ( ('displayname', 'Test2 NewLastname')
            , ('sn',          'NewLastname')
            , ('mobile',      '08154711')
            )
        for k, v in results :
            self.assertEqual (self.ldap_modify_result [dn][k][0][1][0], v)
    # end test_dont_sync_if_vie_user_and_dyn_user

    def test_sync_email_only_from_ad (self) :
        self.setup_ldap ()
        # check initial sync to Roundup
        def get_contacts ():
            return self.db.user.get (self.testuser3, 'contacts')
        self.assertFalse (get_contacts ())
        self.ldap_sync.sync_user_from_ldap ('rcase@ds1.internal')
        self.assertTrue (get_contacts ())
        user_contact = self.db.user_contact.get (get_contacts ()[0], 'contact')
        self.assertEqual (user_contact, 'roman.case@example.com')

        # change contact in Roundup, check if not synced back
        self.user_contact1 = self.db.user_contact.create \
            ( contact = 'case@example.com'
            , contact_type = str ('1')
            )
        self.db.user.set (self.testuser3, contacts = [self.user_contact1])
        self.ldap_sync.sync_user_to_ldap ('rcase@ds1.internal')
        dn = 'CN=Roman Case,OU=internal'
        self.assertNotIn ('mail', self.ldap_modify_result [dn])

        # check if overwritten again with correct mail address
        self.ldap_sync.sync_user_from_ldap ('rcase@ds1.internal')
        self.assertTrue (get_contacts ())
        user_contact = self.db.user_contact.get (get_contacts ()[0], 'contact')
        self.assertEqual (user_contact, 'roman.case@example.com')
    # end test_sync_email_only_from_ad

    def test_sync_supervisor (self) :
        self.setup_ldap ()
        self.ldap_sync.sync_user_to_ldap ('jdoe@ds1.internal')
        dn = 'CN=Jane Doe,OU=external'
        self.assertNotIn ('manager', self.ldap_modify_result [dn])
        
        # set supervisor on external user
        self.db.user.set (self.testuser104, supervisor = self.testuser105)
        self.ldap_sync.sync_user_to_ldap ('jdoe@ds1.internal')
        self.assertIn ('manager', self.ldap_modify_result [dn])

        # unlink vie_user and set internal supervisor
        self.db.user.set (self.testuser104, vie_user = None)
        self.db.user.set (self.testuser4, supervisor = self.testuser3)
        self.ldap_sync.sync_user_to_ldap ('jdoe@ds1.internal')
        new_secretary = self.ldap_modify_result [dn]['manager'][0][1][0]
        self.assertEqual (new_secretary, 'CN=Roman Case,OU=internal')
    # end test_sync_supervisor

    def test_sync_department (self) :
        self.setup_ldap ()
        self.ldap_sync.sync_user_from_ldap ('rcase@ds1.internal')
        self.ldap_sync.sync_user_to_ldap ('rcase@ds1.internal')
        dn = 'CN=Roman Case,OU=internal'
        new_department = self.ldap_modify_result [dn]['department'][0][1][0]
        self.assertEqual \
            (new_department, self.db.department.get (self.department1, 'name'))

        # set department_temp and check override
        department_temp_name = 'dep_override'
        self.db.user.set \
            (self.testuser3, department_temp = department_temp_name)
        self.ldap_sync.sync_user_from_ldap ('rcase@ds1.internal')
        self.ldap_sync.sync_user_to_ldap ('rcase@ds1.internal')
        dn = 'CN=Roman Case,OU=internal'
        new_department = self.ldap_modify_result [dn]['department'][0][1][0]
        self.assertEqual (new_department, department_temp_name)

        # sync department from vie_user
        department_temp_name = 'dep_override_2'
        self.ldap_sync.sync_user_to_ldap ('jdoe@ds1.internal')
        dn = 'CN=Jane Doe,OU=external'
        self.assertNotIn ('department', self.ldap_modify_result [dn])
        self.db.user.set \
            (self.testuser104, department_temp = department_temp_name)
        self.ldap_sync.sync_user_from_ldap ('jdoe@ds1.internal')
        self.ldap_sync.sync_user_to_ldap ('jdoe@ds1.internal')
        new_department = self.ldap_modify_result [dn]['department'][0][1][0]
        self.assertEqual (new_department, department_temp_name)
    # end test_sync_department

    def test_sync_company (self) :
        self.setup_ldap ()
        self.ldap_sync.sync_user_from_ldap ('rcase@ds1.internal')
        self.ldap_sync.sync_user_to_ldap ('rcase@ds1.internal')
        dn = 'CN=Roman Case,OU=internal'
        new_company = self.ldap_modify_result [dn]['company'][0][1][0]
        self.assertEqual \
            (new_company, self.db.org_location.get (self.org_location1, 'name'))

        # change org_location name
        new_org_location = 'new_org_location'
        self.db.org_location.set (self.org_location1, name = new_org_location)
        self.ldap_sync.sync_user_from_ldap ('rcase@ds1.internal')
        self.ldap_sync.sync_user_to_ldap ('rcase@ds1.internal')
        new_company = self.ldap_modify_result [dn]['company'][0][1][0]
        self.assertEqual (new_company, new_org_location)
    # end test_sync_company

    def test_sync_sap_cc (self) :
        self.setup_ldap ()
        self.sap_cc1 = self.db.sap_cc.create \
            ( name = 'cc_test_name'
            , description = 'cc_test_description'
            )
        self.db.user_dynamic.set (self.user_dynamic3_1, sap_cc = self.sap_cc1)
        self.ldap_sync.sync_user_from_ldap ('rcase@ds1.internal')
        self.ldap_sync.sync_user_to_ldap ('rcase@ds1.internal')
        dn = 'CN=Roman Case,OU=internal'
        new_extAttr3 = self.ldap_modify_result \
            [dn]['extensionAttribute3'][0][1][0]
        new_extAttr4 = self.ldap_modify_result \
            [dn]['extensionAttribute4'][0][1][0]
        self.assertEqual \
            (new_extAttr3, self.db.sap_cc.get (self.sap_cc1, 'name'))
        self.assertEqual \
            (new_extAttr4, self.db.sap_cc.get (self.sap_cc1, 'description'))

        # change sap_cc name
        new_sap_cc_name = 'new_org_sap_cc_name'
        self.db.sap_cc.set (self.sap_cc1, name = new_sap_cc_name)
        self.ldap_sync.sync_user_from_ldap ('rcase@ds1.internal')
        self.ldap_sync.sync_user_to_ldap ('rcase@ds1.internal')
        new_extAttr3 = self.ldap_modify_result \
            [dn]['extensionAttribute3'][0][1][0]
        self.assertEqual \
            (new_extAttr3, self.db.sap_cc.get (self.sap_cc1, 'name'))
    # end test_sync_sap_cc

    def test_position_text_sync (self) :
        self.setup_ldap ()
        position = 'Developer'
        self.db.user.set (self.testuser3, position_text = position)
        self.ldap_sync.sync_user_from_ldap ('rcase@ds1.internal')
        self.ldap_sync.sync_user_to_ldap ('rcase@ds1.internal')
        dn = 'CN=Roman Case,OU=internal'
        new_position = self.ldap_modify_result [dn]['title'][0][1][0]
        self.assertEqual (new_position, position)
    # end test_position_text_sync

    def test_sync_attributes_not_directly_updating_vie_user (self) :
        self.setup_ldap ()
        intname = 'jdoe@ds1.internal'
        self.ldap_sync.sync_user_to_ldap   (intname)
        self.ldap_sync.sync_user_from_ldap (intname)

        # change external user, supervisor not synced directly
        self.db.user.set (self.testuser104, supervisor = self.testuser105)
        self.ldap_sync.sync_user_to_ldap ('jdoe@ds1.internal')
        dn    = 'CN=Jane Doe,OU=external'
        newdn = 'CN=Julia Doe,OU=external'
        new_supervisor = self.ldap_modify_result [dn]['manager'][0][1][0]
        self.assertEqual (new_supervisor, 'CN=Vincent Super,OU=external')
        supervisor_vie_user = self.db.user.get (self.testuser4, 'supervisor')
        # no supervisor set yet -> None
        self.assertIsNone (supervisor_vie_user)

        # copy from class to not modify globally
        self.mock_users_by_username = copy.deepcopy \
            (self.mock_users_by_username)
        extname = 'jane.doe@ext1.internal'
        self.mock_users_by_username [intname][1]['manager'] = LDAP_Property \
            (new_supervisor)
        self.ldap_sync.sync_user_from_ldap (intname)
        supervisor_vie_user = self.db.user.get (self.testuser4, 'supervisor')
        self.assertEqual (supervisor_vie_user, self.testuser5)

        # change external user, firstname
        new_firstname = 'Julia'
        self.db.user.set (self.testuser104, firstname = new_firstname)

        # Will not be changed because no dyn user exists
        self.log.warn = self.mock_log
        self.ldap_sync.sync_user_to_ldap (intname)
        msg = 'Not syncing "realname"->"cn": no valid dyn. user'
        self.assertTrue (self.messages [0][0].startswith (msg))
        self.assertTrue (newdn not in self.ldap_modify_result)
        # But the firstname has been changed:
        new_givenname = self.ldap_modify_result [dn]['givenname'][0][1][0]
        self.assertEqual (new_givenname, new_firstname)

        # Create *invalid* (valid_to in the past) user_dynamic
        ud = self.db.user_dynamic.create \
            ( user            = self.testuser104
            , org_location    = self.org_location1
            , valid_from      = Date (str ('2021-01-01'))
            , valid_to        = Date (str ('2021-01-02'))
            , vacation_yearly = 25
            )

        # Will not be changed because no *valid* dyn user exists
        self.messages = []
        self.ldap_sync.sync_user_to_ldap (intname)
        self.assertTrue (self.messages [0][0].startswith (msg))
        self.assertTrue (newdn not in self.ldap_modify_result)
        # Verify that company contains a '*' due to invalid dynamic user
        newcomp = self.ldap_modify_result [dn]['company'][0][1][0]
        self.assertEqual (newcomp, '*testorglocation1')
        # And the firstname has been changed again:
        new_givenname = self.ldap_modify_result [dn]['givenname'][0][1][0]
        self.assertEqual (new_givenname, new_firstname)

        # Now make dynuser valid
        self.db.user_dynamic.set (ud, valid_to = None)
        self.ldap_sync.sync_user_to_ldap (intname)
        new_givenname = self.ldap_modify_result [newdn]['givenname'][0][1][0]
        self.assertEqual (new_givenname, new_firstname)
        firstname_vie_user = self.db.user.get (self.testuser4, 'firstname')
        self.assertEqual (firstname_vie_user, new_firstname)
    # end test_sync_attributes_not_directly_updating_vie_user

    def test_pic_convert_no_resize (self) :
        # Although the original pic is > 15k in size it will be smaller
        # than the 9k limit after conversion to JPEG.
        self.setup_ldap ()
        self.set_testuser1_testpic ()
        self.ldap_sync.sync_user_to_ldap ('testuser1@ds1.internal')
        newdn = 'CN=Test User,OU=internal'
        self.assertEqual \
            (self.ldap_modify_result.keys (), [newdn])
        d = self.ldap_modify_result [newdn]
        self.assertEqual (len (d), 8)
        pic = d ['thumbnailPhoto'][0][1][0]
        self.assertEqual (len (pic), 6034)
        # compute md5sum over synced picture to assert that the picture
        # conversion is stable and produces same result every time.
        # Otherwise we would produce lots of ldap changes!
        # This *may* change for different versions of PIL.
        m = md5 (pic)
        self.assertEqual (m.hexdigest (), 'c3b3e3bd46d5c7e9c82b71e1d92ad1a1')
    # end def test_pic_convert_no_resize

    def test_pic_convert_with_resize (self) :
        # Although the original pic is > 15k in size it will be smaller
        # than the 9k limit after conversion to JPEG. So we need to set
        # the limit lower to trigger the resizing mechanism
        self.setup_ldap ()
        self.set_testuser1_testpic ()
        self.db.config.ext ['LIMIT_PICTURE_SYNC_SIZE'] = '5000'
        self.ldap_sync.sync_user_to_ldap ('testuser1@ds1.internal')
        newdn = 'CN=Test User,OU=internal'
        self.assertEqual \
            (self.ldap_modify_result.keys (), [newdn])
        d = self.ldap_modify_result [newdn]
        self.assertEqual (len (d), 8)
        pic = d ['thumbnailPhoto'][0][1][0]
        self.assertEqual (len (pic), 4663)
        # compute md5sum over synced picture to assert that the picture
        # conversion is stable and produces same result every time.
        # Otherwise we would produce lots of ldap changes!
        # This *may* change for different versions of PIL.
        m = md5 (pic)
        self.assertEqual (m.hexdigest (), '6d339cc744579e0349da05c78a2f1026')
    # end def test_pic_convert_with_resize

# end class Test_Case_LDAP_Sync

def test_suite () :
    suite = unittest.TestSuite ()
    suite.addTest (unittest.makeSuite (Test_Case_LDAP_Sync))
    return suite
# end def test_suite
