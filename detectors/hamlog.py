# Copyright (C) 2012-21 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
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
#    doc
#
# Purpose
#    Detectors for hamlog
#--

from   roundup.exceptions             import Reject
from   hamlib                         import fix_qsl_status
import common

def check_qso_empty (db, cl, nodeid, old_values) :
    """ Retire qsl if qso Link is removed """
    if 'qso' in old_values and not cl.get (nodeid, 'qso') :
        cl.retire (nodeid)
# end def check_qso_empty

def check_dupe_qsl_type (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    common.require_attributes (_, cl, nodeid, new_values, 'qsl_type', 'qso')
    type = new_values ['qsl_type']
    qso  = new_values ['qso']
    qsl  = db.qsl.filter (None, dict (qso = qso, qsl_type = type))
    qn   = db.qsl_type.get (type, 'name')
    if qsl :
        raise Reject (_ ('Duplicate QSL type "%s" for QSO' % qn))
# end def check_dupe_qsl_type

def check_owner_has_qsos (db, cl, nodeid, new_values) :
    _ = db.i18n.gettext
    if 'call' not in new_values :
        return
    oldcalls = set (cl.get (nodeid, 'call'))
    newcalls = set (new_values ['call'])
    deleted  = oldcalls - newcalls
    if not deleted :
        return
    for call in deleted :
        qsos = db.qso.filter (None, dict (owner = call))
        if qsos :
            name = db.ham_call.get (call, 'name')
            raise Reject \
                (_ ('Cant\'t delete "%(name)s" Call has QSOs') % locals ())
        else :
            db.ham_call.retire (call)
# end def check_owner_has_qsos

def fix_stati_qsl (db, cl, nodeid, old_values) :
    fix_qsl_status (db, cl.get (nodeid, 'qso'))
# end def fix_stati_qsl

def fix_stati_qso (db, cl, nodeid, old_values) :
    w = 'wont_qsl_via'
    if  (  not old_values
        or (w in old_values and old_values [w] != cl.get (nodeid, w))
        ) :
        fix_qsl_status (db, nodeid)
# end def fix_stati_qso

def init (db) :
    if 'qso' not in db.classes :
        return
    db.qsl.react  ('set',    check_qso_empty)
    db.qsl.audit  ('create', check_dupe_qsl_type)
    db.qsl.react  ('create', fix_stati_qsl)
    db.qsl.react  ('set',    fix_stati_qsl)
    db.qso.react  ('create', fix_stati_qso)
    db.qso.react  ('set',    fix_stati_qso)
    db.user.audit ('set',    check_owner_has_qsos)
# end def init

### __END__
