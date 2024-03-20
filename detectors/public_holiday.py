#!/usr/bin/python
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
from common    import require_attributes, pretty_range, ymd
from vacation  import try_create_public_holiday, fix_vacation

def _loc_org_check (db, d):
    _ = db.i18n.gettext
    loc = _ ('locations')
    olo = _ ('org_location')
    if not d ['locations'] and not d ['org_location']:
        raise Reject ('One of %(loc)s or %(olo)s must not be empty' % locals ())
    if d ['locations'] and d ['org_location']:
        raise Reject \
            ('Only one of %(loc)s or %(olo)s may be filled in' % locals ())
# end def _loc_org_check

def check_public_holiday (db, cl, nodeid, new_values):
    _ = db.i18n.gettext
    for i in 'name', 'date':
        if i in new_values and not new_values [i]:
            raise Reject ("%(attr)s may not be deleted" % {'attr': _ (i)})
    d = {}
    for i in 'locations', 'org_location':
        d [i] = new_values.get (i, cl.get (nodeid, i))
    _loc_org_check (db, d)
# end def check_public_holiday

def new_public_holiday (db, cl, nodeid, new_values):
    require_attributes \
        (db.i18n.gettext, cl, nodeid, new_values, 'name', 'date')
    d = {}
    for i in 'locations', 'org_location':
        d [i] = new_values.get (i, None)
    _loc_org_check (db, d)
# end def new_public_holiday

def check_dupe_loc (db, cl, nodeid, new_values):
    _    = db.i18n.gettext
    date = new_values.get ('date')
    locs = new_values.get ('locations')
    olos = new_values.get ('org_location')
    if not date:
        assert nodeid
        date = cl.get (nodeid, 'date')
    if not locs and nodeid:
        locs = cl.get (nodeid, 'locations')
    if not olos and nodeid:
        olos = cl.get (nodeid, 'org_location')
    olos = set ()
    locs = set ()
    if locs:
        locs = set (locs)
    if olos:
        olos = set (olos)
    # Get all public holidays on that date
    dt  = date.pretty (ymd)
    phs = db.public_holiday.filter (None, dict (date = dt))
    for phid in phs:
        if phid == nodeid:
            continue
        ph  = db.public_holiday.getnode (phid)
        lo  = set (ph.locations)
        olo = set (ph.org_location)
        if not lo and olo:
            for ol in olo:
                lo.add (db.org_location.get (ol, 'location'))
        if not olo and lo:
            olo = db.org_location.filter (None, dict (location = lo))
        intersect = locs.intersection (lo)
        if intersect:
            iloc = ', '.join \
                ('"' + db.location.get (l, 'name') + '"' for l in intersect)
            raise Reject \
                (_ ('There already is a public holiday on %(dt)s for %(iloc)s')
                % locals ()
                )
        intersect = olos.intersection (olo)
        if intersect:
            iolo = ', '.join \
                ('"' + db.org_location.get (l, 'name') + '"' for l in intersect)
            raise Reject \
                (_ ('There already is a public holiday on %(dt)s for %(iolo)s')
                % locals ()
                )
# end def check_dupe_loc

def fix_daily_recs (db, cl, nodeid, old_values):
    """ If there are existing daily records for this public holiday
        correct the booked public holiday time
    """
    ph = cl.getnode (nodeid)
    dt = pretty_range (ph.date, ph.date)
    drs = db.daily_record.filter (None, dict (date = dt))
    leave = db.daily_record_status.lookup ('leave')
    for id in drs:
        dr = db.daily_record.getnode (id)
        try_create_public_holiday (db, id, dr.date, dr.user)
        # If this is a leave record, we also fix the vacation on that
        # date: The amount of vacation hours will have changed.
        if dr.status == leave:
            fix_vacation (db, dr.user, dr.date, dr.date)
# end def fix_daily_recs

def init (db):
    if 'public_holiday' not in db.classes:
        return
    db.public_holiday.audit  ("create", new_public_holiday)
    db.public_holiday.audit  ("set",    check_public_holiday)
    db.public_holiday.audit  ("create", check_dupe_loc, priority = 150)
    db.public_holiday.audit  ("set",    check_dupe_loc, priority = 150)
    db.public_holiday.react  ("create", fix_daily_recs)
    db.public_holiday.react  ("set",    fix_daily_recs)
# end def init

