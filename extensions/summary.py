#! /usr/bin/python
# Copyright (C) 2006-24 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
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
#
#++
# Name
#    summary
#
# Purpose
#    Time-tracking summary reports, vacation report
#

from __future__ import division
import csv
import time

from math import ceil
from html import escape
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
from roundup.anypy.strings          import StringIO
from roundup.date                   import Date, Interval
from roundup.cgi                    import templating
from roundup.cgi.actions            import Action
from roundup.configuration          import InvalidOptionError
from rsclib.autosuper               import autosuper
from rsclib.PM_Value                import PM_Value
from o_permission                   import dynamic_user_allowed_by_olo

import common
import request_util
import sum_common
import user_dynamic
import vacation

day = common.day
ymd = common.ymd

class Extended_Node (autosuper):
    def __getattr__ (self, name):
        """ Delegate everything to our node """
        if not name.startswith ('__'):
            result = getattr (self.node, name)
            setattr (self, name, result)
            return result
        raise AttributeError (name)
    # end def __getattr__

    def __repr__ (self):
        return "%s (%s)" % (self.__class__.__name__, repr (self.name))
    # end def __repr__

    __str__ = __repr__

# end class Extended_Node

class Extended_Daily_Record (Extended_Node):
    """ Keeps information about the username *and* about the status of
        the daily_records: own records (is_own = True) are records wich
        may be unconditionally viewed by the user. For details about
        permissions, see lib/sum_common.py daily_record_viewable.
    """

    def __init__ (self, db, drid):
        self.node     = db.daily_record.getnode (drid)
        self.username = db.user.get (self.user, 'username')
        self.name     = self.username
        self.is_own   = sum_common.daily_record_viewable \
            (db, db.getuid (), drid)
    # end def __init__

    def __cmp__ (self, other):
        return \
            cmp (self.date, other.date) or cmp (self.username, other.username)
    # end def __cmp__

    def __lt__ (self, other):
        return \
            (  self.date < other.date
            or self.date == other.date and self.username < other.username
            )
    # end def __lt__

# end class Extended_Daily_Record

class Extended_WP (Extended_Node):
    """ Keeps information about the username *and* about the status of
        the work package.
        
        For permissions, see time_wp_viewable in lib/sum_common.py
    """
    def __init__ (self, db, wpid):
        self.node          = db.time_wp.getnode  (wpid)
        self.project_name  = db.time_project.get (self.project, 'name')
        self.is_own        = sum_common.time_wp_viewable \
            (db, db.getuid (), wpid)
        self.effort_perday = PM_Value (0, 1)
        if  (   self.time_start and self.time_end
            and self.planned_effort is not None
            ):
            self.start = s = Date (str (self.time_start))
            self.end   = e = Date (str (self.time_end))
            days       = (e - s).get_tuple () [3]
            if days:
                self.effort_perday = PM_Value (self.planned_effort / days)
    # end def __init__

    def effort (self, date):
        if not self.effort_perday.missing:
            if self.start <= date <= self.end:
                return self.effort_perday
            return PM_Value (0)
        return self.effort_perday
    # end def effort

    def __cmp__ (self, other):
        return \
            (  cmp (self.project_name, other.project_name)
            or cmp (self.name,         other.name)
            )
    # end def __cmp__

    def __lt__ (self, other):
        return \
            (  self.project_name < other.project_name
            or self.project_name == other.project_name
               and self.name < other.name
            )
    # end def __lt__
# end class Extended_WP

class Extended_Time_Record (Extended_Node):
    """ Keeps information about the username *and* about the status of
        the time record: own records (is_own = True) are records wich
        may be unconditionally viewed by the user. This is the case if
        the user owns the wp or owns the daily_record of the time
        record.
    """
    def __init__ (self, db, trid, dr, wp):
        self.node         = db.time_record.getnode  (trid)
        self.dr           = dr [self.node.daily_record]
        self.wp           = wp [self.node.wp]
        self.is_own       = self.dr.is_own or self.wp.is_own
    # end def __init__

    def __getattr__ (self, name):
        """ Delegate everything to first the daily_record, then the wp,
            then our node.
        """
        if not name.startswith ('__'):
            for x in self.dr, self.wp:
                try:
                    result = getattr (x, name)
                    setattr (self, name, result)
                    return result
                except AttributeError:
                    return self.__super.__getattr__ (name)
        raise AttributeError (name)
    # end def __getattr__

    def __cmp__ (self, other):
        return (cmp (self.dr, other.dr) or cmp (self.wp, other.wp))
    # end def __cmp__

    def __lt__ (self, other):
        return self.dr < other.dr or self.dr == other.dr and self.wp < other.wp
    # end def __lt__
# end class Extended_Time_Record

class Dict_Mixin (dict, autosuper):
    """ Used to never pass kw to dict constructor
    """
    def __init__ (self, *args, **kw):
        self.__super.__init__ (*args)
    # end def __init__
# end class Dict_Mixin

class Container (autosuper):
    def __init__ (self, *args, **kw):
        self.i18n = kw ['i18n']
        self.sums  = {}
        self.plans = {}
        self.__super.__init__ (*args, **kw)
    # end def __init__

    def add_user_sum (self, other_container, username, sum, do_sum = True):
        keys = [(other_container, username)]
        if do_sum:
            keys.insert (0, other_container)
        for key in keys:
            if key not in self.sums:
                self.sums [key] = PM_Value (0)
            self.sums [key] += sum
    # end def add_user_sum

    def add_sum_column (self, other_container, column_name, tr, do_sum = True):
        self.add_user_sum \
            ( other_container
            , column_name
            , tr.tr_duration or tr.duration
            , do_sum
            )
    # end def add_sum_column

    def add_sum (self, other_container, tr):
        self.add_sum_column (other_container, tr.username, tr)
    # end def add_sum

    def add_plan (self, other_container, duration):
        if other_container not in self.plans:
            self.plans [other_container] = PM_Value (0)
        self.plans [other_container] += PM_Value (duration, not duration)
    # end def add_plan

    def get_sum (self, other_container, username = None, default = None):
        key = other_container
        if username:
            key = (other_container, username)
        if key in self.sums:
            return self.sums [key]
        return default
    # end def get_sum

    def get_plan (self, other_container, default = None):
        if other_container in self.plans:
            return self.plans [other_container]
        return default
    # end def get_plan

    def as_html (self):
        return escape (str (self))
    # end def as_html

    def __getattr__ (self, name):
        """ Provide a default for all sorts of ids """
        if name.endswith ('.id'):
            return ''
        raise AttributeError (name)
    # end def __getattr__

# end class Container

class Time_Container (Container):
    """ Container for time-ranges: has a start and end date and a hash
        of WP_Container to sum objects.
    """
    def __init__ (self, start, end, **kw):
        self.__super.__init__ (**kw)
        self.start    = start
        self.end      = end
        self.sort_end = end
        self.dict     = {}
    # end def __init__

    def __repr__ (self):
        return "%s (%s, %s)" % (self.__class__.__name__, self.start, self.end)
    # end def __repr__

    __str__ = __repr__

    def __hash__ (self):
        return hash (repr (self))
    # end def __hash__

    def __setitem__ (self, name, value):
        self.dict [name] = value
    # end def __setitem__

    def __getitem__ (self, name):
        return self.dict [name]
    # end def __getitem__

    def __delitem__ (self, name):
        del self.dict [name]
    # end def __delitem__

    def __iter__ (self):
        return self.dict
    # end def __iter__

    def __contains__ (self, name):
        return name in self.dict
    # end def __contains__

# end class Time_Container

class Day_Container (Time_Container):
    def __init__ (self, day, **kw):
        date = Date (day.pretty (ymd))
        self.__super.__init__ (date, date + Interval ('1d'), **kw)
    # end def __init__

    def __str__ (self):
        return self.start.pretty (ymd)
    # end def __str__
# end class Day_Container

class Week_Container (Time_Container):
    def __init__ (self, day, **kw):
        start, end = common.week_from_date  (day)
        self.__super.__init__ (start, end + Interval ('1d'), **kw)
    # end def __init__

    def __str__ (self):
        return "WW %s/%s" % common.weekno_year_from_day (self.start)
    # end def __str__
# end class Week_Container

class Month_Container (Time_Container):
    def __init__ (self, day, **kw):
        year   = day.year
        month  = day.month
        nmonth = day.month + 1
        nyear  = year
        if nmonth > 12:
            nmonth = 1
            nyear = year + 1
        fmt = '%4s-%s-01'
        self.__super.__init__ \
            (Date (fmt % (year, month)), Date (fmt % (nyear, nmonth)), **kw)
    # end def __init__

    def __str__ (self):
        return self.start.pretty ("%B %Y")
    # end def __str__
