#! /usr/bin/python
# Copyright (C) 2020 Dr. Ralf Schlatterbeck Open Source Consulting.
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

def valid_user_stati (db) :
    """ Valid user statis are now valid and valid_ad, this should be
        fixed by adding an 'active' flag to the user_status or similar.
    """
    try :
        db = db._db
    except AttributeError :
        pass
    return db.user_status.filter (None, dict (name = 'valid'))
# end def valid_user_stati

def valid_user_stati_filter (db) :
    return ','.join (valid_user_stati (db))
# end def valid_user_stati_filter

def init (instance) :
    reg = instance.registerUtil
    reg ('valid_user_stati',             valid_user_stati)
    reg ('valid_user_stati_filter',      valid_user_stati_filter)
# end def init

