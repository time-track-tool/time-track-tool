#!/usr/bin/python
from __future__ import unicode_literals
from __future__ import print_function
import os
import re

from csv      import DictReader
from roundup  import instance
from optparse import OptionParser

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
        { 'Product Line'     : 1
        , 'Product Use Case' : 2
        , 'Product Family'   : 3
        }

    def __init__ (self, opt, args) :
        self.opt      = opt
        self.args     = args
        tracker       = instance.open (opt.dir)
        self.db       = db = tracker.open ('admin')
        self.prodcats = {}
        self.prodused = {}
        # Retire some unused product categories:
        #for n in 'HY-eVision\xb2 7.0', 'HY-TTC 200', 'HY-TTC 50' :
        #    ps = db.prodcat.filter (None, dict (level = 3, name = n))
        #    if not ps :
        #        continue
        #    assert len (ps) == 1
        #    c = ps [0]
        #    print ("Retire prodcat%s: %r" % (c, n))
        #    db.prodcat.retire (c)
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
            key = normalize_name (pr.name.decode ('utf-8'))
            self.pr_used  [key] = False
            self.products [key] = pr.id
        d_s = self.opt.delimiter.encode ('utf-8')
        sap_dr = Unicode_DictReader \
            (self.fixer_sap (), delimiter = d_s)
        d_r = self.opt.radix_delimiter.encode ('utf-8')
        rad_dr = Unicode_DictReader \
            (self.fixer_rad (), delimiter = d_r)
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
        self.debug ("RADIX")
        self.rad_recs = []
        self.rad_ids  = {}
        for x in rad_dr :
            self.debug (repr (x))
            id = self.get_material (x)
            if id in self.rad_ids :
                self.verbose ('Ignoring duplicate: %r' % x)
                continue
            self.rad_ids [id] = len (self.rad_recs)
            self.rad_recs.append (x)
            assert x is self.rad_recs [self.rad_ids [id]]
        for id in self.rad_ids :
            try :
                id = int (id)
            except ValueError :
                self.warn ("Ignoring Radix ID: %s" % id)
            if id > 11500 :
                self.warn ("Ignoring Radix ID: %s" % id)
            # Radix wins for IDs < 11500
            if str (id) in self.sap_ids :
                mat = self.get_material \
                    (self.sap_recs [self.sap_ids [str (id)]])
                assert (str (id) == mat)
                self.warn ("Ignoring SAP ID: %s (also in Radix)" % id)
                del self.sap_ids  [str (id)]
        for id in self.sap_ids :
            assert id not in self.rad_ids
    # end def __init__

    def debug (self, text) :
        if self.opt.debug :
            print (text)
    # end def debug

    def get_material (self, rec) :
        for n in 'Material', 'Artikelkode' :
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

    def get_description (self, rec) :
        for n in 'Materialkurztext', 'Bezeichnung' :
            try :
                v = rec [n]
                break
            except KeyError :
                pass
        else :
            raise
        return v
    # end def get_description

    def get_oldcode (self, rec) :
        for n in 'Alte Materialnr.', 'Alter Artikelkode' :
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
    # end def get_oldcode

    def fixer_sap (self) :
        with codecs.open (self.args [0], 'r', self.opt.encoding) as f :
            l = f.next ()
            assert 'MM Report Material Stammdaten' in l
            l = f.next ()
            assert l.strip () == ''
            l = f.next ()
            assert l.startswith ('MM Report Material Stammdaten')
            l = f.next ()
            assert l.strip () == ''
            l = f.next ()
            assert l.startswith ('%sMaterial' % self.opt.delimiter)
            yield (('Ignore-me%s' % l))

            for line in f :
                yield (line)
    # end def fixer_sap

    def fixer_rad (self) :
        if len (self.args) < 2 :
            raise StopIteration ()
        with codecs.open (self.args [1], 'r', self.opt.radix_encoding) as f :
            for line in f :
                yield (line)
    # end def fixer_rad

    def rec_iter (self) :
        for id in sorted (self.rad_ids) :
            idx = self.rad_ids [id]
            yield self.rad_recs [idx]
        for id in sorted (self.sap_ids) :
            idx = self.sap_ids [id]
            yield self.sap_recs [idx]
    # end def rec_iter

    def sync (self) :
        skey = lambda x : x [1]
        for rec in self.rec_iter () :
            if not rec ['Product Family'] :
                self.warn ('Ignoring: %r' % rec)
                continue
            pcats = []
            for k, lvl in sorted (self.levels.iteritems (), key = skey) :
                v = rec [k].strip ()
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
        if self.opt.update :
            self.db.commit()
    # end def sync

    def update_table (self, cls, nodedict, usedict, key, params, key2 = None) :
        assert key or key2
        if key2 and key != key2 and key in nodedict and key2 in nodedict :
            self.warn \
                ("Product %s with material-num %s found twice: %s/%s"
                % (key, key2, nodedict [key], nodedict [key2])
                )
            return None
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
                    if self.opt.update :
                        cls.set (nodedict [k], ** d)
        else :
            if 'sap_material' in params :
                params ['name'] = params ['sap_material']
            if key2 :
                k = key2
            if self.opt.update :
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
            if v or self.opt.invalidate :
                if not v :
                    self.verbose \
                        ("Invalidating %s%s: %s" % (cls.classname, id, k))
                if self.opt.update :
                    cls.set (id, valid = v)
    # end def validity

    def verbose (self, text) :
        if self.opt.verbose :
            print (text)
    # end def verbose

    def warn (self, text) :
        print ('Warning: %s' % text)
    # end def warn

