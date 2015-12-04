# -*- coding: iso-8859-1 -*-
# Copyright (C) 2015 Ralf Schlatterbeck. All rights reserved
# Reichergasse 131, A-3411 Weidling
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

import os
import common
from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

_ = lambda x : x

def retire_check (db, cl, nodeid, old_values) :
    item = cl.getnode (nodeid)
    if item.first_day > item.last_day :
        cl.retire (nodeid)
# end def retire_check

def check_params (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'first_day', 'last_day', 'user')
# end def check_params

def no_user_change (db, cl, nodeid, new_values) :
    if 'user' in new_values :
        user = _ ("user")
        raise Reject (_ ("%(user)s may not be changed") % locals ())
# end def no_user_change

def no_overlap (db, cl, nodeid, new_values) :
    ymd = common.ymd
    if 'first_day' in new_values or 'last_day' in new_values :
        fd = new_values.get ('first_day')
        ld = new_values.get ('last_day')
        u  = new_values.get ('user')
        assert fd and ld and u or nodeid
        if not fd :
            fd = cl.get (nodeid, 'first_day')
        if not ld :
            ld = cl.get (nodeid, 'last_day')
        if not u :
            u = cl.get (nodeid, 'user')
        dt = common.pretty_range (fd, ld)
        d  = dict (user = u)
        fl = dict \
            ( first_day = fd.pretty (';%Y-%m-%d')
            , last_day = ld.pretty ('%Y-%m-%d;')
            )
        for d in (dict (first_day = dt), dict (last_day = dt), fl) :
            results = cl.filter (None, dict (d, user = u))
            for r in results :
                if r == nodeid :
                    continue
                item = cl.getnode (r)
                raise Reject \
                    (_ ("Overlap with existing absence: %s-%s")
                    % (item.first_day.pretty (ymd), item.last_day.pretty (ymd))
                    )
# end def no_overlap

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    if 'absence' in db.classes :
        db.absence.audit         ("create", check_params)
        db.absence.audit         ("set",    check_params)
        db.absence.audit         ("create", no_overlap, priority = 120)
        db.absence.audit         ("set",    no_overlap, priority = 120)
        db.absence.audit         ("set",    no_user_change)
        db.absence.react         ("set",    retire_check)
# end def init
