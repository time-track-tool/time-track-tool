#! /usr/bin/python
# Copyright (C) 2006-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    public_holiday
#
# Purpose
#    Detectors for 'public_holiday'
#

from roundup.exceptions import Reject
from common    import require_attributes, pretty_range
from vacation  import try_create_public_holiday, fix_vacation

def check_public_holiday (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    for i in 'name', 'date', 'locations' :
        if i in new_values and not new_values [i] :
            raise Reject ("%(attr)s may not be deleted" % {'attr' : _ (i)})
# end def check_public_holiday

def new_public_holiday (db, cl, nodeid, new_values) :
    require_attributes \
        (db.i18n.gettext, cl, nodeid, new_values, 'name', 'date', 'locations')
# end def new_public_holiday

def fix_daily_recs (db, cl, nodeid, old_values) :
    """ If there are existing daily records for this public holiday
        correct the booked public holiday time
    """
    ph = cl.getnode (nodeid)
    dt = pretty_range (ph.date, ph.date)
    drs = db.daily_record.filter (None, dict (date = dt))
    leave = db.daily_record_status.lookup ('leave')
    for id in drs :
        dr = db.daily_record.getnode (id)
        try_create_public_holiday (db, id, dr.date, dr.user)
        # If this is a leave record, we also fix the vacation on that
        # date: The amount of vacation hours will have changed.
        if dr.status == leave :
            fix_vacation (db, dr.user, dr.date, dr.date)
# end def fix_daily_recs

def init (db) :
    if 'public_holiday' not in db.classes :
        return
    db.public_holiday.audit  ("create", new_public_holiday)
    db.public_holiday.audit  ("set",    check_public_holiday)
    db.public_holiday.react  ("create", fix_daily_recs)
    db.public_holiday.react  ("set",    fix_daily_recs)
# end def init

