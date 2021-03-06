from roundup import date

def import_data_5 (db, user) :
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-01')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-07')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-08')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '8'
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
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '5'
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
         , start         = '14:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-14')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-15')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:15'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:45'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '05:15'
         , end           = '09:00'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:15'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:45'
         , end           = '20:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '12'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '12'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '12'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-21')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-22')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-25')
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
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-26')
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
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-28')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-29')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '8'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-01-31')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-04')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-05')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-11')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-12')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '12'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '8'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '8'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-18')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-19')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '8'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-25')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-26')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '12'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '12'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-10')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-11')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-02-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-03')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-04')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '05:15'
         , end           = '09:00'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:15'
         , work_location = '6'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '6'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:15'
         , end           = '20:30'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '06:45'
         , end           = '10:00'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '16:00'
         , work_location = '6'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '20:45'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-17')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-18')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:15'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-24')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-25')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:45'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '06:30'
         , end           = '10:00'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '14:00'
         , work_location = '6'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:30'
         , time_activity = '10'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-03-31')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-01')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-04')
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
         , start         = '07:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 0.0
         , work_location = '5'
         , wp            = '19'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-07')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-08')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-11')
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
         , start         = '08:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:45'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '9'
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
         , date = date.Date ('2012-04-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-14')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-15')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '20:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-21')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-22')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '20'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '20'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '20'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '20'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-27')
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
         , start         = '08:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '20'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-28')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-29')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-04-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '8'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-05')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-06')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-09')
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
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-12')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-13')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-19')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-20')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:15'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-23')
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
         , start         = '10:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-26')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-27')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:15'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-05-31')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-02')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-03')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:15'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-06')
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
         , start         = '14:30'
         , end           = '19:45'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-09')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-10')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-13')
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
         , start         = '13:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-16')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-17')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:15'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:45'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:15'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-23')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-24')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-06-30')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-01')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '11:45'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:45'
         , end           = '12:45'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:15'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '11:45'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:15'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-07')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-08')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '18'
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
         , start         = '10:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-14')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-15')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:15'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-21')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-22')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-28')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-29')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-07-31')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-04')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-05')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '25'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '25'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-10')
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
         , start         = '08:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-11')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-12')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '20:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-18')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-19')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '24'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-23')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-24')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-25')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-08-26')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-24')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-25')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-26')
         )
     db.commit ()
# end def import_data_5
