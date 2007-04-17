#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    customer_action
#
# Purpose
#
#    Various actions for editing of customer data
#--

from roundup.cgi.actions            import Action, EditItemAction, SearchAction
from roundup.cgi.exceptions         import Redirect
from roundup.exceptions             import Reject
from roundup.cgi                    import templating
from roundup.date                   import Date, Interval, Range
from roundup.cgi.TranslationService import get_translation

class Create_New_Address (Action) :
    """ Create a new address to be added to the current item (used for
        customer addresses)
    """
    def handle (self) :
        self.request = templating.HTMLRequest (self.client)
        assert (self.client.nodeid)
        klass    = self.db.classes [self.request.classname]
        id       = self.client.nodeid
        attr     = self.form ['@attr'].value.strip ()
        newid    = self.db.address.create \
            ( function  = klass.get (id, 'name')
            , country   = ' '
            )
        klass.set (id, ** {attr : newid})
        self.db.commit ()
        raise Redirect, 'address%s' % newid
    # end def handle
# end class Create_New_Address

def init (instance) :
    global _
    _   = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.config.TRACKER_HOME).gettext
    actn = instance.registerAction
    actn ('create_new_address', Create_New_Address)
    util = instance.registerUtil
    #util ("dynuser_copyfields",       dynuser_copyfields)
# end def init
