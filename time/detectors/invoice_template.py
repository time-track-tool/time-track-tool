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
from roundup.date                   import Date, Interval
from roundup.cgi.TranslationService import get_translation

_ = lambda x : x

def new_iv_template (db, cl, nodeid, new_values) :
    for i in ('tmplate', 'invoice_level', 'interval') :
        if not i in new_values :
            raise Reject, _ ('"%(attr)s" must be filled in') % {'attr' : _ (i)}
    if not 'name' in new_values :
        new_values ['name'] = db.tmplate.get (new_values ['tmplate'], 'name')
# end def new_iv_template

def iv_template_ok (db, cl, nodeid, new_values) :
    for i in ('tmplate', 'invoice_level', 'interval', 'name') :
        x = new_values.get (i, cl.get (nodeid, i))
        if x is None :
            raise Reject, _ ('"%(attr)s" may not be deleted') % {'attr' : _ (i)}
# end def iv_template_ok

def init (db) :
    if 'invoice_template' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.invoice_template.audit ("create", new_iv_template)
    db.invoice_template.audit ("set",    iv_template_ok)
# end def init
