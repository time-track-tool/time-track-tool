#!/usr/bin/python
from __future__ import unicode_literals
from __future__ import print_function
import os
import re

from csv      import DictReader
from roundup  import instance
from argparse import ArgumentParser

splitre = re.compile (r'[ +_/&-]+')

def normalize_name (name) :
    """ Normalize a name from different case etc.
        We assume unicode input.
    >>> print (normalize_name ('Projects + Other'))
    PROJECTS-OTHER
    >>> print (normalize_name ('  Projects + Other  '))
    PROJECTS-OTHER
    >>> print (normalize_name ('PROJECTS-OTHER'))
    PROJECTS-OTHER
    >>> print (normalize_name ('PROJECTS+OTHER'))
    PROJECTS-OTHER
    >>> print (normalize_name ('PROJECTS-OTHERS'))
    PROJECTS-OTHER
    >>> print (normalize_name ('Other'))
    OTHER
    >>> print (normalize_name ('Others'))
    OTHER
    >>> print (normalize_name ('OTHERS'))
    OTHER
    >>> print (normalize_name ('Customized Kits'))
    CUSTOMIZED-KITS
    >>> print (normalize_name ('CUSTOMIZED-KITS'))
    CUSTOMIZED-KITS
    >>> print (normalize_name ('EV / Hybrid Vehicle ECU'))
    EV-HYBRID-VEHICLE-ECU
    >>> print (normalize_name (' EV / Hybrid Vehicle ECU '))
    EV-HYBRID-VEHICLE-ECU
    >>> print (normalize_name (' APC&RD'))
    APC-RD
    >>> print (normalize_name (' 012345'))
    12345
    >>> print (normalize_name ('012345 '))
    12345
    >>> print (normalize_name ('General Purpose ECUs / HMIs'))
    GENERAL-PURPOSE-ECUS-HMIS
    >>> print (normalize_name ('GENERAL-PURPOSE-ECUS/HMIS'))
    GENERAL-PURPOSE-ECUS-HMIS
    >>> print (normalize_name ('HY-eVision\xb2 7.0'))
    VISION2
    >>> print (normalize_name ('HY-TTC 200'))
    TTC-200
    >>> print (normalize_name ('HY-TTC 50'))
    TTC-50
    """
    x = '-'.join (l for l in splitre.split (name.upper ()) if l)
    if x == 'OTHERS' :
        x = 'OTHER'
    if x == 'PROJECTS-OTHERS' :
        x = 'PROJECTS-OTHER'
    if x.startswith ('HY-') :
        if x == 'HY-TTC-50' :
            x = 'TTC-50'
        if x == 'HY-TTC-200' :
            x = 'TTC-200'
        if x == 'HY-EVISION\xb2-7.0' :
            x = 'VISION2'
    try :
        x = str (int (x))
    except ValueError :
        pass
    return x
# end def normalize_name

class UTF8_Recoder (object) :

    def __init__ (self, f) :
        self.file = f
    # end def __init__

    def __iter__ (self) :
        for line in self.file :
            yield (line.encode ('utf-8'))
    # end def __iter__

# end class UTF8_Recoder


class Unicode_DictReader (object) :

    def __init__ (self, f, ** kw):
        f = UTF8_Recoder (f)
        self.reader = DictReader (f, ** kw)
    # end def __init__

    def __iter__ (self) :
        ''' Returns the next dict line as a Unicode dict
        '''
        for d in self.reader :
            r = []
            for k, v in d.iteritems () :
                k = k.decode ('utf-8')
                if v is not None :
                    v = v.decode ('utf-8')
                r.append ((k, v))
            yield dict (r)
    # end def __iter__

# end class Unicode_Reader

