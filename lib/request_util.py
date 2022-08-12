#! /usr/bin/python
# Copyright (C) 2012-22 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    request_util
#
# Purpose
#    Utilities for handling html requests
#
#--

class True_Value (type ("")) :
    """ A class that evaluates to True but can return a zero-length string.
        We use this as return value from a handle routine where the
        output happend to the file descriptor
    """
    def __bool__ (self) :
        return True
    # end def __bool__
    __nonzero__ = __bool__
# end class True_Value

### __END__
