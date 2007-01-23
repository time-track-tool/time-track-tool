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
#    Export_CSV_Names
#
# Purpose
#    Action for exporting current query as CSV (comma separated values)
#--

import csv
import re
try :
    from cStringIO import StringIO
except ImportError :
    from StringIO  import StringIO

from roundup.cgi.actions import Action
from roundup.cgi         import templating
from roundup             import hyperdb

from rsclib.autosuper    import autosuper

from extproperty         import ExtProperty

class Repr (autosuper) :
    def __init__ (self, klass) :
        self.klass = klass
    # end def __init__

    def __call__ (self, itemid, col, x = None) :
        if x is None :
            self.setup (itemid, col)
        if self.x is None :
            return ""
    # end def __call__

    def setup (self, itemid, col) :
        self.x = self.klass.get (itemid, col)
    # end def setup
# end class Repr

class Repr_Date (Repr) :
    def __call__ (self, itemid, col) :
        self.__super.__call__ (itemid, col)
        return self.x.pretty ('%Y-%m-%d')
    # end def __call__
# end class Repr_Date

class Repr_Str (Repr) :
    def __call__ (self, itemid, col, x = None) :
        self.__super.__call__ (itemid, col, x)
        return str (self.x).decode ('utf-8').encode ('latin1')
    # end def __call__
# end class Repr_Str

class Repr_Country (Repr_Str) :
    def __call__ (self, itemid, col) :
        self.setup (itemid, col)
        x = self.x.strip ()
        if x == 'CH' :
            return ''
        self.__super.__call__ (itemid, col, x)
    # end def __call__
# end class Repr_Country

def repr_link (cls, cols) :
    class Repr_Link (Repr) :
        def __call__ (self, itemid, col) :
            self.__super.__call__ (itemid, col)
            s = " ".join (str (cls.get (x, c)) for c in cols)
            return s.decode ('utf-8').encode ('latin1')
        # end def __call__
    # end class Repr_Link
    return Repr_Link ()
# end def repr_link

def repr_func (klass, col) :
    idx = int (col.split ('.', 1)[1])
    class Repr_Func (Repr_Str) :
        def __call__ (self, itemid, col) :
            self.setup (itemid, 'function')
            try :
                self.__super.__call__ \
                    (itemid, 'function', self.x.split ('\n', 2) [idx])
            except AttributeError :
                pass
            except IndexError :
                return ""
            return self.__super.__call__ (itemid, col, self.x)
        # end def __call__
    # end class Repr_Func
    return Repr_Func (klass)
# end def repr_func

def repr_code (klass, adr_types) :
    class Repr_Code (Repr) :
        def __call__ (self, itemid, col) :
            self.setup (itemid, 'adr_type')
            if self.x is None :
                return "0"
            for t in self.x :
                if t in adr_types :
                    return "A"
            return "0"
        # end def __call__
    # end class Repr_Code
    return Repr_Code (klass)
# end def repr_code

class Export_CSV_Names (Action, autosuper) :
    name = 'export'
    permissionType = 'View'
    print_head     = True
    filename       = 'query.csv'
    delimiter      = '\t'
    quoting        = csv.QUOTE_MINIMAL

    def _setup (self, request) :
        columns    = request.columns
        if not columns :
            columns = self.props.keys ()
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

    def build_repr (self) :
        """ Figure out Link columns and build representation methods for them
        """
        self.represent = {}

        repr_date    = Repr_Date    (self.klass)
        repr_str     = Repr_Str     (self.klass)

        def repr_link (cls, cols) :
            def f (itemid, col) :
                x = self.klass.get (itemid, col)
                if x == None :
                    return ""
                else :
                    s = " ".join ([str (cls.get (x, col)) for col in cols])
                    return s.decode ('utf-8').encode ('latin1')
            return f
        # end def repr_link

        def repr_extprop (col) :
            parts = col.split ('.', 1)
            prop  = self.htcls [parts [0]]
            ep    = ExtProperty \
                ( self.utils, prop
                , searchname  = col
                , pretty      = str
                )
            def f (itemid, col) :
                item = templating.HTMLItem \
                    (self.client, request.classname, itemid)
                return ep.as_listentry (item = item, as_link = False)
            # end def f
            return f
        # end def repr_extprop

        for col in self.columns :
            self.represent [col] = repr_str
            if col.startswith ('function.') :
                self.represent [col] = repr_func (self.klass, col)
            elif '.' in col :
                self.represent [col] = repr_extprop (col)
            elif col not in self.props :
                print "oops:", col
                pass
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
        request    = templating.HTMLRequest     (self.client)
        self.utils = templating.TemplatingUtils (self.client)
        filterspec = request.filterspec
        sort       = request.sort
        group      = request.group
        klass      = self.klass = self.db.getclass (request.classname)
        self.props = klass.getprops ()
        self.htcls = templating.HTMLClass (self.client, request.classname)
        self._setup (request)

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
                ([self.represent [col] (itemid, col) for col in self.columns])
        return io.getvalue ()
    # end def handle
# end class Export_CSV_Names

class Export_CSV_Addresses (Export_CSV_Names) :

    print_head = False
    filename   = 'ZFABO.CSV'
    quoting    = csv.QUOTE_NONE

    def _setup (self, request) :
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
        tc             = self.db.adr_type_cat.lookup ('ABO')
        self.adr_types = dict.fromkeys (self.db.adr_type.find (typecat = tc), 1)
        self.represent ['country'] = Repr_Country (self.klass)
        print self.represent ['code']
        self.represent ['code']    = repr_code (self.klass, self.adr_types)
        print self.represent ['code']
        print "done"
    # end def build_repr

# end class Export_Addresses

def init (instance) :
    instance.registerAction ('export_csv_names',     Export_CSV_Names)
    instance.registerAction ('export_csv_addresses', Export_CSV_Addresses)
# end def init
