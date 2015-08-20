# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-13 Ralf Schlatterbeck. All rights reserved
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

import user1_time, user2_time, user3_time, user4_time, user5_time, user6_time
import user7_time, user8_time, user10_time, user11_time, user12_time
import user13_time, user14_time

from operator     import mul
from StringIO     import StringIO
from email.parser import Parser
from mailbox      import mbox

from roundup.exceptions    import Reject
from roundup.configuration import Option

from propl_abo     import properties as properties_abo
from propl_adr     import properties as properties_adr
from propl_erp     import properties as properties_erp
from propl_full    import properties as properties_full
from propl_itadr   import properties as properties_itadr
from propl_it      import properties as properties_it
from propl_kvats   import properties as properties_kvats
from propl_lielas  import properties as properties_lielas
from propl_pr      import properties as properties_pr
from propl_sfull   import properties as properties_sfull
from propl_track   import properties as properties_track
from propl_tt      import properties as properties_time

from sec_abo       import security as security_abo
from sec_adr       import security as security_adr
from sec_erp       import security as security_erp
from sec_full      import security as security_full
from sec_itadr     import security as security_itadr
from sec_it        import security as security_it
from sec_kvats     import security as security_kvats
from sec_lielas    import security as security_lielas
from sec_pr        import security as security_pr
from sec_sfull     import security as security_sfull
from sec_track     import security as security_track
from sec_tt        import security as security_time

from search_abo    import properties as sec_search_abo
from search_adr    import properties as sec_search_adr
from search_erp    import properties as sec_search_erp
from search_full   import properties as sec_search_full
from search_itadr  import properties as sec_search_itadr
from search_it     import properties as sec_search_it
from search_kvats  import properties as sec_search_kvats
from search_lielas import properties as sec_search_lielas
from search_pr     import properties as sec_search_pr
from search_sfull  import properties as sec_search_sfull
from search_track  import properties as sec_search_track
from search_tt     import properties as sec_search_time

from trans_abo     import transprop_perms as transprop_abo
from trans_adr     import transprop_perms as transprop_adr
from trans_erp     import transprop_perms as transprop_erp
from trans_full    import transprop_perms as transprop_full
from trans_itadr   import transprop_perms as transprop_itadr
from trans_kvats   import transprop_perms as transprop_kvats
from trans_lielas  import transprop_perms as transprop_lielas
from trans_pr      import transprop_perms as transprop_pr
from trans_sfull   import transprop_perms as transprop_sfull
from trans_track   import transprop_perms as transprop_track
from trans_tt      import transprop_perms as transprop_time

from trans_search  import classdict  as trans_classprops

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

class _Test_Case (unittest.TestCase) :
    count = 0
    db = None
    roles = ['admin']
    schemafile = None
    maxDiff = None
    allroles = dict.fromkeys \
        (('abo'
        , 'abo+invoice'
        , 'admin'
        , 'adr_readonly'
        , 'anonymous'
        , 'board'
        , 'contact'
        , 'controlling'
        , 'discount'
        , 'doc_admin'
        , 'external'
        , 'finance'
        , 'guest'
        , 'hr'
        , 'hr-leave-approval'
        , 'hr-org-location'
        , 'hr-vacation'
        , 'invoice'
        , 'issue_admin'
        , 'it'
        , 'it-approval'
        , 'ituser'
        , 'itview'
        , 'letter'
        , 'logger'
        , 'msgedit'
        , 'msgsync'
        , 'nosy'
        , 'office'
        , 'pbx'
        , 'pgp'
        , 'procurement'
        , 'product'
        , 'project'
        , 'project_view'
        , 'staff-report'
        , 'subcontract'
        , 'summary_view'
        , 'supportadmin'
        , 'type'
        , 'user'
        ))


    def setup_tracker (self, backend = 'postgresql') :
        """ Install and initialize tracker in dirname, return tracker instance.
            If directory exists, it is wiped out before the operation.
        """
        self.__class__.count += 1
        self.schemafile = self.schemafile or self.schemaname
        self.dirname = '_test_init_%s' % self.count
        self.backend = 'postgresql'
        self.config  = config = configuration.CoreConfig ()
        config.DATABASE       = 'db'
        config.RDBMS_NAME     = "rounduptestttt"
        config.RDBMS_HOST     = "localhost"
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
        init.write_select_db (self.dirname, self.backend)
        self.config.save (os.path.join (self.dirname, 'config.ini'))
        tracker = instance.open (self.dirname)
        if tracker.exists () :
            tracker.nuke ()
            init.write_select_db (self.dirname, self.backend)
        tracker.init (password.Password (self.config.RDBMS_PASSWORD))
        self.tracker = tracker
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

    def test_0_roles (self) :
        self.log.debug ('test_0_roles')
        self.db = self.tracker.open ('admin')
        roles = list (sorted (self.db.security.role.iterkeys ()))
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
            clprops = sorted (self.db.getclass (cls).properties.keys ())
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
            s.extend (sorted (dict.fromkeys (perms).keys ()))
        lr1 = lr2 = None
        l1 = len (secdesc)
        l2 = len (s)
        if l1 < l2 :
            for k in xrange (l2 - l1) :
                secdesc.append ('')
        if l2 < l1 :
            for k in xrange (l1 - l2) :
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
            for p in sorted (self.db.getclass (cls).properties.keys ()) :
                users = []
                for user, uid in sorted (self.users.iteritems ()) :
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
        for cl, props in sorted (trans_classprops.iteritems ()) :
            if cl not in self.db.classes :
                continue
            klass = self.db.classes [cl]
            for p in sorted (props) :
                ps = p.split ('.')
                if ps [0] not in klass.getprops () :
                    continue
                pusers = []
                for user, uid in sorted (self.users.iteritems ()) :
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
            ,  'staff-report'
            ,  'user'
            ))
        self.users = {'admin' : '1', 'anonymous' : '2'}
        for u in self.allroles :
            if u in self.users :
                continue
            roles = u.split ('+')
            if u not in nouserroles :
                roles.append ('user')
            r_ok = (self.db.security.role.has_key (r) for r in roles)
            # wired and :-)
            if not reduce (mul, r_ok, 1) :
                continue
            params = dict \
                ( username = u
                , roles    = ','.join (roles)
                )
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

