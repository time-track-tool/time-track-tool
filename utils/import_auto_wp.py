#!/usr/bin/python
from __future__ import print_function
import sys
import os
from csv     import DictReader
from roundup import date
from roundup import instance
dir     = os.getcwd ()

sys.path.insert (1, os.path.join (dir, 'lib'))
import common

tracker = instance.open (dir)
db      = tracker.open ('admin')

# Date when changes will be effective
due_date = '2020-09-01'

# Dict of (org_location, contract_type) with list of TCs
# We need this for finding users and for adding end-date to WPs
tc_dict = {}

# set of wp which are not closed, used to warn only once
non_closed_wp = set ()

# Open CSV and process it
with open (sys.argv [1], 'r') as f :
    dr = DictReader (f, delimiter = ';')
    for rec in dr :
        #print (rec)
        oloid = rec ['Org.-Loc. Nummer'].strip ()
        try :
            x = int (oloid)
        except ValueError :
            print ("Not importing: Org-Loc ID: %s" % oloid)
            continue
        if rec ['is valid'].strip () != 'yes' :
            print ("Not marked valid: Org-Loc ID: %s, not importing" % oloid)
            continue
        olo   = db.org_location.getnode (oloid)
        if olo.name != rec ['Org-Location'] :
            print \
                ( "Org/Loc name not matching: Got %s expect %s"
                % (rec ['Org-Location'], olo.name)
                )
            continue
        tcid = rec ['Time Cat Nummer'].strip ()
        try :
            x = int (tcid)
        except ValueError :
            print ("Not importing: TC ID: %s" % tcid)
            continue
        tc   = db.time_project.getnode (tcid)
        if tc.name != rec ['Time Category Name'] :
            print \
                ( "Timecat name not matching: Got %s expect %s"
                % (rec ['Time Category Name'], tc.name)
                )
            continue
        ct = '-1'
        if rec ['Contract type'] != 'normal' :
            e  = dict (name = rec ['Contract type'])
            ct = db.contract_type.filter (None, {}, exact_match_spec = e)
            if len (ct) != 1 :
                print ("CT-match: %s" % rec ['Contract type'], ct)
            assert len (ct) == 1
            ct = ct [0]
        assert rec ['is valid'] == 'yes'
        if (olo.id, ct) not in tc_dict :
            tc_dict [(olo.id, ct)] = []
        if tc.id in tc_dict [(olo.id, ct)] :
            print \
                ( "Duplicate Timecat for org_location%s contract_type%s"
                % (olo.id, ct)
                )
        else :
            tc_dict [(olo.id, ct)].append (tc.id)
        da = False
        if rec ['Durations allowed'].strip () == 'yes' :
            da = True
        dur = rec ['Duration'].strip ().strip ('+')
        if not dur :
            dur = None
        da = rec ['Durations allowed'].strip == 'yes'
        # Get all Auto-WP with the given set of parameters
        d = dict \
            ( time_project  = tcid
            , org_location  = oloid
            , contract_type = ct
            )
        aids = db.auto_wp.filter (None, d)
        if aids :
            assert len (aids) == 1
            aid = aids [0]
            ai = db.auto_wp.getnode (aid)
            if ai.name != rec ['Name'] :
                print \
                    ( "Warning: name: %s not matching in DB: %s"
                    % (ai.name, rec ['Name'])
                    )
            if ai.duration != dur :
                print \
                    ( "Warning: duration: %s not matching in DB: %s"
                    % (ai.duration, dur)
                    )
            if ai.durations_allowed != da :
                print \
                    ( "Warning: durations allowed: %s not matching in DB: %s"
                    % (ai.durations_allowed, da)
                    )
            continue
        d = dict \
            ( name = rec ['Name']
            , time_project      = tcid
            , org_location      = oloid
            , duration          = dur
            , durations_allowed = da
            , all_in            = rec ['all-in'].strip () == 'yes'
            , is_valid          = True
            )
        if ct != '-1' :
            d ['contract_type'] = ct
        db.auto_wp.create (** d)
        print ("Created: %s" % str (d))
        sys.stdout.flush ()

