#!/usr/bin/python3

import sys
import re
from rsclib.stateparser import Parser
from datetime           import datetime
from roundup.date       import Date

""" Migrate existing user data for tests to new database structure with
    attendance records
"""

rc = re.compile

class TR_Lifter (Parser) :
    re_creat  = rc (r"db\.time_record\.create")
    re_dr     = rc (r"^\s+. daily_record\s+=\s+(.+)$")
    re_dur    = rc (r"^\s+. duration\s+=\s+(.+)$")
    re_wl     = rc (r"^\s+. work_location\s+=\s+(.+)$")
    re_ta     = rc (r"^\s+. time_activity\s+=\s+(.+)$")
    re_wp     = rc (r"^\s+. wp\s+=\s+(.+)$")
    re_strt   = rc (r"^\s+. start\s+=\s+(.+)$")
    re_end    = rc (r"^\s+. end\s+=\s+(.+)$")
    re_endrec = rc (r"^\s+[)]$")

    encoding = None
    
    matrix = \
        [ ["init",    re_creat,  "timerec", None]
        , ["init",    None,      "init",    "output"]
        , ["timerec", re_dr,     "timerec", None]
        , ["timerec", re_dur,    "timerec", "duration"]
        , ["timerec", re_wl,     "timerec", "workloc"]
        , ["timerec", re_ta,     "timerec", "timeact"]
        , ["timerec", re_wp,     "timerec", "wp"]
        , ["timerec", re_strt,   "timerec", "starttime"]
        , ["timerec", re_end,    "timerec", "endtime"]
        , ["timerec", re_endrec, "init",    "output_rec"]
        ]

    def __init__ (self, *args, **kw) :
        self.rec = {}
        self.__super.__init__ (*args, **kw)
    # end def __init__

    def output (self, state, new_state, match) :
        if self.line.startswith (' ' * 9) :
            print (self.line [1:])
        elif self.line.startswith (' ' * 5) and self.line [6] != ' ' :
            print (self.line [1:])
        else :
            print (self.line)
    # end def output

    def duration (self, state, new_state, match) :
        self.rec ['duration'] = match.group (1)
    # end def duration

    def starttime (self, state, new_state, match) :
        self.rec ['start'] = match.group (1)
    # end def starttime

    def endtime (self, state, new_state, match) :
        self.rec ['end'] = match.group (1)
    # end def endtime

    def timeact (self, state, new_state, match) :
        self.rec ['time_activity'] = match.group (1)
    # end def timeact

    def workloc (self, state, new_state, match) :
        self.rec ['work_location'] = match.group (1)
    # end def workloc

    def wp (self, state, new_state, match) :
        self.rec ['wp'] = match.group (1)
    # end def wp

    def has_attendance (self) :
        if 'work_location' in self.rec :
            return True
        for k in 'start', 'end' :
            if k not in self.rec :
                return False
        return True
    # end def has_attendance

    def compute_duration (self) :
        assert 'duration' not in self.rec
        start = eval (self.rec ['start'])
        end   = eval (self.rec ['end'])
        t = end
        if end == '24:00' :
            t = '00:00'
        dstart = Date (start, offset = 0)
        dend   = Date (t,     offset = 0)
        if end == '24:00' :
            dend += common.day
            dend.hours = dend.seconds = dend.minutes = 0
        assert dstart < dend
        assert (dstart.timestamp () % 900) == 0
        assert (dend.timestamp ()   % 900) == 0
        return (dend - dstart).as_seconds () / 3600.
    # end def compute_duration

    def output_rec (self, state, new_state, match) :
        print ("    tr = db.time_record.create \\")
        print ("        ( daily_record  = dr")
        if 'duration' not in self.rec :
            self.rec ['duration'] = self.compute_duration ()
        for k in 'duration', 'wp', 'time_activity' :
            format = '%s'
            if k in self.rec :
                if k == 'duration' and isinstance (self.rec [k], float) :
                    format = '%.2f'
                f = "        , %-13s = " + format
                print (f % (k, self.rec [k]))
        print ("        )")
        if self.has_attendance () :
            print ("    ar = db.attendance_record.create \\")
            print ("        ( daily_record  = dr")
            print ("        , time_record   = tr")
            for k in 'start', 'end', 'work_location' :
                if k in self.rec :
                    print ("        , %-13s = %s" % (k, self.rec [k]))
            print ("        )")
        self.rec = {}
    # end def output_rec

# end class TR_Lifter

trl = TR_Lifter ()
with open (sys.argv [1], 'r') as f :
    trl.parse (f)
