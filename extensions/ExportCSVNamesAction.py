#! /usr/bin/python3
# Copyright (C) 2004-22 Dr. Ralf Schlatterbeck Open Source Consulting.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import csv
import re
import sys
import codecs
from io import StringIO

from datetime              import datetime
from roundup.cgi.actions   import Action, SearchAction
from roundup.cgi           import templating
from roundup               import hyperdb
from roundup.date          import get_timezone, UTC

from rsclib.autosuper      import autosuper
from rsclib.TeX_CSV_Writer import TeX_CSV_Writer

from extproperty           import ExtProperty
from common                import get_num_locale
from request_util          import True_Value

locale = None

def charsetconv (x):
    return x
# end def charsetconv

class Repr_Str (autosuper):
    def __init__ (self, klass):
        self.klass    = klass
        self.props    = klass.getprops ()
    # end def __init__

    def conv (self, x):
        return charsetconv (x)
    # end def conv

    def __call__ (self, itemid, col, x = None):
        self.col = col
        if x is None:
            x = self.klass.get (itemid, col)
        x = x or ""
        return self.conv (x)
    # end def __call__
# end class Repr_Str

class Repr_Number (Repr_Str):
    def conv (self, x):
        if x is None:
            return ""
        return locale.format_string ("%2.2f", x)
    # end def conv

    def __call__ (self, itemid, col, x = None):
        if x is None:
            x = self.klass.get (itemid, col)
        return self.conv (x)
    # end def __call__
# end class Repr_Number

class Repr_Anschrift (Repr_Str):
    def __call__ (self, itemid, col):
        fields = ('postalcode', 'city')
        x = ' '.join (self.klass.get (itemid, z) for z in fields)
        country = self.klass.get (itemid, 'country')
        if country != 'A':
            x = country + '-' + x
        return self.conv (x)
    # end def __call__
# end class Repr_Anschrift

class Repr_Fullname (Repr_Str):
    def __call__ (self, itemid, col):
        fields = ('lastname', 'firstname', 'function')
        x = ' '.join \
            (y for y in (self.klass.get (itemid, z) for z in fields) if y)
        x = x.replace ('\n', ' ')
        return self.conv (x)
    # end def __call__
# end class Repr_Fullname

class Repr_Notice (Repr_Str):
    def __call__ (self, itemid, col):
        ccls = self.klass.db.msg
        retstr = []
        for id in (self.klass.get (itemid, 'messages') or []):
            date = ccls.get (id, 'date')
            if date:
                retstr.append \
                    ('%04d-%02d-%02d' % (date.year, date.month, date.day) + ':')
            retstr.append (ccls.get (id, 'content').replace ('\n', ' '))
        return self.conv (' '.join (retstr))
    # end def __call__
# end class Repr_Notice

class Repr_Type (Repr_Str):
    def __call__ (self, itemid, col):
        x = ''
        try:
            type = self.klass.db.adr_type.lookup (col.split ('.') [1])
        except KeyError:
            return self.conv (x)
        klass = self.klass
        id    = itemid
        if 'address' in self.props:
            klass = self.klass.db.address
            id    = self.klass.get (itemid, 'address')
        if type in klass.get (id, 'adr_type'):
            x = 'ja'
        return self.conv (x)
    # end def __call__
# end class Repr_Type

class Repr_Date (Repr_Str):
    fulldate = 'measurement', 'usage', 'event', 'event_day'
    def conv (self, x):
        if x:
            tz = self.props [self.col].offset (self.klass.db)
            d  = x.local (tz)
            if self.klass.classname in self.fulldate:
                return \
                    ( '%2d.%02d.%04d %02d:%02d:%02d'
                    % (d.day, d.month, d.year, d.hour, d.minute, d.second)
                    )
            else:
                return '%4d-%02d-%02d' % (d.year, d.month, d.day)
        return self.__super.conv (x)
    # end def conv
# end class Repr_Date

class Repr_Birthdate (Repr_Date):
    def __call__ (self, itemid, col, x = None):
        if x is None:
            x = self.klass.get (itemid, col)
        children = self.klass.filter (None, {'parent': itemid})
        if children:
            x = ', '.join (self.conv 
                (self.klass.get (c, 'birthdate')) for c in children)
            return x
        x = x or ""
        return self.conv (x)
    # end def __call__
# end class Repr_Birthdate

class Repr_Country (Repr_Str):
    def conv (self, x):
        x = x.strip ()
        if x == 'CH':
            return ''
        return self.__super.conv (x)
    # end def conv
# end class Repr_Country

