#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
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

import re

notes_tofu = re.compile \
    (  "\n{3}"
    + r"([^<]+[^< ])\s+<roundup@tttech.com>.*"
    + r"Please respond to .* issue tracker\s+"
    + r"To:.*\s+[cC][cC]:.*\s+Subject.*\s+"
    + r"\1\s+<.*added the comment:"
    , re.MULTILINE | re.DOTALL
    )
notes_autoreply = \
    [ re.compile ( r"out of the office\." )
    , re.compile ( r"Out of office \.\.\.\." )
    , re.compile ( r"out of office from" )
    , re.compile ( r"be out of office" )
    , re.compile ( r"R[eE]: Your EMail" )
    ]
nasty_chars     = re.compile \
    ('\x00\x01\x02\x03\x04\x05\x06\x07\x08'
     '\x0b'
     '\x0e\x0f'
     '\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
     '\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f'
     '\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f'
     .decode ('latin1')
    )

Tofu_msg = \
"""TOFU Alert -- (T)ext (O)ben (F)ullquote (U)nten
   You have quoted another message entirely.
   Corrective action: Do not use the "Reply with History" button in Lotus Notes
   for replying to an email. Use the "Reply" or "Quoted Reply" button.
   If using "Quoted Reply" please keep only the interesting lines of the
   original mail your are replying to.
   Abhilfe: In Lotus Notes nicht den "Reply with History" Button verwenden, um
   auf eine Mail zu reagieren, sondern entweder den "Reply" Button
   verwenden, oder den "Quoted Reply" Button. Bei letzterem aber auch
   aus der Original-Mail nur die interessanten Zeilen aufheben, den Rest
   bitte löschen.
"""

Autoreply_msg = \
"""You tried to submit a new message that looks like an out of office
   autoreply. The roundup tracker has rejected this message.
"""

Nasty_msg = \
"""You tried to submit a new %s that contains forbidden
   control characters from the range
   [\x00-\x09\x0B\x0D-\x1F\x80-\x9F\xFF]. Please check your message and
   resubmit.
"""

def is_tttech_address (db, author) :
    useraddr = db.user.get (author, 'address')
    if useraddr.find ('@tttech.com') < 0 : return 0
    return 1

def title_create_check (db, cl, nodeid, newvalues) :
    """Checks on title when creating new issue
    """
    if not newvalues.has_key ("title") : return
    for r in notes_autoreply :
        if r.search (newvalues ["title"]) :
            raise ValueError, Autoreply_msg

def title_check (db, cl, nodeid, newvalues) :
    """Checks when creating or changing the title
    """
    title_create_check (db, cl, nodeid, newvalues)
    if not newvalues.has_key ("title")          : return
    if not is_tttech_address (db, db.getuid ()) : return
    if nasty_chars.search (newvalues ["title"].decode ('utf-8')) :
        raise ValueError, Nasty_msg % "title"

def msg_check (db, cl, nodeid, newvalues) :
    if not newvalues.has_key ("messages") : return
    msgs = {}
    for m in newvalues ["messages"] :
        msgs [m] = 1
    if nodeid :
        for m in cl.get (nodeid, "messages") :
            if msgs.has_key (m) : del (msgs [m])
    for m in msgs.keys () :
        msg = db.msg.getnode (m)
        if not is_tttech_address (db, msg.author) : continue
        if notes_tofu.search (msg.content) :
            raise ValueError, Tofu_msg
        if nasty_chars.search (msg.content.decode ('utf-8')) :
            raise ValueError, Nasty_msg % "message"

def init (db) :
    db.issue.audit ("create", title_create_check)
    db.issue.audit ("set",    title_check)
    db.issue.audit ("create", msg_check)
    db.issue.audit ("set",    msg_check)
# end def init
