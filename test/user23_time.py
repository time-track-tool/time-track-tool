from roundup import date

def import_data_23 (db, user, olo, parent):
    ct_by_name = {}
    ct_by_name ['Internship'] = parent.ct_intern
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    holo = db.work_location.create \
        ( code = 'Home-AT'
        , description = 'Home Office Location'
        )
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
        , valid_from         = date.Date ("2022-03-01.00:00:00")
        , valid_to           = date.Date ("2022-07-01.00:00:00")
        , weekend_allowed    = 0
        , weekly_hours       = 20.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '1'
        , contract_type      = ct_by_name ['Internship']
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
        , valid_from         = date.Date ("2022-07-01.00:00:00")
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
        , contract_type     = ct_by_name ['Internship']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.special_tp
        )
    aw_by_ct_name [('Internship', 'Special-leave')] = id
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
        , contract_type     = ct_by_name ['Internship']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.nursing_tp
        )
    aw_by_ct_name [('Internship', 'Nursing-leave')] = id
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
        ( name              = 'Sick-leave'
        , contract_type     = ct_by_name ['Internship']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.sick_tp
        )
    aw_by_ct_name [('Internship', 'Sick-leave')] = id
    id = db.auto_wp.create \
        ( name              = 'Public-Holiday'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.holiday_tp
        )
    aw_by_ct_name [(None, 'Public-Holiday')] = id
    id = db.auto_wp.create \
        ( name              = 'Public-Holiday'
        , contract_type     = ct_by_name ['Internship']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.holiday_tp
        )
    aw_by_ct_name [('Internship', 'Public-Holiday')] = id
    id = db.auto_wp.create \
        ( name              = 'Vacation'
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.vacation_tp
        )
    aw_by_ct_name [(None, 'Vacation')] = id
    id = db.auto_wp.create \
        ( name              = 'Vacation'
        , contract_type     = ct_by_name ['Internship']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.vacation_tp
        )
    aw_by_ct_name [('Internship', 'Vacation')] = id
    id = db.auto_wp.create \
        ( name              = 'Comp\Flexi-Time'
        , contract_type     = ct_by_name ['Internship']
        , durations_allowed = 1
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.flexi_tp
        )
    aw_by_ct_name [('Internship', 'Comp\Flexi-Time')] = id
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
        , contract_type     = ct_by_name ['Internship']
        , durations_allowed = 0
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.medical_tp
        )
    aw_by_ct_name [('Internship', 'Medical-Consultation')] = id
    id = db.auto_wp.create \
        ( name              = 'Medical-Consultation'
        , durations_allowed = 0
        , is_valid          = 0
        , org_location      = olo
        , time_project      = parent.medical_tp
        )
    aw_by_ct_name [(None, 'Medical-Consultation')] = id
    au_wp_0 = db.time_wp.create \
        ( name              = '%s -2021-09-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Special-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-07-01.00:00:00')
        , time_end          = date.Date ('2021-09-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.special_tp
        )
    au_wp_1 = db.time_wp.create \
        ( name              = '%s -2021-09-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-07-01.00:00:00')
        , time_end          = date.Date ('2021-09-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_2 = db.time_wp.create \
        ( name              = '%s -2021-09-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-07-01.00:00:00')
        , time_end          = date.Date ('2021-09-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_3 = db.time_wp.create \
        ( name              = '%s -2021-09-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-07-01.00:00:00')
        , time_end          = date.Date ('2021-09-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_4 = db.time_wp.create \
        ( name              = '%s -2021-09-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-07-01.00:00:00')
        , time_end          = date.Date ('2021-09-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_5 = db.time_wp.create \
        ( name              = '%s -2021-09-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Comp\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2021-07-01.00:00:00')
        , time_end          = date.Date ('2021-09-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_6 = db.time_wp.create \
        ( name              = '%s -2021-09-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2021-07-01.00:00:00')
        , time_end          = date.Date ('2021-09-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    au_wp_7 = db.time_wp.create \
        ( name              = '%s -2022-07-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Special-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-03-01.00:00:00')
        , time_end          = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.special_tp
        )
    au_wp_8 = db.time_wp.create \
        ( name              = '%s -2022-07-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-03-01.00:00:00')
        , time_end          = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_9 = db.time_wp.create \
        ( name              = '%s -2022-07-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-03-01.00:00:00')
        , time_end          = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_10 = db.time_wp.create \
        ( name              = '%s -2022-07-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-03-01.00:00:00')
        , time_end          = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_11 = db.time_wp.create \
        ( name              = '%s -2022-07-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-03-01.00:00:00')
        , time_end          = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_12 = db.time_wp.create \
        ( name              = '%s -2022-07-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Comp\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-03-01.00:00:00')
        , time_end          = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_13 = db.time_wp.create \
        ( name              = '%s -2022-07-01' % username
        , auto_wp           = aw_by_ct_name [('Internship', 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2022-03-01.00:00:00')
        , time_end          = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    au_wp_14 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Special-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.special_tp
        )
    au_wp_15 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Nursing-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.nursing_tp
        )
    au_wp_16 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Sick-leave')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.sick_tp
        )
    au_wp_17 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Public-Holiday')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.holiday_tp
        )
    au_wp_18 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Vacation')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.vacation_tp
        )
    au_wp_19 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Comp\Flexi-Time')]
        , bookers           = [user]
        , durations_allowed = 1
        , time_start        = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.flexi_tp
        )
    au_wp_20 = db.time_wp.create \
        ( name              = username
        , auto_wp           = aw_by_ct_name [(None, 'Medical-Consultation')]
        , bookers           = [user]
        , durations_allowed = 0
        , time_start        = date.Date ('2022-07-01.00:00:00')
        , responsible       = parent.user0
        , project           = parent.medical_tp
        )
    id = aw_by_ct_name [('Internship', 'Special-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Special-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('Internship', 'Nursing-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Nursing-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Sick-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('Internship', 'Sick-leave')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Public-Holiday')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('Internship', 'Public-Holiday')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Vacation')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('Internship', 'Vacation')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('Internship', 'Comp\Flexi-Time')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Comp\Flexi-Time')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [('Internship', 'Medical-Consultation')]
    db.auto_wp.set (id, is_valid = True)
    id = aw_by_ct_name [(None, 'Medical-Consultation')]
    db.auto_wp.set (id, is_valid = True)
#    ls = db.leave_submission.create \
#        ( user      = user
#        , first_day = date.Date ('2022-07-11.00:00:00')
#        , last_day  = date.Date ('2022-07-11.00:00:00')
#        , status    = '4'
#        , time_wp   = au_wp_18
#        )
#    ls = db.leave_submission.create \
#        ( user      = user
#        , first_day = date.Date ('2022-08-08.00:00:00')
#        , last_day  = date.Date ('2022-08-09.00:00:00')
#        , status    = '4'
#        , time_wp   = au_wp_18
#        )
#    ls = db.leave_submission.create \
#        ( user      = user
#        , first_day = date.Date ('2022-08-17.00:00:00')
#        , last_day  = date.Date ('2022-08-17.00:00:00')
#        , status    = '4'
#        , time_wp   = au_wp_18
#        )
#    ls = db.leave_submission.create \
#        ( user      = user
#        , first_day = date.Date ('2022-08-26.00:00:00')
#        , last_day  = date.Date ('2022-08-26.00:00:00')
#        , status    = '4'
#        , time_wp   = au_wp_18
#        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '4'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '13:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '13:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '13:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '14:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 4.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '6'
        )
    tatp = db.time_activity.create \
        ( name     = 'Travel passive'
        , travel   = 1
        , is_valid = True
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , time_activity = tatp
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '09:00'
        , work_location = '3'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '17:30'
        , work_location = '6'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , time_activity = tatp
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:30'
        , end           = '18:30'
        , work_location = '3'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-03-31.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 4.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 2.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '11:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = au_wp_10
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = au_wp_10
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 2.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-04-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.25
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '13:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:45'
        , end           = '17:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '6'
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
        , duration      = 2.5
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '15:30'
        , work_location = holo
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '13:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:30'
        , end           = '16:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '11:00'
        , work_location = '4'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.75
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '09:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.75
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '11:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '10:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '8'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '10:00'
        , end           = '13:45'
        , work_location = '4'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:15'
        , end           = '17:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '7'
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
        , duration      = 3.0
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '7'
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
        , duration      = 1.5
        , wp            = '7'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '14:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:00'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '6'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '11:30'
        , work_location = '4'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:00'
        , end           = '16:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.25
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '14:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 5.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 5.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = au_wp_10
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-05-31.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 5.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = au_wp_10
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 5.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 4.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = au_wp_10
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 6.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 3.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '5'
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
        , duration      = 3.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
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
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '5'
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
        , duration      = 3.0
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:00'
        , end           = '17:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.5
        , wp            = '5'
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
        , duration      = 3.0
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '16:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-06-30.00:00:00')
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
        , start         = '13:00'
        , end           = '15:00'
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
        , duration      = 1.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '16:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-04.00:00:00')
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
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '09:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '15:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '9'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '13:00'
        , end           = '16:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 1.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:30'
        , end           = '18:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
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
        , duration      = 2.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.0
        , wp            = au_wp_12
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
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
        , duration      = 2.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '14:30'
        , end           = '18:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.25
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:15'
        , end           = '13:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 6.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 6.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:30'
        , end           = '19:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.5
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '11'
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
        , duration      = 2.25
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '14:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-07-31.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 6.0
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-02.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-03.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 6.0
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '11'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-04.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
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
        , duration      = 2.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '17:45'
        , end           = '19:45'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-05.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:00'
        , end           = '14:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-06.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-07.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-08.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.0
        , wp            = au_wp_12
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-09.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 0.0
        , wp            = au_wp_12
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-10.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '5'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-11.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:15'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-12.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-13.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-14.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-15.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_17
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-16.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-17.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 7.75
        , wp            = au_wp_7
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , work_location = '5'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-18.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-19.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-20.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-21.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-22.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '18:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 4.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:00'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-23.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
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
        , duration      = 3.25
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '15:00'
        , end           = '18:15'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-24.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.0
        , wp            = '10'
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
        , duration      = 1.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '16:00'
        , end           = '17:30'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-25.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '15:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-26.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
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
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-27.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-28.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-29.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-30.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:30'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-08-31.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 5.0
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '17:30'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.25
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '08:45'
        , end           = '12:00'
        , work_location = '1'
        )
    dr = db.daily_record.create \
        ( user = user
        , date = date.Date ('2022-09-01.00:00:00')
        , weekend_allowed   = 0
        , required_overtime = 0
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 3.5
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '12:30'
        , end           = '16:00'
        , work_location = '1'
        )
    tr = db.time_record.create \
        ( daily_record  = dr
        , duration      = 2.75
        , wp            = '10'
        )
    db.attendance_record.create \
        ( daily_record  = dr
        , time_record   = tr
        , start         = '09:15'
        , end           = '12:00'
        , work_location = '1'
        )
    db.commit ()
# end def import_data_23
