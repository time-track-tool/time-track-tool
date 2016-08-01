#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-16 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    common
#
# Purpose
#    Common detectors used more often
#
#--
#
import locale
import datetime
import cgi
from   urllib                 import quote as urlquote
from   time                   import gmtime
from   roundup                import roundupdb, hyperdb
from   roundup.exceptions     import Reject
from   roundup.date           import Date, Interval, Range
from   roundup.hyperdb        import String, Link, Multilink
from   roundup.cgi.templating import MultilinkHTMLProperty, LinkHTMLProperty
from   rup_utils              import translate

TFL = None
try :
    from   _TFL               import TFL
    import _TFL._Meta.Object
    import _TFL.Numeric_Interval
    import _TFL.Interval_Set
except (ImportError, SyntaxError) :
    pass

ymd = '%Y-%m-%d'
day = Interval ('1d')

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

def is_matching_result (cl, kw, search_result) :
    for k, v in kw.iteritems () :
        if isinstance (cl.properties [k], String) :
            if cl.get (search_result, k) != v :
                return False
    return True
# end def is_matching_result

def check_unique (_, cl, id, ** kw) :
    search = cl.filter (None, kw)
    # strings do a substring search.
    for s in search :
        if s != id and is_matching_result (cl, kw, s) :
            r = []
            for k, v in kw.iteritems () :
                attr = _ (str (k))
                val  =    cgi.escape (str (v))
                r.append ("%(attr)s=%(val)s" % locals ())
            raise Reject, _ ("Duplicate: %s") % ', '.join (r)
# end def check_unique

def sort_uniq (list) :
    d = dict ([(x, 1) for x in list])
    k = d.keys ()
    k.sort ()
    return k
# end def sort_uniq

def check_loop (_, cl, id, prop, attr, labelprop = None, ids = None) :
    if ids is None :
        ids = []
    is_multi = isinstance (cl.properties [prop], Multilink)
    assert (is_multi or isinstance (cl.properties [prop], Link))
    if not labelprop :
        labelprop = cl.labelprop ()
    if id :
        ids.append (id)
    if attr :
        if not is_multi :
            attr = [attr]
        for a in attr :
            if a in ids :
                raise Reject, _ ('"%(prop)s" loop: %(labels)s') % dict \
                    ( prop   = _ (prop)
                    , labels = ','.join ([cl.get (i, labelprop) for i in ids])
                    )
            check_loop (_, cl, a, prop, cl.get (a, prop), labelprop, ids)
            ids.pop ()
# end def check_loop

def interval_set_from_string (interval_string) :
    """
        >>> interval_set_from_string ('200-300,500-700')
        Interval_Set ((200, 300), (500, 700))
        >>> interval_set_from_string ('30000-39999')
        Interval_Set ((30000, 39999))
        >>> interval_set_from_string ('300-399, 7000-7999')
        Interval_Set ((300, 399), (7000, 7999))
    """
    intervals = []
    for i in interval_string.split (',') :
        bounds = i.split ('-')
        if len (bounds) == 1 :
            bounds = (bounds [0], bounds [0])
        bounds = (long (b) for b in bounds)
        intervals.append (TFL.Numeric_Interval (* bounds))
    return TFL.Interval_Set (* intervals)
# end def interval_set_from_string

def next_uid_or_gid (last, interval_string) :
    """
        >>> next_uid_or_gid (1, '1-2')
        2L
        >>> next_uid_or_gid (30000, '30000-39999')
        30001L
        >>> next_uid_or_gid (399, '300-399, 7000-7999')
        7000L
    """
    last = long (last) or 0L
    iset = interval_set_from_string (interval_string)
    return iset.next_point_up (last + 1)
# end def next_uid_or_gid

def uid_or_gid_in_range (id, interval_string) :
    """
        >>> uid_or_gid_in_range (2, '47-99')
        False
        >>> uid_or_gid_in_range (46, '47-99')
        False
        >>> uid_or_gid_in_range (100, '47-99')
        False
        >>> uid_or_gid_in_range (47, '47-99')
        True
        >>> uid_or_gid_in_range (49, '47-99')
        True
        >>> uid_or_gid_in_range (99, '47-99')
        True
    """
    iset = interval_set_from_string (interval_string)
    return iset.contains_point (id)
# end def uid_or_gid_in_range

char_table = \
    { 'ä'.decode ('latin1') : 'ae'
    , 'ö'.decode ('latin1') : 'oe'
    , 'ü'.decode ('latin1') : 'ue'
    , 'ß'.decode ('latin1') : 'ss'
    , 'Ä'.decode ('latin1') : 'ae'
    , 'Ö'.decode ('latin1') : 'oe'
    , 'Ü'.decode ('latin1') : 'ue'
    , ' '.decode ('latin1') : '.'
    }
for j in 'abcdefghijklmnopqrstuvwxyz' :
    char_table [j]          = j
    char_table [j.upper ()] = j

def tolower_ascii (name) :
    """ Compute lowercase value from name suitable for email address
    >>> tolower_ascii ('Ralf Schlatterbeck')
    'ralf.schlatterbeck'
    >>> tolower_ascii ('Günther Umläütß'.decode ('latin1').encode ('utf-8'))
    'guenther.umlaeuetss'
    """
    n = []
    for i in name.decode ('utf-8') :
        n.extend (list (char_table.get (i, '')))
    return ''.join (n)