class Product_Sync (object) :

    levels  = \
        { ('Product Line', 'Product line')         : 1
        , ('Product Use Case', 'Product use-case') : 2
        , ('Product Family', 'Product family')     : 3
        }

    def __init__ (self, args) :
        self.args     = args
        tracker       = instance.open (args.dir)
        self.db       = db = tracker.open ('admin')
        self.prodcats = {}
        self.prodused = {}
        for id in db.prodcat.getnodeids (retired = False) :
            pd  = db.prodcat.getnode (id)
            nn  = normalize_name (pd.name.decode ('utf-8'))
            key = (nn, int (pd.level))
            self.prodused [key] = False
            self.prodcats [key] = pd.id

        self.products  = {}
        self.pr_used   = {}
        for id in db.product.getnodeids (retired = False) :
            pr  = db.product.getnode (id)
            key = normalize_name (pr.sap_material.decode ('utf-8'))
            self.pr_used  [key] = False
            self.products [key] = pr.id
        d_s = self.args.delimiter.encode ('utf-8')
        sap_dr = Unicode_DictReader \
            (self.fixer_sap (), delimiter = d_s)
        self.debug ("SAP")
        self.sap_recs = []
        self.sap_ids  = {}
        for x in sap_dr :
            self.debug (repr (x))
            id = self.get_material (x)
            if id in self.sap_ids :
                self.verbose ('Ignoring duplicate: %r' % x)
                continue
            self.sap_ids [id] = len (self.sap_recs)
            self.sap_recs.append (x)
            assert x is self.sap_recs [self.sap_ids [id]]
    # end def __init__

    def debug (self, text) :
        if self.args.debug :
            print (text)
    # end def debug

    def get_description (self, rec) :
        for n in 'Materialkurztext', 'Bezeichnung', 'Description' :
            try :
                v = rec [n]
                break
            except KeyError :
                pass
        else :
            raise
        return v
    # end def get_description

    def get_family (self, rec) :
        for keys in self.levels :
            if 'Product Family' in keys :
                break
        for n in keys :
            try :
                v = rec [n]
                break
            except KeyError :
                pass
        else :
            raise
        return v
    # end def get_family

    def get_material (self, rec) :
        for n in 'Material', 'Artikelkode', 'Material number' :
            try :
                v = rec [n]
                break
            except KeyError :
                pass
        else :
            raise
        try :
            v = str (int (v))
        except ValueError :
            pass
        return v
    # end def get_material

    def get_oldcode (self, rec) :
        """ The old code is no longer available in newer exports.
            We return an empty string in that case.
        """
        for n in 'Old material number', 'Alte Materialnr.', 'Alter Artikelkode':
            try :
                v = rec [n]
                break
            except KeyError :
                pass
        else :
            return ''
        try :
            v = str (int (v))
        except ValueError :
            pass
        return v
    # end def get_oldcode

    def fixer_sap (self) :
        with codecs.open (self.args.sapfile, 'r', self.args.encoding) as f :
            #l = f.next ()
            #assert 'MM Report Material Stammdaten' in l
            #l = f.next ()
            #assert l.strip () == ''
            #l = f.next ()
            #assert l.startswith ('MM Report Material Stammdaten')
            #l = f.next ()
            #assert l.strip () == ''
            #l = f.next ()
            #delim = self.args.delimiter
            #dd = delim * 2
            #assert ('%sMaterial' % delim) in l
            #n = 0
            #while dd in l :
            #    l = l.replace (dd, '%sIgnore-me%s%s' % (delim, n, delim), 1)
            #    n += 1
            #if l.startswith (delim) :
            #    l = 'Ignore-me%s' % n + l
            #    n += 1
            #if l.endswith (delim) :
            #    l = l + 'Ignore-me%s' % n
            #yield l
            for line in f :
                yield (line)
    # end def fixer_sap

    def rec_iter (self) :
        for id in sorted (self.sap_ids) :
            idx = self.sap_ids [id]
            yield self.sap_recs [idx]
    # end def rec_iter

    def sync (self) :
        skey = lambda x : x [1]
        for rec in self.rec_iter () :
            if not self.get_family (rec).strip () :
                self.warn ('Ignoring: %r' % rec)
                continue
            pcats = []
            for keys, lvl in sorted (self.levels.iteritems (), key = skey) :
                for k in keys :
                    try :
                        v = rec [k].strip ()
                        break
                    except KeyError :
                        pass
                else :
                    raise
                if not v or v == '0' or v == '1' :
                    self.warn ('Invalid record: %s=%s' % (k, v))
                    break
                key = (normalize_name (v), lvl)
                par = dict \
                    ( name   = v.encode ('utf-8')
                    , level  = lvl
                    , valid  = True
                    )
                r = self.update_table \
                    (self.db.prodcat, self.prodcats, self.prodused, key, par)
                pcats.append (r)

            v = self.get_material    (rec)
            d = self.get_description (rec)
            a = self.get_oldcode     (rec)
            if a == '-' :
                a = None
            n = a
            if not n :
                n = v

            key  = normalize_name (n)
            key2 = normalize_name (v)
            if key and key2 and key != key2 :
                k1 = k2 = None
                try :
                    k1 = int (key)
                    k2 = int (key2)
                except ValueError :
                    pass
                if k1 and k2 and k1 != k2 :
                    self.warn \
                        ( "Differing numeric Old/New material number: %s %s"
                        % (k1, k2)
                        )
                    #print (key, key2, a, n, v)
                    key2 = a = None
                    n = v
                    key = normalize_name (n)
                    #print (key, key2, a, n, v)
               
            if v and v != '0' and len (pcats) == 3 :
                par = dict \
                    ( name             = n.encode ('utf-8')
                    , description      = d.encode ('utf-8')
                    , sap_material     = v.encode ('utf-8')
                    , valid            = True
                    , product_family   = pcats [2]
                    , product_use_case = pcats [1]
                    , product_line     = pcats [0]
                    )
                self.debug (repr (par))
                p = self.update_table \
                    ( self.db.product
                    , self.products
                    , self.pr_used
                    , key
                    , par
                    , key2
                    )
        self.validity (self.db.prodcat,       self.prodcats, self.prodused)
        #self.validity (self.db.product,       self.products, self.pr_used)
        if self.args.update :
            self.db.commit()
    # end def sync

    def update_table (self, cls, nodedict, usedict, key, params, key2 = None) :
        assert key or key2
        if key2 and key != key2 and key in nodedict and key2 in nodedict :
            self.warn \
                ("Product %s with material-num %s found twice: %s/%s "
                 "using material number: %s"
                % (key, key2, nodedict [key], nodedict [key2], key2)
                )
            key = key2
            self.warn ("KEY: %s" % key2)
        k = key
        if key2 in nodedict :
            k = key2
        if k in nodedict :
            # Update name on first match if we have a new spelling
            if not usedict [k] :
                node = cls.getnode (nodedict [k])
                d = {}
                # We don't update name: This could only mean that up to
                # now we had the SAP-Name (which is fine) and found some
                # long-obsolete old-name in Radix.
                l = ( 'parent', 'prodcat', 'description', 'sap_material'
                    , 'product_family', 'product_line', 'product_use_case'
                    )
                for a in l :
                    if a in params and getattr (node, a) != params [a] :
                        d [str (a)] = params [a]
                if d :
                    self.verbose ("Update %s: %s: %s" % (cls.classname, k, d))
                    if self.args.update :
                        cls.set (nodedict [k], ** d)
        else :
            assert 'sap_material' in params or cls != self.db.product
            if 'sap_material' in params :
                params ['name'] = params ['sap_material']
            if key2 :
                k = key2
            if self.args.update :
                id = cls.create (** params)
            else :
                id = str ('999999') # fake id
            self.verbose \
                ("Create %s%s: %s: %s" % (cls.classname, id, k, params))
            nodedict [k] = id
        usedict [k] = True
        return nodedict [k]
    # end def update_table

    def validity (self, cls, nodedict, usedict) :
        for k, v in usedict.iteritems () :
            id = nodedict [k]
            if v or self.args.invalidate :
                if not v :
                    self.verbose \
                        ("Invalidating %s%s: %s" % (cls.classname, id, k))
                if self.args.update :
                    cls.set (id, valid = v)
    # end def validity

    def verbose (self, text) :
        if self.args.verbose :
            print (text)
    # end def verbose

    def warn (self, text) :
        print ('Warning: %s' % text)
    # end def warn

