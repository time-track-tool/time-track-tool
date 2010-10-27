#!/usr/bin/python

import sys

# pretty print error message for inclusion in regression test
for line in sys.stdin :
    if line.startswith ('AssertionError:') :
        try :
            errmsg = line.split ('!=', 1) [1]
            l = eval (errmsg)
            if isinstance (l, tuple) :
                print "CLASS:", l [0]
                l = l [1]
            for n, (k, v) in enumerate (l) :
                if n :
                    print "        ,",
                else :
                    print "      , [",
                if isinstance (v, type ([])) :
                    print '( %r\n          , %r\n          )' % (k, v)
                else :
                    print '(%r, %r)' % (k, v)
            print '        ]'
        except ValueError:
            print "Unparseable error message:"
            print line.rstrip ()
    else :
        print line.rstrip ()
    sys.stdout.flush ()

