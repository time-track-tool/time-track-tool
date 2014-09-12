#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2014 Dr. Ralf Schlatterbeck Open Source Consulting.
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

from   math import ceil
import common
import user_dynamic
import vacation
from   roundup.date import Date, Interval

def user_leave_submissions (db, context) :
    dt  = '%s;' % Date ('. - 14m').pretty (common.ymd)
    uid = db._db.getuid ()
    d   = dict (user = uid, first_day = dt)
    s   = [('+', 'first_day')]
    ls = db.leave_submission.filter (None, d, s)
    return ls
# end def user_leave_submissions

def approval_stati (db) :
    st  = ('submitted', 'cancel requested')
    st  = [db._db.leave_status.lookup (x) for x in st]
    return dict (status = st)
# end def approval_stati

def approve_leave_submissions (db, context) :
    uid = db._db.getuid ()
    d   = approval_stati (db)
    d ['user'] = db._db.user.find (supervisor = uid)
    ls  = db.leave_submission.filter (None, d)
    return ls
# end def approve_leave_submissions

def approve_leave_submissions_hr (db, context, request) :
    uid = db._db.getuid ()
    if not common.user_has_role (db._db, uid, 'HR-leave-approval') :
        return []
    d   = approval_stati (db)
    fs  = request.filterspec
    if 'status' in fs :
        new_stati = {}
        stati = dict.fromkeys (fs ['status'])
        for s in d ['status'] :
            if s in stati :
                new_stati [s] = 1
        d ['status'] = new_stati.keys ()
    for n in ('user', 'time_wp.project') :
        if n in fs :
            d [n] = fs [n]
    ls  = db.leave_submission.filter (None, d)
    ls  = [l for l in ls if l.user.id != uid]
    return ls
# end def approve_leave_submissions_hr

class Leave_Buttons (object) :
    user_buttons = dict \
        (( ('open',             ( ('submitted',        ""'Submit to %(sunick)s')
                                , ('cancelled',        ""'Cancel')
                                )
           )                   
         , ('submitted',        (('open',              ""'Edit again'), ))
         , ('accepted',         (('cancel requested',  ""'Request Cancel'), ))
        ))

    approve_buttons = dict \
        (( ('submitted',        ( ('accepted',         ""'Accept')
                                , ('declined',         ""'Decline')
                                )
           )
         , ('cancel requested', ( ('cancelled',        ""'Allow cancel')
                                , ('accepted',         ""'Decline cancel')
                                )
           )
        ))

    def __init__ (self, db) :
        self.htmldb    = db
        self.db        = db._db
        self.st_open   = self.db.leave_status.lookup ('open')
        self.st_subm   = self.db.leave_status.lookup ('submitted')
        self.st_accp   = self.db.leave_status.lookup ('accepted')
        self.st_cncr   = self.db.leave_status.lookup ('cancel requested')
        self.uid       = self.db.getuid ()
    # end def __init__

    def button (self, newstate, msg) :
        msg = msg % self.__dict__
        designator = self.ep_status.item.designator ()
        return \
            '''<input type="button" value="%(msg)s" onClick="
               if (submit_once ()) {
                   document.forms.edit_leave_submission
                       ['%(designator)s@status'].value = '%(newstate)s';
                   document.forms.edit_leave_submission.submit ();
               }">
            ''' % locals ()
    # end def button

    def generate (self, ep_status) :
        """ Buttons in leave submission forms (edit or approval)
        """
        ret            = []
        self.ep_status = ep_status
        self.user      = ep_status.item.user.id
        self.sunick    = str (ep_status.item.user.supervisor.nickname).upper ()
        stname         = str (ep_status.prop.name)
        db             = ep_status.item._db
        if (self.uid == self.user and stname in self.user_buttons) :
            for b in self.user_buttons [stname] :
                ret.append (self.button (*b))
        elif stname in self.approve_buttons and self.uid != self.user :
            tp        = ep_status.item.time_wp.project.id
            tp        = db.time_project.getnode (tp)
            first_day = ep_status.item.first_day._value
            last_day  = ep_status.item.last_day._value
            dyn       = user_dynamic.get_user_dynamic (db, self.user, last_day)
            ctype     = dyn.contract_type
            need_hr   = vacation.need_hr_approval \
                (db, tp, self.user, ctype, first_day, last_day)
            if  (  (    self.uid in common.clearance_by (self.db, self.user)
                   and not need_hr
                   )
                or common.user_has_role (self.db, self.uid, 'HR-leave-approval')
                ) :
                for b in self.approve_buttons [stname] :
                    ret.append (self.button (*b))
        if ret :
            ret.append \
                ( '<input type="hidden" name="%s@status" value=%s>'
                % (ep_status.item.designator (), stname)
                )
        return ''.join (ret)
    # end def generate
# end class Leave_Buttons

def remaining_until (db) :
    db  = db._db
    now = Date ('.')
    uid = db.getuid ()
    dyn = user_dynamic.get_user_dynamic (db, uid, now)
    return vacation.next_yearly_vacation_date \
        (db, uid, dyn.contract_type, now) - common.day
# end def remaining_until

def remaining_vacation (db, user, date) :
    return ceil (vacation.remaining_vacation (db, user, date = date) * 2) / 2.
# end def remaining_vacation

def consolidated_vacation (db, user, date) :
    return ceil \
        (vacation.consolidated_vacation (db, user, date = date) * 2) / 2.
# end def remaining_vacation

def _get_ctype (db, user, start, end) :
    now = Date ('.')
    if start <= now <= end :
        dyn = user_dynamic.get_user_dynamic (db, user, now)
    else :
        dyn = user_dynamic.get_user_dynamic (db, user, start)
    return dyn.contract_type
# end def _get_ctype

def _get_stati (db, statusname) :
    st  = [db.leave_status.lookup (statusname)]
    if statusname == 'accepted' :
        st.append (db.leave_status.lookup ('cancel requested'))
    return st
# end def _get_stati

def vacation_with_status (db, user, start, end, statusname) :
    stati = _get_stati (db, statusname)
    ctype = _get_ctype (db, user, start, end)
    return vacation.vacation_submission_days \
        (db, user, ctype, start, end, * stati)
# end def vacation_with_status

def flexitime_with_status (db, user, start, end, statusname) :
    stati = _get_stati (db, statusname)
    ctype = _get_ctype (db, user, start, end)
    return vacation.flexitime_submission_days \
        (db, user, ctype, start, end, * stati)
# end def flexitime_with_status

def init (instance) :
    reg = instance.registerUtil
    reg ('valid_wps',                    vacation.valid_wps)
    reg ('valid_leave_wps',              vacation.valid_leave_wps)
    reg ('valid_leave_projects',         vacation.valid_leave_projects)
    reg ('leave_days',                   vacation.leave_days)
    reg ('user_leave_submissions',       user_leave_submissions)
    reg ('approve_leave_submissions',    approve_leave_submissions)
    reg ('approve_leave_submissions_hr', approve_leave_submissions_hr)
    reg ('Leave_Buttons',                Leave_Buttons)
    reg ('remaining_until',              remaining_until)
    reg ('remaining_vacation',           remaining_vacation)
    reg ('consolidated_vacation',        consolidated_vacation)
    reg ('vacation_with_status',         vacation_with_status)
    reg ('flexitime_with_status',        flexitime_with_status)
    reg ('vacation_time_sum',            vacation.vacation_time_sum)
    reg ('year',                         Interval ('1y'))
    reg ('day',                          common.day)