# end class Product_Sync

def main () :
    dir     = os.getcwd ()

    cmd = OptionParser ("Usage: %prog [options] sap-inputfile radix-inputfile")
    cmd.add_option \
        ( str ('-d'), str ('--directory')
        , dest    = 'dir'
        , help    = 'Tracker instance directory'
        , default = dir
        )
    cmd.add_option \
        ( str ('--debug')
        , dest    = 'debug'
        , help    = 'Debug output'
        , action  = 'store_true'
        )
    cmd.add_option \
        ( str ('-D'), str ('--sap-delimiter')
        , dest    = 'delimiter'
        , help    = 'CSV delimiter for SAP input-file'
        , default = '\t'
        )
    cmd.add_option \
        ( str ('-R'), str ('--radix-delimiter')
        , dest    = 'radix_delimiter'
        , help    = 'CSV delimiter for Radix input-file'
        , default = '\t'
        )
    cmd.add_option \
        ( str ('-E'), str ('--encoding')
        , dest    = 'encoding'
        , help    = 'CSV character encoding for SAP input-file'
        , default = 'latin1'
        )
    cmd.add_option \
        ( str ('-e'), str ('--radix-encoding')
        , dest    = 'radix_encoding'
        , help    = 'CSV character encoding for Radix input-file'
        , default = 'utf-16'
        )
    cmd.add_option \
        ( str ('-i'), str ('--invalidate')
        , dest   = 'invalidate'
        , help   = 'Invalidate if not in import file'
        , action = 'store_true'
        )
    cmd.add_option \
        ( str ('-u'), str ('--update')
        , dest   = 'update'
        , help   = 'Really do synchronisation'
        , action = 'store_true'
        )
    cmd.add_option \
        ( str ('-v'), str ('--verbose')
        , dest   = 'verbose'
        , help   = 'Verbose output'
        , action = 'store_true'
        )
    opt, args = cmd.parse_args ()
    if not (1 <= len (args) <= 2) :
        cmd.error ('Need one or two input files')
        sys.exit  (23)

    ps = Product_Sync (opt, args)
    ps.sync ()

if __name__ == '__main__' :
    import codecs
    import locale
    import sys
    sys.stdout = codecs.getwriter (locale.getpreferredencoding ())(sys.stdout)
    main ()
