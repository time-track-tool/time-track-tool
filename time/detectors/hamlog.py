# -*- coding: iso-8859-1 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck Open Source Consulting.
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
from   roundup.cgi.TranslationService import get_translation

def check_qso_empty (db, cl, nodeid, old_values) :
    """ Retire qsl if qso Link is removed """
    if 'qso' in old_values and not cl.get (nodeid, 'qso') :
        cl.retire (nodeid)
# end def check_qso_empty

def init (db) :
    if 'qso' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext

    db.qsl.react ('set', check_qso_empty)
# end def init

### __END__
