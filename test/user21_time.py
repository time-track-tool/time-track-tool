from roundup import date

def import_data_21 (db, user, olo):
    otp = None
    db.user_dynamic.create \
        ( all_in             = 1
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 7.5
        , hours_mon          = 7.75
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 7.75
        , hours_tue          = 7.75
        , hours_wed          = 7.75
        , max_flexitime      = 5.0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2022-02-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '44'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '44'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '44'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '44'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , work_location = '5'
        , wp            = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:15'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:45'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '07:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:15'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:15'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '4'
        )
    db.commit ()
# end def import_data_21
