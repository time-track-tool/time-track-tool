#! /usr/bin/python2.4
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003-2007 TTTech Computertechnik AG. All rights reserved
# Schoenbrunnerstrasse 7, A--1040 Wien, Austria. office@tttech.com
# ****************************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    xml_for_pygantt
#
# Purpose
#    Queries the Roundup DB and creates XML output for pygantt.
#    Note:
#        1PW == 5PD
#        1PM == 20PD
#        unspecified effort means 1PD for "testing" and 5PD for others
#
# Revision Dates
#    18-Aug-2003 (AGO) Creation
#    20-Aug-2003 (AGO) Only consider non-closed issues, added `toplevel`,
#                      verbosity levels, effort computation corrected
#     1-Sep-2003 (AGO) Fixed dependencies to closed issues
#     4-Sep-2003 (AGO) Effort = 1 PD for issues with status = "testing"
#     5-Sep-2003 (AGO) Verbosity option fixed, top label changed
#     2-Oct-2003 (RSC) coding comment added.
#     3-Dec-2003 (AGO) use `effective_prio` instead of `priority`,
#                      only mention open issues for effort estimation,
#                      exclude closed and suspended issues,
#                      set duration of containers to 0
#    10-Dec-2003 (AGO) `priority` as element instead of attribute
#    11-Dec-2003 (AGO) Debug output removed, version to 0.3.0
#    23-Jan-2004 (AGO) Default for not estimated effort: 9 PD
#    23-Feb-2004 (AGO) Respect the "needs" relation between issues,
#                      reset default estimated effort to 5 PD
#    23-Mar-2007 (GKH) Redesign XML-output
#    ««revision-date»»···
#--

import os
import sys
import time
import re
from   getopt                  import getopt, GetoptError
from   roundup                 import instance, date
from   xml.sax.saxutils        import escape
from   elementtree.ElementTree import Element, SubElement, ElementTree

