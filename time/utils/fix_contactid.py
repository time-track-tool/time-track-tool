#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
import re
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()

tracker = instance.open (dir)
db      = tracker.open ('admin')

last = 0
for id in db.contact.getnodeids () :
    last = max (last, int (id))
db.setid ('contact', str (last))
db.commit ()

