#!/swing/bin/python2.4
# Copyright (C) 2003-9 TTTech Computertechnik GmbH. All rights reserved
# Schoenbrunnerstrasse 7, A--1040 Wien, Austria. office@@tttech.com
# ****************************************************************************
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************

from roundup.hyperdb import Link, Multilink

class prettynode (object) :
    """ Simple pretty-printer for a roundup node. Supports __getitem__
        and __getattr__ for accessing attributes of a roundup node,
        Links and Multilinks are replaced by the labelprop of the linked
        item(s).
    """
    def __init__ (self, node) :
        self.node    = node
        self.cl      = node.cl
        self.db      = node.cl.db
    # end def __init__

    def __getitem__ (self, name) :
        if name == "missing_effort" :
            if self.node.numeric_effort is not None or self.node.composed_of :
                return ""
            else :
                return "*"
        cls = self.cl.getprops (1) [name]
        ids = None
        if isinstance (cls, Link) :
            if self.node [name] is not None :
                ids = [self.node [name]]
        elif isinstance (cls, Multilink) :
            ids = self.node [name]
        if ids is not None:
            retval = []
            for id in ids :
                cls = self.db.getclass (cls.classname)
                if cls :
                    retval.append (str (cls.get (id, cls.labelprop ())))
            return ",".join (retval)
        return self.node [name]
    # end def __getitem__

    __getattr__ = __getitem__
# end class prettynode
