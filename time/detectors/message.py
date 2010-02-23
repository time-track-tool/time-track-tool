#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-10 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
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
#

from roundup.mailgw import parseContent
from roundup.date   import Date

def summarygenerator (db, cl, nodeid, newvalues) :
    ''' If the message doesn't have a summary, make one for it.
    '''
    if newvalues.has_key ('summary') or not newvalues.has_key ('content') :
        return

    summary, content = parseContent (newvalues ['content'], 1, 1)
    newvalues ['summary'] = summary
# end def summarygenerator

def check_params (db, cl, nodeid, newvalues) :
    """ Check if message has an author, use creator if not """
    if 'author' not in newvalues :
        newvalues ['author'] = db.getuid ()
    if 'date' not in newvalues :
        newvalues ['date'] = Date ('.')
# end def check_params

def init(db):
    # fire before changes are made
    db.msg.audit('create', summarygenerator)
    db.msg.audit('create', check_params)
