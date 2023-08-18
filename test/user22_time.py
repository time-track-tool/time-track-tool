from roundup import date

def import_data_22 (db, user, olo):
    otp = None
    leave = db.daily_record_status.lookup ('leave')
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
        , valid_from         = date.Date ("2020-11-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-12-21.00:00:00')
        , last_day  = date.Date ('2020-12-21.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-12-22.00:00:00')
        , last_day  = date.Date ('2020-12-22.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-12-23.00:00:00')
        , last_day  = date.Date ('2020-12-23.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-12-24.00:00:00')
        , last_day  = date.Date ('2020-12-31.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2021-01-04.00:00:00')
        , last_day  = date.Date ('2021-01-05.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:15'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '11:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:00'
        , end           = '18:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '12'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:00'
        , end           = '14:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '13'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '09:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:15'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '12'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '14'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '09:15'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '15'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-10.00:00:00')
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
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '16'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '18:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:00'
        , end           = '14:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '14'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '09:15'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:30'
        , end           = '17:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '17'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '14:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '15'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '15:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:00'
        , end           = '14:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2020-12-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-21'))
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.0
        , wp            = '45'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-22'))
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-23'))
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-24'))
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-25'))
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-26'))
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-27'))
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-28'))
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-29'))
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-30'))
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-31'))
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-01-04'))
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '46'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-01-05'))
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '46'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '18'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '14'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:00'
        , end           = '18:15'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:00'
        , end           = '14:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '14'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '09:15'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '13:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '12:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '15'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '11:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:30'
        , end           = '17:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '15:30'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '11:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:15'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-13.00:00:00')
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
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '16:30'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '14'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:30'
        , end           = '17:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:00'
        , end           = '14:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '14'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '09:15'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:30'
        , end           = '17:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '18'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '19'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-21.00:00:00')
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
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:00'
        , end           = '14:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '14'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '09:15'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:30'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '15'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '10:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '14:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '15:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:30'
        , end           = '17:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '15'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:30'
        , end           = '11:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:30'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '17:30'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '2'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:00'
        , end           = '14:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2021-01-31.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.commit ()
# end def import_data_22