class _Test_Case_Summary (_Test_Case) :
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
            , vacation_yearly     = 25
            , do_leave_process    = True
            )
        self.dep = self.db.department.create \
            ( name       = 'Software Development'
            , valid_from = date.Date ('2004-01-01')
            )
        roles = 'User,Nosy,HR,controlling,project,ITView,IT'.split (',')
        roles.append ('HR-leave-approval')
        sec   = self.db.security
        roles = ','.join (x for x in roles if x.lower () in sec.role)
        self.username0 = 'testuser0'
        self.user0 = self.db.user.create \
            ( username     = self.username0
            , firstname    = 'Test'
            , lastname     = 'User0'
            , org_location = self.olo
            , department   = self.dep
            , roles        = roles
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
            , org_location = self.olo
            , department   = self.dep
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
            , org_location = self.olo
            , department   = self.dep
            , supervisor   = self.user1
            )
        # create initial dyn_user record for each user
        # others will follow during tests
        ud = self.db.user_dynamic.filter (None, dict (user = self.user1))
        self.assertEqual (len (ud), 1)
        self.db.user_dynamic.set \
            ( ud [0]
            , valid_from      = date.Date ('2005-09-01')
            , booking_allowed = False
            , vacation_yearly = 25
            , all_in          = True
            , hours_mon       = 7.75
            , hours_tue       = 7.75
            , hours_wed       = 7.75
            , hours_thu       = 7.75
            , hours_fri       = 7.5
            , vacation_month  = 9
            , vacation_day    = 1
            )
        self.db.user_dynamic.create \
            ( user              = self.user1
            , valid_from        = date.Date ('2005-10-01')
            , booking_allowed   = True
            , vacation_yearly   = 25
            , all_in            = False
            , hours_mon         = 0.0
            , hours_tue         = 0.0
            , hours_wed         = 0.0
            , hours_thu         = 0.0
            , hours_fri         = 0.0
            , daily_worktime    = 0.0
            , org_location      = self.olo
            , department        = self.dep
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
            , vacation_yearly  = 25
            , all_in           = True
            , hours_mon        = 7.75
            , hours_tue        = 7.75
            , hours_wed        = 7.75
            , hours_thu        = 7.75
            , hours_fri        = 7.5
            , supp_per_period  = 40
            , additional_hours = 40
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
            , overtime_reduction = True
            , is_public_holiday  = True
            , responsible        = '1'
            , department         = self.dep
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
            , overtime_reduction = True
            , responsible        = '1'
            , department         = self.dep
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
            , department         = self.dep
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
            , department         = self.dep
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
            , department         = self.dep
            , organisation       = self.org
            , cost_center        = self.cc
            , no_overtime        = True
            , overtime_reduction = True
            , approval_required  = True
            , approval_hr        = False
            , is_vacation        = True
            )
        self.flexi_tp = self.db.time_project.create \
            ( name = 'Flexi'
            , op_project         = False
            , responsible        = self.user1
            , department         = self.dep
            , organisation       = self.org
            , cost_center        = self.cc
            , max_hours          = 0
            , no_overtime        = True
            , approval_required  = True
            , approval_hr        = False
            , is_vacation        = False
            )
        self.special_tp = self.db.time_project.create \
            ( name = 'Special Leave'
            , work_location      = wl_off
            , op_project         = False
            , no_overtime        = True
            , overtime_reduction = True
            , responsible        = '1'
            , department         = self.dep
            , status             = stat_open
            , cost_center        = self.cc
            , approval_required  = True
            , approval_hr        = False
            , is_vacation        = False
            , is_special_leave   = True
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
            , travel             = True
            , responsible        = '1'
            , bookers            = [self.user1, self.user2]
            , cost_center        = self.cc
            )
        self.wps = []
        for i in xrange (40) :
            wp = self.db.time_wp.create \
                ( name           = 'Work Package %s' % i
                , project        = self.normal_tp
                , time_start     = date.Date ('2004-01-01')
                , travel         = True
                , responsible    = '1'
                , bookers        = [self.user1, self.user2]
                , cost_center    = self.cc
                )
            self.wps.append (wp)
        self.vacation_wp = self.db.time_wp.create \
            ( name               = 'Vacation'
            , project            = self.vacation_tp
            , time_start         = date.Date ('2004-01-01')
            , travel             = False
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
            , travel             = False
            , responsible        = '1'
            , bookers            = [self.user1, self.user2]
            , cost_center        = self.cc
            , durations_allowed  = True
            )
        self.special_wp = self.db.time_wp.create \
            ( name               = 'Special'
            , project            = self.special_tp
            , time_start         = date.Date ('2004-01-01')
            , travel             = False
            , responsible        = '1'
            , bookers            = []
            , is_public          = True
            , cost_center        = self.cc
            , durations_allowed  = True
            )
        self.db.commit ()
        self.log.debug ("End of setup")
    # end def setup_db

# end class _Test_Case_Summary


class Test_Case_Support_Timetracker (_Test_Case) :
    schemaname = 'sfull'
    roles = \
        [ 'admin', 'adr_readonly', 'anonymous', 'contact', 'controlling'
        , 'doc_admin', 'hr', 'hr-leave-approval', 'hr-org-location'
        , 'hr-vacation', 'issue_admin', 'it', 'itview'
        , 'msgedit', 'msgsync', 'nosy'
        , 'office', 'project', 'project_view', 'staff-report'
        , 'summary_view', 'supportadmin', 'type', 'user'
        ]
    transprop_perms = transprop_sfull
# end class Test_Case_Support_Timetracker

