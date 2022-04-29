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
    attr = {}
    for i in 'period', 'adr_type' :
        if i in new_values :
            attr [i] = new_values.get (i)
        elif nodeid :
            attr [i] = cl.get (nodeid, i)
        if not i in attr or not attr [i] :
            raise Reject (_ ('"%(attr)s" must be filled in') % {'attr' : _ (i)})
    period   = attr ['period']
    if int (period) != period :
        raise Reject (_ ('period must be an integer'))
#    adr_type = attr ['adr_type']
#    cat = db.adr_type.get  (adr_type, 'typecat')
#    if db.adr_type_cat.get (cat, 'code') != 'ABO' :
#        raise Reject \
#            (_ ('Selected address types must be in type category "ABO"'))
# end def check

def init (db) :
    if 'abo_type' not in db.classes :
        return
    db.abo_type.audit     ("create", check)
    db.abo_type.audit     ("set",    check)
# end def init
