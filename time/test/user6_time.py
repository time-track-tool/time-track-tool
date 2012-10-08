from roundup import date

def import_data_6 (db, user) :
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-03')
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
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-04')
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
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '08:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-06')
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
         , start         = '08:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-07')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:00'
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
         , date = date.Date ('2012-09-08')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-09')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-10')
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
         , date = date.Date ('2012-09-11')
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
         , date = date.Date ('2012-09-12')
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
         , date = date.Date ('2012-09-13')
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
         , start         = '07:30'
         , end           = '12:00'
         , work_location = '5'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-14')
         )
     db.time_record.create \
         ( daily_record  = dr
         , duration      = 7.5
         , work_location = '5'
         , wp            = '5'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-15')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-16')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-17')
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
         , start         = '08:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-18')
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
         , start         = '07:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-19')
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
         , date = date.Date ('2012-09-20')
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
         , date = date.Date ('2012-09-21')
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
         , start         = '07:30'
         , end           = '09:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '15:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-22')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-23')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-24')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:30'
         , end           = '19:00'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '13:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-25')
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
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-26')
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
         , start         = '07:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-27')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:45'
         , end           = '12:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '13:00'
         , end           = '14:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '14:00'
         , end           = '15:00'
         , work_location = '1'
         , wp            = '4'
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
         , start         = '17:00'
         , end           = '17:30'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-28')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:30'
         , end           = '09:00'
         , work_location = '1'
         , wp            = '4'
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
         , start         = '09:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '7'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '16:15'
         , end           = '16:45'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-29')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-09-30')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-01')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '18:15'
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
         , date = date.Date ('2012-10-02')
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
         , start         = '08:15'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-03')
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
         , start         = '07:00'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-04')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:00'
         , end           = '08:30'
         , work_location = '1'
         , wp            = '4'
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
         , date = date.Date ('2012-10-05')
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '07:15'
         , end           = '11:30'
         , work_location = '1'
         , wp            = '4'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '11:30'
         , end           = '12:00'
         , work_location = '1'
         , wp            = '6'
         )
     db.time_record.create \
         ( daily_record  = dr
         , start         = '12:30'
         , end           = '14:15'
         , work_location = '1'
         , wp            = '4'
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-06')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-07')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-08')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-09')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-10')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-11')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-12')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-13')
         )
     dr = db.daily_record.create \
         ( user = user
         , date = date.Date ('2012-10-14')
         )
     db.commit ()
# end def import_data_6
