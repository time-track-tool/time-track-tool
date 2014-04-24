#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from __future__ import print_function
import sys
import os
from time        import time
from email.Utils import formatdate
from smtplib     import SMTP, SMTPRecipientsRefused
from optparse    import OptionParser
from roundup     import instance, date

class WP_Report (object) :

    def __init__ (self, opt) :
        self.opt = opt
        tracker  = instance.open (opt.dir)
        self.db  = tracker.open ('admin')

        now = date.Date ('.')
        exp = now + date.Interval ('%s days' % opt.days)
        wps = self.db.time_wp.filter \
            ( None
            , dict (time_end = '.;%s' % exp.pretty ('%Y-%m-%d'))
            , sort=[('+', 'responsible')]
            )
        self.wps = [self.db.time_wp.getnode (i) for i in wps]
        self.messages = {}
        self.build_mails ()
    # end def __init__

    def build_mails (self) :
        header = \
            ( 'The following work packages expire during the next %s days\n\n'
              'Expire     Project/Work Package Title'
            % self.opt.days
            )
        format = '%10s %-67.67s\n           %-67.67s\n           %s'
        for i in self.wps :
            pdate = i.time_end.pretty ('%Y-%m-%d')
            key   = i.responsible
            prj   = self.db.time_project.get (i.project, 'name')
            url   = self.db.config.TRACKER_WEB + i.cl.classname + i.id
            if key not in self.messages :
                self.messages [key] = []
                self.messages [key].append (header)
            self.messages [key].append (format % (pdate, prj, i.name, url))
        formatted_messages = {}
        for u, v in self.messages.iteritems () :
            formatted_messages [u] = '\n'.join (v)
        self.messages = formatted_messages
    # end def build_mails

    def output (self, fp) :
        for uid, m in sorted (self.messages.iteritems ()) :
            assert (uid)
            user = self.db.user.getnode (uid)
            print ("Expiring Work Packages for %s:" % user.username, file = fp)
            print (m, file = fp)
            print ("", file = fp)
    # end def output

    def send_mails (self) :
        srvr = self.db.config.MAIL_HOST
        if opt.send_via :
            srvr = opt.send_via
        date = "Date: %s" % formatdate (time (), True)
        smtp = SMTP (srvr)
        subj = "Subject: Work Packages expire in the next %s days" \
            % self.opt.days
        mime = '\n'.join \
            (( 'Mime-Version: 1.0'
             , 'Content-Type: text/plain; charset=UTF-8'
             , 'Content-Transfer-Encoding: 8bit'
            ))
        frm = "From: %s" % self.db.config.ADMIN_EMAIL

        for uid, m in sorted (self.messages.iteritems ()) :
            assert (uid)
            user = self.db.user.getnode (uid)
            addr = user.address
            to   = "To: %s" % addr
            try :
                mail = '\n'.join \
                    ((subj, to, frm, date, "X-" + date, mime, '\n', m))
                smtp.sendmail (self.db.config.ADMIN_EMAIL, addr, mail)
            except SMTPRecipientsRefused, cause :
                print (cause, file = sys.stderr)

    # end def send_mails

# end def class WP_Report

cmd = OptionParser (usage = '%prog [options]')
cmd.add_option \
    ('-d', '--tracker-directory'
    , dest    = "dir"
    , help    = "Directory of the tracker to check"
    , default = "."
    )
cmd.add_option \
    ('-e', '--expire-days'
    , dest    = "days"
    , help    = "Time in days to warn in advance before WP expires"
    , type    = "int"
    , default = "5"
    )
cmd.add_option \
    ('-m', '--mail'
    , dest    = "mail"
    , help    = "Send individual reminder mails"
    , action  = "store_true"
    )
cmd.add_option \
    ('-p', '--print'
    , dest    = "prnt"
    , help    = "Print messages on standard output"
    , action  = "store_true"
    )
cmd.add_option \
    ('-s', '--send-email-via'
    , dest    = 'send_via'
    , help    = "Send as email via this server, defaults to roundup mail config"
    , default = None
    )
opt, args = cmd.parse_args ()
if len (args) :
    cmd.error ('No parameters expected')
    sys.exit (23)

sys.path.insert (1, os.path.join (opt.dir, 'lib'))

rpt = WP_Report (opt)
if opt.prnt :
    rpt.output (sys.stdout)
if opt.mail :
    rpt.send_mails ()

