from roundup import date

def import_data_26 (db, user, olo):
    otp = None
    holo = db.work_location.create \
        ( code = 'Home-AT'
        , description = 'Home Office Location'
        )
    db.user_dynamic.create \
        ( all_in             = 1
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 8.0
        , hours_mon          = 8.0
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 8.0
        , hours_tue          = 8.0
        , hours_wed          = 8.0
        , max_flexitime      = 5.0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2023-07-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 40.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '15:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:45'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:15'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '15:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:00'
        , end           = '19:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.25
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:15'
        , end           = '10:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:45'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:45'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.25
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:30'
        , end           = '10:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        , status            = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '5'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '18:00'
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.commit ()
# end def import_data_26
