#! /usr/bin/python
# Copyright (C) 2006-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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

def add_files (db, cl, nodeid, newvalues) :
    """Link files of new messages to files of issue
    """
    if "messages" not in newvalues :
        return
    files = {}
    issuefiles = []
    if "files" in newvalues :
        issuefiles = newvalues ["files"]
    elif nodeid :
        issuefiles = cl.get (nodeid, "files", cache = 0)
    for f in issuefiles :
        files [f] = 1
    for msg_id in newvalues ["messages"] :
        for f in db.msg.get (msg_id, "files") :
            files [f] = 1
    newvalues ["files"] = list (files)

def init (db) :
    if 'issue' not in db.classes :
        return
    db.issue.audit ("create", add_files)
    db.issue.audit ("set",    add_files)
# end def init
