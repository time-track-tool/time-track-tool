#!/usr/bin/python

import sys
from argparse import ArgumentParser
from roundup  import instance, date
from csv      import DictReader

class CSV_Iter :

    def __init__ (self, f, firstline) :
        self.f         = f
        self.firstline = firstline
    # end def __init__

    def __iter__ (self) :
        yield self.firstline
        for line in self.f :
            yield line
    # end def __iter__

# end class CSV_Iter

def pg_iter (fn) :
    with open (fn, 'r') as f :
        for line in f :
            if not line.startswith (';SAP') :
                continue
            break
        it = CSV_Iter (f, line)
        dr = DictReader (it, delimiter = ';')
        for rec in dr :
            if not rec ['English'] :
                continue
            yield rec
# end def pg_iter

def las_iter (lasfile) :
    with open (lasfile, 'r') as f :
        for line in f :
            if line.startswith (';;;Type of Supplier') :
                break
        las = DictReader (f, delimiter = ';')
        for rec in las :
            yield rec
# end def las_iter

def insert_supplier_risk (db, sup, org, srcs) :
    for srg in srcs :
        src = srcs [srg]
        d   = dict \
            (supplier = sup, organisation = org, security_req_group = srg)
        srs = db.pr_supplier_risk.filter (None, d)
        assert len (srs) <= 1
        if len (srs) :
            sr = db.pr_supplier_risk.getnode (srs [0])
            if sr.supplier_risk_category != src :
                db.pr_supplier_risk.set (sr.id, supplier_risk_category = src)
        else :
            db.pr_supplier_risk.create \
                ( supplier               = sup
                , organisation           = org
                , security_req_group     = srg
                , supplier_risk_category = src
                )
# end def insert_supplier_risk

