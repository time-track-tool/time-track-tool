from roundup import date

def import_data_31 (db, user, olo):
    sd = dict (months = 1.0, required_overtime = 1, weekly = 0)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    holo = db.work_location.create \
        ( code = 'Home-AT'
        , description = 'Home Office Location'
        )
    db.user_dynamic.create \
        ( all_in             = 0
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
        , supp_per_period    = 7.0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2022-11-01.00:00:00")
        , valid_to           = date.Date ("2023-07-14.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( additional_hours   = 38.5
        , all_in             = 0
        , booking_allowed    = 1
        , daily_worktime     = 9.0
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
        , supp_weekly_hours  = 38.5
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2023-07-14.00:00:00")
        , valid_to           = date.Date ("2023-12-02.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    otp = None
    db.user_dynamic.create \
        ( additional_hours   = 0.0
        , all_in             = 0
        , booking_allowed    = 0
        , daily_worktime     = 0.0
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , supp_weekly_hours  = 0.0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2023-12-02.00:00:00")
        , valid_to           = date.Date ("2024-03-24.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 0.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    sd = dict (months = 1.0, required_overtime = 1, weekly = 0)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( all_in             = 0
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
        , supp_per_period    = 7.0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2024-07-01.00:00:00")
        , valid_to           = date.Date ("2024-08-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( additional_hours   = 2.0
        , all_in             = 0
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 0.0
        , hours_mon          = 0.5
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 0.5
        , hours_tue          = 0.5
        , hours_wed          = 0.5
        , supp_weekly_hours  = 2.0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2024-08-01.00:00:00")
        , valid_to           = date.Date ("2024-09-16.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 2.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( additional_hours   = 2.0
        , all_in             = 0
        , booking_allowed    = 1
        , daily_worktime     = 9.0
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 0.0
        , hours_mon          = 0.5
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 0.5
        , hours_tue          = 0.5
        , hours_wed          = 0.5
        , supp_weekly_hours  = 2.0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2024-09-16.00:00:00")
        , valid_to           = date.Date ("2024-12-31.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 2.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    otp = None
    db.user_dynamic.create \
        ( all_in             = 0
        , booking_allowed    = 0
        , daily_worktime     = 9.0
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2024-12-31.00:00:00")
        , valid_to           = date.Date ("2025-02-25.00:00:00")
        , weekend_allowed    = 0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    otp = None
    db.user_dynamic.create \
        ( all_in             = 0
        , booking_allowed    = 0
        , daily_worktime     = 9.0
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2025-02-25.00:00:00")
        , valid_to           = date.Date ("2025-04-23.00:00:00")
        , weekend_allowed    = 0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    vc = db.vacation_correction.filter (None, dict (user = user))
    assert len (vc) == 1
    db.vacation_correction.set (vc [0], days = 7.765)
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2024-08-01.00:00:00')
        , absolute = 1
        , days     = 0.0
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2025-02-22.00:00:00')
        , absolute = 0
        , days     = -7.22
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2025-02-25.00:00:00')
        , absolute = 0
        , days     = 3.77
        )
    leave = db.daily_record_status.lookup ('leave')
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-12-27.00:00:00')
        , last_day  = date.Date ('2022-12-30.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-04-06.00:00:00')
        , last_day  = date.Date ('2023-04-14.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-05-04.00:00:00')
        , last_day  = date.Date ('2023-05-05.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-06-09.00:00:00')
        , last_day  = date.Date ('2023-06-23.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-08-28.00:00:00')
        , last_day  = date.Date ('2023-09-01.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-07-18.00:00:00')
        , last_day  = date.Date ('2024-07-19.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-07-22.00:00:00')
        , last_day  = date.Date ('2024-07-26.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-07-29.00:00:00')
        , last_day  = date.Date ('2024-07-31.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-10-22.00:00:00')
        , last_day  = date.Date ('2024-10-25.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-10-28.00:00:00')
        , last_day  = date.Date ('2024-10-31.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    db.commit ()
# end def import_data_31
