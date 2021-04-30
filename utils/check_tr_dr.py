#!/usr/bin/python
from __future__ import print_function

import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

# Check consistency of time_record link to daily record
#                  and daily_record multilink to time_record

verbose = True

# First loop over all time records and check that the tr->dr link and
# the backlink match

for trid in sorted (db.time_record.getnodeids (retired = False), key=int) :
    tr = db.time_record.getnode (trid)
    dr = db.daily_record.getnode (tr.daily_record)
    if verbose and (int (trid) % 100) == 0 :
        print ("tr%s\r" % trid, end = '')
        sys.stdout.flush ()
    if tr.id not in dr.time_record :
        print \
            ("No backlink in daily_record%s for time_record%s" % (dr.id, trid))

# Then loop over all daily records and check that the dr->tr multilink
# and all the backlinks match
for drid in sorted (db.daily_record.getnodeids (retired = False), key=int) :
    dr = db.daily_record.getnode (drid)
    if verbose and (int (drid) % 100) == 0 :
        print ("dr%s\r" % drid, end = '')
        sys.stdout.flush ()
    for trid in dr.time_record :
        tr = db.time_record.getnode (trid)
        if tr.daily_record != drid :
            print \
                ( "Invalid dr link in time_record%s: Got %s expected %s"
                % (trid, tr.daily_record, drid)
                )
