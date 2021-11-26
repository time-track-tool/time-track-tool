from roundup import date

def import_data_18 (db, user, olo) :
    sd = dict (months = 1.0, required_overtime = 1, weekly = 0)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( hours_fri          = 7.5
        , hours_sun          = 0.0
        , hours_wed          = 7.75
        , vacation_yearly    = 25.0
        , all_in             = 0
        , valid_from         = date.Date ("2018-10-01.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 7.75
        , supp_per_period    = 7.0
        , weekend_allowed    = 0
        , hours_mon          = 7.75
        , hours_thu          = 7.75
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , valid_to           = date.Date ("2019-05-01.00:00:00")
        , weekly_hours       = 38.5
        , travel_full        = 0
        , vacation_month     = 1.0
        , hours_sat          = 0.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( hours_fri          = 7.5
        , hours_sun          = 0.0
        , additional_hours   = 38.5
        , hours_wed          = 7.75
        , vacation_yearly    = 25.0
        , all_in             = 0
        , valid_from         = date.Date ("2019-05-01.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 7.75
        , weekend_allowed    = 0
        , hours_mon          = 7.75
        , hours_thu          = 7.75
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , supp_weekly_hours  = 38.5
        , valid_to           = date.Date ("2019-12-01.00:00:00")
        , weekly_hours       = 38.5
        , travel_full        = 0
        , vacation_month     = 1.0
        , hours_sat          = 0.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2018-01-01.00:00:00')
        , absolute = 1
        , days     = 7.765
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-05-20.00:00:00')
        , last_day  = date.Date ('2019-05-20.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-06-28.00:00:00')
        , last_day  = date.Date ('2019-06-28.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-07-05.00:00:00')
        , last_day  = date.Date ('2019-07-05.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-08-09.00:00:00')
        , last_day  = date.Date ('2019-08-16.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-01.00:00:00')
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
        , date = date.Date ('2019-05-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
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
        , date = date.Date ('2019-05-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        , wp            = '5'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '5'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '14:30'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '5'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '14:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '7'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '14:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '1'
        , wp            = '7'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '8'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '14:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '7'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '14:00'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '11:30'
        , work_location = '1'
        , wp            = '5'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:30'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '7'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '14:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '15:00'
        , work_location = '2'
        , wp            = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '5'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '5'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:15'
        , end           = '08:45'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '5'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '11:00'
        , work_location = '1'
        , wp            = '5'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '16:45'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '14:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '14:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-19.00:00:00')
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
        , date = date.Date ('2019-05-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:30'
        , end           = '10:30'
        , work_location = '2'
        , wp            = '5'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '10:30'
        , end           = '11:30'
        , work_location = '2'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:30'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '2'
        , wp            = '9'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '11:00'
        , work_location = '2'
        , wp            = '9'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:30'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '10'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '9'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '9'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '14:30'
        , work_location = '1'
        , wp            = '11'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '11'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '16:45'
        , work_location = '2'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '14:30'
        , end           = '15:30'
        , work_location = '1'
        , wp            = '9'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '14:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '9'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '14:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '9'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:30'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '9'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-05-30.00:00:00')
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
        , date = date.Date ('2019-05-31.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '11:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '12'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '11:00'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '13'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '13'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:30'
        , end           = '13:30'
        , work_location = '2'
        , wp            = '13'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '13:30'
        , end           = '15:30'
        , work_location = '2'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '1'
        , wp            = '13'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '13'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:30'
        , end           = '17:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '1'
        , wp            = '13'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '13'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:30'
        , end           = '16:30'
        , work_location = '1'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:30'
        , end           = '17:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-10.00:00:00')
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
        , date = date.Date ('2019-06-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '15:00'
        , work_location = '2'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '2'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:00'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '17:00'
        , end           = '18:00'
        , work_location = '2'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '1'
        , wp            = '8'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:30'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-20.00:00:00')
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
        , date = date.Date ('2019-06-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '14:00'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '2'
        , wp            = '14'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '14:00'
        , end           = '15:00'
        , work_location = '2'
        , wp            = '12'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '11:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '14'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '11'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '11:00'
        , work_location = '1'
        , wp            = '11'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '16:45'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '11:00'
        , work_location = '2'
        , wp            = '4'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '10'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '6'
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , work_location = '5'
        , wp            = '44'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-06-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '15'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '15'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '8'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:15'
        , end           = '08:45'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '6'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:15'
        , end           = '08:45'
        , work_location = '2'
        , wp            = '15'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '15'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '16:45'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , work_location = '5'
        , wp            = '44'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:30'
        , end           = '17:30'
        , work_location = '2'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '15'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '1'
        , wp            = '15'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '15'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '10:00'
        , work_location = '2'
        , wp            = '15'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:15'
        , work_location = '5'
        , wp            = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '16:45'
        , work_location = '2'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '16:45'
        , work_location = '2'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '11:00'
        , work_location = '2'
        , wp            = '15'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '15'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '15'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '17'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '17'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '17:15'
        , work_location = '2'
        , wp            = '17'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '17'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '11:00'
        , work_location = '1'
        , wp            = '17'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '15'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '15'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '15'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '11:00'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '15'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '17:15'
        , work_location = '2'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '07:15'
        , end           = '07:45'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-07-31.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '10:00'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        , wp            = '15'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '15'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '16:45'
        , work_location = '2'
        , wp            = '15'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '15'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:15'
        , end           = '16:45'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '18'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , work_location = '5'
        , wp            = '44'
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '44'
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '44'
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '44'
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , work_location = '5'
        , wp            = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , work_location = '5'
        , wp            = '44'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '15:00'
        , end           = '17:00'
        , work_location = '1'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:30'
        , end           = '17:30'
        , work_location = '1'
        , wp            = '12'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '14:45'
        , work_location = '1'
        , wp            = '19'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '14:45'
        , end           = '15:45'
        , work_location = '1'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        , wp            = '19'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:30'
        , end           = '11:30'
        , work_location = '1'
        , wp            = '8'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '11:30'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '19'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '10:15'
        , work_location = '2'
        , wp            = '19'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '10:15'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '16:30'
        , end           = '18:00'
        , work_location = '2'
        , wp            = '8'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '14:00'
        , work_location = '1'
        , wp            = '8'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:15'
        , end           = '12:00'
        , work_location = '1'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:15'
        , end           = '08:45'
        , work_location = '2'
        , wp            = '8'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '14:00'
        , end           = '17:00'
        , work_location = '1'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '2'
        , wp            = '16'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '2'
        , wp            = '16'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-08-31.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:15'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:15'
        , work_location = '5'
        , wp            = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '5'
        , wp            = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '17:00'
        , end           = '18:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '2'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '2'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    db.time_record.create \
        ( daily_record  = dr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-09-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-10-31.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-11-01.00:00:00')
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
        , date = date.Date ('2019-11-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-11-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-11-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-11-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-11-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-11-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-11-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-11-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2019-11-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    db.commit ()
# end def import_data_18
