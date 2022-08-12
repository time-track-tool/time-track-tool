#! /usr/bin/python
# Copyright (C) 2013-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    file
#
# Purpose
#    Detectors for file
#
#--
#

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

import common

def check_size (db, cl, nodeid, new_values) :
    if 'content' not in new_values :
        return
    limit = common.Size_Limit (db, 'LIMIT_FILE_SIZE')
    if not limit :
        return
    if new_values ['content'] is None :
        return
    length = len (new_values ['content'] or '')
    if length > limit.limit :
        raise Reject \
            (_ ("Maximum file size %(limit)s exceeded: %(length)s") % locals ())
# end def check_size

def init (db) :
    if 'file' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.file.audit ("create", check_size)
    db.file.audit ("set",    check_size)
# end def init
