#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    sinvoice
#
# Purpose
#    Schema definitions for simple invoice base class -- to be extended
#    by further definitions

from roundup.hyperdb import Class
import schemadef

def init \
    ( db
    , Class
    , Ext_Class
    , String
    , Date
    , Link
    , Multilink
    , Boolean
    , Number
    , ** kw
    ) :

    do_index = "no"
    export   = {}

    currency = Class \
        ( db, ''"currency"
        , name                = String    ()
        , description         = String    ()
        )
    currency.setkey (''"name")

    class Invoice_Class (Ext_Class) :
        """ Create an invoice class that should be extended in later
            definitions -- either as a simple invoice for abo or more
            complex for ERP.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( invoice_no          = String    ()
                , amount              = Number    ()
                , currency            = Link      ("currency")
                , balance_open        = Number    ()
                , amount_payed        = Number    ()
                , open                = Boolean   ()
                , n_sent              = Number    ()
                , last_sent           = Date      ()
                , send_it             = Boolean   ()
                , payment             = Multilink ("payment")
                , letters             = Multilink ("letter")
                )
            self.__super.__init__ (db, classname, ** properties)
            self.setkey (''"invoice_no")
        # end def __init__
    # end class Invoice_Class
    export.update (dict (Invoice_Class = Invoice_Class))

    # The invoice_level number decides for which invoice level we use
    # which template.
    invoice_template = Class \
        ( db, ''"invoice_template"
        , tmplate             = Link      ("tmplate")
        , invoice_level       = Number    ()
        , interval            = Number    ()
        , name                = String    ()
        )
    invoice_template.setkey (''"name")

    payment = Class \
        ( db, ''"payment"
        , invoice             = Link      ("invoice")
        , amount              = Number    ()
        , date_payed          = Date      ()
        , receipt_no          = String    ()
        )
    payment.setkey (''"receipt_no")

    return export
# end def init


def security (db, ** kw) :
    roles = \
        [ ("Invoice"       , "Allowed to change financial data")
        ]

    classes = \
        [ ("currency",         ["User"],    [])
        , ("invoice_template", ["Invoice"], ["Invoice"])
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, [])
# end def security
