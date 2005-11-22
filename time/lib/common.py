# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@mexx.mobile
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
#    common
#
# Purpose
#    Common detectors used more often
#
# Revision Dates
#     9-Nov-2004 (MPH) Creation
#     6-Apr-2005 (RSC) minor comment correction
#                      moved to lib
#    ««revision-date»»···
#--
#
from roundup import roundupdb, hyperdb
from roundup.exceptions import Reject
from roundup.date       import Date, Interval, Range
from time               import gmtime

ymd = '%Y-%m-%d'

def update_feature_status (db, cl, nodeid, new_values) :
    """auditor on feature.set

    update feature's status according to attached tasks/defects status.

    if single task is 'started' -> feature becomes 'open'
    if all tasks are 'accepted' -> feature becomes 'completed'
    if all tasks are 'accepted', but feature has open defects ->
                                   feature becomes 'completed-but-defects'
    """
    tasks   = new_values.get ("tasks")   or db.feature.get (nodeid, "tasks")
    defects = new_values.get ("defects") or db.feature.get (nodeid, "defects")
    open      = False
    completed = False
    task_started  = int (db.task_status.lookup ("started"))
    task_accepted = int (db.task_status.lookup ("accepted"))
    for task in tasks :
        task_status = int (db.task.get (task, "status"))
        if task_status == task_started :
            open = True
            break
        elif task_status >= task_accepted :
            completed = True
        elif task_status < task_started :
            completed = False
    if open :
        status = "open"
    elif completed :
        status = "completed"
    else :
        status = None

    if status == "completed" :
        # check if there are pending defects
        defect_closed = db.defect_status.lookup ("closed")
        has_defects = False
        for defect in defects :
            defect_status = db.defect.get (defect, "status")
            if defect_status < defect_closed :
                has_defects = True
                break
        if has_defects :
            status = "completed-but-defects"
    # set status
    if status :
        curr_status = new_values.get ("status") or \
                      db.feature.get (nodeid, "status")
        if status != curr_status :
            new_values ["status"] = db.feature_status.lookup (status)
# end def update_feature_status

def check_name_len (_, name) :
    if len (name) > 25 :
        raise Reject, \
            _ ('Name "%(name)s" too long (> 25 characters)') % locals ()
# end def name_len

def user_has_role (db, uid, * role) :
    roles = db.user.get (uid, 'roles')
    roles = dict ([(r.lower ().strip (), 1) for r in roles.split (',')])
    role  = [r.lower ().strip () for r in role]
    for r in role :
        if r in roles : return True
    return False
# end def user_has_role

def clearance_by (db, userid, only_subs = False) :
    assert (userid)
    sv = db.user.get (userid, 'supervisor')
    if not sv :
        return []
    ap = db.user.get (sv, 'clearance_by') or sv
    su = db.user.get (ap, 'substitute')
    clearance = [ap]
    if su and db.user.get (ap, 'subst_active') :
        if only_subs :
            return [su]
        clearance.append (su)
    return clearance
# end def clearance_by

def week_from_date (date) :
    wday        = gmtime (date.timestamp ())[6]
    start       = date + Interval ("%sd" % -wday)
    end         = date + Interval ("%sd" % (6 - wday))
    start       = Date (start.pretty (ymd))
    end         = Date (end.pretty   (ymd))
    return start, end
# end def week_from_date

def date_range (db, filterspec) :
    """ Extract date range from a filterspec. If no start time is given,
        use end time as start time, if no end time is given, use start
        time as end time. If not range is given use current week.
    """
    if 'date' in filterspec :
        r = Range (filterspec ['date'], Date)
        if r.to_value is None :
            start = end = r.from_value
        elif r.from_value is None or r.from_value == r.to_value :
            start = end = r.to_value
        else :
            start = r.from_value
            end   = r.to_value
        start = Date (start.pretty (ymd))
        end   = Date (  end.pretty (ymd))
    else :
        date       = Date ('.')
        date       = Date (str (date.local (db.getUserTimezone ())))
        start, end = week_from_date (date)
    return start, end
# end def date_range

def pretty_range (start, end) :
    return ';'.join ([x.pretty (ymd) for x in (start, end)])
# end def pretty_range

