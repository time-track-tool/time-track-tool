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

from roundup.cgi.actions   import Action
from roundup.cgi           import templating
from roundup               import hyperdb

from rsclib.autosuper      import autosuper
from rsclib.TeX_CSV_Writer import TeX_CSV_Writer

from extproperty           import ExtProperty

class Repr_Str (autosuper) :
    def __init__ (self, klass) :
        self.klass = klass
    # end def __init__

    def conv (self, x) :
        return str (x).decode ('utf-8').encode ('latin1', 'replace')
    # end def conv

    def __call__ (self, itemid, col, x = None) :
        if x is None :
            x = self.klass.get (itemid, col)
        x = x or ""
        return self.conv (x)
    # end def __call__
# end class Repr

class Repr_Anschrift (Repr_Str) :
    def __call__ (self, itemid, col) :
        fields = ('postalcode', 'city')
        x = ' '.join (self.klass.get (itemid, z) for z in fields)
        country = self.klass.get (itemid, 'country')
        if country != 'A' :
            x = country + '-' + x
        return self.conv (x)
    # end def __call__
# end class Repr_Anschrift

class Repr_Fullname (Repr_Str) :
    def __call__ (self, itemid, col) :
        fields = ('lastname', 'firstname', 'function')
        x = ' '.join \
            (y for y in (self.klass.get (itemid, z) for z in fields) if y)
        x = x.replace ('\n', ' ')
        return self.conv (x)
    # end def __call__
# end class Repr_Fullname

class Repr_Type (Repr_Str) :
    def __call__ (self, itemid, col) :
        x = ''
        type = self.klass.db.adr_type.lookup (col.split ('.') [1])
        if type in self.klass.get (itemid, 'adr_type') :
            x = 'ja'
        return self.conv (x)
    # end def __call__
# end class Repr_Type

class Repr_Date (Repr_Str) :
    def conv (self, x) :
        if x :
            return '%4d-%02d-%02d' % (x.year, x.month, x.day)
        return self.__super.conv (x)
    # end def conv
# end class Repr_Date

class Repr_Birthdate (Repr_Date) :
    def __call__ (self, itemid, col, x = None) :
        if x is None :
            x = self.klass.get (itemid, col)
        children = self.klass.filter (None, {'parent' : itemid})
        if children :
            x = ', '.join (self.conv 
                (self.klass.get (c, 'birthdate')) for c in children)
            return x
        x = x or ""
        return self.conv (x)
    # end def __call__
# end class Repr_Birthdate

class Repr_Country (Repr_Str) :
    def conv (self, x) :
        x = x.strip ()
        if x == 'CH' :
            return ''
        return self.__super.conv (x)
    # end def conv
# end class Repr_Country

class Repr_Multilink (Repr_Str) :
    def conv (self, x) :
        if x :
            x = ','.join (x)
        return self.__super.conv (x)
    # end def conv
# end class Repr_Multilink

def repr_link (klass, cls, cols) :
    class Repr_Link (Repr_Str) :
        def conv (self, x) :
            if x :
                x = " ".join (str (cls.get (x, c)) for c in cols)
            return self.__super.conv (x)
        # end def conv
    # end class Repr_Link
    return Repr_Link (klass)
# end def repr_link

def repr_func (klass, col) :
    idx = int (col.split ('.', 1)[1])
    class Repr_Func (Repr_Str) :
        def __call__ (self, itemid, col) :
            return self.__super.__call__ (itemid, 'function')
        # end def __call__

        def conv (self, x) :
            try :
                return self.__super.conv (x.split ('\n') [idx])
            except AttributeError :
                pass
            except IndexError :
                return ""
            return self.__super.conv (x)
        # end def conv
    # end class Repr_Func
    return Repr_Func (klass)
# end def repr_func

def repr_code (klass, adr_types) :
    class Repr_Code (Repr_Str) :
        def __call__ (self, itemid, col) :
            return self.__super.__call__ (itemid, 'adr_type')
        # end def __call__

        def conv (self, x) :
            for t in x :
                if t in adr_types :
                    return "A"
            return "0"
        # end def conv
    # end class Repr_Code
    return Repr_Code (klass)
