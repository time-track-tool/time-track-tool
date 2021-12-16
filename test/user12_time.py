from roundup import date

def import_data_12 (db, user, olo) :
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
         , booking_allowed    = 1
         , durations_allowed  = 0
         , hours_tue          = 7.75
         , supp_per_period    = 7.0
         , weekly_hours       = 38.5
         , hours_mon          = 7.75
         , hours_thu          = 7.75
         , valid_from         = date.Date ("2013-01-01.00:00:00")
         , valid_to           = date.Date ("2013-04-01.00:00:00")
         , weekend_allowed    = 0
         , travel_full        = 0
         , hours_sat          = 0.0
         , org_location       = olo
         , overtime_period    = otp
         , user               = user
         )
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
         , booking_allowed    = 1
         , durations_allowed  = 0
         , hours_tue          = 7.75
         , supp_per_period    = 7.0
         , weekly_hours       = 38.5
         , hours_mon          = 7.75
         , hours_thu          = 7.75
         , valid_from         = date.Date ("2013-04-01.00:00:00")
         , valid_to           = date.Date ("2013-07-01.00:00:00")
         , weekend_allowed    = 0
         , travel_full        = 0
         , hours_sat          = 0.0
         , org_location       = olo
         , overtime_period    = otp
         , user               = user
         )
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
         , booking_allowed    = 1
         , durations_allowed  = 0
         , hours_tue          = 7.75
         , supp_per_period    = 7.0
         , weekly_hours       = 38.5
         , hours_mon          = 7.75
         , hours_thu          = 7.75
         , valid_from         = date.Date ("2013-09-01.00:00:00")
         , weekend_allowed    = 0
         , travel_full        = 0
         , hours_sat          = 0.0
         , org_location       = olo
         , overtime_period    = otp
         , user               = user
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-01')
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
         , date = date.Date ('2013-01-02')
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
         , date = date.Date ('2013-01-03')
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
         , date = date.Date ('2013-01-04')
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
         , date = date.Date ('2013-01-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '19:45'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '6'
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
         , date = date.Date ('2013-01-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '8'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , time_activity = '1'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-10')
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
         , date = date.Date ('2013-01-11')
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
         , date = date.Date ('2013-01-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:15'
         , end           = '19:45'
         , work_location = '1'
         , wp            = '8'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '12'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '12:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:15'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '16'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , time_activity = '5'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '21:00'
         , time_activity = '5'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , time_activity = '5'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , time_activity = '5'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '14:00'
         , time_activity = '5'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:45'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-01-31')
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
         , date = date.Date ('2013-02-01')
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
         , date = date.Date ('2013-02-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:15'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:15'
         , end           = '23:45'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '00:00'
         , end           = '00:30'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '6'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '6'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '22:30'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:45'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:15'
         , time_activity = '1'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '13:30'
         , time_activity = '1'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '24'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-02-25')
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
         , date = date.Date ('2013-02-26')
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
         , date = date.Date ('2013-02-27')
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
         , date = date.Date ('2013-02-28')
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
         , date = date.Date ('2013-03-01')
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
         , date = date.Date ('2013-03-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-04')
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
         , date = date.Date ('2013-03-05')
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
         , date = date.Date ('2013-03-06')
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
         , date = date.Date ('2013-03-07')
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
         , date = date.Date ('2013-03-08')
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
         , date = date.Date ('2013-03-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '22:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '21:15'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '24'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:15'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '21:15'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-03-31')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-01')
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
         , date = date.Date ('2013-04-02')
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
         , date = date.Date ('2013-04-03')
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
         , date = date.Date ('2013-04-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '21:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '23:45'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:00'
         , work_location = '6'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '6'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '6'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '13:30'
         , work_location = '6'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:30'
         , work_location = '6'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '13:30'
         , work_location = '6'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '21:30'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '22:00'
         , end           = '22:30'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '21:30'
         , end           = '22:00'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 0.0
         , work_location = '5'
         , wp            = '27'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-04-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 0.0
         , work_location = '5'
         , wp            = '27'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-01')
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
         , date = date.Date ('2013-05-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '20'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '22:00'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-09')
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
         , date = date.Date ('2013-05-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-20')
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
         , date = date.Date ('2013-05-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-05-30')
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
         , date = date.Date ('2013-05-31')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:45'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '30'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '29'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '30'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-06-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '32'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '32'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-10')
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
         , date = date.Date ('2013-09-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '35'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '35'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 0.0
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '21:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:45'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '35'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '21:30'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '21:00'
         , work_location = '1'
         , wp            = '37'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-03')
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
         , date = date.Date ('2013-10-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '37'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-09-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '21:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '21:30'
         , end           = '23:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '32'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '37'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '21:30'
         , work_location = '1'
         , wp            = '37'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '37'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '38'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '37'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '22:00'
         , work_location = '1'
         , wp            = '39'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '39'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '37'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-31')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-01')
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
         , date = date.Date ('2013-11-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '22:00'
         , work_location = '1'
         , wp            = '37'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '37'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '37'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-10-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '37'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '38'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '22:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '41'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '22:00'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '37'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '21:15'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:30'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '22:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '37'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '21:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-16')
         , weekend_allowed   = 1
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-17')
         , weekend_allowed   = 1
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '42'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '21:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '21:30'
         , end           = '22:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 0.0
         , work_location = '5'
         , wp            = '27'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-23')
         , weekend_allowed   = 1
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-24')
         , weekend_allowed   = 1
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '21:15'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '21:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-11-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '22:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '43'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '43'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '38'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '38'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '38'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '38'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '38'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '38'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 0.0
         , work_location = '5'
         , wp            = '27'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 0.0
         , work_location = '5'
         , wp            = '27'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:15'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-09')
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
         , date = date.Date ('2013-12-10')
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
         , date = date.Date ('2013-12-11')
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
         , date = date.Date ('2013-12-12')
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
         , date = date.Date ('2013-12-13')
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
         , date = date.Date ('2013-12-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-23')
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
         , date = date.Date ('2013-12-24')
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
         , duration      = 3.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-25')
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
         , date = date.Date ('2013-12-26')
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
         , date = date.Date ('2013-12-27')
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
         , date = date.Date ('2013-12-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2013-12-30')
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
         , date = date.Date ('2013-12-31')
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
         , duration      = 3.75
         , work_location = '5'
         , wp            = '2'
         )
     db.commit ()
# end def import_data_12
