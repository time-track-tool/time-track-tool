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
import user_dynamic

tracker = instance.open (dir)
db      = tracker.open ('admin')

# Date when changes will be effective
due_date = '2020-09-01'
dd       = date.Date (due_date)

# Dict of (org_location, contract_type) with list of TCs
# We need this for finding users and for adding end-date to WPs
tc_dict = {}

# set of wp which are not closed, used to warn only once
non_closed_wp = set ()

# Open CSV and process it
with open (sys.argv [1], 'r') as f :
    dr = DictReader (f, delimiter = ';')
    for rec in dr :
        if rec ['Import'].strip () != 'yes' :
            print ("Not importing: %s" % rec ['Name'])
            continue
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
        da = rec ['Durations allowed'].strip () == 'yes'
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
                print ("Setting durations_allowed for auto_wp%s" % ai.id)
                db.auto_wp.set (ai.id, durations_allowed = da)
            continue
        d = dict \
            ( name              = rec ['Name']
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
# Commit after creating Auto-WPs
db.commit()

# Now loop over all olo/ct -> tc combinations
for olo, ct in tc_dict :
    tcs = tc_dict [(olo, ct)]
    # Find all dynamic user records for this combination of olo and ct
    # Which are valid on due_date
    # Note that the contract type is '-1' for 'normal' users, so the
    # query will find dynamic user records with empty contract type for
    # those.
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
                , time_start = ';' + due_date + ',-'
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
        # Commit changes to old WPs
        db.commit()

        # Now add dyn user with do_auto_wp flag
        # If the dyn starts on due_date we modify the record in-place
        if dyn.valid_from == dd :
            # Only set flag if not already set
            if not dyn.do_auto_wp :
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
        # Commit new dyn. user record for each user
        db.commit()

# Loop over all obsolete users, find WPs where a user is the only one
# allowed booking and set these WPs to the end-date of the last dyn.
# user record for that user
obs = db.user_status.lookup ('obsolete')
for uid in db.user.filter (None, dict (status = obs)) :
    dyn  = user_dynamic.last_user_dynamic (db, uid)
    if not dyn :
        print ("Obsolete user%s has no dynamic user data" % uid)
    if dyn and dyn.valid_to is None :
        print ("Obsolete user%s has a valid dynamic user record!" % uid)
        continue
    vt   = date.Date ('2000-01-01')
    if dyn :
        vt = dyn.valid_to
    user = db.user.getnode (uid)
    snam = user.username.split ('@', 1) [0]
    # Find WPs where this user is on the bookers list and which has no
    # end-date set. Note that we do not attempt to set the end-date to
    # the correct valid_to of the dynamic user if there already is an
    # end-date -- this would change the end-date of some project WPs
    # too.
    wps = db.time_wp.filter (None, dict (bookers  = uid, time_end = '-'))
    for wpid in wps :
        wp = db.time_wp.getnode (wpid)
        if len (wp.bookers) > 1 :
            continue
        tc = db.time_project.getnode (wp.project)
        t  = 'Auto-closed because last admitted user is obsolete'
        d  = dict (time_end = vt, description = t)
        # Do not allow that wp.name is username, we need that
        # name for the auto-generated WPs, should one of these obsolete
        # users be resurrected this will make problems
        if wp.name == snam :
            d ['name'] = wp.name + ' obsolete'
        print \
            ( "Set time_wp%s (%s.%s): %s"
            % (wp.id, tc.name, wp.name, d)
            )
        db.time_wp.set (wp.id, **d)
    # Commit all WPs for this user
    db.commit()

# Get all Leave requests that are in state 'submitted', do nothing if
# the wp already is an auto-generated wp. Otherwise check if the leave
# overlaps with the due date, if yes issue warning. If no and the leave
# is completele *after* due date *and* we have exactly one auto-wp with
# the same tc we change the wp.
sub    = db.leave_status.lookup ('submitted')
opn    = db.leave_status.lookup ('open')
leaves = db.leave_submission.filter \
    (None, dict (last_day = due_date + ';', status = sub))
for lid in leaves :
    leave = db.leave_submission.getnode (lid)
    wp    = db.time_wp.getnode (leave.time_wp)
    tc    = db.time_project.getnode (wp.project)
    if wp.auto_wp :
        continue
    # Get auto-wp with same tc for this user
    wps = db.time_wp.filter \
        ( None, dict
            ( bookers    = leave.user
            , project    = wp.project
            , time_start = due_date
            )
        )
    assert len (wps) <= 1
    # User has no auto_wp, do nothing
    if not wps :
        continue
    autowp = db.time_wp.getnode (wps [0])
    assert autowp.auto_wp
    if leave.first_day < dd :
        print \
            ( "leave_submission%s for user%s starts before %s"
            % (lid, leave.user, due_date)
            )
        continue
    print \
        ( "Setting leave_submission%s for user%s to time_wp%s (%s.%s)"
        % (lid, leave.user, autowp.id, tc.name, autowp.name)
        )
    db.leave_submission.set (lid, status = opn)
    db.leave_submission.set (lid, time_wp = autowp.id, status = sub)

# Just to be safe; should already be committed at this point
db.commit()
