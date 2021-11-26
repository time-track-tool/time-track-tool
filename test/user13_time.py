from roundup import date

def import_data_13 (db, user, olo) :
     otp = None
     db.user_dynamic.create \
         ( hours_fri          = 7.5
         , hours_sun          = 0.0
         , hours_wed          = 7.75
         , daily_worktime     = 0.0
         , vacation_yearly    = 25.0
         , all_in             = 1
         , booking_allowed    = 1
         , durations_allowed  = 0
         , hours_tue          = 7.75
         , weekend_allowed    = 0
         , hours_mon          = 7.75
         , hours_thu          = 7.75
         , vacation_day       = 1.0
         , valid_from         = date.Date ("2013-01-01.00:00:00")
         , weekly_hours       = 38.5
         , travel_full        = 0
         , vacation_month     = 1.0
         , hours_sat          = 0.0
         , org_location       = olo
         , overtime_period    = otp
         , user               = user
         , max_flexitime      = 5
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-01')
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
         , date = date.Date ('2014-01-02')
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
         , date = date.Date ('2014-01-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-06')
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
         , date = date.Date ('2014-01-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '8'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:15'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '19:30'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:30'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:30'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '21:00'
         , end           = '21:30'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '13:00'
         , time_activity = '7'
         , work_location = '6'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:00'
         , end           = '07:45'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '10:45'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:30'
         , time_activity = '7'
         , work_location = '6'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:00'
         , end           = '21:00'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:30'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:30'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '12'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '11:30'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:15'
         , time_activity = '7'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '13:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , time_activity = '7'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '12'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:00'
         , end           = '20:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '16'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-01-31')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:15'
         , work_location = '5'
         , wp            = '44'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:15'
         , work_location = '5'
         , wp            = '44'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:15'
         , work_location = '5'
         , wp            = '44'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '19'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
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
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '9'
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
         , date = date.Date ('2014-02-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '11:30'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '16:45'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:30'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '20'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:00'
         , end           = '21:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '19:00'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '23:30'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:00'
         , end           = '10:00'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:00'
         , end           = '20:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-02-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '24'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '24'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '21:00'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '27'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:00'
         , end           = '22:00'
         , work_location = '2'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:00'
         , end           = '21:00'
         , work_location = '2'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:00'
         , end           = '20:30'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '30'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '30'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '30'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-03-31')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:15'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , time_activity = '7'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '19:00'
         , end           = '23:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '23:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
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
         , date = date.Date ('2014-04-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-07')
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
         , date = date.Date ('2014-04-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '21:00'
         , end           = '23:45'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '35'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:45'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '11:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '33'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '33'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-21')
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
         , date = date.Date ('2014-04-22')
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
         , date = date.Date ('2014-04-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '20:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '19'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '37'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '8'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '38'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '23'
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
         , date = date.Date ('2014-04-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '39'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-04-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-01')
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
         , date = date.Date ('2014-05-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '36'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '08:00'
         , work_location = '1'
         , wp            = '36'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '25'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '36'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:00'
         , end           = '21:00'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '36'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '36'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '36'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '36'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '19:30'
         , end           = '21:00'
         , time_activity = '7'
         , work_location = '2'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '36'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '36'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:15'
         , end           = '20:30'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-29')
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
         , date = date.Date ('2014-05-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-05-31')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '38'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '33'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '21:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '36'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '22:00'
         , end           = '23:00'
         , work_location = '2'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '23:00'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '05:15'
         , end           = '09:15'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '16:15'
         , time_activity = '7'
         , work_location = '6'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '11:15'
         , time_activity = '10'
         , work_location = '6'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-09')
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
         , date = date.Date ('2014-06-10')
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
         , date = date.Date ('2014-06-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:15'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '14:00'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-13')
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
         , date = date.Date ('2014-06-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-16')
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
         , date = date.Date ('2014-06-17')
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
         , date = date.Date ('2014-06-18')
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
         , date = date.Date ('2014-06-19')
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
         , date = date.Date ('2014-06-20')
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
         , date = date.Date ('2014-06-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-23')
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
         , date = date.Date ('2014-06-24')
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
         , date = date.Date ('2014-06-25')
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
         , date = date.Date ('2014-06-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:30'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:30'
         , work_location = '2'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '30'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-06-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '21:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '19:00'
         , end           = '21:00'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '06:15'
         , end           = '07:15'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '33'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:45'
         , end           = '13:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '16'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '30'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '30'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:15'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:15'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-07-31')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-01')
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
         , date = date.Date ('2014-08-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '30'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-25')
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
         , date = date.Date ('2014-08-26')
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
         , date = date.Date ('2014-08-27')
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
         , date = date.Date ('2014-08-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '22:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-31')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-18')
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
         , date = date.Date ('2014-08-19')
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
         , date = date.Date ('2014-08-20')
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
         , date = date.Date ('2014-08-21')
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
         , date = date.Date ('2014-08-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '44'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-11')
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
         , date = date.Date ('2014-08-12')
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
         , date = date.Date ('2014-08-13')
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
         , date = date.Date ('2014-08-14')
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
         , date = date.Date ('2014-08-15')
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
         , date = date.Date ('2014-08-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-08-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:00'
         , end           = '23:30'
         , time_activity = '7'
         , work_location = '3'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:00'
         , time_activity = '7'
         , work_location = '3'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '19:30'
         , time_activity = '7'
         , work_location = '3'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '05:15'
         , end           = '09:15'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:15'
         , end           = '21:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:15'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '33'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-06')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-07')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-08')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:15'
         , end           = '16:00'
         , work_location = '2'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-09')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-10')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-11')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '21:00'
         , end           = '22:00'
         , work_location = '2'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-12')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-13')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-14')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-15')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '21:30'
         , end           = '22:30'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-16')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-17')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:30'
         , time_activity = '7'
         , work_location = '3'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , time_activity = '7'
         , work_location = '3'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '05:45'
         , end           = '12:00'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-18')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '23:45'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , time_activity = '7'
         , work_location = '3'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:30'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '40'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-19')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '00:00'
         , end           = '00:45'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
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
         , date = date.Date ('2014-09-20')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-21')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-22')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-23')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-24')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-25')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-26')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-27')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-28')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-29')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-09-30')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '40'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-10-01')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-10-02')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-10-03')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-10-04')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2014-10-05')
         , weekend_allowed   = 0
         , required_overtime = 0
         )
     db.commit ()
# end def import_data_13
