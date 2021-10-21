#!/usr/bin/python
import os
import sys
dir = os.getcwd ()
from csv               import DictWriter
from optparse          import OptionParser
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

    def __init__ (self, db, dr, tr, err, sum, tr_duration) :
        self.db  = db
        self.dr  = dr
        self.sum = sum
        self.by_tri = {tr.id : (tr, err, tr_duration)}
        self.by_dri [dr.id] = self
    # end def __init__

    def append (self, tr, err, tr_duration) :
        assert (tr.id not in self.by_tri)
        self.by_tri [tr.id] = (tr, err, tr_duration)
    # end def append

    @property
    def username (self) :
        return self.db.user.get (self.dr.user, 'username')
    # end def username

    def as_text (self) :
        s = []
        s.append \
            ( "Problem for daily_record%s user:%s date:%s"
            % ( self.dr.id
              , self.username
              , self.dr.date.pretty ('%Y-%m-%d')
              )
            )
        for trid in sorted (self.by_tri) :
            tr, err, trd = self.by_tri [trid]
            s.append (err)
        if abs (self.dr.tr_duration_ok - self.sum) < eps :
            s.append ("        but sum in daily_record OK")
        else :
            s.append \
                ( "        Expected %s but got %s for daily_record"
                % (self.sum, self.dr.tr_duration_ok)
                )
        s.append ('')
        return '\n'.join (s)
    # end def as_text

    fieldnames = \
        [ 'user'
        , 'date'
        , 'daily_record'
        , 'time_record'
        , 'sum_day'
        , 'sum_day_cached'
        , 'sum_tr'
        , 'sum_tr_cached'
        ]

    def as_csv (self, writer) :
        for trid in sorted (self.by_tri) :
            tr, err, trd = self.by_tri [trid]
            d = dict \
                ( user           = self.username
                , date           = self.dr.date.pretty ('%Y-%m-%d')
                , daily_record   = self.dr.id
                , time_record    = trid
                , sum_day        = self.sum
                , sum_day_cached = self.dr.tr_duration_ok
                , sum_tr         = trd
                , sum_tr_cached  = tr.tr_duration
                )
            writer.writerow (d)
    # end def as_csv

    @classmethod
    def csv_writer (cls, file) :
        w = DictWriter (file, cls.fieldnames, delimiter = ';')
        w.writerow (dict ((x, x) for x in cls.fieldnames))
        return w
    # end def csv_writer

    @classmethod
    def output (cls) :
        old = None
        for rec in sorted \
            ( cls.by_dri.values ()
            , key = lambda x : (x.username, x.dr.date)
            ) :
            if old != rec.username :
                print rec.username
                old = rec.username
            print rec.as_text ()
    # end def output

    @classmethod
    def output_csv (cls) :
        w = cls.csv_writer (sys.stdout)
        for rec in sorted \
            ( cls.by_dri.values ()
            , key = lambda x : (x.username, x.dr.date)
            ) :
            rec.as_csv (w)
    # end def output_csv

    @classmethod
    def try_new (cls, db, dr, tr, sum, ratio, is_trvl) :
        err = None
        if is_trvl :
            tr_duration = ratio * tr.duration
        else :
            tr_duration = tr.duration
        if tr.tr_duration is None :
            err = "        time_record%s has no tr_duration" % tr.id
        elif abs (tr.tr_duration - tr_duration) > eps :
            err = "        expect %s, got %s for time_record%s" \
                % (tr_duration, tr.tr_duration, tr.id)
        if err :
            if dr.id not in cls.by_dri :
                obj = cls (db, dr, tr, err, sum, tr_duration)
            else :
                obj = cls.by_dri [dr.id]
                assert (obj.sum == sum)
                obj.append (tr, err, tr_duration)
    # end def try_new

# end class Err_Rec

parser = OptionParser ()
parser.add_option \
    ( "-c", "--csv"
    , dest    = "csv"
    , help    = "Output in CSV format"
    , action  = "store_true"
    )
parser.add_option \
    ( "-e", "--end"
    , dest    = "end"
    , help    = "End-Date in YYYY-MM-DD format"
    , default = ''
    )
parser.add_option \
    ( "-s", "--start"
    , dest    = "start"
    , help    = "Start-Date in YYYY-MM-DD format"
    , default = ''
    )
opt, args = parser.parse_args ()

if opt.start or opt.end :
    ids = db.daily_record.filter (None, {'date' : opt.start + ';' + opt.end})
else :
    ids = db.daily_record.getnodeids ()

for dri in ids :
    dr  = db.daily_record.getnode (dri)
    dur = dr.tr_duration_ok
    hours = hhours = 0.0
    tr_full = True
    trs = []
    trvl_tr = {}
    dyn = get_user_dynamic (db, dr.user, dr.date)
    wh  = 0.0
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
            Err_Rec.try_new (db, dr, tr, sum, ratio, tr.id in trvl_tr)
if opt.csv :
    Err_Rec.output_csv ()
else :
    Err_Rec.output ()
