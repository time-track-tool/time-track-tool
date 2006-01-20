#!/usr/bin/python2.4

import sys
import textwrap

from Roundup_Access import Roundup_Access
from roundup.date   import Date

if __name__ == '__main__' :
    if len (sys.argv) != 3 :
        print "Usage: %s <tracker> <org_location>"
        sys.exit (23)

    ra  = Roundup_Access (sys.argv [1], 'dc=tttech,dc=com')
    olo = ra.Org_Location (sys.argv [2])
    print olo.as_dhcp ()

