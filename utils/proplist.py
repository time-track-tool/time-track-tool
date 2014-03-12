#!/usr/bin/python
import sys, os
from optparse          import OptionParser
from roundup           import date
from roundup           import instance

tracker = instance.open (os.getcwd ())
db      = tracker.open ('admin')

parser = OptionParser ()
parser.add_option \
    ( "-l", "--as_list"
    , dest    = "as_list"
    , help    = "Output as python list for use in regression test"
    , default = False
    , action  = "store_true"
    )
parser.add_option \
    ( "-s", "--search"
    , dest    = "search"
    , help    = "Check search permissions for each role"
    , default = False
    , action  = "store_true"
    )
opt, args = parser.parse_args ()

if len (args) :
    parser.error ('No arguments needed')
    exit (23)

if opt.as_list :
    print "properties = \\"
for clcnt, cl in enumerate (sorted (db.getclasses ())) :
    if opt.as_list :
        o = ','
        if clcnt == 0 :
            o = '['
        print "    %s ( '%s'" % (o, cl)
    else :
        print cl
    for n, p in enumerate (sorted (db.getclass (cl).properties.keys ())) :
        rs = ''
        if opt.search :
            rs = '( '
        if opt.as_list :
            if n :
                print "        , %s'%s'" % (rs, p)
            else :
                print "      , [ %s'%s'" % (rs, p)
        else :
            print "    ", p
        if opt.search :
            roles = []
            for role in sorted (db.security.role.iterkeys ()) :
                if db.security.roleHasSearchPermission (role, cl, p) :
                    roles.append (role)
            if opt.as_list :
                r = ', '.join ('"%s"' % r for r in roles)
                print '          , [%s]' % r
                print '          )'
            else :
                print "        ", ', '.join (roles)
    if opt.as_list :
        if not len (db.getclass (cl).properties) :
            print "      , ["
        print "        ]"
        print "      )"
if opt.as_list :
    print "    ]"
    print
    print "if __name__ == '__main__' :"
    print "    for cl, props in properties :"
    print "        print cl"
    print "        for p in props :"
    print "            print '    ', p"

