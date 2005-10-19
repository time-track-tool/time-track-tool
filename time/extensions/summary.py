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

from roundup.date import Date
try :
    from common import pretty_range, week_from_date, ymd, user_has_role
except ImportError :
    ymd            = None
    pretty_range   = None
    week_from_date = None
    user_has_role  = None

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

def update_wps_and_group (wps, group, group_item) :
    for wp in wps.iterkeys () :
        if wp not in group :
            group [wp]      = [group_item]
        else :
            group [wp].append (group_item)
# end def update_wps_and_group

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

def summary_report (db, request) :
    """ TODO:
        - intermediate sums by
          - time_wp_group
          - project
          - cost_center
          - cost_center_group
        - special colors for 
          - daily record not yet accepted
          - no daily record found
    """
    filterspec  = request.filterspec
    sort_by     = request.sort
    group_by    = request.group
    columns     = request.columns
    now         = Date ('.')
    assert (request.classname == 'summary_report')
    sup_users   = user_supervisor_for (db)

    if not columns :
        columns = db.summary_report.getprops ().keys ()

    print filterspec
    date        = filterspec.get ('date', pretty_range (*week_from_date (now)))
    users       = filterspec.get ('user', [])
    sv          = filterspec.get ('supervisor', [])
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
        (None, dict (user = users, date = date))
    print "n_dr:", len (dr)
    dr          = dict \
        ([(d, Extended_Daily_Record (db, d, sup_users)) for d in dr])

    wp          = dict ([(w, 1) for w in filterspec.get ('time_wp', [])])
    wpgs        = filterspec.get ('time_wp_group',     [])
    wp_wpg      = {}
    for wpg in wpgs :
        wps     = dict ([(w, 1) for w in db.time_wp_group.get (wpg, 'wps')])
        update_wps_and_group (wps, wp_wpg, wpg)
        wp.update (wps)
    ccs         = filterspec.get ('cost_center',       [])
    wp_cc       = {}
    for cc in ccs :
        wps     = dict ([(w, 1) for w in db.time_wp.find (cost_center = cc)])
        update_wps_and_group (wps, wp_cc, cc)
        wp.update (wps)
    ccg         = dict \
        ([(c, 1) for c in filterspec.get ('cost_center_group', [])])
    wp_ccg      = {}
    if ccg :
        ccs     = db.cost_center.find (cost_center_group = ccg)
        ccs     = dict ([(c, 1) for c in ccs])
        for cc in ccs :
            wps = dict ([(w, 1) for w in db.time_wp.find (cost_center = cc)])
            update_wps_and_group (wps, wp_ccg, ccg)
            wp.update (wps)
    if not wp :
        wp = dict ([(w, 1) for w in db.time_wp.getnodeids ()])
    print "n_wp:", len (wp)
    work_pkg    = dict ([(w, Extended_WP (db, w)) for w in wp.iterkeys ()])
    time_recs   = [Extended_Time_Record (db, t, dr, work_pkg)
                   for t in db.time_record.find
                    (daily_record = dr, wp = work_pkg)
                  ]
    time_recs   = [t for t in time_recs if t.is_own]
    print "n_tr:", len (time_recs)
    time_recs.sort ()
    usernames   = dict ([(tr.username, 1) for tr in time_recs]).keys ()
    usernames.sort ()
    print usernames
# end def summary_report

def init (instance) :
    global ymd, pretty_range, week_from_date, user_has_role
    sys.path.insert (0, os.path.join (instance.config.HOME, 'lib'))
    from common import pretty_range, week_from_date, ymd, user_has_role
    del sys.path [0]
    util = instance.registerUtil
    util ('summary_report', summary_report)
# end def init
