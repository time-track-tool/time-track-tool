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
from roundup.hyperdb                import Multilink

class Create_New_Address (Action) :
    """ Create a new address to be added to the current item (used for
        customer addresses, supply_address, invoice_address,
        contact_person).
        
        Optional @frm specifies the address to copy.
    """
    copy_attributes = \
        [ 'adr_type', 'birthdate', 'city', 'country'
        , 'firstname', 'function', 'initial', 'lastname', 'lettertitle'
        , 'postalcode', 'salutation', 'street', 'title'
        , 'valid'
        ]
    def handle (self) :
        self.request = templating.HTMLRequest (self.client)
        assert (self.client.nodeid)
        klass    = self.db.classes [self.request.classname]
        id       = self.client.nodeid
        attr     = self.form ['@attr'].value.strip ()
        if '@frm' in self.form :
            frm  = self.form ['@frm'].value.strip ()
            node = self.db.address.getnode (self.db.cust_supp.get (id, frm))
            attributes = dict \
                ((k, node [k]) for k in self.copy_attributes
                 if node [k] is not None
                )
        else :
            attributes = dict \
                ( function  = klass.get (id, 'name')
                , country   = ' '
                )

        newvalue = newid = self.db.address.create (** attributes)
        if isinstance (klass.properties [attr], Multilink) :
            newvalue = klass.get (id, attr) [:]
            newvalue.append (newid)
            newvalue = list (set (newvalue))
        klass.set (id, ** {attr : newvalue})
        self.db.commit ()
        raise Redirect ("%s%s" % (self.request.classname, id))
    # end def handle
# end class Create_New_Address

def del_link (classname, id) :
    return \
        ( "document.forms.itemSynopsis ['@remove@%s'].value = '%s';"
          "alert(document.forms.itemSynopsis ['@remove@%s'].value);"
        % (classname, id, classname)
        )
# end def del_link

def adress_button (db, adr_property_frm, adr_property_to) :
    """Compute address copy button inscription"""
    adr_frm = db._ (adr_property_frm)
    adr_to  = db._ (adr_property_to)
    return db._ (''"new %(adr_to)s from %(adr_frm)s") % locals ()
# end def adress_button

def init (instance) :
    actn = instance.registerAction
    actn ('create_new_address', Create_New_Address)
    util = instance.registerUtil
    util ("del_link",           del_link)
    util ("adress_button",      adress_button)
# end def init
