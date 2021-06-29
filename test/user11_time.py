from roundup import date

def import_data_11 (db, user) :
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-03')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.00
        , wp            = '4'
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
        , duration      = 3.00
        , wp            = '4'
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
        , duration      = 2.00
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
        , date = date.Date ('2013-06-04')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-05')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-06')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-07')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-08')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-09')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-10')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '1'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-11')
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '3'
        )
    ar = db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-12')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-13')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-14')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-15')
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2013-06-16')
        )
    db.commit ()
# end def import_data_11
