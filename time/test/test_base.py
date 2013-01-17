# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Ralf Schlatterbeck. All rights reserved
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

import user1_time, user2_time, user3_time, user4_time, user5_time, user6_time
import user7_time, user8_time

from operator import mul
from StringIO import StringIO

from propl_abo     import properties as properties_abo
from propl_adr     import properties as properties_adr
from propl_erp     import properties as properties_erp
from propl_full    import properties as properties_full
from propl_it      import properties as properties_it
from propl_itadr   import properties as properties_itadr
from propl_kvats   import properties as properties_kvats
from propl_lielas  import properties as properties_lielas
from propl_sfull   import properties as properties_sfull

from sec_abo       import security as security_abo
from sec_adr       import security as security_adr
from sec_erp       import security as security_erp
from sec_full      import security as security_full
from sec_it        import security as security_it
from sec_itadr     import security as security_itadr
from sec_kvats     import security as security_kvats
from sec_lielas    import security as security_lielas
from sec_sfull     import security as security_sfull

from search_abo    import properties as sec_search_abo
from search_adr    import properties as sec_search_adr
from search_erp    import properties as sec_search_erp
from search_full   import properties as sec_search_full
from search_it     import properties as sec_search_it
from search_itadr  import properties as sec_search_itadr
from search_kvats  import properties as sec_search_kvats
from search_lielas import properties as sec_search_lielas
from search_sfull  import properties as sec_search_sfull

from trans_abo     import transprop_perms as transprop_abo
from trans_adr     import transprop_perms as transprop_adr
from trans_erp     import transprop_perms as transprop_erp
from trans_full    import transprop_perms as transprop_full
from trans_itadr   import transprop_perms as transprop_itadr
from trans_kvats   import transprop_perms as transprop_kvats
from trans_lielas  import transprop_perms as transprop_lielas
from trans_sfull   import transprop_perms as transprop_sfull

from trans_search  import classdict  as trans_classprops

from roundup       import instance, configuration, init, password, date
from roundup.cgi   import templating
sys.path.insert (0, os.path.abspath ('lib'))
sys.path.insert (0, os.path.abspath ('extensions'))
from user_dynamic import update_tr_duration, compute_balance
from user_dynamic import overtime_periods, first_user_dynamic, next_user_dynamic
from summary import Staff_Report
from summary import init as summary_init

