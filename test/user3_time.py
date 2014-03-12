from roundup import date

def import_data_3 (db, user) :
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-08')
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
         , start         = '08:45'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '8'
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
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-09')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-10')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-02')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-03')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '12:45'
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
         , wp            = '8'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '11:30'
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
         , date = date.Date ('2010-01-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:45'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-16')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-17')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-19')
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
         , end           = '11:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:45'
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
         , date = date.Date ('2010-01-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:30'
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
         , date = date.Date ('2010-01-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-23')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-24')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-26')
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
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '8'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '10'
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
         , start         = '14:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-30')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-31')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '17:15'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-06')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-07')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
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
         , date = date.Date ('2010-02-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:00'
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
         , start         = '17:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-11')
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
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-13')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-14')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '19:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:30'
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
         , start         = '16:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '12'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-20')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-21')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-22')
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
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-23')
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
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:45'
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
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-27')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-28')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-01')
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
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-02')
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
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '5'
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
         , date = date.Date ('2010-03-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '5'
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
         , date = date.Date ('2010-03-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-06')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-07')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '14'
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
         , start         = '17:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '14'
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
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-13')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-14')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-16')
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
         , start         = '08:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-17')
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
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:45'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-18')
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
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-19')
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
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-20')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-21')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-23')
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
         , start         = '09:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-27')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-28')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '06:30'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-31')
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
         , start         = '08:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-03')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-04')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '08:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '14'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-10')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-11')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '19:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-17')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '13:30'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:30'
         , work_location = '3'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '23:45'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '00:00'
         , end           = '00:30'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '7'
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
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '16'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-23')
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
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-24')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '14:30'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:30'
         , end           = '23:45'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '00:00'
         , end           = '02:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:15'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:45'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-29')
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
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-04-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-01')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-02')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:15'
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
         , date = date.Date ('2010-05-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:45'
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
         , date = date.Date ('2010-05-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-08')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-09')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
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
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-11')
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
         , start         = '08:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:00'
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
         , start         = '17:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '15'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-15')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-16')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '18'
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
         , start         = '16:00'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-22')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-23')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-25')
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
         , start         = '08:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:45'
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
         , date = date.Date ('2010-05-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-28')
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
         , date = date.Date ('2010-05-29')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-30')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-05-31')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.commit ()
# end def import_data_3
