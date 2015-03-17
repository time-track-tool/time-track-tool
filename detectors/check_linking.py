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
from roundup.hyperdb                import Multilink, Link
from linking                        import linkclass_iter
from roundup.cgi.TranslationService import get_translation

classprops = {}

def old_props (cl, prop, nodeid) :
    if not nodeid :
        return []
    v = cl.get (nodeid, prop)
    if not v :
        return []
    if isinstance (cl.properties [prop], Multilink) :
        return v
    return [v]
# end def old_props

def new_props (cl, prop, new_values) :
    if isinstance (cl.properties [prop], Multilink) :
        return new_values [prop]
    return [new_values [prop]]
# end def new_props

def check_linking (db, cl, nodeid, new_values) :
    """ Allow linking to properties only if we created them """
    if db.getuid () == '1' :
        return
    for prop in classprops [cl.classname] :
        if prop not in new_values :
            continue
        old   = dict.fromkeys (old_props (cl, prop, nodeid))
        klass = db.getclass (cl.properties [prop].classname)
        for id in new_props (cl, prop, new_values) :
            if id not in old and klass.get (id, 'creator') != db.getuid () :
                cls  = _ (klass.classname)
                raise Reject, \
                    _ ("You may link only to your own %(cls)s") % locals ()
# end def check_linking

def check_unlinking (db, cl, nodeid, new_values) :
    """ Don't allow unlinking of properties """
    for prop in classprops [cl.classname] :
        if prop not in new_values :
            continue
        # allow admin
        if db.getuid () == '1' :
            continue
        ids = dict.fromkeys (new_props (cl, prop, new_values))
        for id in old_props (cl, prop, nodeid) :
            if id not in ids :
                name  = _ (cl.classname)
                kls   = cl.properties [prop]
                klass = db.getclass (kls.classname)
                cls   = _ (kls.classname)
                # Allow updating user pictures
                if cls == 'File' and name == 'User' :
                    continue
                # Allow Link properties if old linked prop is owned by user
                if  (   isinstance (kls, Link)
                    and klass.get (id, 'creator') == db.getuid ()
                    ) :
                    continue
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