def main () :
    cmd = ArgumentParser ()
    cmd.add_argument \
        ( 'productgroups'
        , help = 'Product group matrix, SAP numbers'
        )
    cmd.add_argument \
        ( 'las'
        , help = 'LAS with supplier risk'
        )
    cmd.add_argument \
        ( '-d', '--directory'
        , dest    = 'dir'
        , help    = 'Tracker instance directory, default=%(default)s'
        , default = '.'
        )
    cmd.add_argument \
        ( '-o', '--orgmap'
        , help    = 'Mapping of organisations in LAS to tracker'
        , default = 'orglist'
        )
    cmd.add_argument \
        ( '-n', '--no_update'
        , dest    = 'update'
        , help    = 'Do not update tracker'
        , default = True
        , action  = 'store_false'
        )
    args    = cmd.parse_args ()
    tracker = instance.open (args.dir)
    db      = tracker.open ('admin')

    sys.path.insert (1, args.dir)
    from common import pretty_range

    orgmap = {}
    with open (args.orgmap) as f :
        dr = DictReader (f, delimiter = ';')
        for rec in dr :
            orgmap [rec ['name_las']] = rec ['names_prtracker'].split ('+')

    il = db.infosec_level
    il_ids = {}
    il_table = \
        [ ('Public',                10, True)
        #, ('Internal',              20, True)
        , ('Normal',                30, False)
        , ('Confidential',          40, True)
        , ('High',                  50, False)
        , ('Strictly Confidential', 60, True)
        , ('Very High',             70, False)
        ]
    try :
        special = il.lookup ('Special')
        il.retire (special)
    except KeyError :
        pass
    for name, order, cons in il_table :
        var = name.lower ()
        id  = None
        try :
            id = il.lookup (name)
        except KeyError :
            pass
        if id :
            node = il.getnode (id)
            d = {}
            if node.order != order :
                d ['order'] = order
            if node.name != name :
                d ['name'] = name
            if node.is_consulting is None or node.is_consulting != cons :
                d ['is_consulting'] = cons
            if d :
                il.set (id, ** d)
        else :
            id = il.create (name = name, order = order, is_consulting = cons)
        il_ids [var] = id
    il_ids ['normal / internal'] = il_ids ['normal']

    srg_table = \
        [ ('Consulting',        'Consulting',                    True)
        , ('Consulting_small',  'Consulting_small',              True)
        , ('COTS',              'COTS',                          False)
        , ('Operation',         'Operation & Operation support', False)
        , ('SW-Dev',            'Software development',          False)
#       , ('hw',                'Hardware',                      False)
        , ('Operation / cloud', 'Cloud based services',          False)
        , ('General',           'General',                       False)
        , ('General_small',     'General_small',                 False)
        ]
    srg = db.security_req_group
    srg_ids = {}
    srg_by_name = {}
    for var, name, is_consulting in srg_table :
        try :
            v = srg.lookup (name)
        except KeyError :
            v = srg.create (name = name, is_consulting = is_consulting)
        srg_ids [var] = v
        srg_by_name [name] = v
    # Lifting of broken LAS csv:
    srg_by_name ['COTS Software'] = srg_by_name ['COTS']
    del srg_by_name ['COTS']
    srg_by_name ['Cloud bases services (*AAS)'] = srg_by_name \
        ['Cloud based services']
    del srg_by_name ['Cloud based services']

    for rec in pg_iter (args.productgroups) :
        srg = rec ['ISEC-Requirements group'].strip ()
        if not srg :
            continue
        if srg == 'n.a.' or srg == 'n.a' or srg == 'TBD' :
            srg = None
        else :
            if srg.startswith ('n.a. /') :
                srg = srg [6:].strip ()
            srg = srg_ids [srg]
        name = rec ['English'].strip ()
        il = rec ['default protection level'].strip ()
        if il.startswith ('n.a. /') :
            il = il [6:].strip ()
        if not il or il == 'n.a.' :
            il = None
        else :
            il = il_ids [il]
        sap_ref = rec ['SAP neu'].strip ()
        try :
            db.product_group.lookup (name)
        except KeyError :
            d = dict \
                ( name               = name
                , sap_ref            = sap_ref
                )
            if il is not None :
                d ['infosec_level'] = il
            if srg is not None :
                d ['security_req_group'] = srg
            db.product_group.create (** d)

    src_ids = {}
    src_by_name = {}
    src_table = \
        [ ('low', 'Low',       10)
        , ('med', 'Medium',    20)
        , ('hi',  'High',      30)
        , ('vhi', 'Very High', 40)
        ]
    for var, name, order in src_table :
        try :
            id = db.supplier_risk_category.lookup (name)
        except KeyError :
            id = db.supplier_risk_category.create (name = name, order = order)
        src_ids [var] = id
        src_by_name [name] = id

    prt = db.purchase_risk_type
    prt_ids = {}
    prt_table = \
        [ ('low', 'Low',             10)
        , ('med', 'Medium',          20)
        , ('hi',  'High',            30)
        , ('vhi', 'Very High',       40)
        , ('dnp', 'Do not purchase', 50)
        ]
    for var, name, order in prt_table :
        try :
            id = prt.lookup (name)
        except KeyError :
            id = prt.create (name = name, order = order)
        prt_ids [var] = id

    # First bunch without a supplier_risk_category:
    # Supplier not in LAS or not evaluated
    # Then entries for each supplier_risk_category
    psr_table = \
        [ (None,  'public',                'med')
        #, (None,  'internal',              'hi')
        , (None,  'normal',                'hi')
        , (None,  'confidential',          'vhi')
        , (None,  'high',                  'vhi')
        , (None,  'strictly confidential', 'dnp')
        , (None,  'very high',             'dnp')
        # Low:
        , ('low', 'public',                'low')
        #, ('low', 'internal',              'low')
        , ('low', 'normal',                'low')
        , ('low', 'confidential',          'low')
        , ('low', 'high',                  'low')
        , ('low', 'strictly confidential', 'med')
        , ('low', 'very high',             'med')
        # Medium:
        , ('med', 'public',                'low')
        #, ('med', 'internal',              'med')
        , ('med', 'normal',                'med')
        , ('med', 'confidential',          'hi')
        , ('med', 'high',                  'hi')
        , ('med', 'strictly confidential', 'vhi')
        , ('med', 'very high',             'vhi')
        # High:
        , ('hi',  'public',                'med')
        #, ('hi',  'internal',              'hi')
        , ('hi',  'normal',                'hi')
        , ('hi',  'confidential',          'vhi')
        , ('hi',  'high',                  'vhi')
        , ('hi',  'strictly confidential', 'dnp')
        , ('hi',  'very high',             'dnp')
        # Very High:
        , ('vhi', 'public',                'hi')
        #, ('vhi', 'internal',              'dnp')
        , ('vhi', 'normal',                'dnp')
        , ('vhi', 'confidential',          'dnp')
        , ('vhi', 'high',                  'dnp')
        , ('vhi', 'strictly confidential', 'dnp')
        , ('vhi', 'very high',             'dnp')
        ]

    payment_types = \
        [ ('Invoice',     10, False)
        , ('Credit Card', 20, True)
        ]

    for src, il, prt in psr_table :
        d  = dict \
            ( infosec_level      = il_ids  [il]
            )
        dd = dict (d)
        d ['purchase_risk_type'] = prt_ids [prt]
        if src is None :
            dd ['supplier_risk_category'] = '-1'
        else :
            dd ['supplier_risk_category'] = src_ids [src]
            d  ['supplier_risk_category'] = src_ids [src]
        ids = db.purchase_security_risk.filter (None, dd)
        if ids :
            assert len (ids) == 1
            id = ids [0]
        else :
            id = db.purchase_security_risk.create (**d)
    for lasrec in las_iter (args.las) :
        if not lasrec ['Consulting_small'] :
            continue
        entity = lasrec ['Entity'].strip ()
        entity = orgmap.get (entity, [entity])
        sname  = lasrec ['Name of Supplier']
        try :
            sup = db.pr_supplier.lookup (sname)
        except KeyError :
            print ("Supplier not found: %s" % sname)
            continue
        srcs   = {}
        for k in srg_by_name :
            srgid = srg_by_name [k]
            if k in lasrec :
                srcs [srgid] = src_by_name [lasrec [k].strip ()]
            elif not k.startswith ('General') :
                raise ValueError ('Invalid LAS Entry: %s' % k)
        for e in entity :
            if e :
                try :
                    org = db.organisation.lookup (e)
                except KeyError :
                    print ("Organisation not found: %s" % e)
                    continue
                insert_supplier_risk (db, sup, org, srcs)
            else :
                # iter over valid orgs
                d = dict (may_purchase = True)
                d ['valid_from'] = ';.,-'
                d ['valid_to']   = '.;,-'
                for org in db.organisation.filter (None, d) :
                    insert_supplier_risk (db, sup, org, srcs)
                break
    for name, order, need in payment_types :
        try :
            pt = db.payment_type.lookup (name)
            pt = db.payment_type.getnode (pt)
            if need != pt.need_approval :
                db.payment_type.set (pt.id, need_approval = need)
        except KeyError :
            pt = db.payment_type.create \
                (name = name, order = order, need_approval = need)
    if args.update :
        db.commit ()
# end def main


if __name__ == '__main__' :
    main ()