class Repr_Multilink (Repr_Str):

    def __call__ (self, itemid, col, x = None):
        self.col = col
        if x is None:
            itm = self.klass.get (itemid, col)
            cls = self.klass.db.getclass (self.props [col].classname)
            lbl = cls.labelprop ()
            x = [cls.get (i, lbl) for i in itm]
        x = x or ""
        return self.conv (x)
    # end def __call__

    def conv (self, x):
        if x:
            x = ','.join (x)
        return self.__super.conv (x)
    # end def conv
# end class Repr_Multilink

def repr_link (klass, cls, cols):
    class Repr_Link (Repr_Str):
        def conv (self, x):
            if x:
                x = " ".join (str (cls.get (x, c)) for c in cols)
            return self.__super.conv (x)
        # end def conv
    # end class Repr_Link
    return Repr_Link (klass)
# end def repr_link

def repr_func (klass, col):
    idx = int (col.split ('.', 1)[1])
    class Repr_Func (Repr_Str):
        def __call__ (self, itemid, col):
            return self.__super.__call__ (itemid, 'function')
        # end def __call__

        def conv (self, x):
            try:
                return self.__super.conv (x.split ('\n') [idx])
            except AttributeError:
                pass
            except IndexError:
                return ""
            return self.__super.conv (x)
        # end def conv
    # end class Repr_Func
    return Repr_Func (klass)
# end def repr_func

def repr_code (klass, adr_types):
    class Repr_Code (Repr_Str):
        def __call__ (self, itemid, col):
            prefix = ''
            if 'address' in self.props:
                prefix = 'address.'
            return self.__super.__call__ (itemid, '%sadr_type' % prefix)
        # end def __call__

        def conv (self, x):
            for t in x:
                if t in adr_types:
                    return "A"
            return "0"
        # end def conv
    # end class Repr_Code
    return Repr_Code (klass)
# end def repr_code