def first_thursday (year) :
    """ compute first thursday in the given year as a Date
        >>> first_thursday (1998)
        <Date 1998-01-01.00:00:0.000000>
        >>> first_thursday ("1998")
        <Date 1998-01-01.00:00:0.000000>
        >>> first_thursday (1999)
        <Date 1999-01-07.00:00:0.000000>
        >>> first_thursday (2000)
        <Date 2000-01-06.00:00:0.000000>
        >>> first_thursday (2001)
        <Date 2001-01-04.00:00:0.000000>
        >>> first_thursday (2002)
        <Date 2002-01-03.00:00:0.000000>
        >>> first_thursday (2003)
        <Date 2003-01-02.00:00:0.000000>
        >>> first_thursday (2004)
        <Date 2004-01-01.00:00:0.000000>
        >>> first_thursday (2005)
        <Date 2005-01-06.00:00:0.000000>
        >>> first_thursday (2006)
        <Date 2006-01-05.00:00:0.000000>
        >>> first_thursday (2007)
        <Date 2007-01-04.00:00:0.000000>
        >>> first_thursday (2008)
        <Date 2008-01-03.00:00:0.000000>
        >>> first_thursday (2009)
        <Date 2009-01-01.00:00:0.000000>
        >>> first_thursday (2010)
        <Date 2010-01-07.00:00:0.000000>
        >>> first_thursday (2011)
        <Date 2011-01-06.00:00:0.000000>
        >>> first_thursday (2012)
        <Date 2012-01-05.00:00:0.000000>
        >>> first_thursday (2013)
        <Date 2013-01-03.00:00:0.000000>
        >>> first_thursday (2014)
        <Date 2014-01-02.00:00:0.000000>
        >>> first_thursday (2015)
        <Date 2015-01-01.00:00:0.000000>
        >>> first_thursday (2016)
        <Date 2016-01-07.00:00:0.000000>
        >>> first_thursday (2017)
        <Date 2017-01-05.00:00:0.000000>
        >>> first_thursday (2018)
        <Date 2018-01-04.00:00:0.000000>
        >>> first_thursday (2019)
        <Date 2019-01-03.00:00:0.000000>
        >>> first_thursday (2020)
        <Date 2020-01-02.00:00:0.000000>
        >>> first_thursday (2021)
        <Date 2021-01-07.00:00:0.000000>
    """
    for i in range (1, 8) :
        date = Date ('%s-01-%02d' % (year, i))
        if gmtime (date.timestamp ()) [6] == 3 : # Thursday
            return date
    assert (0)
# end def first_thursday