class Test_Case_Timetracker (_Test_Case_Summary) :
    schemaname = 'time'
    schemafile = 'time_ldap'
    roles = \
        [ 'admin', 'anonymous', 'controlling', 'doc_admin', 'hr'
        , 'hr-leave-approval', 'hr-org-location', 'hr-vacation', 'nosy'
        , 'office', 'pgp', 'project', 'project_view', 'staff-report'
        , 'summary_view', 'user'
        ]
    transprop_perms = transprop_time

    def setup_user11 (self) :
        self.username11 = 'testuser11'
        self.user11 = self.db.user.create \
            ( username     = self.username11
            , firstname    = 'Nummer11'
            , lastname     = 'User11'
            , org_location = self.olo
            , department   = self.dep
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
            , vacation_yearly   = 25
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
             , 'summary_type' : [2, 4]
             }
        cols = \
            [ 'time_wp'
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
        self.assertEqual (len (lines [0]),  4)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Time Period')
        self.assertEqual (lines [0][2], 'testuser11')
        self.assertEqual (lines [0][3], 'Sum')
        self.assertEqual (lines [1][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [1][1], 'WW 23/2013')
        self.assertEqual (lines [1][2], '5.00')
        self.assertEqual (lines [1][3], '5.00')
        self.assertEqual (lines [2][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [2][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][2], '5.00')
        self.assertEqual (lines [2][3], '5.00')
        self.assertEqual (lines [3][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [3][1], 'WW 24/2013')
        self.assertEqual (lines [3][2], '1.00')
        self.assertEqual (lines [3][3], '1.00')
        self.assertEqual (lines [4][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [4][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [4][2], '1.00')
        self.assertEqual (lines [4][3], '1.00')
        self.assertEqual (lines [5][0], 'Work package Travel/Travel')
        self.assertEqual (lines [5][1], 'WW 24/2013')
        self.assertEqual (lines [5][2], '2.00')
        self.assertEqual (lines [5][3], '2.00')
        self.assertEqual (lines [6][0], 'Work package Travel/Travel')
        self.assertEqual (lines [6][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [6][2], '2.00')
        self.assertEqual (lines [6][3], '2.00')
        self.assertEqual (lines [7][0], 'Sum')
        self.assertEqual (lines [7][1], 'WW 23/2013')
        self.assertEqual (lines [7][2], '5.00')
        self.assertEqual (lines [7][3], '5.00')
        self.assertEqual (lines [8][0], 'Sum')
        self.assertEqual (lines [8][1], 'WW 24/2013')
        self.assertEqual (lines [8][2], '3.00')
        self.assertEqual (lines [8][3], '3.00')
        self.assertEqual (lines [9][0], 'Sum')
        self.assertEqual (lines [9][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [9][2], '8.00')
        self.assertEqual (lines [9][3], '8.00')

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
            , department        = ud.department
            , valid_from        = date.Date ('2013-06-05')
            , booking_allowed   = True
            , vacation_yearly   = 25
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
            , department        = ud.department
            , valid_from        = date.Date ('2013-06-11')
            , booking_allowed   = True
            , vacation_yearly   = 25
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
        self.assertEqual (len (lines [0]), 4)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Time Period')
        self.assertEqual (lines [0][2], 'testuser11')
        self.assertEqual (lines [0][3], 'Sum')
        self.assertEqual (lines [1][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [1][1], 'WW 24/2013')
        self.assertEqual (lines [1][2], '1.00')
        self.assertEqual (lines [1][3], '1.00')
        self.assertEqual (lines [2][0], 'Work package Public Holiday/Holiday')
        self.assertEqual (lines [2][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][2], '1.00')
        self.assertEqual (lines [2][3], '1.00')
        self.assertEqual (lines [3][0], 'Sum')
        self.assertEqual (lines [3][1], 'WW 24/2013')
        self.assertEqual (lines [3][2], '1.00')
        self.assertEqual (lines [3][3], '1.00')
        self.assertEqual (lines [4][0], 'Sum')
        self.assertEqual (lines [4][1], '2013-06-01;2013-06-30')
        self.assertEqual (lines [4][2], '1.00')
        self.assertEqual (lines [4][3], '1.00')
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
             , 'summary_type' : [2, 4]
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
        self.assertEqual (lines [0][1], 'Business Case')
        self.assertEqual (lines [0][2], 'Project type')
        self.assertEqual (lines [0][3], 'Reporting group')
        self.assertEqual (lines [0][4], 'Business Case Id')
        self.assertEqual (lines [0][5], 'Project type Id')
        self.assertEqual (lines [0][6], 'Reporting group Id')
        self.assertEqual (lines [0][7], 'Time Period')
        self.assertEqual (lines [0][8], 'testuser11')
        self.assertEqual (lines [0][9], 'Sum')
        self.assertEqual (lines [1][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [1][1], '')
        self.assertEqual (lines [1][2], 'Further Development')
        self.assertEqual (lines [1][3], '')
        self.assertEqual (lines [1][4], '')
        self.assertEqual (lines [1][5], '2')
        self.assertEqual (lines [1][6], '')
        self.assertEqual (lines [1][7], 'WW 23/2013')
        self.assertEqual (lines [1][8], '5.00')
        self.assertEqual (lines [1][9], '5.00')
        self.assertEqual (lines [2][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [2][1], '')
        self.assertEqual (lines [2][2], 'Further Development')
        self.assertEqual (lines [2][3], '')
        self.assertEqual (lines [2][4], '')
        self.assertEqual (lines [2][5], '2')
        self.assertEqual (lines [2][6], '')
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
        self.assertEqual (lines [5][1], '')
        self.assertEqual (lines [5][2], 'Support')
        self.assertEqual (lines [5][3], '')
        self.assertEqual (lines [5][4], '')
        self.assertEqual (lines [5][5], '4')
        self.assertEqual (lines [5][6], '')
        self.assertEqual (lines [5][7], 'WW 24/2013')
        self.assertEqual (lines [5][8], '2.00')
        self.assertEqual (lines [5][9], '2.00')
        self.assertEqual (lines [6][0], 'Work package Travel/Travel')
        self.assertEqual (lines [6][1], '')
        self.assertEqual (lines [6][2], 'Support')
        self.assertEqual (lines [6][3], '')
        self.assertEqual (lines [6][4], '')
        self.assertEqual (lines [6][5], '4')
        self.assertEqual (lines [6][6], '')
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

        del cols [4]
        del cols [2]
        del cols [0]
        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     10)
        self.assertEqual (len (lines [0]),  7)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Business Case Id')
        self.assertEqual (lines [0][2], 'Project type Id')
        self.assertEqual (lines [0][3], 'Reporting group Id')
        self.assertEqual (lines [0][4], 'Time Period')
        self.assertEqual (lines [0][5], 'testuser11')
        self.assertEqual (lines [0][6], 'Sum')
        self.assertEqual (lines [1][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [1][1], '')
        self.assertEqual (lines [1][2], '2')
        self.assertEqual (lines [1][3], '')
        self.assertEqual (lines [1][4], 'WW 23/2013')
        self.assertEqual (lines [1][5], '5.00')
        self.assertEqual (lines [1][6], '5.00')
        self.assertEqual (lines [2][0], 'Work package A Project/Work Package 0')
        self.assertEqual (lines [2][1], '')
        self.assertEqual (lines [2][2], '2')
        self.assertEqual (lines [2][3], '')
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
        self.assertEqual (lines [5][1], '')
        self.assertEqual (lines [5][2], '4')
        self.assertEqual (lines [5][3], '')
        self.assertEqual (lines [5][4], 'WW 24/2013')
        self.assertEqual (lines [5][5], '2.00')
        self.assertEqual (lines [5][6], '2.00')
        self.assertEqual (lines [6][0], 'Work package Travel/Travel')
        self.assertEqual (lines [6][1], '')
        self.assertEqual (lines [6][2], '4')
        self.assertEqual (lines [6][3], '')
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
              , 'summary_type': [2, 4]
              }
            )
        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     1)
        self.assertEqual (len (lines [0]), 4)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Business Case')
        self.assertEqual (lines [0][2], 'Time Period')
        self.assertEqual (lines [0][3], 'Sum')

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

        cols [0] = 'product_family'
        fs ['product_family'] = '1'
        del fs ['reporting_group']
        sr = summary.Summary_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines),     3)
        self.assertEqual (len (lines [0]), 4)
        self.assertEqual (lines [0][0], 'Level')
        self.assertEqual (lines [0][1], 'Business Case')
        self.assertEqual (lines [0][2], 'Time Period')
        self.assertEqual (lines [0][3], 'Sum')
        self.assertEqual (lines [1][0], 'Business Case Family test')
        self.assertEqual (lines [1][1], 'Family test')
        self.assertEqual (lines [1][2], 'WW 23/2013')
        self.assertEqual (lines [1][3], '5.00')
        self.assertEqual (lines [2][0], 'Business Case Family test')
        self.assertEqual (lines [2][1], 'Family test')
        self.assertEqual (lines [2][2], '2013-06-01;2013-06-30')
        self.assertEqual (lines [2][3], '5.00')

        cols [0] = 'project_type'
        fs ['project_type'] = '4'
        del fs ['product_family']
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
            , org_location = self.olo
            , department   = self.dep
            )
        p = self.db.overtime_period.create \
            ( name              = 'monthly average required'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )
        ud = self.db.user_dynamic.filter (None, dict (user = self.user12))
        self.assertEqual (len (ud), 1)
        self.db.user_dynamic.retire (ud [0])
        self.db.commit ()
    # end def setup_user12

    def test_user12 (self) :
        self.log.debug ('test_user12')
        self.setup_db ()
        self.setup_user12 ()
        self.db.close ()
        self.db = self.tracker.open (self.username12)
        user12_time.import_data_12 (self.db, self.user12, self.dep, self.olo)
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        summary.init (self.tracker)
        fs = { 'user'         : [self.user12]
             , 'date'         : '2013-01-01;2013-12-31'
             , 'summary_type' : [4]
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
            , org_location = self.olo
            , department   = self.dep
            )
        ud = self.db.user_dynamic.filter (None, dict (user = self.user13))
        self.assertEqual (len (ud), 1)
        self.db.user_dynamic.retire (ud [0])
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
        user13_time.import_data_13 (self.db, self.user13, self.dep, self.olo)
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
        self.assertEqual (lines  [1] [7], '')
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

    def setup_user14 (self) :
        self.username14 = 'testuser14'
        self.user14 = self.db.user.create \
            ( username     = self.username14
            , firstname    = 'Nummer14'
            , lastname     = 'User14'
            , org_location = self.olo
            , department   = self.dep
            )
        ud = self.db.user_dynamic.filter (None, dict (user = self.user14))
        self.assertEqual (len (ud), 1)
        self.db.user_dynamic.retire (ud [0])
        self.db.commit ()
    # end def setup_user14

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
        user14_time.import_data_14 (self.db, self.user14, self.dep, self.olo)
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
        self.assertEqual (lines  [1] [7], '')
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
        self.assertEqual (lines  [1] [7], '')
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
        ext.add_option (Option (ext, 'MAIL', 'LEAVE_USER_ACCEPT_RECS_TEXT'))
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
        ext.MAIL_LEAVE_USER_ACCEPT_RECS_TEXT = \
            'The following existing time records have been deleted:\n'
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
        self.db.time_record.create \
            ( daily_record = dr [0]
            , start        = '08:00'
            , end          = '10:00'
            , wp           = self.wps [0]
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
        self.db.time_record.create \
            ( daily_record = dr [0]
            , start        = '10:00'
            , end          = '11:00'
            )
        trs = self.db.time_record.filter (None, dict (daily_record = drs))
        # Stephanitag is on Saturday, two extra records for deletion
        self.assertEqual (len (trs), 5 + 2)

        e = Parser ().parse (open (maildebug, 'r'))
        for h, t in \
            ( ('subject',    'Leave request "Vacation/Vacation" '
                             '2009-12-20 to 2010-01-06 from Test User2')
            , ('precedence', 'bulk')
            , ('to',         'user1@test.test')
            , ('from',       'roundup-admin@your.tracker.email.domain.example')
            ) :
            self.assertEqual (header_decode (e [h]), t)
        self.assertEqual \
            ( e.get_payload ().strip ()
            , 'Test User2 has submitted a leave request\n"Vacation/Vacation".\n'
              'Comment from user: None\n'
              'Please approve or decline at\n'
              'http://localhost:4711/ttt/leave_submission?@template=3Dapprove'
              '\nMany thanks!'
              '\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
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
            ( e.get_payload ().strip ()
            , 'Test User2 has submitted a leave request\n"Leave/Unpaid".\n'
              'Comment from user: None\n'
              'Needs approval by HR.\n'
              'http://localhost:4711/ttt/leave_submission?@template=3Dapprove'
              '\nMany thanks!'
              '\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
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
            ( e.get_payload ().strip ()
            , 'Test User2 has submitted a leave request\n"Leave/Unpaid".\n'
              'Comment from user: None\n'
              'Needs approval by HR.\n'
              'http://localhost:4711/ttt/leave_submission?@template=3Dapprove'
              '\nMany thanks!'
              '\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
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
            ( e.get_payload ().strip ()
            , 'Test User2 has submitted a leave request\n"Flexi/Flexi".\n'
              'Comment from user: None\n'
              'Please approve or decline at\n'
              'http://localhost:4711/ttt/leave_submission?@template=3Dapprove'
              '\nMany thanks!'
              '\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
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
            [ 'Your absence request "Flexi/Flexi" has been accepted.\n\n\n'
              'This is an automatically generated message.\n'
              'Responses to this address are not possible.'
            , 'Dear member of the Office Team,\n'
              'the user Test User2 has approved Flexi/Flexi\n'
              'from 2009-12-04 to 2009-12-04.\n'
              'Please add this information to the time table,\n\n'
              'many thanks!'
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (e.get_payload ().strip (), body [n])
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
        # Stephanitag is on Saturday, vacation records for weekdays and
        # half public holidays
        self.assertEqual (len (trs), 5 + 10)
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
            [ 'Your absence request "Vacation/Vacation" has been accepted.\n'
              'The following existing time records have been deleted:\n\n'
              '2009-12-22: A Project / Work Package 0 08:00-10:00 duration: 2.0'
              '\n'
              '2009-12-22:           /                10:00-11:00 duration: 1.0'
              '\n\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
            , 'Dear member of the Office Team,\n'
              'the user Test User2 has approved Vacation/Vacation\n'
              'from 2009-12-20 to 2010-01-06.\n'
              'Please add this information to the time table,\n\n'
              'many thanks!'
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (e.get_payload ().strip (), body [n])
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
            ( e.get_payload ().strip ()
            , 'Your absence request "Leave/Unpaid" has been declined.\n'
              'Please contact your supervisor.'
              '\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
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
            [ 'Your absence request "Leave/Unpaid" has been accepted.'
              '\n\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
            , 'Dear member of the Office Team,\n'
              'the user Test User2 has approved Leave/Unpaid\n'
              'from 2009-12-03 to 2009-12-03.\n'
              'Please add this information to the time table,\n\n'
              'many thanks!'
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (e.get_payload ().strip (), body [n])
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
            ( e.get_payload ().strip ()
            , 'Test User2 has submitted a cancel request\n'
              '"Vacation/Vacation" from 2009-12-20 to 2010-01-06.\n'
              'Comment from user: Cancel Comment\n'
              'Please approve or decline at\n'
              'http://localhost:4711/ttt/leave_submission?@template=3Dapprove'
              '\nMany thanks!'
              '\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
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
            ( e.get_payload ().strip ()
            , 'Your cancel request "Vacation/Vacation" was not granted.\n'
              'Please contact your supervisor.\n\n'
              'This is an automatically generated message.\n'
              'Responses to this address are not possible.'
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
            [ 'Your cancel request "Vacation/Vacation"\n'
              'from 2009-12-20 to 2010-01-06 was granted.'
              '\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
            , 'Dear member of the Office Team,\n'
              'the user Test User2 has cancelled Vacation/Vacation\n'
              'from 2009-12-20 to 2010-01-06\n'
              'due to Cancel Comment.\n'
              'Please remove this information from the time table,\n\n'
              'many thanks!'
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (e.get_payload ().strip (), body [n])
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
        # Stephanitag is on Saturday, vacation records for weekdays and
        # half public holidays
        self.assertEqual (len (trs), 5)
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
            ( e.get_payload ().strip ()
            , 'Test User2 has submitted a leave request\n"Vacation/Vacation".\n'
              'Comment from user: None\n'
              'Please approve or decline at\n'
              'http://localhost:4711/ttt/leave_submission?@template=3Dapprove'
              '\nMany thanks!'
              '\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
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
            [ 'Test User2 has submitted a leave request\n'
              '"Special Leave/Special".\n'
              'Comment from user: Special leave comment\n'
              'Please approve or decline at\n'
              'http://localhost:4711/ttt/leave_submission?@template=3Dapprove'
              '\nMany thanks!'
              '\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
            , "Dear Test User2,\n"
              "please don't forget to submit written documentation "
              "for your special leave\n"
              "Special Leave/Special from 2010-12-22 to 2010-12-30 to HR,\n"
              "according to our processes.\n"
              "Eg. marriage certificate, new residence registration "
              "(Meldezettel),\n"
              "birth certificate for new child, death notice letter "
              "(Parte).\n\nMany thanks!"
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (e.get_payload ().strip (), body [n])
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
            [ 'Your absence request "Special Leave/Special" has been accepted.'
              '\n\n\nThis is an automatically generated message.\n'
              'Responses to this address are not possible.'
            , 'Dear member of the Office Team,\n'
              'the user Test User2 has approved Special Leave/Special\n'
              'from 2010-12-22 to 2010-12-30.\n'
              'Please add this information to the time table,\n\n'
              'many thanks!'
            , 'Dear member of HR Admin,\n'
              'the user Test User2 has approved Special Leave/Special\n'
              'from 2010-12-22 to 2010-12-30.\n'
              'Comment: Special leave comment\n'
              'Please put it into the paid absence data sheet\n'
              'many thanks!'
            ]
        for n, e in enumerate (box) :
            for h, t in headers [n] :
                self.assertEqual (header_decode (e [h]), t)
            self.assertEqual (e.get_payload ().strip (), body [n])
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
    # end def test_vacation

# end class Test_Case_Timetracker

class Test_Case_Tracker (_Test_Case) :
    schemaname = 'track'
    schemafile = 'trackers'
    roles = \
        [ 'admin', 'anonymous', 'external', 'issue_admin', 'it'
        , 'itview', 'msgedit', 'msgsync', 'nosy', 'pgp', 'supportadmin', 'user'
        ]
    transprop_perms = transprop_track
# end class Test_Case_Tracker

class Test_Case_Fulltracker (_Test_Case_Summary) :
    schemaname = 'full'
    roles = \
        [ 'admin', 'anonymous', 'contact', 'controlling', 'doc_admin'
        , 'external', 'hr', 'hr-leave-approval', 'hr-org-location'
        , 'hr-vacation', 'issue_admin', 'it', 'itview'
        , 'msgedit', 'msgsync', 'nosy'
        , 'office', 'pgp', 'project', 'project_view', 'staff-report'
        , 'summary_view', 'supportadmin', 'user'
        ]
    transprop_perms = transprop_full

    def setup_user3 (self) :
        self.username3 = 'testuser3'
        self.user3 = self.db.user.create \
            ( username     = self.username3
            , firstname    = 'NochEinTest'
            , lastname     = 'User3'
            , org_location = self.olo
            , department   = self.dep
            )
        # create initial dyn_user record for user
        ud = self.db.user_dynamic.filter (None, dict (user = self.user3))
        self.assertEqual (len (ud), 1)
        p = self.db.overtime_period.lookup ('yearly/weekly')
        self.db.user_dynamic.set \
            ( ud [0]
            , valid_from        = date.Date ('2010-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25
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
            , org_location = self.olo
            , department   = self.dep
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
            , vacation_yearly   = 25
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
            , org_location = self.olo
            , department   = self.dep
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
            , vacation_yearly   = 25
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
            , department        = ud.department
            , valid_from        = date.Date ('2012-03-15')
            , booking_allowed   = True
            , vacation_yearly   = 25
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
            , department        = ud.department
            , valid_from        = date.Date ('2012-06-01')
            , booking_allowed   = True
            , vacation_yearly   = 25
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
            , org_location = self.olo
            , department   = self.dep
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
            , vacation_yearly   = 25
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
            , org_location = self.olo
            , department   = self.dep
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
            , vacation_yearly   = 25
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
            , org_location = self.olo
            , department   = self.dep
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
            , vacation_yearly   = 25
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
            , org_location = self.olo
            , department   = self.dep
            )
        # create initial dyn_user record for user
        ud = self.db.user_dynamic.filter (None, dict (user = self.user9))
        self.assertEqual (len (ud), 1)
        self.db.user_dynamic.set \
            ( ud [0]
            , valid_from        = date.Date ('2012-12-31')
            , booking_allowed   = True
            , vacation_yearly   = 25
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
            , org_location = self.olo
            , department   = self.dep
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
            , vacation_yearly   = 25
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
            , department        = ud.department
            , valid_from        = date.Date ('2012-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , overtime_period   = None
            , all_in            = True
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
            , department        = self.dep
            , organisation      = self.org
            , cost_center       = self.cc
            )
    # end def test_rename_status

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
            , vacation_yearly   = 25
            , all_in            = True
            , hours_mon         = 7.75
            , hours_tue         = 7.75
            , hours_wed         = 7.75
            , hours_thu         = 7.75
            , hours_fri         = 7.5
            , daily_worktime    = 0.0
            , org_location      = self.olo
            , department        = self.dep
            )
        self.db.clearCache ()
        self.assertEqual (dr.tr_duration_ok, None)
        self.db.user_dynamic.create \
            ( user              = self.user1
            , valid_from        = date.Date ('2008-01-01')
            , valid_to          = date.Date ('2008-09-11')
            , booking_allowed   = True
            , vacation_yearly   = 25
            , all_in            = False
            , hours_mon         = 5.0
            , hours_tue         = 5.0
            , hours_wed         = 5.0
            , hours_thu         = 5.0
            , hours_fri         = 5.0
            , daily_worktime    = 0.0
            , supp_weekly_hours = 25.
            , org_location      = self.olo
            , department        = self.dep
            , overtime_period   = self.db.overtime_period.lookup ('week')
            )
        self.db.user_dynamic.create \
            ( user              = self.user1
            , valid_from        = date.Date ('2009-01-04')
            , booking_allowed   = True
            , vacation_yearly   = 25
            , all_in            = True
            , hours_mon         = 2.0
            , hours_tue         = 2.0
            , hours_wed         = 2.0
            , hours_thu         = 2.0
            , hours_fri         = 2.0
            , daily_worktime    = 0.0
            , org_location      = self.olo
            , department        = self.dep
            )
        self.db.user_dynamic.create \
            ( user              = self.user1
            , valid_from        = date.Date ('2010-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25
            , all_in            = True
            , hours_mon         = 2.0
            , hours_tue         = 2.0
            , hours_wed         = 2.0
            , hours_thu         = 2.0
            , hours_fri         = 2.0
            , daily_worktime    = 0.0
            , org_location      = self.olo
            , department        = self.dep
            )
        self.db.commit ()
        self.db.close  ()
        self.db = self.tracker.open (self.username1)
        fs = { 'user'         : [self.user1]
             , 'date'         : '2008-09-01;2008-09-10'
             , 'summary_type' : [2, 4]
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
        self.assertEqual (lines [1][11], '15.00')
        self.assertEqual (lines [2][11], '0.00')
        self.assertEqual (lines [3][11], '0.00')
        self.assertEqual (lines [3][10], '910.0')
        fs = { 'user'         : [self.user1]
             , 'date'         : '2009-12-21;2010-01-03'
             , 'summary_type' : [2, 4]
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (lines [1] [1], 'WW 52/2009')
        self.assertEqual (lines [2] [1], 'WW 53/2009')
        self.assertEqual (lines [3] [1], '2009-12-21;2010-01-03')
        self.assertEqual (lines [1][11], '0.00')
        self.assertEqual (lines [2][11], '0.00')
        self.assertEqual (lines [3][11], '0.00')

        for d in ('2006-12-31', '2007-12-31') :
            f = self.db.daily_record_freeze.create \
                ( user           = self.user1
                , frozen         = True
                , date           = date.Date (d)
                )
            f = self.db.daily_record_freeze.getnode (f)
            self.assertEqual (f.balance,        0.0)
            self.assertEqual (f.achieved_hours, 0.0)
            self.assertEqual (f.validity_date,  date.Date (d))

        f = self.db.daily_record_freeze.create \
            ( user           = self.user1
            , frozen         = True
            , date           = date.Date ('2008-09-10')
            )
        f = self.db.daily_record_freeze.getnode (f)
        self.assertEqual (f.balance,       15.0)
        self.assertEqual (f.achieved_hours, 0.0)
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
        self.assertEqual (bal, (0.0, 0))
        bal = user_dynamic.compute_balance \
            (self.db, self.user1, date.Date ('2009-12-27'), sharp_end = True)
        self.assertEqual (bal, (0.0, 0))
        bal = user_dynamic.compute_balance \
            (self.db, self.user1, date.Date ('2010-01-03'), sharp_end = True)
        self.assertEqual (bal, (0.0, 0))

        bal = user_dynamic.compute_balance \
            (self.db, self.user1, date.Date ('2009-12-31'), not_after = True)
        self.assertEqual (bal, (0.0, 0))
        bal = user_dynamic.compute_balance \
            (self.db, self.user1, date.Date ('2009-12-27'), not_after = True)
        self.assertEqual (bal, (0.0, 0))
        bal = user_dynamic.compute_balance \
            (self.db, self.user1, date.Date ('2010-01-03'), not_after = True)
        self.assertEqual (bal, (0.0, 0))

        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (lines [1] [1], 'WW 52/2009')
        self.assertEqual (lines [2] [1], 'WW 53/2009')
        self.assertEqual (lines [3] [1], '2009-12-21;2010-01-03')
        self.assertEqual (lines [1][11], '0.00')
        self.assertEqual (lines [2][11], '0.00')
        self.assertEqual (lines [3][11], '0.00')

        f = self.db.daily_record_freeze.create \
            ( user           = self.user1
            , frozen         = True
            , date           = date.Date ('2009-12-31')
            )
        f = self.db.daily_record_freeze.getnode (f)
        self.assertEqual (f.balance,        0.0)
        self.assertEqual (f.achieved_hours, 0.0)
        self.assertEqual (f.validity_date,  date.Date ('2009-12-31'))

        self.db.daily_record_freeze.set (f.id, frozen = False)
        self.assertEqual (f.balance, None)
        self.db.daily_record_freeze.set (f.id, frozen = True)

        self.db.clearCache ()
        self.assertEqual (f.balance,        0.0)
        self.assertEqual (f.achieved_hours, 0.0)
        self.assertEqual (f.validity_date,  date.Date ('2009-12-31'))

        self.db.clearCache ()

        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (lines [1] [1], 'WW 52/2009')
        self.assertEqual (lines [2] [1], 'WW 53/2009')
        self.assertEqual (lines [3] [1], '2009-12-21;2010-01-03')
        self.assertEqual (lines [1][11], '0.00')
        self.assertEqual (lines [2][11], '0.00')
        self.assertEqual (lines [3][11], '0.00')
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
            , vacation_yearly   = 25
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
            , department        = self.dep
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
             , 'summary_type' : [2, 4]
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
             , 'summary_type' : [2, 4]
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
        self.db.user_dynamic.create \
            ( user              = self.user2
            , valid_from        = date.Date ('2010-01-01')
            , booking_allowed   = True
            , vacation_yearly   = 25
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
            , department        = self.dep
            )
        self.db.clearCache ()
        self.assertEqual (dr1.tr_duration_ok, 7.75)
        self.assertEqual (dr2.tr_duration_ok, None)
    # end def test_user2

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
             , 'summary_type' : [2, 3, 4]
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (len (lines), 31)
        self.assertEqual (lines [0]  [1], 'Time Period')
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
        #from roundup.admin import AdminTool
        #t = AdminTool ()
        #t.tracker_home = '.'
        #t.db = self.db
        #t.verbose = False
        #t.do_export (['/var/tmp/user4'])
        dr = self.db.daily_record.filter \
            (None, dict (user = self.user4, date = '2012-05-04'))
        self.assertEqual (len (dr), 1)
        dr = self.db.daily_record.getnode (dr [0])
        tr = dr.time_record
        self.assertEqual (len (tr), 1)
        tr = self.db.time_record.getnode (tr [0])
        self.assertEqual (tr.duration, 12)
        self.assertEqual (tr.tr_duration, None)
        user_dynamic.update_tr_duration (self.db, dr)
        self.assertEqual (round (tr.tr_duration, 2), round (7.804, 2))
        summary.init (self.tracker)
        fs = { 'user'         : [self.user4]
             , 'date'         : '2012-01-01;2012-05-31'
             , 'summary_type' : [2, 3, 4]
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
             , 'summary_type' : [2, 3, 4]
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
            ,    "0",      "0",      "0",      "0",      "0",      "0"
            ,    "0",      "0",      "0",      "0",      "8.20",  "41.00"
            ,   "41.00",  "41.00",  "41.00",  "41.00",  "41.00",  "41.00"
            ,   "41.00",  "41.00",  "41.00",  "41.00",  "41.00",  "41.00"
            ,   "41.00",  "41.00",  "41.00",  "41.00", "169.40", "161.70"
            ,   "77.00",   "0",      "0",    "172.20", "180.40", "188.60"
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
        for n in xrange (11) :
            self.assertEqual (lines [n + off][12], "week")
        off += 11
        self.assertEqual (lines [off][12], "week, monthly average required")
        off += 1
        for n in xrange (10) :
            self.assertEqual (lines [n + off][12], "monthly average required")
        off += 10
        self.assertEqual (lines [off][12], "monthly average required, week")
        off += 1
        for n in xrange (19) :
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
        for n in xrange (11) :
            self.assertEqual (lines [off + n][14], "")
        off += 11
        self.assertEqual (lines [off]    [14], "7 => 3.82")
        self.assertEqual (lines [off + 1][14], "7 => 3.82")
        self.assertEqual (lines [off + 2][14], "7")
        off += 3
        for n in xrange (4) :
            self.assertEqual (lines [off + n][14], "7 => 6.67")
        off += 4
        self.assertEqual (lines [off][14], "7")
        off += 1
        for n in xrange (4) :
            self.assertEqual (lines [off + n][14], "7 => 6.09")
        off += 4
        for n in xrange (19) :
            self.assertEqual (lines [off + n][14], "")
        off += 19
        self.assertEqual (lines [off]    [14], "7 => 3.82")
        self.assertEqual (lines [off + 1][14], "7 => 6.67")
        self.assertEqual (lines [off + 2][14], "7 => 6.09")
        off += 3
        for n in xrange (4) :
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
             , 'summary_type' : [2, 3, 4]
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
             , 'summary_type' : [2, 3, 4]
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
             , 'summary_type' : [2, 3, 4]
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
            , department        = self.dep
            , user              = self.user8
            , valid_from        = date.Date ('2012-12-17')
            , valid_to          = date.Date ('2012-12-24')
            , booking_allowed   = True
            , vacation_yearly   = 25
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
        self.db.time_record.create \
            ( daily_record  = dr
            , duration      = 8.0
            , work_location = '5'
            , wp            = '5'
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
             , 'summary_type' : [2, 3, 4]
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
             , 'summary_type' : [2, 3, 4]
             }
        class r : filterspec = fs
        sr = summary.Staff_Report \
            (self.db, r, templating.TemplatingUtils (None))
        lines = tuple (csv.reader (StringIO (sr.as_csv ()), delimiter = ','))
        self.assertEqual (len (lines), 14)
        self.assertEqual (lines  [0] [1], 'Time Period')
        self.assertEqual (lines  [0] [6], 'Actual all')
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
        self.assertEqual (lines  [1] [9], '0')
        self.assertEqual (lines [13] [9], '0')
        self.assertEqual (lines  [1] [2], '76.38')
        self.assertEqual (lines [13] [2], '76.38')
        self.assertEqual (lines [13][11], '0.00')
    # end def test_user10

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
        self.db2.commit ()

        self.db1.commit ()

        self.log.debug ("before method")
        method (drid, trid)
        self.log.debug ("after  method")
        self.db1.commit ()

        self.db1.clearCache ()

        self.assertEqual \
            (self.db1.daily_record.get (drid, 'tr_duration_ok'), None)
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
        self.db.time_record.create \
            ( daily_record  = dr
            , duration      = 2.0
            , work_location = '5'
            , wp            = '1'
            )
        request      = Request ()
        env          = dict (PATH_INFO = '', REQUEST_METHOD = 'GET')
        cli          = self.tracker.Client (self.tracker, request, env, None)
        cli.db       = self.db
        cli.language = None
        cli.userid   = self.db.getuid ()
        hcit         = templating.HTMLItem (cli, 'time_record', 1)
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
        user = self.db.user.create \
            ( username = 'user'
            , status = self.db.user_status.lookup ('system')
            , roles = 'User,Nosy'
            )
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
            , numeric_effort = 1
            , category       = pending
            )
        c1 = self.db.issue.create \
            ( title          = "Container"
            , messages       = [m1]
            , release        = 'None'
            , status         = opn
            , numeric_effort = 1
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
            , numeric_effort = 1
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
        self.assertEqual (trok, None)
        self.assertEqual (self.db.time_record.get (trid, 'duration'), 8)
        self.assertEqual (self.db.time_record.get (trid, 'tr_duration'), None)
        self.db.clearCache ()

        dr = self.db.daily_record.getnode (drid)
        user_dynamic.update_tr_duration (self.db, dr)
        self.db.commit ()
        self.db.clearCache ()
        self.assertEqual (self.db.time_record.get (trid, 'duration'), 8)
        self.assertEqual (self.db.time_record.get (trid, 'tr_duration'), 8)
        self.assertEqual (self.db.daily_record.get (drid, 'tr_duration_ok'), 8)
    # end def test_tr_duration
# end class Test_Case_Fulltracker

class Test_Case_Abo (_Test_Case) :
    schemaname = 'abo'
    roles = \
        [ 'abo', 'admin', 'adr_readonly', 'anonymous', 'contact'
        , 'invoice', 'letter', 'product', 'type', 'user'
        ]
    transprop_perms = transprop_abo
# end class Test_Case_Abo

class Test_Case_Adr (_Test_Case) :
    schemaname = 'adr'
    roles = \
        [ 'admin', 'adr_readonly', 'anonymous', 'contact', 'letter'
        , 'type', 'user'
        ]
    transprop_perms = transprop_adr
# end class Test_Case_Adr

class Test_Case_ERP (_Test_Case) :
    schemaname = 'erp'
    roles = \
        [ 'admin', 'adr_readonly', 'anonymous', 'contact', 'discount'
        , 'invoice', 'letter', 'product', 'type', 'user'
        ]
    transprop_perms = transprop_erp
# end class Test_Case_ERP

class Test_Case_IT (_Test_Case) :
    schemaname = 'it'
    roles = ['admin', 'anonymous', 'it', 'ituser', 'itview', 'nosy', 'user']
# end class Test_Case_IT

class Test_Case_ITAdr (_Test_Case) :
    schemaname = 'itadr'
    roles = \
        [ 'admin', 'adr_readonly', 'anonymous', 'contact', 'it'
        , 'itview', 'nosy', 'pbx', 'type', 'user'
        ]
    transprop_perms = transprop_itadr
# end class Test_Case_ITAdr

class Test_Case_Kvats (_Test_Case) :
    schemaname = 'kvats'
    roles = \
        [ 'admin', 'anonymous', 'issue_admin'
        , 'msgedit', 'msgsync', 'nosy', 'user'
        ]
    transprop_perms = transprop_kvats
# end class Test_Case_Kvats

class Test_Case_Lielas (_Test_Case) :
    schemaname = 'lielas'
    roles = ['admin', 'anonymous', 'guest', 'logger', 'user']
    transprop_perms = transprop_lielas
# end class Test_Case_Lielas

class Test_Case_PR (_Test_Case) :
    schemaname = 'pr'
    roles = \
        [ 'admin', 'anonymous', 'board', 'controlling', 'finance', 'hr'
        , 'it-approval', 'nosy', 'pgp', 'procurement', 'project'
        , 'project_view', 'subcontract', 'user'
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
    suite.addTest (unittest.makeSuite (Test_Case_Timetracker))
    suite.addTest (unittest.makeSuite (Test_Case_Tracker))
    suite.addTest (unittest.makeSuite (Test_Case_Support_Timetracker))
    suite.addTest (unittest.makeSuite (Test_Case_Fulltracker))
    return suite
# end def test_suite
