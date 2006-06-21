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
#    summary
#
# Purpose
#    Time-tracking summary reports
#

import sys
import os
import csv
import cgi
import time
try :
    from cStringIO import StringIO
except ImportError :
    from StringIO  import StringIO

from roundup.date                   import Date, Interval
from roundup.cgi                    import templating
from roundup.cgi.TranslationService import get_translation
from roundup.cgi.actions            import Action
from rsclib.autosuper               import autosuper
from rsclib.PM_Value                import PM_Value

_      = lambda x : x

try :
    from common       import pretty_range, week_from_date, ymd, user_has_role \
                           , date_range, weekno_from_day
    from user_dynamic import update_tr_duration, get_user_dynamic
except ImportError :
    ymd                = None
    pretty_range       = None
    week_from_date     = None
    user_has_role      = None
    date_range         = None
    weekno_from_day    = None
    update_tr_duration = None
    get_user_dynamic   = None

sup_cache = {}
def user_supervisor_for (db, uid = None) :
    """ Recursively compute the users for which the given uid is
        supervisor. If uid in not given (None), the current database
        user is taken.
    """
    if not uid :
        uid = db.getuid ()
    if uid in sup_cache :
        return sup_cache [uid]
    sv                = dict ((u, 1) for u in db.user.find (substitute = uid))
    sv [uid]          = 1
    users             = db.user.find (supervisor = sv)
    trans_users       = []
    for u in users :
        if u != uid :
            trans_users.extend (user_supervisor_for (db, u))
    sup_cache [uid] = dict ((u, 1) for u in users + trans_users)
    return sup_cache [uid]
# end def user_supervisor_for

class Extended_Node (autosuper) :
    def __getattr__ (self, name) :
        """ Delegate everything to our node """
        if not name.startswith ('__') :
            result = getattr (self.node, name)
            setattr (self, name, result)
            return result
        raise AttributeError, name
    # end def __getattr__

    def __repr__ (self) :
        return "%s (%s)" % (self.__class__.__name__, repr (self.name))
    # end def __repr__

    __str__ = __repr__

# end class Extended_Node

class Extended_Daily_Record (Extended_Node) :
    """ Keeps information about the username *and* about the status of
        the daily_records: own records (is_own = True) are records wich
        may be unconditionally viewed by the user. This is determined by
        looking at the current db user:
        - HR and Controlling roles own all users
        - a user owns records for his userid
        - a user owns all users for which he is supervisor or substitute
          supervisor
        - the supervisor relationship is transitive.
        - a user owns all users in his department(s)
    """

    def __init__ (self, db, drid, supervised_users) :
        self.node         = db.daily_record.getnode (drid)
        self.username     = db.user.get (self.user, 'username')
        self.name         = self.username
        uid               = db.getuid ()
        self.is_own       = \
            (  user_has_role (db, uid, 'HR', 'Controlling')
            or uid == self.user
            or self.user in supervised_users
            )
    # end def __init__

    def __cmp__ (self, other) :
        return \
            cmp (self.date, other.date) or cmp (self.username, other.username)
    # end def __cmp__
# end class Extended_Daily_Record

class Extended_WP (Extended_Node) :
    """ Keeps information about the username *and* about the status of
        the work package: own records (is_own = True) are records wich
        may be unconditionally viewed by the user. This is the case if
        the user is responsible for the wp or if he is responsible or
        deputy for the project of the WP or if he is in the nosy list
        for the project.
    """
    def __init__ (self, db, wpid) :
        self.node         = db.time_wp.getnode  (wpid)
        self.project_name = db.time_project.get (self.project, 'name')
        uid               = db.getuid ()
        p_owner           = db.time_project.get (self.project, 'responsible')
        p_deputy          = db.time_project.get (self.project, 'deputy')
        p_nosy            = dict \
            ([(i, 1) for i in db.time_project.get (self.project, 'nosy')])
        self.is_own       = \
            (  uid == self.responsible
            or uid == p_owner
            or uid == p_deputy
            or uid in p_nosy
            )
        self.effort_perday = PM_Value (0, 1)
        if  (   self.time_start and self.time_end
            and self.planned_effort is not None
            ) :
            self.start = s     = Date (str (self.time_start))
            self.end   = e     = Date (str (self.time_end))
            days               = (e - s).get_tuple () [3]
            if days :
                self.effort_perday = PM_Value (self.planned_effort / days)
    # end def __init__

    def effort (self, date) :
        if not self.effort_perday.missing :
            if self.start <= date <= self.end :
                return self.effort_perday
            return PM_Value (0)
        return self.effort_perday
    # end def effort

    def __cmp__ (self, other) :
        return \
            (  cmp (self.project_name, other.project_name)
            or cmp (self.name,         other.name)
            )
    # end def __cmp__
