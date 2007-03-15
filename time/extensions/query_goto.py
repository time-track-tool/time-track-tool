#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2007 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
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
#++
# Name
#    query_goto
#
# Purpose
#    Action for redirecting to the view of a query
#--

from roundup.cgi.actions    import Action
from roundup.cgi            import templating
from roundup                import hyperdb
from roundup.cgi.exceptions import Redirect


class Query_Goto (Action) :

    def handle (self) :
        ''' Export the specified search query as CSV. '''
        # figure the request
        request    = self.request = templating.HTMLRequest     (self.client)
        filterspec = request.filterspec
        sort       = request.sort
        group      = request.group
        klass      = self.klass = self.db.getclass (request.classname)
        assert (request.classname == 'query')
        id         = self.client.nodeid
        query = klass.getnode (id)
        raise Redirect, "%s?%s" % (query.klass, query.url)
    # end def handle

# end class Query_Goto

def init (instance) :
    instance.registerAction ('query_goto',     Query_Goto)
# end def init
