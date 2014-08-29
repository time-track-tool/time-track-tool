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

import common
import vacation
from   roundup.date import Date

def user_leave_submissions (db, context) :
    dt  = '%s;' % Date ('. - 14m').pretty (common.ymd)
    uid = db._db.getuid ()
    ls = db.leave_submission.filter (None, dict (user = uid, first_day = dt))
    return ls
# end def user_leave_submissions

def approve_leave_submissions (db, context) :
    uid = db._db.getuid ()
    st  = ('submitted', 'cancel requested')
    st  = [db._db.leave_status.lookup (x) for x in st]
    d   = dict (status = st)
    if not common.user_has_role (db._db, uid, 'HR-leave-approval') :
        d ['user'] = db._db.user.find (supervisor = uid)
    ls  = db.leave_submission.filter (None, d)
    return ls
# end def approve_leave_submissions

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
        if (self.uid == self.user and stname in self.user_buttons) :
            for b in self.user_buttons [stname] :
                ret.append (self.button (*b))
        elif (  self.uid in common.clearance_by (self.db, self.user)
             or common.user_has_role (self.db, self.uid, 'HR-leave-approval')
             ) and stname in self.approve_buttons :
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

def init (instance) :
    reg = instance.registerUtil
    reg ('valid_wps',                 vacation.valid_wps)
    reg ('valid_leave_wps',           vacation.valid_leave_wps)
    reg ('valid_leave_projects',      vacation.valid_leave_projects)
    reg ('leave_days',                vacation.leave_days)
    reg ('user_leave_submissions',    user_leave_submissions)
    reg ('approve_leave_submissions', approve_leave_submissions)
    reg ('Leave_Buttons',             Leave_Buttons)
