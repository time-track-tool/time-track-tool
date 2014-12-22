#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import sys
from   roundup import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')
sys.path.insert (1, os.path.join (dir, 'lib'))

db.return_type.create (name = 'Field Return', order = 1)
db.return_type.create (name = '0-km Return',  order = 2)
db.return_type.create (name = 'Unknown',      order = 3)

db.analysis_result.create \
    (name = 'Unknown', description = 'Unknown error reason')

db.commit()