# end class Month_Container

class Range_Container (Time_Container):
    """ Contains the whole selected time-range """
    def __init__ (self, *args, **kw):
        self.__super.__init__ (*args, **kw)
        self.sort_end = self.end + Interval ('1m')
    # end def __init__

    def __str__ (self):
        return "%s;%s" % (self.start.pretty (ymd), self.end.pretty (ymd))
    # end def __str__
# end class Range_Container

time_container_classes = \
    { 'day'   : Day_Container
    , 'week'  : Week_Container
    , 'month' : Month_Container
    , 'range' : Range_Container
    }

class Comparable_Container (Container, Dict_Mixin):
    sortkey = 50

    def __init__ (self, *args, **kw):
        self.__super.__init__ (*args, **kw)
    # end def __init__

    def __str__ (self):
        return self.name
    # end def __str__

    def __cmp__ (self, other):
        _ = self.i18n.gettext
        return \
            (  cmp (self.sortkey, other.sortkey) 
            or cmp (_ (self.classname), _ (other.classname))
            or cmp (self.name, other.name)
            )
    # end def __cmp__

    def __lt__ (self, other):
        _ = self.i18n.gettext
        return \
            (  self.sortkey < other.sortkey
            or self.sortkey == other.sortkey
               and _ (self.classname) < _ (other.classname)
            or self.sortkey == other.sortkey
               and _ (self.classname) == _ (other.classname)
               and self.name < other.name
            )
    # end def __lt__

# end class Comparable_Container

class Sum_Container (Comparable_Container):
    sortkey = 100
    def __init__ (self, name = "Sum", visible = True, *args, **kw):
        self.__super.__init__ (*args, **kw)
        self.name      = name
        self.visible   = visible
        self.classname = ''
    # end def __init__

    def __repr__ (self):
        classname = self.__class__.__name__
        return "%s (%s, %s, %s)" % \
            (classname, self.name, self.visible, self.__super.__repr__ ())
    # end def __repr__

    def __hash__ (self):
        return hash ((self.__class__, self.name))
    # end def __hash__
# end class Sum_Container

class WP_Container (Comparable_Container):
    def __init__ \
        (self, klass, id, visible = True, verbname = '', *args, **kw):
        self.__super.__init__ (*args, **kw)
        self.klass     = klass
        self.classname = klass.classname
        self.id        = id
        self.visible   = visible
        self.name      = klass.get (id, 'name')
        self.verbname  = verbname

        # defaults for id computation
        self.time_wp_id            = ''
        self.time_wp_no            = ''
        self.time_wp_group_id      = ''
        self.time_wp_summary_no_id = ''
        self.cost_center_id        = ''
        self.cost_center_group_id  = ''
        self.time_project_id       = ''
        self.reporting_group_id    = ''
        self.product_family_id     = ''
        self.project_type_id       = ''
        self.organisation_id       = ''

        # create i18n names
        dummy = ""'time_wp_id'
        dummy = ""'time_wp_no'
        dummy = ""'time_wp_group_id'
        dummy = ""'time_wp_summary_no_id'
        dummy = ""'cost_center_id'
        dummy = ""'cost_center_group_id'
        dummy = ""'time_project_id'
        dummy = ""'reporting_group_id'
        dummy = ""'product_family_id'
        dummy = ""'project_type_id'
        dummy = ""'organisation_id'

        # defaults for name computation
        self.organisation    = ''
        self.product_family  = ''
        self.project_type    = ''
        self.reporting_group = ''

        tp   = None
        cc   = None
        ccg  = None
        rg   = None
        pf   = None
        pt   = None
        org  = None
        wpsn = None
        if klass.classname == 'time_wp':
            self.sortkey = 30
            wp = klass.getnode (id)
            tp = klass.db.time_project.getnode (wp.project)
            p  = tp.name
            self.name  = '/'.join ((p, self.name))
            self.time_wp_id = ('time_wp', id)
            self.time_wp_no = ('time_wp', id)
            if wp.time_wp_summary_no:
                wpsn = klass.db.time_wp_summary_no.getnode \
                    (wp.time_wp_summary_no)
        elif klass.classname == 'time_project':
            tp = klass.getnode (id)
        elif klass.classname == 'time_wp_group':
            wpg = klass.getnode (id)
            self.time_wp_group    = ('time_wp_group', wpg.name)
            self.time_wp_group_id = ('time_wp_group', id)
        elif klass.classname == 'time_wp_summary_no':
            wpsn = klass.getnode (id)
        elif klass.classname == 'cost_center':
            cc  = klass.getnode (id)
        elif klass.classname == 'cost_center_group':
            ccg = klass.getnode (id)
        elif klass.classname == 'reporting_group':
            rg  = [klass.getnode (id)]
        elif klass.classname == 'product_family':
            pf  = [klass.getnode (id)]
        elif klass.classname == 'project_type':
            pt  = klass.getnode (id)
        if tp:
            self.time_project_id = ('time_project', tp.id)
            if tp.cost_center:
                cc  = klass.db.cost_center.getnode     (tp.cost_center)
            if tp.project_type:
                pt  = klass.db.project_type.getnode    (tp.project_type)
            if tp.organisation:
                org = klass.db.organisation.getnode    (tp.organisation)
            rg = [klass.db.reporting_group.getnode (x)
                  for x in tp.reporting_group
                 ]
            pf = [klass.db.product_family.getnode (x)
                  for x in tp.product_family
                 ]
        if cc:
            self.cost_center_id = ('cost_center', cc.id)
            ccg = klass.db.cost_center_group.getnode (cc.cost_center_group)
        if ccg:
            self.cost_center_group_id  = ('cost_center_group', ccg.id)
        if rg:
            self.reporting_group_id    = \
                ('reporting_group', list (sorted (x.id   for x in rg)))
            self.reporting_group       = \
                ('reporting_group', list (sorted (x.name for x in rg)))
        if pf:
            self.product_family_id     = \
                ('product_family', list (sorted (x.id   for x in pf)))
            self.product_family        = \
                ('product_family', list (sorted (x.name for x in pf)))
        if pt:
            self.project_type_id       = ('project_type', pt.id)
            self.project_type          = ('project_type', pt.name)
        if org:
            self.organisation_id       = ('organisation', org.id)
            self.organisation          = ('organisation', org.name)
        if wpsn:
            self.time_wp_summary_no    = ('time_wp_summary_no', wpsn.name)
            self.time_wp_summary_no_id = ('time_wp_summary_no', wpsn.id)
    # end def __init__
    
    def __repr__ (self):
        name = self.__class__.__name__
        return "%s (%s, %s, %s)" % \
            (name, self.classname, self.id, self.__super.__repr__ ())
    # end def __repr__

    def __str__ (self):
        _ = self.i18n.gettext
        if not self.verbname:
            return "%s %s" % (_ (self.classname), self.name)
        return "%s %s %s" % (_ (self.classname), self.name, self.verbname)
    # end def __str__

    def as_html (self):
        _ = self.i18n.gettext
        return "%s %s %s" % \
            ( escape (_ (self.classname)).replace (' ', '&nbsp;')
            , escape (self.name).replace          (' ', '&nbsp;')
            , escape (self.verbname).replace      (' ', '&nbsp;')
            )

    def __hash__ (self):
        return hash ((self.__class__, self.classname, self.id))
    # end def __hash__

    def __getattr__ (self, name):
        if name.endswith ('.id'):
            return getattr (self, name.replace ('.', '_'))
        return self.__super.__getattr__ (name)
    # end def __getattr__

# end class WP_Container

class DR_Container (Comparable_Container):

    def __init__ \
        (self, klass, id, visible = True, *args, **kw):
        self.__super.__init__ (*args, **kw)
        self.klass     = klass
        self.classname = klass.classname
        self.id        = id
        self.visible   = visible
        self.name      = klass.get (id, 'name')
    # end def __init__

    def __hash__ (self):
        return hash ((self.__class__, self.classname, self.id))
    # end def __hash__

# end class DR_Container

