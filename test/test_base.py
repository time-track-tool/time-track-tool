# Copyright (C) 2010-23 Ralf Schlatterbeck. All rights reserved
# Reichergasse 131, A-3411 Weidling
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

import errno
import os
import shutil
import sys
import unittest
import logging
import csv
import re
from io import BytesIO
# For monkey-patching:
import inspect
import ast
import pytest

from . import user1_time, user2_time, user3_time, user4_time, user5_time
from . import user6_time, user7_time, user8_time, user10_time, user11_time
from . import user12_time, user13_time, user14_time, user15_19_vac, user16_leave
from . import user17_time, user18_time, user20_time, user21_time, user22_time
from . import user23_time, user24_time, user25_time, user26_time, user27_time

from operator     import mul
from email.parser import Parser
from mailbox      import mbox
from base64       import b64decode
from copy         import deepcopy

from roundup.anypy.strings import StringIO
from roundup.test          import memorydb
from roundup               import backends
# Inject memorydb
backends.memorydb = memorydb
from roundup               import configuration
from roundup.exceptions    import Reject
from roundup.i18n          import get_translation

Option = configuration.Option


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

from .propl_abo     import properties as properties_abo
from .propl_adr     import properties as properties_adr
from .propl_erp     import properties as properties_erp
from .propl_full    import properties as properties_full
from .propl_itadr   import properties as properties_itadr
from .propl_it      import properties as properties_it
from .propl_kvats   import properties as properties_kvats
from .propl_lielas  import properties as properties_lielas
from .propl_pr      import properties as properties_pr
from .propl_sfull   import properties as properties_sfull
from .propl_track   import properties as properties_track
from .propl_tt      import properties as properties_time

from .sec_abo       import security as security_abo
from .sec_adr       import security as security_adr
from .sec_erp       import security as security_erp
from .sec_full      import security as security_full
from .sec_itadr     import security as security_itadr
from .sec_it        import security as security_it
from .sec_kvats     import security as security_kvats
from .sec_lielas    import security as security_lielas
from .sec_pr        import security as security_pr
from .sec_sfull     import security as security_sfull
from .sec_track     import security as security_track
from .sec_tt        import security as security_time

from .search_abo    import properties as sec_search_abo
from .search_adr    import properties as sec_search_adr
from .search_erp    import properties as sec_search_erp
from .search_full   import properties as sec_search_full
from .search_itadr  import properties as sec_search_itadr
from .search_it     import properties as sec_search_it
from .search_kvats  import properties as sec_search_kvats
from .search_lielas import properties as sec_search_lielas
from .search_pr     import properties as sec_search_pr
from .search_sfull  import properties as sec_search_sfull
from .search_track  import properties as sec_search_track
from .search_tt     import properties as sec_search_time

from .trans_abo     import transprop_perms as transprop_abo
from .trans_adr     import transprop_perms as transprop_adr
from .trans_erp     import transprop_perms as transprop_erp
from .trans_full    import transprop_perms as transprop_full
from .trans_itadr   import transprop_perms as transprop_itadr
from .trans_kvats   import transprop_perms as transprop_kvats
from .trans_lielas  import transprop_perms as transprop_lielas
from .trans_pr      import transprop_perms as transprop_pr
from .trans_sfull   import transprop_perms as transprop_sfull
from .trans_track   import transprop_perms as transprop_track
from .trans_tt      import transprop_perms as transprop_time

from .trans_search  import classdict  as trans_classprops

from roundup       import instance, configuration, init, password, date
from roundup.cgi   import templating
sys.path.insert (0, os.path.abspath ('lib'))
sys.path.insert (0, os.path.abspath ('extensions'))

import common
import summary
import user_dynamic
import vacation
from vac import eoy_vacation

header_regex = re.compile (r'\s*\n')
def header_decode (h) :
    return header_regex.sub ('', h)
# end def header_decode

class _Test_Base :
    count = 0
    db = None
    roles = ['admin']
    schemafile = None
    maxDiff = None
    backend = 'memorydb'
    allroles = dict.fromkeys \
        (('abo'
        , 'abo+invoice'
        , 'admin'
        , 'adr_readonly'
        , 'anonymous'
        , 'board'
        , 'cc-permission'
        , 'ciso'
        , 'contact'
        , 'controlling'
        , 'discount'
        , 'doc_admin'
        , 'dom-user-edit-facility'
        , 'dom-user-edit-gtt'
        , 'dom-user-edit-hr'
        , 'dom-user-edit-office'
        , 'external'
        , 'facility'
        , 'finance'
        , 'functional-role'
        , 'guest'
        , 'hr'
        , 'hr-approval'
        , 'hr-leave-approval'
        , 'hr-org-location'
        , 'hr-vacation'
        , 'invoice'
        , 'issue_admin'
        , 'it'
        , 'it-approval'
        , 'ituser'
        , 'itview'
        , 'kpm-admin'
        , 'letter'
        , 'logger'
        , 'measurement-approval'
        , 'msgedit'
        , 'msgsync'
        , 'nosy'
        , 'office'
        , 'organisation'
        , 'pbx'
        , 'pgp'
        , 'pr-view'
        , 'procure-approval'
        , 'procurement'
        , 'procurement-admin'
        , 'product'
        , 'project'
        , 'project_view'
        , 'quality'
        , 'readonly-user'
        , 'sec-incident-nosy'
        , 'sec-incident-responsible'
        , 'staff-report'
        , 'subcontract'
        , 'subcontract-org'
        , 'sub-login'
        , 'summary_view'
        , 'supportadmin'
        , 'time-report'
        , 'training-approval'
        , 'type'
        , 'user'
        , 'user_view'
        , 'vacation-report'
        ))

    def setup_tracker (self, backend = None) :
        """ Install and initialize tracker in dirname, return tracker instance.
            If directory exists, it is wiped out before the operation.
        """
        self.__class__.count += 1
        self.schemafile = self.schemafile or self.schemaname
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
        config.TRACKER_LANGUAGE = 'en'
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
        self.tracker.i18n = get_translation \
            (tracker_home = tracker.tracker_home)
    # end def setup_tracker

    def setUp (self) :
        self.log           = logging.getLogger ('roundup.test')
        self.properties    = globals () ['properties_' + self.schemaname]
        self.security_desc = globals () ['security_'   + self.schemaname]
        self.search_desc   = globals () ['sec_search_' + self.schemaname]
        self.setup_tracker ()
    # end def setUp

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

class _Test_Case (_Test_Base) :
    def test_0_roles (self) :
        self.log.debug ('test_0_roles')
        self.db = self.tracker.open ('admin')
        roles = list (sorted (self.db.security.role))
        self.assertEqual (roles, self.roles)
        for r in roles :
            self.assertEqual (r in self.allroles, True)
    # end def test_0_roles

    def test_1_schema (self) :
        self.log.debug ('test_1_schema')
        self.db = self.tracker.open ('admin')
        classnames = sorted (self.db.getclasses ())
        for (cl, props), cls in zip (self.properties, classnames) :
            self.assertEqual (cl, cls)
            clprops = sorted (list (self.db.getclass (cls).properties))
            self.assertEqual (props, clprops)
    # end def test_1_schema

    def test_2_security (self) :
        self.log.debug ('test_2_security')
        self.db = self.tracker.open ('admin')
        secdesc = self.security_desc.split ('\n')
        sd2     = []
        # sorting: python dicts are no longer stable from call to call
        for x in secdesc :
            if '[' in x :
                x0, x1 =  x.split ('[', 1)
                x1, x2 = x1.split (']', 1)
                x1 = ', '.join (sorted (x1.split (', ')))
                x = x0 + '[' + x1 + ']' + x2
            if '": (' in x :
                x0, x1 =  x.split ('": (', 1)
                x1, x2 = x1.split (') only', 1)
                x1 = ', '.join (sorted (x1.split (', ')))
                x = x0 + '": (' + x1 + ') only' + x2
            sd2.append (x)
        secdesc = sd2
        s = []
        s.append (secdesc [0])
        s.append (secdesc [1])
        roles = sorted (list (self.db.security.role.items ()))
        for rolename, role in roles :
            s.append ('Role "%(name)s":' % role.__dict__)
            perms = []
            for permission in role.permissions :
                d = permission.__dict__
                if permission.klass :
                    if permission.properties :
                        p = { 'properties'
                            : type (d ['properties'])
                                   (sorted (d ['properties']))
                            }
                        perms.append \
                            ( ' %(description)s (%(name)s for "%(klass)s"' %d
                            + ': %(properties)s only)' % p
                            )
                    else :
                        perms.append \
                            (' %(description)s (%(name)s for "%(klass)s" only)'
                            % d
                            )
                else:
                    perms.append (' %(description)s (%(name)s)' % d)
            s.extend (sorted (list (set (perms))))
        lr1 = lr2 = None
        l1 = len (secdesc)
        l2 = len (s)
        if l1 < l2 :
            for k in range (l2 - l1) :
                secdesc.append ('')
        if l2 < l1 :
            for k in range (l1 - l2) :
                s.append ('')
        for s1, s2 in zip (secdesc, s) :
            if s1.startswith ('Role') :
                lr1 = s1
            if s2.startswith ('Role') :
                lr2 = s2
            self.assertEqual ((lr1, s1), (lr2, s2))
    # end def test_2_security

    def test_3_search (self) :
        self.log.debug ('test_3_search')
        self.db = self.tracker.open ('admin')
        self.create_test_users ()
        classnames = sorted (self.db.getclasses ())
        self.assertEqual (len (classnames), len (self.search_desc))
        for (cl, props), cls in zip (self.search_desc, classnames) :
            self.assertEqual (cl, cls)
            clprops = []
            for p in sorted (self.db.getclass (cls).properties) :
                users = []
                for user in sorted (self.users) :
                    uid = self.users [user]
                    if self.db.security.hasSearchPermission (uid, cl, p) :
                        users.append (user)
                clprops.append ((p, users))
            self.assertEqual ((cl, props), (cl, clprops))
    # end def test_3_search

    transprop_perms = []
    def test_4_transprops (self) :
        self.log.debug ('test_4_transprops')
        self.db = self.tracker.open ('admin')
        self.create_test_users ()
        perms = []
        for cl in sorted (trans_classprops) :
            props = trans_classprops [cl]
            if cl not in self.db.classes :
                continue
            klass = self.db.classes [cl]
            for p in sorted (props) :
                ps = p.split ('.')
                if ps [0] not in klass.getprops () :
                    continue
                pusers = []
                for user in sorted (self.users) :
                    uid = self.users [user]
                    if self.db.security.hasSearchPermission (uid, cl, p) :
                        pusers.append (user)
                perms.append (('.'.join ((cl, p)), pusers))
        for a, b in zip (self.transprop_perms, perms):
            self.assertEqual (a, b)
        self.assertEqual (len (self.transprop_perms), len (perms))
    # end def test_4_transprops

    def create_test_users (self) :
        nouserroles = dict.fromkeys \
            (( 'adr_readonly'
            ,  'external'
            ,  'guest'
            ,  'hr-org-location'
            ,  'ituser'
            ,  'logger'
            ,  'nosy'
            ,  'readonly-user'
            ,  'staff-report'
            ,  'sub-login'
            ,  'user'
            ))
        self.users = {'admin' : '1', 'anonymous' : '2'}
        for u in self.allroles :
            if u in self.users :
                continue
            roles = u.split ('+')
            if u not in nouserroles :
                roles.append ('user')
            # wired and :-)
            r_ok = min (r in self.db.security.role for r in roles)
            if not r_ok :
                continue
            params = dict \
                ( username = u
                , roles    = ','.join (roles)
                )
            if 'firstname' in self.db.user.properties :
                params ['firstname'] = params ['lastname'] = u
            try :
                status = self.db.user_status.lookup ('system')
                params ['status'] = status
            except ValueError :
                pass
            try :
                self.users [u] = self.db.user.create (**params)
            except ValueError :
                self.users [u] = self.db.user.lookup (u)
    # end def create_test_users
# end class _Test_Case