def from_week_number (year, week_no) :
    """ Get first thursday in year, then add days.
        >>> from_week_number (1998, 52)
        (<Date 1998-12-21.00:00:0.000000>, <Date 1998-12-27.00:00:0.000000>)
        >>> from_week_number (1998, 53)
        (<Date 1998-12-28.00:00:0.000000>, <Date 1999-01-03.00:00:0.000000>)
        >>> from_week_number (1999,  1)
        (<Date 1999-01-04.00:00:0.000000>, <Date 1999-01-10.00:00:0.000000>)
        >>> from_week_number (1999, 52)
        (<Date 1999-12-27.00:00:0.000000>, <Date 2000-01-02.00:00:0.000000>)
        >>> from_week_number (2000,  1)
        (<Date 2000-01-03.00:00:0.000000>, <Date 2000-01-09.00:00:0.000000>)
        >>> from_week_number (2000, 52)
        (<Date 2000-12-25.00:00:0.000000>, <Date 2000-12-31.00:00:0.000000>)
        >>> from_week_number (2001,  1)
        (<Date 2001-01-01.00:00:0.000000>, <Date 2001-01-07.00:00:0.000000>)
        >>> from_week_number (2001, 52)
        (<Date 2001-12-24.00:00:0.000000>, <Date 2001-12-30.00:00:0.000000>)
        >>> from_week_number (2002,  1)
        (<Date 2001-12-31.00:00:0.000000>, <Date 2002-01-06.00:00:0.000000>)
        >>> from_week_number (2002, 52)
        (<Date 2002-12-23.00:00:0.000000>, <Date 2002-12-29.00:00:0.000000>)
        >>> from_week_number (2003,  1)
        (<Date 2002-12-30.00:00:0.000000>, <Date 2003-01-05.00:00:0.000000>)
        >>> from_week_number (2003, 52)
        (<Date 2003-12-22.00:00:0.000000>, <Date 2003-12-28.00:00:0.000000>)
        >>> from_week_number (2004,  1)
        (<Date 2003-12-29.00:00:0.000000>, <Date 2004-01-04.00:00:0.000000>)
        >>> from_week_number (2004, 52)
        (<Date 2004-12-20.00:00:0.000000>, <Date 2004-12-26.00:00:0.000000>)
        >>> from_week_number (2004, 53)
        (<Date 2004-12-27.00:00:0.000000>, <Date 2005-01-02.00:00:0.000000>)
        >>> from_week_number (2005,  1)
        (<Date 2005-01-03.00:00:0.000000>, <Date 2005-01-09.00:00:0.000000>)
        >>> from_week_number (2005, 29)
        (<Date 2005-07-18.00:00:0.000000>, <Date 2005-07-24.00:00:0.000000>)
        >>> from_week_number (2005, 52)
        (<Date 2005-12-26.00:00:0.000000>, <Date 2006-01-01.00:00:0.000000>)
        >>> from_week_number (2006,  1)
        (<Date 2006-01-02.00:00:0.000000>, <Date 2006-01-08.00:00:0.000000>)
        >>> from_week_number (2006, 52)
        (<Date 2006-12-25.00:00:0.000000>, <Date 2006-12-31.00:00:0.000000>)
        >>> from_week_number (2007,  1)
        (<Date 2007-01-01.00:00:0.000000>, <Date 2007-01-07.00:00:0.000000>)
        >>> from_week_number (2007, 52)
        (<Date 2007-12-24.00:00:0.000000>, <Date 2007-12-30.00:00:0.000000>)
        >>> from_week_number (2008,  1)
        (<Date 2007-12-31.00:00:0.000000>, <Date 2008-01-06.00:00:0.000000>)
        >>> from_week_number (2008, 52)
        (<Date 2008-12-22.00:00:0.000000>, <Date 2008-12-28.00:00:0.000000>)
        >>> from_week_number (2009,  1)
        (<Date 2008-12-29.00:00:0.000000>, <Date 2009-01-04.00:00:0.000000>)
        >>> from_week_number (2009, 52)
        (<Date 2009-12-21.00:00:0.000000>, <Date 2009-12-27.00:00:0.000000>)
        >>> from_week_number (2009, 53)
        (<Date 2009-12-28.00:00:0.000000>, <Date 2010-01-03.00:00:0.000000>)
        >>> from_week_number (2010,  1)
        (<Date 2010-01-04.00:00:0.000000>, <Date 2010-01-10.00:00:0.000000>)
        >>> from_week_number (2010, 52)
        (<Date 2010-12-27.00:00:0.000000>, <Date 2011-01-02.00:00:0.000000>)
    """
    date = first_thursday (year)
    date = date + Interval ('%dd' % ((week_no - 1) * 7))
    return week_from_date (date)
# end def from_week_number