class Export_CSV_Names (Action, autosuper):
    name           = 'export'
    permissionType = 'View'
    print_head     = True
    filename       = 'query.csv'
    delimiter      = '\t'
    quotechar      = '"'
    quoting        = csv.QUOTE_MINIMAL
    csv_writer     = csv.writer

    def _setup_request (self, setup_filter = False):
        """ figure the request """
        if setup_filter:
            self.fakeFilterVars ()
        request    = self.request = templating.HTMLRequest (self.client)
        self.utils = templating.TemplatingUtils (self.client)
        filterspec = self.filterspec = request.filterspec
        self.sort  = request.sort
        self.group = request.group
        self.klass = self.klass = self.db.getclass (request.classname)
        self.props = self.klass.getprops ()
        self.htcls = templating.HTMLClass (self.client, request.classname)

        if self.db.user.properties.get ('csv_delimiter'):
            d = self.db.user.get (self.db.getuid (), 'csv_delimiter')
            if d and len (d) == 1:
                self.delimiter = d
        global locale
        locale = get_num_locale (self.client, self.db)
    # end def _setup_request

    def _setup (self):
        columns    = self.request.columns
        if not columns:
            columns = list (self.props)
            columns.sort ()
        # full-text search
        if self.request.search_text:
            matches = self.db.indexer.search \
                ( re.findall (r'\b\w{2,25}\b', self.request.search_text)
                , self.klass
                )
        else:
            matches        = None
        self.columns       = \
            [c for c in columns
             if c.split ('.', 1)[0] in self.klass.getprops ()
            ]
        self.print_columns = self.columns
        self.matches       = matches
    # end def _setup

    def build_repr (self):
        """ Figure out Link columns and build representation methods for them
        """
        self.represent = {}

        repr_date      = Repr_Date      (self.klass)
        repr_str       = Repr_Str       (self.klass)
        repr_multilink = Repr_Multilink (self.klass)
        repr_number    = Repr_Number    (self.klass)

        def repr_extprop (col):
            parts = col.split ('.', 1)
            prop  = self.htcls [parts [0]]
            ep    = ExtProperty \
                ( self.utils, prop
                , searchname  = col
                , pretty      = str
                , text_only   = True
                )
            def f (itemid, col):
                item = templating.HTMLItem \
                    (self.client, self.request.classname, itemid)
                s = ep.as_listentry (item = item, as_link = False)
                return charsetconv (s)
            # end def f
            return f
        # end def repr_extprop

        if 'contact_type' in self.db.classes:
                cts = self.db.contact_type.getnodeids (retired = False)
                cts = dict \
                    ((i, self.db.contact_type.get (i, 'name')) for i in cts)
                class Repr_Contact (Repr_Str):
                    def __call__ (self, itemid, col):
                        type = col.split ('.') [1]
                        ccls = self.klass.db.contact
                        contacts = self.klass.get (itemid, 'contacts') or []
                        cnames = []
                        for c in contacts:
                            co = ccls.getnode (c)
                            ct = cts [co.contact_type]
                            if type == 'Telefon':
                                if ct != type and ct != 'Mobiltelefon':
                                    continue
                            else:
                                if ct != type:
                                    continue
                            cnames.append (co.contact)
                        x = ', '.join (cnames)
                        return self.conv (x)
                    # end def __call__
                # end class Repr_Contact

        for col in self.columns:
            self.represent [col] = repr_str
            if col.startswith ('function.'):
                self.represent [col] = repr_func (self.klass, col)
            elif '.' in col:
                if col.startswith ('contact.'):
                    self.represent [col] = Repr_Contact (self.klass)
                elif col.startswith ('type.'):
                    self.represent [col] = Repr_Type (self.klass)
                else:
                    self.represent [col] = repr_extprop (col)
            elif col not in self.props:
                pass
            elif isinstance (self.props [col], hyperdb.Link):
                cn = self.props [col].classname
                cl = self.db.getclass (cn)
                pr = cl.getprops ()
                if 'lastname' in pr and cl.labelprop () != 'username':
                    self.represent [col] = repr_link \
                        (self.klass, cl, ('firstname', 'lastname'))
                else:
                    self.represent [col] = repr_link \
                        (self.klass, cl, (cl.labelprop (),))
            elif isinstance (self.props [col], hyperdb.Multilink):
                self.represent [col] = repr_multilink
            elif isinstance (self.props [col], hyperdb.Date):
                self.represent [col] = repr_date
            elif isinstance (self.props [col], hyperdb.Number):
                self.represent [col] = repr_number
        self.represent ['birthdate'] = Repr_Birthdate (self.klass)
    # end def build_repr

    def hasTransitivePermission (self, perm, itemid, classname, property):
        if '.' in property:
            cls = self.db.getclass (classname)
            for pn in property.split ('.'):
                if itemid is None:
                    return True
                prop = cls.getprops () [pn]
                if isinstance (itemid, list):
                    for i in itemid:
                        if not self.hasTransitivePermission \
                            (perm, i, cls.classname, pn):
                            return False
                    return True
                elif not self.hasPermission \
                    ( perm
                    , itemid    = itemid
                    , classname = cls.classname
                    , property  = pn
                    ):
                    return False
                itemid = cls.get (itemid, pn)
                cls = None
                try:
                    cls = self.db.getclass (prop.classname)
                except AttributeError:
                    pass
            return True
        else:
            return self.hasPermission \
                ( perm
                , itemid    = itemid
                , classname = classname
                , property  = property
                )
    # end def hasTransitivePermission

    def handle (self, outfile = None):
        ''' Export the specified search query as CSV. '''
        self._setup_request ()
        self._setup ()
        filterspec = self.filterspec

        h                        = self.client.additional_headers
        h ['Content-Type']       = 'text/csv'
        # some browsers will honor the filename here...
        h ['Content-Disposition'] = 'inline; filename=%s' % self.filename

        self.client.header ()

        if self.client.env ['REQUEST_METHOD'] == 'HEAD':
            # all done, return a dummy string
            return 'dummy'

        wfile  = self.setup_wfile (outfile)
        writer = self.csv_writer \
            ( wfile
            , dialect   = 'excel'
            , delimiter = self.delimiter
            , quoting   = self.quoting
            , quotechar = self.quotechar
            )
        if self.print_head:
            writer.writerow (self.print_columns)

        self.build_repr ()

        # and search
        for itemid in self.klass.filter_with_permissions \
            (self.matches, filterspec, self.sort, self.group):
            self.client._socket_op \
                ( writer.writerow 
                , ([['', self.represent [col] (itemid, col)]
                    [self.hasTransitivePermission
                        ( 'View'
                        , itemid    = itemid
                        , classname = self.request.classname
                        , property  = col
                        )
                    ]
                   for col in self.columns
                       if col.split ('.', 1)[0] in self.klass.getprops ()]
                  )
                )
        return True_Value ('')
    # end def handle

    def setup_wfile (self, outfile):
        wfile = outfile
        if wfile is None:
            wfile = self.client.request.wfile
        if sys.version_info [0] > 2:
            wfile = codecs.getwriter (self.client.charset) (wfile, 'replace')
        elif self.client.charset != self.client.STORAGE_CHARSET:
            wfile = codecs.EncodedFile \
                ( wfile
                , self.client.STORAGE_CHARSET
                , self.client.charset
                , 'replace'
                )
        return wfile
    # end def setup_wfile

