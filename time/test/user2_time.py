from roundup import date

def import_data_2 (db, user) :
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-03')
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
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
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
         , date = date.Date ('2008-11-05')
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
         , date = date.Date ('2008-11-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:00'
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
         , date = date.Date ('2008-11-07')
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
         , start         = '07:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-08')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-09')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '5'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '4'
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
         , date = date.Date ('2008-11-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '6'
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
         , date = date.Date ('2008-11-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '5'
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
         , start         = '13:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '13:15'
         , work_location = '1'
         , wp            = '5'
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
         , start         = '13:15'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '5'
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
         , date = date.Date ('2008-11-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-15')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-16')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-17')
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
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-18')
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
         , start         = '09:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-19')
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
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
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
         , start         = '13:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '13:00'
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
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-22')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-23')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-24')
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
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-25')
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
         , date = date.Date ('2008-11-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-29')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-11-30')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:45'
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
         , date = date.Date ('2008-12-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:30'
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
         , date = date.Date ('2008-12-06')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-07')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:15'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
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
         , date = date.Date ('2008-12-11')
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
         , start         = '08:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '8'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-13')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-14')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
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
         , date = date.Date ('2008-12-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-19')
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
         , end           = '12:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-20')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-21')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-27')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-28')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2008-12-31')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-03')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-04')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-10')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-11')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-17')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-18')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '7'
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
         , date = date.Date ('2009-01-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
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
         , date = date.Date ('2009-01-21')
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
         , date = date.Date ('2009-01-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:15'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-24')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-25')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '7'
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
         , start         = '15:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '19:30'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-29')
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
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-01-31')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-01')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-02')
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
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-03')
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
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-07')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-08')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-09')
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
         , start         = '12:30'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-10')
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
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:30'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-14')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-15')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-21')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-22')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:15'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '16:45'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:15'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '16:45'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-02-28')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-01')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-07')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-08')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-11')
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
         , start         = '12:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '12'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
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
         , date = date.Date ('2009-03-14')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-15')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-16')
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
         , start         = '10:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-17')
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
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-19')
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
         , start         = '13:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-21')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-22')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-28')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-29')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-03-31')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '9'
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
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '7'
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
         , start         = '12:45'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-04')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-05')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '7'
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
         , start         = '12:45'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-11')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-12')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
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
         , start         = '13:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '14'
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
         , start         = '15:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-18')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-19')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '14:45'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:45'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '6'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-24')
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
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-25')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-26')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
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
         , start         = '12:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '11:00'
         , work_location = '5'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '7'
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
         , date = date.Date ('2009-04-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:30'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-04-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:30'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-02')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-03')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '16'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:45'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-09')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-10')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '9'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-16')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-17')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '10'
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
         , end           = '17:45'
         , work_location = '1'
         , wp            = '19'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-23')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-24')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-25')
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
         , end           = '12:00'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '21'
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
         , date = date.Date ('2009-05-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '13:45'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:45'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-29')
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
         , start         = '12:30'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-30')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-05-31')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '9'
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
         , end           = '14:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-05')
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
         , date = date.Date ('2009-06-06')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-07')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '19'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-10')
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
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-13')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-14')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-16')
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
         , start         = '12:30'
         , end           = '13:15'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:15'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '17'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:15'
         , end           = '19:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:45'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '17'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '17'
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
         , date = date.Date ('2009-06-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:00'
         , end           = '21:45'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-20')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-21')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:00'
         , end           = '20:00'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '20:30'
         , end           = '22:15'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '22'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '14:00'
         , work_location = '6'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:00'
         , work_location = '6'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '19:30'
         , end           = '23:00'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '22'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '19:00'
         , work_location = '6'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '19'
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
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '19:15'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:30'
         , work_location = '1'
         , wp            = '7'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-27')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-28')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-14')
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
         , end           = '12:00'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-15')
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
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '18:45'
         , work_location = '1'
         , wp            = '24'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-17')
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
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-18')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-19')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-11')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-12')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-06-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-04')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-05')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:00'
         , end           = '10:30'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '12:00'
         , work_location = '6'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '18:00'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '6'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:45'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '24'
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
         , start         = '14:45'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '25'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-24')
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
         , start         = '09:15'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-25')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-26')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '24'
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
         , start         = '15:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '17:30'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '18:00'
         , end           = '20:15'
         , work_location = '6'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '6'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:45'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-07-31')
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
         , start         = '08:00'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '6'
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
         , start         = '09:15'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-01')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-02')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '23'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '27'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:15'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:45'
         , end           = '21:00'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:15'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-06')
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
         , start         = '08:45'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:45'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-08')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-09')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:45'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '25'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '13:15'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:15'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '25'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-15')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-16')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '10'
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
         , start         = '08:45'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '13'
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
         , date = date.Date ('2009-08-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:15'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '25'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '25'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-22')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-23')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '25'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-29')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-30')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-08-31')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '26'
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
         , end           = '17:30'
         , work_location = '1'
         , wp            = '18'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:15'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-04')
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
         , start         = '12:30'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-05')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-06')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:45'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:45'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:00'
         , end           = '10:15'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '15:30'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:30'
         , work_location = '6'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-12')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-13')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:45'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:45'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-19')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-20')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:30'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
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
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-23')
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
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:15'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-26')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-27')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '27'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:15'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:15'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-09-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '18'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '19'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-01')
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
         , start         = '12:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '19'
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
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-03')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-04')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '19'
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
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-07')
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
         , start         = '12:45'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '11'
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
         , start         = '09:15'
         , end           = '12:00'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:00'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-10')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-11')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-12')
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
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:15'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '20'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-14')
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
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '26'
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
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-15')
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
         , start         = '12:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '11'
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
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-17')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-18')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '26'
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
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '20'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-23')
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
         , start         = '14:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-24')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-25')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '06:30'
         , end           = '10:15'
         , work_location = '3'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '6'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '6'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '13:00'
         , work_location = '6'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:30'
         , work_location = '6'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '19:30'
         , work_location = '3'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '19:30'
         , end           = '20:30'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '24'
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
         , start         = '08:45'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-10-31')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '32'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '11'
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
         , start         = '09:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-06')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '20'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-07')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-08')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '26'
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
         , start         = '17:30'
         , end           = '20:15'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '13'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '13'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '11:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:45'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-14')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-15')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:45'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '11'
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
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-21')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-22')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '32'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '34'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-28')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-29')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-11-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '11:45'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:15'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '35'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '33'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '36'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '36'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-03')
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
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '21'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-05')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-06')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:45'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '06:30'
         , end           = '10:15'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:30'
         , work_location = '6'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:15'
         , time_activity = '11'
         , work_location = '3'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-12')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-13')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '13:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:45'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '29'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '19'
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
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '30'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '21'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '19'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '11:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:45'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '23'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '20'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-19')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-20')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '35'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '16:15'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '13:15'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:15'
         , end           = '13:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:45'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-24')
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
         , date = date.Date ('2009-12-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '1'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-26')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-27')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-30')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.75
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2009-12-31')
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
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:45'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-08')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '26'
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
         , date = date.Date ('2009-11-01')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:15'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-13')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '31'
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
         , end           = '11:15'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '29'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-15')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '10'
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
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:45'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:45'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-20')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:45'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:45'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-21')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:15'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-22')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
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
         , end           = '13:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '35'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:15'
         , end           = '12:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '35'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '11:45'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '18:15'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '20'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '10'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:15'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-01-29')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '35'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '35'
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
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '35'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '14'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:15'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '34'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '32'
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
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '29'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '11'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-09')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '32'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-10')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '17:45'
         , work_location = '1'
         , wp            = '32'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-11')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '5'
         , wp            = '2'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '16:30'
         , work_location = '5'
         , wp            = '2'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-12')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '11'
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
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '11'
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
         , end           = '11:30'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:15'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-16')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:15'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '11:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '24'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-17')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:00'
         , end           = '15:45'
         , work_location = '1'
         , wp            = '32'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-18')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '12:15'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:15'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '30'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:15'
         , end           = '12:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-19')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '32'
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
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '37'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:00'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-23')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:15'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:45'
         , end           = '17:15'
         , work_location = '1'
         , wp            = '32'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:45'
         , end           = '13:30'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '15'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '9'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:30'
         , end           = '17:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-25')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '17:30'
         , end           = '18:00'
         , work_location = '1'
         , wp            = '31'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-02-26')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '10:15'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:15'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:15'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '31'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:15'
         , end           = '14:30'
         , work_location = '1'
         , wp            = '26'
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
         , start         = '08:00'
         , end           = '08:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:45'
         , end           = '09:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:15'
         , end           = '09:45'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:45'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '38'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:45'
         , end           = '15:15'
         , work_location = '1'
         , wp            = '24'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-02')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '10'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:30'
         , work_location = '1'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:00'
         , work_location = '1'
         , wp            = '24'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '26'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-03')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:00'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '10:00'
         , work_location = '1'
         , wp            = '37'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '10:45'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:45'
         , end           = '12:45'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:15'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:00'
         , end           = '16:30'
         , work_location = '1'
         , wp            = '11'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '15:30'
         , end           = '16:00'
         , work_location = '1'
         , wp            = '28'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '05:00'
         , end           = '09:00'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '37'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:00'
         , work_location = '4'
         , wp            = '37'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '4'
         , wp            = '37'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '05:45'
         , end           = '10:00'
         , time_activity = '10'
         , work_location = '3'
         , wp            = '37'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '32'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:00'
         , end           = '10:30'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '10:30'
         , end           = '11:15'
         , work_location = '1'
         , wp            = '26'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '28'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '19'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '14:45'
         , work_location = '1'
         , wp            = '37'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-06')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2010-03-07')
         )
     db.commit ()
# end def import_data_2
