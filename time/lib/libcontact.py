#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2013 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    contact
#
# Purpose
#    Common library routines for contact
#
#--
#

def cid (db, ct) :
    """ Compute callerid from phone number.
    """
    x  = ''.join (x for x in ct if x.isdigit ())
    if ct.startswith ('+') :
        x = '+' + x
    cc = getattr (db.config.ext, 'TELEPHONY_COUNTRY_CODE', '43')
    ac = getattr (db.config.ext, 'TELEPHONY_AREA_CODE',    '2243')
    if x.startswith ('+' + cc + ac) :
        x = x [len(cc+ac)+1:]
    elif x.startswith ('+' + cc) :
        x = '0' + x [len(cc)+1:]
    elif x.startswith ('+') :
        x = '00' + x [1:]
    return x
# end def cid

### __END__