# end class Product_Sync

def main () :
    dir     = os.getcwd ()

    cmd = ArgumentParser ()
    cmd.add_argument \
        ( str ('sapfile')
        , help    = 'SAP import file'
        )
    cmd.add_argument \
        ( str ('-d'), str ('--directory')
        , dest    = 'dir'
        , help    = 'Tracker instance directory'
        , default = dir
        )
    cmd.add_argument \
        ( str ('--debug')
        , dest    = 'debug'
        , help    = 'Debug output'
        , action  = 'store_true'
        )
    cmd.add_argument \
        ( str ('-D'), str ('--sap-delimiter')
        , dest    = 'delimiter'
        , help    = 'CSV delimiter for SAP input-file,'
                    ' default = TAB'
        , default = '\t'
        )
    cmd.add_argument \
        ( str ('-E'), str ('--encoding')
        , dest    = 'encoding'
        , help    = 'CSV character encoding for SAP input-file,'
                    ' default = "%(default)s"'
        , default = 'latin1'
        )
    cmd.add_argument \
        ( str ('-i'), str ('--invalidate')
        , dest   = 'invalidate'
        , help   = 'Invalidate if not in import file'
        , action = 'store_true'
        )
    cmd.add_argument \
        ( str ('-u'), str ('--update')
        , dest   = 'update'
        , help   = 'Really do synchronisation'
        , action = 'store_true'
        )
    cmd.add_argument \
        ( str ('-v'), str ('--verbose')
        , dest   = 'verbose'
        , help   = 'Verbose output'
        , action = 'store_true'
        )
    args = cmd.parse_args ()

    ps = Product_Sync (args)
    ps.sync ()

if __name__ == '__main__' :
    import codecs
    import locale
    import sys
    sys.stdout = codecs.getwriter (locale.getpreferredencoding ())(sys.stdout)
    main ()
