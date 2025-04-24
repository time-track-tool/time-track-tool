from roundup import date

def import_data_29 (db, user, olo, parent):
    ct_by_name = {}
    otp = None
    holo = db.work_location.create \
        ( code = 'Home-AT'
        , description = 'Home Office Location'
        )
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
        , valid_to           = date.Date ("2025-02-01.00:00:00")
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
        , valid_to           = date.Date ("2025-03-01.00:00:00")
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
        , valid_from         = date.Date ("2025-03-01.00:00:00")
        , valid_to           = date.Date ("2025-04-01.00:00:00")
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
        , valid_from         = date.Date ("2025-04-01.00:00:00")
        , valid_to           = date.Date ("2025-05-01.00:00:00")
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
        ( additional_hours   = 28.5
        , all_in             = 0
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 5.5
        , hours_mon          = 5.75
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 5.75
        , hours_tue          = 5.75
        , hours_wed          = 5.75
        , supp_weekly_hours  = 28.5
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2025-05-01.00:00:00")
        , valid_to           = date.Date ("2026-05-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 28.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    username = db.user.get (user, 'username')
    aw_by_ct_name = {}
    id = db.auto_wp.create \
        ( name              = 'Special-leave'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.special_tp
        )
    aw_by_ct_name [(None, 'Special-leave')] = id
    id = db.auto_wp.create \
        ( name              = 'Nursing-leave'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.nursing_tp
        )
    aw_by_ct_name [(None, 'Nursing-leave')] = id
    id = db.auto_wp.create \
        ( name              = 'Sick-leave'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.sick_tp
        )
    aw_by_ct_name [(None, 'Sick-leave')] = id
    id = db.auto_wp.create \
        ( name              = 'Public-Holiday'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.holiday_tp
        )
    aw_by_ct_name [(None, 'Public-Holiday')] = id
    id = db.auto_wp.create \
        ( name              = 'Vacation'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.vacation_tp
        )
    aw_by_ct_name [(None, 'Vacation')] = id
    id = db.auto_wp.create \
        ( name              = 'Comp\Flexi-Time'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.flexi_tp
        )
    aw_by_ct_name [(None, 'Comp\Flexi-Time')] = id
    id = db.auto_wp.create \
        ( name              = 'Medical-Consultation'
        , durations_allowed = 0
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.medical_tp
        )
    aw_by_ct_name [(None, 'Medical-Consultation')] = id
    au_wp_0 = db.time_wp.create \
        ( name              = '%s -2024-10-17' % username
        , auto_wp           = aw_by_ct_name [(None, 'Special-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2024-10-17.00:00:00')
        , responsible       = parent.user0
        , project           = parent.special_tp
        )
    au_wp_1 = db.time_wp.create \
        ( name              = '%s -2024-10-17' % username
        , auto_wp           = aw_by_ct_name [(None, 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2024-10-17.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_2 = db.time_wp.create \
        ( name              = '%s -2024-10-17' % username
        , auto_wp           = aw_by_ct_name [(None, 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2024-10-17.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_3 = db.time_wp.create \
        ( name              = '%s -2024-10-17' % username
        , auto_wp           = aw_by_ct_name [(None, 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2024-10-17.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_4 = db.time_wp.create \
        ( name              = '%s -2024-10-17' % username
        , auto_wp           = aw_by_ct_name [(None, 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2024-10-17.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_5 = db.time_wp.create \
        ( name              = '%s -2024-10-17' % username
        , auto_wp           = aw_by_ct_name [(None, 'Comp\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2024-10-17.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_6 = db.time_wp.create \
        ( name              = '%s -2024-10-17' % username
        , auto_wp           = aw_by_ct_name [(None, 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2024-10-17.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    au_wp_7 = db.time_wp.create \
        ( name              = '%s -2026-05-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Special-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2024-10-17.00:00:00')
        , time_end          = date.Date ('2026-05-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.special_tp
        )
    au_wp_8 = db.time_wp.create \
        ( name              = '%s -2026-05-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2024-10-17.00:00:00')
        , time_end          = date.Date ('2026-05-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_9 = db.time_wp.create \
        ( name              = '%s -2026-05-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2024-10-17.00:00:00')
        , time_end          = date.Date ('2026-05-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_10 = db.time_wp.create \
        ( name              = '%s -2026-05-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2024-10-17.00:00:00')
        , time_end          = date.Date ('2026-05-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_11 = db.time_wp.create \
        ( name              = '%s -2026-05-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2024-10-17.00:00:00')
        , time_end          = date.Date ('2026-05-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_12 = db.time_wp.create \
        ( name              = '%s -2026-05-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Comp\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2024-10-17.00:00:00')
        , time_end          = date.Date ('2026-05-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_13 = db.time_wp.create \
        ( name              = '%s -2026-05-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2024-10-17.00:00:00')
        , time_end          = date.Date ('2026-05-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    id = aw_by_ct_name [(None, 'Special-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Nursing-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Sick-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Public-Holiday')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Vacation')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Comp\Flexi-Time')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Medical-Consultation')]
    db.auto_wp.set (id, is_valid = True)
    db.commit ()
# end def import_data_29
