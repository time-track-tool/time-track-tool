#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2016 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    update_tr_cache
#
# Purpose
#    update tr_duration cache
#

from user_dynamic import update_tr_duration

def update_tr_cache (db, dr) :
    """ Try to update tr_cache; try up to 5 times
    """
    for i in range (5) :
        try :
            ret = update_tr_duration (db, dr)
            db.commit ()
            break
        except :
            db.rollback ()
    else :
        raise
    return ret
# end def update_tr_cache

#END