class _Report (autosuper):

    def html_item (self, item, **kw):
        if not item and not isinstance (item, dict) and not item == 0:
            return "   <td/>"
        if isinstance (item, PM_Value):
            if item.missing and not item:
                return ('  <td class="missing"/>')
            return \
                ('  <td %sstyle="text-align:right;">%2.02f</td>'
                % (['class="missing" ', ''][not item.missing], item)
                )
        if isinstance (item, type (0.0)) or isinstance (item, type (0)):
            return ('  <td style="text-align:right;">%2.02f</td>' % item)
        if isinstance (item, str):
            return ('  <td>%s</td>' % item)
        if isinstance (item, list):
            return '   <td>%s</td>' % ', '.join (i.as_html () for i in item)
        return ('  <td>%s</td>' % item.as_html ())
    # end def html_item

    def html_header_item (self, item, **kw):
        cls = kw.get ('cls', '')
        if cls:
            cls = ' class="%s"' % cls
        cls = cls or ''
        if hasattr (item, 'as_html'):
            s = item.as_html ()
        else:
            s = str (item)
        return ('  <th%s>%s</th>' % (cls, s))
    # end def html_header_item

    def html_line (self, items):
        items.insert (0, " <tr>")
        items.append (" </tr>")
        self.html_output.extend (items)
    # end def html_line

    def csv_item (self, item, **kw):
        if not item and not isinstance (item, dict) and not item == 0:
            return ''
        if isinstance (item, PM_Value):
            if item.missing and not item:
                return "-"
            return '%2.02f' % item
        if isinstance (item, type (0.0)):
            return '%2.02f' % item
        if isinstance (item, list):
            return '/'.join (str (i) for i in item)
        return str (item)
    # end def csv_item

    def csv_line (self, items):
        self.csvwriter.writerow (items)
    # end def csv_line

    def as_html (self):
        s = self.html_output = ['']
        s.append ('<table class="list" border="1">')
        self.html_line (self.header_line (self.html_header_item))
        self._output   (self.html_line, self.html_item)
        s.append ("</table>")
        return '\n'.join (s)
    # end def as_html

    def as_csv (self):
        io = StringIO ()
        d  = ','
        if 'csv_delimiter' in self.db.user.properties:
            d = self.db.user.get (self.uid, 'csv_delimiter') or d
        self.csvwriter = csv.writer (io, dialect = 'excel', delimiter = d)
        self.csv_line (self.header_line (self.csv_item))
        self._output  (self.csv_line, self.csv_item)
        return io.getvalue ()
    # end def as_csv

    def linked_type (self, id, classname, propname):
        try:
            item = self.htmldb [classname].getItem (id)
            prop = getattr (item, propname)
            return self.utils.ExtProperty (self.utils, prop, item = item)
        except (AttributeError, TypeError):
            return self.db.getclass (classname).get (id, propname)
    # end def linked_type

    def linked_user (self, uid):
        return self.linked_type (uid, 'user', 'username')
    # end def linked_user

    def linked_ctype (self, ctype):
        return self.linked_type (ctype, 'contract_type', 'name')
    # end def linked_ctype

    def supi_clearance (self, user):
        supi = user
        while supi:
            clr  = common.tt_clearance_by (self.db, supi)
            if self.uid in clr:
                return True
            supi = self.db.user.get (supi, 'supervisor')
    # end def supi_clearance

# end class _Report