# end class Extended_WP

class Extended_Time_Record (Extended_Node) :
    """ Keeps information about the username *and* about the status of
        the time record: own records (is_own = True) are records wich
        may be unconditionally viewed by the user. This is the case if
        the user owns the wp or owns the daily_record of the time
        record.
    """
    def __init__ (self, db, trid, dr, wp) :
        self.node         = db.time_record.getnode  (trid)
        self.dr           = dr [self.node.daily_record]
        self.wp           = wp [self.node.wp]
        self.is_own       = self.dr.is_own or self.wp.is_own
    # end def __init__

    def __getattr__ (self, name) :
        """ Delegate everything to first the daily_record, then the wp,
            then our node.
        """
        if not name.startswith ('__') :
            for x in self.dr, self.wp :
                try :
                    result = getattr (x, name)
                    setattr (self, name, result)
                    return result
                except AttributeError :
                    return self.__super.__getattr__ (name)
        raise AttributeError, name
    # end def __getattr__

    def __cmp__ (self, other) :
        return (cmp (self.dr, other.dr) or cmp (self.wp, other.wp))
    # end def __cmp__
# end class Extended_Time_Record

class Container (autosuper) :
    def __init__ (self, * args, ** kw) :
        self.sums  = {}
        self.plans = {}
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def add_sum (self, other_container, tr) :
        self.add_user_sum \
            (other_container, tr.username, tr.tr_duration or tr.duration)
    # end def add_sum

    def add_user_sum (self, other_container, username, sum) :
        for key in other_container, (other_container, username) :
            if key not in self.sums :
                self.sums [key] = PM_Value (0)
            self.sums [key] += sum
    # end def add_user_sum

    def add_plan (self, other_container, duration) :
        if other_container not in self.plans :
            self.plans [other_container] = PM_Value (0)
        self.plans [other_container] += PM_Value (duration, not duration)
    # end def add_plan

    def get_sum (self, other_container, username = None, default = None) :
        key = other_container
        if username :
            key = (other_container, username)
        if key in self.sums :
            return self.sums [key]
        return default
    # end def get_sum

    def get_plan (self, other_container, default = None) :
        if other_container in self.plans :
            return self.plans [other_container]
        return default
    # end def get_plan

    def as_html (self) :
        return cgi.escape (str (self))
    # end def as_html
# end class Container

class Time_Container (Container) :
    """ Container for time-ranges: has a start and end date and a hash
        of WP_Container to sum objects.
    """
    def __init__ (self, start, end) :
        self.__super.__init__ ()
        self.start    = start
        self.end      = end
        self.sort_end = end
    # end def __init__

    def __repr__ (self) :
        return "%s (%s, %s)" % (self.__class__.__name__, self.start, self.end)
    # end def __repr__

    __str__ = __repr__

    def __hash__ (self) :
        return hash (repr (self))
    # end def __hash__
# end class Time_Container

class Day_Container (Time_Container) :
    def __init__ (self, day) :
        date = Date (day.pretty (ymd))
        self.__super.__init__ (date, date + Interval ('1d'))
    # end def __init__

    def __str__ (self) :
        return self.start.pretty (ymd)
    # end def __str__
# end class Day_Container

class Week_Container (Time_Container) :
    def __init__ (self, day) :
        start, end = week_from_date  (day)
        self.__super.__init__ (start, end + Interval ('1d'))
    # end def __init__

    def __str__ (self) :
        return "WW %s/%s" % \
            (weekno_from_day (self.start), self.start.pretty ('%Y'))
    # end def __str__
# end class Week_Container

