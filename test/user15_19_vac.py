from roundup import date

def import_data_15 (db, user, olo) :
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( hours_fri          = 8.0
        , hours_sun          = 0.0
        , additional_hours   = 40.0
        , hours_wed          = 8.0
        , vacation_yearly    = 30.0
        , all_in             = 0
        , valid_from         = date.Date ("2018-05-03.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 8.0
        , weekly_hours       = 40.0
        , hours_mon          = 8.0
        , hours_thu          = 8.0
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , supp_weekly_hours  = 40.0
        , valid_to           = date.Date ("2018-06-01.00:00:00")
        , weekend_allowed    = 0
        , travel_full        = 1
        , vacation_month     = 1.0
        , hours_sat          = 0.0
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
        ( hours_fri          = 8.0
        , hours_sun          = 0.0
        , additional_hours   = 40.0
        , hours_wed          = 8.0
        , vacation_yearly    = 30.0
        , all_in             = 0
        , valid_from         = date.Date ("2018-06-01.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 8.0
        , weekly_hours       = 40.0
        , hours_mon          = 8.0
        , hours_thu          = 8.0
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , supp_weekly_hours  = 40.0
        , valid_to           = date.Date ("2018-11-03.00:00:00")
        , weekend_allowed    = 0
        , travel_full        = 1
        , vacation_month     = 1.0
        , hours_sat          = 0.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '2'
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2018-01-01')
        , absolute = 1
        , days     = 0.0
        )
    db.commit ()
# end def import_data_15

def import_data_16 (db, user, olo) :
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( hours_fri          = 8.0
        , hours_sun          = 0.0
        , additional_hours   = 40.0
        , hours_wed          = 8.0
        , vacation_yearly    = 30.0
        , all_in             = 0
        , valid_from         = date.Date ("2018-04-01.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 8.0
        , weekly_hours       = 40.0
        , hours_mon          = 8.0
        , hours_thu          = 8.0
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , supp_weekly_hours  = 40.0
        , valid_to           = date.Date ("2018-06-01.00:00:00")
        , weekend_allowed    = 0
        , travel_full        = 1
        , vacation_month     = 1.0
        , hours_sat          = 0.0
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
        ( hours_fri          = 6.0
        , hours_sun          = 0.0
        , additional_hours   = 30.0
        , hours_wed          = 6.0
        , vacation_yearly    = 30.0
        , all_in             = 0
        , valid_from         = date.Date ("2018-06-01.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 6.0
        , weekly_hours       = 30.0
        , hours_mon          = 6.0
        , hours_thu          = 6.0
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , supp_weekly_hours  = 30.0
        , valid_to           = date.Date ("2018-10-02.00:00:00")
        , weekend_allowed    = 0
        , travel_full        = 1
        , vacation_month     = 1.0
        , hours_sat          = 0.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '2'
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2018-01-01')
        , absolute = 1
        , days     = 0.0
        )
    db.commit ()
# end def import_data_16

def import_data_17 (db, user, olo) :
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( hours_fri          = 6.0
        , hours_sun          = 0.0
        , additional_hours   = 30.0
        , hours_wed          = 6.0
        , vacation_yearly    = 30.0
        , all_in             = 0
        , valid_from         = date.Date ("2018-01-01.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 6.0
        , weekly_hours       = 30.0
        , hours_mon          = 6.0
        , hours_thu          = 6.0
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , supp_weekly_hours  = 30.0
        , valid_to           = date.Date ("2018-06-01.00:00:00")
        , weekend_allowed    = 0
        , travel_full        = 1
        , vacation_month     = 1.0
        , hours_sat          = 0.0
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
        ( hours_fri          = 6.0
        , hours_sun          = 0.0
        , additional_hours   = 30.0
        , hours_wed          = 6.0
        , vacation_yearly    = 30.0
        , all_in             = 0
        , valid_from         = date.Date ("2018-06-01.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 6.0
        , weekly_hours       = 30.0
        , hours_mon          = 6.0
        , hours_thu          = 6.0
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , supp_weekly_hours  = 30.0
        , valid_to           = date.Date ("2018-08-23.00:00:00")
        , weekend_allowed    = 0
        , travel_full        = 1
        , vacation_month     = 1.0
        , hours_sat          = 0.0
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
        ( hours_fri          = 6.0
        , hours_sun          = 0.0
        , additional_hours   = 30.0
        , hours_wed          = 6.0
        , vacation_yearly    = 30.0
        , all_in             = 0
        , valid_from         = date.Date ("2018-08-23.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 6.0
        , weekly_hours       = 30.0
        , hours_mon          = 6.0
        , hours_thu          = 6.0
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , supp_weekly_hours  = 30.0
        , weekend_allowed    = 0
        , travel_full        = 1
        , vacation_month     = 1.0
        , hours_sat          = 0.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '2'
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2018-01-01')
        , absolute = 1
        , days     = 1.0
        )
    db.commit ()
# end def import_data_17

def import_data_18 (db, user, olo) :
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( hours_fri          = 8.0
        , hours_sun          = 0.0
        , additional_hours   = 40.0
        , hours_wed          = 8.0
        , vacation_yearly    = 30.0
        , all_in             = 0
        , valid_from         = date.Date ("2018-07-02.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 8.0
        , weekly_hours       = 40.0
        , hours_mon          = 8.0
        , hours_thu          = 8.0
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , supp_weekly_hours  = 40.0
        , valid_to           = date.Date ("2019-01-03.00:00:00")
        , weekend_allowed    = 0
        , travel_full        = 1
        , vacation_month     = 1.0
        , hours_sat          = 0.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '2'
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2018-01-01')
        , absolute = 1
        , days     = 0.0
        )
    db.commit ()
# end def import_data_18

def import_data_19 (db, user, olo) :
    sd = dict (months = 0.0, required_overtime = 0, weekly = 1)
    otp = db.overtime_period.filter (None, sd)
    assert len (otp) == 1
    otp = otp [0]
    db.user_dynamic.create \
        ( hours_fri          = 8.0
        , hours_sun          = 0.0
        , additional_hours   = 40.0
        , hours_wed          = 8.0
        , vacation_yearly    = 30.0
        , all_in             = 0
        , valid_from         = date.Date ("2018-05-02.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 8.0
        , weekly_hours       = 40.0
        , hours_mon          = 8.0
        , hours_thu          = 8.0
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , supp_weekly_hours  = 40.0
        , valid_to           = date.Date ("2018-06-01.00:00:00")
        , weekend_allowed    = 0
        , travel_full        = 1
        , vacation_month     = 1.0
        , hours_sat          = 0.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '2'
        )
    otp = None
    db.user_dynamic.create \
        ( hours_fri          = 8.0
        , hours_sun          = 0.0
        , additional_hours   = 40.0
        , hours_wed          = 8.0
        , vacation_yearly    = 30.0
        , all_in             = 0
        , valid_from         = date.Date ("2018-06-01.00:00:00")
        , durations_allowed  = 0
        , hours_tue          = 8.0
        , weekly_hours       = 40.0
        , hours_mon          = 8.0
        , hours_thu          = 8.0
        , vacation_day       = 1.0
        , booking_allowed    = 1
        , supp_weekly_hours  = 40.0
        , weekend_allowed    = 0
        , travel_full        = 1
        , vacation_month     = 1.0
        , hours_sat          = 0.0
        , org_location       = olo
        , overtime_period    = otp
        , user               = user
        , vac_aliq           = '2'
        )
    vcorr = db.vacation_correction.create \
        ( user     = user
        , date     = date.Date ('2018-01-01')
        , absolute = 1
        , days     = 0.0
        )
    db.commit ()
# end def import_data_19
