from roundup import date

def import_data_4 (db, user) :
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-06-18')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-06-19')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-06-20')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-06-21')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-06-22')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-06-23')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-06-24')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-08-13')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-08-14')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-08-15')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-08-16')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-08-17')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-08-18')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-08-19')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-02')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-03')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-04')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-05')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-06')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.25
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-07')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-08')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-09')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-10')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-11')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-12')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-13')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 6.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-14')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-15')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-16')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-17')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-18')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-19')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-20')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.25
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-21')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-22')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-23')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-24')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-25')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-26')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-27')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-28')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-29')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-30')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-01-31')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-01')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-02')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-03')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-04')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-05')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-06')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '2'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-07')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '2'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-08')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '2'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-09')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '2'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-10')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '2'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-11')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-12')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-13')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-14')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-15')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-16')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-17')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-18')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-19')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-20')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-21')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-22')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-23')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-24')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-25')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-26')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-27')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-28')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-02-29')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-01')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-02')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-03')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-04')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-05')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-06')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-07')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-08')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-09')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-10')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-11')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-12')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-13')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-14')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-15')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-16')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-17')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-18')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-19')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-20')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-21')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-22')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-23')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.25
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-24')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-25')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-26')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-27')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-28')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-29')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-30')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-03-31')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-01')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-02')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-03')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-04')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-05')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-06')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-07')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-08')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-09')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-10')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-11')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-12')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-13')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-14')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-15')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-16')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-17')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-18')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-19')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-20')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-21')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-22')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-23')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-24')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-25')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-26')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-27')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-28')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-29')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-04-30')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.25
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-01')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-02')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-03')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-04')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 12.0
        , wp            = '3'
        , time_activity = '10'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-05')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-06')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-07')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-08')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-09')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 9.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-10')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-11')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-12')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-13')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-14')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-15')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-16')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-17')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-18')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-19')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-20')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-21')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-22')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-23')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-24')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-25')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-26')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-27')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-28')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-29')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-30')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-05-31')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-06-01')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-06-02')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-06-03')
        )
    db.commit ()
# end def import_data_4