class Month_Container (Time_Container) :
    def __init__ (self, day) :
        year   = day.year
        month  = day.month
        nmonth = day.month + 1
        nyear  = year
        if nmonth > 12 :
            nmonth = 1
            nyear = year + 1
        fmt = '%4s-%s-01'
        self.__super.__init__ \
            (Date (fmt % (year, month)), Date (fmt % (nyear, nmonth)))
    # end def __init__

    def __str__ (self) :
        return self.start.pretty ("%B %Y")
    # end def __str__
# end class Month_Container

class Range_Container (Time_Container) :
    """ Contains the whole selected time-range """
    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.sort_end = self.end + Interval ('1m')
    # end def __init__

    def __str__ (self) :
        return "%s;%s" % (self.start.pretty (ymd), self.end.pretty (ymd))
    # end def __str__
# end class Range_Container

time_container_classes = \
    { 'day'   : Day_Container
    , 'week'  : Week_Container
    , 'month' : Month_Container
    , 'range' : Range_Container
    }

class Comparable_Container (Container, dict) :
    sortkey = 50
    def __str__ (self) :
        return self.name
    # end def __str__

    def __cmp__ (self, other) :
        return \
            (  cmp (self.sortkey, other.sortkey) 
            or cmp (_ (self.classname), _ (other.classname))
            or cmp (self.name, other.name)
            )
    # end def __cmp__

# end class Comparable_Container

