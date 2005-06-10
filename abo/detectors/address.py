# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Ralf Schlatterbeck. All rights reserved
# Reichergasse 131, A-3411 Weidling
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

from roundup.rup_utils import uni, pretty

Reject = ValueError

def set_adr_defaults (db, cl, nodeid, new_values) :
    """ Set some default values for new address """
    if 'lettertitle' not in new_values  and 'title' in new_values :
        new_values ['lettertitle'] = new_values ['title']
    if 'valid' not in new_values :
        new_values ['valid'] = '1'
    if 'initial' not in new_values and 'firstname' in new_values :
        initial = firstname [0].upper () + '.'
# end def set_adr_defaults

def init (db) :
    db.address.audit ("create", set_adr_defaults)
# end def init
