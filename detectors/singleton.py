#! /usr/bin/python
# Copyright (c) 2010 Ralf Schlatterbeck (rsc@runtux.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from roundup.exceptions             import Reject

def new_singleton (db, cl, nodeid, new_values) :
    """ Note: You probably want to create a singleton during database
        initialisation. Later there is a race condition: The database
        serialisation constraints do *not* enforce that no two items are
        created concurrently. Therefore for *both* concurrent creations
        this auditor will succeed -- resulting in two singletons.
    """
    _ = db.i18n.gettext
    if cl.getnodeids () :
        n = cl.classname
        raise Reject, _ ('May not create another instance of "%s"') % _ (n)
# end def new_singleton

def init (db) :
    singletons = ["dyndns", "transceiver", "umts"]
    for klass in singletons :
        if klass not in db.classes :
            continue
        cl = db.getclass (klass)
        cl.audit ("create", new_singleton)
# end def init
