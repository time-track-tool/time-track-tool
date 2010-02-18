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

eps = 0.0001
class Err_Rec (object) :

    by_dri = {}

    def __init__ (self, db, dr, err) :
        self.db  = db
        self.dr  = dr
        self.by_tri = {tr.id : err}
        self.by_dri [dr.id] = self
    # end def __init__

    def append (self, trid, err) :
        assert (trid not in self.by_tri)
        self.by_tri [trid] = err
    # end def append

    @property
    def username (self) :
        return self.db.user.get (self.dr.user, 'username')
    # end def username

    def as_text (self) :
        s = []
        s.append \
            ( "Problem  for daily_record%s user:%s date:%s"
            % ( self.dr.id
              , self.username
              , self.dr.date.pretty ('%Y-%m-%d')
              )
            )
        for tr, err in sorted (self.by_tri.iteritems ()) :
            s.append (err)
        if abs (dr.tr_duration_ok - sum) < eps :
            s.append ("Problem but sum in daily_record OK")
        else :
            s.append \
                ( "Expected %s but got %s"
                % (sum, dr.tr_duration_ok)
                )
        return '\n'.join (s)
    # end def as_text

    @classmethod
    def try_new (cls, db, dr, tr, ratio, is_trvl) :
        err = None
        if is_trvl :
            tr_duration = ratio * tr.duration
        else :
            tr_duration = tr.duration
        if tr.tr_duration is None :
            err = "Problem: time_record%s has no tr_duration" % tr.id
        elif abs (tr.tr_duration - tr_duration) > eps :
            err = "Problem: expect %s, got %s for time_record%s" \
                % (tr_duration, tr.tr_duration, tr.id)
        if err :
            if dr.id not in cls.by_dri :
                obj = cls (db, dr, err)
            else :
                obj = cls.by_dri [dr.id]
                obj.append (tr.id, err)
    # end def try_new

    @classmethod
    def output (cls) :
        old = None
        for rec in sorted \
            ( cls.by_dri.itervalues ()
            , key = lambda x : (x.username, x.dr.date)
            ) :
            if old and old != rec.username :
                print rec.username
                old = rec.username
            print rec.as_text ()
    # end def output
# end class Err_Rec

for dri in db.daily_record.getnodeids () :
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
    if dur is not None :
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
            Err_Rec.try_new (db, dr, tr, ratio, tr.id in trvl_tr)
Err_Rec.output ()
