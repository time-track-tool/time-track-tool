#!/usr/bin/python
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

countries = set (('Austria', 'Germany', 'Finland', 'Czechia', 'Romania'))

for id in db.vac_aliq.getnodeids (retired = False):
    va = db.vac_aliq.getnode (id)
    if va.name == 'Daily':
        db.vac_aliq.set (id, name = 'Austria')
        countries.remove ('Austria')
        continue
    elif va.name == 'Monthly':
        db.vac_aliq.set (id, name = 'Germany')
        countries.remove ('Germany')
        continue
    elif va.name in countries:
        countries.remove (va.name)
        continue
    else:
        print (va.name)
        assert 0
# Create remaining countries
for c in sorted (countries):
    db.vac_aliq.create (name = c)

db.commit()
