#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2018 Dr. Ralf Schlatterbeck Open Source Consulting.
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

def loadavg () :
    """ Get load average from /proc/loadavg

        The first three fields in this file are load average figures
        giving the number of jobs in the run queue (state R) or
        waiting for disk I/O (state D) averaged over 1, 5, and 15
        minutes. They are the same as the load average numbers given
        by uptime(1) and other programs.

        We use the one-minute average.
    """
    with open ('/proc/loadavg') as f :
        l = f.readline ()
        a1m = float (l.split () [0])
    return a1m
# end def loadavg

def max_load (db) :
    """ We get this from the ext config by default, if nothing is
        specified we return 3.0 here
    """
    try :
        db = db._db
    except AttributeError :
        pass
    v = getattr (db.config.ext, 'LIMIT_MAX_LOAD', None)
    if v :
        v = float (v)
    else :
        v = 3.0
    return v
# end def max_load

def init (instance) :
    reg = instance.registerUtil
    reg ('loadavg',  loadavg)
    reg ('max_load', max_load)
# end def init
