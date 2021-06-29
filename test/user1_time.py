from roundup import date

def import_data_1 (db, user) :
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-01-23')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-01-24')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-01-25')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-01-26')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-01-27')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-01-28')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-01-29')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-06')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-07')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-08')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-09')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-10')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-11')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-12')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-13')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-14')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-15')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-16')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-17')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-18')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-02-19')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-03-20')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-03-21')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-03-22')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-03-23')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-03-24')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-03-25')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2006-03-26')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-12')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-13')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-14')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-30')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-01')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-02')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-03')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-04')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-05')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-06')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-07')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-08')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-09')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-10')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-11')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-12')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-13')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-14')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-15')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-16')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-17')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-18')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-19')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-20')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-21')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-22')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-23')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-24')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-25')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-26')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-27')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-28')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-29')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-12-30')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-23')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-24')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-25')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-26')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-27')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-28')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-29')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-01')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-02')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-03')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-04')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-05')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-06')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-07')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-08')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-09')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-10')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-11')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-12')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-13')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-14')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-15')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-16')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-17')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-18')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-19')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-20')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-21')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-11-22')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-01')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-02')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-03')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-04')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-05')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-06')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-07')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-08')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-09')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-10')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-11')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-12')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-13')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-14')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-15')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-16')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-17')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-18')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-19')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-20')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-21')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-22')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-23')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-24')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-25')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-26')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-27')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-28')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2009-10-29')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-03')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-04')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-05')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-04')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-05')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-06')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-07')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-08')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-09')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-10')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-01')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-02')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-03')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-11')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-15')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-16')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-17')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-18')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-19')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-20')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-21')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-22')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-23')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-24')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-07')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-08')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-09')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-31')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-01')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-02')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-06')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-25')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-26')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-27')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-28')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-29')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-30')
        )
    db.commit ()
# end def import_data_1
