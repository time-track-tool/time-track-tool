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

import user1_time, user2_time

from roundup     import instance, configuration, init, password, date
from roundup.cgi import templating
sys.path.insert (0, os.path.abspath ('lib'))
sys.path.insert (0, os.path.abspath ('extensions'))
from user_dynamic import update_tr_duration, compute_balance
from user_dynamic import overtime_periods, first_user_dynamic, next_user_dynamic
from summary import Staff_Report
from summary import init as summary_init

class _Test_Case (unittest.TestCase) :
    count = 0
    db = None

    def setup_tracker (self, schema = 'full.py', backend = 'postgresql') :
        """ Install and initialize tracker in dirname, return tracker instance.
            If directory exists, it is wiped out before the operation.
        """
        self.__class__.count += 1
        self.dirname = '_test_init_%s' % self.count
        self.backend = 'postgresql'
        self.config  = config = configuration.CoreConfig ()
        config.DATABASE       = 'db'
        config.RDBMS_NAME     = "rounduptest"
        config.RDBMS_HOST     = "localhost"
        config.RDBMS_USER     = "rounduptest"
        config.RDBMS_PASSWORD = "rounduptest"
        config.MAIL_DOMAIN    = "your.tracker.email.domain.example"
        config.TRACKER_WEB    = "http://localhost:4711/ttt/"
        config.init_logging ()
        self.tearDown ()
        srcdir = os.path.join (os.path.dirname (__file__), '..')
        os.mkdir (self.dirname)
        for f in ( 'detectors', 'extensions', 'html', 'initial_data.py'
                 , 'lib', 'locale', 'schema', 'schemas/%s' % schema
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
# end class _Test_Case

class Test_Case_Timetracker (_Test_Case) :
    def setup_db (self) :
        self.db = self.tracker.open ('admin')
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
        self.holiday_tp = self.db.time_project.create \
            ( name = 'Public Holiday'
            , work_location     = wl_off
            , op_project        = False
            , no_overtime       = True
            , is_public_holiday = True
            , responsible       = '1'
            , department        = self.dep
            , status            = stat_open
            )
        self.unpaid_tp = self.db.time_project.create \
            ( name = 'Leave'
            , work_location     = wl_off
            , op_project        = False
            , no_overtime       = True
            , responsible       = '1'
            , department        = self.dep
            , status            = stat_open
            )
        self.travel_tp = self.db.time_project.create \
            ( name = 'Travel'
            , work_location     = wl_trav
            , op_project        = False
            , responsible       = '1'
            , department        = self.dep
            , status            = stat_open
            )
        self.normal_tp = self.db.time_project.create \
            ( name = 'A Project'
            , op_project        = True
            , responsible       = self.user1
            , department        = self.dep
            , organisation      = self.org
            )
        self.ccg = self.db.cost_center_group.create (name = 'CCG')
        self.cc = self.db.cost_center.create \
            ( name              = 'CC'
            , cost_center_group = self.ccg
            , organisation      = self.org
            , status            = self.db.cost_center_status.lookup ('Open')
            )
        self.holiday_wp = self.db.time_wp.create \
            ( name              = 'Holiday'
            , project           = self.holiday_tp
            , time_start        = date.Date ('2004-01-01')
            , durations_allowed = True
            , responsible       = '1'
            , bookers           = [self.user1, self.user2]
            , cost_center       = self.cc
            )
        self.unpaid_wp = self.db.time_wp.create \
            ( name              = 'Unpaid'
            , project           = self.holiday_tp
            , time_start        = date.Date ('2004-01-01')
            , durations_allowed = True
            , responsible       = '1'
            , bookers           = [self.user1, self.user2]
            , cost_center       = self.cc
            )
        self.travel_wp = self.db.time_wp.create \
            ( name              = 'Travel'
            , project           = self.holiday_tp
            , time_start        = date.Date ('2004-01-01')
            , travel            = True
            , responsible       = '1'
            , bookers           = [self.user1, self.user2]
            , cost_center       = self.cc
            )
        for i in xrange (40) :
            self.db.time_wp.create \
                ( name              = 'Work Package %s' % i
                , project           = self.normal_tp
                , time_start        = date.Date ('2004-01-01')
                , travel            = True
                , responsible       = '1'
                , bookers           = [self.user1, self.user2]
                , cost_center       = self.cc
                )
        self.db.commit ()
    # end def setup_db

    def test_rename_status (self) :
        self.setup_db ()
        # test that renaming the 'New' time_project_status will still work
        tps = self.db.time_project_status.lookup ('New')
        self.db.time_project_status.set (tps, name = 'Something')
        self.normal_tp = self.db.time_project.create \
            ( name = 'Another Project'
            , op_project        = True
            , responsible       = self.user1
            , department        = self.dep
            , organisation      = self.org
            )
        # same for cost_center
        ccs = self.db.cost_center_status.lookup ('New')
        self.db.cost_center_status.set (ccs, name = 'Something')
        self.cc = self.db.cost_center.create \
            ( name              = 'CC-New'
            , cost_center_group = self.ccg
            , organisation      = self.org
            )
    # end def test_rename_status

    def test_user1 (self) :
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
        self.assertEqual (lines [1] [1], 'WW 36/2008')
        self.assertEqual (lines [2] [1], 'WW 37/2008')
        self.assertEqual (lines [3] [1], '2008-09-01;2008-09-10')
        self.assertEqual (lines [1][10], '15.00')
        self.assertEqual (lines [2][10], '0.00')
        self.assertEqual (lines [3][10], '0.00')
        self.assertEqual (lines [3] [9], '910.0')
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
        self.assertEqual (lines [1][10], '0.00')
        self.assertEqual (lines [2][10], '0.00')
        self.assertEqual (lines [3][10], '0.00')

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
        self.assertEqual (lines [1][10], '0.00')
        self.assertEqual (lines [2][10], '0.00')
        self.assertEqual (lines [3][10], '0.00')

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
        self.assertEqual (lines [1][10], '0.00')
        self.assertEqual (lines [2][10], '0.00')
        self.assertEqual (lines [3][10], '0.00')
    # end def test_user1

    def test_user2 (self) :
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
        sr = Staff_Report (self.db, r, templating.TemplatingUtils (None))
        lines = [x.strip ().split (',') for x in sr.as_csv ().split ('\n')]
        self.assertEqual (len (lines), 5)
        self.assertEqual (lines [1] [1], 'WW 52/2008')
        self.assertEqual (lines [2] [1], 'WW 1/2009')
        self.assertEqual (lines [3] [1], '2008-12-22;2009-01-04')
        self.assertEqual (lines [1][10], '0.00')
        self.assertEqual (lines [2][10], '0.00')
        self.assertEqual (lines [3][10], '0.00')

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
        self.assertEqual (lines [1][10], '113.12')
        self.assertEqual (lines [2][10], '113.12')
        self.assertEqual (lines [3][10], '113.12')
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

    def concurrency (self, method) :
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
        self.db1.commit ()

        dr  = self.db2.daily_record.getnode (drid)
        dud = dr.tr_duration_ok
        tr  = self.db2.time_record.getnode (trid)
        dut = tr.tr_duration
        self.db2.commit ()
        update_tr_duration (self.db2, dr)
        self.db2.commit ()

        method (drid, trid)
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
        self.concurrency (self.concurrency_create)
    # end def test_concurrency_create

    def test_concurrency_retire (self) :
        self.concurrency (self.concurrency_retire)
    # end def test_concurrency_retire

    def test_concurrency_set (self) :
        self.concurrency (self.concurrency_set)
    # end def test_concurrency_set

    def test_tr_duration (self) :
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

def test_suite () :
    suite = unittest.TestSuite ()
    suite.addTest (unittest.makeSuite (Test_Case_Timetracker))
    return suite
# end def test_suite
