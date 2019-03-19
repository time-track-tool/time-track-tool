#!/usr/bin/python

import os
import sys
from argparse import ArgumentParser
from roundup  import instance

""" Get a leave_submission number and check the time-records for that
    leave submission. Add the leave submissions if necessary.
"""

def main () :
    cmd = ArgumentParser ()
    cmd.add_argument \
        ( 'leave_submission'
        , help = 'Leave submission number'
        )
    cmd.add_argument \
        ( '-d', '--directory'
        , help    = 'Tracker directory'
        , default = os.getcwd ()
        )
    cmd.add_argument \
        ( '-u', '--user'
        , help    = 'User to open DB as'
        , default = 'admin'
        )
    args = cmd.parse_args ()
    sys.path.insert (1, os.path.join (args.directory, 'lib'))
    import common
    import vacation
    tracker = instance.open (args.directory)
    db = tracker.open (args.user)
    ls = db.leave_submission.getnode (args.leave_submission)
    leave = db.daily_record_status.lookup ('leave')
    d  = dict ()
    d ['daily_record.user'] = ls.user
    d ['daily_record.date'] = common.pretty_range (ls.first_day, ls.last_day)
    d ['daily_record.status'] = leave
    trs = db.time_record.filter (None, d)
    if trs :
        print ("Found time records, exiting")
        return
    dy = ls.first_day
    off = db.work_location.lookup ('off')
    while dy <= ls.last_day :
        du = mindu = vacation.leave_duration (db, ls.user, dy)
        dt = common.pretty_range (dy, dy)
        dr = db.daily_record.filter (None, dict (user = ls.user, date = dt))
        wp = db.time_wp.getnode (ls.time_wp)
        tp = db.time_project.getnode (wp.project)
        if tp.max_hours is not None :
            mindu = min (du, tp.max_hours)
        assert len (dr) == 1
        if mindu :
            db.time_record.create \
                ( daily_record  = dr [0]
                , duration      = mindu
                , work_location = off
                , wp            = ls.time_wp
                )
        db.daily_record.set (dr [0], status = leave)
        dy += common.day
    db.commit ()
# end def main

if __name__ == '__main__' :
    main ()
