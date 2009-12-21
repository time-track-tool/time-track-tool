#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    linking
#
# Purpose
#    permission-relevant linked classes (msg, file)
#
#--
#

from roundup.hyperdb import Link, Multilink


def linkclass_iter (db, classname) :
    """ For the given classname find all properties in other classes
        that link to that class.
    """
    for clname in sorted (db.getclasses ()) :
        for p, v in sorted (db.getclass (clname).properties.iteritems ()) :
            if  (    (isinstance (v, Multilink) or isinstance (v, Link))
                and v.classname == classname
                ) :
                yield (clname, p)
# end def linkclass_iter

### __END__
