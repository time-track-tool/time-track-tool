#!/usr/bin/python
#from __future__ import unicode_literals
import os
import re

from csv      import DictReader
from roundup  import instance
from optparse import OptionParser

splitre = re.compile (r'[ +_/&-]+')

def normalize_name (name) :
    """ Normalize a name from different case etc.
        We assume unicode input.
    >>> print normalize_name ('Projects + Other')
    PROJECTS-OTHER
    >>> print normalize_name ('PROJECTS-OTHER')
    PROJECTS-OTHER
    >>> print normalize_name ('PROJECTS+OTHER')
    PROJECTS-OTHER
    >>> print normalize_name ('Other')
    OTHER
    >>> print normalize_name ('Others')
    OTHER
    >>> print normalize_name ('OTHERS')
    OTHER
    >>> print normalize_name ('Customized Kits')
    CUSTOMIZED-KITS
    >>> print normalize_name ('CUSTOMIZED-KITS')
    CUSTOMIZED-KITS
    >>> print normalize_name ('EV / Hybrid Vehicle ECU')
    EV-HYBRID-VEHICLE-ECU
    >>> print normalize_name (' EV / Hybrid Vehicle ECU ')
    EV-HYBRID-VEHICLE-ECU
    >>> print normalize_name (' APC&RD')
    APC-RD
    """
    x = '-'.join (l for l in splitre.split (name.upper ()) if l)
    if x == 'OTHERS' :
        x = 'OTHER'
    return x
# end def normalize_name

class Product_Sync (object) :

    levels  = \
        { 'Product Line'     : 1
        , 'Product Use Case' : 2
        , 'Product Family'   : 3
        , 'Artikelnummer'    : 4
        }

    def __init__ (self, opt, args) :
        self.opt      = opt
        self.args     = args
        tracker       = instance.open (opt.dir)
        self.db       = db = tracker.open ('admin')
        self.prodcats = {}
        self.prodused = {}
        for id in db.prodcat.getnodeids (retired = False) :
            pd  = db.prodcat.getnode (id)
            key = (normalize_name (pd.name.decode ('utf-8')), pd.level)
            self.prodused [key] = False
            self.prodcats [key] = pd.id

        self.bu_s     = {}
        self.bu_used  = {}
        for id in db.business_unit.getnodeids (retired = False) :
            bu  = db.business_unit.getnode (id)
            key = normalize_name (bu.name.decode ('utf-8'))
            self.bu_used [key] = False
            self.bu_s    [key] = bu.id

        self.products  = {}
        self.pr_used   = {}
        for id in db.product.getnodeids (retired = False) :
            pr  = db.product.getnode (id)
            key = normalize_name (pr.name.decode ('utf-8'))
            self.pr_used  [key] = False
            self.products [key] = pr.id
    # end def __init__

    def sync (self) :
        dr = DictReader (open (self.args [0], 'r'), delimiter = '\t')

        for rec in dr :
            for k, lvl in self.levels.iteritems () :
                v = rec [k].strip ().decode ('latin1')
                if not v or v == '0' or v == '1' :
                    continue
                key = (normalize_name (v), lvl)
                par = dict \
                    (name = v.encode ('utf-8'), level = lvl, valid = True)
                r = self.update_table \
                    (self.db.prodcat, self.prodcats, self.prodused, key, par)
                if lvl == 4 :
                    pc4 = r

            v   = rec ['Selling BU'].decode ('latin1')
            key = normalize_name (v)
            par = dict (name = v.encode ('utf-8'), valid = True)
            bu  = None
            if v and v != 'ALL-BUSINESS-UNITS' and v != '0' :
                bu  = self.update_table \
                    (self.db.business_unit, self.bu_s, self.bu_used, key, par)

            v   = rec ['Artikelbeschreibung'].decode ('latin1')
            key = normalize_name (v)
            par = dict \
                ( name          = v.encode ('utf-8')
                , prodcat       = pc4
                , business_unit = bu
                , is_series     = False
                , valid         = True
                )
            self.update_table \
                (self.db.product, self.products, self.pr_used, key, par)
        self.validity (self.db.prodcat,       self.prodcats, self.prodused)
        self.validity (self.db.business_unit, self.bu_s,     self.bu_used)
        self.validity (self.db.product,       self.products, self.pr_used)
        if self.opt.update :
            self.db.commit()
    # end def sync

    def update_table (self, cls, nodedict, usedict, key, params) :
        if key in nodedict :
            # Update name on first match if we have a new spelling
            if not usedict [key] :
                name = cls.get (nodedict [key], 'name')
                if name != params ['name'] :
                    cls.set (nodedict [key], name = params ['name'])
        else :
            id = cls.create (** params)
            nodedict [key] = id
        usedict [key] = True
        return nodedict [key]
    # end def update_table

    def validity (self, cls, nodedict, usedict) :
        for k, v in usedict.iteritems () :
            id = nodedict [k]
            cls.set (id, valid = v)
    # end def validity

# end class Product_Sync

def main () :
    dir     = os.getcwd ()

    cmd = OptionParser ()
    cmd.add_option \
        ( '-d', '--directory'
        , dest    = 'dir'
        , help    = 'Tracker instance directory'
        , default = dir
        )
    cmd.add_option \
        ( '-u', '--update'
        , dest   = 'update'
        , help   = 'Really do synchronisation'
        , action = 'store_true'
        )
    cmd.add_option \
        ( '-v', '--verbose'
        , dest   = 'verbose'
        , help   = 'Verbose output'
        , action = 'store_true'
        )
    opt, args = cmd.parse_args ()
    if len (args) != 1 :
        cmd.error ('Need input file')
        sys.exit  (23)

    ps = Product_Sync (opt, args)
    ps.sync ()

if __name__ == '__main__' :
    main ()
