from roundup import date

def import_data_27 (db, user, olo, parent):
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    holo = db.work_location.create \
        ( code = 'Home-AT'
        , description = 'Home Office Location'
        )
    db.user_dynamic.create \
        ( additional_hours   = 40.0
        , all_in             = 0
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 8.0
        , hours_mon          = 8.0
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 8.0
        , hours_tue          = 8.0
        , hours_wed          = 8.0
        , supp_weekly_hours  = 40.0
        , travel_full        = 1
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 30.0
        , valid_from         = date.Date ("2021-02-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 40.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '2'
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2021-02-01.00:00:00')
        , absolute = 1
        , days     = 0.0
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2022-01-01.00:00:00')
        , absolute = 0
        , days     = 0.0
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2022-08-01.00:00:00')
        , absolute = 1
        , days     = 0.0
        , contract_type = parent.ct_pt
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2023-09-25.00:00:00')
        , absolute = 1
        , days     = 0.0
        )
    otp = None
    db.user_dynamic.create \
        ( additional_hours   = 0.0
        , all_in             = 0
        , booking_allowed    = 0
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , supp_weekly_hours  = 0.0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 30.0
        , valid_from         = date.Date ("2022-01-13.00:00:00")
        , valid_to           = date.Date ("2022-04-23.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 0.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '2'
        )
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( additional_hours   = 16.0
        , all_in             = 0
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 4.0
        , hours_mon          = 0.0
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 4.0
        , hours_tue          = 4.0
        , hours_wed          = 4.0
        , supp_weekly_hours  = 16.0
        , travel_full        = 1
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 24.0
        , valid_from         = date.Date ("2022-08-01.00:00:00")
        , valid_to           = date.Date ("2023-09-24.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 16.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '2'
        , contract_type      = parent.ct_pt
        )
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( additional_hours   = 35.0
        , all_in             = 0
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 7.0
        , hours_mon          = 7.0
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 7.0
        , hours_tue          = 7.0
        , hours_wed          = 7.0
        , supp_weekly_hours  = 35.0
        , travel_full        = 1
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 30.0
        , valid_from         = date.Date ("2023-09-25.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 35.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '2'
        )
    leave = db.daily_record_status.lookup ('leave')
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-01-03.00:00:00')
        , last_day  = date.Date ('2022-01-05.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-01-07.00:00:00')
        , last_day  = date.Date ('2022-01-12.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-12-19.00:00:00')
        , last_day  = date.Date ('2023-01-03.00:00:00')
        , status    = '7'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-12-19.00:00:00')
        , last_day  = date.Date ('2022-12-30.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-01-03.00:00:00')
        , last_day  = date.Date ('2023-01-03.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-03-14.00:00:00')
        , last_day  = date.Date ('2023-03-21.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-08-08.00:00:00')
        , last_day  = date.Date ('2023-08-08.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-01-03'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '44'
        ) 
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-01-04'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-01-05'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-01-07'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-01-08'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-01-09'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-01-10'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-01-11'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-01-12'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 8.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-20'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        ) 
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-21'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-22'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-23'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-24'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-25'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-26'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-27'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-28'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-29'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-30'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-31'))
    assert len (dr) == 1
    dr = dr [0]
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-01'))
    assert len (dr) == 1
    dr = dr [0]
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-02'))
    assert len (dr) == 1
    dr = dr [0]
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-03'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '44'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-08'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '44'
        ) 
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5' 
        ) 
    db.daily_record.set (dr, status = leave)
    db.commit ()
# end def import_data_27
