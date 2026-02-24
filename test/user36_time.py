from roundup import date

def import_data_36 (db, user, olo, parent):
    ct_by_name = {}
    id = db.contract_type.create \
        ( name  = 'marginal employment'
        , order = 1
        )
    ct_by_name ['marginal employment'] = id
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( additional_hours   = 20.0
        , all_in             = 0
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 4.0
        , hours_mon          = 4.0
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 4.0
        , hours_tue          = 4.0
        , hours_wed          = 4.0
        , supp_weekly_hours  = 20.0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2022-09-16.00:00:00")
        , valid_to           = date.Date ("2023-02-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 20.0
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
        , valid_from         = date.Date ("2023-02-01.00:00:00")
        , valid_to           = date.Date ("2025-01-01.00:00:00")
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
        , valid_from         = date.Date ("2025-02-01.00:00:00")
        , valid_to           = date.Date ("2025-08-01.00:00:00")
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
        , valid_from         = date.Date ("2025-08-01.00:00:00")
        , valid_to           = date.Date ("2025-12-05.00:00:00")
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
        ( additional_hours   = 3.0
        , all_in             = 0
        , booking_allowed    = 1
        , contract_type      = ct_by_name ['marginal employment']
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 1.0
        , hours_mon          = 0.5
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 0.5
        , hours_tue          = 0.5
        , hours_wed          = 0.5
        , supp_weekly_hours  = 3.0
        , travel_full        = 0
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 25.0
        , valid_from         = date.Date ("2025-12-05.00:00:00")
        , valid_to           = date.Date ("2026-06-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 3.0
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
        , valid_from         = date.Date ("2026-06-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        )
    username = db.user.get (user, 'username')
    aw_by_ct_name = {}
    id = db.auto_wp.create \
        ( name              = 'Special-leave'
        , contract_type     = ct_by_name ['marginal employment']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.special_tp
        )
    aw_by_ct_name [('marginal employment', 'Special-leave')] = id
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
        , contract_type     = ct_by_name ['marginal employment']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.nursing_tp
        )
    aw_by_ct_name [('marginal employment', 'Nursing-leave')] = id
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
        , contract_type     = ct_by_name ['marginal employment']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.sick_tp
        )
    aw_by_ct_name [('marginal employment', 'Sick-leave')] = id
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
        , contract_type     = ct_by_name ['marginal employment']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.holiday_tp
        )
    aw_by_ct_name [('marginal employment', 'Public-Holiday')] = id
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
        , contract_type     = ct_by_name ['marginal employment']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.vacation_tp
        )
    aw_by_ct_name [('marginal employment', 'Vacation')] = id
    id = db.auto_wp.create \
        ( name              = 'Vacation'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.vacation_tp
        )
    aw_by_ct_name [(None, 'Vacation')] = id
    id = db.auto_wp.create \
        ( name              = 'Comp\\Flexi-Time'
        , contract_type     = ct_by_name ['marginal employment']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.flexi_tp
        )
    aw_by_ct_name [('marginal employment', 'Comp\\Flexi-Time')] = id
    id = db.auto_wp.create \
        ( name              = 'Comp\\Flexi-Time'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.flexi_tp
        )
    aw_by_ct_name [(None, 'Comp\\Flexi-Time')] = id
    id = db.auto_wp.create \
        ( name              = 'Medical-Consultation'
        , contract_type     = ct_by_name ['marginal employment']
        , durations_allowed = 0
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.medical_tp
        )
    aw_by_ct_name [('marginal employment', 'Medical-Consultation')] = id
    id = db.auto_wp.create \
        ( name              = 'Medical-Consultation'
        , durations_allowed = 0
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.medical_tp
        )
    aw_by_ct_name [(None, 'Medical-Consultation')] = id
    au_wp_0 = db.time_wp.create \
        ( name              = '%s -2025-01-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Special-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-09-16.00:00:00')
        , time_end          = date.Date ('2025-01-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.special_tp
        )
    au_wp_1 = db.time_wp.create \
        ( name              = '%s -2025-01-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-09-16.00:00:00')
        , time_end          = date.Date ('2025-01-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_2 = db.time_wp.create \
        ( name              = '%s -2025-01-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-09-16.00:00:00')
        , time_end          = date.Date ('2025-01-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_3 = db.time_wp.create \
        ( name              = '%s -2025-01-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-09-16.00:00:00')
        , time_end          = date.Date ('2025-01-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_4 = db.time_wp.create \
        ( name              = '%s -2025-01-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-09-16.00:00:00')
        , time_end          = date.Date ('2025-01-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_5 = db.time_wp.create \
        ( name              = '%s -2025-01-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Comp\\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-09-16.00:00:00')
        , time_end          = date.Date ('2025-01-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_6 = db.time_wp.create \
        ( name              = '%s -2025-01-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2022-09-16.00:00:00')
        , time_end          = date.Date ('2025-01-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    au_wp_7 = db.time_wp.create \
        ( name              = '%s -2025-12-05' % username
        , auto_wp           = aw_by_ct_name [(None, 'Special-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-02-01.00:00:00')
        , time_end          = date.Date ('2025-12-05.00:00:00')
        , responsible       = parent.user0
        , project           = parent.special_tp
        )
    au_wp_8 = db.time_wp.create \
        ( name              = '%s -2025-12-05' % username
        , auto_wp           = aw_by_ct_name [(None, 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-02-01.00:00:00')
        , time_end          = date.Date ('2025-12-05.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_9 = db.time_wp.create \
        ( name              = '%s -2025-12-05' % username
        , auto_wp           = aw_by_ct_name [(None, 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-02-01.00:00:00')
        , time_end          = date.Date ('2025-12-05.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_10 = db.time_wp.create \
        ( name              = '%s -2025-12-05' % username
        , auto_wp           = aw_by_ct_name [(None, 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-02-01.00:00:00')
        , time_end          = date.Date ('2025-12-05.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_11 = db.time_wp.create \
        ( name              = '%s -2025-12-05' % username
        , auto_wp           = aw_by_ct_name [(None, 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-02-01.00:00:00')
        , time_end          = date.Date ('2025-12-05.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_12 = db.time_wp.create \
        ( name              = '%s -2025-12-05' % username
        , auto_wp           = aw_by_ct_name [(None, 'Comp\\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-02-01.00:00:00')
        , time_end          = date.Date ('2025-12-05.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_13 = db.time_wp.create \
        ( name              = '%s -2025-12-05' % username
        , auto_wp           = aw_by_ct_name [(None, 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2025-02-01.00:00:00')
        , time_end          = date.Date ('2025-12-05.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    au_wp_14 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Special-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.special_tp
        )
    au_wp_15 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_16 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_17 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_18 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_19 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Comp\\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_20 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    au_wp_21 = db.time_wp.create \
        ( name              = '%s -2026-06-01' % username
        , auto_wp           = aw_by_ct_name [('marginal employment', 'Special-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-12-05.00:00:00')
        , time_end          = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.special_tp
        )
    au_wp_22 = db.time_wp.create \
        ( name              = '%s -2026-06-01' % username
        , auto_wp           = aw_by_ct_name [('marginal employment', 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-12-05.00:00:00')
        , time_end          = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_23 = db.time_wp.create \
        ( name              = '%s -2026-06-01' % username
        , auto_wp           = aw_by_ct_name [('marginal employment', 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-12-05.00:00:00')
        , time_end          = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_24 = db.time_wp.create \
        ( name              = '%s -2026-06-01' % username
        , auto_wp           = aw_by_ct_name [('marginal employment', 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-12-05.00:00:00')
        , time_end          = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_25 = db.time_wp.create \
        ( name              = '%s -2026-06-01' % username
        , auto_wp           = aw_by_ct_name [('marginal employment', 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-12-05.00:00:00')
        , time_end          = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_26 = db.time_wp.create \
        ( name              = '%s -2026-06-01' % username
        , auto_wp           = aw_by_ct_name [('marginal employment', 'Comp\\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2025-12-05.00:00:00')
        , time_end          = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_27 = db.time_wp.create \
        ( name              = '%s -2026-06-01' % username
        , auto_wp           = aw_by_ct_name [('marginal employment', 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2025-12-05.00:00:00')
        , time_end          = date.Date ('2026-06-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2025-12-05.00:00:00')
        , absolute = 1
        , days     = 0.0
        , contract_type = '1'
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2026-06-01.00:00:00')
        , absolute = 0
        , days     = 0.0
        )
    leave = db.daily_record_status.lookup ('leave')
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-12-05.00:00:00')
        , last_day  = date.Date ('2022-12-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-12-07.00:00:00')
        , last_day  = date.Date ('2022-12-09.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2022-12-23.00:00:00')
        , last_day  = date.Date ('2022-12-31.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-01-02.00:00:00')
        , last_day  = date.Date ('2023-01-08.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-02-27.00:00:00')
        , last_day  = date.Date ('2023-02-28.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-05-19.00:00:00')
        , last_day  = date.Date ('2023-05-19.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-06-05.00:00:00')
        , last_day  = date.Date ('2023-06-16.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-07-19.00:00:00')
        , last_day  = date.Date ('2023-07-21.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-08-14.00:00:00')
        , last_day  = date.Date ('2023-08-20.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-10-27.00:00:00')
        , last_day  = date.Date ('2023-10-31.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-12-27.00:00:00')
        , last_day  = date.Date ('2024-01-07.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-01-29.00:00:00')
        , last_day  = date.Date ('2024-02-04.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-04-24.00:00:00')
        , last_day  = date.Date ('2024-04-26.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-04-29.00:00:00')
        , last_day  = date.Date ('2024-05-05.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-05-10.00:00:00')
        , last_day  = date.Date ('2024-05-10.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-05-31.00:00:00')
        , last_day  = date.Date ('2024-05-31.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-08-12.00:00:00')
        , last_day  = date.Date ('2024-08-14.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-08-16.00:00:00')
        , last_day  = date.Date ('2024-08-25.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-12-05.00:00:00')
        , last_day  = date.Date ('2024-12-05.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-12-06.00:00:00')
        , last_day  = date.Date ('2024-12-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-12-09.00:00:00')
        , last_day  = date.Date ('2024-12-09.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-12-10.00:00:00')
        , last_day  = date.Date ('2024-12-10.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-12-18.00:00:00')
        , last_day  = date.Date ('2024-12-20.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2024-12-21.00:00:00')
        , last_day  = date.Date ('2024-12-31.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-03-21.00:00:00')
        , last_day  = date.Date ('2025-03-21.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-04-07.00:00:00')
        , last_day  = date.Date ('2025-04-07.00:00:00')
        , status    = '4'
        , time_wp   = au_wp_11
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-04-17.00:00:00')
        , last_day  = date.Date ('2025-04-22.00:00:00')
        , status    = '4'
        , time_wp   = au_wp_11
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-05-30.00:00:00')
        , last_day  = date.Date ('2025-05-30.00:00:00')
        , status    = '4'
        , time_wp   = au_wp_11
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-06-26.00:00:00')
        , last_day  = date.Date ('2025-06-26.00:00:00')
        , status    = '4'
        , time_wp   = au_wp_11
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-08-03.00:00:00')
        , last_day  = date.Date ('2025-08-17.00:00:00')
        , status    = '4'
        , time_wp   = au_wp_11
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2025-11-23.00:00:00')
        , last_day  = date.Date ('2025-12-04.00:00:00')
        , status    = '4'
        , time_wp   = au_wp_11
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2026-06-29.00:00:00')
        , last_day  = date.Date ('2026-07-05.00:00:00')
        , status    = '3'
        , time_wp   = au_wp_18
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2026-09-21.00:00:00')
        , last_day  = date.Date ('2026-09-27.00:00:00')
        , status    = '3'
        , time_wp   = au_wp_18
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2026-12-21.00:00:00')
        , last_day  = date.Date ('2027-01-03.00:00:00')
        , status    = '3'
        , time_wp   = au_wp_18
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2026-04-27.00:00:00')
        , last_day  = date.Date ('2026-05-03.00:00:00')
        , status    = '3'
        , time_wp   = au_wp_25
        )
    id = aw_by_ct_name [('marginal employment', 'Special-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Special-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('marginal employment', 'Nursing-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Nursing-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('marginal employment', 'Sick-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Sick-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('marginal employment', 'Public-Holiday')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Public-Holiday')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('marginal employment', 'Vacation')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Vacation')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('marginal employment', 'Comp\\Flexi-Time')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Comp\\Flexi-Time')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('marginal employment', 'Medical-Consultation')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Medical-Consultation')]
    db.auto_wp.set (id, is_valid = True)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-05'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-06'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-07'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-08'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2022-12-09'))
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
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
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
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-02'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-03'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-04'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-05'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-06'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '1'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-07'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-01-08'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-02-27'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-02-28'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-05-19'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-06'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-07'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-10'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-11'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-12'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-13'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-14'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-15'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-06-16'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-07-19'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-07-21'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-14'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-15'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-16'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-17'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-18'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-19'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-08-20'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-10-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-10-28'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-10-29'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-10-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-10-31'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-28'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-30'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-31'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-01'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-06'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-07'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-01-31'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-02-01'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-02-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-02-03'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-02-04'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-04-24'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-04-25'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-04-26'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-04-29'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-04-30'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-05-01'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-05-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-05-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-05-04'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-05-05'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-05-10'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-05-31'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-12'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-13'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-14'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-16'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-17'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-08-18'))
    assert len (dr) == 1
    dr = dr [0]
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-05'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-06'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-09'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-10'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-18'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-19'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-20'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-21'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-22'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-23'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-24'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-25'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2024-12-26'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-03-21'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-07'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-17'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-18'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-19'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-20'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-21'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-04-22'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-06-26'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-03'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-04'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-05'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-06'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-07'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-08'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-09'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-10'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-11'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-12'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-13'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-14'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-15'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-16'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-08-17'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-23'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-24'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-25'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-26'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-27'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-28'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-29'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-11-30'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-01'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-02'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-03'))
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
    dr = db.daily_record.filter (None, dict (user = user, date = '2025-12-04'))
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
# end def import_data_36