# end def repr_code

class Export_CSV_Names (Action, autosuper) :
    name           = 'export'
    permissionType = 'View'
    print_head     = True
    filename       = 'query.csv'
    delimiter      = '\t'
    quotechar      = '"'
    quoting        = csv.QUOTE_MINIMAL
    csv_writer     = csv.writer

    def _setup (self) :
        columns    = self.request.columns
        if not columns :
            columns = self.props.keys ()
            columns.sort ()
        # full-text search
        if self.request.search_text :
            matches = self.db.indexer.search \
                (re.findall (r'\b\w{2,25}\b', self.request.search_text), klass)
        else :
            matches        = None
        self.columns       = columns
        self.print_columns = columns
        self.matches       = matches
    # end def _setup

    def build_repr (self) :
        """ Figure out Link columns and build representation methods for them
        """
        self.represent = {}

        repr_date      = Repr_Date      (self.klass)
        repr_str       = Repr_Str       (self.klass)
        repr_multilink = Repr_Multilink (self.klass)

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
                    (self.client, self.request.classname, itemid)
                return ep.as_listentry (item = item, as_link = False)
            # end def f
            return f
        # end def repr_extprop

        cts = self.db.contact_type.getnodeids (retired = False)
        cts = dict ((i, self.db.contact_type.get (i, 'name')) for i in cts)
        class Repr_Contact (Repr_Str) :
            def __call__ (self, itemid, col) :
                type = col.split ('.') [1]
                ccls = self.klass.db.contact
                contacts = self.klass.get (itemid, 'contacts') or []
                cnames = []
                for c in contacts :
                    co = ccls.getnode (c)
                    ct = cts [co.contact_type]
                    if type == 'Telefon' :
                        if ct != type and ct != 'Mobiltelefon' :
                            continue
                    else :
                        if ct != type :
                            continue
                    cnames.append (co.contact)
                x = ', '.join (cnames)
                return self.conv (x)
            # end def __call__
        # end class Repr_Contact

        for col in self.columns :
            self.represent [col] = repr_str
            if col.startswith ('function.') :
                self.represent [col] = repr_func (self.klass, col)
            elif '.' in col :
                if col.startswith ('contact.') :
                    self.represent [col] = Repr_Contact (self.klass)
                elif col.startswith ('type.') :
                    self.represent [col] = Repr_Type (self.klass)
                else :
                    self.represent [col] = repr_extprop (col)
            elif col not in self.props :
                pass
            elif isinstance (self.props [col], hyperdb.Link) :
                cn = self.props [col].classname
                cl = self.db.getclass (cn)
                pr = cl.getprops ()
                if 'lastname' in pr and cl.labelprop () != 'username' :
                    self.represent [col] = repr_link \
                        (self.klass, cl, ('firstname', 'lastname'))
                else :
                    self.represent [col] = repr_link \
                        (self.klass, cl, (cl.labelprop (),))
            elif isinstance (self.props [col], hyperdb.Multilink) :
                self.represent [col] = repr_multilink
            elif isinstance (self.props [col], hyperdb.Date) :
                self.represent [col] = repr_date
        self.represent ['birthdate'] = Repr_Birthdate (self.klass)
    # end def build_repr

    def handle (self) :
        ''' Export the specified search query as CSV. '''
        # figure the request
        request    = self.request = templating.HTMLRequest (self.client)
        self.utils = templating.TemplatingUtils (self.client)
        filterspec = request.filterspec
        sort       = request.sort
        group      = request.group
        klass      = self.klass = self.db.getclass (request.classname)
        self.props = klass.getprops ()
        self.htcls = templating.HTMLClass (self.client, request.classname)

        if self.db.user.properties.get ('csv_delimiter') :
            d = self.db.user.get (self.db.getuid (), 'csv_delimiter')
            if d and len (d) == 1 :
                self.delimiter = d

        self._setup ()

        h                        = self.client.additional_headers
        h ['Content-Type']       = 'text/csv'
        # some browsers will honor the filename here...
        h ['Content-Disposition'] = 'inline; filename=%s' % self.filename

        self.client.header ()

        if self.client.env ['REQUEST_METHOD'] == 'HEAD' :
            # all done, return a dummy string
            return 'dummy'

        io = StringIO ()
        writer = self.csv_writer \
            ( io
            , dialect   = 'excel'
            , delimiter = self.delimiter
            , quoting   = self.quoting
            , quotechar = self.quotechar
            )
        if self.print_head :
            writer.writerow (self.print_columns)

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
    filename   = 'ABO.CSV'
    quoting    = csv.QUOTE_NONE
    quotechar  = None

    def _setup (self) :
        self.columns = self.print_columns = \
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
        self.matches   = None
        self.delimiter = '\t'
    # end def _setup

    def build_repr (self) :
        self.__super.build_repr ()
        tc             = self.db.adr_type_cat.lookup ('ABO')
        self.adr_types = dict.fromkeys (self.db.adr_type.find (typecat = tc), 1)
        self.represent ['country'] = Repr_Country (self.klass)
        self.represent ['code']    = repr_code (self.klass, self.adr_types)
    # end def build_repr

