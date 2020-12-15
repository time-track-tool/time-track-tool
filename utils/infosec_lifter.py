#!/usr/bin/python

from argparse import ArgumentParser
from roundup  import instance
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

def main () :
    cmd = ArgumentParser ()
    cmd.add_argument \
        ( 'productgroups'
        , help = 'Product group matrix, SAP numbers'
        )
    cmd.add_argument \
        ( str ('-d'), str ('--directory')
        , dest    = 'dir'
        , help    = 'Tracker instance directory, default=%(default)s'
        , default = '.'
        )
    args    = cmd.parse_args ()
    tracker = instance.open (args.dir)
    db      = tracker.open ('admin')

    il = db.infosec_level
    il_ids = {}
    il_table = \
        [ ('Public',                10, True)
        , ('Internal',              20, True)
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

    srg_table = \
        [ ('Consulting',        'Consulting',                    True)
        , ('Consulting_small',  'Consulting_small',              True)
        , ('COTS',              'COTS',                          False)
        , ('Operation',         'Operation & Operation Support', False)
        , ('SW-Dev',            'Software development',          False)
#       , ('hw',                'Hardware',                      False)
        , ('Operation / cloud', 'Cloud based services',          False)
        ]
    srg = db.security_req_group
    srg_ids = {}
    for var, name, is_consulting in srg_table :
        try :
            v = srg.lookup (name)
        except KeyError :
            v = srg.create (name = name, is_consulting = is_consulting)
        srg_ids [var] = v

    for rec in pg_iter (args.productgroups) :
        srg = rec ['ISEC-Requirements group'].strip ()
        if not srg :
            continue
        if srg == 'n.a.' or srg == 'n.a' :
            srg = None
        else :
            if srg == 'n.a. / COTS' :
                srg = 'COTS'
            srg = srg_ids [srg]
        name = rec ['English'].strip ()
        il = rec ['default protection level'].strip ()
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
        , (None,  'internal',              'hi')
        , (None,  'normal',                'hi')
        , (None,  'confidential',          'vhi')
        , (None,  'high',                  'vhi')
        , (None,  'strictly confidential', 'dnp')
        , (None,  'very high',             'dnp')
        # Low:
        , ('low', 'public',                'low')
        , ('low', 'internal',              'low')
        , ('low', 'normal',                'low')
        , ('low', 'confidential',          'low')
        , ('low', 'high',                  'low')
        , ('low', 'strictly confidential', 'med')
        , ('low', 'very high',             'med')
        # Medium:
        , ('med', 'public',                'low')
        , ('med', 'internal',              'med')
        , ('med', 'normal',                'med')
        , ('med', 'confidential',          'hi')
        , ('med', 'high',                  'hi')
        , ('med', 'strictly confidential', 'vhi')
        , ('med', 'very high',             'vhi')
        # High:
        , ('hi',  'public',                'med')
        , ('hi',  'internal',              'hi')
        , ('hi',  'normal',                'hi')
        , ('hi',  'confidential',          'vhi')
        , ('hi',  'high',                  'vhi')
        , ('hi',  'strictly confidential', 'dnp')
        , ('hi',  'very high',             'dnp')
        # Very High:
        , ('vhi', 'public',                'hi')
        , ('vhi', 'internal',              'dnp')
        , ('vhi', 'normal',                'dnp')
        , ('vhi', 'confidential',          'dnp')
        , ('vhi', 'high',                  'dnp')
        , ('vhi', 'strictly confidential', 'dnp')
        , ('vhi', 'very high',             'dnp')
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
    db.commit ()
# end def main


if __name__ == '__main__' :
    main ()