class Sum_Container (Comparable_Container, dict) :
    sortkey = 100
    def __init__ (self, name = "Sum", visible = True, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.name      = name
        self.visible   = visible
        self.classname = ''
    # end def __init__

    def __repr__ (self) :
        classname = self.__class__.__name__
        return "%s (%s, %s, %s)" % \
            (classname, self.name, self.visible, self.__super.__repr__ ())
    # end def __repr__

    def __hash__ (self) :
        return hash ((self.__class__, self.name))
    # end def __hash__
# end class Sum_Container

class WP_Container (Comparable_Container, dict) :
    def __init__ \
        (self, klass, id, visible = True, verbname = '', * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.klass     = klass
        self.classname = klass.classname
        self.id        = id
        self.visible   = visible
        self.name      = klass.get (id, 'name')
        self.verbname  = verbname

        if klass.classname == 'time_wp' :
            self.sortkey = 30
            p = klass.db.time_project.get (klass.get (id, 'project'), 'name')
            self.name  = '/'.join ((p, self.name))
    # end def __init__
    
    def __repr__ (self) :
        name = self.__class__.__name__
        return "%s (%s, %s, %s)" % \
            (name, self.classname, self.id, self.__super.__repr__ ())
    # end def __repr__

    def __str__ (self) :
        return "%s %s %s" % (_ (self.classname), self.name, self.verbname)
    # end def __str__

    def as_html (self) :
        return "%s %s %s" % \
            ( cgi.escape (_ (self.classname)).replace (' ', '&nbsp;')
            , cgi.escape (self.name).replace          (' ', '&nbsp;')
            , cgi.escape (self.verbname).replace      (' ', '&nbsp;')
            )

    def __hash__ (self) :
        return hash ((self.__class__, self.classname, self.id))
    # end def __hash__
# end class WP_Container

class Summary_Report :
    """ TODO:
        - special colors for 
          - daily record not yet accepted
          - no daily record found -- involves checking dynamic user data
        FIXME: Check where we need naive dates...
    """
    def __init__ (self, db, request) :
        try :
            db = db._db
        except AttributeError :
            pass
        filterspec      = request.filterspec
        sort_by         = request.sort
        group_by        = request.group
        columns         = request.columns
        now             = Date ('.')
        assert (request.classname == 'summary_report')
        sup_users       = user_supervisor_for (db)
        wp_containers   = []
        if not columns :
            columns     = db.summary_report.getprops ().keys ()
        self.columns    = dict ((c, True) for c in columns)
        status          = filterspec.get \
            ('status', db.daily_record_status.getnodeids ())
        timestamp       = time.time ()
        show_empty      = filterspec.get ('show_empty',     'no')
        show_all_users  = filterspec.get ('show_all_users', 'no')
        self.show_empty = show_empty == 'yes'
        show_all_users  = self.show_all_users = show_all_users == 'yes'
        travel_act      = db.time_activity.filter (None, {'travel' : True})
        travel_act      = dict ((a, 1) for a in travel_act)
        self.show_plan  = 'planned_effort' in self.columns

        #print "time", timestamp
        #print filterspec
        #print self.columns, self.show_plan
        start, end  = date_range (db, filterspec)
        users       = filterspec.get ('user', [])
        sv          = dict ((i, 1) for i in filterspec.get ('supervisor', []))
        svu         = []
        if sv :
            svu     = db.user.find (supervisor = sv)
        users       = dict ((u, 1) for u in users + svu).keys ()
        olo_or_dept = False
        drecs       = {}
        org_dep_usr = {}
        for cl in 'department', 'org_location' :
            spec = dict ((s, 1) for s in filterspec.get (cl, []))
            if spec :
                olo_or_dept = True
                udrs        = []
                for i in db.user_dynamic.find (** {cl : spec}) :
                    ud = db.user_dynamic.getnode (i)
                    if  (   ud.valid_from < end
                        and (not ud.valid_to or ud.valid_to > start)
                        ) :
                        udrs.append (ud)
                        org_dep_usr [ud.user] = 1
                for ud in udrs :
                    udstart = max (ud.valid_from, start)
                    if ud.valid_to :
                        udend = min (ud.valid_to - Interval ('1d'), end)
                    else :
                        udend = end
                    assert (udstart < udend)
                    drs = db.daily_record.filter \
                        ( None, dict 
                            ( user   = ud.user
                            , date   = pretty_range (udstart, udend)
                            , status = status
                            )
                        )
                    edr = Extended_Daily_Record
                    drs = [edr (db, d, sup_users) for d in drs]
                    drecs.update (dict ((d.id, d) for d in drs))

        #print "after departments:", time.time () - timestamp
        if not users and not olo_or_dept :
            users   = db.user.getnodeids () # also invalid users!
        #print users, start, end, status
        dr          = []
        if users :
            dr = db.daily_record.filter \
                ( None, dict 
                    ( user   = users
                    , date   = pretty_range (start, end)
                    , status = status
                    )
                )
        #print "n_dr:", len (dr), time.time () - timestamp
        dr          = dict \
            ((d, Extended_Daily_Record (db, d, sup_users)) for d in dr)
        #print "after users:", time.time () - timestamp
        dr.update (drecs)
        #print "after dr.update:", time.time () - timestamp
        self.dr_by_user_date = dict \
            (((str (v.username), v.date.pretty (ymd)), v)
             for v in dr.itervalues ()
            )
        #print "after dr_dat_usr:", time.time () - timestamp

        trvl_tr     = []
        if dr :
            trvl_tr = db.time_record.find \
                (daily_record = dr, time_activity = travel_act)
        trvl_dr     = {}
        for trid in trvl_tr :
            t = db.time_record.getnode (trid)
            if  (  t.time_activity not in travel_act
                or t.tr_duration and t.activity > dr [t.daily_record].activity
                ) :
                continue
            trvl_dr [t.daily_record] = dr [t.daily_record]
        if trvl_dr :
            for d in trvl_dr.itervalues () :
                #print "update"
                update_tr_duration (db, d)
            db.commit ()
        #print "trv daily_recs", len (trvl_dr), time.time () - timestamp

        wp          = dict ((w, 1) for w in filterspec.get ('time_wp', []))
        #print "native wp", len (wp), time.time () - timestamp

        wpgs        = filterspec.get ('time_wp_group',     [])
        for wpg in wpgs :
            wp_containers.append \
                ( WP_Container
                    ( db.time_wp_group, wpg
                    , 'time_wp_group' in self.columns
                    , ''
                    , [(w, 1) for w in db.time_wp_group.get (wpg, 'wps')]
                    )
                )
            wp.update (wp_containers [-1])
        #print "wpgs", len (wp), time.time () - timestamp
        projects    = filterspec.get ('time_project',      [])
        #print projects
        for p in projects :
            #print p, db.time_wp.find (project = p)
            wp_containers.append \
                ( WP_Container
                    ( db.time_project, p
                    , 'time_project' in self.columns
                    , ''
                    , [(w, 1) for w in db.time_wp.find (project = p)]
                    )
                )
            #print wp_containers [-1]
            wp.update (wp_containers [-1])
        #print "projects", len (wp), time.time () - timestamp
        ccs         = filterspec.get ('cost_center',       [])
        for cc in ccs :
            wp_containers.append \
                ( WP_Container
                    ( db.cost_center, cc
                    , 'cost_center' in self.columns
                    , ''
                    , [(w, 1) for w in db.time_wp.find (cost_center = cc)]
                    )
                )
            wp.update (wp_containers [-1])
        #print "ccs", len (wp), time.time () - timestamp
        ccgs        = filterspec.get ('cost_center_group', [])
        for ccg in ccgs :
            ccs     = db.cost_center.find (cost_center_group = ccg)
            ccs     = dict ((c, 1) for c in ccs)
            wp_containers.append \
                ( WP_Container 
                    ( db.cost_center_group, ccg
                    , 'cost_center_group' in self.columns
                    )
                )
            for cc in ccs :
                wps = dict ((w,1) for w in db.time_wp.find (cost_center = cc))
                wp_containers [-1].update (wps)
            wp.update (wp_containers [-1])
        #print "ccgs", len (wp), time.time () - timestamp
        if  (    not wp
            and 'time_wp'           not in filterspec
            and 'time_wp_group'     not in filterspec
            and 'time_project'      not in filterspec
            and 'cost_center'       not in filterspec
            and 'cost_center_group' not in filterspec
            ) :
            wp = dict ((w, 1) for w in db.time_wp.getnodeids ())
        #print "wp-default", len (wp), time.time () - timestamp
        #print "n_wp:", len (wp)
        work_pkg    = dict ((w, Extended_WP (db, w)) for w in wp.iterkeys ())
        #print "ext wp", time.time () - timestamp
        time_recs   = []
        # 276 sec: (4.6 min) (for Decos: ~ 250 sec)
        if dr and wp :
            time_recs = []
            for d in dr.itervalues () :
                for t in d.time_record :
                    if db.time_record.get (t, 'wp') in work_pkg :
                        tr = Extended_Time_Record (db, t, dr, work_pkg)
                        time_recs.append (tr)
        #print "ext time_recs", len (time_recs), time.time () - timestamp
        time_recs   = [t for t in time_recs if t.is_own]
        #print "own time_recs", len (time_recs), time.time () - timestamp
        time_recs.sort ()
        #print "srt time_recs", len (time_recs), time.time () - timestamp
        if self.show_empty :
            usrs      = users + org_dep_usr.keys ()
            usernames = dict ((db.user.get (u, 'username'), 1) for u in usrs)
            usernames = usernames.keys ()
        else :
            usernames = dict ((tr.username, 1) for tr in time_recs).keys ()
        #print "         usernames", time.time () - timestamp
        uids_by_name  = dict ((u, db.user.lookup (u)) for u in usernames)
        # filter out users without a dyn user record in our date range
        #print usernames
        if not self.show_all_users :
            users = []
            for u in usernames :
                d   = start
                while d <= end :
                    if get_user_dynamic (db, uids_by_name [u], d) :
                        users.append (u)
                        break
                    d = d + Interval ('1d')
            usernames = users

        #print "filtered usernames", time.time () - timestamp
        usernames.sort ()
        #print "sorted   usernames", time.time () - timestamp
        #print usernames
        
        # append only wps where somebody actually booked on
        wps         = dict ((tr.wp.id, 1) for tr in time_recs)
        for w in wps.iterkeys () :
            wp_containers.append \
                ( WP_Container 
                    ( db.time_wp, w
                    , 'time_wp' in self.columns
                    , [''
                      , ( '%s %s'
                        % ( _ ('cost_center')
                          , db.cost_center.get
                            (db.time_wp.get (w, 'cost_center'), 'name')
                          )
                        )
                      ]['cost_center' in self.columns]
                    , ((w, 1),)
                    )
                )
        #print "filtered wps", time.time () - timestamp
        wp_containers.append \
            (Sum_Container (_ ('Sum'), 'summary' in self.columns, wps))

        # Build time containers
        rep_types  = filterspec.get \
            ('summary_type', [db.summary_type.lookup ('range')])
        rep_types  = [db.summary_type.get (i, 'name') for i in rep_types]
        time_containers = dict ((t, []) for t in rep_types)
        d = start
        while d <= end :
            for t, cont in time_containers.iteritems () :
                if not cont or cont [-1].end <= d :
                    try :
                        cont.append (time_container_classes [t] (d))
                    except TypeError :
                        cont.append (time_container_classes [t] (start, end))
            d = d + Interval ('1d')
        #print "time containers", time.time () - timestamp
        wp_containers = [w for w in wp_containers if w.visible]
        wp_containers.sort ()
        #print "sorted wp containers", time.time () - timestamp
        # invert wp_containers
        containers_by_wp = {}
        for wc in wp_containers :
            for w in wc :
                if w in containers_by_wp :
                    containers_by_wp [w].append (wc)
                else :
                    containers_by_wp [w]      = [wc]
        #print "inverted wp containers", time.time () - timestamp
        tc_pointers = dict ((i, 0) for i in time_containers.iterkeys ())
        #print "after tc_pointers", time.time () - timestamp

        d        = start
        tidx     = 0
        invalid  = PM_Value (0, 1)
        # wp may not be viewable due to permissions
        valid_wp = \
            [w for w in work_pkg.itervalues () if w.id in containers_by_wp]
        while d <= end :
            no_daily_record = \
                [u for u in usernames
                 if (   (u, d.pretty (ymd)) not in self.dr_by_user_date
                    and (  self.show_all_users
                        or get_user_dynamic (db, uids_by_name [u], d)
                        )
                    )
                ]
            #print "user", len (no_daily_record), time.time () - timestamp
            for tcp in tc_pointers.iterkeys () :
                while (d >= time_containers [tcp][tc_pointers [tcp]].sort_end) :
                    tc_pointers [tcp] += 1
                tc = time_containers [tcp][tc_pointers [tcp]]
                for w in valid_wp :
                    for wc in containers_by_wp [w.id] :
                        wc.add_plan (tc, w.effort (d))
                        tc.add_plan (wc, w.effort (d))
                        for u in no_daily_record :
                            wc.add_user_sum (tc, u, invalid)
                            tc.add_user_sum (wc, u, invalid)
            #print "plan", time.time () - timestamp
            while tidx < len (time_recs) and time_recs [tidx].date == d :
                t  = time_recs [tidx]
                for tcp in tc_pointers.iterkeys () :
                    tc = time_containers [tcp][tc_pointers [tcp]]
                    for wpc in containers_by_wp [t.wp.id] :
                        tc. add_sum (wpc, t)
                        wpc.add_sum (tc,  t)
                tidx += 1
            d = d + Interval ('1d')
            #print "1d", time.time () - timestamp
        #print "SUMs built", time.time () - timestamp
        self.wps             = wps
        self.usernames       = usernames
        self.start           = start
        self.end             = end
        self.time_containers = time_containers
        self.wp_containers   = wp_containers
    # end def __init__

    def html_item (self, item) :
        if not item and not isinstance (item, dict) and not item == 0 :
            return "   <td/>"
        if isinstance (item, PM_Value) :
            if item.missing and not item :
                return ('  <td class="missing"/>')
            return \
                ('  <td %sstyle="text-align:right;">%2.02f</td>'
                % (['class="missing" ', ''][not item.missing], item)
                )
        if isinstance (item, type (0.0)) or isinstance (item, PM_Value) :
            return ('  <td style="text-align:right;">%2.02f</td>' % item)
        return ('  <td>%s</td>' % item.as_html ())
    # end def html_item

    def html_header_item (self, item) :
        return ('  <th>%s</th>' % str (item))
    # end def html_header_item

    def html_line (self, items) :
        items.insert (0, " <tr>")
        items.append (" </tr>")
        self.html_output.extend (items)
    # end def html_line

    def csv_item (self, item) :
        if not item and not isinstance (item, dict) and not item == 0 :
            return ''
        if isinstance (item, PM_Value) :
            if item.missing and not item :
                return "-"
            return '%2.02f' % item
        if isinstance (item, type (0.0)) :
            return '%2.02f' % item
        return str (item)
    # end def csv_item

    def csv_line (self, items) :
        self.csvwriter.writerow (items)
    # end def csv_line

    def header_line (self, formatter) :
        line = []
        line.append (formatter (_ ('Container')))
        line.append (formatter (_ ('time')))
        if 'user' in self.columns :
            for u in self.usernames :
                line.append (formatter (u))
        line.append (formatter (_ ('Sum')))
        if self.show_plan :
            for i in 'planned_effort', '%', 'remaining' :
                line.append (formatter (_ (i)))
        return line
    # end def header_line

    def _output_line (self, wpc, type, idx, formatter) :
        line = []
        tc   = self.time_containers [type][idx]
        line.append (formatter (wpc))
        line.append (formatter (tc))
        if 'user' in self.columns :
            for u in self.usernames :
                line.append (formatter (tc.get_sum (wpc, u, '')))
        sum = tc.get_sum (wpc, default = PM_Value (0.0))
        line.append (formatter (sum))
        if self.show_plan :
            plan = tc.get_plan (wpc)
            line.append (formatter (plan))
            if plan :
                line.append (formatter (sum * 100. / plan))
                line.append (formatter (plan - sum))
            else :
                missing = plan is None or plan.missing
                line.append (formatter (PM_Value (0, missing)))
                line.append (formatter (PM_Value (0, missing)))
        return line
    # end def _output_line

    def _output (self, line_formatter, item_formatter) :
        start = self.start + Interval ('1d')
        end   = max \
            ([self.time_containers [i][-1].sort_end
              for i in self.time_containers.keys ()
            ])
        for wpc in self.wp_containers :
            tc_pointers = dict \
                ([(i, 0) for i in self.time_containers.iterkeys ()])
            d = start
            containertypes = 'day', 'week', 'month', 'range' # order matters.
            while d <= end :
                for tcp in [i for i in containertypes if i in tc_pointers] :
                    try :
                        tc = self.time_containers [tcp][tc_pointers [tcp]]
                    except IndexError :
                        continue
                    if d >= tc.sort_end :
                        if  (   wpc.visible
                            and (self.show_empty or tc.get_sum (wpc))
                            ) :
                            line_formatter \
                                ( self._output_line
                                  (wpc, tcp, tc_pointers [tcp], item_formatter)
                                )
                        tc_pointers [tcp] += 1
                d = d + Interval ('1d')
    # end def _output

    def as_html (self) :
        s = self.html_output = ['']
        s.append ('<table class="list" border="1">')
        self.html_line (self.header_line (self.html_header_item))
        self._output   (self.html_line, self.html_item)
        s.append ("</table>")
        return '\n'.join (s)
    # end def as_html

    def as_csv (self) :
        io             = StringIO ()
        self.csvwriter = csv.writer (io, dialect = 'excel', delimiter = ',')
        self.csv_line (self.header_line (self.csv_item))
        self._output  (self.csv_line, self.csv_item)
        return io.getvalue ()
    # end def as_csv
# end class Summary_Report

class csv_summary_report (Action) :
    def handle (self) :
        request                   = templating.HTMLRequest (self.client)
        h                         = self.client.additional_headers
        h ['Content-Type']        = 'text/csv'
        h ['Content-Disposition'] = 'inline; filename=summary.csv'
        self.client.header    ()
        if self.client.env ['REQUEST_METHOD'] == 'HEAD' :
            # all done, return a dummy string
            return 'dummy'
        summary                   = Summary_Report (self.db, request)
        return summary.as_csv ()
    # end def handle
# end class csv_summary_report

def init (instance) :
    global _, ymd, pretty_range, week_from_date, user_has_role, date_range
    global weekno_from_day, update_tr_duration, get_user_dynamic
    sys.path.insert (0, os.path.join (instance.config.HOME, 'lib'))
    _   = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.config.TRACKER_HOME).gettext
    from common import pretty_range, week_from_date, ymd, user_has_role \
                     , date_range, weekno_from_day
    from user_dynamic import update_tr_duration, get_user_dynamic
    del sys.path [0]
    util   = instance.registerUtil
    util   ('Summary_Report',     Summary_Report)
    action = instance.registerAction
    action ('csv_summary_report', csv_summary_report)
# end def init
