# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Ralf Schlatterbeck. All rights reserved
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
from linking                        import linkclass_iter
from roundup.cgi.TranslationService import get_translation

classprops = {}

def old_props (cl, prop, nodeid) :
    if not nodeid :
        return []
    return cl.get (nodeid, prop)
# end def old_props

def check_linking (db, cl, nodeid, new_values) :
    """ Allow linking to properties only if we created them """
    for prop in classprops [cl.classname] :
        if prop not in new_values :
            continue
        old   = dict.fromkeys (old_props (cl, prop, nodeid))
        klass = db.getclass (cl.properties [prop].classname)
        for id in new_values [prop] :
            if id not in old and klass.get (id, 'creator') != db.getuid () :
                cls  = _ (klass)
                raise Reject, \
                    _ ("You may link only to your own %(cls)s") % locals ()
# end def check_linking

def check_unlinking (db, cl, nodeid, new_values) :
    """ Don't allow unlinking of properties """
    for prop in classprops [cl.classname] :
        if prop not in new_values :
            continue
        ids = dict.fromkeys (new_values [prop])
        for id in old_props (cl, prop, nodeid) :
            if id not in ids :
                name = _ (cl.classname)
                cls  = _ (cl.properties [prop].classname)
                raise Reject, \
                    _ ("You may not unlink %(cls)s from %(name)s") % locals ()
# end def check_unlinking

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    # certain checks of linking/unlinking of files and messages
    for x in 'msg', 'file' :
        for cl, prop in linkclass_iter (db, x) :
            if cl not in classprops :
                classprops [cl] = [prop]
                klass = db.getclass (cl)
                klass.audit ("create", check_linking)
                klass.audit ("create", check_unlinking)
                klass.audit ("set",    check_linking)
                klass.audit ("set",    check_unlinking)
            else :
                classprops [cl].append (prop)
# end def init
