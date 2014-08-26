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

def init (instance) :
    reg = instance.registerUtil
    reg ('valid_wps',              vacation.valid_wps)
    reg ('valid_leave_wps',        vacation.valid_leave_wps)
    reg ('leave_days',             vacation.leave_days)
    reg ('user_leave_submissions', user_leave_submissions)
