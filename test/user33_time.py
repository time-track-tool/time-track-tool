from roundup import date

def import_data_33 (db, user, olo):
    otp = None
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
        , valid_from         = date.Date ("2024-12-01.00:00:00")
        , valid_to           = date.Date ("2025-01-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    otp = None
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
        , valid_from         = date.Date ("2025-02-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2024-12-01.00:00:00')
        , absolute = 1
        , days     = 7.765
        )
    leave = db.daily_record_status.lookup ('leave')
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-03-06.00:00:00')
        , last_day  = date.Date ('2025-03-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-04-14.00:00:00')
        , last_day  = date.Date ('2025-04-17.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-05-02.00:00:00')
        , last_day  = date.Date ('2025-05-02.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-07-23.00:00:00')
        , last_day  = date.Date ('2025-07-23.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-08-18.00:00:00')
        , last_day  = date.Date ('2025-08-29.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-09-03.00:00:00')
        , last_day  = date.Date ('2025-09-03.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-12-15.00:00:00')
        , last_day  = date.Date ('2025-12-23.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-03-06'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-14'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-15'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-16'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-17'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-05-02'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-23'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-18'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-19'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-20'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-21'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-22'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-23'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-24'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-25'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-26'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-27'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-28'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-29'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-09-03'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-15'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-16'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-17'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-18'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-19'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-20'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-21'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-22'))
    assert len (dr) == 1
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-23'))
    assert len (dr) == 1
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
    db.commit ()
# end def import_data_33
