# Copyright (C) 2009-21 Ralf Schlatterbeck. All rights reserved
# Reichergasse 131, A-3411 Weidling
# ****************************************************************************
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ****************************************************************************

from roundup.exceptions             import Reject
from roundup.hyperdb                import Multilink, Link
from linking                        import linkclass_iter
import common

classprops = {}
# Exceptions from unlink check for multilinks (only if linked item is
# created by same db-user who now tries to unlink)
exceptions = { 'purchase_request' : ['messages'] }

# Exceptions for Links
# We allow unlinking of messages for kpm: we have message fields that
# re-link on change. For the user class we allow file for user picture.
l_exceptions = dict (kpm = 'msg', user = 'file')

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
    _ = db.i18n.gettext
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
                raise Reject \
                    (_ ("You may link only to your own %(cls)s") % locals ())
# end def check_linking

def check_unlinking (db, cl, nodeid, new_values) :
    """ Don't allow unlinking of properties """
    _ = db.i18n.gettext
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
                # Check Link property exceptions:
                if cl.classname in l_exceptions :
                    if l_exceptions [cl.classname] == kls.classname :
                        continue
                # Allow Link properties if old linked prop is owned by user
                if  (   isinstance (kls, Link)
                    and klass.get (id, 'creator') == db.getuid ()
                    ) :
                    continue
                # Allow Multilink properties in exceptions if linked
                # prop is owned by user
                if  (   prop in exceptions.get (cl.classname, [])
                    and klass.get (id, 'creator') == db.getuid ()
                    ) :
                    continue
                # Allow IT and admin roles
                if common.user_has_role (db, db.getuid (), 'it', 'admin') :
                    continue
                raise Reject \
                    (_ ("You may not unlink %(cls)s from %(name)s") % locals ())
# end def check_unlinking

def init (db) :
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