# end class Export_CSV_Names

class Export_CSV_Addresses (Export_CSV_Names):

    print_head = False
    filename   = 'ABO.CSV'
    quoting    = csv.QUOTE_NONE
    quotechar  = None

    def _setup (self):
        prefix = ''
        if 'address' in self.props:
            prefix = 'address.'
        self.columns = self.print_columns = \
            [ 'title'
            , 'firstname'
            , 'lastname'
            , 'function.0'
            , 'function.1'
            , 'function.2'
            , prefix + 'street'
            , prefix + 'country'
            , prefix + 'postalcode'
            , prefix + 'city'
            , 'code'
            ]
        self.matches   = None
        self.delimiter = '\t'
    # end def _setup

    def build_repr (self):
        self.__super.build_repr ()
        tc             = self.db.adr_type_cat.lookup ('ABO')
        self.adr_types = dict.fromkeys (self.db.adr_type.find (typecat = tc), 1)
        self.represent ['country'] = Repr_Country (self.klass)
        self.represent ['code']    = repr_code (self.klass, self.adr_types)
    # end def build_repr

# end class Export_CSV_Addresses

class Export_CSV_Legacy_Format (Export_CSV_Names):
    filename   = 'export.csv'

    def _setup (self):
        self.__super._setup ()
        prefix = ''
        if 'address' in self.props:
            prefix = 'address.'
        self.columns = \
            [ 'salutation'
            , 'title'
            , 'fullname'
            , prefix + 'street'
            , prefix + 'postalcode'
            , prefix + 'city'
            , 'birthdate'
            , 'contact.Telefon'
            , 'notice'
            , 'creation'
            , 'activity'
            , 'contact.Email'
            , 'type.Petition-EU'
            , 'type.DD-Vb'
            , 'type.G-DD-Vb'
            ]
        self.print_columns = \
            ( 'Anrede'
            , 'Titel'
            , 'Name'
            , 'Strasse'
            , 'PLZ'
            , 'Ort'
            , 'Geburtsdatum'
            , 'Telefon'
            , 'Bemerkungen'
            , 'Eintragedatum'
            , 'Letzte Aenderung'
            , 'E-mail'
            , 'EU-Aus-Pet.'
            , 'DD-Vb'
            , 'G-DD-Vb'
            )
        self.filterspec ['parent'] = '-1'
    # end def _setup

    def build_repr (self):
        self.__super.build_repr ()
        empty = lambda x, y: ''
        self.represent ['notice']   = Repr_Notice (self.klass)
        self.represent ['fullname'] = Repr_Fullname (self.klass)
    # end def build_repr

# end class Export_CSV_Legacy_Format