def weekno_from_day (date) :
    """ Compute the week number from the given date
        >>> weekno_from_day (Date ('2005-08-26'))
        34
        >>> weekno_from_day (Date ("1998-12-21"))
        52
        >>> weekno_from_day (Date ("1998-12-27"))
        52
        >>> weekno_from_day (Date ("1998-12-28"))
        53
        >>> weekno_from_day (Date ("1999-01-03"))
        53
        >>> weekno_from_day (Date ("1999-01-04"))
        1
        >>> weekno_from_day (Date ("1999-01-10"))
        1
        >>> weekno_from_day (Date ("1999-12-27"))
        52
        >>> weekno_from_day (Date ("2000-01-02"))
        52
        >>> weekno_from_day (Date ("2000-01-03"))
        1
        >>> weekno_from_day (Date ("2000-01-09"))
        1
        >>> weekno_from_day (Date ("2000-12-25"))
        52
        >>> weekno_from_day (Date ("2000-12-31"))
        52
        >>> weekno_from_day (Date ("2001-01-01"))
        1
        >>> weekno_from_day (Date ("2001-01-07"))
        1
        >>> weekno_from_day (Date ("2001-12-24"))
        52
        >>> weekno_from_day (Date ("2001-12-30"))
        52
        >>> weekno_from_day (Date ("2001-12-31"))
        1
        >>> weekno_from_day (Date ("2002-01-06"))
        1
        >>> weekno_from_day (Date ("2002-12-23"))
        52
        >>> weekno_from_day (Date ("2002-12-29"))
        52
        >>> weekno_from_day (Date ("2002-12-30"))
        1
        >>> weekno_from_day (Date ("2003-01-05"))
        1
        >>> weekno_from_day (Date ("2003-12-22"))
        52
        >>> weekno_from_day (Date ("2003-12-28"))
        52
        >>> weekno_from_day (Date ("2003-12-29"))
        1
        >>> weekno_from_day (Date ("2004-01-04"))
        1
        >>> weekno_from_day (Date ("2004-12-20"))
        52
        >>> weekno_from_day (Date ("2004-12-26"))
        52
        >>> weekno_from_day (Date ("2004-12-27"))
        53
        >>> weekno_from_day (Date ("2005-01-02"))
        53
        >>> weekno_from_day (Date ("2005-01-03"))
        1
        >>> weekno_from_day (Date ("2005-01-09"))
        1
        >>> weekno_from_day (Date ("2005-07-18"))
        29
        >>> weekno_from_day (Date ("2005-07-24"))
        29
        >>> weekno_from_day (Date ("2005-12-26"))
        52
        >>> weekno_from_day (Date ("2006-01-01"))
        52
        >>> weekno_from_day (Date ("2006-01-02"))
        1
        >>> weekno_from_day (Date ("2006-01-08"))
        1
        >>> weekno_from_day (Date ("2006-12-25"))
        52
        >>> weekno_from_day (Date ("2006-12-31"))
        52
        >>> weekno_from_day (Date ("2007-01-01"))
        1
        >>> weekno_from_day (Date ("2007-01-07"))
        1
        >>> weekno_from_day (Date ("2007-12-24"))
        52
        >>> weekno_from_day (Date ("2007-12-30"))
        52
        >>> weekno_from_day (Date ("2007-12-31"))
        1
        >>> weekno_from_day (Date ("2008-01-06"))
        1
        >>> weekno_from_day (Date ("2008-12-22"))
        52
        >>> weekno_from_day (Date ("2008-12-28"))
        52
        >>> weekno_from_day (Date ("2008-12-29"))
        1
        >>> weekno_from_day (Date ("2009-01-04"))
        1
        >>> weekno_from_day (Date ("2009-12-21"))
        52
        >>> weekno_from_day (Date ("2009-12-27"))
        52
        >>> weekno_from_day (Date ("2009-12-28"))
        53
        >>> weekno_from_day (Date ("2010-01-03"))
        53
        >>> weekno_from_day (Date ("2010-01-04"))
        1
        >>> weekno_from_day (Date ("2010-01-10"))
        1
        >>> weekno_from_day (Date ("2010-12-27"))
        52
        >>> weekno_from_day (Date ("2011-01-02"))
        52
    """
    date   = Date (str (date))
    wday   = gmtime (date.timestamp ())[6]
    date   = date + Interval ('%dd' % (3 - wday)) # Thursday that week
    yday2  = gmtime (date.timestamp ())[7]
    d      = first_thursday (date.year)
    yday1  = gmtime (d.timestamp    ())[7]
    assert ((yday2 - yday1) % 7 == 0)
    return int ((yday2 - yday1) / 7 + 1)
# end def weekno_from_day

def monthstart_twoweeksago (date = '.') :
    """return the last month start from at least two weeks ago as a
       roundup date string. We need this for some default queries that
       need a date range.

       >>> monthstart_twoweeksago ('2005-01-01')
       '2004-12-01'
       >>> monthstart_twoweeksago ('2005-11-22')
       '2005-11-01'
       >>> monthstart_twoweeksago ('2005-11-13')
       '2005-10-01'
       >>> monthstart_twoweeksago ('2005-11-14')
       '2005-10-01'
       >>> monthstart_twoweeksago ('2005-11-15')
       '2005-11-01'
    """
    d = Date (date) - Interval ('14d')
    d.day = 1
    return d.pretty (ymd)
# end def monthstart_twoweeksago

### __END__
