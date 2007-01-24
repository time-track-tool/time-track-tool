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

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

_ = lambda x : x

def check (db, cl, nodeid, new_values) :
    if 'code' in new_values and cl.get (nodeid, 'code') == 'ABO' :
        raise Reject, _ \
            ('address type category "ABO" is used by the system '
             'and may not be changed.'
            )
# end def check

def retire_check (db, cl, nodeid, new_values) :
    if cl.get (nodeid, 'code') == 'ABO' :
        raise Reject, _ \
            ('address type category "ABO" is used by the system '
             'and may not be changed.'
            )
# end def retire_check

def init (db) :
    if 'adr_type_cat' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.adr_type_cat.audit ("set",    check)
    db.adr_type_cat.audit ("retire", retire_check)
# end def init
