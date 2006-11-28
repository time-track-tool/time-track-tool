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
#    public_holiday
#
# Purpose
#    Detectors for 'public_holiday'
#

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

_      = lambda x : x

def check_public_holiday (db, cl, nodeid, new_values) :
    for i in 'name', 'date', 'locations' :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be deleted" % {'attr' : _ (i)}
# end def check_public_holiday

def new_public_holiday (db, cl, nodeid, new_values) :
    for i in 'name', 'date', 'locations' :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
# end def new_public_holiday

def init (db) :
    if 'public_holiday' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.public_holiday.audit  ("create", new_public_holiday)
    db.public_holiday.audit  ("set",    check_public_holiday)
# end def init

