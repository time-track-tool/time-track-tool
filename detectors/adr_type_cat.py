# Copyright (C) 2004-21 Ralf Schlatterbeck. All rights reserved
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

from roundup.exceptions             import Reject

def check (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    if 'code' in new_values and cl.get (nodeid, 'code') == 'ABO' :
        raise Reject \
            (_ ('address type category "ABO" is used by the system '
                'and may not be changed.'
               )
            )
# end def check

def retire_check (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    if cl.get (nodeid, 'code') == 'ABO' :
        raise Reject \
            (_ ('address type category "ABO" is used by the system '
                'and may not be changed.'
               )
            )
# end def retire_check

def new_adr_type_cat (db, cl, nodeid, new_values) :
    if 'type_valid' not in new_values :
        new_values ['type_valid'] = True
# end def new_adr_type_cat

def init (db) :
    if 'adr_type_cat' not in db.classes :
        return
    db.adr_type_cat.audit ("set",    check)
    db.adr_type_cat.audit ("retire", retire_check)
    db.adr_type_cat.audit ("create", new_adr_type_cat)
# end def init
