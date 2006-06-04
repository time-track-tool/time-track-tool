#! /usr/bin/python
# Copyright (C) 1998 TTTech Computertechnik GmbH. All rights reserved
# Schoenbrunnerstrasse 7, A--1040 Wien, Austria. office@@tttech.com
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
    if not newvalues.has_key ("messages") :
        return
    files = {}
    issuefiles = []
    if newvalues.has_key ("files") :
        issuefiles = newvalues ["files"]
    elif nodeid :
        issuefiles = cl.get (nodeid, "files", cache = 0)
    for f in issuefiles :
        files [f] = 1
    for msg_id in newvalues ["messages"] :
        for f in db.msg.get (msg_id, "files") :
            files [f] = 1
    newvalues ["files"] = files.keys ()

def init (db) :
    if 'issue' not in db.classes :
        return
    db.issue.audit ("create", add_files)
    db.issue.audit ("set",    add_files)
# end def init
