#! /usr/bin/python
# Copyright (C) 2023 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    o_permission
#
# Purpose
#    Routines for handling permissions bound to org/location
#

from roundup.date import Date
import user_dynamic

def get_allowed_olo (db, uid):
    """ Return a set of allowed org location ids for that user """
    assert 'org_location' in db.o_permission.properties
    ids = db.o_permission.filter (None, dict (user = uid))
    assert len (ids) <= 1
    if ids:
        operm = db.o_permission.getnode (ids [0])
        return set (operm.org_location)
    elif 'user_dynamic' in db.classes:
        now = Date ('.')
        dyn = user_dynamic.get_user_dynamic (db, uid, now)
        if dyn and dyn.org_location:
            return {dyn.org_location}
    return {()}
# end def get_allowed_olo

def get_allowed_org (db, uid):
    ids = db.o_permission.filter (None, dict (user = uid))
    assert len (ids) <= 1
    if 'org_location' in db.o_permission.properties:
        olo = get_allowed_olo (db, uid)
        org = set (db.org_location.get (ol, 'organisation') for ol in olo)
        return org
    operm = db.o_permission.getnode (ids [0])
    return set (operm.organisation)
# end def get_allowed_org