class Summary_Report (_Report):
    """ Perform computations for a summary report.
        A note on permissions: Permission to vie a time_record for the
        summary report is granted if the user has access to either the
        time_wp or the daily_record. Special check functions in
        sum_common are used for this. For details see the "is_own"
        property of Extended_WP, Extended_Daily_Record and
        Extended_Time_Record.
    """
    def __init__ (self, db, request, utils, is_csv = False):
        self.htmldb     = db
        self.utils      = utils
        try:
            db = db._db
        except AttributeError:
            pass
        self.db         = db
        _               = db.i18n.gettext
        self.uid        = db.getuid ()
        filterspec      = request.filterspec
        sort_by         = request.sort
        group_by        = request.group
        columns         = request.columns
        now             = Date ('.')
        assert (request.classname == 'summary_report')
        wp_containers   = []
        if not columns:
            columns     = list (db.summary_report.getprops ())
        self.columns    = dict ((c, True) for c in columns)
        status          = filterspec.get \
            ('status', db.daily_record_status.getnodeids ())
        timestamp       = time.time ()
        show_empty      = filterspec.get ('show_empty',     'no')
        show_all_users  = filterspec.get ('show_all_users', 'no')
        show_missing    = filterspec.get ('show_missing',   'no')
        op_project      = filterspec.get ('op_project', None)
        op_project      = {'yes' : True, 'no' : False}.get (op_project, None)
        self.show_empty = show_empty == 'yes'
        show_all_users  = self.show_all_users = show_all_users == 'yes'
        show_missing    = show_missing == 'yes' and not is_csv
        travel_act      = db.time_activity.filter (None, {'travel' : True})
        travel_act      = dict ((a, 1) for a in travel_act)
        self.show_plan  = 'planned_effort' in self.columns

        db.log_info ("summary_report: time: %s" % timestamp)
        db.log_info ("summary_report: filterspec: %s" % filterspec)
        db.log_info ("summary_report: columns: %s, plan: %s"
            % (self.columns, self.show_plan))
        start, end  = common.date_range (db, filterspec)
        users       = filterspec.get ('user', [])
        sv          = dict ((i, 1) for i in filterspec.get ('supervisor', []))
        svu         = []
        # Summary report can only be seen by role Summary-Report now
        if not common.user_has_role (self.db, self.uid, 'Summary-Report'):
            self.wps             = {}
            self.usernames       = []
            self.start           = start
            self.end             = end
            self.time_containers = {}
            self.wp_containers   = []
            self.dr_containers   = []
            return

        if sv:
            svu = db.user.find (supervisor = sv)
        users         = list (set (users).union (svu))
        olo_or_dept   = False
        drecs         = {}
        org_dep_usr   = {}
        dr_containers = []
        for cl in 'org_location', 'sap_cc':
            spec = dict ((s, 1) for s in filterspec.get (cl, []))
            if spec:
                olo_or_dept = True
                udrs        = []
                by_id       = {}
                for id in spec:
                    c = DR_Container \
                        ( db.classes [cl]
                        , id
                        , cl in self.columns
                        , i18n = db.i18n
                        )
                    dr_containers.append (c)
                    by_id [id] = c
                    
                for i in db.user_dynamic.find (** {cl : spec}):
                    ud = db.user_dynamic.getnode (i)
                    if  (   ud.valid_from <= end
                        and (not ud.valid_to or ud.valid_to > start)
                        ):
                        udrs.append (ud)
                        org_dep_usr [ud.user] = 1
                for ud in udrs:
                    udstart = max (ud.valid_from, start)
                    if ud.valid_to:
                        udend = min (ud.valid_to - Interval ('1d'), end)
                    else:
                        udend = end
                    assert (udstart <= udend)
                    drs = db.daily_record.filter \
                        ( None, dict 
                            ( user   = ud.user
                            , date   = common.pretty_range (udstart, udend)
                            , status = status
                            )
                        )
                    edr = Extended_Daily_Record
                    drs = [edr (db, d) for d in drs]
                    by_id [getattr (ud, cl)].update (dict.fromkeys (drs))
                    drecs.update (dict ((d.id, d) for d in drs))

        db.log_info ("summary_report: after deps: %s" 
            % (time.time () - timestamp))
        if not users and not olo_or_dept:
            users   = db.user.getnodeids () # also invalid users!
        db.log_info ("summary_report: users: %s, %s-%s, status: %s"
            % (users, start, end, status))
        dr          = []
        if users:
            dr = db.daily_record.filter \
                ( None, dict 
                    ( user   = users
                    , date   = common.pretty_range (start, end)
                    , status = status
                    )
                )
        db.log_info ("summary_report: n_dr: %s (%s)"
            % (len (dr), time.time () - timestamp))
        dr = dict ((d, Extended_Daily_Record (db, d)) for d in dr)
        db.log_info ("summary_report: after users: %s"
            % (time.time () - timestamp))
        dr.update (drecs)
        db.log_info ("summary_report: after dr.update: %s"
            % (time.time () - timestamp))
        self.dr_by_user_date = dict \
            (((str (dr [k].username), dr [k].date.pretty (ymd)), dr [k])
             for k in dr
            )
        db.log_info ("summary_report: after dr_dat_usr: %s"
            % (time.time () - timestamp))

        wp          = dict ((w, 1) for w in filterspec.get ('time_wp', []))
        db.log_info ("summary_report: native wp: %s (%s)"
            % (len (wp), time.time () - timestamp))

        by_project_attr = []
        pts         = filterspec.get ('project_type',    [])
        for pt in pts:
            prj = db.time_project.filter (None, dict (project_type = pt))
            if not prj:
                continue
            by_project_attr.extend (prj)
            pwps = db.time_wp.find (project = prj)
            if not pwps:
                continue
            if pt != '-1':
                wp_containers.append \
                    ( WP_Container
                        ( db.project_type, pt
                        , 'project_type' in self.columns
                          or 'project_type.id' in self.columns
                        , ''
                        , [ (x, 1) for x in pwps ]
                        , i18n = db.i18n
                        )
                    )
            wp.update ((x, 1) for x in pwps)
        rgs         = filterspec.get ('reporting_group',    [])
        for rg in rgs:
            prj = db.time_project.filter (None, dict (reporting_group = rg))
            if not prj:
                continue
            by_project_attr.extend (prj)
            pwps = db.time_wp.find (project = prj)
            if not pwps:
                continue
            if rg != '-1':
                wp_containers.append \
                    ( WP_Container
                        ( db.reporting_group, rg
                        , 'reporting_group' in self.columns
                          or 'reporting_group.id' in self.columns
                        , ''
                        , [ (x, 1) for x in pwps ]
                        , i18n = db.i18n
                        )
                    )
            wp.update ((x, 1) for x in pwps)
        pfs         = filterspec.get ('product_family',     [])
        for pf in pfs:
            prj = db.time_project.filter (None, dict (product_family = pf))
            if not prj:
                continue
            by_project_attr.extend (prj)
            pwps = db.time_wp.find (project = prj)
            if not pwps:
                continue
            if pf != '-1':
                wp_containers.append \
                    ( WP_Container
                        ( db.product_family, pf
                        , 'product_family' in self.columns
                          or 'product_family.id' in self.columns
                        , ''
                        , [ (x, 1) for x in pwps ]
                        , i18n = db.i18n
                        )
                    )
            wp.update ((x, 1) for x in pwps)
        wpsns       = filterspec.get ('time_wp_summary_no', [])
        for wpsn in wpsns:
            wps = db.time_wp.filter (None, dict (time_wp_summary_no = wpsn))
            if not wps:
                continue
            if wpsn != '-1':
                wp_containers.append \
                    ( WP_Container
                        ( db.time_wp_summary_no, wpsn
                        , 'time_wp_summary_no' in self.columns
                        , ''
                        , [ (x, 1) for x in wps ]
                        , i18n = db.i18n
                        )
                    )
            wp.update ((x, 1) for x in wps)
        wpgs        = filterspec.get ('time_wp_group',     [])
        for wpg in wpgs:
            wp_containers.append \
                ( WP_Container
                    ( db.time_wp_group, wpg
                    , 'time_wp_group' in self.columns
                    , ''
                    , [(w, 1) for w in db.time_wp_group.get (wpg, 'wps')]
                    , i18n = db.i18n
                    )
                )
            wp.update (wp_containers [-1])
        db.log_info ("summary_report: wpgs: %s (%s)"
            % (len (wp), time.time () - timestamp))
        selected_by_op_project = []
        if op_project is not None:
            selected_by_op_project = db.time_project.filter \
                (None, dict (op_project = op_project))
        projects    = filterspec.get ('time_project',      [])
        db.log_info ("summary_report: projects: %s" % projects)
        for p in projects + selected_by_op_project + by_project_attr:
            pwps = db.time_wp.find (project = p)
            db.log_info ("summary_report: project: %s wp: %s" % (p, pwps))
            wp_containers.append \
                ( WP_Container
                    ( db.time_project, p
                    , 'time_project' in self.columns
                    , ''
                    , [(w, 1) for w in pwps]
                    , i18n = db.i18n
                    )
                )
            db.log_info ("summary_report: wpc: %s" % wp_containers [-1])
            wp.update (wp_containers [-1])
        db.log_info ("summary_report: after projects: wps: %s (%s)"
            % (len (wp), time.time () - timestamp))
        ccs         = filterspec.get ('cost_center',       [])
        for cc in ccs:
            wp_containers.append \
                ( WP_Container
                    ( db.cost_center, cc
                    , 'cost_center' in self.columns
                    , ''
                    , [(w, 1) for w in db.time_wp.find (cost_center = cc)]
                    , i18n = db.i18n
                    )
                )
            wp.update (wp_containers [-1])
        db.log_info ("summary_report: ccs: %s (%s)"
            % (len (wp), time.time () - timestamp))
        ccgs        = filterspec.get ('cost_center_group', [])
        for ccg in ccgs:
            ccs     = db.cost_center.find (cost_center_group = ccg)
            ccs     = dict ((c, 1) for c in ccs)
            wp_containers.append \
                ( WP_Container 
                    ( db.cost_center_group, ccg
                    , 'cost_center_group' in self.columns
                    , i18n = db.i18n
                    )
                )
            for cc in ccs:
                wps = dict ((w,1) for w in db.time_wp.find (cost_center = cc))
                wp_containers [-1].update (wps)
            wp.update (wp_containers [-1])
        db.log_info ("summary_report: ccgs: %s (%s)"
            % (len (wp), time.time () - timestamp))
        if  (    not wp
            and 'time_wp'            not in filterspec
            and 'time_wp_group'      not in filterspec
            and 'time_project'       not in filterspec
            and 'cost_center'        not in filterspec
            and 'cost_center_group'  not in filterspec
            and 'product_family'     not in filterspec
            and 'project_type'       not in filterspec
            and 'reporting_group'    not in filterspec
            ):
            wp = dict ((w, 1) for w in db.time_wp.getnodeids ())
        db.log_info ("summary_report: wp-default: n_wp: %s (%s)"
            % (len (wp), time.time () - timestamp))
        work_pkg    = dict ((w, Extended_WP (db, w)) for w in wp)
        db.log_info ("summary_report: ext wp (%s)" % (time.time () - timestamp))
        time_recs   = []
        # 276 sec: (4.6 min) (for Decos: ~ 250 sec)
        if dr and wp:
            time_recs = []
            for k in dr:
                d = dr [k]
                for t in d.time_record:
                    if db.time_record.get (t, 'wp') in work_pkg:
                        tr = Extended_Time_Record (db, t, dr, work_pkg)
                        time_recs.append (tr)
        db.log_info ("summary_report: ext time_recs: %s (%s)"
            % (len (time_recs), time.time () - timestamp))
        time_recs   = [t for t in time_recs if t.is_own]
        db.log_info ("summary_report: own time_recs: %s (%s)"
            % (len (time_recs), time.time () - timestamp))
        time_recs.sort ()
        db.log_info ("summary_report: srt time_recs: %s (%s)"
            % (len (time_recs), time.time () - timestamp))
        if self.show_empty:
            usrs         = users + list (org_dep_usr)
            uids_by_name = dict ((db.user.get (u, 'username'), u) for u in usrs)
            # filter out users without a dyn user record in our date range
            # Except for those who have booked in the range
            if not self.show_all_users:
                users = {}
                for u in uids_by_name:
                    uid = uids_by_name [u]
                    d   = start
                    while d <= end:
                        if user_dynamic.get_user_dynamic (db, uid, d):
                            users [u] = uid
                            break
                        d = d + Interval ('1d')
                for tr in time_recs:
                    u = tr.username
                    users [u] = uids_by_name [u]
                uids_by_name = users
            usernames    = list (uids_by_name)
        else:
            usernames    = list (set (tr.username for tr in time_recs))
            uids_by_name = dict ((u, db.user.lookup (u)) for u in usernames)
        db.log_info ("summary_report:          usernames (%s)"
            % (time.time () - timestamp))

        db.log_info ("summary_report: filtered usernames (%s)"
            % (time.time () - timestamp))
        usernames = list (sorted (usernames))
        db.log_info ("summary_report: sorted   usernames (%s)"
            % (time.time () - timestamp))
        
        # append only wps where somebody actually booked on
        wps         = dict ((tr.wp.id, 1) for tr in time_recs)
        for w in wps:
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
                    , i18n = db.i18n
                    )
                )
        db.log_info ("summary_report: filtered wps (%s)"
            % (time.time () - timestamp))
        if not projects + selected_by_op_project:
            tprojects   = dict ((tr.wp.project, 1) for tr in time_recs)
            for p in tprojects:
                wp_containers.append \
                    ( WP_Container
                        ( db.time_project, p
                        , 'time_project' in self.columns
                        , ''
                        , [(w, 1) for w in db.time_wp.find (project = p)]
                        , i18n = db.i18n
                        )
                    )
                wp.update (wp_containers [-1])
        wp_containers.append \
            ( Sum_Container
                ( _ ('Sum')
                , 'summary' in self.columns
                , wps
                , i18n = db.i18n
                )
            )

        # Build time containers
        rep_types  = filterspec.get \
            ('summary_type', [db.summary_type.lookup ('range')])
        rep_types  = [db.summary_type.get (i, 'name') for i in rep_types]
        time_containers = dict ((t, []) for t in rep_types)
        d = start
        while d <= end:
            for t in time_containers:
                cont = time_containers [t]
                if not cont or cont [-1].end <= d:
                    ccls = time_container_classes [t]
                    if t == 'range':
                        cont.append (ccls (start, end, i18n = db.i18n))
                    else:
                        cont.append (ccls (d, i18n = db.i18n))
            d = d + Interval ('1d')
        db.log_info ("summary_report: time containers (%s)"
            % (time.time () - timestamp))
        wp_containers = [w for w in wp_containers if w.visible]
        wp_containers.sort ()
        dr_containers = [c for c in dr_containers if c.visible]
        dr_containers.sort ()
        db.log_info ("summary_report: sorted containers (%s)"
            % (time.time () - timestamp))
        # invert wp_containers
        containers_by_wp = {}
        for wc in wp_containers:
            for w in wc:
                if w in containers_by_wp:
                    containers_by_wp [w].append (wc)
                else:
                    containers_by_wp [w]      = [wc]
        # invert dr_containers:
        containers_by_dr = {}
        for c in dr_containers:
            for dr in c:
                if dr.id in containers_by_dr:
                    containers_by_dr [dr.id].append (c)
                else:
                    containers_by_dr [dr.id]      = [c]
        db.log_info ("summary_report: inverted containers (%s)"
            % (time.time () - timestamp))
        tc_pointers = dict ((i, 0) for i in time_containers)
        db.log_info ("summary_report: after tc_pointers (%s)"
            % (time.time () - timestamp))

        d        = start
        tidx     = 0
        invalid  = PM_Value (0, 1)
        # wp may not be viewable due to permissions
        valid_wp = \
            [work_pkg [k] for k in work_pkg
             if work_pkg [k].id in containers_by_wp
            ]
        while d <= end:
            if show_missing:
                no_daily_record = \
                    [u for u in usernames
                     if (   (u, d.pretty (ymd)) not in self.dr_by_user_date
                        and (  self.show_all_users
                            or user_dynamic.get_user_dynamic
                                (db, uids_by_name [u], d)
                            )
                        )
                    ]
                db.log_info ("summary_report: user dr_len: %s (%s)"
                    % (len (no_daily_record), time.time () - timestamp))
            for tcp in tc_pointers:
                while (d >= time_containers [tcp][tc_pointers [tcp]].sort_end):
                    tc_pointers [tcp] += 1
                tc = time_containers [tcp][tc_pointers [tcp]]
                if self.show_plan or show_missing:
                    for w in valid_wp:
                        for wc in containers_by_wp [w.id]:
                            if self.show_plan:
                                wc.add_plan (tc, w.effort (d))
                                tc.add_plan (wc, w.effort (d))
                            if show_missing:
                                for u in no_daily_record:
                                    wc.add_user_sum (tc, u, invalid)
                                    tc.add_user_sum (wc, u, invalid)
                db.log_info ("summary_report: plan (%s)"
                    % (time.time () - timestamp))
            while tidx < len (time_recs) and time_recs [tidx].date == d:
                t  = time_recs [tidx]
                for tcp in tc_pointers:
                    tc = time_containers [tcp][tc_pointers [tcp]]
                    for wpc in containers_by_wp.get (t.wp.id, []):
                        tc. add_sum (wpc, t)
                        wpc.add_sum (tc,  t)
                        for drc in containers_by_dr.get (t.dr.id, []):
                            tc. add_sum_column (wpc, drc.name, t, False)
                            wpc.add_sum_column (tc,  drc.name, t, False)
                tidx += 1
            d = d + Interval ('1d')
            db.log_info ("summary_report: 1d (%s)" % (time.time () - timestamp))
        db.log_info ("summary_report: SUMs built (%s)"
            % (time.time () - timestamp))
        self.wps             = wps
        self.usernames       = usernames
        self.start           = start
        self.end             = end
        self.time_containers = time_containers
        self.wp_containers   = wp_containers
        self.dr_containers   = dr_containers
    # end def __init__

    id_attrs = \
        [ '.'.join ((x, 'id')) for x in
            ( 'time_wp'
            , 'time_project'
            , 'time_wp_group'
            , 'cost_center'
            , 'cost_center_group'
            , 'organisation'
            , 'product_family'
            , 'project_type'
            , 'reporting_group'
            , 'time_wp_summary_no'
            )
        ]

    name_attrs = \
        [ 'organisation'
        , 'product_family'
        , 'project_type'
        , 'reporting_group'
        ]

    def header_line (self, formatter):
        _ = self.db.i18n.gettext
        line = []
        line.append (formatter (_ ('Container')))
        for k in self.name_attrs:
            if k in self.columns:
                line.append (formatter (_ (k)))
        for k in self.id_attrs:
            if k in self.columns:
                line.append (formatter (_ (k)))
        if 'time_wp.wp_no' in self.columns:
            line.append (formatter (_ ('time_wp.wp_no')))
        line.append (formatter (_ ('time')))
        if 'user' in self.columns:
            for u in self.usernames:
                line.append (formatter (u))
        for dr in self.dr_containers:
            line.append (formatter (_ (dr.name)))
        line.append (formatter (_ ('Sum')))
        if self.show_plan:
            for i in 'planned_effort', '%', 'remaining':
                line.append (formatter (_ (i)))
        return line
    # end def header_line

    def _output_line (self, wpc, typ, idx, formatter):
        line = []
        tc   = self.time_containers [typ][idx]
        line.append (formatter (wpc))
        for k in self.name_attrs:
            if k in self.columns:
                col = getattr (wpc, k, None)
                if col:
                    try:
                        cls = getattr (self.htmldb, col [0])
                        if isinstance (col [1], list):
                            cols = []
                            for i in col [1]:
                                itm = cls.getItem (i)
                                c = self.utils.ExtProperty \
                                    ( self.utils
                                    , itm.name
                                    , item = itm
                                    )
                                cols.append (c)
                            col = cols
                        else:
                            itm = cls.getItem (col [1])
                            col = self.utils.ExtProperty \
                                ( self.utils
                                , itm.name
                                , item = itm
                                )
                    except AttributeError:
                        col = col [1]
                line.append (formatter (col))
        for k in self.id_attrs:
            if k in self.columns:
                col = getattr (wpc, k)
                if col:
                    try:
                        cls = getattr (self.htmldb, col [0])
                        if isinstance (col [1], list):
                            cols = []
                            for i in col [1]:
                                itm = cls.getItem (i)
                                c   = self.utils.ExtProperty \
                                    ( self.utils
                                    , itm.name
                                    , item = itm
                                    , displayprop = 'id'
                                    )
                                cols.append (c)
                            col = cols
                        else:
                            itm = cls.getItem (col [1])
                            col = self.utils.ExtProperty \
                                ( self.utils
                                , itm.name
                                , item = itm
                                , displayprop = 'id'
                                )
                    except AttributeError:
                        col = col [1]
                line.append (formatter (col))
        if 'time_wp.wp_no' in self.columns:
            col = getattr (wpc, 'time_wp_no', None)
            if col:
                try:
                    cls = getattr (self.htmldb, col [0])
                    itm = cls.getItem (col [1])
                    col = self.utils.ExtProperty \
                        ( self.utils
                        , itm.wp_no
                        , item = itm
                        )
                except AttributeError:
                    col = ''
            line.append (formatter (col))
        line.append (formatter (tc))
        if 'user' in self.columns:
            for u in self.usernames:
                line.append (formatter (tc.get_sum (wpc, u, '')))
        for dr in self.dr_containers:
            line.append (formatter (tc.get_sum (wpc, dr.name, '')))
        sum = tc.get_sum (wpc, default = PM_Value (0.0))
        line.append (formatter (sum))
        if self.show_plan:
            plan = tc.get_plan (wpc)
            line.append (formatter (plan))
            if plan:
                line.append (formatter (sum * 100. / plan))
                line.append (formatter (plan - sum))
            else:
                missing = plan is None or plan.missing
                line.append (formatter (PM_Value (0, missing)))
                line.append (formatter (PM_Value (0, missing)))
        return line
    # end def _output_line

    def _output (self, line_formatter, item_formatter):
        start = self.start + Interval ('1d')
        if not self.time_containers:
            end = self.end
        else:
            end   = max \
                ([self.time_containers [i][-1].sort_end
                  for i in self.time_containers
                ])
        for wpc in self.wp_containers:
            tc_pointers = dict \
                ([(i, 0) for i in self.time_containers])
            d = start
            containertypes = 'day', 'week', 'month', 'range' # order matters.
            while d <= end:
                for tcp in [i for i in containertypes if i in tc_pointers]:
                    try:
                        tc = self.time_containers [tcp][tc_pointers [tcp]]
                    except IndexError:
                        continue
                    if d >= tc.sort_end:
                        if  (   wpc.visible
                            and (self.show_empty or tc.get_sum (wpc))
                            ):
                            line_formatter \
                                ( self._output_line
                                  (wpc, tcp, tc_pointers [tcp], item_formatter)
                                )
                        tc_pointers [tcp] += 1
                d = d + Interval ('1d')
    # end def _output
