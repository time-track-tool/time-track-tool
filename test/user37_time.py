from roundup import date

def import_data_37 (db, user, olo, vac_aliq = '1'):
    otp = None
    db.user_dynamic.create \
        ( all_in             = 1
        , booking_allowed    = 1
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
        , valid_from         = date.Date ("2018-04-03.00:00:00")
        , valid_to           = date.Date ("2020-09-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = vac_aliq
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
        , valid_from         = date.Date ("2020-09-01.00:00:00")
        , valid_to           = date.Date ("2020-11-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = vac_aliq
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
        , valid_from         = date.Date ("2020-11-01.00:00:00")
        , valid_to           = date.Date ("2021-02-25.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = vac_aliq
        )
    if vac_aliq != '1':
        vc = db.vacation_correction.create \
            ( user     = user
            , date     = date.Date ('2021-03-25')
            , absolute = True
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
        , valid_from         = date.Date ("2021-03-25.00:00:00")
        , valid_to           = date.Date ("2022-10-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = vac_aliq
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
        , valid_from         = date.Date ("2022-10-01.00:00:00")
        , valid_to           = date.Date ("2025-01-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = vac_aliq
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
        , valid_from         = date.Date ("2025-01-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = vac_aliq
        )
    leave = db.daily_record_status.lookup ('leave')
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2018-07-27.00:00:00')
        , last_day  = date.Date ('2018-07-30.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2018-10-29.00:00:00')
        , last_day  = date.Date ('2018-11-02.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2018-11-14.00:00:00')
        , last_day  = date.Date ('2018-11-16.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2018-12-21.00:00:00')
        , last_day  = date.Date ('2018-12-28.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-01-28.00:00:00')
        , last_day  = date.Date ('2019-01-28.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-03-22.00:00:00')
        , last_day  = date.Date ('2019-03-25.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-04-03.00:00:00')
        , last_day  = date.Date ('2019-04-03.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-04-11.00:00:00')
        , last_day  = date.Date ('2019-04-12.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-05-13.00:00:00')
        , last_day  = date.Date ('2019-05-24.00:00:00')
        , status    = '7'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-05-13.00:00:00')
        , last_day  = date.Date ('2019-05-15.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-05-16.00:00:00')
        , last_day  = date.Date ('2019-05-24.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-07-01.00:00:00')
        , last_day  = date.Date ('2019-07-01.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-08-22.00:00:00')
        , last_day  = date.Date ('2019-09-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-11-06.00:00:00')
        , last_day  = date.Date ('2019-11-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-11-18.00:00:00')
        , last_day  = date.Date ('2019-11-18.00:00:00')
        , status    = '7'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-11-25.00:00:00')
        , last_day  = date.Date ('2019-11-28.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-12-10.00:00:00')
        , last_day  = date.Date ('2019-12-10.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-12-17.00:00:00')
        , last_day  = date.Date ('2019-12-17.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2019-12-27.00:00:00')
        , last_day  = date.Date ('2020-01-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-01-23.00:00:00')
        , last_day  = date.Date ('2020-01-23.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-01-27.00:00:00')
        , last_day  = date.Date ('2020-01-27.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-02-06.00:00:00')
        , last_day  = date.Date ('2020-02-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-03-02.00:00:00')
        , last_day  = date.Date ('2020-03-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-04-06.00:00:00')
        , last_day  = date.Date ('2020-04-10.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-06-09.00:00:00')
        , last_day  = date.Date ('2020-06-09.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-06-29.00:00:00')
        , last_day  = date.Date ('2020-07-10.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-11-23.00:00:00')
        , last_day  = date.Date ('2020-11-27.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-12-07.00:00:00')
        , last_day  = date.Date ('2020-12-07.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-12-21.00:00:00')
        , last_day  = date.Date ('2020-12-23.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2020-12-28.00:00:00')
        , last_day  = date.Date ('2020-12-31.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2021-01-04.00:00:00')
        , last_day  = date.Date ('2021-01-08.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2021-02-19.00:00:00')
        , last_day  = date.Date ('2021-02-19.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2021-02-22.00:00:00')
        , last_day  = date.Date ('2021-02-23.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2021-02-24.00:00:00')
        , last_day  = date.Date ('2021-02-24.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2021-07-01.00:00:00')
        , last_day  = date.Date ('2021-07-01.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2021-08-24.00:00:00')
        , last_day  = date.Date ('2021-08-24.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2021-09-06.00:00:00')
        , last_day  = date.Date ('2021-09-17.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-02-14.00:00:00')
        , last_day  = date.Date ('2022-02-14.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-05-16.00:00:00')
        , last_day  = date.Date ('2022-05-20.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-06-22.00:00:00')
        , last_day  = date.Date ('2022-06-22.00:00:00')
        , status    = '7'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-06-28.00:00:00')
        , last_day  = date.Date ('2022-06-28.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-08-01.00:00:00')
        , last_day  = date.Date ('2022-08-05.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-09-02.00:00:00')
        , last_day  = date.Date ('2022-09-02.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-09-05.00:00:00')
        , last_day  = date.Date ('2022-09-13.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-10-13.00:00:00')
        , last_day  = date.Date ('2022-10-13.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-10-27.00:00:00')
        , last_day  = date.Date ('2022-10-28.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-10-31.00:00:00')
        , last_day  = date.Date ('2022-10-31.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-11-14.00:00:00')
        , last_day  = date.Date ('2022-11-14.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-12-26.00:00:00')
        , last_day  = date.Date ('2023-01-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-04-06.00:00:00')
        , last_day  = date.Date ('2023-04-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-04-11.00:00:00')
        , last_day  = date.Date ('2023-04-12.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-05-02.00:00:00')
        , last_day  = date.Date ('2023-05-05.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-06-08.00:00:00')
        , last_day  = date.Date ('2023-06-09.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-07-12.00:00:00')
        , last_day  = date.Date ('2023-07-12.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-07-20.00:00:00')
        , last_day  = date.Date ('2023-07-20.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-08-21.00:00:00')
        , last_day  = date.Date ('2023-09-01.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-11-13.00:00:00')
        , last_day  = date.Date ('2023-11-17.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-12-18.00:00:00')
        , last_day  = date.Date ('2023-12-22.00:00:00')
        , status    = '7'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-12-20.00:00:00')
        , last_day  = date.Date ('2023-12-28.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-12-29.00:00:00')
        , last_day  = date.Date ('2023-12-29.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-01-02.00:00:00')
        , last_day  = date.Date ('2024-01-05.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-01-08.00:00:00')
        , last_day  = date.Date ('2024-01-09.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-04-02.00:00:00')
        , last_day  = date.Date ('2024-04-02.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-04-25.00:00:00')
        , last_day  = date.Date ('2024-04-26.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-07-01.00:00:00')
        , last_day  = date.Date ('2024-07-05.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-08-19.00:00:00')
        , last_day  = date.Date ('2024-08-30.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-11-18.00:00:00')
        , last_day  = date.Date ('2024-11-20.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-11-21.00:00:00')
        , last_day  = date.Date ('2024-11-22.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-12-27.00:00:00')
        , last_day  = date.Date ('2025-01-03.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-04-22.00:00:00')
        , last_day  = date.Date ('2025-04-22.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-05-08.00:00:00')
        , last_day  = date.Date ('2025-05-08.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-05-30.00:00:00')
        , last_day  = date.Date ('2025-06-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-07-14.00:00:00')
        , last_day  = date.Date ('2025-07-25.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-10-27.00:00:00')
        , last_day  = date.Date ('2025-10-27.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-11-17.00:00:00')
        , last_day  = date.Date ('2025-11-21.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-12-29.00:00:00')
        , last_day  = date.Date ('2026-01-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2026-04-02.00:00:00')
        , last_day  = date.Date ('2026-04-02.00:00:00')
        , status    = '3'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2026-05-18.00:00:00')
        , last_day  = date.Date ('2026-05-22.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2026-07-13.00:00:00')
        , last_day  = date.Date ('2026-07-24.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2026-09-16.00:00:00')
        , last_day  = date.Date ('2026-09-18.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2026-12-28.00:00:00')
        , last_day  = date.Date ('2026-12-30.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-07-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-07-28'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-07-29'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-07-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-10-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-10-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-10-31'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-11-01'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-11-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-11-14'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-11-15'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-11-16'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-12-21'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-12-22'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-12-23'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-12-24'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-12-25'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-12-26'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-12-27'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2018-12-28'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-01-28'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-03-22'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-03-23'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-03-24'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-03-25'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-04-03'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-04-11'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-04-12'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-13'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-14'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-15'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-16'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-17'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-18'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-19'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-20'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-21'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-22'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-23'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-05-24'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-07-01'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-08-22'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-08-23'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-08-24'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-08-25'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-08-26'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-08-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-08-28'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-08-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-08-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-08-31'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-09-01'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-09-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-09-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-09-04'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-09-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-09-06'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-11-06'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-11-25'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-11-26'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-11-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-11-28'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-12-10'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-12-17'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-12-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-12-28'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-12-29'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-12-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2019-12-31'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-01-01'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-01-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-01-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-01-04'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-01-05'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-01-06'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-01-23'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-01-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-02-06'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-03-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-03-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-03-04'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-03-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-03-06'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-04-06'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-04-07'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-04-08'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-04-09'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-04-10'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-06-09'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-06-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-06-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-07-01'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-07-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-07-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-07-04'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-07-05'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-07-06'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-07-07'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-07-08'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-07-09'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-07-10'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-11-23'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-11-24'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-11-25'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-11-26'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-11-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-07'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-21'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-22'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-23'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-28'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2020-12-31'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-01-04'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-01-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-01-06'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-01-07'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-01-08'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-02-19'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-02-22'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-02-23'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-02-24'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-07-01'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-08-24'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-06'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-07'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-08'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-09'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-10'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-11'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-12'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-13'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-14'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-15'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-16'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2021-09-17'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-02-14'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-05-16'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-05-17'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-05-18'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-05-19'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-05-20'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-06-28'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-08-01'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-08-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-08-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-08-04'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-08-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-09-02'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-09-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-09-06'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-09-07'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-09-08'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-09-09'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-09-10'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-09-11'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-09-12'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-09-13'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-10-13'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-10-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-10-28'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-10-31'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-11-14'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-26'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-28'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-31'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-01'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-04'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-06'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-04-06'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-04-11'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-04-12'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-05-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-05-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-05-04'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-05-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-08'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-09'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-07-12'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-07-20'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-21'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-22'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-23'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-24'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-25'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-26'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-27'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-28'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-31'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-09-01'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-11-13'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-11-14'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-11-15'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-11-16'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-11-17'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-20'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-21'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-22'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-23'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-24'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-25'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-26'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-27'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-28'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-04'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-08'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-09'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-04-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-04-25'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-04-26'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-07-01'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-07-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-07-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-07-04'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-07-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-19'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-20'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-21'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-22'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-23'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-24'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-25'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-26'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-28'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-11-18'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-11-19'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-11-20'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-11-21'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-11-22'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-28'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-29'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-31'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-01-01'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-01-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-01-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-22'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-05-08'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-05-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-05-31'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-06-01'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-06-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-06-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-06-04'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-06-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-06-06'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-14'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-15'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-16'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-17'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-18'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-19'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-20'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-21'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-22'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-24'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-07-25'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-10-27'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-17'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-18'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-19'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-20'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-21'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-31'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-01-01'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-01-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-01-03'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-01-04'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-01-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-01-06'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-05-18'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-05-19'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-05-20'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-05-21'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-05-22'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-13'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-14'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-15'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-16'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-17'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-18'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-19'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-20'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-21'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-22'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-23'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-07-24'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-09-16'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-09-17'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-09-18'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-12-28'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-12-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2026-12-30'))
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
# end def import_data_37
