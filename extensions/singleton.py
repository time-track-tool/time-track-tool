#! /usr/bin/python
# Copyright (C) 2006-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    singleton
#
# Purpose
#    Redirect to the one and only instance
#

from roundup.cgi.actions    import Action
from roundup.cgi            import templating
from roundup.cgi.exceptions import Redirect

class Singleton (Action) :
    def handle (self) :
        # figure the request
        request    = self.request = templating.HTMLRequest (self.client)
        klass      = self.klass = self.db.getclass (request.classname)
        id         = self.client.nodeid
        if not id :
            ids = klass.getnodeids ()
            if ids :
                id = ids [0]
        if id :
            raise Redirect ('%s%s' % (request.classname, id))
        add = ''
        if request.classname == 'dyndns' :
            add = '&local_hostname=localhost'
        raise Redirect ('%s?@template=item%s' % (request.classname, add))
    # end def handle
# end class Singleton

def init (instance) :
    instance.registerAction ('singleton', Singleton)
# end def init
