from roundup import date

def import_data_44 (db, user, olo):
    otp = None
    holo = db.work_location.create \
        ( code = 'Home-AT'
        , description = 'Home Office Location'
        )
    db.user_dynamic.create \
        ( all_in             = 1
        , booking_allowed    = 1
        , durations_allowed  = 1
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
        , valid_from         = date.Date ("2018-01-01.00:00:00")
        , valid_to           = date.Date ("2018-03-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2018-02-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tatp = db.time_activity.create \
        ( name     = 'Travel passive'
        , travel   = 1
        , is_valid = True
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , time_activity = tatp
        , wp            = '4'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '4'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '5'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , time_activity = tatp
        , wp            = '4'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2018-02-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '5'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '4'
        , time_activity = tatp
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '4'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , time_activity = tatp
        , wp            = '4'
        )
    db.commit ()
# end def import_data_44
