#!/usr/bin/python
import sys, os
from argparse          import ArgumentParser
from roundup           import date
from roundup           import instance

tracker = instance.open (os.getcwd ())
db      = tracker.open ('admin')

parser = ArgumentParser ()
parser.add_argument \
    ( "-l", "--as_list"
    , dest    = "as_list"
    , help    = "Output as python list for use in regression test"
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

if args.as_list :
    print "properties = \\"
for clcnt, cl in enumerate (sorted (db.getclasses ())) :
    klass = db.getclass (cl)
    if args.as_list :
        o = ','
        if clcnt == 0 :
            o = '['
        print "    %s ( '%s'" % (o, cl)
    else :
        print cl
    for n, p in enumerate (sorted (klass.properties.keys ())) :
        rs = ''
        if args.search :
            rs = '( '
        if args.as_list :
            if n :
                print "        , %s'%s'" % (rs, p)
            else :
                print "      , [ %s'%s'" % (rs, p)
        else :
            if args.verbose :
                prp = klass.properties [p]
                typ = prp.__class__.__name__
                print "    ", p, typ, getattr (prp, 'classname', '')
            else :
                print "    ", p
        if args.search :
            roles = []
            for role in sorted (db.security.role.iterkeys ()) :
                if db.security.roleHasSearchPermission (cl, p, role) :
                    roles.append (role)
            if args.as_list :
                r = ', '.join ('"%s"' % r for r in roles)
                print '          , [%s]' % r
                print '          )'
            else :
                print "        ", ', '.join (roles)
    if args.as_list :
        if not len (db.getclass (cl).properties) :
            print "      , ["
        print "        ]"
        print "      )"
if args.as_list :
    print "    ]"
    print
    print "if __name__ == '__main__' :"
    print "    for cl, props in properties :"
    print "        print cl"
    print "        for p in props :"
    print "            print '    ', p"

