#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    daily_record_freeze
#
# Purpose
#    Detectors for daily_record_freeze entries
#
#--
#

from roundup                        import roundupdb, hyperdb
from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation
from roundup.date                   import Date, Interval

from freeze                         import frozen
from user_dynamic                   import get_user_dynamic, last_user_dynamic
from user_dynamic                   import compute_balance

day  = Interval ('1d')

def check_editable (db, cl, nodeid, new_values, date = None) :
    if not date :
        date = new_values.get ('date') or cl.get (nodeid, 'date')
    user = new_values.get ('user') or cl.get (nodeid, 'user')
    fr = frozen (db, user, date)
    if cl == db.daily_record_freeze :
        fr = [f for f in fr if f != nodeid]
    if fr :
        raise Reject, _ ("Already frozen: %(date)s") % locals ()
    if not get_user_dynamic (db, user, date) :
        raise Reject, _ ("No dyn. user rec for %(user)s %(date)s") % locals ()
# end def check_editable

def check_thawed_records (db, user, date) :
    cl     = db.daily_record_freeze
    before = (date - day).pretty (';%Y-%m-%d')
    thawed = cl.filter (None, dict (user = user, date = before, frozen = False))
    if thawed :
        raise Reject, \
            _ ("Thawed freeze records before %(date)s") % locals ()
# end def check_thawed_records

periods = ['week', 'month', 'year']

def new_freeze_record (db, cl, nodeid, new_values) :
    for i in ('date', 'user') :
        if i not in new_values :
            raise Reject, _ ("%(attr)s must be set") % {'attr' : _ (i)}
    date = new_values ['date']
    user = new_values ['user']
    if date >= Date ('.-10d') :
        raise Reject, _ ("Freezing only for dates >= 10 days in the past")
    date.hour = date.minute = date.second = 0
    if 'frozen' not in new_values :
        new_values ['frozen'] = True
    if new_values ['frozen'] :
        check_thawed_records (db, user, date)
    check_editable (db, cl, nodeid, new_values)
    for p in periods :
        attr = p + '_balance'
        if attr not in new_values or new_values [attr] is None :
            new_values [attr] = compute_balance \
                (db, user, date, p, not_after = True)
# end def new_freeze_record

def new_overtime (db, cl, nodeid, new_values) :
    for i in ('date', 'user', 'value') :
        if i not in new_values :
            raise Reject, _ ("%(attr)s must be set") % {'attr' : _ (i)}
    date = new_values ['date']
    date.hour = date.minute = date.second = 0
    check_editable (db, cl, nodeid, new_values)
# end def new_freeze_record

def check_freeze_record (db, cl, nodeid, new_values) :
    """Check that edits of a freeze record are ok.
       
       - editable
       - no thawed records before current record

       This also has to handle the case that while thawed the daily
       record was edited and we don't have a valid daily_record any
       longer. In that case we change the date to the last valid
       daily_record date. If that date is already frozen we retire the
       current record.
    """
    for i in ('date', 'user') :
        if i in new_values :
            raise Reject, _ ("%(attr)s must not be changed") % {'attr' : _ (i)}
    date = cl.get (nodeid, 'date')
    user = cl.get (nodeid, 'user')
    dyn  = get_user_dynamic (db, user, date)
    if not dyn :
        dyn    = last_user_dynamic (db, user, date = date)
        prev   = cl.filter \
            ( None
            , dict (user = user, date = date.pretty (';%Y-%m-%d'))
            , group = [('-', 'date')]
            )
        prev   = [p for p in prev if p != nodeid]
        if prev :
            prev = db.daily_record_freeze.getnode (prev [0])
        assert (dyn.valid_to)
        # already frozen??
        if prev and prev.date >= dyn.valid_to - day :
            for k in new_values.keys () :
                del new_values [k]
            cl.retire (nodeid)
            return
        date = dyn.valid_to - day
        new_values ['date'] = date
    check_editable (db, cl, nodeid, new_values, date = date)
    old_frozen = cl.get (nodeid, 'frozen')
    new_frozen = new_values.get ('frozen', old_frozen)
    freezing   = new_frozen != old_frozen and new_frozen
    if freezing :
        check_thawed_records (db, user, date)
    for p in periods :
        attr = p + '_balance'
        if  freezing :
            new_values [attr] = compute_balance \
                (db, user, date, p, not_after = True)
        else :
            new_values [attr] = None
# end def check_freeze_record

def check_overtime (db, cl, nodeid, new_values) :
    for i in ('user',) :
        if i in new_values :
            raise Reject, _ ("%(attr)s must not be changed") % {'attr' : _ (i)}
    for i in ('date', 'value') :
        if i in new_values and new_values [i] is None :
            raise Reject, _ ("%(attr)s must remain filled") % {'attr' : _ (i)}
    check_editable (db, cl, nodeid, new_values)
# end def check_overtime

def init (db) :
    if 'daily_record_freeze' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.daily_record_freeze.audit ("create", new_freeze_record)
    db.daily_record_freeze.audit ("set",    check_freeze_record)
    db.overtime_correction.audit ("create", new_overtime)
    db.overtime_correction.audit ("set",    check_overtime)
# end def init