# Now loop over all olo/ct -> tc combinations
for olo, ct in tc_dict :
    tcs = tc_dict [(olo, ct)]
    # Find all dynamic user records for this combination of olo and ct
    # Which are valid on due_date
    # Note that the contract type is '-1' for 'normal' users, so the
    # query will find dynamic user records with empty contract type for
    # those.
    dd = date.Date (due_date)
    e  = common.pretty_range (date.Date (due_date) + common.day) + ',-'
    d  = dict \
        ( org_location  = olo
        , contract_type = ct
        , valid_from    = ';' + due_date
        , valid_to      = e
        )
    du = db.user_dynamic.filter (None, d)
    for did in du :
        dyn  = db.user_dynamic.getnode (did)
        # Nothing to do if booking not allowed
        if not dyn.booking_allowed :
            continue
        user = db.user.getnode (dyn.user)
        snam = user.username.split ('@', 1) [0]

        # Find WP for each of the tc where the user may book on
        for tcid in tcs :
            tc = db.time_project.getnode (tcid)
            d  = dict \
                ( bookers    = dyn.user
                , project    = tcid
                , auto_wp    = '-1' # must be empty!
                , time_start = ';' + due_date
                , time_end   = e
                )
            wps = db.time_wp.filter (None, d)
            if len (wps) > 1 :
                print \
                    ( "Warning: User %s may book on more than one WP "
                      "for time_project%s (%s): %s"
                    % (dyn.user, tcid, tc.name, wps)
                    )
            for wpid in wps :
                wp = db.time_wp.getnode (wpid)
                assert wp.auto_wp is None
                if len (wp.bookers) > 1 :
                    if wp.id not in non_closed_wp :
                        non_closed_wp.add (wp.id)
                        print \
                            ( "Not closing time_wp%s (%s.%s)"
                            % (wp.id, tc.name, wp.name)
                            )
                    continue
                # Already set expiration date? (should not happen)
                d = {}
                if wp.time_end is None or wp.time_end > dd :
                    d = dict (time_end = dd)
                # Do not allow that wp.name is username, we need that
                # name for the auto-generated WPs
                if wp.name == snam :
                    d ['name'] = wp.name + ' obsolete'
                if d :
                    print \
                        ( "Set time_wp%s (%s.%s): %s"
                        % (wp.id, tc.name, wp.name, d)
                        )
                    db.time_wp.set (wp.id, **d)

        # Now add dyn user with do_auto_wp flag
        # If the dyn starts on due_date we modify the record in-place
        if dyn.valid_from == dd :
            print ("Setting user_dynamic%s do_auto_wp" % dyn.id)
            db.user_dynamic.set (dyn.id, do_auto_wp = True)
        else :
            vy = dyn.vacation_yearly
            if not vy :
                vy = db.org_location.get (dyn.org_location, 'vacation_yearly')
            if not vy :
                vy = 1
            d = dict \
                ( additional_hours      = dyn.additional_hours
                , all_in                = dyn.all_in
                , booking_allowed       = dyn.booking_allowed
                , daily_worktime        = dyn.daily_worktime
                , department            = dyn.department
                , do_auto_wp            = True
                , durations_allowed     = dyn.durations_allowed
                , exemption             = dyn.exemption
                , hours_mon             = dyn.hours_mon
                , hours_tue             = dyn.hours_tue
                , hours_wed             = dyn.hours_wed
                , hours_thu             = dyn.hours_thu
                , hours_fri             = dyn.hours_fri
                , hours_sat             = dyn.hours_sat
                , hours_sun             = dyn.hours_sun
                , max_flexitime         = dyn.max_flexitime or 0
                , org_location          = dyn.org_location
                , overtime_period       = dyn.overtime_period
                , sap_cc                = dyn.sap_cc
                , short_time_work_hours = dyn.short_time_work_hours
                , supp_per_period       = dyn.supp_per_period
                , supp_weekly_hours     = dyn.supp_weekly_hours
                , travel_full           = dyn.travel_full
                , user                  = dyn.user
                , vac_aliq              = dyn.vac_aliq
                , vacation_day          = dyn.vacation_day or 1
                , vacation_month        = dyn.vacation_month or 1
                , vacation_yearly       = vy
                , valid_from            = dd
                , valid_to              = dyn.valid_to
                , weekend_allowed       = dyn.weekend_allowed
                )
            if dyn.contract_type :
                d ['contract_type'] = dyn.contract_type
            print ("Creating dynamic user for user%s" % dyn.user)
            dynid = db.user_dynamic.create (**d)
            dyn = db.user_dynamic.getnode (dynid)
        sys.stdout.flush ()

db.commit()
