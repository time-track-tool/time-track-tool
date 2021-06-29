from roundup import date

def import_data_7 (db, user) :
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-15')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '4'
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
        , duration      = 4.25
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '17:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-16')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '07:45'
        , end           = '12:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:45'
        , end           = '16:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-17')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-18')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-19')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '5'
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
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:30'
        , end           = '18:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-20')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.50
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '17:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-21')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '07:45'
        , end           = '13:15'
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
        , start         = '13:45'
        , end           = '16:15'
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
        , start         = '16:15'
        , end           = '18:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-22')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '4'
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
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '5'
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
        , date = date.Date ('2012-11-23')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.50
        , wp            = '8'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '07:30'
        , end           = '09:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '4'
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
        , duration      = 2.50
        , wp            = '5'
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
        , duration      = 2.25
        , wp            = '6'
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
        , date = date.Date ('2012-11-24')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-25')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-26')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:15'
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
        , start         = '12:45'
        , end           = '14:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:15'
        , end           = '17:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-27')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.75
        , wp            = '4'
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
        , duration      = 2.50
        , wp            = '4'
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
        , date = date.Date ('2012-11-28')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '10:15'
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
        , start         = '10:15'
        , end           = '12:15'
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
        , start         = '12:45'
        , end           = '14:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:45'
        , end           = '17:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-29')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '13:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:45'
        , end           = '17:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-11-30')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '07:00'
        , end           = '12:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:45'
        , end           = '16:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-01')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-02')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-03')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:15'
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
        , start         = '12:45'
        , end           = '15:45'
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
        , start         = '15:45'
        , end           = '17:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-04')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '8'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:45'
        , end           = '15:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:45'
        , end           = '18:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-05')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.00
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '11:15'
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
        , start         = '11:15'
        , end           = '12:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:45'
        , end           = '16:30'
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
        , start         = '16:30'
        , end           = '18:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-06')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '4'
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
        , duration      = 4.50
        , wp            = '8'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '17:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-07')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '8'
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
        , duration      = 1.25
        , wp            = '5'
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
        , date = date.Date ('2012-12-08')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-09')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-10')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.50
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '10:45'
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
        , start         = '10:45'
        , end           = '12:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.00
        , wp            = '5'
        , time_activity = '10'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:15'
        , end           = '18:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-11')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '4'
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
        , duration      = 2.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '15:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '5'
        , time_activity = '10'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:45'
        , end           = '17:00'
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
        , start         = '17:00'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-12')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.50
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.25
        , wp            = '5'
        , time_activity = '10'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:00'
        , end           = '21:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-13')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '07:45'
        , end           = '09:00'
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
        , start         = '09:00'
        , end           = '10:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '5'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:30'
        , end           = '13:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.75
        , wp            = '8'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:15'
        , end           = '16:00'
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
        , start         = '16:00'
        , end           = '18:00'
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
        , start         = '18:00'
        , end           = '20:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-14')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.75
        , wp            = '6'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.75
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:15'
        , end           = '15:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-15')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-16')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-17')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '4'
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
        , duration      = 3.00
        , wp            = '4'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.50
        , wp            = '8'
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
        , date = date.Date ('2012-12-18')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-19')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-20')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-21')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-22')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-23')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-24')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '5'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '2'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '16:45'
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-25')
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
        , date = date.Date ('2012-12-26')
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
        , date = date.Date ('2012-12-27')
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
        , date = date.Date ('2012-12-28')
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
        , date = date.Date ('2012-12-29')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-30')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2012-12-31')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.00
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '5'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '2'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '16:45'
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-01-01')
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
        , date = date.Date ('2013-01-02')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-01-03')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-01-04')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-01-05')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-01-06')
        )
    db.commit ()
# end def import_data_7
