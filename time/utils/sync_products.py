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

def update_table (cls, nodedict, usedict, key, params) :
    if key in nodedict :
        # Update name on first match if we have a new spelling
        if not usedict [key] and nodedict [key].name != params ['name'] :
            cls.set (nodedict [key].id, name = params ['name'])
    else :
        id = cls.create (** params)
        nodedict [key] = db.prodcat.getnode (id)
    usedict [key] = True
    return nodedict [key]
# end def update_table

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

tracker = instance.open (opt.dir)
db      = tracker.open ('admin')

prodcats = {}
prodused = {}
for id in db.prodcat.getnodeids (retired = False) :
    pd  = db.prodcat.getnode (id)
    key = (normalize_name (pd.name.decode ('utf-8')), pd.level)
    prodused [key] = False
    prodcats [key] = pd

business_units = {}
bu_used        = {}
for id in db.business_unit.getnodeids (retired = False) :
    bu  = db.business_unit.getnode (id)
    key = normalize_name (pd.name.decode ('utf-8'))
    bu_used        [key] = False
    business_units [key] = bu

products = {}
pr_used  = {}
for id in db.product.getnodeids (retired = False) :
    pr  = db.product.getnode (id)
    key = normalize_name (pr.name.decode ('utf-8'))
    pr_used  [key] = False
    products [key] = pr

dr = DictReader (open (args [0], 'r'), delimiter = '\t')
levels = \
    { 'Product Line'     : 1
    , 'Product Use Case' : 2
    , 'Product Family'   : 3
    , 'Artikelnummer'    : 4
    }

for rec in dr :
    for k, lvl in levels.iteritems () :
        v = rec [k].strip ().decode ('latin1')
        if not v or v == '0' or v == '1' :
            continue
        key = (normalize_name (v), lvl)
        par = dict (name = v.encode ('utf-8'), level = lvl, valid = True)
        r = update_table (db.prodcat, prodcats, prodused, key, par)
        if lvl == 4 :
            pc4 = r

    v   = rec ['Selling BU'].decode ('latin1')
    key = normalize_name (v)
    par = dict (name = v.encode ('utf-8'), valid = True)
    bu  = update_table (db.business_unit, business_units, bu_used, key, par)

    v   = rec ['Artikelbeschreibung'].decode ('latin1')
    key = normalize_name (v)
    par = dict \
        ( name          = v.encode ('utf-8')
        , prodcat       = pc4.id
        , business_unit = bu.id
        , is_series     = False
        , valid         = True
        )
    update_table (db.product, products, pr_used, key, par)

if opt.update :
    db.commit()
