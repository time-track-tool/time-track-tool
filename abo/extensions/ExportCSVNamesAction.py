#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#
#++
# Name
#    ExportCSVNamesAction
#
# Purpose
#    Action for exporting current query as CSV (comma separated values)
#--

import csv
import re

from rsclib.autosuper    import autosuper
from roundup.cgi.actions import Action
from roundup.cgi         import templating
from roundup             import hyperdb
try :
    from cStringIO import StringIO
except ImportError :
    from StringIO  import StringIO

def repr_date (x) :
    if x is None :
        return ""
    else :
        return x.pretty ('%Y-%m-%d')
# end def repr_date

def repr_str (x) :
    if x is None :
        return ""
    return str (x).decode ('utf-8').encode ('latin1')
# end def repr_str

def repr_country (x) :
    x = x.strip ()
    if x == 'CH' :
        return ''
    return repr_str (x)
# end def repr_country

def repr_link (cls, cols) :
    def f (x) :
        if x is None :
            return ""
        else :
            s = " ".join ([str (cls.get (x, col)) for col in cols])
            return s.decode ('utf-8').encode ('latin1')
    return f
# end def repr_link

def repr_func (col) :
    idx = int (col.split ('.')[1])
    def f (x) :
        try :
            return repr_str (x.split ('\n', 2) [idx])
        except AttributeError :
            pass
        except IndexError :
            return ""
        if x : return repr_str (x)
        return ""
    return f
# end def repr_func

def repr_code (cls, adr_types) :
    def f (x) :
        if x is None :
            return "0"
        for t in x :
            if t in adr_types :
                return "A"
        return "0"
    return f
# end def repr_code

class Export_CSV_Names (Action, autosuper) :
    name           = 'export'
    permissionType = 'View'
    print_head     = True
    filename       = 'query.csv'
    delimiter      = '\t'
    quoting        = csv.QUOTE_MINIMAL

    def _setup (self, request, props) :
        columns    = request.columns
        if not columns :
            columns = props.keys ()
            columns.sort ()
        # full-text search
        if request.search_text :
            matches = self.db.indexer.search \
                (re.findall (r'\b\w{2,25}\b', request.search_text), klass)
        else :
            matches = None
        self.columns = columns
        self.matches = matches
    # end def _setup

    def _attr (self, col) :
        if col == 'code' :
            return 'adr_type'
        try :
            return col.split ('.')[0]
        except AttributeError :
            pass
        return col
    # end def _attr

    def build_repr (self) :
        """ Figure out Link columns and build representation methods for them
        """
        self.represent = {}

        for col in self.columns :
            self.represent [col] = repr_str
            if col == 'code' :
                self.represent [col] = repr_code (col, self.adr_types)
            elif col.startswith ('function.') :
                self.represent [col] = repr_func (col)
            elif isinstance (self.props [col], hyperdb.Link) :
                cn = self.props [col].classname
                cl = self.db.getclass (cn)
                pr = cl.getprops ()
                if 'lastname' in pr and cl.labelprop () != 'username' :
                    self.represent [col] = repr_link \
                        (cl, ('firstname', 'lastname'))
                else :
                    self.represent [col] = repr_link (cl, (cl.labelprop (),))
            elif isinstance (self.props [col], hyperdb.Date) :
                self.represent [col] = repr_date
    # end def build_repr

    def handle (self) :
        ''' Export the specified search query as CSV. '''
        # figure the request
        request    = templating.HTMLRequest (self.client)
        filterspec = request.filterspec
        sort       = request.sort
        group      = request.group
        klass      = self.db.getclass (request.classname)
        self.props = klass.getprops ()
        self._setup (request, self.props)

        typecat        = self.db.adr_type_cat.lookup ('ABO')
        self.adr_types = dict \
            ([(i, 1) for i in self.db.adr_type.find (typecat = typecat)])

        h                        = self.client.additional_headers
        h ['Content-Type']       = 'text/csv'
        # some browsers will honor the filename here...
        h ['Content-Disposition'] = 'inline; filename=%s' % self.filename

        self.client.header ()

        if self.client.env ['REQUEST_METHOD'] == 'HEAD' :
            # all done, return a dummy string
            return 'dummy'

        io = StringIO ()
        writer = csv.writer \
            ( io
            , dialect   = 'excel'
            , delimiter = self.delimiter
	    , quoting   = self.quoting
            )
        if self.print_head :
            writer.writerow (self.columns)

        self.build_repr ()

        # and search
        for itemid in klass.filter (self.matches, filterspec, sort, group) :
            writer.writerow \
                ( [self.represent [col] (klass.get (itemid, self._attr (col)))
                   for col in self.columns
                  ]
                )

        return io.getvalue ()
    # end def handle
# end class Export_CSV_Names

class Export_CSV_Addresses (Export_CSV_Names) :

    print_head = False
    filename   = 'ZFABO.CSV'
    quoting    = csv.QUOTE_NONE

    def _setup (self, request, props) :
        self.columns = \
            [ 'title'
            , 'firstname'
            , 'lastname'
            , 'function.0'
            , 'function.1'
            , 'function.2'
            , 'street'
            , 'country'
            , 'postalcode'
            , 'city'
            , 'code'
            ]
        self.matches = None
    # end def _setup

    def build_repr (self) :
        self.__super.build_repr ()
        self.represent ['country'] = repr_country
    # end def build_repr

# end class Export_Addresses

def init (instance) :
    instance.registerAction ('export_csv_names',     Export_CSV_Names)
    instance.registerAction ('export_csv_addresses', Export_CSV_Addresses)
# end def init
