#!/usr/bin/python
import os
import sys

from roundup import instance

tracker = instance.open('.')
db = tracker.open('admin')

# create new project types
db.project_type.create(name = 'Customer project',                          order = 1, valid = True)
db.project_type.create(name = 'Product development project',               order = 2, valid = True)
db.project_type.create(name = 'Research project',                          order = 3, valid = True)
db.project_type.create(name = 'Technical infrastructure internal project', order = 4, valid = True)
db.project_type.create(name = 'Organization internal project',             order = 5, valid = True)
db.project_type.create(name = 'Other Internal project',                    order = 6, valid = True)
db.project_type.create(name = 'Engineering service',                       order = 7, valid = True)
db.project_type.create(name = 'Maintenance & Support service',             order = 8, valid = True)

# deactive old project types and rank them down
db.project_type.set('1', order = 9,  valid = False)
db.project_type.set('2', order = 10, valid = False)
db.project_type.set('3', order = 11, valid = False)
db.project_type.set('4', order = 12, valid = False)
db.project_type.set('5', order = 13, valid = False)
db.project_type.set('6', order = 14, valid = False)
db.project_type.set('7', order = 15, valid = False)
db.commit()
