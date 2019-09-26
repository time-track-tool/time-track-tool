#!/usr/bin/python
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

infosec = dict (Normal = 10, High = 20, Special = 40)
infosec ['Very High'] = 30
for name in infosec :
    try :
        id = db.infosec_level.lookup (name)
        node = db.infosec_level.getnode (id)
        if not node.order :
            db.infosec_level.set (id, order = infosec [name])
    except KeyError :
        db.infosec_level.create (name = name, order = infosec [name])

db.commit()