class _Test_Case (unittest.TestCase) :
    count = 0
    db = None
    roles = ['admin']
    allroles = dict.fromkeys \
        (('abo'
        , 'abo+invoice'
        , 'admin'
        , 'adr_readonly'
        , 'anonymous'
        , 'contact'
        , 'controlling'
        , 'discount'
        , 'doc_admin'
        , 'external'
        , 'guest'
        , 'hr'
        , 'hr-org-location'
        , 'invoice'
        , 'issue_admin'
        , 'it'
        , 'ituser'
        , 'itview'
        , 'letter'
        , 'logger'
        , 'nosy'
        , 'office'
        , 'pgp'
        , 'product'
        , 'project'
        , 'project_view'
        , 'supportadmin'
        , 'type'
        , 'user'
        ))


    def setup_tracker (self, backend = 'postgresql') :
        """ Install and initialize tracker in dirname, return tracker instance.
            If directory exists, it is wiped out before the operation.
        """
        self.__class__.count += 1
        self.dirname = '_test_init_%s' % self.count
        self.backend = 'postgresql'
        self.config  = config = configuration.CoreConfig ()
        config.DATABASE       = 'db'
        config.RDBMS_NAME     = "rounduptestttt"
        config.RDBMS_HOST     = "localhost"
        config.RDBMS_USER     = "rounduptest"
        config.RDBMS_PASSWORD = "rounduptest"
        config.MAIL_DOMAIN    = "your.tracker.email.domain.example"
        config.TRACKER_WEB    = "http://localhost:4711/ttt/"
        config.RDBMS_TEMPLATE = "template0"
        config.init_logging ()
        self.tearDown ()
        srcdir = os.path.join (os.path.dirname (__file__), '..')
        os.mkdir (self.dirname)
        for f in ( 'detectors', 'extensions', 'html', 'initial_data.py'
                 , 'lib', 'locale', 'schema'
                 , 'schemas/%s.py' % self.schemaname
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
        nouserroles = \
            [ 'adr_readonly'
            , 'guest'
            , 'hr-org-location'
            , 'ituser'
            , 'logger'
            , 'nosy'
            , 'user'
            , 'external'
            ]
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

class Test_Case_Support_Timetracker (_Test_Case) :
    schemaname = 'sfull'
    roles = \
        [ 'admin', 'adr_readonly', 'anonymous', 'contact', 'controlling'
        , 'doc_admin', 'hr', 'hr-org-location', 'issue_admin', 'it'
        , 'itview', 'nosy'
        , 'office', 'project', 'project_view', 'supportadmin', 'type', 'user'
        ]
    transprop_perms = transprop_sfull
# end class Test_Case_Support_Timetracker

class Test_Case_Timetracker (_Test_Case) :
    schemaname = 'full'
    roles = \
        [ 'admin', 'anonymous', 'contact', 'controlling', 'doc_admin'
        , 'external', 'hr', 'hr-org-location', 'issue_admin', 'it'
        , 'itview', 'nosy'
        , 'office', 'pgp', 'project', 'project_view', 'supportadmin', 'user'
        ]
    transprop_perms = transprop_full

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
            ( name         = 'The Org, Vienna'
            , location     = self.loc
            , organisation = self.org
            )
        self.dep = self.db.department.create \
            ( name       = 'Software Development'
            , valid_from = date.Date ('2004-01-01')
            )
        self.username0 = 'testuser0'
        self.user0 = self.db.user.create \
            ( username     = self.username0
            , firstname    = 'Test'
            , lastname     = 'User0'
            , org_location = self.olo
            , department   = self.dep
            , roles        = 'User,Nosy,HR,controlling,project,ITView,IT'
            )
        self.username1 = 'testuser1'
        self.user1 = self.db.user.create \
            ( username     = self.username1
            , firstname    = 'Test'
            , lastname     = 'User1'
            , org_location = self.olo
            , department   = self.dep
            )
        self.username2 = 'testuser2'
        self.user2 = self.db.user.create \
            ( username     = self.username2
            , firstname    = 'Test'
            , lastname     = 'User2'
            , org_location = self.olo
            , department   = self.dep
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
            )
        self.travel_tp = self.db.time_project.create \
            ( name = 'Travel'
            , work_location      = wl_trav
            , op_project         = False
            , responsible        = '1'
            , department         = self.dep
            , status             = stat_open
            , cost_center        = self.cc
            )
        self.normal_tp = self.db.time_project.create \
            ( name = 'A Project'
            , op_project         = True
            , responsible        = self.user1
            , department         = self.dep
            , organisation       = self.org
            , cost_center        = self.cc
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
            , project            = self.holiday_tp
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
        for i in xrange (40) :
            self.db.time_wp.create \
                ( name           = 'Work Package %s' % i
                , project        = self.normal_tp
                , time_start     = date.Date ('2004-01-01')
                , travel         = True
                , responsible    = '1'
                , bookers        = [self.user1, self.user2]
                , cost_center    = self.cc
                )
        self.db.commit ()
        self.log.debug ("End of setup")
    # end def setup_db

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
        week = self.db.overtime_period.lookup ('week')
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
            , supp_weekly_hours = 42.0
            , additional_hours  = 40.0
            , overtime_period   = week
            )
        p = self.db.overtime_period.create \
            ( name              = 'monthly average required'
            , months            = 1
            , weekly            = False
            , required_overtime = True
            , order             = 3
            )

        self.db.user_dynamic.create \
            ( user              = self.user8
            , org_location      = self.olo
            , department        = self.dep
            , valid_from        = date.Date ('2012-10-01')
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
        update_tr_duration (self.db, dr)
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
        summary_init (self.tracker)
        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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
        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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

        dyn = first_user_dynamic (self.db, self.user1)
        self.assertEqual (dyn.valid_from, date.Date ('2005-09-01'))
        op  = overtime_periods \
            (self.db, self.user1, dyn.valid_from, date.Date ('2009-12-31'))
        self.assertEqual (len (op), 1)
        self.assertEqual (op [0][0], date.Date ('2005-10-01'))
        self.assertEqual (op [0][1], date.Date ('2008-09-10'))
        self.assertEqual (op [0][2].name, 'week')
        dyn = next_user_dynamic (self.db, dyn)
        self.assertEqual (dyn.valid_from, date.Date ('2005-10-01'))
        dyn = next_user_dynamic (self.db, dyn)
        self.assertEqual (dyn.valid_from, date.Date ('2006-01-01'))
        self.assertEqual (dyn.overtime_period, None)

        bal = compute_balance \
            (self.db, self.user1, date.Date ('2009-12-31'), sharp_end = True)
        self.assertEqual (bal, (0.0, 0))
        bal = compute_balance \
            (self.db, self.user1, date.Date ('2009-12-27'), sharp_end = True)
        self.assertEqual (bal, (0.0, 0))
        bal = compute_balance \
            (self.db, self.user1, date.Date ('2010-01-03'), sharp_end = True)
        self.assertEqual (bal, (0.0, 0))

        bal = compute_balance \
            (self.db, self.user1, date.Date ('2009-12-31'), not_after = True)
        self.assertEqual (bal, (0.0, 0))
        bal = compute_balance \
            (self.db, self.user1, date.Date ('2009-12-27'), not_after = True)
        self.assertEqual (bal, (0.0, 0))
        bal = compute_balance \
            (self.db, self.user1, date.Date ('2010-01-03'), not_after = True)
        self.assertEqual (bal, (0.0, 0))

        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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

        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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
        summary_init (self.tracker)
        ndr = self.db.daily_record.getnode ('51')
        self.assertEqual (len (ndr.time_record), 2)
        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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
        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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
        update_tr_duration (self.db, dr1)
        self.assertEqual (dr1.tr_duration_ok, 7.75)
        dr2 = self.db.daily_record.filter \
            (None, dict (user = self.user2, date = '2010-01-01')) [0]
        dr2 = self.db.daily_record.getnode (dr2)
        update_tr_duration (self.db, dr2)
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
        summary_init (self.tracker)
        fs = { 'user'         : [self.user3]
             , 'date'         : '2010-01-01;2010-05-31'
             , 'summary_type' : [2, 3, 4]
             }
        class r : filterspec = fs
        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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
        update_tr_duration (self.db, dr)
        self.assertEqual (round (tr.tr_duration, 2), round (7.804, 2))
        summary_init (self.tracker)
        fs = { 'user'         : [self.user4]
             , 'date'         : '2012-01-01;2012-05-31'
             , 'summary_type' : [2, 3, 4]
             }
        class r : filterspec = fs
        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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
        summary_init (self.tracker)
        fs = { 'user'         : [self.user5]
             , 'date'         : '2012-01-01;2012-09-28'
             , 'summary_type' : [2, 3, 4]
             }
        class r : filterspec = fs
        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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
        summary_init (self.tracker)
        fs = { 'user'         : [self.user6]
             , 'date'         : '2012-09-01;2012-10-08'
             , 'summary_type' : [2, 3, 4]
             }
        class r : filterspec = fs
        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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
        summary_init (self.tracker)
        fs = { 'user'         : [self.user7]
             , 'date'         : '2012-11-15;2012-12-18'
             , 'summary_type' : [2, 3, 4]
             }
        class r : filterspec = fs
        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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
#        f = self.db.daily_record_freeze.create \
#            ( user           = self.user8
#            , frozen         = True
#            , date           = date.Date ('2012-12-31')
#            )
        self.db.commit ()
        self.db.close ()
        self.db = self.tracker.open (self.username0)
        dtstart = date.Date ('2012-11-01')
        dtend   = date.Date ('2013-01-06')
        yend    = date.Date ('2012-12-31')
        tbl = \
            ( (dtstart,                  date.Date ('2012-11-30'))
            , (date.Date ('2012-12-01'), date.Date ('2012-12-30'))
            , (yend,                     yend)
            , (date.Date ('2013-01-01'), dtend)
            )
        for n, (s, e, p) in enumerate \
            (overtime_periods (self.db, self.user8, dtstart, dtend)) :
            self.assertEqual (p.name, 'monthly average required')
            print >> sys.stderr, "enumerate-otp", s, e
            #self.assertEqual ((n, (s, e)), (n, tbl [n]))
        summary_init (self.tracker)
        fs = { 'user'         : [self.user8]
             , 'date'         : '2013-01-01;2013-01-16'
             , 'summary_type' : [2, 3, 4]
             }
#        fs = { 'user'         : [self.user8]
#             , 'date'         : '2012-12-30;2013-01-16'
#             , 'summary_type' : [2, 3, 4]
#             }
        class r : filterspec = fs
        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
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
        self.assertEqual (lines  [1] [2], '5.78') # balance_start
        self.assertEqual (lines  [5][11], '8.44') # balance_end
    # end def test_user8

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
        update_tr_duration (self.db2, dr)
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
        update_tr_duration (self.db, dr)
        self.db.commit ()
        self.db.clearCache ()
        self.assertEqual (self.db.time_record.get (trid, 'duration'), 8)
        self.assertEqual (self.db.time_record.get (trid, 'tr_duration'), 8)
        self.assertEqual (self.db.daily_record.get (drid, 'tr_duration_ok'), 8)
    # end def test_tr_duration
# end class Test_Case_Timetracker

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
        , 'itview', 'nosy', 'type', 'user'
        ]
    transprop_perms = transprop_itadr
# end class Test_Case_ITAdr

class Test_Case_Kvats (_Test_Case) :
    schemaname = 'kvats'
    roles = ['admin', 'anonymous', 'issue_admin', 'nosy', 'user']
    transprop_perms = transprop_kvats
# end class Test_Case_Kvats

class Test_Case_Lielas (_Test_Case) :
    schemaname = 'lielas'
    roles = ['admin', 'anonymous', 'guest', 'logger', 'user']
    transprop_perms = transprop_lielas
# end class Test_Case_Lielas

def test_suite () :
    suite = unittest.TestSuite ()
    suite.addTest (unittest.makeSuite (Test_Case_Abo))
    suite.addTest (unittest.makeSuite (Test_Case_Adr))
    suite.addTest (unittest.makeSuite (Test_Case_ERP))
    suite.addTest (unittest.makeSuite (Test_Case_IT))
    suite.addTest (unittest.makeSuite (Test_Case_ITAdr))
    suite.addTest (unittest.makeSuite (Test_Case_Kvats))
    suite.addTest (unittest.makeSuite (Test_Case_Lielas))
    suite.addTest (unittest.makeSuite (Test_Case_Support_Timetracker))
    suite.addTest (unittest.makeSuite (Test_Case_Timetracker))
    return suite
# end def test_suite
