#!/usr/bin/python3
import sys, os
import csv
from argparse import ArgumentParser
from roundup  import date
from roundup  import instance

def ldap_sync_type (to_ldap, frm_ldap) :
    if to_ldap and frm_ldap :
        return 'both'
    if to_ldap :
        return 'to ldap'
    if frm_ldap :
        return 'from ldap'
    return ''
# end def ldap_sync_type

def get_bool_cfg (db, name) :
    cfgitem = getattr (db.config.ext, name, None)
    if cfgitem :
        if cfgitem.lower () in ('true', 'yes', '1') :
            return True
        return False
    return None
# end def get_bool_cfg

parser = ArgumentParser ()
group  = parser.add_mutually_exclusive_group ()

group.add_argument \
    ( "-c", "--csv"
    , dest    = "as_csv"
    , help    = "Output as CSV"
    , default = False
    , action  = "store_true"
    )
group.add_argument \
    ( "-d", "--directory"
    , dest    = "directory"
    , help    = "Directory of Tracker"
    , default = '.'
    )
group.add_argument \
    ( "-D", "--delimiter"
    , dest    = "delimiter"
    , help    = "Delimiter for CSV"
    , default = '\t'
    )
group.add_argument \
    ( "-l", "--as-list"
    , dest    = "as_list"
    , help    = "Output as python list for use in regression test"
    , default = False
    , action  = "store_true"
    )
parser.add_argument \
    ( "-L", "--ldap"
    , dest    = "ldap"
    , help    = "Output LDAP attributes (currently only to csv)"
    , default = False
    , action  = "store_true"
    )
parser.add_argument \
    ( "-s", "--search"
    , dest    = "search"
    , help    = "Check search permissions for each role"
    , default = False
    , action  = "store_true"
    )
parser.add_argument \
    ( "-v", "--verbose"
    , dest    = "verbose"
    , help    = "Output types in addition to property names"
    , default = False
    , action  = "store_true"
    )
args = parser.parse_args ()

sys.path.insert (1, os.path.join (args.directory, 'lib'))
sys.path.insert (1, os.path.join (args.directory, 'extensions'))
from help      import combined_name
from ldap_sync import LDAP_Roundup_Sync
tracker = instance.open (args.directory)
db      = tracker.open ('admin')
_       = db.i18n.gettext

if args.as_csv :
    writer = csv.writer (sys.stdout, delimiter = args.delimiter)
    l = ['table', 'property', 'gui-name']
    if args.ldap :
        l.extend (('ldap attribute', 'sync direction'))
    writer.writerow (l)
if args.as_list :
    print ("properties = \\")
lds = None
if args.ldap :
    lds = LDAP_Roundup_Sync (db)
for clcnt, cl in enumerate (sorted (db.getclasses ())) :
    klass = db.getclass (cl)
    if args.as_list :
        o = ','
        if clcnt == 0 :
            o = '['
        print ("    %s ( '%s'" % (o, cl))
    elif args.as_csv :
        writer.writerow ((cl, '', _ (cl)))
    else :
        print (cl)
    for n, p in enumerate (sorted (klass.properties)) :
        rs = ''
        if args.search :
            rs = '( '
        if args.as_list :
            if n :
                print ("        , %s'%s'" % (rs, p))
            else :
                print ("      , [ %s'%s'" % (rs, p))
        elif args.as_csv :
            l = ['', p, _ (combined_name (cl, p))]
            if args.ldap and cl in ('user', 'user_contact') :
                assert cl in lds.attr_map
                if cl == 'user' :
                    amap = lds.attr_map ['user']
                    if p in amap :
                        l.append (amap [p][0])
                        to_ldap = \
                            (   bool (amap [p][1])
                            and get_bool_cfg (db, 'LDAP_UPDATE_LDAP')
                            )
                        frm_ldap = \
                            (   bool (amap [p][2])
                            and get_bool_cfg (db, 'LDAP_UPDATE_ROUNDUP')
                            )
                        l.append (ldap_sync_type (to_ldap, frm_ldap))
                elif p == 'contact' :
                    l.append \
                        ('by type: mail, telephoneNumber, mobile, pager')
                    to_ldap  = get_bool_cfg (db, 'LDAP_UPDATE_LDAP')
                    frm_ldap = get_bool_cfg (db, 'LDAP_UPDATE_ROUNDUP')
                    l.append (ldap_sync_type (to_ldap, frm_ldap))
            writer.writerow (l)
        else :
            if args.verbose :
                prp = klass.properties [p]
                typ = prp.__class__.__name__
                print ("    ", p, typ, getattr (prp, 'classname', ''))
            else :
                print ("    ", p)
        if args.search :
            roles = []
            for role in sorted (db.security.role) :
                if db.security.roleHasSearchPermission (cl, p, role) :
                    roles.append (role)
            if args.as_list :
                r = ', '.join ('"%s"' % r for r in roles)
                print ('          , [%s]' % r)
                print ('          )')
            else :
                print ("        ", ', '.join (roles))
    if args.as_list :
        if not len (db.getclass (cl).properties) :
            print ("      , [")
        print ("        ]")
        print ("      )")
if args.as_list :
    print ("    ]")
    print ()
    print ("if __name__ == '__main__' :")
    print ("    for cl, props in properties :")
    print ("        print cl")
    print ("        for p in props :")
    print ("            print '    ', p")

