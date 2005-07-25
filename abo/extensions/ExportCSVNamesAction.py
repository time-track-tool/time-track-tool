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

from roundup.cgi.actions import Action
from roundup.cgi import templating
from roundup import hyperdb

import csv
import re

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

class Export_CSV_Names (Action) :
    name = 'export'
    permissionType = 'View'

    def handle (self) :
        ''' Export the specified search query as CSV. '''
        # figure the request
        request    = templating.HTMLRequest (self.client)
        filterspec = request.filterspec
        sort       = request.sort
        group      = request.group
        columns    = request.columns
        klass      = self.db.getclass (request.classname)
        props      = klass.getprops ()
        if not columns :
            columns = props.keys ()
            columns.sort ()

        # full-text search
        if request.search_text :
            matches = self.db.indexer.search (
                re.findall (r'\b\w{2,25}\b', request.search_text), klass)
        else :
            matches = None

        h                        = self.client.additional_headers
        h ['Content-Type']       = 'text/csv'
        # some browsers will honor the filename here...
        h ['Content-Disposition'] = 'inline; filename=query.csv'

        self.client.header ()

        if self.client.env ['REQUEST_METHOD'] == 'HEAD' :
            # all done, return a dummy string
            return 'dummy'

        writer = csv.writer (self.client.request.wfile)
        writer.writerow (columns)

        # Figure out Link columns
        represent = {}

        def repr_link (cls, cols) :
            def f (x) :
                if x == None :
                    return ""
                else :
                    s = " ".join ([str (cls.get (x, col)) for col in cols])
                    return s.decode ('utf-8').encode ('latin1')
            return f
        # end def repr_link

        for col in columns :
            represent [col] = repr_str
            if isinstance (props [col], hyperdb.Link) :
                cn = props [col].classname
                cl = self.db.getclass (cn)
                pr = cl.getprops ()
                if 'lastname' in pr and cl.labelprop () != 'username' :
                    represent [col] = repr_link (cl, ('firstname', 'lastname'))
                else :
                    represent [col] = repr_link (cl, (cl.labelprop (),))
            elif isinstance (props [col], hyperdb.Date) :
                represent [col] = repr_date
            elif col.startswith ('function.') :
                idx = int (col.split ('.')[1])
                represent [col] = repr_func (idx)

        # and search
        for itemid in klass.filter (matches, filterspec, sort, group) :
            writer.writerow ([represent [col] (klass.get (itemid, col)) for 
                col in columns])

        return '\n'
    # end def handle
# end class Export_CSV_Names

def repr_func (idx) :
    def f (x) :
        try :
            return x.split ('\n', 2) [idx]
        except AttributeError :
            pass
        except IndexError :
            pass
        return ""
    return f

class Export_CSV_Addresses (Export_CSV_Names) :
    pass
# end class Export_Addresses

def init (instance) :
    instance.registerAction ('export_csv_names',     Export_CSV_Names)
    instance.registerAction ('export_csv_addresses', Export_CSV_Addresses)
# end def init