# end class Summary_Report

class HTML_List:

    def __init__ (self, delimiter = ' + '):
        self.items     = []
        self.delimiter = delimiter
    # end def __init__

    def append (self, item):
        self.items.append (item)
    # end def append

    def as_html (self):
        return self.delimiter.join (i.as_html () for i in self.items)
    # end def as_html

    def __repr__ (self):
        return self.delimiter.join (str (i) for i in self.items)
    # end def __repr__

# end class HTML_List

class HTML_Link:

    def __init__ (self, value, href):
        self.value = value
        self.href  = href
    # end def __init__

    def as_html (self):
        return '<a href="%(href)s">%(value)s</a>' % self.__dict__
    # end def as_html

    def __repr__ (self):
        return str (self.value)
    # end def __repr__
    __str__ = __repr__

# end class HTML_Link

class Staff_Report (_Report):
    ''"Staff Report" # for translation in web-interface
    fields = \
        ( ""'balance_start'
        , ""'actual_open'
        , ""'actual_submitted'
        , ""'actual_accepted'
        , ""'actual_all'
        , ""'required'
        , ""'supp_hours_2'
        , ""'supp_weekly_hours'
        , ""'overtime_correction'
        , ""'balance_end'
        , ""'overtime_period'
        )
    #####     field                    allow for all (HR only if unset)
    period_fields = \
        ( (""'achieved_supplementary', 1)
        , (""'supp_per_period',        1)
        , (""'additional_hours',       1)
        )

    def __init__ (self, db, request, utils, is_csv = False):
        timestamp    = time.time ()
        self.htmldb  = db
        try:
            db = db._db
        except AttributeError:
            pass
        self.db      = db
        self.uid     = db.getuid ()
        db.log_info  ("staff_report: %s" % timestamp)
        stati        = (db.daily_record_status.getnode (i)
                        for i in db.daily_record_status.getnodeids ()
                       )
        self.stati   = dict ((i.id, i.name) for i in stati)
        # leave is also uneditable.
        for id, n in self.stati.items ():
            if n == 'leave':
                self.stati [id] = 'accepted'
        self.request = request
        self.utils   = utils
        filterspec   = request.filterspec
        status       = filterspec.get \
            ('status', db.daily_record_status.getnodeids ())
        start, end   = common.date_range (db, filterspec)
        self.start   = start
        self.end     = end
        st           = filterspec.get \
            ('summary_type', [db.summary_type.lookup ('range')])
        sum_types    = dict ((db.summary_type.get (i, 'name'), 1) for i in st)
        # Backwards compatible, all users having a valid dyn user record
        # and *end* of reporting period, so we specify 'end' twice here:
        users        = sum_common.get_users (db, filterspec, end, end)
        all_in = filterspec.get ('all_in')
        if all_in is not None:
            all_in = all_in == 'yes'
        for u in list (users):
            dyn = user_dynamic.get_user_dynamic (db, u, end)
            if not dyn:
                dyn = user_dynamic.last_user_dynamic (db, u, end)
                # Check if we have a valid dyn during reporting period
                if  (   not dyn
                    or  not dyn.valid_to
                    or (   not (start <= dyn.valid_from     <= end)
                       and not (start <= dyn.valid_to - day <= end)
                       )
                    ):
                    dyn = None
            if  (  not dyn
                or all_in is not None and all_in != bool (dyn.all_in)
                or not self.staff_permission_ok (u, dyn)
                ):
                del users [u]
        self.users = sorted \
            ( list (users)
            , key = lambda x : db.user.get (x, 'username')
            )
        db.log_info  ("staff_report: users: %s" % (time.time () - timestamp))
        self.values      = values = {}
        self.need_period = False
        period_objects   = dict \
            (week = common.period_week, month = common.period_month)
        for u in self.users:
            dyn        = user_dynamic.get_user_dynamic (db, u, end)
            values [u] = []
            for period in 'week', 'month', 'range':
                if period not in sum_types:
                    continue
                ccls = time_container_classes [period]
                if period == 'range':
                    container = ccls (start, end, i18n = db.i18n)
                    values [u].append   (container)
                    self.fill_container (container, u, dyn, start, end)
                else:
                    date = start
                    while date <= end:
                        eop = common.end_of_period \
                            (date, period_objects [period])
                        if eop > end:
                            eop = end
                        container = ccls (date, i18n = db.i18n)
                        values [u].append   (container)
                        self.fill_container (container, u, dyn, date, eop)
                        date = eop + day
                db.log_info \
                    ( "staff_report: %s/%s: %s"
                    % (period, u, time.time () - timestamp)
                    )
        db.commit () # commit cached daily_record values
    # end def __init__

    def fill_container (self, container, user, dyn, start, end):
        db      = self.db
        u       = user
        otp     = user_dynamic.overtime_periods (db, user, start, end)
        periods = [p [2] for p in otp]
        ov = db.overtime_correction.filter \
            (None, dict (user = u, date = common.pretty_range (start, end)))
        try:
            ovs = HTML_List ()
            for x in ov:
                item  = self.htmldb.overtime_correction.getItem (x)
                value = item.value
                ep    = self.utils.ExtProperty
                ovs.append \
                    ( ep
                        ( self.utils, value
                        , item         = item
                        , is_labelprop = True
                        )
                    )
            container ['overtime_correction'] = ovs
        except AttributeError:
            container ['overtime_correction'] = ' + '.join \
                (str (db.overtime_correction.get (i, 'value')) for i in ov)
        container ['overtime_period']        = \
            ', '.join (p.name for p in periods)
        container ['balance_start']          = 0.0
        container ['balance_end']            = 0.0
        container ['supp_per_period']        = ''
        container ['actual_all']             = 0
        container ['actual_open']            = 0
        container ['actual_submitted']       = 0
        container ['actual_accepted']        = 0
        container ['required']               = 0.0
        container ['supp_hours_2']           = 0
        container ['supp_weekly_hours']      = 0.0
        container ['additional_hours']       = 0
        container ['achieved_supplementary'] = ''
        effective_overtime = []

        bal       = user_dynamic.compute_balance (db, u, start - day, True) [0]
        container ['balance_start'] += bal
        #db.commit () # immediately commit cached tr_duration if changed
        bal, asup = user_dynamic.compute_balance (db, u, end,         True)
        container ['balance_end']   += bal
        container ['achieved_supplementary'] = asup
        #db.commit () # immediately commit cached tr_duration if changed
        for s, e, period in otp:
            #print "otp:", period.name, s.pretty (ymd), e.pretty (ymd)
            if not common.period_is_weekly (period):
                self.need_period = True
                pd  = user_dynamic.Period_Data (db, user, s, e, period, 0.0)
                opp = pd.overtime_per_period
                if opp is not None:
                    effective_overtime.append ('=> %.2f' % opp)
        supp_pp = {}
        d = start
        while d <= end:
            do_perd = do_week = do_ovt = False
            dur = user_dynamic.durations (db, u, d)
            #db.commit () # immediately commit cached tr_duration if changed
            for period in periods:
                do_perd = do_perd or \
                    (   not common.period_is_weekly (period)
                    and user_dynamic.use_work_hours (db, dur.dyn, period)
                    )
                do_week = do_week or \
                    (   period.weekly
                    and user_dynamic.use_work_hours (db, dur.dyn, period)
                    )
                do_ovt  = do_ovt or period.required_overtime
            if dur.supp_per_period:
                supp_pp [str (int (dur.supp_per_period))] = True
            assert (not dur.tr_duration or dur.dr_status)
            container ['actual_all'] += dur.tr_duration
            if dur.dr_status:
                f = 'actual_' + self.stati [dur.dr_status]
                container [f] += dur.tr_duration
            wh = dur.day_work_hours * (do_week or do_perd)
            container ['required']          += wh
            if do_ovt:
                container ['supp_hours_2']  += wh + dur.required_overtime
            container ['supp_weekly_hours'] += dur.supp_weekly_hours * do_week
            container ['additional_hours']  += dur.additional_hours  * do_perd
            d = d + day
        cont = [' / '.join (supp_pp)]
        if len (effective_overtime) == 1:
            cont.append (effective_overtime [0])
        container ['supp_per_period'] = ' '.join (cont)
        # db.commit () # commit cached daily_record values
    # end def fill_container

    def staff_permission_ok (self, user, dynuser):
        if user == self.uid:
            return True
        if self.supi_clearance (user):
            return True
        if not dynamic_user_allowed_by_olo (self.db, self.uid, dynuser.id):
            return False
        if common.user_has_role (self.db, self.uid, 'HR', 'staff-report'):
            return True
        if common.user_has_role (self.db, self.uid, 'HR-Org-Location'):
            hrt = user_dynamic.hr_olo_role_for_this_user_dyn
            if hrt (self.db, self.uid, dynuser):
                return True
        return False
    # end def staff_permission_ok

    def is_allowed (self, user = None):
        """ HR is currently allowed to view everything including some
            columns hidden for others.
        """
        return common.user_has_role (self.db, self.uid, 'HR', 'HR-Org-Location')
    # end is_allowed

    def header_line (self, formatter):
        _ = self.db.i18n.gettext
        line = []
        line.append (formatter (_ ('user')))
        line.append (formatter (_ ('time')))
        for f in self.fields:
            line.append (formatter (_ (f)))
        if self.need_period:
            for f, perm in self.period_fields:
                if perm or self.is_allowed ():
                    line.append (formatter (_ (f)))
        return line
    # end def header_line

    def _output (self, line_formatter, item_formatter):
        for u in self.users:
            user = self.linked_user (u)
            for container in self.values [u]:
                line  = []
                line.append (item_formatter (user))
                line.append (item_formatter (container))
                for f in self.fields:
                    line.append (item_formatter (container [f]))
                if self.need_period:
                    for f, perm in self.period_fields:
                        if perm or self.is_allowed ():
                            line.append (item_formatter (container [f]))
                line_formatter (line)
    # end def _output

