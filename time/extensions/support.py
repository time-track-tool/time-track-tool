#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    support
#
# Purpose
#    Support-Tracker related utilities
#
#--
#

try :
    # fail at runtime if these are used
    from email.parser import Parser
except ImportError :
    pass

def has_x_roundup_cc_header (db, msg) :
    try :
        db = db._db
    except AttributeError :
        pass
    if 'header' in db.msg.properties and msg.header :
        h = Parser ().parsestr (str (msg.header), headersonly = True)
        rcc = h.get_all ('X-ROUNDUP-CC')
        if rcc :
            return True
    return False
# end def has_x_roundup_cc_header

def init (instance) :
    reg = instance.registerUtil
    reg ('has_x_roundup_cc_header', has_x_roundup_cc_header)
# end def init