class Pygantt_XML :
    """Queries the Roundup DB and creates XML output for pygantt."""

    VERBOSE       = 0 # 0 ... no output to stderr at all
                      # 1 ... only warnings
                      # 2 ... arguments and basic steps
                      # 3 ... full tree info
                      # 4 ... everything
    VERSION       = "0.3.5"
    DEFAULT_USER  = "admin"
    DEFAULT_PATH  = "/roundup/tracker/ttt"
    DEFAULT_FILE  = "for_pygantt.xml"
    DEFAULT_ISSUE = "[5060]"

    def __init__ \
        ( self
        , user     = None
        , tpath    = None
        , oname    = None
        , toplevel = None
        , verbose  = None
        ) :

        if verbose is not None :
            self.VERBOSE = int (verbose)
        if self.VERBOSE > 1 :
            self.debug ("Pygantt_XML, Version",  self.VERSION)
        self.user     = user  or self.DEFAULT_USER
        self.tpath    = tpath or self.DEFAULT_PATH
        self.oname    = oname or self.DEFAULT_FILE
        self.toplevel = eval (toplevel or self.DEFAULT_ISSUE)
        self.now      = date.Date (".")
        if self.VERBOSE > 1 :
            self.debug ("Roundup user        = %s" % self.user)
            self.debug ("Path to tracker     = %s" % self.tpath)
            self.debug ("Name of output file = %s" % self.oname)
            self.debug ("Considering toplevel issues %s ..." % self.toplevel)
            self.debug ("Launching tracker ...")
        self.tracker  = instance.open (self.tpath)
        sys.path.insert (1, os.path.join (self.tpath, "lib"))
        import user_dynamic
        self.get_user_dynamic  = user_dynamic.get_user_dynamic
        self.last_user_dynamic = user_dynamic.last_user_dynamic
        self.weekly_hours      = user_dynamic.weekly_hours
        if self.VERBOSE > 1 :
            self.debug ( "Loading roundup data base ...")
        self.db       = self.tracker.open (self.user)
        self.s_closed = self.db.status.lookup ("closed")
        self.s_test   = self.db.status.lookup ("testing")
        self.s_susp   = self.db.status.lookup ("suspended")
    # end def __init__

    def debug (self, msg) :
        print >> sys.stderr, msg

    def __call__ (self) :
        self.processed = {}
        self.pending   = {}
        tree           = Element ("project", id = "SW-Tasks")
        SubElement (tree, "label").text = ("Task(s) %s." % self.toplevel)
        SubElement (tree, "import-resources", file = "workers.xml")

        if self.VERBOSE > 1 :
            self.debug ("Writing `part_of` tree ...")
        for issue_id in self.toplevel :
            if self.VERBOSE > 2 :
                self.debug \
                    ("Issue %d is top-level. Processing it now ..." % issue_id)
            issue = self.db.issue.getnode (issue_id)
            self.process_issue (issue, tree)

        if self.VERBOSE > 1 :
            self.debug ("\nWriting issues due to `depends_on` or `needs` ...")
        while self.pending :
            (issue_id, issue) = self.pending.popitem ()
            if issue_id not in self.processed :
                if self.VERBOSE > 2 :
                    self.debug ("Adding %s ... "  % issue_id)
                self.process_issue (issue, tree)
            else :
                if self.VERBOSE > 3 :
                    self.debug ("%s already included." % issue_id)

        file = open (self.oname, "w")
        ElementTree (tree).write (file, encoding = "utf-8")
        if self.VERBOSE > 1 :
            self.debug ("Done.")
    # end def __call__

    def collect_parts (self, issue, tree) :
        """First add all parts of `issue` to `processed`. Continue
           recursively by calling `process_issue`. Then analyze
           the dependencies and add them to `pending` if not already
           in `processed`.
        """

        for part_id in issue.composed_of :
            part = self.db.issue.getnode (part_id)
            if part.status in (self.s_closed, self.s_susp) :
                if self.VERBOSE > 3 :
                    self.debug \
                        ("Not adding %s, because it is closed or "
                         "suspended." % part_id
                        )
                continue
            if self.VERBOSE > 2 :
                self.debug ("Adding %s ... (part of)"  % part_id)
            self.process_issue (part, tree)

        for part_id in (issue.depends + issue.needs) :
            if part_id in self.processed :
                if self.VERBOSE > 3 :
                    self.debug ("%s already included." % part_id)
            elif part_id in self.pending :
                if self.VERBOSE > 3 :
                    self.debug ("%s already pending."  % part_id)
            else :
                part = self.db.issue.getnode (part_id)
                if part.status == self.s_closed :
                    if self.VERBOSE > 3 :
                        self.debug ("Not keeping closed %s in mind." % part_id)
                else :
                    if self.VERBOSE > 2 :
                        self.debug \
                            ("Keeping in mind %s ...  (dependable)" % part_id)
                    self.pending [part_id] = self.db.issue.getnode (part_id)
    # end def collect_parts

    def process_issue (self, issue, tree) :
        """Process an issue: Write the XML output, add the `issue`
           to `processed` and continue recursively calling `collect_parts`.
        """

        task = SubElement (tree, "task", id = ("%s" % issue.id))
        self.write_task (issue, task)
        self.processed [issue.id] = issue
        self.collect_parts (issue, task)
    # end def process_issue

    def reduce_date (self, date) :
        """ `date` is a `roundup.date.Date`. Returning: YYYY/MM/DD."""

        return ("%s" % date).split (".")[0] .replace ("-", "/")
    # end def reduce_date

    def write_task (self, issue, tree) :
        user = self.db.user.getnode (issue.responsible)
        SubElement (tree, "label").text = \
            ("%s" %
                ( escape (issue.title [:50])
                + ("","...")[len (issue.title) > 50]
                )
            )
        SubElement (tree, "priority").text = \
            ("%d" % (issue.effective_prio or issue.priority))

        ### XXX still not taking candidates into account
        username = 
        SubElement \
            ( tree
            , "use-resource"
            , idref = "%s" % (user.nickname or user.username)
            , type  = "worker"
            )
        if not issue.composed_of :
            effort = issue.numeric_effort or (5, 1)[issue.status == self.s_test]
            effort = int (effort + .5)
            SubElement (tree, "duration", unit = "days").text = ("%s" % effort)
        else : # fill containers with a dummy length of 0 days
            SubElement (tree, "duration", unit = "days").text = "0"

        for dep_id in issue.depends or [] :
            if self.db.issue.getnode (dep_id).status != self.s_closed :
                SubElement \
                    ( tree
                    , "constraint"
                    , type = "begin-after-end"
                    ).text = ("%s" % dep_id)
        for dep_id in issue.needs or [] :
            if self.db.issue.getnode (dep_id).status != self.s_closed :
                SubElement \
                    ( tree
                    , "constraint"
                    , type = "end-after-end"
                    ).text = ("%s" % dep_id)
        if issue.deadline :
            SubElement \
                ( tree
                , "constraint"
                , type = "end-before-date"
                ).text = ("%s" % self.reduce_date (issue.deadline))
        if issue.earliest_start :
            SubElement \
                ( tree
                , "constraint"
                , type = "begin-after-date"
                ).text = ("%s" % self.reduce_date (issue.earliest_start))
    # end def write_task

    def output_workers (self, file = sys.stdout) :
        week = []
        tree = Element ("resources-list", type = "worker")
        tt   = SubElement (tree, "timetable", id = "weekend")
        SubElement (tt, "dayoff", type = "weekday").text = "saturday"
        SubElement (tt, "dayoff", type = "weekday").text = "sunday"
        for day in ("monday", "tuesday", "wednesday", "thursday", "friday") :
            tt = SubElement (tree, "timetable", id = day)
            SubElement (tt, "dayoff", type = "weekday").text = day
            week.append (day)
        stati = [self.db.user_status.lookup (i)
                 for i in ("valid", "obsolete", "system")
                ]
        for uid in self.db.user.filter (None, dict (status = stati)) :
            dyn = self.get_user_dynamic (self.db, uid, self.now)
            if not dyn :
                dyn = self.last_user_dynamic (self.db, uid)
            user = self.db.user.getnode (uid)
            if not user.nickname and not user.realname :
                continue
            r    = SubElement \
                ( tree
                , "resource"
                , id       = (user.nickname or user.username).decode ("utf-8")
                , fullname = user.realname.decode ("utf-8")
                )
            SubElement (r, "use-timetable", idref = "weekend")
            wh = 38.5
            if dyn :
                wh = self.weekly_hours (dyn) or 38.5
            wh *= 4
            wh += 7.75 * 4 - 1
            wh = int (wh)
            wh = int (wh / (7.75 * 4))
            for i in range (wh, 5) :
                SubElement (r, "use-timetable", idref = week [i])
        ElementTree (tree).write (file, encoding = "utf-8")
    # end def output_workers

