#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-
from __future__ import print_function
import sys
import os
from time            import time
from email.utils     import formatdate, formataddr
from smtplib         import SMTP, SMTPRecipientsRefused
from email.mime.text import MIMEText
from argparse        import ArgumentParser
from roundup         import instance

class IT_Report (object):

    def __init__ (self, opt):
        self.opt = opt
        tracker  = instance.open (opt.dir)
        self.db  = tracker.open ('admin')

        stati    = ['new', 'open', 'feedback']
        stati    = [self.db.it_issue_status.lookup (x) for x in stati]
        issues   = self.db.it_issue.filter \
            ( None
            , dict (status=stati)
            , sort=[('+', 'status'), ('+', 'creation')]
            )
        self.issues   = [self.db.it_issue.getnode (i) for i in issues]
        self.status   = dict \
            ((k, self.db.it_issue_status.get (k, 'name')) for k in stati)
        self.messages = {}
        self.build_mails ()
    # end def __init__

    def build_mails (self):
        header = '   ID Status   Date       Title'
        format = '%5s %-8s %10s %-53.53s'
        fmt2   = ' ' * 14 + ' %-63.63s'
        for i in self.issues:
            pdate = i.creation.pretty ('%Y-%m-%d')
            key   = i.responsible
            if key not in self.messages:
                self.messages [key] = []
                self.messages [key].append (header)
                self.messages [key].append ('')
            self.messages [key].append \
                (format % (i.id, self.status [i.status], pdate, i.title))
            self.messages [key].append \
                (fmt2 % (self.db.config.TRACKER_WEB + i.cl.classname + i.id))
            self.messages [key].append ('')
        formatted_messages = {}
        for u in self.messages:
            formatted_messages [u] = '\n'.join (self.messages [u])
        self.messages = formatted_messages
    # end def build_mails

    def output (self, fp):
        for uid in sorted (self.messages):
            assert (uid)
            user = self.db.user.getnode (uid)
            print ("IT-Issues for %s:" % user.username, file = fp)
            print (self.messages [uid], file = fp)
            print ("", file = fp)
    # end def output

    def send_mails (self):
        srvr = self.db.config.MAIL_HOST
        if opt.send_via:
            srvr = opt.send_via
        smtp = SMTP (srvr)

        frm  = opt.mailfrom or self.db.config.ADMIN_EMAIL
        if '@' not in frm:
            frm = '@'.join ((frm, self.db.config.MAIL_DOMAIN))

        for uid in sorted (self.messages):
            assert (uid)
            m    = self.messages [uid]
            user = self.db.user.getnode (uid)
            addr = user.address
            msg  = MIMEText (m, 'plain', 'utf-8')
            msg ['Subject'] = "Status of IT-issues"
            msg ['To']      = addr
            msg ['Date']    = formatdate (time (), True)
            msg ['From']    = formataddr (('Do not reply', frm))
            try:
                smtp.sendmail (frm, addr, msg.as_string ())
            except SMTPRecipientsRefused as cause:
                print (cause, file = sys.stderr)

    # end def send_mails

# end def class IT_Report

cmd = ArgumentParser ()
cmd.add_argument \
    ('-d', '--tracker-directory'
    , dest    = "dir"
    , help    = "Directory of the tracker to check"
    , default = "."
    )
cmd.add_argument \
    ('-f', '--from'
    , dest    = "mailfrom"
    , help    = "Send mail with this from address "
                "(defaults to roundup admin email)"
    )
cmd.add_argument \
    ('-m', '--mail'
    , dest    = "mail"
    , help    = "Send individual reminder mails"
    , action  = "store_true"
    )
cmd.add_argument \
    ('-p', '--print'
    , dest    = "prnt"
    , help    = "Print messages on standard output"
    , action  = "store_true"
    )
cmd.add_argument \
    ('-s', '--send-email-via'
    , dest    = 'send_via'
    , help    = "Send as email via this server, defaults to roundup mail config"
    , default = None
    )
opt = cmd.parse_args ()

sys.path.insert (1, os.path.join (opt.dir, 'lib'))

from common import user_has_role

rpt = IT_Report (opt)
if opt.prnt:
    rpt.output (sys.stdout)
if opt.mail:
    rpt.send_mails ()