# end class Staff_Report

class Vacation_Report (_Report):
    ''"Vacation Report" # for translation in web-interface
    fields = \
        ( (""'yearly entitlement',   1)
        , (""'yearly prorated',      2)
        , (""'carry forward',        3)
        , (""'entitlement total',    4)
        , (""'approved days',        5)
        , (""'approved_submissions', 6)
        , (""'vacation corrections', 7)
        , (""'remaining vacation',   8)
        , (""'additional_submitted', 9)
        , (""'flexi_time',          10)
        , (""'flexi_sub',           11)
        , (""'flexi_max',           12)
        , (""'flexi_rem',           13)
        , (""'special_leave',       14)
        , (""'special_sub',         15)
        )
    header_classes = \
        { 'remaining vacation' : 'emphasized'
        }

    def __init__ (self, db, request, utils, is_csv = False):
        timestamp        = time.time ()
        self.htmldb      = db
        self.need_period = False
        try:
            db = db._db
        except AttributeError:
            pass
        self.db      = db
        self.uid     = db.getuid ()
        self.hv = hv = common.user_has_role \
            (self.db, self.uid, 'HR-vacation', 'Vacation-report')
        db.log_info  ("vacation_report: %s" % timestamp)
        st_accp = db.leave_status.lookup ('accepted')
        st_cnrq = db.leave_status.lookup ('cancel requested')
        st_subm = db.leave_status.lookup ('submitted')
        self.request = request
        self.utils   = utils
        filterspec   = request.filterspec
        now          = Date ('.')
        year         = now.get_tuple () [0]
        d = filterspec.get ('date')
        fields       = dict (self.fields)
        # By default show obsolete users, users might have a time-limited
        # contract, they would be confused if they can't see vacation
        # report
        self.show_obsolete = True
        if 'show_obsolete' in filterspec:
            self.show_obsolete = filterspec ['show_obsolete'] == 'yes'
        opt = \
            ( 'approved_submissions'
            , 'additional_submitted'
            , 'flexi_time'
            , 'flexi_sub'
            , 'flexi_max'
            , 'flexi_rem'
            , 'special_leave'
            , 'special_sub'
            )
        for k in opt:
            if k not in request.columns:
                del fields [k]
        self.fields  = sorted \
            (list (fields), key = lambda x : fields [x])

        if d:
            try:
                if ';' in d:
                    start, end = d.split (';')
                    if not start:
                        start = None
                    else:
                        start = Date (start)
                    if end:
                        end   = Date (end)
                    else:
                        end   = Date ('%s-12-31' % year)
                else:
                    start = end = Date (d)
            except ValueError:
                start = end = Date ('%s-12-31' % year)
        else:
            start = end = Date ('%s-12-31' % year)
        self.start       = start
        self.end         = end
        soy              = common.start_of_year (end)
        users            = sum_common.get_users (db, filterspec, soy, end)
        min_user_date    = {}
        max_user_date    = {}
        user_vc          = {}
        self.user_ctypes = {}
        for u in list (users):
            srt = [('+', 'date')]
            vcs = db.vacation_correction.filter \
                (None, dict (user = u, absolute = True), sort = srt)
            if not vcs:
                del users [u]
                continue
            ctypes = {}
            for id in vcs:
                vc = db.vacation_correction.getnode (id)
                if vc.contract_type not in ctypes:
                    ctypes [vc.contract_type] = vc
            for ctype in ctypes:
                vc = ctypes [ctype]
                if start:
                    md = min_user_date [(u, ctype)] = max (vc.date, start)
                else:
                    md = min_user_date [(u, ctype)] = vc.date
                mind = md
                if start == end:
                    mind = Date ('%s-01-01' % start.year)
                if end and min_user_date [(u, ctype)] > end:
                    continue
                dyn  = vacation.vac_get_user_dynamic (db, u, ctype, md)
                if  (  not dyn or (dyn.valid_from and dyn.valid_from > end)
                    or not self.permission_ok (u, dyn, check_olo = False)
                    ):
                    continue
                last_dyn = ldyn = dyn
                while ldyn and ldyn.valid_to and ldyn.valid_to < end:
                    ldyn = vacation.vac_next_user_dynamic (db, ldyn)
                    if ldyn:
                        last_dyn = ldyn
                if last_dyn.valid_to:
                    max_user_date [(u, ctype)] = last_dyn.valid_to
                    if last_dyn.valid_to < mind:
                        continue
                # Second permission check *with* check_olo
                if not self.permission_ok (u, last_dyn, check_olo = True):
                    continue
                user_vc [(u, ctype)] = vc
                if u not in self.user_ctypes:
                    self.user_ctypes [u] = []
                self.user_ctypes [u].append (ctype)
        self.users = sorted \
            ( list (users)
            , key = lambda x : db.user.get (x, 'username')
            )
        db.log_info ("vacation_report: users: %s" % (time.time () - timestamp))
        self.values = values = {}
        year = Interval ('1y')
        for u in self.users:
            if u not in self.user_ctypes:
                continue
            for ctype in self.user_ctypes [u]:
                vc = user_vc [(u, ctype)]
                yday, pd, carry, ltot = vacation.vacation_params \
                    (db, u, min_user_date [(u, ctype)], vc, hv)
                ld    = None
                d     = yday
                if hv:
                    d = min (d, self.end)
                if ld is None:
                    ld = pd
                # Round up to next multiple of 0.5 days
                while d and d <= end:
                    # Find latest vacation correction at or before d
                    dts = common.pretty_range (None, d)
                    srt = [('-', 'date')]
                    vcd = dict \
                        ( user          = u
                        , absolute      = True
                        , contract_type = ctype
                        , date          = dts
                        )
                    vci = db.vacation_correction.filter (None, vcd, sort = srt)
                    if vci [0] != vc.id:
                        vc = db.vacation_correction.getnode (vci [0])
                        yday, pd, carry, ltot = vacation.vacation_params \
                            (db, u, min_user_date [(u, ctype)], vc, hv)
                    rcarry = carry
                    if not hv:
                        rcarry = float (ceil (carry))
                    if (u, ctype) in max_user_date:
                        if max_user_date [(u, ctype)] <= ld:
                            break
                    fd = ld
                    if fd.year != d.year:
                        fd = fd + day
                    container = Day_Container (d, i18n = db.i18n)
                    container ['is_obsolete'] = False
                    uname = self.linked_user (u)
                    if not ctype:
                        container ['user'] = uname
                    else:
                        lct = self.linked_ctype (ctype)
                        lst = HTML_List (' / ')
                        lst.append (uname)
                        lst.append (lct)
                        container ['user'] = lst
                    dep = {}
                    dyn = vacation.vac_get_user_dynamic (db, u, ctype, d)
                    ent = {}
                    lastdyn = dyn
                    while (dyn and dyn.valid_from < d):
                        lastdyn = dyn
                        ent [dyn.vacation_yearly] = 1
                        dyn = vacation.vac_next_user_dynamic (db, dyn)
                    container ['is_obsolete'] = self.is_obsolete (dyn, d)
                    v = list (sorted (ent))
                    # Use '..' as separator to prevent excel from computing
                    # difference if exported to excel
                    if len (v) > 1:
                        container ['yearly entitlement'] = \
                            '%s .. %s' % (v [0], v [-1])
                    elif len (v) == 1:
                        container ['yearly entitlement'] = v [0]
                    else:
                        container ['yearly entitlement'] = 0.0
                    container ['carry forward'] = rcarry
                    cons = vacation.consolidated_vacation \
                        (db, u, ctype, d, to_eoy = not hv)
                    et = float (cons - ltot + carry)
                    yp = float (cons - ltot)
                    # new carry and remaining vacation
                    carry = rv = vacation.remaining_vacation \
                        (db, u, ctype, d, cons, to_eoy = not hv)
                    if not hv:
                        # ceil in Py3 will return an int if possible ugh
                        et = float (ceil (et))
                        yp = float (ceil (yp))
                        rc = float (ceil (cons))
                        rv = float (ceil (carry))
                    container ['entitlement total']  = et
                    container ['yearly prorated']    = yp
                    container ['remaining vacation'] = rv
                    val = vacation.vacation_time_sum (db, u, ctype, fd, d)
                    r   = ('HR-vacation', 'HR-leave-approval')
                    if common.user_has_role (self.db, self.uid, *r):
                        dt   = common.pretty_range (ld, d)
                        url  = ( '%sleave_submission?@template=approve_hr&'
                                 '@filter=user,first_day&@startwith=0&'
                                 '@pagesize=20&'
                               )
                        url %= db.config.TRACKER_WEB
                        url += urlencode (dict (user = u, first_day = dt))
                        container ['approved days'] = HTML_Link (val, url)
                    else:
                        container ['approved days'] = val
                    if 'additional_submitted' in self.fields:
                        container ['additional_submitted'] = \
                            vacation.vacation_submission_days \
                                (db, u, ctype, fd, d, st_subm)
                    if 'flexi_time' in self.fields:
                        container ['flexi_time'] = \
                            vacation.flexitime_submission_days \
                                (db, u, ctype, fd, d, st_accp, st_cnrq)
                    if 'flexi_sub' in self.fields:
                        container ['flexi_sub'] = \
                            vacation.flexitime_submission_days \
                                (db, u, ctype, fd, d, st_subm)
                    if 'flexi_max' in self.fields:
                        container ['flexi_max'] = \
                            vacation.flexi_alliquot (db, u, fd, ctype)
                    if 'flexi_rem' in self.fields:
                        container ['flexi_rem'] = \
                            vacation.flexi_remain (db, u, fd, ctype) or ''
                    if 'special_leave' in self.fields:
                        container ['special_leave'] = \
                            vacation.special_submission_days \
                                (db, u, ctype, fd, d, st_accp, st_cnrq)
                    if 'special_sub' in self.fields:
                        container ['special_sub'] = \
                            vacation.special_submission_days \
                                (db, u, ctype, fd, d, st_subm)
                    ltot = cons

                    if 'approved_submissions' in self.fields:
                        container ['approved_submissions'] = \
                            vacation.vacation_submission_days \
                                (db, u, ctype, fd, d, st_accp, st_cnrq)

                    vd = common.pretty_range (fd, d)
                    vcids = db.vacation_correction.filter \
                        ( None
                        , dict 
                            ( user          = u
                            , date          = vd
                            , contract_type = ctype
                            )
                        )
                    try:
                        vcs = HTML_List ()
                        for x in vcids:
                            item  = self.htmldb.vacation_correction.getItem (x)
                            days  = item.days
                            ep    = self.utils.ExtProperty
                            vcs.append \
                                ( ep
                                    ( self.utils, days 
                                    , item         = item
                                    , is_labelprop = True
                                    )
                                )
                        container ['vacation corrections'] = vcs
                    except AttributeError:
                        container ['vacation corrections'] = ' + '.join \
                            (str (db.vacation_correction.get (i, 'days'))
                             for i in vcids
                            )
                    if (u, ctype) not in self.values:
                        self.values [(u, ctype)] = []
                    self.values [(u, ctype)].append (container)

                    nd = vacation.next_yearly_vacation_date \
                        (db, u, ctype, d + day)
                    ld = d
                    # Allow intermediate dates only for hr-vacation role
                    if nd > end and d < end and hv:
                        d = end
                    else:
                        d = nd - day
    # end def __init__

    def is_obsolete (self, dyn, date):
        """ Check if user becomes obsolete during this reporting period.
        """
        if not dyn:
            return True
        if not dyn.valid_to:
            return False
        if dyn.valid_to > date + common.day:
            return False
        return True
    # end def is_obsolete

    def permission_ok (self, user, dynuser, check_olo = True):
        if user == self.uid:
            return True
        if self.supi_clearance (user):
            return True
        if  (   check_olo
            and not dynamic_user_allowed_by_olo (self.db, self.uid, dynuser.id)
            ):
            return False
        if self.hv:
            return True
        return False
    # end def permission_ok

    def header_line (self, formatter):
        _ = self.db.i18n.gettext
        line = []
        line.append (formatter (_ ('user')))
        line.append (formatter (_ ('time')))
        vr = "javascript:help_window" \
             "('vacation_report?@template=helptext',500,400)"
        for f in self.fields:
            fld = HTML_Link (_ (f), vr)
            cls = self.header_classes.get (f, '')
            line.append (formatter (fld, cls = cls))
        if self.need_period:
            for f, perm in self.period_fields:
                if perm or self.is_allowed ():
                    line.append (formatter (_ (f)))
        return line
    # end def header_line

    def _output (self, line_formatter, item_formatter):
        for u in self.users:
            if u not in self.user_ctypes:
                continue
            for ctype in self.user_ctypes [u]:
                if (u, ctype) not in self.values:
                    continue
                for container in self.values [(u, ctype)]:
                    if  (   container ['is_obsolete']
                        and abs (container ['remaining vacation']) <= 0.05
                        and not self.show_obsolete
                        ):
                        continue
                    line  = []
                    line.append (item_formatter (container ['user']))
                    line.append (item_formatter (container))
                    for f in self.fields:
                        line.append (item_formatter (container [f]))
                    if self.need_period:
                        for f, perm in self.period_fields:
                            if perm or self.is_allowed ():
                                line.append (item_formatter (container [f]))
                    line_formatter (line)
    # end def _output

