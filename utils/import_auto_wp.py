#!/usr/bin/python
from __future__ import print_function
import sys
import os
from csv     import DictReader
from roundup import date
from roundup import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

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
            , is_valid          = True
            )
        if ct != '-1' :
            d ['contract_type'] = ct
        db.auto_wp.create (** d)
        print ("Created: %s" % str (d))

db.commit()
