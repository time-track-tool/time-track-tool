#!/usr/bin/python
import sys, os
from roundup           import date
from roundup           import instance

tracker = instance.open (os.getcwd ())
db      = tracker.open ('admin')

as_list = False
if len (sys.argv) > 1 and sys.argv [1] == '--as_list' :
    as_list = True

if as_list :
    print "properties = \\"
for clcnt, cl in enumerate (sorted (db.getclasses ())) :
    if as_list :
        o = ','
        if clcnt == 0 :
            o = '['
        print "    %s ( '%s'" % (o, cl)
    else :
        print cl
    for n, p in enumerate (sorted (db.getclass (cl).properties.keys ())) :
        if as_list :
            if n :
                print "        , '%s'" % p
            else :
                print "      , [ '%s'" % p
        else :
            print "    ", p
    if as_list :
        if not len (db.getclass (cl).properties) :
            print "      , ["
        print "        ]"
        print "      )"
if as_list :
    print "    ]"
    print
    print "if __name__ == '__main__' :"
    print "    for cl, props in properties :"
    print "        print cl"
    print "        for p in props :"
    print "            print '    ', p"

