#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    access routines for 'user_dynamic'
#

from roundup.date import Date

dynamic = {} # cache

def get_user_dynamic (db, user, date) :
    """ Get a user_dynamic record by user and date.
        Return None if no record could be found.
    """
    global dynamic
    user = str  (user)
    date = Date (date)
    if user in dynamic :
        dyn = dynamic [user]
    else :
        dyn = [db.user_dynamic.getnode (i) for i in db.user_dynamic.filter
                (None, {'user' : user}, sort = ('-', 'valid_from'))
              ]
        dynamic [user] = dyn
    # search linearly -- we don't expect more than say 10-30 dynamic
    # user records per user. We dont want to have a binary search
    # algorithm here: the first record found is probably the current one
    # (the one with the latest start date) so we will usually match the
    # first here if not editing old records.
    for d in dyn :
        if date >= d.valid_from :
            if not d.valid_to or date < d.valid_to :
                return d
            break
    return None
# end def get_user_dynamic
