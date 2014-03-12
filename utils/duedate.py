#!/usr/bin/python
# Copyright (C) 2009 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
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

import sys
from email.Utils  import formatdate
from smtplib      import SMTP, SMTPRecipientsRefused
from optparse     import OptionParser
from roundup      import instance, hyperdb
from roundup.date import Date

class ReportLine (object) :
    format = \
        ( "%(id)5s %(assignedto)-10.10s %(deadline)10s %(priority)-15.15s "
          "%(status)-12s\n      %(title)-70.70s"
        )
    def __init__ (self, node) :
        self.node = node
        self.cl   = node.cl
        self.db   = node.cl.db

    def __str__ (self) :
        return self.format % self

    def __getitem__ (self, name) :
        subhead = dict ((x,x) for x in self.db.issue.getprops ().iterkeys ())
        if self.node [name] is None :
            return ''
        try :
            classname = getattr (self.node.cl.getprops () [name], 'classname')
            cl = self.db.getclass (classname)
            return cl.get (self.node [name], cl.labelprop ())
        except AttributeError :
            pass
        if isinstance (self.node.cl.getprops () [name], hyperdb.Date) :
            return self.node [name].pretty ('%Y-%m-%d')
        return self.node [name]
# end class ReportLine

class UserReport (object) :
    def __init__ (self, report, email) :
        self.report       = report
        self.db           = report.db
        self.email        = email
        self.report_lines = []
        self.nosy_lines   = []
        self.all_lines    = []
        self.headings     = \
            [ "Issues you're responsible for:"
            , "Nosy Issues:"
            , "Other Issues you wanted to see:"
            ]

    def __str__ (self) :
        s = []
        subhead = dict ((x,x) for x in self.db.issue.getprops ().iterkeys ())
        for h, lines in \
            zip ( self.headings
                , (self.report_lines, self.nosy_lines, self.all_lines)
                ) :
            if lines :
                s.append (h)
                s.append (ReportLine.format % subhead)
                for l in lines :
                    s.append (str (l))
                s.append ("")
        return "\n".join (s)

    def mail (self, smtp, header) :
        content = str (self)
        if not content :
            return
        to    = "To: %s" % self.email
        date  = "Date: %s"   % formatdate (self.report.now.timestamp (), True)
        mime  = \
            [ 'Mime-Version: 1.0'
            , 'Content-Type: text/plain; charset=UTF-8'
            , 'Content-Transfer-Encoding: 8bit'
            ]
        smtp.sendmail \
            ( self.db.config.ADMIN_EMAIL
            , self.email
            , '\n'.join \
                ( header
                + [to, date, "X-" + date]
                + mime
                + ["\n", content]
                )
            )
# end class UserReport

class Report (object) :

    def __init__ \
        (self, db, date
        , send_mail = False
        , users     = []
        , mailall   = []
        , do_nosy   = False
        ) :
        self.db     = db
        self.date   = Date (date)
        self.output = self.print_results
        if send_mail :
            self.output = self.mail_results
        self.users = list (users)
        if self.users :
            self.users.extend (mailall)
        self.now = Date ('.')
        stati = dict ((db.status.get (i, 'name'), i)
                      for i in db.status.getnodeids ())
        for n in 'deferred', 'done-cbb', 'resolved' :
            del stati [n]
        self.user_reports = {}
        issues = db.issue.filter \
            ( None
            , dict 
                ( status = stati.values ()
                , deadline = ';%s' % self.date.pretty ('%Y-%m-%d.%H:%M:%S')
                )
            , sort = [('+', 'deadline'), ('+', 'priority')]
            )
        for i in issues :
            n = db.issue.getnode (i)

            if n.assignedto :
                u = self.add_user (db.user.get (n.assignedto, 'address'))
                if u :
                    u.report_lines.append (ReportLine (n))
            if do_nosy :
                for uid in n.nosy :
                    if uid != n.assignedto :
                        u = self.add_user (db.user.get (uid, 'address'))
                        if u :
                            u.nosy_lines.append (ReportLine (n))
            for m in mailall :
                u = self.add_user (m)
                if u :
                    u.all_lines.append (ReportLine (n))

    def add_user (self, email) :
        if self.users and email not in self.users :
            return None
        if email not in self.user_reports :
            self.user_reports [email] = UserReport (self, email)
        return self.user_reports [email]

    def print_results (self) :
        for email, report in self.user_reports.iteritems () :
            print "%s:\n" % email, str (report)

    def mail_results (self) :
        smtp = SMTP (self.db.config.MAIL_HOST)
        header = \
            [ "Subject: Summary of pending bug reports until %s"
            % self.date.pretty ('%Y-%m-%d')
            ]
        for report in self.user_reports.values () :
            try :
                report.mail (smtp, header)
            except SMTPRecipientsRefused, cause :
                print >> sys.stderr, cause
# end class Report

def main () :
    cmd = OptionParser ()
    cmd.add_option \
        ( "-d", "--date"
        , dest    = "date"
        , help    = "Specify cut-off date for due-date"
        , default = ".+1w"
        )
    cmd.add_option \
        ( "-m", "--mail"
        , dest    = "mails"
        , help    = "Add mail address to receive summary of all open issues"
        , default = []
        , action  = "append"
        )
    cmd.add_option \
        ( "-n", "--nosy"
        , dest    = "nosy"
        , help    = "Add nosy issues to report"
        , action  = "store_true"
        )
    cmd.add_option \
        ( "-s", "--send"
        , dest    = "send"
        , help    = "Send reports via email (default: print only)"
        , action  = "store_true"
        )
    cmd.add_option \
        ( "-t", "--tracker"
        , dest    = "tpath"
        , help    = "Path to tracker instance"
        , default = "."
        )
    cmd.add_option \
        ( "-u", "--user"
        , dest    = "users"
        , help    = "Send/print report only for specified users"
        , action  = "append"
        , default = []
        )
    (options, args) = cmd.parse_args ()
    tracker = instance.open (options.tpath)
    db = tracker.open ("admin")
    r = Report \
        ( db
        , date      = options.date
        , send_mail = options.send
        , users     = options.users
        , mailall   = options.mails
        , do_nosy   = options.nosy
        )
    r.output ()
    db.close ()

if __name__ == "__main__" :
    main ()