class _Test_Base_Summary :
    def setup_db (self) :
        self.db = self.tracker.open ('admin')
        self.db.overtime_period.create \
            ( name   = 'yearly/weekly'
            , months = 12
            , order  = 1.5
            , weekly = True
            )
        self.org = self.db.organisation.create \
            ( name        = 'The Org'
            , description = 'A Test Organisation'
            , mail_domain = 'example.com'
            , valid_from  = date.Date ('2004-01-01')
            )
        self.loc = self.db.location.create \
            ( name    = 'Vienna'
            , country = 'Austria'
            , address = 'Vienna, Austria'
            )
        self.olo = self.db.org_location.create \
            ( name                = 'The Org, Vienna'
            , location            = self.loc
            , organisation        = self.org
            , vacation_legal_year = False
            , vacation_yearly     = 25.0
            , do_leave_process    = True
            , vac_aliq            = '1'
            )
        self.olo2 = self.db.org_location.create \
            ( name                = 'Another Org, Vienna'
            , location            = self.loc
            , organisation        = self.org
            , vacation_legal_year = False
            , vacation_yearly     = 25.0
            , do_leave_process    = True
            , vac_aliq            = '1'
            )
        roles = 'User,Nosy,HR,controlling,project,ITView,IT'.split (',')
        roles.append ('HR-leave-approval')
        roles.append ('User_View')
        sec   = self.db.security
        roles = ','.join (x for x in roles if x.lower () in sec.role)
        self.username0 = 'testuser0'
        self.user0 = self.db.user.create \
            ( username     = self.username0
            , firstname    = 'Test'
            , lastname     = 'User0'
            , roles        = roles
            )
        user_dynamic.user_create_magic (self.db, self.user0, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user0
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        cts  = self.db.user.get (self.user0, 'contacts')
        cmin = 0xFFFF
        mail = self.db.uc_type.lookup ('Email')
        m    = None
        for ctid in cts :
            ct = self.db.user_contact.getnode (ctid)
            if ct.contact_type == mail and ct.order < cmin :
                cmin = ct.order
                m    = ct.id
        self.db.user_contact.set (m, contact = 'user0@test.test')
        self.username1 = 'testuser1'
        self.user1 = self.db.user.create \
            ( username     = self.username1
            , firstname    = 'Test'
            , lastname     = 'User1'
            )
        user_dynamic.user_create_magic (self.db, self.user1, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user1
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        cts  = self.db.user.get (self.user1, 'contacts')
        cmin = 0xFFFF
        mail = self.db.uc_type.lookup ('Email')
        m    = None
        for ctid in cts :
            ct = self.db.user_contact.getnode (ctid)
            if ct.contact_type == mail and ct.order < cmin :
                cmin = ct.order
                m    = ct.id
        self.db.user_contact.set (m, contact = 'user1@test.test')
        # Small change of race condition if running this test at
        # midnight, think we can live with this.
        now = date.Date ('.')
        self.month, self.day = now.get_tuple () [1:3]
        self.db.org_location.set (self.olo, vacation_legal_year = True)
        self.username2 = 'testuser2'
        self.user2 = self.db.user.create \
            ( username     = self.username2
            , firstname    = 'Test'
            , lastname     = 'User2'
            , supervisor   = self.user1
            )
        user_dynamic.user_create_magic (self.db, self.user2, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user2
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        # create initial dyn_user record for each user
        # others will follow during tests
        ud = self.db.user_dynamic.filter (None, dict (user = self.user1))
        self.assertEqual (len (ud), 1)
        self.db.user_dynamic.set \
            ( ud [0]
            , valid_from      = date.Date ('2005-09-01')
            , booking_allowed = False
            , vacation_yearly = 25.0
            , all_in          = True
            , hours_mon       = 7.75
            , hours_tue       = 7.75
            , hours_wed       = 7.75
            , hours_thu       = 7.75
            , hours_fri       = 7.5
            , vacation_month  = 9
            , vacation_day    = 1
            , max_flexitime   = 5
            )
        self.db.user_dynamic.create \
            ( user              = self.user1
            , valid_from        = date.Date ('2005-10-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , daily_worktime    = 0.0
            , org_location      = self.olo
            , supp_weekly_hours = 40
            , overtime_period   = self.db.overtime_period.lookup ('week')
            )
        self.assertEqual \
            ( self.db.user_dynamic.get (ud [0], 'valid_to')
            , date.Date ('2005-10-01')
            )
        ud = self.db.user_dynamic.filter (None, dict (user = self.user2))
        self.assertEqual (len (ud), 1)
        self.db.user_dynamic.set \
            ( ud [0]
            , valid_from       = date.Date ('2008-11-03')
            , booking_allowed  = True
            , vacation_yearly  = 25.0
            , all_in           = True
            , hours_mon        = 7.75
            , hours_tue        = 7.75
            , hours_wed        = 7.75
            , hours_thu        = 7.75
            , hours_fri        = 7.5
            , supp_per_period  = 40
            , additional_hours = 40
            , max_flexitime    = 5
            )
        ud = self.db.user_dynamic.filter (None, dict (user = self.user0))
        self.assertEqual (len (ud), 1)
        self.db.user_dynamic.set \
            ( ud [0]
            , valid_from     = date.Date ('2013-02-02')
            , vacation_day   = 2
            , vacation_month = 2
            )
        f = self.db.daily_record_freeze.create \
            ( user           = self.user1
            , balance        = 0.0
            , achieved_hours = 0.0
            , frozen         = True
            , date           = date.Date ('2005-12-31')
            )
        f = self.db.daily_record_freeze.getnode (f)
        self.assertEqual (f.balance,        0.0)
        self.assertEqual (f.achieved_hours, 0.0)
        self.assertEqual (f.validity_date,  date.Date ('2005-12-25'))
        wl_off    = self.db.work_location.lookup ('off')
        wl_trav   = self.db.work_location.lookup ('off-site/trav.')
        stat_open = self.db.time_project_status.lookup ('Open')
        self.ccg = self.db.cost_center_group.create (name = 'CCG')
        self.cc = self.db.cost_center.create \
            ( name               = 'CC'
            , cost_center_group  = self.ccg
            , status             = self.db.cost_center_status.lookup ('Open')
            )
        self.holiday_tp = self.db.time_project.create \
            ( name = 'Public Holiday'
            , work_location      = wl_off
            , op_project         = False
            , no_overtime        = True
            , no_overtime_day    = False
            , overtime_reduction = True
            , is_public_holiday  = True
            , responsible        = '1'
            , status             = stat_open
            , cost_center        = self.cc
            , approval_required  = False
            , approval_hr        = False
            , is_vacation        = False
            )
        self.unpaid_tp = self.db.time_project.create \
            ( name = 'Leave'
            , work_location      = wl_off
            , op_project         = False
            , no_overtime        = True
            , no_overtime_day    = True
            , overtime_reduction = True
            , responsible        = '1'
            , status             = stat_open
            , cost_center        = self.cc
            , approval_required  = True
            , approval_hr        = True
            , is_vacation        = False
            )
        self.travel_tp = self.db.time_project.create \
            ( name = 'Travel'
            , work_location      = wl_trav
            , op_project         = False
            , responsible        = '1'
            , status             = stat_open
            , cost_center        = self.cc
            , approval_required  = False
            , approval_hr        = False
            , is_vacation        = False
            )
        self.normal_tp = self.db.time_project.create \
            ( name = 'A Project'
            , op_project         = True
            , responsible        = self.user1
            , status             = stat_open
            , organisation       = self.org
            , cost_center        = self.cc
            , approval_required  = False
            , approval_hr        = False
            , is_vacation        = False
            )
        self.vacation_tp = self.db.time_project.create \
            ( name = 'Vacation'
            , op_project         = False
            , responsible        = self.user1
            , status             = stat_open
            , organisation       = self.org
            , cost_center        = self.cc
            , no_overtime        = True
            , no_overtime_day    = False
            , overtime_reduction = True
            , approval_required  = True
            , approval_hr        = False
            , is_vacation        = True
            )
        self.flexi_tp = self.db.time_project.create \
            ( name = 'Flexi'
            , op_project         = False
            , responsible        = self.user1
            , status             = stat_open
            , organisation       = self.org
            , cost_center        = self.cc
            , max_hours          = 0
            , no_overtime        = True
            , no_overtime_day    = True
            , approval_required  = True
            , approval_hr        = False
            , is_vacation        = False
            )
        self.special_tp = self.db.time_project.create \
            ( name = 'Special Leave'
            , work_location      = wl_off
            , op_project         = False
            , no_overtime        = True
            , no_overtime_day    = True
            , overtime_reduction = True
            , responsible        = '1'
            , status             = stat_open
            , cost_center        = self.cc
            , approval_required  = True
            , approval_hr        = False
            , is_vacation        = False
            , is_special_leave   = True
            )
        self.nursing_tp = self.db.time_project.create \
            ( name = 'Nursing-Leave'
            , work_location      = wl_off
            , op_project         = False
            , no_overtime        = True
            , no_overtime_day    = True
            , overtime_reduction = True
            , responsible        = '1'
            , status             = stat_open
            , cost_center        = self.cc
            , approval_required  = True
            , approval_hr        = True
            , is_vacation        = False
            )
        self.sick_tp = self.db.time_project.create \
            ( name = 'Sick-Leave'
            , work_location      = wl_off
            , op_project         = False
            , no_overtime        = True
            , no_overtime_day    = True
            , overtime_reduction = True
            , responsible        = '1'
            , status             = stat_open
            , cost_center        = self.cc
            , approval_required  = True
            , approval_hr        = True
            , is_vacation        = False
            )
        self.medical_tp = self.db.time_project.create \
            ( name = 'Medical-Consultation'
            , work_location      = wl_off
            , op_project         = False
            , no_overtime        = True
            , no_overtime_day    = True
            , overtime_reduction = True
            , responsible        = '1'
            , status             = stat_open
            , cost_center        = self.cc
            , approval_required  = True
            , approval_hr        = True
            , is_vacation        = False
            )
        self.holiday_wp = self.db.time_wp.create \
            ( name               = 'Holiday'
            , project            = self.holiday_tp
            , time_start         = date.Date ('2004-01-01')
            , durations_allowed  = True
            , responsible        = '1'
            , bookers            = [self.user1, self.user2]
            , cost_center        = self.cc
            )
        self.unpaid_wp = self.db.time_wp.create \
            ( name               = 'Unpaid'
            , project            = self.unpaid_tp
            , time_start         = date.Date ('2004-01-01')
            , durations_allowed  = True
            , responsible        = '1'
            , bookers            = [self.user1, self.user2]
            , cost_center        = self.cc
            )
        self.travel_wp = self.db.time_wp.create \
            ( name               = 'Travel'
            , project            = self.travel_tp
            , time_start         = date.Date ('2004-01-01')
            , responsible        = '1'
            , bookers            = [self.user1, self.user2]
            , cost_center        = self.cc
            )
        self.wps = []
        for i in range (40) :
            wp = self.db.time_wp.create \
                ( name               = 'Work Package %s' % i
                , project            = self.normal_tp
                , time_start         = date.Date ('2004-01-01')
                , responsible        = '1'
                , bookers            = [self.user1, self.user2]
                , cost_center        = self.cc
                )
            self.wps.append (wp)
        self.vacation_wp = self.db.time_wp.create \
            ( name               = 'Vacation'
            , project            = self.vacation_tp
            , time_start         = date.Date ('2004-01-01')
            , responsible        = '1'
            , bookers            = [self.user1, self.user2]
            , cost_center        = self.cc
            , durations_allowed  = True
            )
        self.assertEqual (self.vacation_wp, '44')
        self.flexi_wp = self.db.time_wp.create \
            ( name               = 'Flexi'
            , project            = self.flexi_tp
            , time_start         = date.Date ('2004-01-01')
            , responsible        = '1'
            , bookers            = [self.user1, self.user2]
            , cost_center        = self.cc
            , durations_allowed  = True
            )
        self.special_wp = self.db.time_wp.create \
            ( name               = 'Special'
            , project            = self.special_tp
            , time_start         = date.Date ('2004-01-01')
            , responsible        = '1'
            , bookers            = []
            , is_public          = True
            , cost_center        = self.cc
            , durations_allowed  = True
            )
        self.db.commit ()
        self.log.debug ("End of setup")
    # end def setup_db
# end class _Test_Base_Summary

class _Test_Case_Summary (_Test_Base_Summary, _Test_Case) :
    pass

class Test_Case_Support_Timetracker (_Test_Case, unittest.TestCase) :
    schemaname = 'sfull'
    roles = \
        [ 'admin', 'adr_readonly', 'anonymous', 'cc-permission', 'contact'
        , 'controlling' , 'doc_admin', 'facility', 'functional-role', 'hr'
        , 'hr-leave-approval', 'hr-org-location'
        , 'hr-vacation', 'issue_admin', 'it', 'itview'
        , 'msgedit', 'msgsync', 'nosy', 'office', 'organisation'
        , 'procurement', 'project'
        , 'project_view', 'sec-incident-nosy'
        , 'sec-incident-responsible', 'staff-report', 'sub-login'
        , 'summary_view' , 'supportadmin', 'time-report', 'type', 'user'
        , 'vacation-report'
        ]
    transprop_perms = transprop_sfull
# end class Test_Case_Support_Timetracker

class Test_Case_Timetracker (_Test_Case_Summary, unittest.TestCase) :
    schemaname = 'time'
    schemafile = 'time_ldap'
    roles = \
        [ 'admin', 'anonymous', 'cc-permission', 'controlling', 'doc_admin'
        , 'dom-user-edit-facility', 'dom-user-edit-gtt', 'dom-user-edit-hr'
        , 'dom-user-edit-office', 'facility', 'functional-role', 'hr'
        , 'hr-leave-approval', 'hr-org-location', 'hr-vacation', 'it', 'nosy'
        , 'office', 'organisation', 'pgp', 'procurement', 'project'
        , 'project_view', 'staff-report', 'sub-login', 'summary_view'
        , 'time-report', 'user', 'user_view', 'vacation-report'
        ]
    transprop_perms = transprop_time

    def check_user_perms (self, ad_domain) :
        roles    = 'User,Nosy'
        valid    = self.db.user_status.lookup ('valid')
        obsolete = self.db.user_status.lookup ('obsolete')
        # Now create a user
        u = self.db.user.create \
            ( username  = 'testuser'
            , firstname = 'Testuser'
            , lastname  = 'Usertestuser'
            , ad_domain = ad_domain
            )
        u_domain = 'testuser@' + ad_domain
        self.assertEqual (self.db.user.get (u, 'username'), u_domain)
        self.assertEqual (self.db.user.get (u, 'roles'), roles)
        self.assertEqual (self.db.user.get (u, 'status'), valid)
        self.assertEqual (self.db.user.get (u, 'ad_domain'), ad_domain)
        # Modify it
        self.db.user.set (u, lastname = 'Nocheintest')
        self.assertEqual (self.db.user.get (u, 'lastname'), 'Nocheintest')
        # Verify we cannot set ad_domain to wrong value
        self.assertRaises \
            (Reject, self.db.user.set, u, ad_domain = 'example.com')
        self.assertEqual (self.db.user.get (u, 'ad_domain'), ad_domain)
        # Verify we cannot set status to wrong value
        self.db.user.set (u, status = self.db.user_status.lookup ('system'))
        self.assertEqual (self.db.user.get (u, 'status'), valid)
        # Allow setting to obsolete
        self.db.user.set (u, status = obsolete)
        self.assertEqual (self.db.user.get (u, 'status'), obsolete)
        # Allow setting to valid again
        self.db.user.set (u, status = valid)
        self.assertEqual (self.db.user.get (u, 'status'), valid)
        # Try editing a different user
        self.assertRaises \
            (Reject, self.db.user.set, self.user2, status = obsolete)
        # Try editing a dynamic user record not belonging to our domain
        self.assertRaises \
            (Reject, self.db.user_dynamic.set, '1', vacation_yearly = 27)
        # Try creating a dynamic user record
        id = self.db.user_dynamic.create \
            ( org_location    = self.olo
            , vacation_yearly = 23
            , user            = u
            , valid_from      = date.Date ('.')
            )
        self.assertEqual (self.db.user_dynamic.get (id, 'vacation_yearly'), 23)
    # end def check_user_perms

    def test_domain_user_edit (self) :
        self.log.debug ('test_domain_user_edit')
        self.setup_db ()
        self.db.user.set (self.user1, roles = 'User,Nosy,Dom-User-Edit-GTT')
        ad_domain = 'some.test.domain'
        roles     = 'User,Nosy'
        valid     = self.db.user_status.lookup ('valid')
        obsolete  = self.db.user_status.lookup ('obsolete')
        dpid = self.db.domain_permission.create \
            ( ad_domain       = ad_domain
            , users           = [self.user1]
            , default_roles   = roles
            , timetracking_by = self.user2
            , clearance_by    = '1'
            , status          = valid
            )
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username1)
        self.check_user_perms (ad_domain)
        # Do *not* commit
        self.db.rollback ()
        self.db.close ()
        self.db = self.tracker.open ('admin')
        # Change permission to role-based and retry the whole test.
        self.db.domain_permission.set \
            (dpid, users = [], roles_enabled = 'Dom-User-Edit-GTT')
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username1)
        self.check_user_perms (ad_domain)
    # end def test_domain_user_edit

    def setup_user11 (self) :
        self.username11 = 'testuser11'
        self.user11 = self.db.user.create \
            ( username     = self.username11
            , firstname    = 'Nummer11'
            , lastname     = 'User11'
            )
        user_dynamic.user_create_magic (self.db, self.user11, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user11
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        # create initial dyn_user record for user
        ud = self.db.user_dynamic.filter (None, dict (user = self.user11))
        self.assertEqual (len (ud), 1)
        ud = self.db.user_dynamic.getnode (ud [0])
        week = self.db.overtime_period.lookup ('week')
        self.db.user_dynamic.set \
            ( ud.id
            , valid_from        = date.Date ('2011-12-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_weekly_hours = 45.0
            , additional_hours  = 40.0
            , overtime_period   = week
            )
        self.db.product_family.create \
            (name = 'Family test',  responsible = self.user11)
        self.db.product_family.create \
            (name = 'Family xyzzy', responsible = self.user11)
        self.db.reporting_group.create \
            (name = 'RG test',  responsible = self.user11)
        self.db.reporting_group.create \
            (name = 'RG xyzzy', responsible = self.user11)
        self.db.time_project.set \
            ( '4'
            , reporting_group = ['1']
            , product_family  = ['1']
            , project_type    = '2'
            , organisation    = '1'
            )
        self.db.time_project.set \
            ( '3'
            , reporting_group = ['2']
            , product_family  = ['2']
            , project_type    = '4'
            , organisation    = '1'
            )
        self.db.commit ()
    # end def setup_user11

    def test_user11_sap_cc (self) :
        self.log.debug ('test_user11_sap_cc')
        self.setup_db ()
        self.setup_user11 ()
        sap_cc = self.db.sap_cc.create (name = "SAP-1")
        ud = self.db.user_dynamic.filter (None, dict (user = self.user11))
        self.assertEqual (len (ud), 1)
        ud = self.db.user_dynamic.getnode (ud [0])
        week = self.db.overtime_period.lookup ('week')
        self.db.user_dynamic.set \
            ( ud.id
            , sap_cc = sap_cc
            )
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username11)
        user11_time.import_data_11 (self.db, self.user11)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'sap_cc'       : [sap_cc]
             , 'date'         : '2013-06-01;2013-06-30'
             , 'summary_type' : ['2', '4']
             }
        cols = \
            [ 'time_wp'
            , 'user'
            , 'summary'
            , 'sap_cc'
            ]

        class r :
            filterspec = fs
            columns = cols
            sort = None
            group = None
            classname = 'summary_report'

        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     10)
        self.assertEqual (len (lines [0]),  5)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Time Period')
        self.assertEqual (lines [0][2], 'testuser11')
        self.assertEqual (lines [0][3], 'SAP-1')
        self.assertEqual (lines [0][4], 'Sum')
        self.assertEqual (lines [1][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [1][1], 'WW 23/2013')
        self.assertEqual (lines [1][2], '5.00')
        self.assertEqual (lines [1][3], '5.00')
        self.assertEqual (lines [1][4], '5.00')
        self.assertEqual (lines [2][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [2][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][2], '5.00')
        self.assertEqual (lines [2][3], '5.00')
        self.assertEqual (lines [2][4], '5.00')
        self.assertEqual (lines [3][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [3][1], 'WW 24/2013')
        self.assertEqual (lines [3][2], '1.00')
        self.assertEqual (lines [3][3], '1.00')
        self.assertEqual (lines [3][4], '1.00')
        self.assertEqual (lines [4][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [4][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [4][2], '1.00')
        self.assertEqual (lines [4][3], '1.00')
        self.assertEqual (lines [4][4], '1.00')
        self.assertEqual (lines [5][0], 'Work package Travel/Travel')
        self.assertEqual (lines [5][1], 'WW 24/2013')
        self.assertEqual (lines [5][2], '2.00')
        self.assertEqual (lines [5][3], '2.00')
        self.assertEqual (lines [5][4], '2.00')
        self.assertEqual (lines [6][0], 'Work package Travel/Travel')
        self.assertEqual (lines [6][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [6][2], '2.00')
        self.assertEqual (lines [6][3], '2.00')
        self.assertEqual (lines [6][4], '2.00')
        self.assertEqual (lines [7][0], 'Sum')
        self.assertEqual (lines [7][1], 'WW 23/2013')
        self.assertEqual (lines [7][2], '5.00')
        self.assertEqual (lines [7][3], '5.00')
        self.assertEqual (lines [7][4], '5.00')
        self.assertEqual (lines [8][0], 'Sum')
        self.assertEqual (lines [8][1], 'WW 24/2013')
        self.assertEqual (lines [8][2], '3.00')
        self.assertEqual (lines [8][3], '3.00')
        self.assertEqual (lines [8][4], '3.00')
        self.assertEqual (lines [9][0], 'Sum')
        self.assertEqual (lines [9][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [9][2], '8.00')
        self.assertEqual (lines [9][3], '8.00')
        self.assertEqual (lines [9][4], '8.00')

        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open ('admin')
        ud = self.db.user_dynamic.filter (None, dict (user = self.user11))
        ud = self.db.user_dynamic.getnode (ud [0])
        self.db.user_dynamic.set \
            ( ud.id
            , sap_cc = None
            )
        self.db.user_dynamic.create \
            ( user              = self.user11
            , org_location      = ud.org_location
            , valid_from        = date.Date ('2013-06-05')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_weekly_hours = 45.0
            , additional_hours  = 40.0
            , overtime_period   = week
            , sap_cc            = sap_cc
            )
        self.db.user_dynamic.create \
            ( user              = self.user11
            , org_location      = ud.org_location
            , valid_from        = date.Date ('2013-06-11')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_weekly_hours = 45.0
            , additional_hours  = 40.0
            , overtime_period   = week
            , sap_cc            = None
            )
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     5)
        self.assertEqual (len (lines [0]), 5)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Time Period')
        self.assertEqual (lines [0][2], 'testuser11')
        self.assertEqual (lines [0][3], 'SAP-1')
        self.assertEqual (lines [0][4], 'Sum')
        self.assertEqual (lines [1][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [1][1], 'WW 24/2013')
        self.assertEqual (lines [1][2], '1.00')
        self.assertEqual (lines [1][3], '1.00')
        self.assertEqual (lines [1][4], '1.00')
        self.assertEqual (lines [2][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [2][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][2], '1.00')
        self.assertEqual (lines [2][3], '1.00')
        self.assertEqual (lines [2][4], '1.00')
        self.assertEqual (lines [3][0], 'Sum')
        self.assertEqual (lines [3][1], 'WW 24/2013')
        self.assertEqual (lines [3][2], '1.00')
        self.assertEqual (lines [3][3], '1.00')
        self.assertEqual (lines [3][4], '1.00')
        self.assertEqual (lines [4][0], 'Sum')
        self.assertEqual (lines [4][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [4][2], '1.00')
        self.assertEqual (lines [4][3], '1.00')
        self.assertEqual (lines [4][4], '1.00')
    # end def test_user11_sap_cc

    def test_user11 (self) :
        self.log.debug ('test_user11')
        self.setup_db ()
        self.setup_user11 ()
        self.db.close ()
        self.db = self.tracker.open (self.username11)
        user11_time.import_data_11 (self.db, self.user11)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user'         : [self.user11]
             , 'date'         : '2013-06-01;2013-06-30'
             , 'summary_type' : ['2', '4']
             }
        cols = \
            [ 'product_family'
            , 'product_family.id'
            , 'project_type'
            , 'project_type.id'
            , 'reporting_group'
            , 'reporting_group.id'
            , 'time_wp'
            , 'user'
            , 'summary'
            ]

        class r :
            filterspec = fs
            columns = cols
            sort = None
            group = None
            classname = 'summary_report'

        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     10)
        self.assertEqual (len (lines [0]), 10)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Product family')
        self.assertEqual (lines [0][2], 'Project type')
        self.assertEqual (lines [0][3], 'Reporting group')
        self.assertEqual (lines [0][4], 'Product family Id')
        self.assertEqual (lines [0][5], 'Project type Id')
        self.assertEqual (lines [0][6], 'Reporting group Id')
        self.assertEqual (lines [0][7], 'Time Period')
        self.assertEqual (lines [0][8], 'testuser11')
        self.assertEqual (lines [0][9], 'Sum')
        self.assertEqual (lines [1][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [1][1], 'Family test')
        self.assertEqual (lines [1][2], 'Further Development')
        self.assertEqual (lines [1][3], 'RG test')
        self.assertEqual (lines [1][4], '1')
        self.assertEqual (lines [1][5], '2')
        self.assertEqual (lines [1][6], '1')
        self.assertEqual (lines [1][7], 'WW 23/2013')
        self.assertEqual (lines [1][8], '5.00')
        self.assertEqual (lines [1][9], '5.00')
        self.assertEqual (lines [2][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [2][1], 'Family test')
        self.assertEqual (lines [2][2], 'Further Development')
        self.assertEqual (lines [2][3], 'RG test')
        self.assertEqual (lines [2][4], '1')
        self.assertEqual (lines [2][5], '2')
        self.assertEqual (lines [2][6], '1')
        self.assertEqual (lines [2][7], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][8], '5.00')
        self.assertEqual (lines [2][9], '5.00')
        self.assertEqual (lines [3][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [3][1], '')
        self.assertEqual (lines [3][2], '')
        self.assertEqual (lines [3][3], '')
        self.assertEqual (lines [3][4], '')
        self.assertEqual (lines [3][5], '')
        self.assertEqual (lines [3][6], '')
        self.assertEqual (lines [3][7], 'WW 24/2013')
        self.assertEqual (lines [3][8], '1.00')
        self.assertEqual (lines [3][9], '1.00')
        self.assertEqual (lines [4][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [4][1], '')
        self.assertEqual (lines [4][2], '')
        self.assertEqual (lines [4][3], '')
        self.assertEqual (lines [4][4], '')
        self.assertEqual (lines [4][5], '')
        self.assertEqual (lines [4][6], '')
        self.assertEqual (lines [4][7], '2013-06-01;2013-06-30')
        self.assertEqual (lines [4][8], '1.00')
        self.assertEqual (lines [4][9], '1.00')
        self.assertEqual (lines [5][0], 'Work package Travel/Travel')
        self.assertEqual (lines [5][1], 'Family xyzzy')
        self.assertEqual (lines [5][2], 'Support')
        self.assertEqual (lines [5][3], 'RG xyzzy')
        self.assertEqual (lines [5][4], '2')
        self.assertEqual (lines [5][5], '4')
        self.assertEqual (lines [5][6], '2')
        self.assertEqual (lines [5][7], 'WW 24/2013')
        self.assertEqual (lines [5][8], '2.00')
        self.assertEqual (lines [5][9], '2.00')
        self.assertEqual (lines [6][0], 'Work package Travel/Travel')
        self.assertEqual (lines [6][1], 'Family xyzzy')
        self.assertEqual (lines [6][2], 'Support')
        self.assertEqual (lines [6][3], 'RG xyzzy')
        self.assertEqual (lines [6][4], '2')
        self.assertEqual (lines [6][5], '4')
        self.assertEqual (lines [6][6], '2')
        self.assertEqual (lines [6][7], '2013-06-01;2013-06-30')
        self.assertEqual (lines [6][8], '2.00')
        self.assertEqual (lines [6][9], '2.00')
        self.assertEqual (lines [7][0], 'Sum')
        self.assertEqual (lines [7][1], '')
        self.assertEqual (lines [7][2], '')
        self.assertEqual (lines [7][3], '')
        self.assertEqual (lines [7][4], '')
        self.assertEqual (lines [7][5], '')
        self.assertEqual (lines [7][6], '')
        self.assertEqual (lines [7][7], 'WW 23/2013')
        self.assertEqual (lines [7][8], '5.00')
        self.assertEqual (lines [7][9], '5.00')
        self.assertEqual (lines [8][0], 'Sum')
        self.assertEqual (lines [8][1], '')
        self.assertEqual (lines [8][2], '')
        self.assertEqual (lines [8][3], '')
        self.assertEqual (lines [8][4], '')
        self.assertEqual (lines [8][5], '')
        self.assertEqual (lines [8][6], '')
        self.assertEqual (lines [8][7], 'WW 24/2013')
        self.assertEqual (lines [8][8], '3.00')
        self.assertEqual (lines [8][9], '3.00')
        self.assertEqual (lines [9][0], 'Sum')
        self.assertEqual (lines [9][1], '')
        self.assertEqual (lines [9][2], '')
        self.assertEqual (lines [9][3], '')
        self.assertEqual (lines [9][4], '')
        self.assertEqual (lines [9][5], '')
        self.assertEqual (lines [9][6], '')
        self.assertEqual (lines [9][7], '2013-06-01;2013-06-30')
        self.assertEqual (lines [9][8], '8.00')
        self.assertEqual (lines [9][9], '8.00')

        # keep .id columns
        #   [ 'product_family.id'
        #   , 'project_type.id'
        #   , 'reporting_group.id'
        #   , 'time_wp'
        #   , 'user'
        #   , 'summary'
        #   ]
        del cols [4]
        del cols [2]
        del cols [0]
        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     10)
        self.assertEqual (len (lines [0]),  7)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Product family Id')
        self.assertEqual (lines [0][2], 'Project type Id')
        self.assertEqual (lines [0][3], 'Reporting group Id')
        self.assertEqual (lines [0][4], 'Time Period')
        self.assertEqual (lines [0][5], 'testuser11')
        self.assertEqual (lines [0][6], 'Sum')
        self.assertEqual (lines [1][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [1][1], '1')
        self.assertEqual (lines [1][2], '2')
        self.assertEqual (lines [1][3], '1')
        self.assertEqual (lines [1][4], 'WW 23/2013')
        self.assertEqual (lines [1][5], '5.00')
        self.assertEqual (lines [1][6], '5.00')
        self.assertEqual (lines [2][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [2][1], '1')
        self.assertEqual (lines [2][2], '2')
        self.assertEqual (lines [2][3], '1')
        self.assertEqual (lines [2][4], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][5], '5.00')
        self.assertEqual (lines [2][6], '5.00')
        self.assertEqual (lines [3][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [3][1], '')
        self.assertEqual (lines [3][2], '')
        self.assertEqual (lines [3][3], '')
        self.assertEqual (lines [3][4], 'WW 24/2013')
        self.assertEqual (lines [3][5], '1.00')
        self.assertEqual (lines [3][6], '1.00')
        self.assertEqual (lines [4][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [4][1], '')
        self.assertEqual (lines [4][2], '')
        self.assertEqual (lines [4][3], '')
        self.assertEqual (lines [4][4], '2013-06-01;2013-06-30')
        self.assertEqual (lines [4][5], '1.00')
        self.assertEqual (lines [4][6], '1.00')
        self.assertEqual (lines [5][0], 'Work package Travel/Travel')
        self.assertEqual (lines [5][1], '2')
        self.assertEqual (lines [5][2], '4')
        self.assertEqual (lines [5][3], '2')
        self.assertEqual (lines [5][4], 'WW 24/2013')
        self.assertEqual (lines [5][5], '2.00')
        self.assertEqual (lines [5][6], '2.00')
        self.assertEqual (lines [6][0], 'Work package Travel/Travel')
        self.assertEqual (lines [6][1], '2')
        self.assertEqual (lines [6][2], '4')
        self.assertEqual (lines [6][3], '2')
        self.assertEqual (lines [6][4], '2013-06-01;2013-06-30')
        self.assertEqual (lines [6][5], '2.00')
        self.assertEqual (lines [6][6], '2.00')
        self.assertEqual (lines [7][0], 'Sum')
        self.assertEqual (lines [7][1], '')
        self.assertEqual (lines [7][2], '')
        self.assertEqual (lines [7][3], '')
        self.assertEqual (lines [7][4], 'WW 23/2013')
        self.assertEqual (lines [7][5], '5.00')
        self.assertEqual (lines [7][6], '5.00')
        self.assertEqual (lines [8][0], 'Sum')
        self.assertEqual (lines [8][1], '')
        self.assertEqual (lines [8][2], '')
        self.assertEqual (lines [8][3], '')
        self.assertEqual (lines [8][4], 'WW 24/2013')
        self.assertEqual (lines [8][5], '3.00')
        self.assertEqual (lines [8][6], '3.00')
        self.assertEqual (lines [9][0], 'Sum')
        self.assertEqual (lines [9][1], '')
        self.assertEqual (lines [9][2], '')
        self.assertEqual (lines [9][3], '')
        self.assertEqual (lines [9][4], '2013-06-01;2013-06-30')
        self.assertEqual (lines [9][5], '8.00')
        self.assertEqual (lines [9][6], '8.00')

        # Only product_family column
        #   [ 'product_family'
        #   ]
        del cols [2]
        del cols [1:]
        cols [0] = 'product_family'
        del fs ['user']
        fs ['reporting_group'] = '2'
        self.assertEqual (cols, ['product_family'])
        self.assertEqual \
            ( fs
            , { 'date': '2013-06-01;2013-06-30'
              , 'reporting_group': '2'
              , 'summary_type': ['2', '4']
              }
            )
        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     1)
        self.assertEqual (len (lines [0]), 4)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Product family')
        self.assertEqual (lines [0][2], 'Time Period')
        self.assertEqual (lines [0][3], 'Sum')

        # Only reporting_group column
        #   [ 'reporting_group'
        #   ]
        cols [0] = 'reporting_group'
        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     3)
        self.assertEqual (len (lines [0]), 4)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Reporting group')
        self.assertEqual (lines [0][2], 'Time Period')
        self.assertEqual (lines [0][3], 'Sum')
        self.assertEqual (lines [1][0], 'Reporting group RG xyzzy')
        self.assertEqual (lines [1][1], 'RG xyzzy')
        self.assertEqual (lines [1][2], 'WW 24/2013')
        self.assertEqual (lines [1][3], '2.00')
        self.assertEqual (lines [2][0], 'Reporting group RG xyzzy')
        self.assertEqual (lines [2][1], 'RG xyzzy')
        self.assertEqual (lines [2][2], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][3], '2.00')

        # Only product_family column
        #   [ 'product_family'
        #   ]
        cols [0] = 'product_family'
        fs ['product_family'] = '1'
        del fs ['reporting_group']
        self.assertEqual \
            ( fs
            , { 'date': '2013-06-01;2013-06-30'
              , 'product_family': '1'
              , 'summary_type': ['2', '4']
              }
            )
        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     3)
        self.assertEqual (len (lines [0]), 4)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Product family')
        self.assertEqual (lines [0][2], 'Time Period')
        self.assertEqual (lines [0][3], 'Sum')
        self.assertEqual (lines [1][0], 'Product family Family test')
        self.assertEqual (lines [1][1], 'Family test')
        self.assertEqual (lines [1][2], 'WW 23/2013')
        self.assertEqual (lines [1][3], '5.00')
        self.assertEqual (lines [2][0], 'Product family Family test')
        self.assertEqual (lines [2][1], 'Family test')
        self.assertEqual (lines [2][2], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][3], '5.00')

        # Only project_type column
        #   [ 'project_type'
        #   ]
        cols [0] = 'project_type'
        fs ['project_type'] = '4'
        del fs ['product_family']
        self.assertEqual \
            ( fs
            , { 'date': '2013-06-01;2013-06-30'
              , 'project_type': '4'
              , 'summary_type': ['2', '4']
              }
            )
        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     3)
        self.assertEqual (len (lines [0]), 4)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Project type')
        self.assertEqual (lines [0][2], 'Time Period')
        self.assertEqual (lines [0][3], 'Sum')
        self.assertEqual (lines [1][0], 'Project type Support')
        self.assertEqual (lines [1][1], 'Support')
        self.assertEqual (lines [1][2], 'WW 24/2013')
        self.assertEqual (lines [1][3], '2.00')
        self.assertEqual (lines [2][0], 'Project type Support')
        self.assertEqual (lines [2][1], 'Support')
        self.assertEqual (lines [2][2], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][3], '2.00')

        #   [ 'project_type'
        #   , 'organisation.id'
        #   , 'time_wp.id'
        #   , 'time_wp'
        #   ]
        cols.append ('organisation.id')
        cols.append ('time_wp.id')
        cols.append ('time_wp')
        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     5)
        self.assertEqual (len (lines [0]), 6)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Project type')
        self.assertEqual (lines [0][2], 'Work package Id')
        self.assertEqual (lines [0][3], 'Organisation Id')
        self.assertEqual (lines [0][4], 'Time Period')
        self.assertEqual (lines [0][5], 'Sum')
        self.assertEqual (lines [1][0], 'Work package Travel/Travel')
        self.assertEqual (lines [1][1], 'Support')
        self.assertEqual (lines [1][2], '3')
        self.assertEqual (lines [1][3], '1')
        self.assertEqual (lines [1][4], 'WW 24/2013')
        self.assertEqual (lines [1][5], '2.00')
        self.assertEqual (lines [2][0], 'Work package Travel/Travel')
        self.assertEqual (lines [2][1], 'Support')
        self.assertEqual (lines [2][2], '3')
        self.assertEqual (lines [2][3], '1')
        self.assertEqual (lines [2][4], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][5], '2.00')
        self.assertEqual (lines [3][0], 'Project type Support')
        self.assertEqual (lines [3][1], 'Support')
        self.assertEqual (lines [3][2], '')
        self.assertEqual (lines [3][3], '')
        self.assertEqual (lines [3][4], 'WW 24/2013')
        self.assertEqual (lines [3][5], '2.00')
        self.assertEqual (lines [4][0], 'Project type Support')
        self.assertEqual (lines [4][1], 'Support')
        self.assertEqual (lines [4][2], '')
        self.assertEqual (lines [4][3], '')
        self.assertEqual (lines [4][4], '2013-06-01;2013-06-30')
        self.assertEqual (lines [4][5], '2.00')

        #   [ 'project_type'
        #   , 'organisation'
        #   , 'time_wp.id'
        #   , 'time_wp'
        #   ]
        cols [1] = 'organisation'
        self.assertEqual \
            (cols, ['project_type', 'organisation', 'time_wp.id', 'time_wp'])
        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     5)
        self.assertEqual (len (lines [0]), 6)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Organisation')
        self.assertEqual (lines [0][2], 'Project type')
        self.assertEqual (lines [0][3], 'Work package Id')
        self.assertEqual (lines [0][4], 'Time Period')
        self.assertEqual (lines [0][5], 'Sum')
        self.assertEqual (lines [1][0], 'Work package Travel/Travel')
        self.assertEqual (lines [1][1], 'The Org')
        self.assertEqual (lines [1][2], 'Support')
        self.assertEqual (lines [1][3], '3')
        self.assertEqual (lines [1][4], 'WW 24/2013')
        self.assertEqual (lines [1][5], '2.00')
        self.assertEqual (lines [2][0], 'Work package Travel/Travel')
        self.assertEqual (lines [2][1], 'The Org')
        self.assertEqual (lines [2][2], 'Support')
        self.assertEqual (lines [2][3], '3')
        self.assertEqual (lines [2][4], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][5], '2.00')
        self.assertEqual (lines [3][0], 'Project type Support')
        self.assertEqual (lines [3][1], '')
        self.assertEqual (lines [3][2], 'Support')
        self.assertEqual (lines [3][3], '')
        self.assertEqual (lines [3][4], 'WW 24/2013')
        self.assertEqual (lines [3][5], '2.00')
        self.assertEqual (lines [4][0], 'Project type Support')
        self.assertEqual (lines [4][1], '')
        self.assertEqual (lines [4][2], 'Support')
        self.assertEqual (lines [4][3], '')
        self.assertEqual (lines [4][4], '2013-06-01;2013-06-30')
        self.assertEqual (lines [4][5], '2.00')
    # end def test_user11

    def setup_user12 (self) :
        self.username12 = 'testuser12'
        self.user12 = self.db.user.create \
            ( username     = self.username12
            , firstname    = 'Nummer12'
            , lastname     = 'User12'
            )
        p = self.db.overtime_period.create \
            ( name              = 'monthly average required'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )
        self.db.commit ()
    # end def setup_user12

    def test_user12 (self) :
        self.log.debug ('test_user12')
        self.setup_db ()
        self.setup_user12 ()
        self.db.close ()
        self.db = self.tracker.open (self.username12)
        user12_time.import_data_12 (self.db, self.user12, self.olo)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user'         : [self.user12]
             , 'date'         : '2013-01-01;2013-12-31'
             , 'summary_type' : ['4']
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 2)
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [2], 'Balance Start')
        self.assertEqual (lines  [0] [6], 'Actual all')
        self.assertEqual (lines  [0] [7], 'required')
        self.assertEqual (lines  [0] [8], 'Supp. hours average')
        self.assertEqual (lines  [0] [9], 'Supplementary hours')
        self.assertEqual (lines  [0][11], 'Balance End')
        self.assertEqual (lines  [0][12], 'Overtime period')
        self.assertEqual (lines  [1] [1], '2013-01-01;2013-12-31')
        self.assertEqual (lines  [1] [2], '0.00')
        self.assertEqual (lines  [1] [6], '1791.47')
        self.assertEqual (lines  [1] [7], '1663.25')
        self.assertEqual (lines  [1] [8], '1720.35')
        self.assertEqual (lines  [1][11], '71.13')
        self.db.close ()
    # end def test_user12

    def setup_user13 (self) :
        self.username13 = 'testuser13'
        self.user13 = self.db.user.create \
            ( username     = self.username13
            , firstname    = 'Nummer13'
            , lastname     = 'User13'
            )
        self.db.commit ()
    # end def setup_user13

    def test_user13_vacation (self) :
        self.log.debug ('test_user13')
        self.setup_db ()
        self.setup_user13 ()
        # Allow report
        rl = self.db.user.get (self.user0, 'roles')
        self.db.user.set (self.user0, roles = ','.join ((rl, 'hr-vacation')))
        self.db.commit ()
        self.db.close  ()
        self.db = self.tracker.open (self.username13)
        user13_time.import_data_13 (self.db, self.user13, self.olo)
        vc = self.db.vacation_correction.filter \
            (None, dict (user = self.user13))
        self.assertEqual (len (vc), 1)
        vc = self.db.vacation_correction.getnode (vc [0])
        self.assertEqual (vc.absolute, True)
        self.db.vacation_correction.set \
            (vc.id, days = 7.27, date = date.Date ('2014-01-01'))
        self.db.commit ()
        self.db.close  ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user' : [self.user13], 'date' : '2014-01-01;2015-12-31' }
        class r : filterspec = fs ; columns = {'additional_submitted'}
        sr = summary.Vacation_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 3)
        self.assertEqual (len (lines [0]), 10)
        self.assertEqual (lines  [0] [0], 'User')
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [2], 'yearly entitlement')
        self.assertEqual (lines  [0] [3], 'yearly prorated')
        self.assertEqual (lines  [0] [4], 'carry forward from previous year')
        self.assertEqual (lines  [0] [5], 'entitlement total')
        self.assertEqual (lines  [0] [6], 'approved days')
        self.assertEqual (lines  [0] [7], 'vacation corrections')
        self.assertEqual (lines  [0] [8], 'remaining vacation')
        self.assertEqual (lines  [0] [9], 'additional submitted')
        self.assertEqual (lines  [1] [0], 'testuser13')
        self.assertEqual (lines  [1] [1], '2014-12-31')
        self.assertEqual (lines  [1] [2], '25.00')
        self.assertEqual (lines  [1] [3], '25.00')
        self.assertEqual (lines  [1] [4], '7.27')
        self.assertEqual (lines  [1] [5], '32.27')
        self.assertEqual (lines  [1] [6], '23.0')
        self.assertEqual (lines  [1] [7], '7.27')
        self.assertEqual (lines  [1] [8], '9.27')
        self.assertEqual (lines  [1] [9], '0.00')
        self.assertEqual (lines  [2] [0], 'testuser13')
        self.assertEqual (lines  [2] [1], '2015-12-31')
        self.assertEqual (lines  [2] [2], '25.00')
        self.assertEqual (lines  [2] [3], '25.00')
        self.assertEqual (lines  [2] [4], '9.27')
        self.assertEqual (lines  [2] [5], '34.27')
        self.assertEqual (lines  [2] [6], '0.0')
        self.assertEqual (lines  [2] [7], '')
        self.assertEqual (lines  [2] [8], '34.27')
        self.assertEqual (lines  [2] [9], '0.00')

        self.assertEqual \
            (33, eoy_vacation (self.db, self.user13, date.Date ('2014-12-31')))
        self.assertEqual \
            (35, eoy_vacation (self.db, self.user13, date.Date ('2015-12-31')))
        self.db.close ()
    # end def test_user13_vacation

    def test_user15_19_vac_monthly (self) :
        self.log.debug ('test_user15_19_vac_monthly')
        self.setup_db ()
        self.uid_by_name = {}
        for u in range (15, 20) :
            un = 'testuser%s' % u
            uid = self.db.user.create \
                ( username     = un
                , firstname    = 'Nummer%s' % un
                , lastname     = 'User%s' % un
                )
            self.uid_by_name [un] = uid
        # Allow report
        rl = self.db.user.get (self.user0, 'roles')
        self.db.user.set (self.user0, roles = ','.join ((rl, 'hr-vacation')))
        self.db.commit ()
        self.db.close  ()
        self.db = self.tracker.open ('admin')
        user15_19_vac.import_data_15 \
            (self.db, self.uid_by_name ['testuser15'], self.olo)
        user15_19_vac.import_data_16 \
            (self.db, self.uid_by_name ['testuser16'], self.olo)
        user15_19_vac.import_data_17 \
            (self.db, self.uid_by_name ['testuser17'], self.olo)
        user15_19_vac.import_data_18 \
            (self.db, self.uid_by_name ['testuser18'], self.olo)
        user15_19_vac.import_data_19 \
            (self.db, self.uid_by_name ['testuser19'], self.olo)
        self.db.commit ()
        self.db.close  ()
        self.db = self.tracker.open ('admin')
        with pytest.raises (Reject):
            vcorr = self.db.vacation_correction.create \
                ( user     = self.uid_by_name ['testuser15']
                , date     = date.Date ('2018-01-01')
                , absolute = 1
                , days     = 0.0
                )
        self.db.rollback ()
        self.db.close  ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user' : self.uid_by_name.values ()
             , 'date' : '2018-01-01;2018-12-31'
             }
        class r : filterspec = fs ; columns = {}
        sr = summary.Vacation_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 6)
        self.assertEqual (len (lines [0]), 9)
        self.assertEqual (lines  [0] [0], 'User')
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [2], 'yearly entitlement')
        self.assertEqual (lines  [0] [3], 'yearly prorated')
        self.assertEqual (lines  [0] [4], 'carry forward from previous year')
        self.assertEqual (lines  [0] [5], 'entitlement total')
        self.assertEqual (lines  [0] [6], 'approved days')
        self.assertEqual (lines  [0] [7], 'vacation corrections')
        self.assertEqual (lines  [0] [8], 'remaining vacation')
        self.assertEqual (lines  [1] [0], 'testuser15')
        self.assertEqual (lines  [1] [1], '2018-12-31')
        self.assertEqual (lines  [1] [2], '30.00')
        self.assertEqual (lines  [1] [3], '15.00')
        self.assertEqual (lines  [1] [4], '0.00')
        self.assertEqual (lines  [1] [5], '15.00')
        self.assertEqual (lines  [1] [6], '0.0')
        self.assertEqual (lines  [1] [7], '0.0')
        self.assertEqual (lines  [1] [8], '15.00')
        self.assertEqual (lines  [2] [0], 'testuser16')
        self.assertEqual (lines  [2] [1], '2018-12-31')
        self.assertEqual (lines  [2] [2], '30.00')
        self.assertEqual (lines  [2] [3], '15.00')
        self.assertEqual (lines  [2] [4], '0.00')
        self.assertEqual (lines  [2] [5], '15.00')
        self.assertEqual (lines  [2] [6], '0.0')
        self.assertEqual (lines  [2] [7], '0.0')
        self.assertEqual (lines  [2] [8], '15.00')
        self.assertEqual (lines  [3] [0], 'testuser17')
        self.assertEqual (lines  [3] [1], '2018-12-31')
        self.assertEqual (lines  [3] [2], '30.00')
        self.assertEqual (lines  [3] [3], '30.00')
        self.assertEqual (lines  [3] [4], '1.00')
        self.assertEqual (lines  [3] [5], '31.00')
        self.assertEqual (lines  [3] [6], '0.0')
        self.assertEqual (lines  [3] [7], '1.0')
        self.assertEqual (lines  [3] [8], '31.00')
        self.assertEqual (lines  [4] [0], 'testuser18')
        self.assertEqual (lines  [4] [1], '2018-12-31')
        self.assertEqual (lines  [4] [2], '30.00')
        self.assertEqual (lines  [4] [3], '12.50')
        self.assertEqual (lines  [4] [4], '0.00')
        self.assertEqual (lines  [4] [5], '12.50')
        self.assertEqual (lines  [4] [6], '0.0')
        self.assertEqual (lines  [4] [7], '0.0')
        self.assertEqual (lines  [4] [8], '12.50')
        self.assertEqual (lines  [5] [0], 'testuser19')
        self.assertEqual (lines  [5] [1], '2018-12-31')
        self.assertEqual (lines  [5] [2], '30.00')
        self.assertEqual (lines  [5] [3], '17.50')
        self.assertEqual (lines  [5] [4], '0.00')
        self.assertEqual (lines  [5] [5], '17.50')
        self.assertEqual (lines  [5] [6], '0.0')
        self.assertEqual (lines  [5] [7], '0.0')
        self.assertEqual (lines  [5] [8], '17.50')
        fs = { 'user' : self.uid_by_name.values ()
             , 'date' : '2019-01-01;2019-12-31'
             }
        class r : filterspec = fs ; columns = {}
        sr = summary.Vacation_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 4)
        self.assertEqual (len (lines [0]), 9)
        self.assertEqual (lines  [0] [0], 'User')
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [2], 'yearly entitlement')
        self.assertEqual (lines  [0] [3], 'yearly prorated')
        self.assertEqual (lines  [0] [4], 'carry forward from previous year')
        self.assertEqual (lines  [0] [5], 'entitlement total')
        self.assertEqual (lines  [0] [6], 'approved days')
        self.assertEqual (lines  [0] [7], 'vacation corrections')
        self.assertEqual (lines  [0] [8], 'remaining vacation')
        self.assertEqual (lines  [1] [0], 'testuser17')
        self.assertEqual (lines  [1] [1], '2019-12-31')
        self.assertEqual (lines  [1] [2], '30.00')
        self.assertEqual (lines  [1] [3], '30.00')
        self.assertEqual (lines  [1] [4], '31.00')
        self.assertEqual (lines  [1] [5], '61.00')
        self.assertEqual (lines  [1] [6], '0.0')
        self.assertEqual (lines  [1] [7], '')
        self.assertEqual (lines  [1] [8], '61.00')
        self.assertEqual (lines  [2] [0], 'testuser18')
        self.assertEqual (lines  [2] [1], '2019-12-31')
        self.assertEqual (lines  [2] [2], '30.00')
        self.assertEqual (lines  [2] [3], '2.50')
        self.assertEqual (lines  [2] [4], '12.50')
        self.assertEqual (lines  [2] [5], '15.00')
        self.assertEqual (lines  [2] [6], '0.0')
        self.assertEqual (lines  [2] [7], '')
        self.assertEqual (lines  [2] [8], '15.00')
        self.assertEqual (lines  [3] [0], 'testuser19')
        self.assertEqual (lines  [3] [1], '2019-12-31')
        self.assertEqual (lines  [3] [2], '30.00')
        self.assertEqual (lines  [3] [3], '30.00')
        self.assertEqual (lines  [3] [4], '17.50')
        self.assertEqual (lines  [3] [5], '47.50')
        self.assertEqual (lines  [3] [6], '0.0')
        self.assertEqual (lines  [3] [7], '')
        self.assertEqual (lines  [3] [8], '47.50')

        fs = { 'user' : self.uid_by_name.values ()
             , 'date' : '2019-01-01;2019-02-03'
             }
        class r : filterspec = fs ; columns = {}
        sr = summary.Vacation_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 4)
        self.assertEqual (len (lines [0]), 9)
        self.assertEqual (lines  [0] [0], 'User')
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [2], 'yearly entitlement')
        self.assertEqual (lines  [0] [3], 'yearly prorated')
        self.assertEqual (lines  [0] [4], 'carry forward from previous year')
        self.assertEqual (lines  [0] [5], 'entitlement total')
        self.assertEqual (lines  [0] [6], 'approved days')
        self.assertEqual (lines  [0] [7], 'vacation corrections')
        self.assertEqual (lines  [0] [8], 'remaining vacation')
        self.assertEqual (lines  [1] [0], 'testuser17')
        self.assertEqual (lines  [1] [1], '2019-02-03')
        self.assertEqual (lines  [1] [2], '30.00')
        self.assertEqual (lines  [1] [3], '2.50')
        self.assertEqual (lines  [1] [4], '31.00')
        self.assertEqual (lines  [1] [5], '33.50')
        self.assertEqual (lines  [1] [6], '0.0')
        self.assertEqual (lines  [1] [7], '')
        self.assertEqual (lines  [1] [8], '33.50')
        self.assertEqual (lines  [2] [0], 'testuser18')
        self.assertEqual (lines  [2] [1], '2019-02-03')
        self.assertEqual (lines  [2] [2], '30.00')
        self.assertEqual (lines  [2] [3], '2.50')
        self.assertEqual (lines  [2] [4], '12.50')
        self.assertEqual (lines  [2] [5], '15.00')
        self.assertEqual (lines  [2] [6], '0.0')
        self.assertEqual (lines  [2] [7], '')
        self.assertEqual (lines  [2] [8], '15.00')
        self.assertEqual (lines  [3] [0], 'testuser19')
        self.assertEqual (lines  [3] [1], '2019-02-03')
        self.assertEqual (lines  [3] [2], '30.00')
        self.assertEqual (lines  [3] [3], '5.00')
        self.assertEqual (lines  [3] [4], '17.50')
        self.assertEqual (lines  [3] [5], '22.50')
        self.assertEqual (lines  [3] [6], '0.0')
        self.assertEqual (lines  [3] [7], '')
        self.assertEqual (lines  [3] [8], '22.50')

        self.db.close ()
    # end def test_user15_19_vac_monthly

    def setup_user14 (self) :
        self.username14 = 'testuser14'
        self.user14 = self.db.user.create \
            ( username     = self.username14
            , firstname    = 'Nummer14'
            , lastname     = 'User14'
            )
        self.db.commit ()
    # end def setup_user14

    def test_user14_dyn_csv (self) :
        """  Test csv export for dynamic user data
        """

        class FakeRequest (object) :
            rfile = None
            def start_response (self, a, b) :
                pass
        # end class FakeRequest
        self.log.debug ('test_user14_dyn_csv')
        self.setup_db ()
        self.setup_user14 ()
        sapcc = self.db.sap_cc.create (name = 'SAP-CC', description = 'TEST')
        self.db.user_dynamic.set ('3', sap_cc = sapcc)
        # Allow user0
        rl = self.db.user.get (self.user0, 'roles')
        rl = ','.join ((rl, 'controlling'))
        self.db.user.set (self.user0, roles = rl)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        req = FakeRequest ()
        q = []
        q.append \
            (':columns=id,user,valid_from,valid_to,sap_cc,sap_cc.id,'
             'sap_cc.description'
            )
        q.append ('@sort=user')
        q.append (':filter=user')
        q.append ('user=testuser1,testuser2')
        env = dict (PATH_INFO = '', REQUEST_METHOD = 'GET')
        env ['QUERY_STRING'] = '&'.join (q)
        cli = self.tracker.Client (self.tracker, req, env, None)
        cli.db = self.db
        cli.language = 'en'
        cli.userid = self.db.getuid ()
        cli.classname = 'user_dynamic'
        cls = self.tracker.cgi_actions ['export_csv_names']
        exp = cls (cli)
        io = BytesIO ()
        exp.handle (outfile = io)
        # A way to test for python3
        v = io.getvalue ()
        if isinstance (u'', str) :
            v = v.decode ('utf-8')
        lines = tuple (csv.reader (StringIO (v), delimiter = '\t'))
        self.assertEqual (len (lines), 4)
        self.assertEqual (len (lines [0]), 7)
        self.assertEqual (lines  [0] [0], 'id')
        self.assertEqual (lines  [0] [1], 'user')
        self.assertEqual (lines  [0] [2], 'valid_from')
        self.assertEqual (lines  [0] [3], 'valid_to')
        self.assertEqual (lines  [0] [4], 'sap_cc')
        self.assertEqual (lines  [0] [5], 'sap_cc.id')
        self.assertEqual (lines  [0] [6], 'sap_cc.description')
        self.assertEqual (lines  [1] [0], '2')
        self.assertEqual (lines  [1] [1], 'testuser1')
        self.assertEqual (lines  [1] [2], '2005-09-01')
        self.assertEqual (lines  [1] [3], '2005-10-01')
        self.assertEqual (lines  [1] [4], '')
        self.assertEqual (lines  [1] [5], '')
        self.assertEqual (lines  [1] [6], '')
        self.assertEqual (lines  [2] [0], '4')
        self.assertEqual (lines  [2] [1], 'testuser1')
        self.assertEqual (lines  [2] [2], '2005-10-01')
        self.assertEqual (lines  [2] [3], '')
        self.assertEqual (lines  [2] [4], '')
        self.assertEqual (lines  [2] [5], '')
        self.assertEqual (lines  [2] [6], '')
        self.assertEqual (lines  [3] [0], '3')
        self.assertEqual (lines  [3] [1], 'testuser2')
        self.assertEqual (lines  [3] [2], '2008-11-03')
        self.assertEqual (lines  [3] [3], '')
        self.assertEqual (lines  [3] [4], 'SAP-CC')
        self.assertEqual (lines  [3] [5], '1')
        self.assertEqual (lines  [3] [6], 'TEST')
    # end def test_user14_dyn_csv

    def test_user14_tr_csv (self) :
        """  Test csv export for time_record
        """

        class FakeRequest (object) :
            rfile = None
            def start_response (self, a, b) :
                pass
        # end class FakeRequest
        self.log.debug ('test_user14_tr_csv')
        self.setup_db ()
        self.setup_user14 ()
        # Allow user0
        rl = self.db.user.get (self.user0, 'roles')
        rl = ','.join ((rl, 'controlling'))
        self.db.user.set (self.user0, roles = rl)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username14)
        user14_time.import_data_14 (self.db, self.user14, self.olo)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        req = FakeRequest ()
        q = []
        q.append \
            (':columns=daily_record.user,daily_record.date,'
             'daily_record.status,wp.project,wp,time_activity,'
             'duration,tr_duration,comment'
            )
        q.append (':sort=daily_record.user,daily_record.date,wp.project,wp')
        q.append (':filter=daily_record.user,daily_record.date')
        q.append ('daily_record.user=testuser14')
        q.append ('daily_record.date=2015-01-01')
        env = dict (PATH_INFO = '', REQUEST_METHOD = 'GET')
        env ['QUERY_STRING'] = '&'.join (q)
        cli = self.tracker.Client (self.tracker, req, env, None)
        cli.db = self.db
        cli.language = 'en'
        cli.userid = self.db.getuid ()
        cli.classname = 'time_record'
        cls = self.tracker.cgi_actions ['export_csv_names']
        exp = cls (cli)
        io = BytesIO ()
        exp.handle (outfile = io)
        v = io.getvalue ()
        if isinstance (u'', str):
            v = v.decode ('utf-8')
        lines = tuple (csv.reader (StringIO (v), delimiter = '\t'))
        self.assertEqual (len (lines), 2)
        self.assertEqual (len (lines [0]), 9)
        self.assertEqual (lines  [0] [0], 'daily_record.user')
        self.assertEqual (lines  [0] [1], 'daily_record.date')
        self.assertEqual (lines  [0] [2], 'daily_record.status')
        self.assertEqual (lines  [0] [3], 'wp.project')
        self.assertEqual (lines  [0] [4], 'wp')
        self.assertEqual (lines  [0] [5], 'time_activity')
        self.assertEqual (lines  [0] [6], 'duration')
        self.assertEqual (lines  [0] [7], 'tr_duration')
        self.assertEqual (lines  [0] [8], 'comment')
        self.assertEqual (lines  [1] [0], 'testuser14')
        self.assertEqual (lines  [1] [1], '2015-01-01')
        self.assertEqual (lines  [1] [2], 'open')
        self.assertEqual (lines  [1] [3], 'Public Holiday')
        self.assertEqual (lines  [1] [4], 'Holiday')
        self.assertEqual (lines  [1] [5], '')
        self.assertEqual (lines  [1] [6], '7.75')
        self.assertEqual (lines  [1] [7], '7.75')
        self.assertEqual (lines  [1] [8], '')
    # end def test_user14_tr_csv

    def test_user14_ar_csv (self) :
        """  Test csv export for attendance_record
        """

        class FakeRequest (object) :
            rfile = None
            def start_response (self, a, b) :
                pass
        # end class FakeRequest
        self.log.debug ('test_user14_ar_csv')
        self.setup_db ()
        self.setup_user14 ()
        # Allow user0
        rl = self.db.user.get (self.user0, 'roles')
        rl = ','.join ((rl, 'controlling'))
        self.db.user.set (self.user0, roles = rl)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username14)
        user14_time.import_data_14 (self.db, self.user14, self.olo)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        req = FakeRequest ()
        q = []
        q.append \
            (':columns=daily_record.user,daily_record.date,'
             'daily_record.status,work_location,start,end'
            )
        q.append (':sort=daily_record.user,daily_record.date,start')
        q.append (':filter=daily_record.user,daily_record.date')
        q.append ('daily_record.user=testuser14')
        q.append ('daily_record.date=2015-01-07')
        env = dict (PATH_INFO = '', REQUEST_METHOD = 'GET')
        env ['QUERY_STRING'] = '&'.join (q)
        cli = self.tracker.Client (self.tracker, req, env, None)
        cli.db = self.db
        cli.language = 'en'
        cli.userid = self.db.getuid ()
        cli.classname = 'attendance_record'
        cls = self.tracker.cgi_actions ['export_csv_names']
        exp = cls (cli)
        io = BytesIO ()
        exp.handle (outfile = io)
        v = io.getvalue ()
        if isinstance (u'', str):
            v = v.decode ('utf-8')
        lines = tuple (csv.reader (StringIO (v), delimiter = '\t'))
        self.assertEqual (len (lines), 3)
        self.assertEqual (len (lines [0]), 6)
        self.assertEqual (lines  [0] [0], 'daily_record.user')
        self.assertEqual (lines  [0] [1], 'daily_record.date')
        self.assertEqual (lines  [0] [2], 'daily_record.status')
        self.assertEqual (lines  [0] [3], 'work_location')
        self.assertEqual (lines  [0] [4], 'start')
        self.assertEqual (lines  [0] [5], 'end')
        self.assertEqual (lines  [1] [0], 'testuser14')
        self.assertEqual (lines  [1] [1], '2015-01-07')
        self.assertEqual (lines  [1] [2], 'open')
        self.assertEqual (lines  [1] [3], 'office')
        self.assertEqual (lines  [1] [4], '08:15')
        self.assertEqual (lines  [1] [5], '12:00')
        self.assertEqual (lines  [2] [0], 'testuser14')
        self.assertEqual (lines  [2] [1], '2015-01-07')
        self.assertEqual (lines  [2] [2], 'open')
        self.assertEqual (lines  [2] [3], 'office')
        self.assertEqual (lines  [2] [4], '12:30')
        self.assertEqual (lines  [2] [5], '17:00')
    # end def test_user14_ar_csv

    def test_user14_vacation (self) :
        self.log.debug ('test_user14')
        self.setup_db ()
        self.setup_user14 ()
        # Allow report
        rl = self.db.user.get (self.user0, 'roles')
        self.db.user.set (self.user0, roles = ','.join ((rl, 'hr-vacation')))
        self.db.commit ()
        self.db.close  ()
        self.db = self.tracker.open (self.username14)
        user14_time.import_data_14 (self.db, self.user14, self.olo)
        vc = self.db.vacation_correction.filter \
            (None, dict (user = self.user14))
        self.assertEqual (len (vc), 1)
        vc = self.db.vacation_correction.getnode (vc [0])
        self.assertEqual (vc.absolute, True)
        self.db.vacation_correction.set \
            (vc.id, days = 6.027, date = date.Date ('2015-01-01'))
        self.db.commit ()
        self.db.close  ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user' : [self.user14], 'date' : '2015-01-01;2015-12-31' }
        class r : filterspec = fs ; columns = {'additional_submitted'}
        sr = summary.Vacation_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 2)
        self.assertEqual (len (lines [0]), 10)
        self.assertEqual (lines  [0] [0], 'User')
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [2], 'yearly entitlement')
        self.assertEqual (lines  [0] [3], 'yearly prorated')
        self.assertEqual (lines  [0] [4], 'carry forward from previous year')
        self.assertEqual (lines  [0] [5], 'entitlement total')
        self.assertEqual (lines  [0] [6], 'approved days')
        self.assertEqual (lines  [0] [7], 'vacation corrections')
        self.assertEqual (lines  [0] [8], 'remaining vacation')
        self.assertEqual (lines  [0] [9], 'additional submitted')
        self.assertEqual (lines  [1] [0], 'testuser14')
        self.assertEqual (lines  [1] [1], '2015-12-31')
        self.assertEqual (lines  [1] [2], '25.00')
        self.assertEqual (lines  [1] [3], '10.34')
        self.assertEqual (lines  [1] [4], '6.03')
        self.assertEqual (lines  [1] [5], '16.37')
        self.assertEqual (lines  [1] [6], '10.0')
        self.assertEqual (lines  [1] [7], '6.027')
        self.assertEqual (lines  [1] [8], '6.37')
        self.assertEqual (lines  [1] [9], '0.00')
        self.db.close  ()

        self.db = self.tracker.open (self.username14)
        sr = summary.Vacation_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 2)
        self.assertEqual (len (lines [0]), 10)
        self.assertEqual (lines  [0] [0], 'User')
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [2], 'yearly entitlement')
        self.assertEqual (lines  [0] [3], 'yearly prorated')
        self.assertEqual (lines  [0] [4], 'carry forward from previous year')
        self.assertEqual (lines  [0] [5], 'entitlement total')
        self.assertEqual (lines  [0] [6], 'approved days')
        self.assertEqual (lines  [0] [7], 'vacation corrections')
        self.assertEqual (lines  [0] [8], 'remaining vacation')
        self.assertEqual (lines  [0] [9], 'additional submitted')
        self.assertEqual (lines  [1] [0], 'testuser14')
        self.assertEqual (lines  [1] [1], '2015-12-31')
        self.assertEqual (lines  [1] [2], '25.00')
        self.assertEqual (lines  [1] [3], '11.00')
        self.assertEqual (lines  [1] [4], '7.00')
        self.assertEqual (lines  [1] [5], '17.00')
        self.assertEqual (lines  [1] [6], '10.00')
        self.assertEqual (lines  [1] [7], '6.027')
        self.assertEqual (lines  [1] [8], '7.00')
        self.assertEqual (lines  [1] [9], '0.00')

        self.db.close ()
    # end def test_user14_vacation

    def test_vacation (self) :
        self.log.debug ('test_vacation')
        maildebug = os.path.join (self.dirname, 'maildebug')
        self.setup_db ()
        ext = self.db.config.ext
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_NOTIFY_SUBJECT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_NOTIFY_TEXT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_NOTIFY_EMAIL'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_CANCEL_SUBJECT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_CANCEL_TEXT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_CANCEL_EMAIL'))
        ext.add_option (Option (ext, 'MAIL', 'SPECIAL_LEAVE_NOTIFY_SUBJECT'))
        ext.add_option (Option (ext, 'MAIL', 'SPECIAL_LEAVE_NOTIFY_TEXT'))
        ext.add_option (Option (ext, 'MAIL', 'SPECIAL_LEAVE_NOTIFY_EMAIL'))
        ext.add_option (Option (ext, 'MAIL', 'SPECIAL_LEAVE_CANCEL_SUBJECT'))
        ext.add_option (Option (ext, 'MAIL', 'SPECIAL_LEAVE_CANCEL_TEXT'))
        ext.add_option (Option (ext, 'MAIL', 'SPECIAL_LEAVE_CANCEL_EMAIL'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_SUPERVISOR_SUBMIT_SUBJECT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_SUPERVISOR_SUBMIT_TEXT'))
        ext.add_option \
            (Option (ext, 'MAIL', 'LEAVE_SUPERVISOR_SUBMIT_APPROVE_HR'))
        ext.add_option \
            (Option (ext, 'MAIL', 'LEAVE_SUPERVISOR_SUBMIT_APPROVE_SV'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_SUPERVISOR_CRQ_SUBJECT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_SUPERVISOR_CRQ_TEXT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_SUPERVISOR_CRQ_APPROVE_HR'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_SUPERVISOR_CRQ_APPROVE_SV'))
        ext.add_option (Option (ext, 'MAIL', 'SPECIAL_LEAVE_USER_SUBJECT'))
        ext.add_option (Option (ext, 'MAIL', 'SPECIAL_LEAVE_USER_TEXT'))

        ext.add_option (Option (ext, 'MAIL', 'LEAVE_USER_ACCEPT_SUBJECT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_USER_ACCEPT_TEXT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_USER_ACCEPT_TIMERECS_TEXT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_USER_ACCEPT_ATTRECS_TEXT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_USER_DECLINE_SUBJECT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_USER_DECLINE_TEXT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_USER_CANCELLED_SUBJECT'))
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_USER_CANCELLED_TEXT'))
        ext.add_option \
            (Option (ext, 'MAIL', 'LEAVE_USER_NOT_CANCELLED_SUBJECT'))
        ext.add_option \
            (Option (ext, 'MAIL', 'LEAVE_USER_NOT_CANCELLED_TEXT'))
        ext.MAIL_LEAVE_NOTIFY_EMAIL = 'office@example.com'
        ext.MAIL_LEAVE_NOTIFY_SUBJECT = \
            ('Leave "%(tp_name)s/%(wp_name)s" '
             '%(first_day)s to %(last_day)s accepted'
            )
        ext.MAIL_LEAVE_NOTIFY_TEXT = \
            ('Dear member of the Office Team,\n'
             'the user $(firstname)s $(lastname)s has approved '
             '$(tp_name)s/$(wp_name)s\n'
             'from $(first_day)s to $(last_day)s.\n'
             'Please add this information to the time table,\n\n'
             'many thanks!'
            )
        ext.MAIL_LEAVE_CANCEL_EMAIL = 'office@example.com'
        ext.MAIL_LEAVE_CANCEL_SUBJECT = \
            ('Leave "%(tp_name)s/%(wp_name)s" '
             '%(first_day)s to %(last_day)s cancelled'
            )
        ext.MAIL_LEAVE_CANCEL_TEXT = \
            ('Dear member of the Office Team,\n'
             'the user $(firstname)s $(lastname)s has cancelled '
             '$(tp_name)s/$(wp_name)s\n'
             'from $(first_day)s to $(last_day)s\n'
             'due to $(comment_cancel)s.\n'
             'Please remove this information from the time table,\n\n'
             'many thanks!'
            )
        ext.MAIL_SPECIAL_LEAVE_NOTIFY_EMAIL = 'hr-admin@example.com'
        ext.MAIL_SPECIAL_LEAVE_NOTIFY_SUBJECT = \
            ('Leave "%(tp_name)s/%(wp_name)s" '
             '%(first_day)s to %(last_day)s accepted'
            )
        ext.MAIL_SPECIAL_LEAVE_NOTIFY_TEXT = \
            ('Dear member of HR Admin,\n'
             'the user $(firstname)s $(lastname)s has approved '
             '$(tp_name)s/$(wp_name)s\n'
             'from $(first_day)s to $(last_day)s.\n'
             'Comment: $(comment)s\n'
             'Please put it into the paid absence data sheet\n'
             'many thanks!'
            )
        ext.MAIL_SPECIAL_LEAVE_CANCEL_EMAIL = 'hr-admin@example.com'
        ext.MAIL_SPECIAL_LEAVE_CANCEL_SUBJECT = \
            ('Leave "%(tp_name)s/%(wp_name)s" '
             '%(first_day)s to %(last_day)s cancelled'
            )
        ext.MAIL_SPECIAL_LEAVE_CANCEL_TEXT = \
            ('Dear member of HR Admin,\n'
             'the user $(firstname)s $(lastname)s has cancelled '
             '$(tp_name)s/$(wp_name)s\n'
             'from $(first_day)s to $(last_day)s.\n'
             'Comment: $(comment_cancel)s\n'
             'Please remove this from the paid absence data sheet.\n'
             'many thanks!'
            )
        ext.MAIL_LEAVE_SUPERVISOR_SUBMIT_SUBJECT = \
            ('Leave request "$(tp_name)s/$(wp_name)s" '
             '$(first_day)s to $(last_day)s\n'
             'from $(firstname)s $(lastname)s'
            )
        ext.MAIL_LEAVE_SUPERVISOR_SUBMIT_TEXT = \
            ('$(firstname)s $(lastname)s has submitted a leave request\n'
             '"$(tp_name)s/$(wp_name)s".\n'
             'Comment from user: $(comment)s\n'
             '$(approval_type)s\n'
             '$(url)s\n'
             'Many thanks!\n\n'
             'This is an automatically generated message.\n'
             'Responses to this address are not possible.'
            )
        ext.MAIL_LEAVE_SUPERVISOR_SUBMIT_APPROVE_HR = \
            'Needs approval by HR.'
        ext.MAIL_LEAVE_SUPERVISOR_SUBMIT_APPROVE_SV = \
            'Please approve or decline at'
        ext.MAIL_LEAVE_SUPERVISOR_CRQ_SUBJECT = \
            ('Cancel request "$(tp_name)s/$(wp_name)s" '
             '$(first_day)s to $(last_day)s\n'
             'from $(firstname)s $(lastname)s'
            )
        ext.MAIL_LEAVE_SUPERVISOR_CRQ_TEXT = \
            ('$(firstname)s $(lastname)s has submitted a cancel request\n'
             '"$(tp_name)s/$(wp_name)s" from $(first_day)s to $(last_day)s.\n'
             'Comment from user: $(comment_cancel)s\n'
             '$(approval_type)s\n'
             '$(url)s\n'
             'Many thanks!\n\n'
             'This is an automatically generated message.\n'
             'Responses to this address are not possible.'
            )
        ext.MAIL_LEAVE_SUPERVISOR_CRQ_APPROVE_HR = \
            'Needs approval by HR.'
        ext.MAIL_LEAVE_SUPERVISOR_CRQ_APPROVE_SV = \
            'Please approve or decline at'
        ext.MAIL_SPECIAL_LEAVE_USER_SUBJECT = \
            ('Your Leave "%(tp_name)s/%(wp_name)s"\n'
             '%(first_day)s to %(last_day)s'
            )
        ext.MAIL_SPECIAL_LEAVE_USER_TEXT = \
            ("Dear $(firstname)s $(lastname)s,\n"
             "please don't forget to submit written documentation "
             "for your special leave\n$(tp_name)s/$(wp_name)s "
             "from $(first_day)s to $(last_day)s to HR,\n"
             "according to our processes.\n"
             "Eg. marriage certificate, new residence registration"
             " (Meldezettel),\n"
             "birth certificate for new child, death notice letter (Parte).\n"
             "$(nl)sMany thanks!"
            )
        ext.MAIL_LEAVE_USER_ACCEPT_SUBJECT = \
            ('Leave "$(tp_name)s/$(wp_name)s"\n'
             '$(first_day)s to $(last_day)s accepted'
            )
        ext.MAIL_LEAVE_USER_ACCEPT_TEXT = \
            ('Your absence request "$(tp_name)s/$(wp_name)s" '
             'has been accepted.\n'
             '$(deleted_records)s\n\n'
             'This is an automatically generated message.\n'
             'Responses to this address are not possible.\n'
            )
        ext.MAIL_LEAVE_USER_ACCEPT_TIMERECS_TEXT = \
            'The following existing time records have been deleted:\n'
        ext.MAIL_LEAVE_USER_ACCEPT_ATTRECS_TEXT = \
            'The following existing attendance records have been deleted:\n'
        ext.MAIL_LEAVE_USER_DECLINE_SUBJECT = \
            ('Leave "$(tp_name)s/$(wp_name)s"\n'
             '$(first_day)s to $(last_day)s declined'
            )
        ext.MAIL_LEAVE_USER_DECLINE_TEXT = \
            ('Your absence request "$(tp_name)s/$(wp_name)s" has been '
             'declined.\n'
             'Please contact your supervisor.\n\n'
             'This is an automatically generated message.\n'
             'Responses to this address are not possible.\n'
            )
        ext.MAIL_LEAVE_USER_CANCELLED_SUBJECT = \
            ('Leave "$(tp_name)s/$(wp_name)s"\n'
             '$(first_day)s to $(last_day)s cancelled'
            )
        ext.MAIL_LEAVE_USER_CANCELLED_TEXT = \
            ('Your cancel request "$(tp_name)s/$(wp_name)s"\n'
             'from $(first_day)s to $(last_day)s was granted.\n\n'
             'This is an automatically generated message.\n'
             'Responses to this address are not possible.\n'
            )
        ext.MAIL_LEAVE_USER_NOT_CANCELLED_SUBJECT = \
            ('Leave "$(tp_name)s/$(wp_name)s" '
             '$(first_day)s to $(last_day)s not cancelled'
            )
        ext.MAIL_LEAVE_USER_NOT_CANCELLED_TEXT = \
            ('Your cancel request "$(tp_name)s/$(wp_name)s" was not granted.\n'
             'Please contact your supervisor.\n\n'
             'This is an automatically generated message.\n'
             'Responses to this address are not possible.\n'
            )

        for d in '2008-11-03', '2008-11-30', '2008-12-31' :
            dt = date.Date (d)
            self.assertEqual \
                ( vacation.consolidated_vacation (self.db, self.user2, None, dt)
                , (28. + 31.) * 25. / 366.
                )
            self.assertEqual \
                ( vacation.remaining_vacation (self.db, self.user2, None, dt)
                , (28. + 31.) * 25. / 366.
                )
        for d in '2009-01-01', '2009-01-30', '2009-12-31' :
            dt = date.Date (d)
            self.assertEqual \
                ( vacation.consolidated_vacation (self.db, self.user2, None, dt)
                , (28. + 31.) * 25. / 366. + 25.
                )
            self.assertEqual \
                ( vacation.remaining_vacation (self.db, self.user2, None, dt)
                , (28. + 31.) * 25. / 366. + 25.
                )
        s   = [('+', 'user'), ('+', 'date')]
        vcs = self.db.vacation_correction.filter (None, {}, sort = s)
        self.assertEqual (len (vcs), 3)
        d = dict \
            (( ('1', (self.user0, date.Date ('2013-02-02')))
            ,  ('2', (self.user1, date.Date ('2005-09-01')))
            ,  ('3', (self.user2, date.Date ('2008-01-01')))
            ))
        for id in vcs :
            vc = self.db.vacation_correction.getnode (id)
            self.assertEqual (vc.user, d [id][0])
            self.assertEqual (vc.date, d [id][1])
            self.assertEqual (vc.days, 0)
            self.assertEqual (vc.absolute, True)
        self.assertEqual (len (vcs), 3)
        self.db.public_holiday.create \
            ( date        = date.Date ('2008-12-24')
            , description = 'Heiligabend'
            , is_half     = True
            , locations   = [self.loc]
            , name        = 'Heiligabend'
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2008-12-25')
            , description = 'Weihnachten'
            , is_half     = False
            , locations   = [self.loc]
            , name        = 'Weihnachten'
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2008-12-26')
            , description = 'Stephanitag'
            , is_half     = False
            , locations   = [self.loc]
            , name        = 'Stephanitag'
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2008-12-31')
            , description = 'Silvester'
            , is_half     = True
            , locations   = [self.loc]
            , name        = 'Silvester'
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2009-12-24')
            , description = 'Heiligabend'
            , is_half     = True
            , locations   = [self.loc]
            , name        = 'Heiligabend'
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2009-12-25')
            , description = 'Weihnachten'
            , is_half     = False
            , locations   = [self.loc]
            , name        = 'Weihnachten'
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2009-12-26')
            , description = 'Stephanitag'
            , is_half     = False
            , locations   = [self.loc]
            , name        = 'Stephanitag'
            )
        self.silvester = self.db.public_holiday.create \
            ( date        = date.Date ('2009-12-31')
            , description = 'Silvester'
            , is_half     = False # For testing!
            , locations   = [self.loc]
            , name        = 'Silvester'
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2010-01-01')
            , description = 'Neujahr'
            , is_half     = False
            , locations   = [self.loc]
            , name        = 'Neujahr'
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2010-01-06')
            , description = 'Heilige drei Koenige'
            , is_half     = False
            , locations   = [self.loc]
            , name        = 'Heilige drei Koenige'
            )
        st_open = self.db.leave_status.lookup ('open')
        st_subm = self.db.leave_status.lookup ('submitted')
        st_accp = self.db.leave_status.lookup ('accepted')
        st_decl = self.db.leave_status.lookup ('declined')
        st_carq = self.db.leave_status.lookup ('cancel requested')
        st_canc = self.db.leave_status.lookup ('cancelled')
        ud  = self.db.user_dynamic.filter \
            (None, dict (user = self.user1), sort = [('+', 'valid_from')]) [0]
        dyn = self.db.user_dynamic.getnode (ud)
        self.assertEqual (dyn.vacation_yearly, 25)
        ud  = self.db.user_dynamic.filter (None, dict (user = self.user2)) [0]
        dyn = self.db.user_dynamic.getnode (ud)
        self.assertEqual (dyn.vacation_yearly, 25)
        self.assertEqual (dyn.vacation_month, 1)
        self.assertEqual (dyn.vacation_day, 1)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username2)
        self.assertRaises (Reject, self.db.leave_submission.create)
        self.assertRaises \
            ( Reject, self.db.leave_submission.create
            , first_day = date.Date ('2009-12-20')
            )
        self.assertRaises \
            ( Reject, self.db.leave_submission.create
            , first_day = date.Date ('2009-12-20')
            , last_day  = date.Date ('2009-12-31')
            , time_wp   = self.holiday_wp
            )
        self.assertRaises \
            ( Reject, self.db.leave_submission.create
            , first_day = date.Date ('2009-12-20')
            , last_day  = date.Date ('2009-12-31')
            , time_wp   = self.vacation_wp
            , user      = self.user1
            )
        self.assertRaises \
            ( Reject, self.db.leave_submission.create
            , first_day = date.Date ('2009-12-20')
            , last_day  = date.Date ('2009-12-31')
            , time_wp   = self.vacation_wp
            , user      = self.user2
            , status    = self.db.leave_status.lookup ('accepted')
            )
        # Request for 0 days (date is a Saturday)
        self.assertRaises \
            ( Reject, self.db.leave_submission.create
            , first_day = date.Date ('2009-12-19')
            , last_day  = date.Date ('2009-12-19')
            , time_wp   = self.vacation_wp
            , user      = self.user2
            )
        # Request for 0 days (date is a public holiday)
        self.assertRaises \
            ( Reject, self.db.leave_submission.create
            , first_day = date.Date ('2009-12-26')
            , last_day  = date.Date ('2009-12-26')
            , time_wp   = self.vacation_wp
            , user      = self.user2
            )
        # first/last exchanged
        self.assertRaises \
            ( Reject, self.db.leave_submission.create
            , first_day = date.Date ('2009-12-27')
            , last_day  = date.Date ('2009-12-26')
            , time_wp   = self.vacation_wp
            , user      = self.user2
            )
        # time_wp = self.vacation_wp is the default
        vs = self.db.leave_submission.create \
            ( first_day = date.Date ('2009-12-22')
            , last_day  = date.Date ('2009-12-22')
            )
        # Created with *submitted*, set to open
        self.db.leave_submission.set (vs, status = st_open);
        # Cancel should work for user
        self.db.leave_submission.set (vs, status = st_canc);
        vs = self.db.leave_submission.create \
            ( first_day = date.Date ('2009-12-22')
            , last_day  = date.Date ('2009-12-22')
            )
        self.db.leave_submission.set (vs, status = st_open);
        un = self.db.leave_submission.create \
            ( first_day = date.Date ('2009-12-02')
            , last_day  = date.Date ('2009-12-02')
            , time_wp   = self.unpaid_wp
            )
        self.db.leave_submission.set (un, status = st_open);
        u2 = self.db.leave_submission.create \
            ( first_day = date.Date ('2009-12-03')
            , last_day  = date.Date ('2009-12-03')
            , time_wp   = self.unpaid_wp
            )
        self.db.leave_submission.set (u2, status = st_open);
        za = self.db.leave_submission.create \
            ( first_day = date.Date ('2009-12-04')
            , last_day  = date.Date ('2009-12-04')
            , time_wp   = self.flexi_wp
            )
        self.db.leave_submission.set (za, status = st_open);
        self.assertRaises \
            ( Reject, self.db.leave_submission.set
            , za
            , first_day = date.Date ('2009-12-05')
            )
        # First year: 4.04 days vacation, this is rounded *up* so user
        # should be able to request 5 days and supervisor should be able
        # to accept this.
        v2 = self.db.leave_submission.create \
            ( first_day = date.Date ('2008-12-22')
            , last_day  = date.Date ('2008-12-30')
            , time_wp   = self.vacation_wp
            )
        vac2 = self.db.leave_submission.getnode (v2)
        self.assertEqual \
            ( vacation.leave_days
                (self.db, self.user2, vac2.first_day, vac2.last_day)
            , 4.5
            )
        os.unlink (maildebug)

        self.assertRaises \
            ( Reject, self.db.leave_submission.create
            , first_day = date.Date ('2009-12-20')
            , last_day  = date.Date ('2009-12-31')
            , time_wp   = self.vacation_wp
            )
        self.db.leave_submission.set \
            ( vs
            , first_day = date.Date ('2009-12-20')
            , last_day  = date.Date ('2010-01-06')
            )
        dt = date.Date ('2009-12-22')
        dr = self.db.daily_record.filter \
            ( None
            , dict
                ( user = self.user2
                , date = common.pretty_range (dt, dt)
                )
            )
        self.assertEqual (len (dr), 1)
        tr = self.db.time_record.create \
            ( daily_record  = dr [0]
            , wp            = self.wps [0]
            , duration      = 2.0
            )
        ar1 = self.db.attendance_record.create \
            ( daily_record  = dr [0]
            , time_record   = tr
            , start         = '08:00'
            , end           = '10:00'
            , work_location = '1'
            )
        dr_sub = self.db.daily_record_status.lookup ('submitted')
        dr_opn = self.db.daily_record_status.lookup ('open')
        self.db.daily_record.set (dr [0], status = dr_sub)
        # may not submit with existing non-open daily recs
        self.assertRaises \
            ( Reject, self.db.leave_submission.set
            , vs
            , status = st_subm
            )
        # Make dr open again
        self.db.daily_record.set (dr [0], status = dr_opn)
        self.assertRaises \
            ( Reject, self.db.leave_submission.create
            , first_day = date.Date ('2009-12-22')
            , last_day  = date.Date ('2009-12-22')
            , time_wp   = self.vacation_wp
            )
        for st in (st_accp, st_decl, st_carq) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , vs
                , status = st
                )
        vsn  = self.db.leave_submission.getnode (vs)
        dt   = common.pretty_range (vsn.first_day, vsn.last_day)
        drs  = self.db.daily_record.filter \
            ( None
            , dict (user = self.user2, date = dt)
            , [('+', 'date')]
            )
        self.assertEqual (len (drs), 18)
        self.db.leave_submission.set (vs, status = st_subm)
        # May *not* submit the daily record
        self.assertRaises \
            ( Reject, self.db.daily_record.set
            , dr [0]
            , status = dr_sub
            )
        # But may still create time_recs in range
        tr = self.db.time_record.create \
            ( daily_record = dr [0]
            , duration     = 1.0
            )
        ar2 = self.db.attendance_record.create \
            ( daily_record = dr [0]
            , time_record  = tr
            , start        = '10:00'
            , end          = '11:00'
            )
        trs = self.db.time_record.filter (None, dict (daily_record = drs))
        ars = self.db.attendance_record.filter (None, dict (daily_record = drs))
        # Stephanitag is on Saturday, two extra records for deletion
        self.assertEqual (len (trs), 5 + 2)
        self.assertEqual (len (ars), 5 + 2)

        e = Parser ().parse (open (maildebug, 'r'))
        for h, t in \
            ( ('subject',    'Leave request "Vacation/Vacation" '
                             '2009-12-20 to 2010-01-06 from Test User2')
            , ('precedence', 'bulk')
            , ('to',         'user1@test.test')
            , ('from',       'roundup-admin@your.tracker.email.domain.example')
            ) :
            self.assertEqual (header_decode (e [h]), t)
        # base64-encoded body
        self.assertEqual \
            ( b64decode (e.get_payload ()).strip ()
            , b'Test User2 has submitted a leave request\n'
              b'"Vacation/Vacation".\n'
              b'Comment from user: None\n'
              b'Please approve or decline at\n'
              b'http://localhost:4711/ttt/leave_submission?@template=approve\n'
              b'Many thanks!\n\n'
              b'This is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            )
        os.unlink (maildebug)
        for st in (st_accp, st_decl, st_carq, st_canc) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , vs
                , status = st
                )
        self.db.leave_submission.set (vs, status = st_open)
        self.db.leave_submission.set (vs, status = st_subm)
        os.unlink (maildebug)
        self.db.leave_submission.set (un, status = st_subm)
        e = Parser ().parse (open (maildebug, 'r'))
        for h, t in \
            ( ('subject',    'Leave request "Leave/Unpaid" '
                             '2009-12-02 to 2009-12-02 from Test User2')
            , ('precedence', 'bulk')
            , ('to',         'user1@test.test, user0@test.test')
            , ('from',       'roundup-admin@your.tracker.email.domain.example')
            ) :
            self.assertEqual (header_decode (e [h]), t)
        self.assertEqual \
            ( b64decode (e.get_payload ()).strip ()
            , b'Test User2 has submitted a leave request\n'
              b'"Leave/Unpaid".\n'
              b'Comment from user: None\n'
              b'Needs approval by HR.\n'
              b'http://localhost:4711/ttt/leave_submission?@template=approve\n'
              b'Many thanks!\n\n'
              b'This is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            )
        os.unlink (maildebug)
        self.db.leave_submission.set (u2, status = st_subm)
        e = Parser ().parse (open (maildebug, 'r'))
        for h, t in \
            ( ('subject',    'Leave request "Leave/Unpaid" '
                             '2009-12-03 to 2009-12-03 from Test User2')
            , ('precedence', 'bulk')
            , ('to',         'user1@test.test, user0@test.test')
            , ('from',       'roundup-admin@your.tracker.email.domain.example')
            ) :
            self.assertEqual (header_decode (e [h]), t)
        self.assertEqual \
            ( b64decode (e.get_payload ()).strip ()
            , b'Test User2 has submitted a leave request\n'
              b'"Leave/Unpaid".\n'
              b'Comment from user: None\n'
              b'Needs approval by HR.\n'
              b'http://localhost:4711/ttt/leave_submission?@template=approve\n'
              b'Many thanks!\n\n'
              b'This is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            )
        os.unlink (maildebug)
        self.db.leave_submission.set (za, status = st_subm)
        e = Parser ().parse (open (maildebug, 'r'))
        for h, t in \
            ( ('subject',    'Leave request "Flexi/Flexi" '
                             '2009-12-04 to 2009-12-04 from Test User2')
            , ('precedence', 'bulk')
            , ('to',         'user1@test.test')
            , ('from',       'roundup-admin@your.tracker.email.domain.example')
            ) :
            self.assertEqual (header_decode (e [h]), t)
        self.assertEqual \
            ( b64decode (e.get_payload ()).strip ()
            , b'Test User2 has submitted a leave request\n'
              b'"Flexi/Flexi".\n'
              b'Comment from user: None\n'
              b'Please approve or decline at\n'
              b'http://localhost:4711/ttt/leave_submission?@template=approve\n'
              b'Many thanks!\n\n'
              b'This is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            )
        os.unlink (maildebug)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        for v in za, vs :
            for st in (st_open, st_carq, st_canc) :
                self.assertRaises \
                    ( Reject, self.db.leave_submission.set
                    , v
                    , status = st
                    )
        self.db.leave_submission.set (za, status = st_accp)
        box = mbox (maildebug, create = False)
        headers = \
            [ ( ('subject',    'Leave "Flexi/Flexi" '
                               '2009-12-04 to 2009-12-04 accepted')
              , ('precedence', 'bulk')
              , ('to',         'test.user@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            , ( ('subject',    'Leave "Flexi/Flexi" '
                               '2009-12-04 to 2009-12-04 accepted')
              , ('precedence', 'bulk')
              , ('to',         'office@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            ]
        body = \
            [ b'Your absence request "Flexi/Flexi" has been accepted.\n\n\n'
              b'This is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            , b'Dear member of the Office Team,\n'
              b'the user Test User2 has approved Flexi/Flexi\n'
              b'from 2009-12-04 to 2009-12-04.\n'
              b'Please add this information to the time table,\n\n'
              b'many thanks!'
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (b64decode (e.get_payload ()).strip (), body [n])
        os.unlink (maildebug)
        dt = self.db.leave_submission.get (za, 'first_day')
        dt = common.pretty_range (dt, dt)
        dr = self.db.daily_record.filter \
            (None, dict (user = self.user2, date = dt))
        self.assertEqual (len (dr), 1)
        tr = self.db.time_record.filter \
            (None, {'daily_record' : dr, 'wp.project.approval_required' : True})
        self.assertEqual (len (tr), 1)
        self.assertEqual (self.db.time_record.get (tr [0], 'duration'), 0)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username1)
        # For the change of public holiday, user1 needs role hr (or controlling)
        # This is because we also change historic time records in the
        # reactor
        self.db.user.set (self.user1, roles='user,hr')
        self.db.commit ()
        for st in (st_open, st_carq, st_canc) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , vs
                , status = st
                )
        # Should be possible that user1 sets this,
        # request 4.5 with 4.03 remaining days:
        self.db.leave_submission.set (v2, status = st_accp)
        os.unlink (maildebug)
        self.db.public_holiday.set (self.silvester, is_half = True)
        self.db.leave_submission.set (vs, status = st_accp)
        vsn  = self.db.leave_submission.getnode (vs)
        dt   = common.pretty_range (vsn.first_day, vsn.last_day)
        drs  = self.db.daily_record.filter \
            ( None
            , dict (user = vsn.user, date = dt)
            , [('+', 'date')]
            )
        self.assertEqual (len (drs), 18)
        trs = self.db.time_record.filter (None, dict (daily_record = drs))
        ars = self.db.attendance_record.filter (None, dict (daily_record = drs))
        # Stephanitag is on Saturday, vacation records for weekdays and
        # half public holidays
        self.assertEqual (len (trs), 5 + 10)
        self.assertEqual (len (ars), 5 + 10)
        box = mbox (maildebug, create = False)
        headers = \
            [ ( ('subject',    'Leave "Vacation/Vacation" '
                               '2009-12-20 to 2010-01-06 accepted')
              , ('precedence', 'bulk')
              , ('to',         'test.user@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            , ( ('subject',    'Leave "Vacation/Vacation" '
                               '2009-12-20 to 2010-01-06 accepted')
              , ('precedence', 'bulk')
              , ('to',         'office@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            ]
        body = \
            [ b'Your absence request "Vacation/Vacation" has been accepted.\n'
              b'\nThe following existing time records have been deleted:\n'
              b'2009-12-22: A Project / Work Package 0 duration: 2.0\n'
              b'2009-12-22:           /                duration: 1.0\n'
              b'\nThe following existing attendance records '
              b'have been deleted:\n'
              b'2009-12-22: office 08:00-10:00\n'
              b'2009-12-22:        10:00-11:00\n'
              b'\n\nThis is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            , b'Dear member of the Office Team,\n'
              b'the user Test User2 has approved Vacation/Vacation\n'
              b'from 2009-12-20 to 2010-01-06.\n'
              b'Please add this information to the time table,\n\n'
              b'many thanks!'
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (b64decode (e.get_payload ()).strip (), body [n])
        os.unlink (maildebug)
        for st in (st_accp, st_decl) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , un
                , status = st
                )
        for st in (st_decl, st_subm) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , vs
                , status = st
                )
        for x in (vs, un) :
            for st in (st_open, st_carq, st_canc) :
                self.assertRaises \
                    ( Reject, self.db.leave_submission.set
                    , x
                    , status = st
                    )
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        self.db.leave_submission.set (un, status = st_decl)
        e = Parser ().parse (open (maildebug, 'r'))
        for h, t in \
            ( ('subject',    'Leave "Leave/Unpaid" '
                             '2009-12-02 to 2009-12-02 declined')
            , ('precedence', 'bulk')
            , ('to',         'test.user@example.com')
            , ('from',       'roundup-admin@your.tracker.email.domain.example')
            ) :
            self.assertEqual (header_decode (e [h]), t)
        self.assertEqual \
            ( b64decode (e.get_payload ()).strip ()
            , b'Your absence request "Leave/Unpaid" has been declined.\n'
              b'Please contact your supervisor.'
              b'\n\nThis is an automatically generated message.\n'
              b'Responses to this address are not possible.'
        )
        os.unlink (maildebug)
        self.db.leave_submission.set (u2, status = st_accp)
        box = mbox (maildebug, create = False)
        headers = \
            [ ( ('subject',    'Leave "Leave/Unpaid" '
                               '2009-12-03 to 2009-12-03 accepted')
              , ('precedence', 'bulk')
              , ('to',         'test.user@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            , ( ('subject',    'Leave "Leave/Unpaid" '
                               '2009-12-03 to 2009-12-03 accepted')
              , ('precedence', 'bulk')
              , ('to',         'office@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            ]
        body = \
            [ b'Your absence request "Leave/Unpaid" has been accepted.'
              b'\n\n\nThis is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            , b'Dear member of the Office Team,\n'
              b'the user Test User2 has approved Leave/Unpaid\n'
              b'from 2009-12-03 to 2009-12-03.\n'
              b'Please add this information to the time table,\n\n'
              b'many thanks!'
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (b64decode (e.get_payload ()).strip (), body [n])
        os.unlink (maildebug)
        for st in (st_open, st_subm, st_decl, st_carq, st_canc) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , za
                , status = st
                )
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username2)
        for x in (vs, un) :
            for st in (st_open, st_subm, st_canc) :
                self.assertRaises \
                    ( Reject, self.db.leave_submission.set
                    , x
                    , status = st
                    )
        for st in (st_accp, st_carq) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , un
                , status = st
                )
        self.assertRaises \
            ( Reject, self.db.leave_submission.set
            , vs
            , status = st_decl
            )
        self.db.leave_submission.set \
            (vs, status = st_carq, comment_cancel = 'Cancel Comment')
        e = Parser ().parse (open (maildebug, 'r'))
        for h, t in \
            ( ('subject',    'Cancel request "Vacation/Vacation" '
                             '2009-12-20 to 2010-01-06 from Test User2'
              )
            , ('precedence', 'bulk')
            , ('to',         'user1@test.test')
            , ('from',       'roundup-admin@your.tracker.email.domain.example')
            ) :
            self.assertEqual (header_decode (e [h]), t)
        self.assertEqual \
            ( b64decode (e.get_payload ()).strip ()
            , b'Test User2 has submitted a cancel request\n'
              b'"Vacation/Vacation" from 2009-12-20 to 2010-01-06.\n'
              b'Comment from user: Cancel Comment\n'
              b'Please approve or decline at\n'
              b'http://localhost:4711/ttt/leave_submission?@template=approve'
              b'\nMany thanks!'
              b'\n\nThis is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            )
        os.unlink (maildebug)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        for st in (st_open, st_subm, st_decl) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , vs
                , status = st
                )
        self.db.close ()
        self.db = self.tracker.open (self.username1)
        for st in (st_open, st_subm, st_decl) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , vs
                , status = st
                )
        self.db.leave_submission.set (vs, status = st_accp)
        e = Parser ().parse (open (maildebug, 'r'))
        for h, t in \
            ( ('subject',    'Leave "Vacation/Vacation" '
                             '2009-12-20 to 2010-01-06 not cancelled')
            , ('precedence', 'bulk')
            , ('to',         'test.user@example.com')
            , ('from',       'roundup-admin@your.tracker.email.domain.example')
            ) :
            self.assertEqual (header_decode (e [h]), t)
        self.assertEqual \
            ( b64decode (e.get_payload ()).strip ()
            , b'Your cancel request "Vacation/Vacation" was not granted.\n'
              b'Please contact your supervisor.\n\n'
              b'This is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            )
        os.unlink (maildebug)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username2)
        self.db.leave_submission.set (vs, status = st_carq)
        os.unlink (maildebug)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username1)
        self.db.leave_submission.set (vs, status = st_canc)
        box = mbox (maildebug, create = False)
        headers = \
            [ ( ('subject',    'Leave "Vacation/Vacation" '
                             '2009-12-20 to 2010-01-06 cancelled')
              , ('precedence', 'bulk')
              , ('to',         'test.user@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            , ( ('subject',    'Leave "Vacation/Vacation" '
                               '2009-12-20 to 2010-01-06 cancelled')
              , ('precedence', 'bulk')
              , ('to',         'office@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            ]
        body = \
            [ b'Your cancel request "Vacation/Vacation"\n'
              b'from 2009-12-20 to 2010-01-06 was granted.'
              b'\n\nThis is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            , b'Dear member of the Office Team,\n'
              b'the user Test User2 has cancelled Vacation/Vacation\n'
              b'from 2009-12-20 to 2010-01-06\n'
              b'due to Cancel Comment.\n'
              b'Please remove this information from the time table,\n\n'
              b'many thanks!'
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (b64decode (e.get_payload ()).strip (), body [n])
        os.unlink (maildebug)
        vsn  = self.db.leave_submission.getnode (vs)
        dt   = common.pretty_range (vsn.first_day, vsn.last_day)
        drs  = self.db.daily_record.filter \
            ( None
            , dict (user = vsn.user, date = dt)
            , [('+', 'date')]
            )
        self.assertEqual (len (drs), 18)
        trs = self.db.time_record.filter (None, dict (daily_record = drs))
        ars = self.db.attendance_record.filter (None, dict (daily_record = drs))
        # Stephanitag is on Saturday, vacation records for weekdays and
        # half public holidays
        self.assertEqual (len (trs), 5)
        self.assertEqual (len (ars), 5)
        for st in (st_open, st_subm, st_accp, st_decl, st_carq) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , vs
                , status = st
                )
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username2)
        for st in (st_open, st_subm, st_accp, st_decl, st_carq) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , vs
                , status = st
                )
        # should go through, although existing cancelled record
        vs = self.db.leave_submission.create \
            ( first_day = date.Date ('2009-12-22')
            , last_day  = date.Date ('2009-12-22')
            )
        # should go through, although existing declined record
        za = self.db.leave_submission.create \
            ( first_day = date.Date ('2009-12-02')
            , last_day  = date.Date ('2009-12-02')
            , time_wp   = self.flexi_wp
            )
        os.unlink (maildebug)
        # Another vacation in 2008 which is already fully booked
        v3 = self.db.leave_submission.create \
            ( first_day = date.Date ('2008-12-02')
            , last_day  = date.Date ('2008-12-02')
            )
        e = Parser ().parse (open (maildebug, 'r'))
        for h, t in \
            ( ('subject',    'Leave request "Vacation/Vacation" '
                             '2008-12-02 to 2008-12-02 from Test User2')
            , ('precedence', 'bulk')
            , ('to',         'user1@test.test')
            , ('from',       'roundup-admin@your.tracker.email.domain.example')
            ) :
            self.assertEqual (header_decode (e [h]), t)
        self.assertEqual \
            ( b64decode (e.get_payload ()).strip ()
            , b'Test User2 has submitted a leave request\n'
              b'"Vacation/Vacation".\n'
              b'Comment from user: None\n'
              b'Please approve or decline at\n'
              b'http://localhost:4711/ttt/leave_submission?@template=approve'
              b'\nMany thanks!'
              b'\n\nThis is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            )
        os.unlink (maildebug)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username1)
        # supervisor can't accept/decline this, 2008 already fully booked
        for st in (st_open, st_accp, st_decl, st_carq, st_canc) :
            self.assertRaises \
                ( Reject, self.db.leave_submission.set
                , v3
                , status = st
                )
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username2)
        # Require comment for special leave
        self.assertRaises \
            ( Reject, self.db.leave_submission.create
            , first_day = date.Date ('2010-12-22')
            , last_day  = date.Date ('2010-12-30')
            , time_wp   = self.special_wp
            )
        spl = self.db.leave_submission.create \
            ( first_day = date.Date ('2010-12-22')
            , last_day  = date.Date ('2010-12-30')
            , time_wp   = self.special_wp
            , comment   = "Special leave comment"
            )
        self.db.leave_submission.set (spl, status = st_open)
        os.unlink (maildebug)
        self.assertRaises \
            ( Reject, self.db.leave_submission.set
            , spl
            , comment = None
            )
        self.db.leave_submission.set (spl, status = st_subm)
        self.assertRaises \
            ( Reject, self.db.leave_submission.set
            , spl
            , comment = "Changed comment"
            )
        box = mbox (maildebug, create = False)
        headers = \
            [ ( ('subject',    'Leave request "Special Leave/Special" '
                               '2010-12-22 to 2010-12-30 from Test User2')
              , ('precedence', 'bulk')
              , ('to',         'user1@test.test')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            , ( ('subject',    'Your Leave "Special Leave/Special" '
                               '2010-12-22 to 2010-12-30')
              , ('precedence', 'bulk')
              , ('to',         'test.user@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            ]
        body = \
            [ b'Test User2 has submitted a leave request\n'
              b'"Special Leave/Special".\n'
              b'Comment from user: Special leave comment\n'
              b'Please approve or decline at\n'
              b'http://localhost:4711/ttt/leave_submission?@template=approve'
              b'\nMany thanks!'
              b'\n\nThis is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            , b"Dear Test User2,\n"
              b"please don't forget to submit written documentation "
              b"for your special leave\n"
              b"Special Leave/Special from 2010-12-22 to 2010-12-30 to HR,\n"
              b"according to our processes.\n"
              b"Eg. marriage certificate, new residence registration "
              b"(Meldezettel),\n"
              b"birth certificate for new child, death notice letter "
              b"(Parte).\n\nMany thanks!"
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (b64decode (e.get_payload ()).strip (), body [n])
        os.unlink (maildebug)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username1)
        self.db.leave_submission.set (spl, status = st_accp)
        box = mbox (maildebug, create = False)
        headers = \
            [ ( ('subject',    'Leave "Special Leave/Special" '
                               '2010-12-22 to 2010-12-30 accepted')
              , ('precedence', 'bulk')
              , ('to',         'test.user@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            , ( ('subject',    'Leave "Special Leave/Special" '
                               '2010-12-22 to 2010-12-30 accepted')
              , ('precedence', 'bulk')
              , ('to',         'office@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            , ( ('subject',    'Leave "Special Leave/Special" '
                               '2010-12-22 to 2010-12-30 accepted')
              , ('precedence', 'bulk')
              , ('to',         'hr-admin@example.com')
              , ('from',       'roundup-admin@'
                               'your.tracker.email.domain.example')
              )
            ]
        body = \
            [ b'Your absence request "Special Leave/Special" has been accepted.'
              b'\n\n\nThis is an automatically generated message.\n'
              b'Responses to this address are not possible.'
            , b'Dear member of the Office Team,\n'
              b'the user Test User2 has approved Special Leave/Special\n'
              b'from 2010-12-22 to 2010-12-30.\n'
              b'Please add this information to the time table,\n\n'
              b'many thanks!'
            , b'Dear member of HR Admin,\n'
              b'the user Test User2 has approved Special Leave/Special\n'
              b'from 2010-12-22 to 2010-12-30.\n'
              b'Comment: Special leave comment\n'
              b'Please put it into the paid absence data sheet\n'
              b'many thanks!'
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (b64decode (e.get_payload ()).strip (), body [n])
        os.unlink (maildebug)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username2)
        self.db.leave_submission.set \
            (v2, status = st_carq, comment_cancel = 'Cancel Comment')
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username1)
        self.db.leave_submission.set (v2, status = st_canc)
        vs2 = self.db.leave_submission.getnode (v2)
        dt  = common.pretty_range (vs2.first_day, vs2.last_day)
        drs = self.db.daily_record.filter \
            (None, dict (user = self.user2, date = dt))
        for did in drs :
            dr = self.db.daily_record.getnode (did)
            self.assertEqual (dr.status, dr_opn)
        os.unlink (maildebug)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open ('admin')
        # Set wrong time on one of the time records
        # ['11', '27', '28', '29', '30', '31', '32', '33', '34']
        self.db.time_record.set_inner ('28', duration = 5)
        self.db.commit ()
        self.db.close ()
        # Now the error will *not* be corrected when the dynamic user
        # record changes *after* the error.
        self.db = self.tracker.open (self.username0)
        freeze = date.Date ('2010-12-31')
        to     = date.Date ('2012-01-01')
        self.db.daily_record_freeze.create (date = freeze, user = self.user2)
        self.db.user_dynamic.set ('3', valid_to = to)
    # end def test_vacation

    def setup_user16 (self) :
        self.username16 = 'testuser16'
        self.user16 = self.db.user.create \
            ( username     = self.username16
            , firstname    = 'Nummer16'
            , lastname     = 'User16'
            )
        user_dynamic.user_create_magic (self.db, self.user16, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user16
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        ud = self.db.user_dynamic.filter (None, dict (user = self.user16))
        self.assertEqual (len (ud), 1)
        self.db.user_dynamic.retire (ud [0])
        # allow user16 to book on wp 44
        self.db.time_wp.set (self.vacation_wp, bookers = [self.user16])
        self.db.commit ()
    # end def setup_user16

    def setup_user17 (self) :
        self.username17 = 'testuser17'
        self.user17 = self.db.user.create \
            ( username     = self.username17
            , firstname    = 'Nummer17'
            , lastname     = 'User17'
            )
        self.db.commit ()
    # end def setup_user17

    def setup_user18 (self) :
        self.username18 = 'testuser18'
        self.user18 = self.db.user.create \
            ( username     = self.username18
            , firstname    = 'Nummer18'
            , lastname     = 'User18'
            )
        self.db.commit ()
    # end def setup_user18

    def test_edit_dynuser_leave (self) :
        self.log.debug ('test_edit_dynuser_leave')
        self.setup_db ()
        self.setup_user16 ()
        # import user 16, dyn user start at 2018-10-01 and ends at 2019-01-31
        user16_leave.import_data_16 (self.db, self.user16, self.olo)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username16)
        # get id from single user dynamic record
        id = self.db.user_dynamic.filter (None, dict (user = self.user16)) [0]
        dyn = self.db.user_dynamic.getnode (id)

        # simulate edit of valid from
        # from 2018-10-01 to 2018-10-02 in user dynamic
        # should succeed
        self.db.user_dynamic.set (id, valid_from = date.Date ('2018-10-02'))

        # simulate edit of valid from
        # from 2018-10-02 to 2018-10-03 in user dynamic
        # should fail, because there is a leave request on 2018-10-02
        try :
            self.db.user_dynamic.set (id, valid_from = date.Date ('2018-10-03'))
        except Reject as err :
           self.assertEqual \
               ( str (err)
               , "There are open leave requests before 2018-10-03"
               )

        # Simulate that user requests and HR cancels the leave request
        # (2018-10-02)
        # find this leave request
        leave_ids = self.db.leave_submission.filter \
            ( None
            , dict
                ( user     = dyn.user
                , last_day = '2018-10-02'
                )
            )
        # check that request was found
        self.assertEqual (1, len (leave_ids))
        # user cancels request
        cr = self.db.leave_status.lookup ('cancel requested')
        self.db.leave_submission.set \
            (leave_ids [0], status=cr, comment_cancel = ' ')
        self.db.commit ()

        # User with HR-leave-approvel approves
        self.db1 = self.tracker.open (self.username0)
        self.db1.user.set (self.user0, roles = 'user,nosy,hr-leave-approval')
        cd = self.db1.leave_status.lookup ('cancelled')
        self.db1.leave_submission.set (leave_ids [0], status=cd)
        self.db1.commit ()
        self.db1.close ()

        # Now we can set the start-date
        self.db.user_dynamic.set (id, valid_from = date.Date ('2018-10-03'))

        # Find public holiday on 2018-10-26
        trs = self.db.time_record.filter \
            ( None
            , { 'daily_record.user': dyn.user
              , 'daily_record.date': '2018-10-26'
              }
            )
        # check that only one time_record is found
        self.assertEqual (1, len (trs))
        # check that time record is not retired
        self.assertEqual (False, self.db.time_record.is_retired (trs [0]))
        # simulate edit of valid from from 2018-10-01 to 2018-11-29 in user dynamic
        # should succeed, and 2019-10-26 should be automatically retired
        self.db.user_dynamic.set (id, valid_from = date.Date ('2018-11-29'))
        # check that time record is retired now
        self.assertEqual (True, self.db.time_record.is_retired (trs [0]))

        # simulate edit of valid from from 2018-11-29 to 2018-11-30 in user dynamic
        # should fail, because there is a time record on 2019-11-29
        try :
            self.db.user_dynamic.set (id, valid_from = date.Date ('2018-11-30'))
        except Reject as err :
           self.assertEqual \
               ( str (err)
               , "There are (non public holiday) time records before 2018-11-30"
               )

        # simulate edit of valid from from 2019-01-31 to 2019-01-01 in user dynamic
        # should succeed
        self.db.user_dynamic.set (id, valid_to = date.Date ('2019-01-01'))

        # simulate edit of valid from from 2019-01-01 to 2018-12-31 (open
        # interval, the valid_to date is *not* included in the validity span of
        # the dyn_user) in user dynamic should fail, because there are leave
        # requests after 2018-12-31
        try :
            self.db.user_dynamic.set (id, valid_to = date.Date ('2018-12-31'))
        except Reject as err :
           self.assertEqual \
               ( str (err)
               , "There are open leave requests at or after 2018-12-31"
               )

        # Simulate that user requests and HR cancels the leave request
        # (2018-12-14 - 2018-12-31)
        # find this leave request
        leave_ids = self.db.leave_submission.filter \
            ( None
            , dict
                ( user     = dyn.user
                , last_day = '2018-12-31'
                )
            )
        # check that request was found
        self.assertEqual (1, len (leave_ids))
        # user cancels request
        cr = self.db.leave_status.lookup ('cancel requested')
        self.db.leave_submission.set \
            (leave_ids [0], status=cr, comment_cancel = ' ')
        self.db.commit ()

        # User with HR-leave-approvel approves
        self.db1 = self.tracker.open (self.username0)
        cd = self.db1.leave_status.lookup ('cancelled')
        self.db1.leave_submission.set (leave_ids [0], status=cd)
        self.db1.commit ()
        self.db1.close ()

        # now settings the end date is possible
        self.db.user_dynamic.set (id, valid_to = date.Date ('2018-12-31'))

        try :
            self.db.user_dynamic.set (id, valid_to = date.Date ('2018-12-13'))
        except Reject as err :
           self.assertEqual \
               ( str (err)
               , "There are (non public holiday) time records at or after 2018-12-13"
               )

        trs = self.db.time_record.filter \
            ( None
            , { 'daily_record.user': dyn.user
              , 'daily_record.date': '2018-12-13'
              }
            )
        # check that only one time_record is found
        self.assertEqual (2, len (trs))
        for tr in trs :
            self.db.time_record.retire (tr)
        self.db.user_dynamic.set (id, valid_to = date.Date ('2018-12-13'))
    # end def test_edit_dynuser_leave

    def test_dynuser_create_modify (self) :
        self.log.debug ('test_dynuser_create_modify')
        self.setup_db ()
        otp = self.db.overtime_period.create \
            ( name              = 'monthly average required'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )
        self.setup_user17 ()
        self.setup_user18 ()
        # allow user17 and user18 to book on wp 44
        self.db.time_wp.set \
            (self.vacation_wp, bookers = [self.user18, self.user17])
        # import user 17 and 18
        user17_time.import_data_17 (self.db, self.user17, self.olo)
        user18_time.import_data_18 (self.db, self.user18, self.olo)
        self.db.commit ()
        ud = self.db.user_dynamic.create \
            ( hours_fri          = 1.0
            , hours_sun          = 0.0
            , additional_hours   = 5.0
            , hours_wed          = 1.0
            , vacation_yearly    = 25.0
            , all_in             = 0
            , valid_from         = date.Date ("2019-10-01.00:00:00")
            , durations_allowed  = 0
            , hours_tue          = 1.0
            , weekend_allowed    = 0
            , hours_mon          = 1.0
            , hours_thu          = 1.0
            , vacation_day       = 1.0
            , booking_allowed    = 1
            , supp_weekly_hours  = 5.0
            , valid_to           = date.Date ("2019-12-17.00:00:00")
            , weekly_hours       = 5.0
            , travel_full        = 0
            , vacation_month     = 1.0
            , hours_sat          = 0.0
            , org_location       = self.olo
            , overtime_period    = '1'
            , user               = self.user17
            , vac_aliq           = '1'
            )
        dyn = self.db.user_dynamic.getnode (ud)
        self.assertEqual (dyn.valid_from, date.Date ('2019-10-01'))
        self.assertEqual (dyn.valid_to,   date.Date ('2019-12-17'))
        prev = user_dynamic.prev_user_dynamic (self.db, dyn)
        self.assertEqual (prev.valid_from, date.Date ('2018-12-17'))
        self.assertEqual (prev.valid_to,   date.Date ('2019-10-01'))

        self.assertRaises (Reject, self.db.user_dynamic.create
            , hours_fri          = 7.5
            , hours_sun          = 0.0
            , additional_hours   = 38.5
            , hours_wed          = 7.75
            , vacation_yearly    = 25.0
            , all_in             = 0
            , valid_from         = date.Date ("2019-10-01.00:00:00")
            , durations_allowed  = 0
            , hours_tue          = 7.75
            , weekend_allowed    = 0
            , hours_mon          = 7.75
            , hours_thu          = 7.75
            , vacation_day       = 1.0
            , booking_allowed    = 1
            , supp_weekly_hours  = 38.5
            , valid_to           = date.Date ("2019-12-02.00:00:00")
            , weekly_hours       = 38.5
            , travel_full        = 0
            , vacation_month     = 1.0
            , hours_sat          = 0.0
            , org_location       = self.olo
            , overtime_period    = '1'
            , user               = self.user18
            , vac_aliq           = '1'
            )

        ud = self.db.user_dynamic.create \
            ( hours_fri          = 7.5
            , hours_sun          = 0.0
            , additional_hours   = 38.5
            , hours_wed          = 7.75
            , vacation_yearly    = 25.0
            , all_in             = 0
            , valid_from         = date.Date ("2019-10-01.00:00:00")
            , durations_allowed  = 0
            , hours_tue          = 7.75
            , weekend_allowed    = 0
            , hours_mon          = 7.75
            , hours_thu          = 7.75
            , vacation_day       = 1.0
            , booking_allowed    = 1
            , supp_weekly_hours  = 38.5
            , valid_to           = date.Date ("2019-12-01.00:00:00")
            , weekly_hours       = 38.5
            , travel_full        = 0
            , vacation_month     = 1.0
            , hours_sat          = 0.0
            , org_location       = self.olo
            , overtime_period    = '1'
            , user               = self.user18
            , vac_aliq           = '1'
            )
        dyn = self.db.user_dynamic.getnode (ud)
        self.assertEqual (dyn.valid_from, date.Date ('2019-10-01'))
        self.assertEqual (dyn.valid_to,   date.Date ('2019-12-01'))
        prev = user_dynamic.prev_user_dynamic (self.db, dyn)
        self.assertEqual (prev.valid_from, date.Date ('2019-05-01'))
        self.assertEqual (prev.valid_to,   date.Date ('2019-10-01'))
    # end def test_dynuser_create_modify

    def test_auto_wp (self) :
        self.setup_db ()
        self.db.commit ()
        # Now we have 3 users.
        for id in (self.holiday_tp, self.vacation_tp) :
            tp = self.db.time_project.getnode (id)
            self.db.auto_wp.create \
                ( is_valid     = True
                , name         = 'TEST %s' % tp.name
                , org_location = self.olo
                , time_project = id
                )
        # normal_tp with duration
        tp = self.db.time_project.getnode (self.normal_tp)
        auto_wp_onboarding = self.db.auto_wp.create \
            ( is_valid           = True
            , duration           = date.Interval ('3w')
            , name               = 'TEST %s' % tp.name
            , org_location       = self.olo
            , time_project       = self.normal_tp
            )
        d = self.db.user_dynamic.filter \
            (None, {}, sort = [('+', 'user'), ('+', 'valid_from')])
        # We have 4 dyn user records (without contract_type set)
        # id  uid from       to
        # '1' '3' 2013-02-02 None
        # '2' '4' 2005-09-01 2005-10-01
        # '4' '4' 2005-10-01 None
        # '3' '5' 2008-11-03

        u = self.username0
        n = '%s -%s' % (u, '2013-02-23')
        self.db.user_dynamic.set ('1', do_auto_wp = True)
        count = 0
        expected = \
            [ ('1', u, date.Date ('2013-02-02'), None)
            , ('2', u, date.Date ('2013-02-02'), None)
            , ('3', n, date.Date ('2013-02-02'), date.Date ('2013-02-23'))
            ]
        actual = []
        # All WPs created so far only have user '4' in bookers.
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        self.db.user_dynamic.set ('1', valid_to = date.Date ('2013-02-22'))
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        n = '%s -%s' % (u, '2013-02-22')
        expected = \
            [ ('1', n, date.Date ('2013-02-02'), date.Date ('2013-02-22'))
            , ('2', n, date.Date ('2013-02-02'), date.Date ('2013-02-22'))
            , ('3', n, date.Date ('2013-02-02'), date.Date ('2013-02-22'))
            ]
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        id = self.db.user_dynamic.create \
            ( user              = self.user0
            , valid_from        = date.Date ('2013-02-22')
            , valid_to          = date.Date ('2013-02-27')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , daily_worktime    = 0.0
            , org_location      = self.olo
            , supp_weekly_hours = 40
            , overtime_period   = self.db.overtime_period.lookup ('week')
            , do_auto_wp        = True
            )
        self.assertEqual (id, '5')
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        n  = '%s -%s' % (u, '2013-02-27')
        n2 = '%s -%s' % (u, '2013-02-23')
        expected = \
            [ ('1',  n, date.Date ('2013-02-02'), date.Date ('2013-02-27'))
            , ('2',  n, date.Date ('2013-02-02'), date.Date ('2013-02-27'))
            , ('3', n2, date.Date ('2013-02-02'), date.Date ('2013-02-23'))
            ]
        actual = []
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        tp = self.db.time_project.getnode (self.travel_tp)
        tv = self.db.auto_wp.create \
            ( is_valid     = True
            , name         = 'TEST %s' % tp.name
            , org_location = self.olo
            , time_project = self.travel_tp
            )
        expected = \
            [ ('1',  n, date.Date ('2013-02-02'), date.Date ('2013-02-27'))
            , ('2',  n, date.Date ('2013-02-02'), date.Date ('2013-02-27'))
            , ('3', n2, date.Date ('2013-02-02'), date.Date ('2013-02-23'))
            , ('4',  n, date.Date ('2013-02-02'), date.Date ('2013-02-27'))
            ]
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        self.db.auto_wp.set (tv, is_valid = False)
        expected = \
            [ ('1',  n, date.Date ('2013-02-02'), date.Date ('2013-02-27'))
            , ('2',  n, date.Date ('2013-02-02'), date.Date ('2013-02-27'))
            , ('3', n2, date.Date ('2013-02-02'), date.Date ('2013-02-23'))
            ]
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        self.db.user_dynamic.set ('1', valid_from = date.Date ('2013-02-03'))
        # Note that the limited record also changes the end date!
        n2 = '%s -%s' % (u, '2013-02-24')
        expected = \
            [ ('1',  n, date.Date ('2013-02-03'), date.Date ('2013-02-27'))
            , ('2',  n, date.Date ('2013-02-03'), date.Date ('2013-02-27'))
            , ('3', n2, date.Date ('2013-02-03'), date.Date ('2013-02-24'))
            ]
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        self.db.user_dynamic.set ('1', do_auto_wp = False)
        expected = \
            [ ('1',  n, date.Date ('2013-02-22'), date.Date ('2013-02-27'))
            , ('2',  n, date.Date ('2013-02-22'), date.Date ('2013-02-27'))
            , ('3', n2, date.Date ('2013-02-22'), date.Date ('2013-02-24'))
            ]
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        # No change if we set all_in on the dyn user
        self.assertEqual (self.db.user_dynamic.get ('5', 'all_in'), False)
        self.db.user_dynamic.set ('5', all_in = True, max_flexitime = 5)
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        # But now if we set all_in = False on the auto_wp:
        self.db.auto_wp.set ('1', all_in = False)
        expected = \
            [ ('2',  n, date.Date ('2013-02-22'), date.Date ('2013-02-27'))
            , ('3', n2, date.Date ('2013-02-22'), date.Date ('2013-02-24'))
            ]
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        # And set all_in = False in the dyn user:
        self.db.user_dynamic.set ('5', all_in = False)
        expected = \
            [ ('1',  n, date.Date ('2013-02-22'), date.Date ('2013-02-27'))
            , ('2',  n, date.Date ('2013-02-22'), date.Date ('2013-02-27'))
            , ('3', n2, date.Date ('2013-02-22'), date.Date ('2013-02-24'))
            ]
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        # Change org_location
        self.db.user_dynamic.set ('5', org_location = self.olo2)
        expected = []
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        self.db.user_dynamic.set ('5', org_location = self.olo)
        expected = \
            [ ('1',  n, date.Date ('2013-02-22'), date.Date ('2013-02-27'))
            , ('2',  n, date.Date ('2013-02-22'), date.Date ('2013-02-27'))
            , ('3', n2, date.Date ('2013-02-22'), date.Date ('2013-02-24'))
            ]
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        self.db.user_dynamic.set ('5', do_auto_wp = False)
        expected = []
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '3'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        # Test the auto-wp case with a delimited auto-wp
        # We have 2 dyn user records for user '4':
        # id  uid from       to
        # '2' '4' 2005-09-01 2005-10-01
        # '4' '4' 2005-10-01 None
        # We set only the dyn_user record '4' auto_wp = True
        # This should not create a wp because
        # 2005-09-01 + 3w = 2005-09-22
        # Then we extend the auto_wp duration (by setting the auto_wp to
        # false and creating a new one?) to 6w. This should now create
        # an auto wp starting 2005-10-01 and ending 2005-10-13.

        # Thaw
        f = self.db.daily_record_freeze.filter (None, dict (user = '4'))
        self.assertEqual (len (f), 1)
        self.db.daily_record_freeze.set (f [0], frozen = False)

        self.db.user_dynamic.set ('4', do_auto_wp = True)
        n  = 'testuser1'
        expected = \
            [ ('1', n, date.Date ('2005-10-01'), None)
            , ('2', n, date.Date ('2005-10-01'), None)
            ]
        actual = []
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '4'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            if not wp.auto_wp :
                continue
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        self.db.auto_wp.set \
            (auto_wp_onboarding, duration = date.Interval ('6w'))

        actual = []
        n3 = 'testuser1 -2005-10-13'
        expected.append \
            (('3', n3, date.Date ('2005-10-01'), date.Date ('2005-10-13')))
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '4'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            if not wp.auto_wp :
                continue
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

        self.db.auto_wp.set \
            (auto_wp_onboarding, duration = date.Interval ('3w'))

        actual = []
        expected = \
            [ ('1', n, date.Date ('2005-10-01'), None)
            , ('2', n, date.Date ('2005-10-01'), None)
            ]
        wps = self.db.time_wp.filter \
            (None, dict (bookers = '4'), sort = ('+', 'auto_wp.id'))
        for w in wps :
            wp = self.db.time_wp.getnode (w)
            if not wp.auto_wp :
                continue
            actual.append ((wp.auto_wp, wp.name, wp.time_start, wp.time_end))
        self.assertEqual (expected, actual)

    # end def test_auto_wp

    def setup_user20 (self) :
        self.username20 = 'testuser20'
        self.user20 = self.db.user.create \
            ( username     = self.username20
            , firstname    = 'Nummer20'
            , lastname     = 'User20'
            )
        p = self.db.overtime_period.create \
            ( name              = 'monthly average required'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )
        self.db.commit ()
    # end def setup_user20

    def test_user20 (self) :
        self.log.debug ('test_user20')
        self.setup_db ()
        self.setup_user20 ()
        self.db.close ()
        self.db = self.tracker.open (self.username20)
        user20_time.import_data_20 (self.db, self.user20, self.olo)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        self.db.overtime_correction.create \
            ( date  = date.Date ('2022-02-02')
            , user  = self.user20
            , value = 30.17
            )
        self.db.commit ()
        summary.init (self.tracker)
        fs = { 'user'         : [self.user20]
             , 'date'         : '2022-03-01;2022-04-03'
             , 'summary_type' : ['2', '3']
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 8)
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [2], 'Balance Start')
        self.assertEqual (lines  [0] [6], 'Actual all')
        self.assertEqual (lines  [0] [7], 'required')
        self.assertEqual (lines  [0] [8], 'Supp. hours average')
        self.assertEqual (lines  [0] [9], 'Supplementary hours')
        self.assertEqual (lines  [0][11], 'Balance End')
        self.assertEqual (lines  [0][12], 'Overtime period')
        self.assertEqual (lines  [0][14], 'Supp. hours / period')
        self.assertEqual (lines  [1] [1], 'WW 9/2022')
        self.assertEqual (lines  [2] [1], 'WW 10/2022')
        self.assertEqual (lines  [3] [1], 'WW 11/2022')
        self.assertEqual (lines  [4] [1], 'WW 12/2022')
        self.assertEqual (lines  [5] [1], 'WW 13/2022')
        self.assertEqual (lines  [6] [1], 'March 2022')
        self.assertEqual (lines  [7] [1], 'April 2022')
        self.assertEqual (lines  [1] [2], '36.08')
        self.assertEqual (lines  [4] [2], '39.95')
        self.assertEqual (lines  [4] [6], '42.25')
        self.assertEqual (lines  [4] [7], '38.50')
        self.assertEqual (lines  [4] [8], '41.76')
        self.assertEqual (lines  [4][11], '40.44')
        self.assertEqual (lines  [5] [2], '40.44')
        self.assertEqual (lines  [5] [6], '39.75')
        self.assertEqual (lines  [5] [7], '38.50')
        self.assertEqual (lines  [5] [8], '39.80')
        self.assertEqual (lines  [5] [9], '23.10')
        self.assertEqual (lines  [5][11], '40.39') # 36.02
        self.assertEqual (lines  [6] [2], '36.08')
        self.assertEqual (lines  [6] [6], '198.25')
        self.assertEqual (lines  [6] [7], '177.25')
        self.assertEqual (lines  [6] [8], '190.95')
        self.assertEqual (lines  [6] [9], '15.40')
        self.assertEqual (lines  [6][11], '43.49') # 39.12
        self.assertEqual (lines  [7] [2], '43.49') # 39.12
        self.assertEqual (lines  [7] [6], '4.50')
        self.assertEqual (lines  [7] [7], '7.50')
        self.assertEqual (lines  [7] [8], '0')
        self.assertEqual (lines  [7] [9], '7.70')
        self.assertEqual (lines  [7][11], '40.39') # 36.02
        # Now change the rest of April to use the first dyn params
        dynid = self.db.user_dynamic.create \
            ( additional_hours   = 38.5
            , all_in             = 0
            , booking_allowed    = 1
            , daily_worktime     = 9.0
            , do_auto_wp         = 1
            , durations_allowed  = 0
            , exemption          = 0
            , hours_mon          = 7.75
            , hours_tue          = 7.75
            , hours_wed          = 7.75
            , hours_thu          = 7.75
            , hours_fri          = 7.5
            , hours_sat          = 0.0
            , hours_sun          = 0.0
            , org_location       = self.olo
            , overtime_period    = '1'
            , supp_weekly_hours  = 38.5
            , travel_full        = 0
            , user               = self.user20
            , vac_aliq           = '1'
            , vacation_day       = 1.0
            , vacation_month     = 1.0
            , vacation_yearly    = 25.0
            , valid_from         = date.Date ("2022-04-01")
            , valid_to           = date.Date ("2022-08-06")
            , weekend_allowed    = 0
            , weekly_hours       = 38.5
            )
        assert dynid == '7'
        dyn = self.db.user_dynamic.getnode ('6')
        assert dyn.valid_to.pretty ('%Y-%m-%d') == '2022-04-01'
        self.db.user_dynamic.set \
            ( '6'
            , additional_hours  = None
            , supp_weekly_hours = None
            , supp_per_period   = 15.0
            , overtime_period   = '5'
            )
        self.db.commit ()
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 8)
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [2], 'Balance Start')
        self.assertEqual (lines  [0] [6], 'Actual all')
        self.assertEqual (lines  [0] [7], 'required')
        self.assertEqual (lines  [0] [8], 'Supp. hours average')
        self.assertEqual (lines  [0] [9], 'Supplementary hours')
        self.assertEqual (lines  [0][11], 'Balance End')
        self.assertEqual (lines  [0][12], 'Overtime period')
        self.assertEqual (lines  [0][14], 'Supp. hours / period')
        self.assertEqual (lines  [1] [1], 'WW 9/2022')
        self.assertEqual (lines  [2] [1], 'WW 10/2022')
        self.assertEqual (lines  [3] [1], 'WW 11/2022')
        self.assertEqual (lines  [4] [1], 'WW 12/2022')
        self.assertEqual (lines  [5] [1], 'WW 13/2022')
        self.assertEqual (lines  [6] [1], 'March 2022')
        self.assertEqual (lines  [7] [1], 'April 2022')
        self.assertEqual (lines  [1] [2], '36.08')
        self.assertEqual (lines  [4] [2], '39.95')
        self.assertEqual (lines  [4] [6], '42.25')
        self.assertEqual (lines  [4] [7], '38.50')
        self.assertEqual (lines  [4] [8], '41.76')
        self.assertEqual (lines  [4][11], '40.44')
        self.assertEqual (lines  [5] [2], '40.44')
        self.assertEqual (lines  [5] [6], '39.75')
        self.assertEqual (lines  [5] [7], '38.50')
        self.assertEqual (lines  [5] [8], '41.11')
        self.assertEqual (lines  [5] [9], '7.70')
        self.assertEqual (lines  [5][11], '39.08')
        self.assertEqual (lines  [6] [2], '36.08')
        self.assertEqual (lines  [6] [6], '198.25')
        self.assertEqual (lines  [6] [7], '177.25')
        self.assertEqual (lines  [6] [8], '192.25')
        self.assertEqual (lines  [6] [9], '0.00')
        self.assertEqual (lines  [6][11], '42.08')
        self.assertEqual (lines  [7] [2], '42.08')
        self.assertEqual (lines  [7] [6], '4.50')
        self.assertEqual (lines  [7] [7], '7.50')
        self.assertEqual (lines  [7] [8], '0')
        self.assertEqual (lines  [7] [9], '7.70')
        self.assertEqual (lines  [7][11], '39.08')

        self.db.close ()
    # end def test_user20

    def setup_user21 (self) :
        self.username21 = 'testuser21'
        self.user21 = self.db.user.create \
            ( username     = self.username21
            , firstname    = 'Nummer21'
            , lastname     = 'User21'
            )
        self.db.time_wp.set (self.vacation_wp, bookers = [self.user21])
        self.db.commit ()
    # end def setup_user21

    def gen_user21_dynamic (self):
        self.db.user_dynamic.create \
            ( all_in             = 1
            , booking_allowed    = 1
            , do_auto_wp         = 1
            , durations_allowed  = 0
            , exemption          = 0
            , hours_fri          = 7.5
            , hours_mon          = 7.75
            , hours_sat          = 0.0
            , hours_sun          = 0.0
            , hours_thu          = 7.75
            , hours_tue          = 7.75
            , hours_wed          = 7.75
            , max_flexitime      = 5.0
            , travel_full        = 0
            , vacation_day       = 1.0
            , vacation_month     = 1.0
            , vacation_yearly    = 25.0
            , valid_from         = date.Date ("2023-10-01.00:00:00")
            , weekend_allowed    = 0
            , weekly_hours       = 38.5
            , org_location       = self.olo
            , user               = self.user21
            , vac_aliq           = '1'
            )
    # end def gen_user21_dynamic

    def user21_inner (self):
        # monkey-patch avg_hours_per_week_this_year
        n   = 'avg_hours_per_week_this_year'
        fun = getattr (vacation, n)
        txt = inspect.getsource (fun)
        now = date.Date ('2023-01-18.16:00')
        d = dict \
            ( Date         = lambda x: now
            , common       = common
            , user_dynamic = user_dynamic
            )
        mod = ast.parse (txt)
        exec (compile (mod, '<string>', 'exec'), d)
        # This calls the newly-compiled function
        v = d [n] (self.db, self.user21, now)
        assert "%.2f" % v == "40.64"
        # No longer necessary to monkey-patch with optional enddate
        v = vacation.avg_hours_per_week_this_year \
            (self.db, self.user21, now, enddate = date.Date ('2023-03-15'))
        assert "%.2f" % v == "40.13"
        # Test a year in the future
        dt = date.Date ('2024-05-01')
        v = vacation.avg_hours_per_week_this_year \
            (self.db, self.user21, dt, enddate = date.Date ('2023-03-15'))
        assert "%.2f" % v == "0.00"
    # end def user21_inner

    def test_user21 (self) :
        self.log.debug ('test_user21')
        self.setup_db ()
        self.setup_user21 ()
        self.db.close ()
        self.db = self.tracker.open (self.username21)
        user21_time.import_data_21 (self.db, self.user21, self.olo)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        # Test twice with different dyn user records (one is in the
        # future and should not change the outcome but only with one of
        # them we used to get a traceback)
        self.user21_inner ()
        self.gen_user21_dynamic ()
        self.user21_inner ()
    # end def test_user21

    def setup_user22 (self) :
        self.username22 = 'testuser22'
        self.user22 = self.db.user.create \
            ( username     = self.username22
            , firstname    = 'Nummer22'
            , lastname     = 'User22'
            )
        self.db.time_wp.set (self.vacation_wp, bookers = [self.user22])
        self.db.public_holiday.create \
            ( date        = date.Date ('2020-12-24')
            , is_half     = True
            , locations   = [self.loc]
            , name        = 'Heiligabend'
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2020-12-25')
            , is_half     = False
            , locations   = [self.loc]
            , name        = 'Weihnachten'
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2020-12-26')
            , is_half     = False
            , locations   = [self.loc]
            , name        = 'Stephanitag'
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2020-12-31')
            , is_half     = True
            , locations   = [self.loc]
            , name        = 'Silvester'
            )
        self.db.commit ()
    # end def setup_user22

    def test_user22 (self) :
        self.log.debug ('test_user22')
        self.setup_db ()
        self.setup_user22 ()
        self.db.close ()
        self.db = self.tracker.open ('admin')
        user22_time.import_data_22 (self.db, self.user22, self.olo)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        dyn = self.db.user_dynamic.filter (None, dict (user = self.user22))
        assert len (dyn) == 1
        dyn = dyn [0]
        dt  = date.Date ('2021-02-01')
        flt = self.db.leave_submission.filter
        #self.db.user_dynamic.set (dyn, valid_to = dt)
        self.db.user_dynamic.create \
            ( all_in             = 1
            , booking_allowed    = 1
            , do_auto_wp         = 1
            , durations_allowed  = 0
            , exemption          = 0
            , max_flexitime      = 5.0
            , travel_full        = 0
            , vacation_day       = 1.0
            , vacation_month     = 1.0
            , vacation_yearly    = 25.0
            , valid_from         = date.Date ("2020-12-01.00:00:00")
            , weekend_allowed    = 0
            , weekly_hours       = 40
            , org_location       = self.olo
            , user               = self.user22
            , vac_aliq           = '1'
            )
        leave = self.db.daily_record_status.lookup ('leave')
        d   = \
            { 'daily_record.user'   : self.user22
            , 'daily_record.date'   : '2020-12-21;2021-01-28'
            , 'daily_record.status' : leave
            }
        found_vac = found_spec = found_hol = found_flex = 0
        trids = self.db.time_record.filter (None, d)
        assert len (trids) == 13
        for trid in trids:
            tr = self.db.time_record.getnode (trid)
            dr = self.db.daily_record.getnode (tr.daily_record)
            dt = dr.date.pretty (common.ymd)
            wp = self.db.time_wp.getnode (tr.wp)
            tp = self.db.time_project.getnode (wp.project)
            ho = self.db.public_holiday.filter (None, dict (date = dt))
            if ho:
                ho = self.db.public_holiday.getnode (ho [0])
            else:
                ho = None
            found_vac  += bool (tp.is_vacation)
            found_spec += bool (tp.is_special_leave)
            found_hol  += bool (tp.is_public_holiday)
            found_flex += tp.max_hours == 0
            if tp.is_special_leave or tp.is_vacation or tp.is_public_holiday:
                h = 8
                if ho and ho.is_half:
                    h = 4
                assert tr.duration == h
            if tp.max_hours == 0:
                assert tr.duration == 0
        assert found_spec == 2
        assert found_vac  == 7
        assert found_hol  == 3
        assert found_flex == 1

        self.db.commit ()
        self.db.close ()
    # end def test_user22

    def setup_user23 (self) :
        self.username23 = 'testuser23'
        self.user23 = self.db.user.create \
            ( username     = self.username23
            , firstname    = 'Nummer23'
            , lastname     = 'User23'
            )
        self.ct_intern = self.db.contract_type.create \
            ( name  = 'Internship'
            , order = 1
            )
        self.db.user_dynamic.create \
            ( additional_hours   = 20.0
            , all_in             = 0
            , booking_allowed    = 1
            , do_auto_wp         = 1
            , durations_allowed  = 0
            , exemption          = 0
            , hours_fri          = 4.0
            , hours_mon          = 4.0
            , hours_sat          = 0.0
            , hours_sun          = 0.0
            , hours_thu          = 4.0
            , hours_tue          = 4.0
            , hours_wed          = 4.0
            , supp_weekly_hours  = 20.0
            , travel_full        = 0
            , vacation_day       = 1.0
            , vacation_month     = 1.0
            , vacation_yearly    = 25.0
            , valid_from         = date.Date ("2021-07-01.00:00:00")
            , valid_to           = date.Date ("2021-09-01.00:00:00")
            , weekend_allowed    = 0
            , weekly_hours       = 20.0
            , org_location       = self.olo
            , user               = self.user23
            , vac_aliq           = '1'
            , contract_type      = self.ct_intern
            )
        # These are needed because WPs names must be unique for the same TP
        # Should we again need to import auto wp stuff we need to factor
        # this out.
        wl_off    = self.db.work_location.lookup ('off')
        stat_open = self.db.time_project_status.lookup ('Open')
    # end def

    def test_user23 (self) :
        self.log.debug ('test_user23')
        self.setup_db ()
        self.setup_user23 ()
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open ('admin')
        # Monkey-patch the detector list to remove auto wp checks
        old_priolist_wp = self.db.time_wp.auditors ['create']
        pl = deepcopy (old_priolist_wp)
        # Priolist has (prio, name, function) tuples
        for i, item in enumerate (pl.list):
            if item [1] == 'wp_check_auto_wp':
                del pl.list [i]
                break
        self.db.time_wp.auditors ['create'] = pl
        user23_time.import_data_23 (self.db, self.user23, self.olo, self)
        self.db.commit ()
        # Restore detectors
        self.db.time_wp.auditors ['create'] = old_priolist_wp
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        dyn = self.db.user_dynamic.filter \
            (None, dict (user = self.user23, valid_from = '2022-03-01'))
        assert len (dyn) == 1
        dyn = self.db.user_dynamic.getnode (dyn [0])
        self.db.user_dynamic.set (dyn.id, contract_type = None)
        self.db.close ()
    # end def test_user23

    def setup_user24 (self) :
        self.username24 = 'testuser24'
        self.user24 = self.db.user.create \
            ( username     = self.username24
            , firstname    = 'Nummer24'
            , lastname     = 'User24'
            , supervisor   = self.user0
            , address      = 'testuser24@example.com'
            )
        p = self.db.overtime_period.create \
            ( name              = 'month average'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )
        # We need to import the data *before* we create public holidays,
        # otherwise the time records for these would be created during
        # import
        # Monkey-patch the detector list to remove auto wp checks
        old_priolist_wp = self.db.time_wp.auditors ['create']
        pl = deepcopy (old_priolist_wp)
        dl = []
        # Priolist has (prio, name, function) tuples
        for i, item in enumerate (pl.list):
            if item [1] == 'wp_check_auto_wp':
                del pl.list [i]
                break
        old_priolist_ph = self.db.public_holiday.reactors ['create']
        pl = deepcopy (old_priolist_ph)
        # Priolist has (prio, name, function) tuples
        for i, item in enumerate (pl.list):
            if item [1] == 'fix_daily_recs':
                del pl.list [i]
                break
        self.db.public_holiday.reactors ['create'] = pl
        user24_time.import_data_24 (self.db, self.user24, self.olo, self)
        # We need the public holidays in Dec
        self.db.public_holiday.create \
            ( date        = date.Date ('2023-12-08')
            , description = 'Maria Empfängis'
            , name        = 'Maria Empfängis'
            , locations   = [self.loc]
            , is_half     = False
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2023-12-24')
            , description = 'Heiligabend'
            , name        = 'Heiligabend'
            , locations   = [self.loc]
            , is_half     = False
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2023-12-25')
            , description = 'Christtag'
            , name        = 'Christtag'
            , locations   = [self.loc]
            , is_half     = False
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2023-12-26')
            , description = 'Stefanitag'
            , name        = 'Stefanitag'
            , locations   = [self.loc]
            , is_half     = False
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2023-12-31')
            , description = 'Silvester'
            , name        = 'Silvester'
            , locations   = [self.loc]
            , is_half     = False
            )
        # Restore detectors
        self.db.time_wp.auditors        ['create'] = old_priolist_wp
        self.db.public_holiday.reactors ['create'] = old_priolist_ph
    # end def setup_user24

    def test_user24 (self):
        self.log.debug ('test_user24')
        self.setup_db ()
        self.setup_user24 ()
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        ud = self.db.user_dynamic.filter \
            (None, dict (user = self.user24, valid_to = '2023-11-30'))
        assert len (ud) == 1
        dt = date.Date ('2023-12-01')
        self.db.user_dynamic.set (ud [0], valid_to = dt)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username24)
        # Now check if we can set to cancel requested:
        # This used to raise
        # 'Editing of time records only for status "open"'
        # This leave_submission is 2023-12-23-2023-12-31
        self.db.leave_submission.set ('6', status = '6', comment_cancel = 'bla')
        # Now check if the same happens when we pass the wp
        # This leave_submission is 2023-12-05-2023-12-10
        # This used to raise 'Work package must not be specified'
        # The wp is passed by the mask in the web interface.
        self.db.leave_submission.set \
            ('2', status = '6', comment_cancel = 'bla', time_wp = '58')
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        d = dict (user = self.user24, status = '6')
        for l in self.db.leave_submission.filter (None, d):
            self.db.leave_submission.set (l, status = '7')
        self.db.commit ()
        self.db.close ()
    # end def test_user24

    def setup_user25 (self) :
        self.username25 = 'testuser25'
        self.user25 = self.db.user.create \
            ( username     = self.username25
            , firstname    = 'Nummer25'
            , lastname     = 'User25'
            , supervisor   = self.user0
            , address      = 'testuser25@example.com'
            )
        p = self.db.overtime_period.create \
            ( name              = 'month average'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )
        self.db.time_wp.set ('44', bookers = [self.user25])
        # We need to import the data *before* we create public holidays,
        # otherwise the time records for these would be created during
        # import
        old_priolist_ph = self.db.public_holiday.reactors ['create']
        pl = deepcopy (old_priolist_ph)
        # Priolist has (prio, name, function) tuples
        for i, item in enumerate (pl.list):
            if item [1] == 'fix_daily_recs':
                del pl.list [i]
                break
        self.db.public_holiday.reactors ['create'] = pl
        user25_time.import_data_25 (self.db, self.user25, self.olo, self)
        # We need the public holidays in Dec
        self.db.public_holiday.create \
            ( date        = date.Date ('2020-12-24')
            , description = 'Heiligabend'
            , name        = 'Heiligabend'
            , locations   = [self.loc]
            , is_half     = False
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2020-12-25')
            , description = 'Christtag'
            , name        = 'Christtag'
            , locations   = [self.loc]
            , is_half     = False
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2020-12-26')
            , description = 'Stefanitag'
            , name        = 'Stefanitag'
            , locations   = [self.loc]
            , is_half     = False
            )
        self.db.public_holiday.create \
            ( date        = date.Date ('2020-12-31')
            , description = 'Silvester'
            , name        = 'Silvester'
            , locations   = [self.loc]
            , is_half     = False
            )
        # Restore detectors
        self.db.public_holiday.reactors ['create'] = old_priolist_ph
        # Make public holiday wp end 2020-01-01
        self.db.time_wp.set \
            ( self.holiday_wp
            , time_end = date.Date ('2020-01-01')
            , name     = 'Old Public Holiday'
            )
        # And create new public holiday wp
        self.holiday_wp_new = self.db.time_wp.create \
            ( name               = 'Holiday'
            , project            = self.holiday_tp
            , time_start         = date.Date ('2020-01-01')
            , durations_allowed  = True
            , responsible        = '1'
            , cost_center        = self.cc
            , bookers            = [self.user25]
            )
        # Need to freeze
        self.db.daily_record_freeze.create \
            ( date = date.Date ('2021-12-31')
            , user = self.user25
            )
    # end def setup_user25

    def test_user25 (self):
        self.log.debug ('test_user25')
        self.setup_db ()
        self.setup_user25 ()
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        self.db.user_dynamic.set \
            (self.dyn25, valid_to = date.Date ('2023-10-01'))
        self.db.commit ()
        self.db.close ()
    # end def test_user25

    def setup_user26 (self) :
        self.username26 = 'testuser26'
        self.user26 = self.db.user.create \
            ( username     = self.username26
            , firstname    = 'Nummer26'
            , lastname     = 'User26'
            , supervisor   = self.user0
            , address      = 'testuser26@example.com'
            )
        p = self.db.overtime_period.create \
            ( name              = 'month average'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )
        self.db.time_wp.set ('44', bookers = [self.user26])
        self.locj = self.db.location.create \
            ( name    = 'Japan'
            , country = 'Japan'
            , address = 'Japan'
            )
        self.oloj = self.db.org_location.create \
            ( name                = 'Org J'
            , location            = self.locj
            , organisation        = self.org
            , vacation_legal_year = False
            , vacation_yearly     = 25.0
            , do_leave_process    = True
            , vac_aliq            = '1'
            )
        user26_time.import_data_26 (self.db, self.user26, self.olo)
        # We need a public holiday
        self.db.public_holiday.create \
            ( date        = date.Date ('2023-08-11')
            , description = 'Mountain day'
            , name        = 'Mountain day'
            , locations   = [self.locj]
            , is_half     = False
            )
        self.db.time_wp.set (self.holiday_wp, bookers = [self.user26])
    # end def setup_user26

    def test_user26 (self):
        self.log.debug ('test_user26')
        self.setup_db ()
        self.setup_user26 ()
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username26)
        dn = self.db.user_dynamic.filter (None, dict (user = self.user26))
        assert len (dn) == 1
        self.db.user_dynamic.set (dn [0], org_location = self.oloj)
        dr = self.db.daily_record.filter (None, dict (date = '2023-08-11'))
        assert len (dr) == 1
        dr = dr [0]
        vacation.try_create_public_holiday \
            (self.db, dr, date.Date ('2023-08-11'), self.user26)
        self.db.commit ()
        self.db.close ()
    # end def test_user26

    def setup_user27 (self) :
        self.username27 = 'testuser27'
        self.user27 = self.db.user.create \
            ( username     = self.username27
            , firstname    = 'Nummer27'
            , lastname     = 'User27'
            , supervisor   = self.user0
            , address      = 'testuser27@example.com'
            )
        p = self.db.overtime_period.create \
            ( name              = 'month average'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )
        self.db.time_wp.set ('44', bookers = [self.user27])
        self.ct_pt = self.db.contract_type.create \
            ( name  = 'part time'
            , order = 1
            )
        user27_time.import_data_27 (self.db, self.user27, self.olo, self)
        self.db.time_wp.set (self.holiday_wp, bookers = [self.user27])
        # HR-vacation role for user0
        u0 = self.db.user.getnode (self.user0)
        roles = u0.roles + ",HR-vacation"
        self.db.user.set (self.user0, roles = roles)
    # end def setup_user27

    def test_user27 (self):
        self.log.debug ('test_user27')
        self.setup_db ()
        self.setup_user27 ()
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username27)
        u0 = self.db.user.getnode (self.user0)
        print ('Roles user0: %s' % u0.roles, file = sys.stderr)
        for id in self.db.vac_aliq.getnodeids (retired = False):
            va = self.db.vac_aliq.getnode (id)
            print (va.name, file = sys.stderr)
        d = { 'daily_record.user': self.user27 }
        trids = self.db.time_record.filter (None, d)
        print ("Time records:", len (trids), file = sys.stderr)
        for id in trids:
            tr = self.db.time_record.getnode (id)
            dr = self.db.daily_record.getnode (tr.daily_record)
            print ( tr.id, dr.date, dr.status, tr.wp, tr.duration
                  , file = sys.stderr
                  )
        drids = self.db.daily_record.filter \
            ( None, dict (user = self.user27, date = '2022-01-01;')
            , sort = ('+', 'date')
            )
        print ("Daily records:", len (drids), file = sys.stderr)
        for id in drids:
            dr = self.db.daily_record.getnode (id)
            print (dr.date, dr.status, file = sys.stderr)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user' : [self.user27], 'date' : '2022-01-01;2023-12-31' }
        class r : filterspec = fs ; columns = {}
        sr = summary.Vacation_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        for j in range (4):
            for i in range (9):
                print (lines [j+1][i], file=sys.stderr)
        self.assertEqual (len (lines), 5)
        self.assertEqual (len (lines [0]), 9)
        self.assertEqual (lines  [0] [0], 'User')
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [2], 'yearly entitlement')
        self.assertEqual (lines  [0] [3], 'yearly prorated')
        self.assertEqual (lines  [0] [4], 'carry forward from previous year')
        self.assertEqual (lines  [0] [5], 'entitlement total')
        self.assertEqual (lines  [0] [6], 'approved days')
        self.assertEqual (lines  [0] [7], 'vacation corrections')
        self.assertEqual (lines  [0] [8], 'remaining vacation')
        self.assertEqual (lines  [1] [0], 'testuser27')
        self.assertEqual (lines  [1] [1], '2022-12-31')
        self.assertEqual (lines  [1] [2], '30.00')
        self.assertEqual (lines  [1] [3], '7.50')
        self.assertEqual (lines  [1] [4], '27.50')
        self.assertEqual (lines  [1] [5], '35.00')
        self.assertEqual (lines  [1] [6], '7.0')
        self.assertEqual (lines  [1] [7], '0.0')
        self.assertEqual (lines  [1] [8], '28.00')
        self.assertEqual (lines  [2] [0], 'testuser27')
        self.assertEqual (lines  [2] [1], '2023-12-31')
        self.assertEqual (lines  [2] [2], '30.00')
        self.assertEqual (lines  [2] [3], '7.50')
        self.assertEqual (lines  [2] [4], '0.00')
        self.assertEqual (lines  [2] [5], '7.50')
        self.assertEqual (lines  [2] [6], '0.0')
        self.assertEqual (lines  [2] [7], '0.0')
        self.assertEqual (lines  [2] [8], '7.50')
        self.assertEqual (lines  [3] [0], 'testuser27 / part time')
        self.assertEqual (lines  [3] [1], '2022-12-31')
        self.assertEqual (lines  [3] [2], '24.00')
        self.assertEqual (lines  [3] [3], '10.00')
        self.assertEqual (lines  [3] [4], '0.00')
        self.assertEqual (lines  [3] [5], '10.00')
        self.assertEqual (lines  [3] [6], '8.0')
        self.assertEqual (lines  [3] [7], '0.0')
        self.assertEqual (lines  [3] [8], '2.00')
        self.assertEqual (lines  [4] [0], 'testuser27 / part time')
        self.assertEqual (lines  [4] [1], '2023-12-31')
        self.assertEqual (lines  [4] [2], '24.00')
        self.assertEqual (lines  [4] [3], '16.00')
        self.assertEqual (lines  [4] [4], '2.00')
        self.assertEqual (lines  [4] [5], '18.00')
        self.assertEqual (lines  [4] [6], '2.0')
        self.assertEqual (lines  [4] [7], '')
        self.assertEqual (lines  [4] [8], '16.00')
        #assert 0
        self.db.commit ()
        self.db.close ()
    # end def test_user27

# end class Test_Case_Timetracker

class Test_Case_Tracker (_Test_Case, unittest.TestCase) :
    schemaname = 'track'
    schemafile = 'trackers'
    roles = \
        [ 'admin', 'anonymous', 'dom-user-edit-facility'
        , 'dom-user-edit-gtt', 'dom-user-edit-hr'
        , 'dom-user-edit-office', 'external'
        , 'issue_admin', 'it', 'ituser'
        , 'itview', 'kpm-admin', 'msgedit', 'msgsync', 'nosy', 'pgp'
        , 'readonly-user', 'sec-incident-nosy'
        , 'sec-incident-responsible', 'sub-login', 'supportadmin'
        , 'user', 'user_view'
        ]
    transprop_perms = transprop_track
# end class Test_Case_Tracker

class Test_Case_Fulltracker (_Test_Case_Summary, unittest.TestCase) :
    schemaname = 'full'
    roles = \
        [ 'admin', 'anonymous', 'cc-permission', 'contact', 'controlling'
        , 'doc_admin', 'dom-user-edit-facility', 'dom-user-edit-gtt'
        , 'dom-user-edit-hr', 'dom-user-edit-office'
        , 'external', 'facility', 'functional-role', 'hr'
        , 'hr-leave-approval', 'hr-org-location'
        , 'hr-vacation', 'issue_admin', 'it', 'itview'
        , 'msgedit', 'msgsync', 'nosy', 'office', 'organisation'
        , 'pgp', 'procurement', 'project', 'project_view'
        , 'sec-incident-nosy', 'sec-incident-responsible'
        , 'staff-report', 'sub-login', 'summary_view', 'supportadmin'
        , 'time-report', 'user', 'user_view', 'vacation-report'
        ]
    transprop_perms = transprop_full

    def setup_user3 (self) :
        self.username3 = 'testuser3'
        self.user3 = self.db.user.create \
            ( username     = self.username3
            , firstname    = 'NochEinTest'
            , lastname     = 'User3'
            )
        user_dynamic.user_create_magic (self.db, self.user3, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user3
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        # create initial dyn_user record for user
        ud = self.db.user_dynamic.filter (None, dict (user = self.user3))
        self.assertEqual (len (ud), 1)
        p = self.db.overtime_period.lookup ('yearly/weekly')
        self.db.user_dynamic.set \
            ( ud [0]
            , valid_from        = date.Date ('2010-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , additional_hours  = 40
            , supp_weekly_hours = 45.0
            , supp_per_period   = 84.0
            , overtime_period   = p
            , weekend_allowed   = True
            )
        self.db.commit ()
    # end def setup_user3

    def setup_user4 (self) :
        self.username4 = 'testuser4'
        self.user4 = self.db.user.create \
            ( username     = self.username4
            , firstname    = 'Nummer4'
            , lastname     = 'User4'
            )
        user_dynamic.user_create_magic (self.db, self.user4, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user4
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        # create initial dyn_user record for user
        ud = self.db.user_dynamic.filter (None, dict (user = self.user4))
        self.assertEqual (len (ud), 1)
        p = self.db.overtime_period.create \
            ( name              = 'month average'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )

        self.db.user_dynamic.set \
            ( ud [0]
            , valid_from        = date.Date ('2012-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_per_period   = 7
            , overtime_period   = p
            , weekend_allowed   = True
            )
        self.db.commit ()
    # end def setup_user4

    def setup_user5 (self) :
        self.username5 = 'testuser5'
        self.user5 = self.db.user.create \
            ( username     = self.username5
            , firstname    = 'Nummer5'
            , lastname     = 'User5'
            )
        user_dynamic.user_create_magic (self.db, self.user5, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user5
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        # public holidays
        vienna = self.db.location.lookup ('Vienna')
        hd = \
            ( ("New Year's Day", "Neujahr",             "2012-01-01")
            , ("Epiphany",       "Heilige drei K.",     "2012-01-06")
            , ("Easter Monday",  "Ostermontag",         "2012-04-09")
            , ("May Day",        "Tag der Arbeit",      "2012-05-01")
            , ("Ascension Day",  "Christi Himmelfahrt", "2012-05-17")
            , ("Pentecost",      "Pfingstsonntag",      "2012-05-27")
            , ("Pentecost",      "Pfingsmontag",        "2012-05-28")
            , ("Corpus Christi", "Fronleichnam",        "2012-06-07")
            , ("Assumption",     "Himmelfahrt",         "2012-08-15")
            )
        for name, desc, dt in hd :
            dt = date.Date (dt)
            self.db.public_holiday.create \
                ( name        = name
                , description = desc
                , date        = dt
                , locations   = [vienna]
                )
        # create initial dyn_user record for user
        ud = self.db.user_dynamic.filter (None, dict (user = self.user5))
        self.assertEqual (len (ud), 1)
        ud = self.db.user_dynamic.getnode (ud [0])
        p = self.db.overtime_period.create \
            ( name              = 'monthly average required'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )
        week = self.db.overtime_period.lookup ('week')

        self.db.user_dynamic.set \
            ( ud.id
            , valid_from        = date.Date ('2012-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_weekly_hours = 38.5
            , additional_hours  = 38.5
            , overtime_period   = week
            , weekend_allowed   = True
            )
        self.db.user_dynamic.create \
            ( user              = self.user5
            , org_location      = ud.org_location
            , valid_from        = date.Date ('2012-03-15')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_per_period   = 7
            , overtime_period   = p
            , weekend_allowed   = True
            )
        self.db.user_dynamic.create \
            ( user              = self.user5
            , org_location      = ud.org_location
            , valid_from        = date.Date ('2012-06-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_weekly_hours = 41.0
            , additional_hours  = 40.0
            , overtime_period   = week
            , weekend_allowed   = True
            )
        self.db.commit ()
    # end def setup_user5

    def setup_user6 (self) :
        self.username6 = 'testuser6'
        self.user6 = self.db.user.create \
            ( username     = self.username6
            , firstname    = 'Nummer6'
            , lastname     = 'User6'
            )
        user_dynamic.user_create_magic (self.db, self.user6, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user6
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        # create initial dyn_user record for user
        ud = self.db.user_dynamic.filter (None, dict (user = self.user6))
        self.assertEqual (len (ud), 1)
        ud = self.db.user_dynamic.getnode (ud [0])
        p = self.db.overtime_period.create \
            ( name              = 'monthly average required'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )

        self.db.user_dynamic.set \
            ( ud.id
            , valid_from        = date.Date ('2012-09-03')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_per_period   = 15.0
            , overtime_period   = p
            )
        self.db.commit ()
    # end def setup_user6

    def setup_user7 (self) :
        self.username7 = 'testuser7'
        self.user7 = self.db.user.create \
            ( username     = self.username7
            , firstname    = 'Nummer7'
            , lastname     = 'User7'
            )
        user_dynamic.user_create_magic (self.db, self.user7, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user7
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        # create initial dyn_user record for user
        ud = self.db.user_dynamic.filter (None, dict (user = self.user7))
        self.assertEqual (len (ud), 1)
        ud = self.db.user_dynamic.getnode (ud [0])
        p = self.db.overtime_period.create \
            ( name              = 'monthly average required'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )

        self.db.user_dynamic.set \
            ( ud.id
            , valid_from        = date.Date ('2012-11-15')
            , valid_to          = date.Date ('2013-05-16')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_per_period   = 15.0
            , overtime_period   = p
            )
        self.db.commit ()
    # end def setup_user7

    def setup_user8 (self) :
        self.username8 = 'testuser8'
        self.user8 = self.db.user.create \
            ( username     = self.username8
            , firstname    = 'Nummer8'
            , lastname     = 'User8'
            )
        user_dynamic.user_create_magic (self.db, self.user8, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user8
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        # create initial dyn_user record for user
        ud = self.db.user_dynamic.filter (None, dict (user = self.user8))
        self.assertEqual (len (ud), 1)
        p = self.db.overtime_period.create \
            ( name              = 'monthly average required'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )
        self.db.user_dynamic.set \
            ( ud [0]
            , valid_from        = date.Date ('2012-12-31')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_per_period   = 7.0
            , overtime_period   = p
            )
        self.db.commit ()
    # end def setup_user8

    def setup_user9 (self) :
        self.username9 = 'testuser9'
        self.user9 = self.db.user.create \
            ( username     = self.username9
            , firstname    = 'Nummer9'
            , lastname     = 'User9'
            )
        user_dynamic.user_create_magic (self.db, self.user9, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user9
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        # create initial dyn_user record for user
        ud = self.db.user_dynamic.filter (None, dict (user = self.user9))
        self.assertEqual (len (ud), 1)
        self.db.user_dynamic.set \
            ( ud [0]
            , valid_from        = date.Date ('2012-12-31')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , overtime_period   = None
            , all_in            = False
            )
        self.db.overtime_correction.create \
            ( user    = self.user9
            , value   = 45.0
            , comment = 'Test overtime correction'
            , date    = date.Date ('2013-01-01')
            )
        self.db.commit ()
    # end def setup_user9

    def setup_user10 (self) :
        self.username10 = 'testuser10'
        self.user10 = self.db.user.create \
            ( username     = self.username10
            , firstname    = 'Nummer10'
            , lastname     = 'User10'
            )
        user_dynamic.user_create_magic (self.db, self.user10, self.olo)
        self.db.user_dynamic.create \
            ( user            = self.user10
            , valid_from      = date.Date ('.')
            , org_location    = self.olo
            , vacation_yearly = 25.0
            )
        # create initial dyn_user record for user
        ud = self.db.user_dynamic.filter (None, dict (user = self.user10))
        self.assertEqual (len (ud), 1)
        ud = self.db.user_dynamic.getnode (ud [0])
        week = self.db.overtime_period.lookup ('week')
        self.db.user_dynamic.set \
            ( ud.id
            , valid_from        = date.Date ('2011-12-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_weekly_hours = 45.0
            , additional_hours  = 40.0
            , overtime_period   = week
            )
        self.db.user_dynamic.create \
            ( user              = self.user10
            , org_location      = ud.org_location
            , valid_from        = date.Date ('2012-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , overtime_period   = None
            , all_in            = True
            , max_flexitime     = 5
            )
        self.db.overtime_correction.create \
            ( user    = self.user10
            , value   = 76.38
            , comment = 'Test overtime correction'
            , date    = date.Date ('2011-12-28')
            )
        self.db.overtime_correction.create \
            ( user    = self.user10
            , value   = -76.38
            , comment = 'Test overtime correction'
            , date    = date.Date ('2012-12-28')
            )
        self.db.commit ()
    # end def setup_user10

    def test_rename_status (self) :
        self.log.debug ('test_rename_status')
        self.setup_db ()
        # test that renaming the 'New' cost_center status will still work
        ccs = self.db.cost_center_status.lookup ('New')
        self.db.cost_center_status.set (ccs, name = 'Something')
        self.cc = self.db.cost_center.create \
            ( name              = 'CC-New'
            , cost_center_group = self.ccg
            )
        # test that renaming the 'New' time_project_status will still work
        tps = self.db.time_project_status.lookup ('New')
        self.db.time_project_status.set (tps, name = 'Something')
        self.normal_tp = self.db.time_project.create \
            ( name = 'Another Project'
            , op_project        = True
            , responsible       = self.user1
            , organisation      = self.org
            , cost_center       = self.cc
            )
    # end def test_rename_status

    def test_user3 (self) :
        self.log.debug ('test_user3')
        self.setup_db ()
        self.setup_user3 ()
        self.db.close ()
        self.db = self.tracker.open (self.username3)
        user3_time.import_data_3 (self.db, self.user3)
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user'         : [self.user3]
             , 'date'         : '2010-01-01;2010-05-31'
             , 'summary_type' : ['2', '3', '4']
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (len (lines), 31)
        self.assertEqual (lines [0]  [1], 'Time Period')
        self.assertEqual (lines [0]  [6], 'Actual all')
        self.assertEqual (lines [0]  [9], 'Supplementary hours')
        self.assertEqual (lines [0] [11], 'Balance End')
        self.assertEqual (lines [0] [13], 'Achieved supplementary hours')
        self.assertEqual (lines [1]  [1], 'WW 53/2009')
        self.assertEqual (lines [2]  [1], 'WW 1/2010')
        self.assertEqual (lines [16] [6], '57.62')
        self.assertEqual (lines [16] [9], '45.00')
        self.assertEqual (lines [16][11], '12.62')
        self.assertEqual (lines [16][13], '5.00')
        self.assertEqual (lines [17] [6], '52.88')
        self.assertEqual (lines [17] [9], '45.00')
        self.assertEqual (lines [17][11], '20.50')
        self.assertEqual (lines [17][13], '10.00')
        self.assertEqual (lines [18] [1], 'WW 17/2010')
        self.assertEqual (lines [18] [6], '38.50')
        self.assertEqual (lines [18] [9], '45.00')
        self.assertEqual (lines [18][11], '20.50')
        self.assertEqual (lines [18][13], '10.00')
        self.assertEqual (lines [19] [1], 'WW 18/2010')
        self.assertEqual (lines [19] [6], '38.50')
        self.assertEqual (lines [19] [9], '45.00')
        self.assertEqual (lines [19][11], '20.50')
        self.assertEqual (lines [19][13], '10.00')
    # end def test_user3

    def test_user4 (self) :
        self.log.debug ('test_user4')
        self.setup_db ()
        self.setup_user4 ()
        self.db.close ()
        self.db = self.tracker.open (self.username4)
        user4_time.import_data_4 (self.db, self.user4)
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        dr = self.db.daily_record.filter \
            (None, dict (user = self.user4, date = '2012-05-04'))
        self.assertEqual (len (dr), 1)
        dr = self.db.daily_record.getnode (dr [0])
        tr = dr.time_record
        self.assertEqual (len (tr), 1)
        tr = self.db.time_record.getnode (tr [0])
        self.assertEqual (tr.duration, 12)
        self.assertEqual (round (tr.tr_duration, 2), round (7.804, 2))
        user_dynamic.update_tr_duration (self.db, dr)
        self.assertEqual (round (tr.tr_duration, 2), round (7.804, 2))
        summary.init (self.tracker)
        fs = { 'user'         : [self.user4]
             , 'date'         : '2012-01-01;2012-05-31'
             , 'summary_type' : ['2', '3', '4']
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (len (lines), 31)
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [6], 'Actual all')
        self.assertEqual (lines  [0] [8], 'Supp. hours average')
        self.assertEqual (lines  [0][11], 'Balance End')
        self.assertEqual (lines  [1] [1], 'WW 52/2011')
        self.assertEqual (lines  [2] [1], 'WW 1/2012')
        self.assertEqual (lines [24] [1], 'January 2012')
        self.assertEqual (lines [28] [1], 'May 2012')
        self.assertEqual (lines [29] [1], '2012-01-01;2012-05-31')
        self.assertEqual (lines  [1] [2], '0.00') # balance_start

        self.assertEqual (lines  [1] [6], '0')
        self.assertEqual (lines  [1] [8], '0.00')
        self.assertEqual (lines  [1][11], '0.00')
        self.assertEqual (lines  [2] [6], '40.00')
        self.assertEqual (lines  [2] [8], '39.77')
        self.assertEqual (lines  [2][11], '0.23')
        self.assertEqual (lines  [3] [6], '38.75')
        self.assertEqual (lines  [3] [8], '40.09')
        self.assertEqual (lines  [3][11], '-1.11')
        self.assertEqual (lines  [4] [6], '40.25')
        self.assertEqual (lines  [4] [8], '40.09')
        self.assertEqual (lines  [4][11], '-0.95')
        self.assertEqual (lines  [5] [6], '40.75')
        self.assertEqual (lines  [5] [8], '40.09')
        self.assertEqual (lines  [5][11], '-0.30')
        self.assertEqual (lines  [6] [6], '38.50')
        self.assertEqual (lines  [6] [8], '40.14')
        self.assertEqual (lines  [6][11], '-1.93')
        self.assertEqual (lines  [7] [6], '38.50')
        self.assertEqual (lines  [7] [8], '38.50')
        self.assertEqual (lines  [7][11], '-1.93')
        self.assertEqual (lines  [8] [6], '45.00')
        self.assertEqual (lines  [8] [8], '40.17')
        self.assertEqual (lines  [8][11], '2.90')
        self.assertEqual (lines  [9] [6], '41.75')
        self.assertEqual (lines  [9] [8], '40.17')
        self.assertEqual (lines  [9][11], '4.48')
        self.assertEqual (lines [10] [6], '40.75')
        self.assertEqual (lines [10] [8], '40.14')
        self.assertEqual (lines [10][11], '5.10')
        self.assertEqual (lines [11] [6], '41.75')
        self.assertEqual (lines [11] [8], '40.09')
        self.assertEqual (lines [11][11], '6.76')
        self.assertEqual (lines [12] [6], '41.75')
        self.assertEqual (lines [12] [8], '40.09')
        self.assertEqual (lines [12][11], '8.42')
        self.assertEqual (lines [13] [6], '41.25')
        self.assertEqual (lines [13] [8], '40.09')
        self.assertEqual (lines [13][11], '9.58')
        self.assertEqual (lines [14] [6], '40.00')
        self.assertEqual (lines [14] [8], '40.09')
        self.assertEqual (lines [14][11], '9.48')
        self.assertEqual (lines [15] [6], '40.75')
        self.assertEqual (lines [15] [8], '40.17')
        self.assertEqual (lines [15][11], '10.07')
        self.assertEqual (lines [16] [6], '42.50')
        self.assertEqual (lines [16] [8], '39.83')
        self.assertEqual (lines [16][11], '12.73')
        self.assertEqual (lines [17] [6], '42.75')
        self.assertEqual (lines [17] [8], '40.17')
        self.assertEqual (lines [17][11], '15.32')
        self.assertEqual (lines [18] [6], '41.75')
        self.assertEqual (lines [18] [8], '40.17')
        self.assertEqual (lines [18][11], '16.90')
        self.assertEqual (lines [19] [6], '41.55')
        self.assertEqual (lines [19] [8], '39.75')
        self.assertEqual (lines [19][11], '18.71')
        self.assertEqual (lines [20] [6], '43.00')
        self.assertEqual (lines [20] [8], '40.02')
        self.assertEqual (lines [20][11], '21.69')
        self.assertEqual (lines [21] [6], '38.50')
        self.assertEqual (lines [21] [8], '39.72')
        self.assertEqual (lines [21][11], '20.47')

        self.assertEqual (lines [24] [6], '175.25')
        self.assertEqual (lines [24] [8], '176.18')
        self.assertEqual (lines [24][11], '-0.93')
        self.assertEqual (lines [25] [6], '174.00')
        self.assertEqual (lines [25] [8], '167.08')
        self.assertEqual (lines [25][11], '5.98')
        self.assertEqual (lines [26] [6], '179.25')
        self.assertEqual (lines [26] [8], '176.25')
        self.assertEqual (lines [26][11], '8.98')
        self.assertEqual (lines [27] [6], '175.50')
        self.assertEqual (lines [27] [8], '168.42')
        self.assertEqual (lines [27][11], '16.07')
        self.assertEqual (lines [28] [6], '185.30')
        self.assertEqual (lines [28] [8], '183.64')
        self.assertEqual (lines [28][11], '17.73')
        self.assertEqual (lines [29] [6], '889.30')
        self.assertEqual (lines [29] [8], '871.57')
        self.assertEqual (lines [29][11], '17.73')
    # end def test_user4

    def test_user5 (self) :
        self.log.debug ('test_user5')
        self.setup_db ()
        self.setup_user5 ()
        self.db.close ()
        self.db = self.tracker.open (self.username5)
        user5_time.import_data_5 (self.db, self.user5)
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user'         : [self.user5]
             , 'date'         : '2012-01-01;2012-09-28'
             , 'summary_type' : ['2', '3', '4']
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 51)
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [6], 'Actual all')
        self.assertEqual (lines  [0] [8], 'Supp. hours average')
        self.assertEqual (lines  [0] [9], 'Supplementary hours')
        self.assertEqual (lines  [0][11], 'Balance End')
        self.assertEqual (lines  [0][12], 'Overtime period')
        self.assertEqual (lines  [1] [1], 'WW 52/2011')
        self.assertEqual (lines  [2] [1], 'WW 1/2012')
        self.assertEqual (lines [41] [1], 'January 2012')
        self.assertEqual (lines [49] [1], 'September 2012')
        self.assertEqual (lines [50] [1], '2012-01-01;2012-09-28')
        self.assertEqual (lines  [1] [2], '0.00') # balance_start

        # Actual all
        for n, v in enumerate \
            ((   "0.00",  "38.50",  "41.50",  "41.00",  "38.50",  "40.50"
            ,   "43.50",  "42.00",  "44.50",  "38.50",  "44.50",  "45.50"
            ,   "39.25",  "43.50",  "35.00",  "44.00",  "44.25",  "42.00"
            ,   "39.75",  "39.00",  "38.50",  "41.50",  "41.00",  "43.75"
            ,   "39.00",  "38.50",  "39.25",  "38.50",  "38.50",  "38.50"
            ,   "42.00",  "38.50",  "47.75",  "43.25",  "29.50",   "0"
            ,    "0",      "0",      "0",      "0.00", "176.25", "177.00"
            ,  "188.00", "173.00", "182.75", "169.75", "173.50", "143.00"
            ,    "0.00", "1383.25"
            )) :
            self.assertEqual (lines [n + 1][6], v)
        # Supp. hours average
        for n, v in enumerate \
            ((   "0",      "0",      "0",     "0",     "0",    "0"
            ,    "0",      "0",      "0",     "0",     "0",    "39.14"
            ,   "40.09",  "40.09",  "40.17", "39.83", "40.17", "40.17"
            ,   "39.75",  "40.02",  "39.72", "40.02", "39.41",  "0"
            ,    "0",      "0",      "0",     "0",     "0",     "0"
            ,    "0",      "0",      "0",     "0",     "0",     "0"
            ,    "0",      "0",      "0",     "0",     "0",     "0"
            ,  "173.07", "168.42", "183.34",  "0",     "0",     "0"
            ,    "0",   "1518.07"
            )) :
            self.assertEqual (lines [n + 1][8], v)
        # Supplementary hours
        for n, v in enumerate \
            ((   "0.00",  "38.50",  "38.50",  "38.50",  "38.50",  "38.50"
            ,   "38.50",  "38.50",  "38.50",  "38.50",  "38.50",  "23.10"
            ,    "0.00",   "0.00",   "0.00",   "0.00",   "0.00",   "0.00"
            ,    "0.00",   "0.00",   "0.00",   "0.00",   "8.20",  "41.00"
            ,   "41.00",  "41.00",  "41.00",  "41.00",  "41.00",  "41.00"
            ,   "41.00",  "41.00",  "41.00",  "41.00",  "41.00",  "41.00"
            ,   "41.00",  "41.00",  "41.00",  "41.00", "169.40", "161.70"
            ,   "77.00",   "0.00",   "0.00", "172.20", "180.40", "188.60"
            , "164.00", "1113.30"
            )) :
            self.assertEqual (lines [n + 1][9], v)
        for n, v in enumerate \
            ((    "0.00",    "0.00",    "3.00",    "5.50",  "5.50",  "7.50"
            ,    "12.50",   "16.00",   "22.00",   "22.00", "28.00", "34.51"
            ,    "33.67",   "37.08",   "31.92",   "36.08", "40.17", "42.00"
            ,    "42.00",   "40.98",   "39.76",   "41.24", "42.13", "44.88"
            ,    "44.88",   "44.88",   "44.88",   "44.88", "44.88", "44.88"
            ,    "45.88",   "45.88",   "52.63",   "54.88", "45.88",  "7.38"
            ,   "-31.12",  "-69.62", "-108.12", "-146.62",  "6.85", "22.15"
            ,    "37.08",   "41.67",   "41.08",   "44.88", "45.88",  "7.38"
            ,  "-146.62", "-146.62"
            )) :
            self.assertEqual (lines [n + 1][11], v)
        off = 1
        for n in range (11) :
            self.assertEqual (lines [n + off][12], "week")
        off += 11
        self.assertEqual (lines [off][12], "week, monthly average required")
        off += 1
        for n in range (10) :
            self.assertEqual (lines [n + off][12], "monthly average required")
        off += 10
        self.assertEqual (lines [off][12], "monthly average required, week")
        off += 1
        for n in range (19) :
            self.assertEqual (lines [n + off][12], "week")
        off += 19
        self.assertEqual (lines [off][12], "week, monthly average required")
        self.assertEqual (lines [off + 1][12], "monthly average required")
        self.assertEqual (lines [off + 2][12], "monthly average required")
        self.assertEqual (lines [off + 3][12], "week")
        self.assertEqual (lines [off + 4][12], "week")
        self.assertEqual (lines [off + 5][12], "week")
        self.assertEqual (lines [off + 6][12], "week")
        self.assertEqual \
            (lines [off + 7][12], "week, monthly average required, week")

        off = 1
        for n in range (11) :
            self.assertEqual (lines [off + n][14], "")
        off += 11
        self.assertEqual (lines [off]    [14], "7 => 3.82")
        self.assertEqual (lines [off + 1][14], "7 => 3.82")
        self.assertEqual (lines [off + 2][14], "7")
        off += 3
        for n in range (4) :
            self.assertEqual (lines [off + n][14], "7 => 6.67")
        off += 4
        self.assertEqual (lines [off][14], "7")
        off += 1
        for n in range (4) :
            self.assertEqual (lines [off + n][14], "7 => 6.09")
        off += 4
        for n in range (19) :
            self.assertEqual (lines [off + n][14], "")
        off += 19
        self.assertEqual (lines [off]    [14], "7 => 3.82")
        self.assertEqual (lines [off + 1][14], "7 => 6.67")
        self.assertEqual (lines [off + 2][14], "7 => 6.09")
        off += 3
        for n in range (4) :
            self.assertEqual (lines [off + n][14], "")
        off += 4
        self.assertEqual (lines [off]    [14], "7")
    # end def test_user5

    def test_user6 (self) :
        self.log.debug ('test_user6')
        self.setup_db ()
        self.setup_user6 ()
        self.db.close ()
        self.db = self.tracker.open (self.username6)
        user6_time.import_data_6 (self.db, self.user6)
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user'         : [self.user6]
             , 'date'         : '2012-09-01;2012-10-08'
             , 'summary_type' : ['2', '3', '4']
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 11)
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [6], 'Actual all')
        self.assertEqual (lines  [0] [8], 'Supp. hours average')
        self.assertEqual (lines  [0] [9], 'Supplementary hours')
        self.assertEqual (lines  [0][11], 'Balance End')
        self.assertEqual (lines  [0][12], 'Overtime period')
        self.assertEqual (lines  [1] [1], 'WW 35/2012')
        self.assertEqual (lines  [8] [1], 'September 2012')
        self.assertEqual (lines  [9] [1], 'October 2012')
        self.assertEqual (lines [10] [1], '2012-09-01;2012-10-08')
        self.assertEqual (lines  [1] [2], '0.00') # balance_start
        self.assertEqual (lines [10][11], '9.59') # balance_end
    # end def test_user6

    def test_user7 (self) :
        self.log.debug ('test_user7')
        self.setup_db ()
        self.setup_user7 ()
        self.db.close ()
        self.db = self.tracker.open (self.username7)
        user7_time.import_data_7 (self.db, self.user7)
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user'         : [self.user7]
             , 'date'         : '2012-11-15;2012-12-18'
             , 'summary_type' : ['2', '3', '4']
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 10)
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [6], 'Actual all')
        self.assertEqual (lines  [0] [8], 'Supp. hours average')
        self.assertEqual (lines  [0] [9], 'Supplementary hours')
        self.assertEqual (lines  [0][11], 'Balance End')
        self.assertEqual (lines  [0][12], 'Overtime period')
        self.assertEqual (lines  [1] [1], 'WW 46/2012')
        self.assertEqual (lines  [7] [1], 'November 2012')
        self.assertEqual (lines  [8] [1], 'December 2012')
        self.assertEqual (lines  [9] [1], '2012-11-15;2012-12-18')
        self.assertEqual (lines  [7] [7], '92.25')
        self.assertEqual (lines  [7] [8], '100.43')
        self.assertEqual (lines  [1] [2], '0.00') # balance_start
        self.assertEqual (lines  [9][11], '3.80') # balance_end
    # end def test_user7

    def test_user8 (self) :
        self.log.debug ('test_user8')
        self.setup_db ()
        self.setup_user8 ()
        self.db.close ()
        self.db = self.tracker.open (self.username8)
        user8_time.import_data_8 (self.db, self.user8)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user'         : [self.user8]
             , 'date'         : '2013-01-01;2013-01-16'
             , 'summary_type' : ['2', '3', '4']
             }
        class r : filterspec = fs
        self.user8_staff_report (r, '-0.33', '2.32')
        self.db.close ()

        self.db = self.tracker.open (self.username8)
        ud = self.db.user_dynamic.filter (None, dict (user = self.user8))
        self.assertEqual (len (ud), 1)
        self.db.user_dynamic.set (ud [0], valid_from = date.Date ('2012-12-24'))
        self.db.user_dynamic.create \
            ( org_location      = self.olo
            , user              = self.user8
            , valid_from        = date.Date ('2012-12-17')
            , valid_to          = date.Date ('2012-12-24')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , additional_hours  = 40
            , supp_weekly_hours = 42
            , overtime_period   = self.db.overtime_period.lookup ('week')
            )
        dr = self.db.daily_record.create \
            ( user = self.user8
            , date = date.Date ('2012-12-28')
            )
        trn = self.db.time_record.create \
            ( daily_record  = dr
            , duration      = 8.0
            , wp            = '5'
            )
        self.db.attendance_record.create \
            ( daily_record  = dr
            , time_record   = trn
            , work_location = '5'
            )
        f = self.db.daily_record_freeze.create \
            ( user           = self.user8
            , frozen         = True
            , date           = date.Date ('2012-12-31')
            )
        self.db.commit ()
        f = self.db.daily_record_freeze.getnode (f)
        self.assertEqual (f.validity_date.pretty (common.ymd), "2012-12-31")
        self.db.close ()

        self.db = self.tracker.open (self.username0)
        self.user8_staff_report (r, '-71.00', '-68.35')
    # end def test_user8

    def user8_staff_report (self, r, balance_start, balance_end) :
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 6)
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [6], 'Actual all')
        self.assertEqual (lines  [0] [8], 'Supp. hours average')
        self.assertEqual (lines  [0] [9], 'Supplementary hours')
        self.assertEqual (lines  [0][11], 'Balance End')
        self.assertEqual (lines  [0][12], 'Overtime period')
        self.assertEqual (lines  [1] [1], 'WW 1/2013')
        self.assertEqual (lines  [4] [1], 'January 2013')
        self.assertEqual (lines  [5] [1], '2013-01-01;2013-01-16')
        self.assertEqual (lines  [4] [7], '92.50')
        self.assertEqual (lines  [4] [8], '95.85')
        self.assertEqual (lines  [1] [2], balance_start)
        self.assertEqual (lines  [5][11], balance_end)
    # end def user8_staff_report

    def test_user9 (self) :
        self.log.debug ('test_user9')
        self.setup_db ()
        self.setup_user9 ()
        self.db.close ()
        self.db = self.tracker.open (self.username9)
        # No typo: Re-use data from user8
        user8_time.import_data_8 (self.db, self.user9)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user'         : [self.user9]
             , 'date'         : '2013-01-01;2013-01-16'
             , 'summary_type' : ['2', '3', '4']
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 6)
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [6], 'Actual all')
        self.assertEqual (lines  [0] [8], 'Supp. hours average')
        self.assertEqual (lines  [0] [9], 'Supplementary hours')
        self.assertEqual (lines  [0][10], 'Overtime correction')
        self.assertEqual (lines  [0][11], 'Balance End')
        self.assertEqual (lines  [0][12], 'Overtime period')
        self.assertEqual (lines  [1] [1], 'WW 1/2013')
        self.assertEqual (lines  [1][10], '45.0')
        self.assertEqual (lines  [4] [1], 'January 2013')
        self.assertEqual (lines  [5] [1], '2013-01-01;2013-01-16')
        self.assertEqual (lines  [5][10], '45.0')
        self.assertEqual (lines  [4] [7], '0.00')
        self.assertEqual (lines  [4] [8], '0')
        self.assertEqual (lines  [1] [2], '0.00')
        self.assertEqual (lines  [5][11], '45.00')
    # end def test_user9

    def test_user10 (self) :
        self.log.debug ('test_user10')
        self.setup_db ()
        self.setup_user10 ()
        self.db.close ()
        self.db = self.tracker.open (self.username10)
        user10_time.import_data_10 (self.db, self.user10)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user'         : [self.user10]
             , 'date'         : '2012-12-01;2013-01-31'
             , 'summary_type' : ['2', '3', '4']
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 14)
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [2], 'Balance Start')
        self.assertEqual (lines  [0] [6], 'Actual all')
        self.assertEqual (lines  [0] [7], 'required')
        self.assertEqual (lines  [0] [8], 'Supp. hours average')
        self.assertEqual (lines  [0] [9], 'Supplementary hours')
        self.assertEqual (lines  [0][10], 'Overtime correction')
        self.assertEqual (lines  [0][11], 'Balance End')
        self.assertEqual (lines  [0][12], 'Overtime period')
        self.assertEqual (lines  [1] [1], 'WW 48/2012')
        self.assertEqual (lines  [5][10], '-76.38')
        self.assertEqual (lines [11] [1], 'December 2012')
        self.assertEqual (lines [12] [1], 'January 2013')
        self.assertEqual (lines [13] [1], '2012-12-01;2013-01-31')
        self.assertEqual (lines [13][10], '-76.38')
        self.assertEqual (lines  [1] [7], '0.00')
        self.assertEqual (lines [13] [7], '0.00')
        self.assertEqual (lines  [1] [8], '0')
        self.assertEqual (lines [13] [8], '0')
        self.assertEqual (lines  [1] [9], '0.00')
        self.assertEqual (lines [13] [9], '0.00')
        self.assertEqual (lines  [1] [2], '76.38')
        self.assertEqual (lines [13] [2], '76.38')
        self.assertEqual (lines [13][11], '0.00')
    # end def test_user10

    def test_extproperty (self) :
        self.log.debug ('test_extproperty')
        class Request :
            """ Fake html request """
            rfile = None
            def start_response (self, a, b) :
                pass
        # end class Request
        self.setup_db ()
        dr = self.db.daily_record.create \
            ( user = self.user1
            , date = date.Date ('2009-12-08')
            )
        tr = self.db.time_record.create \
            ( daily_record  = dr
            , duration      = 2.0
            , wp            = '1'
            )
        self.db.attendance_record.create \
            ( daily_record  = dr
            , time_record   = tr
            , work_location = '5'
            )
        request      = Request ()
        env          = dict (PATH_INFO = '', REQUEST_METHOD = 'GET')
        cli          = self.tracker.Client (self.tracker, request, env, None)
        cli.db       = self.db
        cli.language = None
        cli.userid   = self.db.getuid ()
        hcit         = templating.HTMLItem (cli, 'time_record', '1')
        dr           = hcit.daily_record
        wp           = hcit.wp
        utils        = templating.TemplatingUtils (cli)
        e = utils.ExtProperty \
            ( utils, hcit.duration, item = hcit
            , searchable = True
            , force_link = True
            )
        r = '<a tabindex="-1" class="run" href="time_record1">2.0</a>'
        self.assertEqual (e.as_listentry (), r)
        e = utils.ExtProperty \
            ( utils, hcit.duration, item = hcit
            , searchable  = True
            , force_link  = True
            , displayprop = 'id'
            )
        r = '<a tabindex="-1" class="run" href="time_record1">1</a>'
        self.assertEqual (e.as_listentry (), r)
        e = utils.ExtProperty \
            ( utils, dr
            , searchable = True
            )
        r = '<a tabindex="-1" class="" href="daily_record1">2009-12-08</a>'
        self.assertEqual (e.as_listentry (), r)
        e = utils.ExtProperty \
            ( utils, dr
            , searchname = 'daily_record.id'
            , searchable = True
            )
        r = '<a tabindex="-1" class="" href="daily_record1">1</a>'
        self.assertEqual (e.as_listentry (), r)
        e = utils.ExtProperty \
            ( utils, dr
            , searchname = 'daily_record.user'
            , searchable = True
            )
        r = '<a tabindex="-1" class="" href="user5">testuser1</a>'
        self.assertEqual (e.as_listentry (), r)
        e = utils.ExtProperty \
            ( utils, dr
            , searchname = 'daily_record.user.id'
            , searchable = False
            )
        r = '<a tabindex="-1" class="" href="user5">5</a>'
        self.assertEqual (e.as_listentry (), r)
        e = utils.ExtProperty \
            ( utils, wp
            , searchname = 'wp.id'
            , searchable = False
            )
        r = '<a tabindex="-1" class="" href="time_wp1">1</a>'
        self.assertEqual (e.as_listentry (), r)
    # end def test_extproperty

    def test_maturity_index (self) :
        self.log.debug ('test_maturity_index')
        self.db = self.tracker.open ('admin')
        d = dict \
            ( username = 'user'
            , status = self.db.user_status.lookup ('system')
            , roles = 'User,Nosy'
            )
        if 'firstname' in self.db.user.properties :
            d ['firstname'] = d ['lastname'] = 'm.i.user'
        user = self.db.user.create (** d)
        pending = self.db.category.lookup ('pending')
        self.db.category.set (pending, responsible = user)
        self.db.commit ()
        self.db.clearCache ()
        self.db.close ()
        self.db = self.tracker.open ('user')
        opn = self.db.status.lookup ('open')
        m1 = self.db.msg.create (content="new issue", subject="new issue")
        m2 = self.db.msg.create (content="Mistaken", subject="Mistaken")
        mc = self.db.issue.create \
            ( title          = "Master Container"
            , messages       = [m1]
            , release        = 'None'
            , status         = opn
            , effort_hours   = 8
            , category       = pending
            )
        c1 = self.db.issue.create \
            ( title          = "Container"
            , messages       = [m1]
            , release        = 'None'
            , status         = opn
            , effort_hours   = 8
            , category       = pending
            , part_of        = mc
            )
        self.assertEqual (self.db.issue.get (c1, 'status'), opn)
        self.assertEqual (self.db.issue.get (c1, 'maturity_index'), 5.0)
        c2 = self.db.issue.create \
            ( title          = "Container"
            , messages       = [m1]
            , release        = 'None'
            , status         = opn
            , effort_hours   = 8
            , category       = pending
            , part_of        = mc
            )
        self.assertEqual (self.db.issue.get (c2, 'status'), opn)
        self.assertEqual (self.db.issue.get (c2, 'maturity_index'), 5.0)
        i1 = self.db.issue.create \
            ( title    = "Issue no. 1"
            , messages = [m1]
            , release  = '1'
            , status   = opn
            , part_of  = c1
            )
        self.assertEqual (self.db.issue.get (c1, 'maturity_index'), 10.0)
        i2 = self.db.issue.create \
            ( title    = "Issue no. 2"
            , messages = [m1]
            , release  = '2'
            , status   = opn
            , part_of  = c1
            )
        self.assertEqual (self.db.issue.get (c1, 'maturity_index'), 20.0)
        i3 = self.db.issue.create \
            ( title    = "Issue no. 3"
            , messages = [m1]
            , release  = '3'
            , status   = opn
            , part_of  = c2
            )
        self.db.commit ()
        self.assertEqual (self.db.issue.get (i1, 'maturity_index'), 10.0)
        self.assertEqual (self.db.issue.get (i2, 'maturity_index'), 10.0)
        self.assertEqual (self.db.issue.get (i3, 'maturity_index'), 10.0)
        self.assertEqual (self.db.issue.get (c1, 'maturity_index'), 20.0)
        self.assertEqual (self.db.issue.get (c2, 'maturity_index'), 10.0)
        self.assertEqual (self.db.issue.get (mc, 'maturity_index'), 30.0)

        self.db.issue.set (i1, part_of = c2)
        self.assertEqual (self.db.issue.get (i1, 'maturity_index'), 10.0)
        self.assertEqual (self.db.issue.get (c1, 'maturity_index'), 10.0)
        self.assertEqual (self.db.issue.get (c2, 'maturity_index'), 20.0)
        self.assertEqual (self.db.issue.get (mc, 'maturity_index'), 30.0)

        # close
        mistaken = self.db.kind.lookup ('Mistaken')
        self.db.issue.set (i1, kind = mistaken, messages = [m1, m2])
        self.assertEqual (self.db.issue.get (i1, 'maturity_index'),  0.0)
        self.assertEqual (self.db.issue.get (c2, 'maturity_index'), 10.0)
        self.assertEqual (self.db.issue.get (mc, 'maturity_index'), 20.0)

        self.db2 = self.tracker.open ('user')
        self.db2.issue.get (c1, 'maturity_index')
        self.db2.issue.get (c2, 'maturity_index')
        self.db2.commit ()

        self.db.commit ()

        # concurrency: check that we don't cache values over commits
        self.assertEqual (self.db2.issue.get (c1, 'maturity_index'), 10.0)
        self.assertEqual (self.db2.issue.get (c2, 'maturity_index'), 10.0)
        self.assertEqual (self.db2.issue.get (mc, 'maturity_index'), 20.0)
        self.db2.issue.set (i3, part_of = c1)
        self.db2.commit ()
        self.assertEqual (self.db2.issue.get (c1, 'maturity_index'), 20.0)
        self.assertEqual (self.db2.issue.get (c2, 'maturity_index'),  0.0)
        self.assertEqual (self.db2.issue.get (mc, 'maturity_index'), 20.0)
    # end def test_maturity_index

    def test_tr_duration (self) :
        self.log.debug ('test_tr_duration')
        trid = '4'
        self.setup_db ()
        self.db.close ()
        self.db = None
        self.db = self.tracker.open (self.username1)
        user1_time.import_data_1 (self.db, self.user1)
        self.db.close ()
        self.db = self.tracker.open ('admin')

        self.db.time_record.set (trid, duration = 7)
        self.db.time_record.set (trid, duration = 8)
        drid = self.db.time_record.get (trid, 'daily_record')
        self.db.commit ()
        self.db.clearCache ()

        trok = self.db.daily_record.get (drid, 'tr_duration_ok')
        self.assertEqual (trok, 8)
        self.assertEqual (self.db.time_record.get (trid, 'duration'), 8)
        self.assertEqual (self.db.time_record.get (trid, 'tr_duration'), 8)
        l1 = len (self.db.getjournal ('daily_record', drid))
        self.db.clearCache ()

        dr = self.db.daily_record.getnode (drid)
        user_dynamic.update_tr_duration (self.db, dr)
        self.db.commit ()
        self.db.clearCache ()
        l2 = len (self.db.getjournal ('daily_record', drid))
        self.assertEqual (self.db.time_record.get (trid, 'duration'), 8)
        self.assertEqual (self.db.time_record.get (trid, 'tr_duration'), 8)
        self.assertEqual (self.db.daily_record.get (drid, 'tr_duration_ok'), 8)
        # No change in history with update_tr_duration: tr_duration_ok
        # has already been computed when setting time_record
        self.assertEqual (l1, l2)
    # end def test_tr_duration
# end class Test_Case_Fulltracker

class Test_Case_Concurrency (_Test_Base, _Test_Base_Summary, unittest.TestCase) :
    schemaname = 'full'
    backend = 'postgresql'

    def concurrency (self, method) :
        """ Ensure that no cached values from previous transaction are used.
            It is no concurrency test (which would fail due to a
            concurrent update) in the sense that we have two concurrent
            transactions.
        """
        trid = '4'
        self.setup_db ()
        self.db.close ()
        self.db = None
        self.db = self.tracker.open (self.username1)
        user1_time.import_data_1 (self.db, self.user1)
        self.db.close ()
        self.db  = None

        self.db1 = self.tracker.open ('admin')
        self.db2 = self.tracker.open ('admin')
        self.db1.time_record.set (trid, duration = 7)
        self.db1.time_record.set (trid, duration = 8)
        drid = self.db1.time_record.get (trid, 'daily_record')
        tr_d1 = self.db1.time_record.get  (trid, 'tr_duration')
        dr_d1 = self.db1.daily_record.get (drid, 'tr_duration_ok')
        self.log.debug ("db1.commit after time_record.set")
        self.db1.commit ()

        dr  = self.db2.daily_record.getnode (drid)
        dud = dr.tr_duration_ok
        tr  = self.db2.time_record.getnode (trid)
        dut = tr.tr_duration
        self.log.debug ("db2.commit - 1 after get")
        self.db2.commit ()
        user_dynamic.update_tr_duration (self.db2, dr)
        self.log.debug ("db2.commit - 2 after update_tr_duration")
        l2 = len (self.db2.getjournal ('daily_record', drid))
        self.db2.commit ()

        l1 = len (self.db1.getjournal ('daily_record', drid))
        self.db1.commit ()

        # Since the update happened immediately after transaction in d1,
        # the update_tr_duration did nothing and we should not see a
        # different count here.
        self.assertEqual (l1, l2)

        self.log.debug ("before method")
        method (drid, trid)
        self.log.debug ("after  method")
        self.db1.commit ()

        self.db1.clearCache ()

        # Verify that the history has grown and that the last element in
        # the history is value 'None' -- means that the tr_duration_ok
        # was set to None by some auditor and was automagically
        # recomputed by the reactor, resulting in the *previous* value
        # (the one in the journal) to be None
        j  = list \
            ( sorted
                ( self.db1.getjournal ('daily_record', drid)
                , key = lambda x : x [1]
                )
            )
        l3 = len (j)
        self.assertEqual (l3 > l1, True)
        self.assertEqual (j [-1][-1]['tr_duration_ok'], None)
        self.assertEqual \
            ( self.db1.daily_record.get (drid, 'tr_duration_ok') is not None
            , True
            )
    # end def concurrency

    def concurrency_create (self, drid, trid) :
        self.db1.time_record.create (duration = 5, daily_record = drid)
    # end def concurrency_set

    def concurrency_retire (self, drid, trid) :
        self.db1.time_record.set (trid, duration = None)
    # end def concurrency_set

    def concurrency_set (self, drid, trid) :
        self.db1.time_record.set (trid, duration = 5)
    # end def concurrency_set

    def test_concurrency_create (self) :
        self.log.debug ('test_concurrency_create')
        self.concurrency (self.concurrency_create)
    # end def test_concurrency_create

    def test_concurrency_retire (self) :
        self.log.debug ('test_concurrency_retire')
        self.concurrency (self.concurrency_retire)
    # end def test_concurrency_retire

    def test_concurrency_set (self) :
        self.log.debug ('test_concurrency_set')
        self.concurrency (self.concurrency_set)
    # end def test_concurrency_set

    def test_user1 (self) :
        self.log.debug ('test_user1')
        self.setup_db ()
        self.db.close ()
        self.db = self.tracker.open (self.username1)
        user1_time.import_data_1 (self.db, self.user1)
        self.db.close ()
        self.db = self.tracker.open ('admin')
        self.db.overtime_correction.create \
            ( user    = self.user1
            , value   = 910.0
            , comment = 'Auf null stellen, da keine Eintraege'
            , date    = date.Date ('2008-09-07')
            )
        dr = self.db.daily_record.filter \
            (None, dict (user = self.user1, date = '2006-01-23')) [0]
        dr = self.db.daily_record.getnode (dr)
        user_dynamic.update_tr_duration (self.db, dr)
        self.assertEqual (dr.tr_duration_ok, 0)
        self.db.user_dynamic.create \
            ( user              = self.user1
            , valid_from        = date.Date ('2006-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = True
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , daily_worktime    = 0.0
            , org_location      = self.olo
            , max_flexitime     = 5
            )
        self.db.clearCache ()
        self.assertEqual (dr.tr_duration_ok, 0)
        self.db.user_dynamic.create \
            ( user              = self.user1
            , valid_from        = date.Date ('2008-01-01')
            , valid_to          = date.Date ('2008-09-11')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 5.0
            , hours_tue         = 5.0
            , hours_wed         = 5.0
            , hours_thu         = 5.0
            , hours_fri         = 5.0
            , daily_worktime    = 0.0
            , supp_weekly_hours = 25.
            , org_location      = self.olo
            , overtime_period   = self.db.overtime_period.lookup ('week')
            )
        self.db.user_dynamic.create \
            ( user              = self.user1
            , valid_from        = date.Date ('2009-01-04')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = True
            , hours_mon         = 2.0
            , hours_tue         = 2.0
            , hours_wed         = 2.0
            , hours_thu         = 2.0
            , hours_fri         = 2.0
            , daily_worktime    = 0.0
            , org_location      = self.olo
            , max_flexitime     = 5
            )
        self.db.user_dynamic.create \
            ( user              = self.user1
            , valid_from        = date.Date ('2010-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = True
            , hours_mon         = 2.0
            , hours_tue         = 2.0
            , hours_wed         = 2.0
            , hours_thu         = 2.0
            , hours_fri         = 2.0
            , daily_worktime    = 0.0
            , org_location      = self.olo
            , max_flexitime     = 5
            )
        self.db.commit ()
        self.db.close  ()
        self.db = self.tracker.open (self.username1)
        fs = { 'user'         : [self.user1]
             , 'date'         : '2008-09-01;2008-09-10'
             , 'summary_type' : ['2', '4']
             }
        class r : filterspec = fs
        summary.init (self.tracker)
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (len (lines), 5)
        self.assertEqual (lines [0] [0], 'User')
        self.assertEqual (lines [0] [1], 'Time Period')
        self.assertEqual (lines [0] [2], 'Balance Start')
        self.assertEqual (lines [0] [3], 'Actual open')
        self.assertEqual (lines [0] [4], 'Actual submitted')
        self.assertEqual (lines [0] [5], 'Actual accepted')
        self.assertEqual (lines [0] [6], 'Actual all')
        self.assertEqual (lines [0] [7], 'required')
        self.assertEqual (lines [0] [8], 'Supp. hours average')
        self.assertEqual (lines [0] [9], 'Supplementary hours')
        self.assertEqual (lines [0][10], 'Overtime correction')
        self.assertEqual (lines [0][11], 'Balance End')
        self.assertEqual (lines [0][12], 'Overtime period')
        self.assertEqual (lines [1] [1], 'WW 36/2008')
        self.assertEqual (lines [2] [1], 'WW 37/2008')
        self.assertEqual (lines [3] [1], '2008-09-01;2008-09-10')
        self.assertEqual (lines [1][11], '-23.50')
        self.assertEqual (lines [2][11], '-38.50')
        self.assertEqual (lines [3][11], '-38.50')
        self.assertEqual (lines [3][10], '910.0')
        fs = { 'user'         : [self.user1]
             , 'date'         : '2009-12-21;2010-01-03'
             , 'summary_type' : ['2', '4']
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (lines [1] [1], 'WW 52/2009')
        self.assertEqual (lines [2] [1], 'WW 53/2009')
        self.assertEqual (lines [3] [1], '2009-12-21;2010-01-03')
        self.assertEqual (lines [1][11], '-38.50')
        self.assertEqual (lines [2][11], '-38.50')
        self.assertEqual (lines [3][11], '-38.50')

        for d in ('2006-12-31', '2007-12-31') :
            f = self.db.daily_record_freeze.create \
                ( user           = self.user1
                , frozen         = True
                , date           = date.Date (d)
                )
            f = self.db.daily_record_freeze.getnode (f)
            self.assertEqual (f.balance,        -38.5)
            self.assertEqual (f.achieved_hours, 0.0)
            self.assertEqual (f.validity_date,  date.Date (d))

        f = self.db.daily_record_freeze.create \
            ( user           = self.user1
            , frozen         = True
            , date           = date.Date ('2008-09-10')
            )
        f = self.db.daily_record_freeze.getnode (f)
        self.assertEqual (f.balance,       -23.5)
        self.assertEqual (f.achieved_hours,  0.0)
        self.assertEqual (f.validity_date,  date.Date ('2008-09-07'))

        dyn = user_dynamic.first_user_dynamic (self.db, self.user1)
        self.assertEqual (dyn.valid_from, date.Date ('2005-09-01'))
        op  = user_dynamic.overtime_periods \
            (self.db, self.user1, dyn.valid_from, date.Date ('2009-12-31'))
        self.assertEqual (len (op), 1)
        self.assertEqual (op [0][0], date.Date ('2005-10-01'))
        self.assertEqual (op [0][1], date.Date ('2008-09-10'))
        self.assertEqual (op [0][2].name, 'week')
        dyn = user_dynamic.next_user_dynamic (self.db, dyn)
        self.assertEqual (dyn.valid_from, date.Date ('2005-10-01'))
        dyn = user_dynamic.next_user_dynamic (self.db, dyn)
        self.assertEqual (dyn.valid_from, date.Date ('2006-01-01'))
        self.assertEqual (dyn.overtime_period, None)

        bal = user_dynamic.compute_balance \
            (self.db, self.user1, date.Date ('2009-12-31'), sharp_end = True)
        self.assertEqual (bal, (-38.5, 0))
        bal = user_dynamic.compute_balance \
            (self.db, self.user1, date.Date ('2009-12-27'), sharp_end = True)
        self.assertEqual (bal, (-38.5, 0))
        bal = user_dynamic.compute_balance \
            (self.db, self.user1, date.Date ('2010-01-03'), sharp_end = True)
        self.assertEqual (bal, (-38.5, 0))

        bal = user_dynamic.compute_balance \
            (self.db, self.user1, date.Date ('2009-12-31'), not_after = True)
        self.assertEqual (bal, (-38.5, 0))
        bal = user_dynamic.compute_balance \
            (self.db, self.user1, date.Date ('2009-12-27'), not_after = True)
        self.assertEqual (bal, (-38.5, 0))
        bal = user_dynamic.compute_balance \
            (self.db, self.user1, date.Date ('2010-01-03'), not_after = True)
        self.assertEqual (bal, (-38.5, 0))

        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (lines [1] [1], 'WW 52/2009')
        self.assertEqual (lines [2] [1], 'WW 53/2009')
        self.assertEqual (lines [3] [1], '2009-12-21;2010-01-03')
        self.assertEqual (lines [1][11], '-38.50')
        self.assertEqual (lines [2][11], '-38.50')
        self.assertEqual (lines [3][11], '-38.50')

        f = self.db.daily_record_freeze.create \
            ( user           = self.user1
            , frozen         = True
            , date           = date.Date ('2009-12-31')
            )
        f = self.db.daily_record_freeze.getnode (f)
        self.assertEqual (f.balance,        -38.5)
        self.assertEqual (f.achieved_hours,   0.0)
        self.assertEqual (f.validity_date,  date.Date ('2009-12-31'))

        self.db.daily_record_freeze.set (f.id, frozen = False)
        self.assertEqual (f.balance, None)
        self.db.daily_record_freeze.set (f.id, frozen = True)

        self.db.clearCache ()
        self.assertEqual (f.balance,      -38.5)
        self.assertEqual (f.achieved_hours, 0.0)
        self.assertEqual (f.validity_date,  date.Date ('2009-12-31'))

        self.db.clearCache ()

        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (lines [1] [1], 'WW 52/2009')
        self.assertEqual (lines [2] [1], 'WW 53/2009')
        self.assertEqual (lines [3] [1], '2009-12-21;2010-01-03')
        self.assertEqual (lines [1][11], '-38.50')
        self.assertEqual (lines [2][11], '-38.50')
        self.assertEqual (lines [3][11], '-38.50')
    # end def test_user1

    def test_user2 (self) :
        self.log.debug ('test_user2')
        self.setup_db ()
        self.db.close ()
        self.db = self.tracker.open (self.username2)
        user2_time.import_data_2 (self.db, self.user2)
        self.db.close ()
        self.db = self.tracker.open ('admin')
        self.db.user_dynamic.create \
            ( user              = self.user2
            , valid_from        = date.Date ('2009-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_weekly_hours = 38.5
            , additional_hours  = 38.5
            , overtime_period   = self.db.overtime_period.lookup ('week')
            , org_location      = self.olo
            )
        f = self.db.daily_record_freeze.create \
            ( user           = self.user2
            , frozen         = True
            , date           = date.Date ('2008-12-31')
            )
        f = self.db.daily_record_freeze.getnode (f)
        self.assertEqual (f.balance,        0.0)
        self.assertEqual (f.achieved_hours, 0.0)
        self.assertEqual (f.validity_date,  date.Date ('2008-12-31'))
        self.db.commit ()
        self.db.close  ()
        self.db = self.tracker.open (self.username2)
        fs = { 'user'         : [self.user2]
             , 'date'         : '2008-12-22;2009-01-04'
             , 'summary_type' : ['2', '4']
             }
        class r : filterspec = fs
        summary.init (self.tracker)
        ndr = self.db.daily_record.getnode ('51')
        self.assertEqual (len (ndr.time_record), 2)
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (len (lines), 5)
        self.assertEqual (lines [1] [1], 'WW 52/2008')
        self.assertEqual (lines [2] [1], 'WW 1/2009')
        self.assertEqual (lines [3] [1], '2008-12-22;2009-01-04')
        self.assertEqual (lines [1][11], '0.00')
        self.assertEqual (lines [2][11], '0.00')
        self.assertEqual (lines [3][11], '0.00')

        fs = { 'user'         : [self.user2]
             , 'date'         : '2009-12-21;2010-01-03'
             , 'summary_type' : ['2', '4']
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (len (lines), 5)
        self.assertEqual (lines [1] [1], 'WW 52/2009')
        self.assertEqual (lines [2] [1], 'WW 53/2009')
        self.assertEqual (lines [3] [1], '2009-12-21;2010-01-03')
        self.assertEqual (lines [1][11], '113.12')
        self.assertEqual (lines [2][11], '113.12')
        self.assertEqual (lines [3][11], '113.12')
        f = self.db.daily_record_freeze.create \
            ( user           = self.user2
            , frozen         = True
            , date           = date.Date ('2009-12-31')
            )
        f = self.db.daily_record_freeze.getnode (f)
        self.assertEqual (f.balance,        113.125)
        self.assertEqual (f.achieved_hours, 0.0)
        self.assertEqual (f.validity_date,  date.Date ('2009-12-27'))
        # test split of frozen dyn record and reset of tr_duration
        dr1 = self.db.daily_record.filter \
            (None, dict (user = self.user2, date = '2009-12-31')) [0]
        dr1 = self.db.daily_record.getnode (dr1)
        user_dynamic.update_tr_duration (self.db, dr1)
        self.assertEqual (dr1.tr_duration_ok, 7.75)
        dr2 = self.db.daily_record.filter \
            (None, dict (user = self.user2, date = '2010-01-01')) [0]
        dr2 = self.db.daily_record.getnode (dr2)
        user_dynamic.update_tr_duration (self.db, dr2)
        self.assertEqual (dr2.tr_duration_ok, 7.5)
        # Get len of journal
        l1_1 = len (self.db.getjournal ('daily_record', dr1.id))
        l2_1 = len (self.db.getjournal ('daily_record', dr2.id))
        self.db.user_dynamic.create \
            ( user              = self.user2
            , valid_from        = date.Date ('2010-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25.0
            , all_in            = False
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , supp_weekly_hours = 38.5
            , additional_hours  = 38.5
            , overtime_period   = self.db.overtime_period.lookup ('week')
            , org_location      = self.olo
            )
        self.db.clearCache ()
        self.assertEqual (dr1.tr_duration_ok, 7.75)
        self.assertEqual (dr2.tr_duration_ok, 7.5)
        # Get len of journal, tr_duration_ok should have been recomputed
        l1_2 = len (self.db.getjournal ('daily_record', dr1.id))
        l2_2 = len (self.db.getjournal ('daily_record', dr2.id))
        # Rec dr1 was *not* updated
        self.assertEqual (l1_1, l1_2)
        # Rec dr2 *was* updated due to update of user_dynamic. Since
        # the *old* user_dynamic record was changed *and* the new one
        # was created we have more than two updates.
        self.assertEqual (l2_2 - l2_1 >= 4, True)
    # end def test_user2

# end class Test_Case_Concurrency

class Test_Case_Abo (_Test_Case, unittest.TestCase) :
    schemaname = 'abo'
    roles = \
        [ 'abo', 'admin', 'adr_readonly', 'anonymous', 'contact'
        , 'invoice', 'letter', 'product', 'type', 'user', 'user_view'
        ]
    transprop_perms = transprop_abo
# end class Test_Case_Abo

class Test_Case_Adr (_Test_Case, unittest.TestCase) :
    schemaname = 'adr'
    roles = \
        [ 'admin', 'adr_readonly', 'anonymous', 'contact', 'letter'
        , 'type', 'user', 'user_view'
        ]
    transprop_perms = transprop_adr
# end class Test_Case_Adr

class Test_Case_ERP (_Test_Case, unittest.TestCase) :
    schemaname = 'erp'
    roles = \
        [ 'admin', 'adr_readonly', 'anonymous', 'contact', 'discount'
        , 'invoice', 'letter', 'product', 'type', 'user'
        ]
    transprop_perms = transprop_erp
# end class Test_Case_ERP

class Test_Case_IT (_Test_Case, unittest.TestCase) :
    schemaname = 'it'
    roles = \
        [ 'admin', 'anonymous'
        , 'it', 'ituser', 'itview', 'nosy'
        , 'sec-incident-nosy', 'sec-incident-responsible'
        , 'user', 'user_view'
        ]
# end class Test_Case_IT

class Test_Case_ITAdr (_Test_Case, unittest.TestCase) :
    schemaname = 'itadr'
    roles = \
        [ 'admin', 'adr_readonly', 'anonymous', 'contact', 'it'
        , 'itview', 'nosy', 'pbx'
        , 'sec-incident-nosy', 'sec-incident-responsible'
        , 'type', 'user', 'user_view'
        ]
    transprop_perms = transprop_itadr
# end class Test_Case_ITAdr

class Test_Case_Kvats (_Test_Case, unittest.TestCase) :
    schemaname = 'kvats'
    roles = \
        [ 'admin', 'anonymous', 'issue_admin'
        , 'msgedit', 'msgsync', 'nosy', 'user'
        ]
    transprop_perms = transprop_kvats
# end class Test_Case_Kvats

class Test_Case_Lielas (_Test_Case, unittest.TestCase) :
    schemaname = 'lielas'
    roles = ['admin', 'anonymous', 'guest', 'logger', 'user', 'user_view']
    transprop_perms = transprop_lielas
# end class Test_Case_Lielas

class Test_Case_PR (_Test_Case, unittest.TestCase) :
    schemaname = 'pr'
    roles = \
        [ 'admin', 'anonymous', 'board', 'ciso', 'controlling'
        , 'dom-user-edit-facility', 'dom-user-edit-gtt', 'dom-user-edit-hr'
        , 'dom-user-edit-office', 'finance', 'hr'
        , 'hr-approval', 'it', 'it-approval', 'measurement-approval', 'nosy'
        , 'pgp', 'pr-view', 'procure-approval'
        , 'procurement', 'procurement-admin', 'project'
        , 'project_view', 'quality', 'sub-login'
        , 'subcontract', 'subcontract-org'
        , 'training-approval', 'user', 'user_view'
        ]
    transprop_perms = transprop_pr
# end class Test_Case_PR

def test_suite () :
    suite = unittest.TestSuite ()
    suite.addTest (unittest.makeSuite (Test_Case_Abo))
    suite.addTest (unittest.makeSuite (Test_Case_Adr))
    suite.addTest (unittest.makeSuite (Test_Case_ERP))
    suite.addTest (unittest.makeSuite (Test_Case_IT))
    suite.addTest (unittest.makeSuite (Test_Case_ITAdr))
    suite.addTest (unittest.makeSuite (Test_Case_Kvats))
    suite.addTest (unittest.makeSuite (Test_Case_Lielas))
    suite.addTest (unittest.makeSuite (Test_Case_PR))
    suite.addTest (unittest.makeSuite (Test_Case_Tracker))
    suite.addTest (unittest.makeSuite (Test_Case_Timetracker))
    suite.addTest (unittest.makeSuite (Test_Case_Support_Timetracker))
    suite.addTest (unittest.makeSuite (Test_Case_Fulltracker))
    return suite
# end def test_suite