# end class Vacation_Report

class CSV_Report (Action, autosuper):
    def handle (self, outfile = None):
        request                   = templating.HTMLRequest     (self.client)
        self.utils                = templating.TemplatingUtils (self.client)
        h                         = self.client.additional_headers
        h ['Content-Type']        = 'text/csv'
        h ['Content-Disposition'] = 'inline; filename=summary.csv'
        self.client.header    ()
        if self.client.env ['REQUEST_METHOD'] == 'HEAD':
            # all done, return a dummy string
            return 'dummy'
        io = outfile
        if io is None:
            io = self.client.request.wfile
        report = self.report_class (self.db, request, self.utils, is_csv = True)
        io.write (report.as_csv ().encode ('utf-8'))
        return request_util.True_Value ()
    # end def handle
# end class CSV_Report

class CSV_Summary_Report (CSV_Report):
    report_class = Summary_Report
# end class CSV_Summary_Report

class CSV_Staff_Report (CSV_Report):
    report_class = Staff_Report
# end class CSV_Staff_Report

class CSV_Vacation_Report (CSV_Report):
    report_class = Vacation_Report
# end class CSV_Vacation_Report

def summary_report_links (db):
    """ Returns a list of summary-report links: We look up the config
        value summary_report_redirect in section ttt. If we find an
        entry we add a link to the redirect page with subject "Summary
        Report" and the original summary report with the text "Summary
        Report (old)". If not found we only return the normal summary
        report link as the only item. To be used in page.html for the
        menu.
    """
    _ = db.i18n.gettext
    orig = ('summary_report', 'View', 1, ('',''))
    old  = ('summary_report', 'View', 1, (_('Summary Report (old)'),''))
    red  = ('summary_report', 'View', 1, ('','redirect'))

    try:
        redir = db.config.ext.TTT_SUMMARY_REPORT_REDIRECT
    except InvalidOptionError:
        redir = None
    if redir:
        return [old, red]
    return [orig]
# end def summary_report_links

def init (instance):
    util   = instance.registerUtil
    util   ('Summary_Report',       Summary_Report)
    util   ('Staff_Report',         Staff_Report)
    util   ('Vacation_Report',      Vacation_Report)
    util   ('summary_report_links', summary_report_links)
    action = instance.registerAction
    action ('csv_summary_report',   CSV_Summary_Report)
    action ('csv_staff_report',     CSV_Staff_Report)
    action ('csv_vacation_report',  CSV_Vacation_Report)
# end def init