# end class Pygantt_XML

if __name__ == "__main__" :

    def usage () :
        usage_msg = ( "Usage: %s [-h|--help] [-v|--verbose v] [-t|--tracker t]"
                      "[-o|--output o] [-i|--issues i] [-w|--workers w]\n"
                    % sys.argv [0]
                    )
        sys.stderr.write (usage_msg)
        sys.exit ()
    # end def usage

    tpath    = None
    oname    = None
    woname   = None
    toplevel = None
    verbose  = None
    try:
        opts, args = getopt \
            ( sys.argv [1:]
            , "hv:t:o:w:i:"
            , ["help", "verbose=", "tracker=", "output=", "workers=" "issues="]
            )
    except GetoptError :
        usage ()
    if args:
        usage ()
    for o, a in opts :
        if o in ("-h", "--help") :
            usage ()
        if o in ("-v", "--verbose") :
            verbose = a
        if o in ("-t", "--tracker") :
            tpath = a
        if o in ("-o", "--output") :
            oname = a
        if o in ("-w", "--workers") :
            woname = a
        if o in ("-i", "--issues") :
            toplevel = a

    x = Pygantt_XML \
        ( tpath    = tpath
        , oname    = oname
        , toplevel = toplevel
        , verbose  = verbose
        )
    x ()
    if woname :
        out = open (woname, "w")
    else :
        out = sys.stdout
    x.output_workers (out)

### __END__ xml_for_pygantt


