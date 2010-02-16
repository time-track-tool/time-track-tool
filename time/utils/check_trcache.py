#!/usr/bin/python
import os
import sys
dir = os.getcwd ()
from roundup           import date
from roundup           import instance
sys.path.insert (0, os.path.join (dir, 'lib'))
from user_dynamic import round_daily_work_hours, get_user_dynamic
from user_dynamic import travel_worktime, day_work_hours
tracker  = instance.open (dir)
db       = tracker.open ('admin')

for dri in db.daily_record.getnodeids () :
    eps = 0.0001
    dr  = db.daily_record.getnode (dri)
    dur = dr.tr_duration_ok
    hours = hhours = 0.0
    tr_full = True
    trs = []
    trvl_tr = {}
    dyn = get_user_dynamic (db, dr.user, dr.date)
    oopsed = False
    if dyn :
        tr_full = dyn.travel_full
        wh = round_daily_work_hours (day_work_hours (dyn, dr.date))
    if dur is None :
        if dr.time_record :
            pass
            #print "Oops: daily_record%s has no tr_duration" % dri
    else :
        for tri in dr.time_record :
            tr = db.time_record.getnode (tri)
            trs.append (tr)
            hours += tr.duration
            act    = tr.time_activity
            trvl = not tr_full and act and db.time_activity.get (act, 'travel')
            if trvl :
                hhours += tr.duration / 2.
                trvl_tr [tri] = tr
            else :
                hhours += tr.duration
        sum, ratio = travel_worktime (hours, hhours, wh)
        for tr in trs :
            if tr.id in trvl_tr :
                tr_duration = ratio * tr.duration
            else :
                tr_duration = tr.duration
            if tr.tr_duration is None :
                if not oopsed :
                    print "Oops  for daily_record%s" % tri
                    oopsed = True
                print "Oops: time_record%s has not tr_duration" % tr.id
            elif abs (tr.tr_duration - tr_duration) > eps :
                if not oopsed :
                    print "Oops  for daily_record%s" % tri
                    oopsed = True
                print "Oops: expect %s, got %s for time_record%s" \
                    % (tr_duration, tr.tr_duration, tr.id)
        if oopsed and abs (dr.tr_duration_ok - sum) < eps :
            print "Oopsed but sum OK"
    oopsed = False
    
