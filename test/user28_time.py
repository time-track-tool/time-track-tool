from roundup import date

def import_data_28 (db, user, olo, parent):
    ct_by_name = {}
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    holo = db.work_location.create \
        ( code = 'Home-AT'
        , description = 'Home Office Location'
        )
    db.user_dynamic.create \
        ( additional_hours   = 15.0
        , all_in             = 0
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 3.0
        , hours_mon          = 3.0
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 3.0
        , hours_tue          = 3.0
        , hours_wed          = 3.0
        , supp_weekly_hours  = 15.0
        , travel_full        = 1
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 30.0
        , valid_from         = date.Date ("2020-09-01.00:00:00")
        , valid_to           = date.Date ("2023-03-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 15.0
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
        ( additional_hours   = 25.0
        , all_in             = 0
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 5.0
        , hours_mon          = 5.0
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 5.0
        , hours_tue          = 5.0
        , hours_wed          = 5.0
        , supp_weekly_hours  = 25.0
        , travel_full        = 1
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 30.0
        , valid_from         = date.Date ("2023-03-01.00:00:00")
        , valid_to           = date.Date ("2023-07-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 25.0
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
        ( additional_hours   = 25.0
        , all_in             = 0
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 5.0
        , hours_mon          = 5.0
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 5.0
        , hours_tue          = 5.0
        , hours_wed          = 5.0
        , supp_weekly_hours  = 25.0
        , travel_full        = 1
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 30.0
        , valid_from         = date.Date ("2023-07-01.00:00:00")
        , valid_to           = date.Date ("2023-08-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 25.0
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
        ( additional_hours   = 15.0
        , all_in             = 0
        , booking_allowed    = 1
        , do_auto_wp         = 1
        , durations_allowed  = 0
        , exemption          = 0
        , hours_fri          = 3.0
        , hours_mon          = 3.0
        , hours_sat          = 0.0
        , hours_sun          = 0.0
        , hours_thu          = 3.0
        , hours_tue          = 3.0
        , hours_wed          = 3.0
        , supp_weekly_hours  = 15.0
        , travel_full        = 1
        , vacation_day       = 1.0
        , vacation_month     = 1.0
        , vacation_yearly    = 30.0
        , valid_from         = date.Date ("2023-10-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 15.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '2'
        )
    username = db.user.get (user, 'username')
    aw_by_ct_name = {}
    id = db.auto_wp.create \
        ( name              = 'Nursing-leave'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.nursing_tp
        )
    aw_by_ct_name [(None, 'Nursing-leave')] = id
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
    id = db.auto_wp.create \
        ( name              = 'Public-Holiday'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.holiday_tp
        )
    aw_by_ct_name [(None, 'Public-Holiday')] = id
    id = db.auto_wp.create \
        ( name              = 'Sick-leave'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.sick_tp
        )
    aw_by_ct_name [(None, 'Sick-leave')] = id
    id = db.auto_wp.create \
        ( name              = 'Vacation'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.vacation_tp
        )
    aw_by_ct_name [(None, 'Vacation')] = id
    au_wp_0 = db.time_wp.create \
        ( name              = '%s -2023-08-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2023-08-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_1 = db.time_wp.create \
        ( name              = '%s -2023-08-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Comp\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2023-08-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_2 = db.time_wp.create \
        ( name              = '%s -2023-08-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2023-08-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    au_wp_3 = db.time_wp.create \
        ( name              = '%s -2023-08-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2023-08-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_4 = db.time_wp.create \
        ( name              = '%s -2023-08-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2023-08-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_5 = db.time_wp.create \
        ( name              = '%s -2023-08-01' % username
        , auto_wp           = aw_by_ct_name [(None, 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2020-09-01.00:00:00')
        , time_end          = date.Date ('2023-08-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_6 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2023-10-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_7 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Comp\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2023-10-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_8 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2023-10-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    au_wp_9 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2023-10-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_10 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2023-10-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_11 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2023-10-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    leave = db.daily_record_status.lookup ('leave')
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-01-02.00:00:00')
        , last_day  = date.Date ('2023-01-06.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-02-20.00:00:00')
        , last_day  = date.Date ('2023-02-22.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-04-20.00:00:00')
        , last_day  = date.Date ('2023-04-21.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-05-29.00:00:00')
        , last_day  = date.Date ('2023-06-02.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-06-05.00:00:00')
        , last_day  = date.Date ('2023-06-09.00:00:00')
        , status    = '4'
        , time_wp   = '44'
        )
    id = aw_by_ct_name [(None, 'Nursing-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Comp\Flexi-Time')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Medical-Consultation')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Public-Holiday')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Sick-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Vacation')]
    db.auto_wp.set (id, is_valid = True)
    db.commit ()
# end def import_data_28
