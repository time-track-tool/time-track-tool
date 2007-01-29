#!/usr/bin/python
import sys
import time
import csv
import os
import re
from roundup           import date
from textwrap          import fill
from roundup           import instance

arglen = len (sys.argv)
if arglen != 2 : 
    sys.stderr.write ('Usage: %s invoicelist\n' % sys.argv [0])
    sys.exit ()

list    = [i.strip () for i in open (sys.argv [1])]
tracker = instance.open ('/home/ralf/roundup/abo')
db      = tracker.open ('admin')
for i in list :
    db.invoice.set (i, send_it = False)
    print i
db.commit ()

