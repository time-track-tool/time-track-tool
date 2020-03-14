#! /usr/bin/python
# Copyright (C) 2013 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#++
# Name
#    dial
#
# Purpose
#    Action(s) for dialling

from urllib                 import urlopen
from roundup.cgi.actions    import Action
from roundup.cgi            import templating
from roundup.cgi.exceptions import Redirect

class Dial (Action) :

    def handle (self) :
        ''' Dial the given number -- for expect a snom with URL dialling. '''
        # figure the request
        request    = self.request = templating.HTMLRequest     (self.client)
        filterspec = request.filterspec
        sort       = request.sort
        group      = request.group
        klass      = self.klass = self.db.getclass (request.classname)
        assert (request.classname == 'contact')
        id         = self.client.nodeid
        contact    = klass.getnode (id)
        cids       = self.db.callerid.filter (None, dict (contact = id))
        callerid   = self.db.callerid.getnode (cids [0])
        user       = self.db.user.getnode (self.db.getuid ())
        sipdev     = self.db.sip_device.getnode (user.sip_device)
        url = 'http://%s:%s@%s:80/command.htm?number=%s&outgoing_uri=%s@%s' % \
            ( sipdev.http_username
            , sipdev.http_password
            , sipdev.name
            , callerid.number
            , sipdev.pbx_username
            , sipdev.pbx_hostname
            )
        #print url
        #print callerid.number
        try :
            f = urlopen (url)
            f.read  ()
            f.close ()
        except EOFError :
            pass
        raise Redirect, "address%s" % contact.address
    # end def handle

# end class Dial

def init (instance) :
    instance.registerAction ('dial', Dial)
# end def init
