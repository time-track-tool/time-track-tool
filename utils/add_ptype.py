#!/usr/bin/python
import os
import sys
from roundup           import instance
from optparse          import OptionParser
from rsclib.autosuper  import autosuper
from roundup.hyperdb   import Multilink

tracker = instance.open ('.')
db      = tracker.open ('admin')

db.project_type.create (order = 1, name = 'Initial Development')
db.project_type.create (order = 2, name = 'Further Development')
db.project_type.create (order = 3, name = 'Maintenance')
db.project_type.create (order = 4, name = 'Support')
db.project_type.create (order = 5, name = 'Engineering')
db.commit()