# end def tolower_ascii


def uniq (_, cl, id, ** kw) :
    """ Function for regression-testing new_nickname
    """
    rej  = { 'gst' : 1, 'gsr' : 1 }
    nick = kw.get ('nickname')
    user = kw.get ('username')
    if nick in rej or user in rej :
        raise Reject, "BLA"
# end def uniq

def new_nickname (_, cl, nodeid, lfn, lln, uniq = check_unique) :
    """ Compute a new nickname that does not collide with an existing
        one.
        >>> new_nickname (None, None, None, 'guenther', 'stdl', uniq)
        'gsd'
        >>> new_nickname (None, None, None, 'guenther', 'st', uniq)
        'ust'
    """
    for f in lfn :
        for l1 in lln [:-1] :
            for l2 in lln [1:] :
                nick = ''.join ((f, l1, l2))
                try :
                    uniq (_, cl, nodeid, nickname = nick)
                    uniq (_, cl, nodeid, username = nick)
                    return nick
                except Reject :
                    pass
    return None
# end def new_nickname

def user_has_role (db, uid, * role) :
    roles = db.user.get (uid, 'roles')
    if not roles :
        return False
    roles = dict.fromkeys (role_list (roles))
    role  = [r.lower ().strip () for r in role]
    for r in role :
        if r in roles : return True
    return False
# end def user_has_role

def get_uids_with_role (db, role) :
    users = []
    for uid in db.user.getnodeids (retired = False) :
        if user_has_role (db, uid, role) :
            users.append (uid)
    return users
