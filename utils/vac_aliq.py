#!/usr/bin/python
import sys
import os
from roundup           import date
from roundup           import instance

startdate = date.Date ('2018-01-01')
olos      = dict.fromkeys (('4', '5', '6', '35'))
vaold     = '1'
vanew     = '2'
vac_y     = 30

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

sys.path.insert (1, os.path.join (dir, 'lib'))

import user_dynamic

for n in 'Daily', 'Monthly' :
    try :
        db.vac_aliq.lookup (n)
    except KeyError :
        db.vac_aliq.create (name = n)
db.commit ()

# Loop over all org_locations and set vac_aliq if unset and
# do_leave_process is set. Also set the olos from above.

for id in db.org_location.getnodeids (retired = False) :
    olo = db.org_location.getnode (id)
    if id in olos :
        if not olo.vacation_yearly :
            db.org_location.set (id, vacation_yearly = vac_y)
    if olo.vac_aliq is not None :
        continue
    if id in olos :
        db.org_location.set (id, do_leave_process = True, vac_aliq = vanew)
    elif olo.do_leave_process :
        db.org_location.set (id, vac_aliq = vaold)
db.commit ()

# Loop over all existing absolute vacation corrections and set vac_aliq
# in respective user_dynamic records
for id in db.vacation_correction.filter (None, dict (absolute = True)) :
    vc  = db.vacation_correction.getnode (id)
    dyn = user_dynamic.first_user_dynamic (db, vc.user, date = vc.date)
    if not dyn :
        print "WARN: No dyn user %s/%s" % (vc.user, vc.date)
    while dyn :
        if dyn.vac_aliq is None :
            db.user_dynamic.set (dyn.id, vac_aliq = vaold)
        dyn = user_dynamic.next_user_dynamic (db, dyn)

db.commit ()
