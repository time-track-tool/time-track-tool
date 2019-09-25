#!/usr/bin/python
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

infosec = ('Default (High)', 'Very High', 'Special')
for name in infosec :
    try :
        db.infosec_level.lookup (name)
    except KeyError :
        db.infosec_level.create (name = name)

db.commit()
