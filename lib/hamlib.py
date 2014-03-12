#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    hamlog
#
# Purpose
#    Common library routines for ham operation
#
#--
#

def fix_qsl_status (db, qso_id) :
    """Fix stati (qsl_r_status, qsl_s_status, no_qsl_status) for whole db.
       can be used after changing the status and qsl_type configuration.
    """
    stati = dict (qsl_r_status = 0, qsl_s_status = 0, no_qsl_status = 0)
    qsl_ids = db.qsl.filter (None, dict (qso = qso_id))
    for qsl_id in qsl_ids :
        qsl = db.qsl.getnode (qsl_id)
        if qsl.date_recv :
            stati ['qsl_r_status'] \
                |= int (db.qsl_type.get (qsl.qsl_type, 'code'))
        if qsl.date_sent :
            stati ['qsl_s_status'] \
                |= int (db.qsl_type.get (qsl.qsl_type, 'code'))
    for qsl_type_id in db.qso.get (qso_id, 'wont_qsl_via') :
        stati ['no_qsl_status'] |= int (db.qsl_type.get (qsl_type_id, 'code'))
    for k in stati.keys () :
        stati [k] = db.qsl_status.filter (None, dict (code = stati [k])) [0]
    db.qso.set (qso_id, **stati)
# end def fix_qsl_status


### __END__
