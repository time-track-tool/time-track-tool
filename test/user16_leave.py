from roundup import date

def import_data_16 (db, user, dep, olo) :
     sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
     otp = db.overtime_period.filter (None, sd)
     assert len (otp) == 1
     otp = otp [0]
     db.user_dynamic.create \
         ( hours_fri          = 8.0
         , hours_sun          = 0.0
         , additional_hours   = 40.0
         , hours_wed          = 8.0
         , vacation_yearly    = 30.0
         , all_in             = 0
         , valid_from         = date.Date ("2018-10-01.00:00:00")
         , durations_allowed  = 0
         , hours_tue          = 8.0
         , weekly_hours       = 40.0
         , hours_mon          = 8.0
         , hours_thu          = 8.0
         , vacation_day       = 1.0
         , booking_allowed    = 1
         , supp_weekly_hours  = 40.0
         , valid_to           = date.Date ("2019-01-01.00:00:00")
         , weekend_allowed    = 0
         , travel_full        = 1
         , vacation_month     = 1.0
         , hours_sat          = 0.0
         , department         = dep
         , org_location       = olo
         , overtime_period    = otp
         , user               = user
         , vac_aliq           = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 4.0
         , work_location = '5'
         , wp            = '1'
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 4.0
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-31')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 4.0
         , work_location = '5'
         , wp            = '1'
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 4.0
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-04')
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
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-06')
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
         , start         = '07:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2018-12-13')
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
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2019-01-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 8.0
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2019-01-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2019-01-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2019-01-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2019-01-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2019-01-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     ls = db.leave_submission.create \
         ( user      = user
         , first_day = date.Date ('2018-12-07')
         , last_day  = date.Date ('2018-12-07')
         , status    = '4'
         , time_wp   = '44'
         )
     ls = db.leave_submission.create \
         ( user      = user
         , first_day = date.Date ('2018-12-14')
         , last_day  = date.Date ('2018-12-31')
         , status    = '4'
         , time_wp   = '44'
         )
     db.commit ()
# end def import_data_16