# end class Export_CSV_Addresses

class Export_CSV_Legacy_Format (Export_CSV_Names) :
    filename   = 'export.csv'

    def _setup (self) :
        self.columns = \
            [ 'salutation'
            , 'title'
            , 'fullname'
            , 'street'
            , 'postalcode'
            , 'city'
            , 'birthdate'
            , 'contact.Telefon'
            , 'anm'
            , 'creation'
            , 'contact.Email'
            , 'type.Petition-EU'
            , 'type.DD-Vb'
            , 'type.G-DD-Vb'
            ]
        self.print_columns = \
            ( 'Anrede'
            , 'Titel'
            , 'Name'
            , 'Straße'
            , 'PLZ'
            , 'Ort'
            , 'Geburtsdatum'
            , 'Telefon'
            , 'Bemerkungen'
            , 'Eintragedatum'
            , 'E-mail'
            , 'EU-Aus-Pet.'
            , 'DD-Vb'
            , 'G-DD-Vb'
            )
        self.matches = None
    # end def _setup

    def build_repr (self) :
        self.__super.build_repr ()
        empty = lambda x, y : ''
        for k in 'anm', :
            self.represent [k] = empty
        self.represent ['fullname'] = Repr_Fullname (self.klass)
    # end def build_repr

# end class Export_CSV_Legacy_Format

class Export_TeX (Export_CSV_Names) :
    filename   = 'query.txt'
    csv_writer = TeX_CSV_Writer

    def _setup (self) :
        self.columns = \
            [ 'salutation'
            , 'nr'
            , 'street'
            , 'title'
            , 'firstname'
            , 'lastname'
            , 'function'
            , 'bez'
            , 'anm'
            , 'anschrift'
            , 'gruppe'
            , 'locked'
            , 'zh'
            , 'adrtyp'
            ]
        self.print_columns = \
            ( 'anrede'
            , 'nr'
            , 'strasse'
            , 'titel'
            , 'vorname'
            , 'zuname'
            , 'institut'
            , 'bez'
            , 'anm'
            , 'anschrift'
            , 'gruppe'
            , 'locked'
            , 'zh'
            , 'adrtyp'
            )
        self.matches   = None
        self.delimiter = ';'

    def build_repr (self) :
        self.__super.build_repr ()
        empty = lambda x, y : ''
        for k in 'nr', 'bez', 'anm', 'gruppe', 'locked', 'zh', 'adrtyp' :
            self.represent [k] = empty
        self.represent ['anschrift'] = Repr_Anschrift (self.klass)
    # end def build_repr

# end class Export_TeX

def init (instance) :
    instance.registerAction ('export_csv_names',        Export_CSV_Names)
    instance.registerAction ('export_csv_tex',          Export_TeX)
    instance.registerAction ('export_csv_addresses',    Export_CSV_Addresses)
    instance.registerAction ('export_legacy_addresses', Export_CSV_Legacy_Format)
# end def init
