from roundup import date

def import_data_3 (db, user) :
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-04')
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
        , date = date.Date ('2010-01-05')
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
        , date = date.Date ('2010-01-06')
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
        , date = date.Date ('2010-01-07')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:30'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.75
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '10:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '18:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-08')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '10:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.50
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '09:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '8'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:15'
        , end           = '11:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:15'
        , end           = '13:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '15:30'
        , work_location = '1'
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
        , duration      = 7.5
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
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:45'
        , end           = '13:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:45'
        , end           = '12:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '15:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '8'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:00'
        , end           = '18:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-12')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '9'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:45'
        , end           = '14:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:45'
        , end           = '18:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-13')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '19:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '13:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-14')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:30'
        , end           = '14:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '11:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-15')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:45'
        , work_location = '1'
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
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-19')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '13:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '11:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-20')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-21')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '19:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:30'
        , end           = '14:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-22')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '07:45'
        , end           = '12:15'
        , work_location = '1'
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
        , date = date.Date ('2010-01-25')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-26')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '13:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '8'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:00'
        , end           = '18:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-27')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.50
        , wp            = '10'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '13:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-28')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 6.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-29')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '13:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-30')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-01-31')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-01')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.50
        , wp            = '11'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '09:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-02')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '11:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.75
        , wp            = '2'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:30'
        , end           = '17:15'
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-03')
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
        , date = date.Date ('2010-02-04')
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
        , date = date.Date ('2010-02-05')
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
        , date = date.Date ('2010-02-06')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-07')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-08')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-09')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '19:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '14:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-10')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:00'
        , end           = '17:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-11')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '9'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-12')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-13')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-14')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-15')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-16')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-17')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:45'
        , end           = '19:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '14:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-18')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '12'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:30'
        , end           = '17:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-19')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-20')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-21')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-22')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '16:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.75
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '13:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.50
        , wp            = '9'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-23')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.50
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:00'
        , end           = '17:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-24')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-25')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.50
        , wp            = '13'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '13'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '07:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '16:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-26')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-27')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-02-28')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-01')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-02')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:00'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-03')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 6.00
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '19:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '13:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-04')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-05')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '11:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-06')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-07')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-08')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-09')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:00'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-10')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '11:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-11')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-12')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '11:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '12:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-13')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-14')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-15')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:00'
        , end           = '18:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-16')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:00'
        , end           = '19:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-17')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '15'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '15:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:45'
        , end           = '17:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-18')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.50
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:00'
        , end           = '17:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-19')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '10:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-20')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-21')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-22')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '9'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '15'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '10:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-23')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:00'
        , end           = '19:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-24')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-25')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:30'
        , end           = '15:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '11:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:30'
        , end           = '17:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-26')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '11:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '12:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-27')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-28')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-29')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '06:30'
        , end           = '08:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '09:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:00'
        , end           = '12:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-30')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.50
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '07:45'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '17:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-03-31')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '10:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.50
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '09:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-01')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.25
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '07:45'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-02')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-03')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-04')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-05')
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
        , date = date.Date ('2010-04-06')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '07:30'
        , end           = '08:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.50
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-07')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:45'
        , end           = '14:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:15'
        , end           = '18:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-08')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-09')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.75
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '10:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-10')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-11')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-12')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '18:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.25
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-13')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.75
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '18:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-14')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.75
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '19:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '13:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-15')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-16')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-17')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-18')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.75
        , wp            = '7'
        , time_activity = '11'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '13:30'
        , work_location = '3'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '17:30'
        , work_location = '3'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 6.25
        , wp            = '7'
        , time_activity = '10'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:30'
        , end           = '23:45'
        , work_location = '3'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-19')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.50
        , wp            = '7'
        , time_activity = '10'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '00:00'
        , end           = '00:30'
        , work_location = '3'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.75
        , wp            = '16'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:30'
        , end           = '17:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-20')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 6.00
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '19:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-21')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.50
        , wp            = '14'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-22')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '14:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '17'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-23')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '17'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:00'
        , end           = '14:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-24')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-25')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.75
        , wp            = '7'
        , time_activity = '10'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '14:30'
        , work_location = '3'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '7'
        , time_activity = '11'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '18:00'
        , work_location = '3'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '7'
        , time_activity = '11'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '18:30'
        , end           = '23:45'
        , work_location = '3'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-26')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '00:00'
        , end           = '02:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.50
        , wp            = '18'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '11:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '7'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:30'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '16:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-27')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:15'
        , end           = '17:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '18'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-28')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '17'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '14:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '17:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-29')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '17'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '13'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:00'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-04-30')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.50
        , wp            = '17'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '07:30'
        , end           = '13:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-01')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-02')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-03')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-04')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 6.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '19:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '13:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-05')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-06')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.50
        , wp            = '18'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:45'
        , end           = '17:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-07')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '11:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-08')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-09')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-10')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-11')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '19:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '14:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-12')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '15'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:00'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-13')
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
        , date = date.Date ('2010-05-14')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '11:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.00
        , wp            = '15'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:15'
        , end           = '12:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-15')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-16')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-17')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '13:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '17:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-18')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '11:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '18'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:00'
        , end           = '19:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-19')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-20')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-21')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-22')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-23')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-24')
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
        , date = date.Date ('2010-05-25')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '19:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '14:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-26')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-27')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-28')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-29')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-30')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2010-05-31')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    db.commit ()
# end def import_data_3
