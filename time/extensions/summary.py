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
try :
    from cStringIO import StringIO
except ImportError :
    from StringIO  import StringIO

from roundup.date                   import Date, Interval
from roundup.cgi                    import templating
from roundup.cgi.TranslationService import get_translation
from roundup.cgi.actions            import Action

_      = lambda x : x

try :
    from common import pretty_range, week_from_date, ymd, user_has_role \
                     , date_range, weekno_from_day
except ImportError :
    ymd             = None
    pretty_range    = None
    week_from_date  = None
    user_has_role   = None
    date_range      = None
    weekno_from_day = None

class _autosuper (type) :
    def __init__ (cls, name, bases, dict) :
        super   (_autosuper, cls).__init__ (name, bases, dict)
        setattr (cls, "_%s__super" % name, super (cls))
    # end def __init__
# end class _autosuper

class autosuper (object) :
    __metaclass__ = _autosuper
    pass
# end class autosuper

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
    sv                = dict ([(u, 1) for u in db.user.find (substitute = uid)])
    sv [uid]          = 1
    users             = db.user.find (supervisor = sv)
    trans_users       = []
    for u in users :
        trans_users.extend (user_supervisor_for (db, u))
    sup_cache [uid] = dict ([(u, 1) for u in users + trans_users])
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
        deputy for the project of the WP.
    """
    def __init__ (self, db, wpid) :
        self.node         = db.time_wp.getnode  (wpid)
        self.project_name = db.time_project.get (self.project, 'name')
        uid               = db.getuid ()
        p_owner           = db.time_project.get (self.project, 'responsible')
        p_deputy          = db.time_project.get (self.project, 'deputy')
        self.is_own       = \
            (uid == self.responsible or uid == p_owner or uid == p_deputy)
    # end def __init__

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
        self.sums = {}
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def add (self, other_container, tr) :
        for key in other_container, (other_container, tr.username) :
            if key not in self.sums :
                self.sums [key]  = tr.duration
            else :
                self.sums [key] += tr.duration
    # end def add

    def get (self, other_container, username = None, default = None) :
        key = other_container
        if username :
            key = (other_container, username)
        if key in self.sums :
            return self.sums [key]
        return default
    # end def get
# end class Container

class Time_Container (Container) :
    """ Container for time-ranges: has a start and end date and a hash
        of WP_Container to sum objects.
    """
    def __init__ (self, start, end) :
        self.__super.__init__ ()
        self.start = start
        self.end   = end
    # end def __init__

    def __repr__ (self) :
        return "%s (%s, %s)" % (self.__class__.__name__, self.start, self.end)
    # end def __repr__

    __str__ = __repr__

    def __hash__ (self) :
        return hash (str (self))
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
            month = 1
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
    def __str__ (self) :
        return _ ("All")
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
    def __init__ (self, klass, id, visible = True, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.klass     = klass
        self.classname = klass.classname
        self.id        = id
        self.visible   = visible
        self.name      = klass.get (id, 'name')

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
        return "%s %s" % (_ (self.classname), self.name)
    # end def __str__

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
        filterspec    = request.filterspec
        sort_by       = request.sort
        group_by      = request.group
        columns       = request.columns
        now           = Date ('.')
        assert (request.classname == 'summary_report')
        sup_users     = user_supervisor_for (db)
        wp_containers = []
        if not columns :
            columns   = db.summary_report.getprops ().keys ()
        self.columns  = dict ([(c, True) for c in columns])

        #print filterspec
        start, end  = date_range (db, filterspec)
        users       = filterspec.get ('user', [])
        sv          = dict ([(i, 1) for i in filterspec.get ('supervisor', [])])
        svu         = []
        if sv :
            svu     = db.user.find (supervisor = sv)
        users       = dict ([(u, 1) for u in users + svu]).keys ()
        if not users :
            valid   = db.user_status.lookup ('valid')
            users   = db.user.find (status = valid)
        # FIXME: get user_dynamic records for all dept and org_locs
        # then compute the daily_records that match.
        dr          = db.daily_record.filter \
            ( None, dict 
                ( user   = users
                , date   = pretty_range (start, end)
                , status = db.daily_record_status.lookup ('accepted')
                )
            )
        #print "n_dr:", len (dr)
        dr          = dict \
            ([(d, Extended_Daily_Record (db, d, sup_users)) for d in dr])

        wp          = dict ([(w, 1) for w in filterspec.get ('time_wp', [])])

        wpgs        = filterspec.get ('time_wp_group',     [])
        for wpg in wpgs :
            wp_containers.append \
                ( WP_Container
                    ( db.time_wp_group, wpg
                    , 'time_wp_group' in self.columns
                    , [(w, 1) for w in db.time_wp_group.get (wpg, 'wps')]
                    )
                )
            wp.update (wp_containers [-1])
        projects    = filterspec.get ('time_project',      [])
        for p in projects :
            wp_containers.append \
                ( WP_Container
                    ( db.time_project, p
                    , 'time_project' in self.columns
                    , [(w, 1) for w in db.time_wp.find (project = p)]
                    )
                )
            wp.update (wp_containers [-1])
        ccs         = filterspec.get ('cost_center',       [])
        for cc in ccs :
            wp_containers.append \
                ( WP_Container
                    ( db.cost_center, cc
                    , 'cost_center' in self.columns
                    , [(w, 1) for w in db.time_wp.find (cost_center = cc)]
                    )
                )
            wp.update (wp_containers [-1])
        ccgs        = filterspec.get ('cost_center_group', [])
        for ccg in ccgs :
            ccs     = db.cost_center.find (cost_center_group = ccg)
            ccs     = dict ([(c, 1) for c in ccs])
            wp_containers.append \
                ( WP_Container 
                    ( db.cost_center_group, ccg
                    , 'cost_center_group' in self.columns
                    )
                )
            for cc in ccs :
                wps = dict ([(w,1) for w in db.time_wp.find (cost_center = cc)])
                wp_containers [-1].update (wps)
            wp.update (wp_containers [-1])
        if not wp :
            wp = dict ([(w, 1) for w in db.time_wp.getnodeids ()])
        #print "n_wp:", len (wp)
        work_pkg    = dict ([(w, Extended_WP (db, w)) for w in wp.iterkeys ()])
        time_recs   = []
        if dr :
            time_recs = [Extended_Time_Record (db, t, dr, work_pkg)
                         for t in db.time_record.find
                          (daily_record = dr, wp = work_pkg)
                        ]
        time_recs   = [t for t in time_recs if t.is_own]
        #print "n_tr:", len (time_recs)
        time_recs.sort ()
        usernames   = dict ([(tr.username, 1) for tr in time_recs]).keys ()
        usernames.sort ()
        #print usernames
        
        # append only wps where somebody actually booked on
        wps         = dict ([(tr.wp.id, 1) for tr in time_recs])
        for w in wps.iterkeys () :
            wp_containers.append \
                ( WP_Container 
                    ( db.time_wp, w
                    , 'time_wp' in self.columns
                    , ((w, 1),)
                    )
                )
        wp_containers.append \
            (Sum_Container (_ ('Sum'), 'summary' in self.columns, wps))

        # Build time containers
        rep_types  = filterspec.get ('summary_type', ('1', '2', '3'))
        rep_types  = [db.summary_type.get (i, 'name') for i in rep_types]
        time_containers = dict ([(t, []) for t in rep_types])
        d = start
        while d <= end :
            for t, cont in time_containers.iteritems () :
                if not cont or cont [-1].end <= d :
                    try :
                        cont.append (time_container_classes [t] (d))
                    except TypeError :
                        cont.append \
                            ( time_container_classes [t]
                                (start, end + Interval ('1m'))
                            )
            d = d + Interval ('1d')
        wp_containers.sort ()
        # invert wp_containers
        containers_by_wp = {}
        for wc in wp_containers :
            for w in wc :
                if w in containers_by_wp :
                    containers_by_wp [w].append (wc)
                else :
                    containers_by_wp [w]      = [wc]
        tc_pointers = dict ([(i, 0) for i in time_containers.iterkeys ()])
        for t in time_recs :
            for tcp in tc_pointers.iterkeys () :
                while t.date >= time_containers [tcp][tc_pointers [tcp]].end :
                    tc_pointers [tcp] += 1
                tc = time_containers [tcp][tc_pointers [tcp]]
                for wpc in containers_by_wp [t.wp.id] :
                    tc. add (wpc, t)
                    wpc.add (tc,  t)
        self.wps             = wps
        self.usernames       = usernames
        self.start           = start
        self.end             = end
        self.time_containers = time_containers
        self.wp_containers   = wp_containers
    # end def __init__

    def html_item (self, item) :
        if not item :
            return "   <td/>"
        if isinstance (item, type (0.0)) :
            return ('  <td style="text-align:right;">%2.02f</td>' % item)
        return ('  <td>%s</td>' % str (item))
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
        if not item :
            return ''
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
        return line
    # end def header_line

    def _output_line (self, wpc, type, idx, formatter) :
        line = []
        tc   = self.time_containers [type][idx]
        line.append (formatter (wpc))
        line.append (formatter (tc))
        if 'user' in self.columns :
            for u in self.usernames :
                line.append (formatter (tc.get (wpc, u, '')))
        line.append (formatter (tc.get (wpc)))
        return line
    # end def _output_line

    def _output (self, line_formatter, item_formatter) :
        start = self.start + Interval ('1d')
        end   = max \
            ([self.time_containers [i][-1].end
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
                    if d >= tc.end :
                        if wpc.visible :
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
    global weekno_from_day
    sys.path.insert (0, os.path.join (instance.config.HOME, 'lib'))
    _   = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.config.TRACKER_HOME).gettext
    from common import pretty_range, week_from_date, ymd, user_has_role \
                     , date_range, weekno_from_day
    del sys.path [0]
    util   = instance.registerUtil
    util   ('Summary_Report',     Summary_Report)
    action = instance.registerAction
    action ('csv_summary_report', csv_summary_report)
# end def init
