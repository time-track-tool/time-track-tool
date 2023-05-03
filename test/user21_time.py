from roundup import date

def import_data_21 (db, user, olo):
    otp = None
    travel_passive = db.time_activity.create \
	( name     = 'Travel passiv'
	, travel   = 1
	, is_valid = True
	)
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
        , valid_to           = date.Date ("2023-02-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
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
        , valid_from         = date.Date ("2023-02-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
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
        , valid_from         = date.Date ("2023-10-01.00:00:00")
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
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-19.00:00:00')
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
        , date = date.Date ('2023-01-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:45'
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
        , date = date.Date ('2023-01-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-23.00:00:00')
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
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:30'
        , end           = '20:30'
        , time_activity = travel_passive
        , work_location = '3'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '4'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '4'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '4'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '4'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '4'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '4'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '13:15'
        , end           = '17:30'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '07:30'
        , end           = '13:15'
        , time_activity = travel_passive
        , work_location = '3'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-30.00:00:00')
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
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-01-31.00:00:00')
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
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-01.00:00:00')
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
        , date = date.Date ('2023-02-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '18:15'
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
        , date = date.Date ('2023-02-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:15'
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
    db.time_record.create \
        ( daily_record  = dr
        , start         = '18:15'
        , end           = '19:15'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-08.00:00:00')
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
        , date = date.Date ('2023-02-09.00:00:00')
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
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:30'
        , end           = '09:45'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '10:15'
        , end           = '11:15'
        , work_location = '5'
        , wp            = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:00'
        , end           = '15:15'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-13.00:00:00')
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
        , start         = '07:45'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , work_location = '5'
        , wp            = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , work_location = '5'
        , wp            = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-27.00:00:00')
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
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-02-28.00:00:00')
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
        , date = date.Date ('2023-03-01.00:00:00')
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
        , date = date.Date ('2023-03-02.00:00:00')
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
        , date = date.Date ('2023-03-03.00:00:00')
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
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:30'
        , end           = '12:30'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '14:30'
        , end           = '15:15'
        , work_location = '5'
        , wp            = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:45'
        , end           = '18:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-07.00:00:00')
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
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:30'
        , end           = '14:15'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '15:45'
        , work_location = '5'
        , wp            = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '17:30'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:30'
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
        , date = date.Date ('2023-03-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:30'
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
        , date = date.Date ('2023-03-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '11:00'
        , work_location = '5'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '13:00'
        , end           = '16:45'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-14.00:00:00')
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
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-15.00:00:00')
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
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '18:30'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '10:45'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:30'
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
        , date = date.Date ('2023-03-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-20.00:00:00')
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
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-21.00:00:00')
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
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-22.00:00:00')
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
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:45'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:15'
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
        , date = date.Date ('2023-03-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '13:00'
        , end           = '18:45'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:15'
        , end           = '12:30'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-03-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:30'
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
        , date = date.Date ('2023-03-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:30'
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
        , date = date.Date ('2023-03-31.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:30'
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
        , date = date.Date ('2023-04-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-03.00:00:00')
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
        , date = date.Date ('2023-04-04.00:00:00')
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
        , date = date.Date ('2023-04-05.00:00:00')
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
        , date = date.Date ('2023-04-06.00:00:00')
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
        , date = date.Date ('2023-04-07.00:00:00')
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
        , date = date.Date ('2023-04-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:45'
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
        , date = date.Date ('2023-04-12.00:00:00')
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
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-13.00:00:00')
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
        , date = date.Date ('2023-04-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:45'
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
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:45'
        , end           = '09:15'
        , work_location = '5'
        , wp            = '4'
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
        , start         = '10:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-18.00:00:00')
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
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-19.00:00:00')
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
        , date = date.Date ('2023-04-20.00:00:00')
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
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:45'
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
        , date = date.Date ('2023-04-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-24.00:00:00')
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
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:45'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-26.00:00:00')
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
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:30'
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
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-28.00:00:00')
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
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-04-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.commit ()
# end def import_data_21
