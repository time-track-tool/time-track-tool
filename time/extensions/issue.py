# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Philipp Gortan <gortan@tttech.com>
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
# ****************************************************************************
#
#++
# Name
#    issue
#
# Purpose
#    Provide utitity functions for the issue class and friends
#
# Revision Dates
#    11-Dec-2007 (PGO) Creation
#    12-Dec-2007 (RSC) Remove i18n hack
#    ««revision-date»»···
#--

def filter_status_transitions (status_prop) :
    if status_prop :
        return {'id' : [t.target._value for t in status_prop.transitions]}
    return {}
# end def filter_status_transitions

def init (instance) :
    reg = instance.registerUtil
    reg ('filter_status_transitions', filter_status_transitions)
# end def init

### __END__ issue