class Export_CSV_Lielas (Export_CSV_Names, SearchAction):
    def handle (self, outfile = None):
        ''' Export the specified search query as special CSV format. '''
        ''' Export the specified search query as CSV. '''
        self._setup_request (True)
        self._setup         ()

        h                        = self.client.additional_headers
        h ['Content-Type']       = 'text/csv'
        # some browsers will honor the filename here...
        h ['Content-Disposition'] = 'inline; filename=%s' % self.filename

        self.client.header ()

        if self.client.env ['REQUEST_METHOD'] == 'HEAD':
            # all done, return a dummy string
            return 'dummy'

        sensorspec = {}
        for k in self.filterspec:
            v = self.filterspec [k]
            if k.startswith ('sensor.'):
                sensorspec [k [7:]] = v
            if k == 'sensor':
                sensorspec ['id'] = v

        sensor_sort = \
            [ 'device.device_group'
            , 'device.order'
            , 'device.name'
            , 'device.adr'
            , 'order'
            , 'name'
            , 'adr'
            ]

        last_dg = last_d = None
        lines   = [[''], [''], ['Adr.'], ['date/time'], ['']]
        sids    = []
        for s in self.db.sensor.filter_iter \
            (None, sensorspec, group = [('+', k) for k in sensor_sort]):
            s  = self.db.sensor.getnode (s)
            d  = self.db.device.getnode (s.device)
            if d.device_group:
                dg = self.db.device_group.getnode (d.device_group)
            else:
                dg = None
            if dg and dg.id != last_dg:
                lines [0].append (charsetconv (dg.name))
                last_dg = dg.id
            else:
                lines [0].append ('')
            if d.id != last_d:
                lines [1].append (charsetconv (d.name))
                lines [2].append (charsetconv (d.adr))
                last_d = d.id
            else:
                lines [1].append ('')
                lines [2].append ('')
            lines [3].append (charsetconv (s.name))
            lines [4].append (charsetconv (s.unit))
            sids.append (s.id)
        index_by_sid = {}
        for n, sid in enumerate (sids):
            index_by_sid [sid] = n + 1

        wfile  = self.setup_wfile (outfile)
        writer = self.csv_writer \
            ( wfile
            , dialect   = 'excel'
            , delimiter = self.delimiter
            , quoting   = self.quoting
            , quotechar = self.quotechar
            )
        for l in lines:
            self.client._socket_op (writer.writerow, l)

        sort = []
        for dir, key in self.group + self.sort:
            if key == 'date':
                sort.append ((dir, key))
                break
        else:
            sort.append (('+', 'date'))
        for k in sensor_sort:
            sort.append (('+', 'sensor.' + k))

        repr_date   = Repr_Date   (self.klass)
        repr_number = Repr_Number (self.klass)
        # and search
        last_date = None
        line      = None
        tz = self.klass.getprops () ['date'].offset (self.db)
        # optimized sql version for postgres (maybe would work for
        # mysql, too, sqlite won't work, it doesn't return date as a
        # datetime object
        if self.db.__module__.endswith ('back_postgresql'):
            TZ = get_timezone (tz)
            classname = self.klass.classname
            proptree, sql, args = self.klass._filter_sql \
                (self.matches, self.filterspec, sort, retr=1)
            classes = {}
            for p in proptree:
                if 'retrieve' in p.need_for:
                    cn   = p.parent.classname
                    if cn != classname:
                        continue
                    ptid = p.parent.id
                    key  = (cn, ptid)
                    if key not in classes:
                        classes [key] = ptdict = {}
                    classes [key][p.name] = p
            assert (len (classes) == 1)
            self.db.sql (sql, args)
            while True:
                row = self.db.cursor.fetchone ()
                if not row: break
                nodeid = str (row [ptdict ['id'].sql_idx])
                sens   = str (row [ptdict ['sensor'].sql_idx])
                dt     = row [ptdict ['date'].sql_idx]
                val    = row [ptdict ['val'].sql_idx]
                if dt != last_date:
                    if line:
                        self.client._socket_op (writer.writerow, line)
                    last_date = dt
                    line = [''] * (len (sids) + 2)
                    dt   = datetime (tzinfo = UTC, *dt.timetuple ()[:6])
                    line [0] = dt.astimezone (TZ).strftime \
                        ('%02d.%02m.%04Y %H:%M:%S')
                line [index_by_sid [sens]] = locale.format_string ("%2.2f", val)
        else:
            for itemid in self.klass.filter_iter \
                (self.matches, self.filterspec, sort):
                item = self.klass.getnode (itemid)
                if item.date != last_date:
                    if line:
                        self.client._socket_op (writer.writerow, line)
                    last_date = item.date
                    line = [''] * (len (sids) + 2)
                    d = item.date.local (tz)
                    line [0] = '%02d.%02d.%04d %02d:%02d:%02d' \
                        % (d.day, d.month, d.year, d.hour, d.minute, d.second)
                line [index_by_sid [item.sensor]] = locale.format_string \
                    ("%2.2f", item.val)
        if line:
            self.client._socket_op (writer.writerow, line)

        return True_Value ()
    # end def handle
# end class Export_CSV_Lielas

class Export_TeX (Export_CSV_Names):
    filename   = 'query.txt'
    csv_writer = TeX_CSV_Writer

    def _setup (self):
        self.__super._setup ()
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
        self.delimiter = ';'
    # end def _setup

    def build_repr (self):
        self.__super.build_repr ()
        empty = lambda x, y: ''
        for k in 'nr', 'bez', 'anm', 'gruppe', 'locked', 'zh', 'adrtyp':
            self.represent [k] = empty
        self.represent ['anschrift'] = Repr_Anschrift (self.klass)
    # end def build_repr

# end class Export_TeX

def init (instance):
    instance.registerAction ('export_csv_names',     Export_CSV_Names)
    instance.registerAction ('export_csv_tex',       Export_TeX)
    instance.registerAction ('export_csv_addresses', Export_CSV_Addresses)
    instance.registerAction ('export_legacy',        Export_CSV_Legacy_Format)
    instance.registerAction ('export_csv_lielas',    Export_CSV_Lielas)
# end def init
