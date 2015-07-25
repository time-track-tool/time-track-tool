#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2015 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#++
# Name
#    ext_tracker
#
# Purpose
#    Utilities for external trackers
#
#--

from roundup.cgi.TranslationService import get_translation

def get_kpm (db, issue) :
    """ If the issue is a kpm-synchronized issue (this means it has
        ext_tracker set to an external tracker with the is_kpm flag set)
        this function returns an attached (Link1) kpm class.
        This has a pointer to an instance. At most one such object
        should be found (it's an error if there is more than one).
        If none is found we create a new one and return it.
    """
    kpm_attr = db.kpm.filter (None, dict (issue = issue.id))
    assert len (kpm_attr) <= 1
    if kpm_attr :
        return kpm_attr [0]
    else :
        # Check if the issue is a kpm issue
        if not issue.ext_tracker.is_kpm :
            return None
        # If it was already synced before we have an ext_id this needs
        # to be modified by a script -- or potentially the syncer should
        # handle this. We return None so the form will not display
        # additional kpm info.
        if issue.ext_id :
            return None
        else :
            kpm = db._db.kpm.create (issue = issue.id)
            db._db.commit ()
    return db.kpm.filter (None, dict (issue = issue.id)) [0]
# end def get_kpm

def init (instance) :
    global _
    _   = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.config.TRACKER_HOME).gettext
    instance.registerUtil ('get_kpm',  get_kpm)
# end def init
