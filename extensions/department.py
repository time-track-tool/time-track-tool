#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2018 Dr. Ralf Schlatterbeck Open Source Consulting.
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

from roundup.date import Date

def valid_departments (db) :
    """ Return all valid department ids.
    """
    try :
        db = db._db
    except AttributeError :
        pass
    now = Date ('.')
    ids = []
    for id in db.department.getnodeids (retired = False) :
        dept = db.department.getnode (id)
        if dept.valid_to is None :
            ids.append (id)
            continue
        if dept.valid_to > now :
            ids.append (id)
    return ids
# end def valid_departments

def init (instance) :
    instance.registerUtil ('valid_departments',  valid_departments)
# end def init
