from roundup import date

def import_data_24 (db, user, olo, parent):
    ct_by_name = {}
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
        , valid_from         = date.Date ("2021-04-01.00:00:00")
        , valid_to           = date.Date ("2023-11-30.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 38.5
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
        , valid_from         = date.Date ("2023-12-01.00:00:00")
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
    au_wp_0 = db.time_wp.create \
        ( name              = '%s -2023-11-30' % username
        , auto_wp           = aw_by_ct_name [(None, 'Special-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-04-01.00:00:00')
        , time_end          = date.Date ('2023-11-30.00:00:00')
        , responsible       = parent.user0
        , project           = parent.special_tp
        )
    au_wp_1 = db.time_wp.create \
        ( name              = '%s -2023-11-30' % username
        , auto_wp           = aw_by_ct_name [(None, 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-04-01.00:00:00')
        , time_end          = date.Date ('2023-11-30.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_2 = db.time_wp.create \
        ( name              = '%s -2023-11-30' % username
        , auto_wp           = aw_by_ct_name [(None, 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-04-01.00:00:00')
        , time_end          = date.Date ('2023-11-30.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_3 = db.time_wp.create \
        ( name              = '%s -2023-11-30' % username
        , auto_wp           = aw_by_ct_name [(None, 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-04-01.00:00:00')
        , time_end          = date.Date ('2023-11-30.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    # This has incorrect name (to prevent name collision) and no end
    # date. This is later auto-corrected when auto wp is modified.
    au_wp_4 = db.time_wp.create \
        ( name              = '%s -2023-11-30 zoppel' % username
        , auto_wp           = aw_by_ct_name [(None, 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-04-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_5 = db.time_wp.create \
        ( name              = '%s -2023-11-30' % username
        , auto_wp           = aw_by_ct_name [(None, 'Comp\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-04-01.00:00:00')
        , time_end          = date.Date ('2023-11-30.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_6 = db.time_wp.create \
        ( name              = '%s -2023-11-30' % username
        , auto_wp           = aw_by_ct_name [(None, 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2021-04-01.00:00:00')
        , time_end          = date.Date ('2023-11-30.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    au_wp_7 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Special-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2023-12-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.special_tp
        )
    au_wp_8 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2023-12-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_9 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2023-12-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_10 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2023-12-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_11 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2023-12-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_12 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Comp\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2023-12-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_13 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2023-12-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2021-04-01.00:00:00')
        , absolute = 1
        , days     = 7.765
        )
    leave = db.daily_record_status.lookup ('leave')
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-12-04.00:00:00')
        , last_day  = date.Date ('2023-12-31.00:00:00')
        , status    = '7'
        , time_wp   = au_wp_4
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-12-05.00:00:00')
        , last_day  = date.Date ('2023-12-10.00:00:00')
        , status    = '4'
        , time_wp   = au_wp_4
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-12-11.00:00:00')
        , last_day  = date.Date ('2023-12-22.00:00:00')
        , status    = '7'
        , time_wp   = au_wp_4
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-12-13.00:00:00')
        , last_day  = date.Date ('2023-12-17.00:00:00')
        , status    = '4'
        , time_wp   = au_wp_11
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-12-18.00:00:00')
        , last_day  = date.Date ('2023-12-22.00:00:00')
        , status    = '4'
        , time_wp   = au_wp_11
        )
    ls = db.leave_submission.create \
        ( user      = user
        , first_day = date.Date ('2023-12-23.00:00:00')
        , last_day  = date.Date ('2023-12-31.00:00:00')
        , status    = '4'
        , time_wp   = au_wp_4
        )
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
    id = aw_by_ct_name [(None, 'Special-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Nursing-leave')]
    db.auto_wp.set (id, is_valid = True)
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '19:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '12:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '13:30'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '11:00'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:45'
        , end           = '16:30'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:30'
        , end           = '19:45'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.75
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '15:15'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '11:45'
        , work_location = holo
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:30'
        , end           = '19:30'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '15:45'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '11:30'
        , work_location = holo
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '13:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '09:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.75
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '18:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '12:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.25
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '17:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '18:45'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:15'
        , work_location = holo
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:45'
        , end           = '18:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '11:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '13:30'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '11:00'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '14:30'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '17:15'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '14:00'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '12:30'
        , work_location = holo
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = au_wp_2
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '13:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '15:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '18:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:00'
        , end           = '13:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.25
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:45'
        , end           = '11:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_3
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '13:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '13:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '17:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '18:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '19:30'
        , work_location = holo
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '14:30'
        , work_location = holo
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '10:30'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '13:30'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '10:45'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-08-31.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-09-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-12-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-12-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2023-12-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-04'))
    assert len (dr) == 1
    dr = dr [0]
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-05'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_4
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-06'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_4
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-07'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_4
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-08'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = au_wp_3
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-09'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-10'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-11'))
    assert len (dr) == 1
    dr = dr [0]
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-12'))
    assert len (dr) == 1
    dr = dr [0]
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-13'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_11
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-14'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_11
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-15'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = au_wp_11
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-16'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-17'))
    assert len (dr) == 1
    dr = dr [0]
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-18'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_11
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-19'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_11
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
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_11
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-21'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_11
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    db.daily_record.set (dr, status = leave)
    dr = db.daily_record.filter (None, dict (user = user, date = '2023-12-22'))
    assert len (dr) == 1
    dr = dr [0]
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.5
        , wp            = au_wp_11
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
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
        , wp            = au_wp_3
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
        , wp            = au_wp_3
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
        , wp            = au_wp_4
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
        , wp            = au_wp_4
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
        , wp            = au_wp_4
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
    db.commit ()
# end def import_data_24