# end def get_uids_with_role

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
    """ Return start and end of week from give date
        >>> week_from_date (Date ('2007-01-01'))
        (<Date 2007-01-01.00:00:00.000>, <Date 2007-01-07.00:00:00.000>)
        >>> week_from_date (Date ('2006-01-01'))
        (<Date 2005-12-26.00:00:00.000>, <Date 2006-01-01.00:00:00.000>)
    """
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
    r = None
    f = filterspec.get ('date', None)
    if f:
        if ';' not in f:
            f = ';'.join ((f,f))
        r = Range (f, Date)
    if r and (r.to_value or r.from_value) :
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
        >>> f = '<Date %Y-%m-%d.%H:%M>'
        >>> first_thursday (1998).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 1998-01-01.00:00:00>'
        >>> first_thursday ("1998").pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 1998-01-01.00:00:00>'
        >>> first_thursday (1999).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 1999-01-07.00:00:00>'
        >>> first_thursday (2000).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2000-01-06.00:00:00>'
        >>> first_thursday (2001).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2001-01-04.00:00:00>'
        >>> first_thursday (2002).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2002-01-03.00:00:00>'
        >>> first_thursday (2003).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2003-01-02.00:00:00>'
        >>> first_thursday (2004).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2004-01-01.00:00:00>'
        >>> first_thursday (2005).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2005-01-06.00:00:00>'
        >>> first_thursday (2006).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2006-01-05.00:00:00>'
        >>> first_thursday (2007).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2007-01-04.00:00:00>'
        >>> first_thursday (2008).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2008-01-03.00:00:00>'
        >>> first_thursday (2009).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2009-01-01.00:00:00>'
        >>> first_thursday (2010).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2010-01-07.00:00:00>'
        >>> first_thursday (2011).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2011-01-06.00:00:00>'
        >>> first_thursday (2012).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2012-01-05.00:00:00>'
        >>> first_thursday (2013).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2013-01-03.00:00:00>'
        >>> first_thursday (2014).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2014-01-02.00:00:00>'
        >>> first_thursday (2015).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2015-01-01.00:00:00>'
        >>> first_thursday (2016).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2016-01-07.00:00:00>'
        >>> first_thursday (2017).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2017-01-05.00:00:00>'
        >>> first_thursday (2018).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2018-01-04.00:00:00>'
        >>> first_thursday (2019).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2019-01-03.00:00:00>'
        >>> first_thursday (2020).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2020-01-02.00:00:00>'
        >>> first_thursday (2021).pretty ('<Date %Y-%m-%d.%H:%M:%S>')
        '<Date 2021-01-07.00:00:00>'
    """
    for i in range (1, 8) :
        date = Date ('%s-01-%02d' % (year, i))
        if gmtime (date.timestamp ()) [6] == 3 : # Thursday
            return date
    assert (0)
# end def first_thursday

def from_week_number (year, week_no) :
    """ Get first thursday in year, then add days.
        >>> f = 'Date %Y-%m-%d.%H:%M:%S'
        >>> [d.pretty (f) for d in from_week_number (1998, 52)]
        ['Date 1998-12-21.00:00:00', 'Date 1998-12-27.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (1998, 53)]
        ['Date 1998-12-28.00:00:00', 'Date 1999-01-03.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (1999,  1)]
        ['Date 1999-01-04.00:00:00', 'Date 1999-01-10.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (1999, 52)]
        ['Date 1999-12-27.00:00:00', 'Date 2000-01-02.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2000,  1)]
        ['Date 2000-01-03.00:00:00', 'Date 2000-01-09.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2000, 52)]
        ['Date 2000-12-25.00:00:00', 'Date 2000-12-31.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2001,  1)]
        ['Date 2001-01-01.00:00:00', 'Date 2001-01-07.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2001, 52)]
        ['Date 2001-12-24.00:00:00', 'Date 2001-12-30.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2002,  1)]
        ['Date 2001-12-31.00:00:00', 'Date 2002-01-06.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2002, 52)]
        ['Date 2002-12-23.00:00:00', 'Date 2002-12-29.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2003,  1)]
        ['Date 2002-12-30.00:00:00', 'Date 2003-01-05.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2003, 52)]
        ['Date 2003-12-22.00:00:00', 'Date 2003-12-28.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2004,  1)]
        ['Date 2003-12-29.00:00:00', 'Date 2004-01-04.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2004, 52)]
        ['Date 2004-12-20.00:00:00', 'Date 2004-12-26.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2004, 53)]
        ['Date 2004-12-27.00:00:00', 'Date 2005-01-02.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2005,  1)]
        ['Date 2005-01-03.00:00:00', 'Date 2005-01-09.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2005, 29)]
        ['Date 2005-07-18.00:00:00', 'Date 2005-07-24.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2005, 52)]
        ['Date 2005-12-26.00:00:00', 'Date 2006-01-01.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2006,  1)]
        ['Date 2006-01-02.00:00:00', 'Date 2006-01-08.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2006, 52)]
        ['Date 2006-12-25.00:00:00', 'Date 2006-12-31.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2007,  1)]
        ['Date 2007-01-01.00:00:00', 'Date 2007-01-07.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2007, 52)]
        ['Date 2007-12-24.00:00:00', 'Date 2007-12-30.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2008,  1)]
        ['Date 2007-12-31.00:00:00', 'Date 2008-01-06.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2008, 52)]
        ['Date 2008-12-22.00:00:00', 'Date 2008-12-28.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2009,  1)]
        ['Date 2008-12-29.00:00:00', 'Date 2009-01-04.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2009, 52)]
        ['Date 2009-12-21.00:00:00', 'Date 2009-12-27.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2009, 53)]
        ['Date 2009-12-28.00:00:00', 'Date 2010-01-03.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2010,  1)]
        ['Date 2010-01-04.00:00:00', 'Date 2010-01-10.00:00:00']
        >>> [d.pretty (f) for d in from_week_number (2010, 52)]
        ['Date 2010-12-27.00:00:00', 'Date 2011-01-02.00:00:00']
    """
    date = first_thursday (year)
    date = date + Interval ('%dd' % ((week_no - 1) * 7))
    return week_from_date (date)
# end def from_week_number

def weekno_year_from_day (date) :
    """ Compute the week number from the given date
        >>> weekno_year_from_day (Date ('2005-08-26'))
        (34, 2005)
        >>> weekno_year_from_day (Date ("1998-12-21"))
        (52, 1998)
        >>> weekno_year_from_day (Date ("1998-12-27"))
        (52, 1998)
        >>> weekno_year_from_day (Date ("1998-12-28"))
        (53, 1998)
        >>> weekno_year_from_day (Date ("1999-01-03"))
        (53, 1998)
        >>> weekno_year_from_day (Date ("1999-01-04"))
        (1, 1999)
        >>> weekno_year_from_day (Date ("1999-01-10"))
        (1, 1999)
        >>> weekno_year_from_day (Date ("1999-12-27"))
        (52, 1999)
        >>> weekno_year_from_day (Date ("2000-01-02"))
        (52, 1999)
        >>> weekno_year_from_day (Date ("2000-01-03"))
        (1, 2000)
        >>> weekno_year_from_day (Date ("2000-01-09"))
        (1, 2000)
        >>> weekno_year_from_day (Date ("2000-12-25"))
        (52, 2000)
        >>> weekno_year_from_day (Date ("2000-12-31"))
        (52, 2000)
        >>> weekno_year_from_day (Date ("2001-01-01"))
        (1, 2001)
        >>> weekno_year_from_day (Date ("2001-01-07"))
        (1, 2001)
        >>> weekno_year_from_day (Date ("2001-12-24"))
        (52, 2001)
        >>> weekno_year_from_day (Date ("2001-12-30"))
        (52, 2001)
        >>> weekno_year_from_day (Date ("2001-12-31"))
        (1, 2002)
        >>> weekno_year_from_day (Date ("2002-01-06"))
        (1, 2002)
        >>> weekno_year_from_day (Date ("2002-12-23"))
        (52, 2002)
        >>> weekno_year_from_day (Date ("2002-12-29"))
        (52, 2002)
        >>> weekno_year_from_day (Date ("2002-12-30"))
        (1, 2003)
        >>> weekno_year_from_day (Date ("2003-01-05"))
        (1, 2003)
        >>> weekno_year_from_day (Date ("2003-12-22"))
        (52, 2003)
        >>> weekno_year_from_day (Date ("2003-12-28"))
        (52, 2003)
        >>> weekno_year_from_day (Date ("2003-12-29"))
        (1, 2004)
        >>> weekno_year_from_day (Date ("2004-01-04"))
        (1, 2004)
        >>> weekno_year_from_day (Date ("2004-12-20"))
        (52, 2004)
        >>> weekno_year_from_day (Date ("2004-12-26"))
        (52, 2004)
        >>> weekno_year_from_day (Date ("2004-12-27"))
        (53, 2004)
        >>> weekno_year_from_day (Date ("2005-01-02"))
        (53, 2004)
        >>> weekno_year_from_day (Date ("2005-01-03"))
        (1, 2005)
        >>> weekno_year_from_day (Date ("2005-01-09"))
        (1, 2005)
        >>> weekno_year_from_day (Date ("2005-07-18"))
        (29, 2005)
        >>> weekno_year_from_day (Date ("2005-07-24"))
        (29, 2005)
        >>> weekno_year_from_day (Date ("2005-12-26"))
        (52, 2005)
        >>> weekno_year_from_day (Date ("2006-01-01"))
        (52, 2005)
        >>> weekno_year_from_day (Date ("2006-01-02"))
        (1, 2006)
        >>> weekno_year_from_day (Date ("2006-01-08"))
        (1, 2006)
        >>> weekno_year_from_day (Date ("2006-12-25"))
        (52, 2006)
        >>> weekno_year_from_day (Date ("2006-12-31"))
        (52, 2006)
        >>> weekno_year_from_day (Date ("2007-01-01"))
        (1, 2007)
        >>> weekno_year_from_day (Date ("2007-01-07"))
        (1, 2007)
        >>> weekno_year_from_day (Date ("2007-12-24"))
        (52, 2007)
        >>> weekno_year_from_day (Date ("2007-12-30"))
        (52, 2007)
        >>> weekno_year_from_day (Date ("2007-12-31"))
        (1, 2008)
        >>> weekno_year_from_day (Date ("2008-01-06"))
        (1, 2008)
        >>> weekno_year_from_day (Date ("2008-12-22"))
        (52, 2008)
        >>> weekno_year_from_day (Date ("2008-12-28"))
        (52, 2008)
        >>> weekno_year_from_day (Date ("2008-12-29"))
        (1, 2009)
        >>> weekno_year_from_day (Date ("2009-01-04"))
        (1, 2009)
        >>> weekno_year_from_day (Date ("2009-12-21"))
        (52, 2009)
        >>> weekno_year_from_day (Date ("2009-12-27"))
        (52, 2009)
        >>> weekno_year_from_day (Date ("2009-12-28"))
        (53, 2009)
        >>> weekno_year_from_day (Date ("2010-01-03"))
        (53, 2009)
        >>> weekno_year_from_day (Date ("2010-01-04"))
        (1, 2010)
        >>> weekno_year_from_day (Date ("2010-01-10"))
        (1, 2010)
        >>> weekno_year_from_day (Date ("2010-12-27"))
        (52, 2010)
        >>> weekno_year_from_day (Date ("2011-01-02"))
        (52, 2010)
    """
    date   = Date (str (date))
    wday   = gmtime (date.timestamp ())[6]
    date   = date + Interval ('%dd' % (3 - wday)) # Thursday that week
    yday2  = gmtime (date.timestamp ())[7]
    d      = first_thursday (date.year)
    yday1  = gmtime (d.timestamp    ())[7]
    assert ((yday2 - yday1) % 7 == 0)
    return int ((yday2 - yday1) / 7 + 1), int (date.year)
# end def weekno_year_from_day

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

def is_month_end (date) :
    """ return True if the given date is the last day of a month
        >>> is_month_end (Date ('2006-01-31'))
        True
        >>> is_month_end (Date ('2006-01-30'))
        False
        >>> is_month_end (Date ('2006-02-28'))
        True
        >>> is_month_end (Date ('2007-02-28'))
        True
        >>> is_month_end (Date ('2008-02-28'))
        False
        >>> is_month_end (Date ('2008-02-29'))
        True
        >>> is_month_end (Date ('2004-02-28'))
        False
        >>> is_month_end (Date ('2004-02-29'))
        True
        >>> is_month_end (Date ('2000-02-28'))
        False
        >>> is_month_end (Date ('2000-02-29'))
        True
        >>> is_month_end (Date ('2006-12-31'))
        True
        >>> is_month_end (Date ('2006-12-30'))
        False
    """
    tomorrow = date + Interval ('1d')
    return date.month != tomorrow.month
# end def is_month_end

def start_of_month (date) :
    """ Return date matching first of month for given date
        >>> f = '%Y-%m-%d.%H:%M:%S'
        >>> start_of_month (Date ('2006-01-01.23:17')).pretty (f)
        '2006-01-01.00:00:00'
        >>> start_of_month (Date ('2006-01-31.23:17')).pretty (f)
        '2006-01-01.00:00:00'
        >>> start_of_month (Date ('2006-01-17.23:17')).pretty (f)
        '2006-01-01.00:00:00'
        >>> start_of_month (Date ('2006-01-17.00:00')).pretty (f)
        '2006-01-01.00:00:00'
    """
    date = Date (date.pretty ('%Y-%m-01'))
    return date
# end def start_of_month

_month_lookup = \
    {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

def end_of_month (date) :
    """ Compute end of month relative to given date
        >>> f = '%Y-%m-%d.%H:%M:%S'
        >>> end_of_month (Date ('2006-01-31')).pretty (f)
        '2006-01-31.00:00:00'
        >>> end_of_month (Date ('2006-01-30')).pretty (f)
        '2006-01-31.00:00:00'
        >>> end_of_month (Date ('2006-02-28')).pretty (f)
        '2006-02-28.00:00:00'
        >>> end_of_month (Date ('2007-02-28')).pretty (f)
        '2007-02-28.00:00:00'
        >>> end_of_month (Date ('2008-02-28')).pretty (f)
        '2008-02-29.00:00:00'
        >>> end_of_month (Date ('2008-02-29')).pretty (f)
        '2008-02-29.00:00:00'
        >>> end_of_month (Date ('2004-02-28')).pretty (f)
        '2004-02-29.00:00:00'
        >>> end_of_month (Date ('2004-02-29')).pretty (f)
        '2004-02-29.00:00:00'
        >>> end_of_month (Date ('2000-02-28')).pretty (f)
        '2000-02-29.00:00:00'
        >>> end_of_month (Date ('2000-02-29')).pretty (f)
        '2000-02-29.00:00:00'
        >>> end_of_month (Date ('2006-12-31')).pretty (f)
        '2006-12-31.00:00:00'
        >>> end_of_month (Date ('2006-12-30')).pretty (f)
        '2006-12-31.00:00:00'
        >>> end_of_month (Date ('2006-03-01')).pretty (f)
        '2006-03-31.00:00:00'
        >>> end_of_month (Date ('2006-04-01')).pretty (f)
        '2006-04-30.00:00:00'
        >>> end_of_month (Date ('2006-05-01')).pretty (f)
        '2006-05-31.00:00:00'
        >>> end_of_month (Date ('2006-06-01')).pretty (f)
        '2006-06-30.00:00:00'
        >>> end_of_month (Date ('2006-07-01')).pretty (f)
        '2006-07-31.00:00:00'
        >>> end_of_month (Date ('2006-08-01')).pretty (f)
        '2006-08-31.00:00:00'
        >>> end_of_month (Date ('2006-09-01')).pretty (f)
        '2006-09-30.00:00:00'
        >>> end_of_month (Date ('2006-10-01')).pretty (f)
        '2006-10-31.00:00:00'
        >>> end_of_month (Date ('2006-11-01')).pretty (f)
        '2006-11-30.00:00:00'
        >>> for k in range (1, 13) :
        ...     assert (is_month_end (end_of_month (Date ('2006-%02d-07' % k))))
    """
    if date.month != 2 :
        return Date \
            ( '%04d-%02d-%02d'
            % (date.year, date.month, _month_lookup [date.month])
            )
    for k in 28, 29 :
        d = Date ('%04d-%02d-%02d' % (date.year, date.month, k))
        if is_month_end (d) :
            return d
    assert (0)
# end def end_of_month

def start_of_year (date) :
    """ Return date matching first of year for given date
        >>> f = '%Y-%m-%d.%H:%M:%S'
        >>> start_of_year (Date ('2006-01-01.23:17')).pretty (f)
        '2006-01-01.00:00:00'
        >>> start_of_year (Date ('2006-01-31.23:17')).pretty (f)
        '2006-01-01.00:00:00'
        >>> start_of_year (Date ('2006-01-17.23:17')).pretty (f)
        '2006-01-01.00:00:00'
        >>> start_of_year (Date ('2006-01-17.00:00')).pretty (f)
        '2006-01-01.00:00:00'
        >>> start_of_year (Date ('2006-07-17.23:17:05')).pretty (f)
        '2006-01-01.00:00:00'
        >>> start_of_year (Date ('2006-12-17.23:17:05')).pretty (f)
        '2006-01-01.00:00:00'
        >>> start_of_year (Date ('2006-12-31.23:17:05')).pretty (f)
        '2006-01-01.00:00:00'
        >>> start_of_year (Date ('2006-12-31.23:59:59')).pretty (f)
        '2006-01-01.00:00:00'
    """
    date = Date (date.pretty ('%Y-01-01'))
    return date
# end def start_of_year

def next_search_date (date, direction = '+') :
    """ Return find-pattern for date matching everything after next day
        (or everything before previous if direction is '-')
        >>> next_search_date (Date ('2006-01-01.23:17'))
        '2006-01-02;'
        >>> next_search_date (Date ('2006-01-01.23:17'), '-')
        ';2005-12-31'
    """
    day  = Interval ('%s1d' % direction)
    return (Date (date.pretty (ymd)) + day).pretty \
        ( '%s%s%s'
        % ( [';', ''][direction == '+']
          , ymd
          , [';', ''][direction != '+']
          )
        )
# end def next_search_date

def period_is_weekly (period) :
    return period.weekly and not period.months
# end def period_is_weekly

def overtime_period_week (db) :
    try :
        db = db._db
    except AttributeError :
        pass
    ids = db.overtime_period.filter (None, dict (weekly = True, months = 0))
    assert (len (ids) <= 1)
    if ids :
        return db.overtime_period.getnode (ids [0])
    return None
# end def overtime_period_week

class Fake_Period (object) :
    """ Fake period class, needed to emulate a Class overtime_period
        database object for regression testing and start/end of period
        computations.
    """
    def __init__ (self, weekly, months) :
        self.weekly = weekly
        self.months = months
    # end __init__
# end class Fake_Period

period_month = Fake_Period (0, 1)
period_week  = Fake_Period (1, 0)

def _period_start_end (date, period) :
    """ Compute start of given period from date and indication if given
        date ends the period
        >>> P = Fake_Period
        >>> _period_start_end (Date ('2007-01-07'), P (1, 0))
        (<Date 2007-01-01.00:00:00.000>, True)
        >>> _period_start_end (Date ('2007-01-01'), P (1, 0))
        (<Date 2007-01-01.00:00:00.000>, False)
        >>> _period_start_end (Date ('2006-01-01'), P (1, 0))
        (<Date 2005-12-26.00:00:00.000>, True)
        >>> _period_start_end (Date ('2007-01-31'), P (0, 1))
        (<Date 2007-01-01.00:00:00.000>, True)
        >>> _period_start_end (Date ('2007-01-07'), P (1, 1))
        (<Date 2007-01-01.00:00:00.000>, False)
        >>> _period_start_end (Date ('2007-02-28'), P (0, 2))
        (<Date 2007-01-01.00:00:00.000>, True)
        >>> _period_start_end (Date ('2007-02-07'), P (1, 2))
        (<Date 2007-01-01.00:00:00.000>, False)
        >>> _period_start_end (Date ('2007-03-31'), P (0, 3))
        (<Date 2007-01-01.00:00:00.000>, True)
        >>> _period_start_end (Date ('2007-03-07'), P (1, 3))
        (<Date 2007-01-01.00:00:00.000>, False)
        >>> _period_start_end (Date ('2007-04-30'), P (0, 4))
        (<Date 2007-01-01.00:00:00.000>, True)
        >>> _period_start_end (Date ('2007-04-07'), P (1, 4))
        (<Date 2007-01-01.00:00:00.000>, False)
        >>> _period_start_end (Date ('2007-06-30'), P (0, 6))
        (<Date 2007-01-01.00:00:00.000>, True)
        >>> _period_start_end (Date ('2007-06-07'), P (1, 6))
        (<Date 2007-01-01.00:00:00.000>, False)
        >>> _period_start_end (Date ('2007-12-31'), P (0, 12))
        (<Date 2007-01-01.00:00:00.000>, True)
        >>> _period_start_end (Date ('2007-12-07'), P (1, 12))
        (<Date 2007-01-01.00:00:00.000>, False)
        >>> _period_start_end (Date ('2010-04-17'), P (1, 12))
        (<Date 2010-01-01.00:00:00.000>, False)
        >>> _period_start_end (Date ('2010-05-02'), P (1, 12))
        (<Date 2010-01-01.00:00:00.000>, False)
        >>> _period_start_end (Date ('2013-02-08'), P (0, 1))
        (<Date 2013-02-01.00:00:00.000>, False)
    """
    if period_is_weekly (period) :
        start, end = week_from_date (date)
        return start, date == end
    elif period.months == 12 :
        return start_of_year (date), date.month == 12 and date.day == 31
    d = start_of_month (date)
    while (d.month - 1) % period.months :
        d = start_of_month (d - day)
    return d, end_of_period (date, period) == Date (date.pretty (ymd))
# end def _period_start_end

def start_of_period (date, period) :
    """ Compute start of given period from date """
    return _period_start_end (date, period) [0]
# end def start_of_period

def freeze_date (date, period) :
    """ Return end of last freeze period before or at date """
    if not date :
        date = Date ('.')
    try :
        date = Date (date._value)
    except AttributeError :
        pass
    start, is_end = _period_start_end (date, period)
    if is_end :
        return Date (date.pretty (ymd))
    return start - day
# end def freeze_date

def week_freeze_date (date) :
    return freeze_date (date, period_week)
# end def week_freeze_date

def end_of_period (date, period) :
    """ Compute end of given period from date
        >>> P = Fake_Period
        >>> end_of_period (Date ('2007-01-07'), P (1, 0))
        <Date 2007-01-07.00:00:00.000>
        >>> end_of_period (Date ('2007-01-01'), P (1, 0))
        <Date 2007-01-07.00:00:00.000>
        >>> end_of_period (Date ('2006-01-01'), P (1, 0))
        <Date 2006-01-01.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (0, 1))
        <Date 2007-01-31.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (1, 1))
        <Date 2007-01-31.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (0, 2))
        <Date 2007-02-28.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (1, 2))
        <Date 2007-02-28.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (0, 3))
        <Date 2007-03-31.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (1, 3))
        <Date 2007-03-31.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (0, 4))
        <Date 2007-04-30.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (1, 4))
        <Date 2007-04-30.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (0, 6))
        <Date 2007-06-30.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (1, 6))
        <Date 2007-06-30.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (0, 12))
        <Date 2007-12-31.00:00:00.000>
        >>> end_of_period (Date ('2007-01-07'), P (1, 12))
        <Date 2007-12-31.00:00:00.000>
        >>> end_of_period (Date ('2010-04-26'), P (1, 12))
        <Date 2010-12-31.00:00:00.000>
        >>> end_of_period (Date ('2010-05-02'), P (1, 12))
        <Date 2010-12-31.00:00:00.000>
    """
    if period_is_weekly (period) :
        start, end = week_from_date (date)
        return end
    if period.months == 12 :
        return Date ('%s-12-31' % date.year)
    d = end_of_month (date)
    while d.month % period.months :
        d = end_of_month (d + day)
    return d
# end def end_of_period

def auto_retire (db, cl, nodeid, new_values, multilink_attr) :
    """ Retire all nodes which are no longer linked to by the new
        version of a multilink
    """
    if multilink_attr not in new_values :
        return
    new = dict.fromkeys (new_values [multilink_attr])
    old = dict.fromkeys (cl.get (nodeid, multilink_attr))
    cls = db.classes [cl.properties [multilink_attr].classname]
    for o in old.iterkeys () :
        if o not in new :
            cls.retire (o)
# end def auto_retire

def require_attributes (_, cl, nodeid, new_values, * attributes) :
    for a in attributes :
        if a not in cl.properties :
            continue
        attr = _ (a)
        if not nodeid and (a not in new_values or new_values [a] is None) :
            raise Reject, _ (''"%(attr)s must be specified") % locals ()
        elif nodeid and new_values.get (a, cl.get (nodeid, a)) is None :
            raise Reject, _ (''"%(attr)s must not be empty") % locals ()
# end def require_attributes

def check_attribute_lines (_, new_values, name, length) :
    attr = new_values.get (name)
    if name in new_values and attr is not None :
        l = len (attr.split ('\n'))
        if l > length :
            atname = _ (name)
            raise Reject, _ \
                (''"%(atname)s must not exceed %(length)s lines") % locals ()
# end def check_attribute_lines

def reject_attributes (_, new_values, * attributes) :
    for a in attributes :
        attr = _ (a)
        if a in new_values :
            raise Reject, _ (''"%(attr)s must not be specified") % locals ()
# end def reject_attributes

def default_status (new_values, status_class, valid = True, status = 'status') :
    """ Set a default status for a new item if none is given.

        assumes that a status class has a "valid" attribute and selects
        the first status that is equal to the given valid parameter.
    """
    if status not in new_values :
        stati = status_class.filter (None, {'valid' : valid})
        assert (stati)
        new_values [status] = stati [0]
# end def default_status

def changed_values (old_values, cl, id) :
    """ In a reactor compute the changed values -- old_values may
        contain attributes that didn't change.
        We ignore system attributes creation, creator, activity, actor
    """
    exc = dict.fromkeys ('creation creator activity actor'.split ())
    changed = []
    for k in old_values.iterkeys () :
        if k not in exc and old_values [k] != cl.get (id, k) :
            changed.append (k)
    return changed
# end def changed_values

def lookalike_computation (db, cl, nodeid, new_values) :
    for field in cl.properties.iterkeys () :
        if  (    'lookalike_' + field in cl.properties
            and  (  field in new_values
                 or nodeid and 'lookalike_' + field in new_values
                 ) 
            ) :
            nv = new_values.get (field)
            if field not in new_values :
                nv = cl.get (nodeid, field)
            if nv is None :
                new_values ['lookalike_' + field] = None
            else :
                new_values ['lookalike_' + field] = translate (nv)
# end def lookalike_computation

def persons_for_adr (db, nodeid) :
    return db.person.filter (None, dict (address = nodeid))
# end def adr_for_person

def tracker_languages (client, db) :
    try :
        db = db._db
    except AttributeError :
        pass
    language = client.language or db.config["TRACKER_LANGUAGE"]
    if not isinstance (language, list) :
        language = [language]
    return language
# end def tracker_languages

def get_num_locale (client, db) :
    for l in tracker_languages (client, db) :
        try :
            locale.setlocale (locale.LC_NUMERIC, locale.normalize (l))
            break
        except locale.Error :
            pass
    return locale
# end def get_num_locale

def update_emails (db, uid, verbose = False) :
    """ Update address and alternate_addresses of a user from the
        contacts of this user. Used by changed_contact reactor and can
        be used in scripts to sync contacts.
    """
    user   = db.user.getnode (uid)
    emails = []
    o_alt  = {}
    if user.alternate_addresses :
        o_alt  = dict.fromkeys \
            (x.strip () for x in user.alternate_addresses.split ('\n'))
    email = db.uc_type.lookup ('Email')
    for c in user.contacts :
        if db.user_contact.get (c, 'contact_type') == email :
            emails.append (db.user_contact.getnode (c))
    alt = {}
    adr = None
    for n, e in enumerate (sorted (emails, key = lambda x : x.order)) :
        if n :
            alt [e.contact] = None
        else :
            adr = e.contact
    d = {}
    if adr != user.address :
        d ['address'] = adr
    if alt != o_alt :
        d ['alternate_addresses'] = '\n'.join (alt)
    if d :
        if verbose :
            print "Updating %s %s" \
                % ( user.username
                  , ' '.join (': '.join ((k, v)) for k, v in d.iteritems ())
                  )
        db.user.set (user.id, ** d)
# end def update_emails

class Size_Limit (object) :
    def __init__ (self, db, config) :
        try :
            db = db._db
        except AttributeError :
            pass
        try :
            limit = getattr (db.config.ext, config)
        except AttributeError :
            limit = None
        if isinstance (limit, str) :
            if limit.endswith ('k') or limit.endswith ('K') :
                limit = int (limit [:-1]) * 1024
            elif limit.endswith ('M') :
                limit = int (limit [:-1]) * 1024 * 1024
            else :
                limit = int (limit)
        self.limit = limit
    # end def __init__

    def __str__ (self) :
        if self.limit is None :
            return 'No limit'
        if self.limit % (1024 * 1024) == 0 :
            return "%sM" % (self.limit / (1024 * 1024))
        if self.limit % 1024 == 0 :
            return "%sk" % (self.limit / 1024)
        return "%s" % self.limit
    # end def __str__
    __repr__ = __str__

    def __nonzero__ (self) :
        return bool (self.limit)
    # end def __nonzero__

# end class Size_Limit

def fix_date (date) :
    if date :
        return Date (date.pretty (ymd))
    return date
# end fix_date

def ydays (ydate) :
    """ Return number of days in given year, parameter is either a
        roundup.date.Date object or an integer year.

    >>> ydays (2000)
    366
    >>> ydays (2001)
    365
    >>> ydays (2004)
    366
    >>> ydays (2016)
    366
    >>> ydays (Date ('2016-01-01'))
    366
    >>> ydays (Date ('2016-12-01'))
    366
    >>> ydays (Date ('2016-12-31'))
    366
    """
    if isinstance (ydate, int) :
        ydate = datetime.date (ydate, 12, 31)
    else :
        ydate = datetime.date (ydate.year, 12, 31)
    return ydate.timetuple().tm_yday
# end def ydays

default_attributes = dict \
    ( issue   =
        ('area category confidential deadline doc_issue_status'
         ' earliest_start effective_prio external_users inherit_ext'
         ' keywords kind nosy numeric_effort part_of priority release'
         ' responsible severity title'
        ).split ()
    , support =
        ('bcc category cc classification confidential customer'
         ' emails external_ref lot nosy number_effected numeric_effort'
         ' prio prodcat product related_issues related_support'
         ' release responsible serial_number title type warranty'
        ).split ()
    , purchase_request =
        ('continuous_obligation contract_term delivery_deadline'
         ' department frame_purchase organisation part_of_budget'
         ' purchase_type renegotiations requester safety_critical'
         ' sap_cc termination_date terms_conditions'
         ' time_project title pr_currency'
        ).split ()
    )

def copy_url (context, attributes = None) :
    """ Create URL for copying (most attributes of) an item """
    cls = context._classname
    url = ['%(cls)s?:template=item' % locals ()]
    atr = attributes or default_attributes [cls]
    for a in atr :
        val = ''
        if isinstance (context [a], MultilinkHTMLProperty) :
            if context [a] :
                val = ','.join (p.id for p in context [a])
        elif isinstance (context [a], LinkHTMLProperty) :
            if context [a] and not context [a].is_retired () :
                val = context [a].id
        else :
            val = str (context [a])
        url.append ('%s=%s' % (a, urlquote (val)))
    if cls == 'purchase_request' and atr == default_attributes [cls] :
        atrs = \
            ( 'index', 'supplier', 'description', 'offer_number'
            , 'units', 'price_per_unit', 'vat', 'sap_cc', 'time_project'
            , 'purchase_type'
            )
        n = -1
        for n, ofr in enumerate (context ['offer_items']) :
            for a in atrs :
                val = None
                if isinstance (ofr [a], MultilinkHTMLProperty) :
                    if ofr [a] :
                        val = ','.join (p.id for p in ofr [a])
                elif isinstance (ofr [a], LinkHTMLProperty) :
                    if ofr [a] and not ofr [a].is_retired () :
                        val = ofr [a].id
                else :
                    val = str (ofr [a])
                if val is not None :
                    url.append \
                        ( 'pr_offer_item-%s@%s=%s'
                        % (n+1, a, urlquote (val))
                        )
        if n >= 0 :
            url.append ('offer_list_length=%s' % (n + 1))
    return '&'.join (url)
# end def copy_url

def copy_js (linkid = 'copyme') :
    """ Create Javascript for use e.g. in onClick to copy
        (most attributes of) an item
    """
    code = "document.getElementById ('%(linkid)s').click ();" % locals ()
    return code
# end def copy_js

def role_list (roles) :
    if not roles :
        return []
    return [x.lower ().strip () for x in roles.split (',')]
# end def role_list

def check_roles (db, cl, nodeid, new_values, rname = 'roles') :
    if rname in new_values :
        roles = new_values [rname]
        if roles :
            roles = roles.strip ()
        if roles :
            roles = role_list (roles)
            for r in roles :
                if not db.security.role.has_key (r) :
                    raise Reject ('Role "%s" does not exist' % r)
# end def check_roles

def get_default_it_prio (db) :
    if 'default' in db.it_prio.properties :
        default = db.it_prio.filter (None, dict (default = True))
        if default :
            return default [0]
    try :
        return db.it_prio.lookup ('assistance')
    except KeyError :
        pass
    return None
# end def get_default_it_prio

def filter_status_transitions (context, *invalid_states) :
    # there was a check for closing -- we leave the logic in
    may_close = True
    classname = context.status._prop.classname
    cls       = context.status._db.getclass (classname)
    invalid   = [cls.lookup (x) for x in invalid_states]
    if context.status :
        if 'status_transition' in context._db.classes :
            if context.kind and context.kind.simple :
                values = \
                    [t.target.id for t in context.status.simple_transitions
                     if t.target.name != 'closed' or may_close
                    ]
            else :
                values = \
                    [t.target.id for t in context.status.transitions
                     if t.target.name != 'closed' or may_close
                    ]
        else :
            values = \
                [t.id for t in context.status.transitions
                 if t.name != 'closed' or may_close
                ]
        values = [v for v in values if v not in invalid]
        return {'id' : values}
    return {}
# end def filter_status_transitions

### __END__
