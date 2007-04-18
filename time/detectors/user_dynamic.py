#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    user_dynamic
#
# Purpose
#    Detectors for 'user_dynamic'
#

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

from freeze       import frozen
from user_dynamic import last_user_dynamic, day
from common       import require_attributes

def check_ranges (cl, nodeid, user, valid_from, valid_to) :
    if valid_to :
        valid_to.hour   = valid_to.minute   = valid_to.second   = 0
    valid_from.hour     = valid_from.minute = valid_from.second = 0
    if valid_to and valid_from >= valid_to :
        raise Reject, \
            "valid_from (%(valid_from)s) must be > valid_to (%(valid_to)s)" \
            % locals ()
    dynrecs    = cl.find (user = user)
    empty_seen = False
    for dr in dynrecs :
        if dr == nodeid :
            continue
        r = cl.getnode (dr)
        rvalid_from, rvalid_to = (r.valid_from, r.valid_to)
        if not r.valid_to :
            assert (not empty_seen)
            empty_seen = True
            if (   valid_to
               and valid_from <= rvalid_from
               and valid_to   >  rvalid_from
               ) or (not valid_to and valid_from <= rvalid_from) :
                raise Reject, \
                    ( "%(valid_from)s;%(valid_to)s overlaps with "
                      "%(rvalid_from)s;"
                    % locals ()
                    )
        else :
            if not (valid_from >= rvalid_to or valid_to <= rvalid_from) :
                raise Reject, \
                    ( _ ("%(valid_from)s;%(valid_to)s overlaps with "
                         "%(rvalid_from)s;%(rvalid_to)s"
                        )
                    % locals ()
                    )
    return valid_from, valid_to
# end def check_ranges

def check_vacation (attr, new_values) :
    if attr in new_values :
        vacation = new_values [attr]
        if vacation is None :
            return
        if vacation <= 0 and attr != 'vacation_remaining' :
            raise Reject, \
                _ ( "%(attr)s must be positive or empty") % locals ()
# end def check_vacation

def check_overtime_parameters (db, cl, nodeid, new_values) :
    pass
# end def check_overtime_parameters

def check_user_dynamic (db, cl, nodeid, new_values) :
    for i in 'user', :
        if i in new_values and cl.get (nodeid, i) :
            raise Reject, "%(attr)s may not be changed" % {'attr' : _ (i)}
    for i in 'valid_from', 'org_location', 'department' :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be empty" % {'attr' : _ (i)}
    user     = new_values.get ('user',         cl.get (nodeid, 'user'))
    old_from = cl.get (nodeid, 'valid_from')
    val_from = new_values.get ('valid_from',   old_from)
    val_to   = new_values.get ('valid_to',     cl.get (nodeid, 'valid_to'))
    olo      = new_values.get ('org_location', cl.get (nodeid, 'org_location'))
    dept     = new_values.get ('department',   cl.get (nodeid, 'department'))
    # Note: The valid_to date is *not* part of the validity interval of
    # the user_dynamic record. So when checking for frozen status we
    # can allow exactly the valid_to date.
    if  (   frozen (db, user, old_from)
        and (  new_values.keys () != ['valid_to']
            or not val_to
            or frozen (db, user, val_to)
            )
        ) :
        #print user, val_to, day, val_to - day, new_values.keys ()
        raise Reject, _ ("Frozen: %(old_from)s") % locals ()
    last = last_user_dynamic (db, user)
    if  (   ('org_location' in new_values or 'department' in new_values)
        and (not val_to or last.id == nodeid or last.valid_from < val_from)
        ) :
        db.user.set (user, org_location = olo, department = dept)
    if 'valid_from' in new_values or 'valid_to' in new_values :
        new_values ['valid_from'], new_values ['valid_to'] = \
            check_ranges (cl, nodeid, user, val_from, val_to)
    check_overtime_parameters (db, cl, nodeid, new_values)
    for i in 'vacation_yearly', 'vacation_remaining' :
        check_vacation (i, new_values)
# end def check_user_dynamic


def new_user_dynamic (db, cl, nodeid, new_values) :
    require_attributes \
        ( _
        , cl
        , nodeid
        , new_values
        , 'user'
        , 'valid_from'
        , 'org_location'
        , 'department'
        )
    user       = new_values ['user']
    valid_from = new_values ['valid_from']
    valid_to   = new_values.get ('valid_to', None)
    olo        = new_values ['org_location']
    dept       = new_values ['department']
    if frozen (db, user, valid_from) :
        raise Reject, _ ("Frozen: %(valid_from)s") % locals ()
    last = last_user_dynamic (db, user)
    if not valid_to or not last or last.valid_from < valid_from :
        db.user.set (user, org_location = olo, department = dept)
    if 'durations_allowed' not in new_values :
        new_values ['durations_allowed'] = False
    new_values ['valid_from'], new_values ['valid_to'] = \
        check_ranges (cl, nodeid, user, valid_from, valid_to)
    for i in 'vacation_yearly', 'vacation_remaining' :
        check_vacation (i, new_values)
    check_overtime_parameters (db, cl, nodeid, new_values)
    # FIXME: Todo: compute remaining vacation from old dyn record and
    # all time tracking data for this user.
    # No: if vacation data is missing look up backwards until a vacation
    # record is found
# end def new_user_dynamic

def close_existing (db, cl, nodeid, old_values) :
    """ Check if there is already a user_dynamic record with no valid_to
        date. If there is one and the current record created also has no
        valid_to date, we set the valid_to of the found record to the
        valid_from of the current record.
    """
    current = cl.getnode (nodeid)
    dynrecs = cl.find (user = current.user)
    for dr in dynrecs :
        if dr == nodeid :
            continue
        r = cl.getnode (dr)
        if not r.valid_to and current.valid_from >= r.valid_from :
            cl.set (dr, valid_to = current.valid_from)
            break
# end def close_existing

def init (db) :
    if 'user_dynamic' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.user_dynamic.audit  ("create", new_user_dynamic)
    db.user_dynamic.audit  ("set",    check_user_dynamic)
    db.user_dynamic.react  ("create", close_existing)
# end def init

### __END__ user_dynamic
