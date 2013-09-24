#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from __future__ import print_function
import sys
import os
from time        import time
from email.Utils import formatdate
from smtplib     import SMTP, SMTPRecipientsRefused
from optparse    import OptionParser
from roundup     import instance

class Support_Report (object) :

    def __init__ (self, opt) :
        self.opt = opt
        tracker  = instance.open (opt.dir)
        self.db  = tracker.open ('admin')

        stati    = [self.db.sup_status.lookup (x) for x in ('open', 'customer')]
        sissues  = self.db.support.filter \
            ( None
            , dict (status=stati)
            , sort=[('+', 'status'), ('+', 'creation')]
            )
        self.sowner  = self.db.user.lookup ('support')

        self.status  = dict \
            ((k, self.db.sup_status.get (k, 'name')) for k in stati)

        self.unassigned = []
        self.todo       = []
        for i in sissues :
            sissue = self.db.support.getnode (i)
            if sissue.responsible == self.sowner :
                self.unassigned.append (sissue)
            else :
                self.todo.append (sissue)
        cls = self.db.sup_classification.getnodeids (retired = False)
        cls = [self.db.sup_classification.getnode (i) for i in cls]
        self.classification     = dict ((x.id, x.name) for x in cls)
        self.classification [None] = '-'
        self.raw_messages       = {}
        self.formatted_messages = {}
        self.nonosy_customers   = {}
        self.build_mails ()
    # end def __init__

    def append_mails (self, sissue, heading, idx) :
        """ Append to all users which are concerned with the customer of
            this support issue.
        """
        if not sissue.customer :
            cstname = '-'
        else :
            customer = self.db.customer.getnode (sissue.customer)
            cstname  = customer.name
        self.append_msg ('', sissue, heading, idx, cstname)
        if not sissue.customer :
            return
        users = dict.fromkeys (customer.nosy or [])
        if customer.responsible :
            users [customer.responsible] = None
        if self.sowner in users :
            del users [self.sowner]
        for u in users.keys () :
            status = self.db.user.get (u, 'status')
            if not self.db.user_status.get (status, 'is_nosy') :
                del users [u]
        if not users :
            self.nonosy_customers [customer.id] = customer
        for u in users :
            self.append_msg (u, sissue, heading, idx, cstname)
    # end def append_mails

    def append_msg (self, key, sissue, heading, idx, cstname) :
        if key not in self.raw_messages :
            self.raw_messages [key] = [[], []]
        mm = self.raw_messages [key]
        if not mm [idx] :
            mm [idx].append (heading)
            mm [idx].append \
                ('Issue Status   Date       Responsible    Classification    '
                 'Serial Number\n      Customer\n      Title\n'
                 '      Related Issues\n'
                )
        mm [idx].append (self.pretty_issue (sissue, cstname))
    # end def append_msg

    def build_mails (self) :
        for i in self.unassigned :
            self.append_mails (i, 'Unassigned Support Issues:', 0)
        for i in self.todo :
            self.append_mails (i, 'Open/customer Support Issues:', 1)
        if self.nonosy_customers :
            self.raw_messages [''].append ([])
            nn = self.raw_messages [''][-1]
            nn.append ('Customers without valid responsible or nosy:')
            nn.append ('ID    Customer Name')
            for c in sorted \
                ( self.nonosy_customers.itervalues ()
                , key = lambda x : int (x.id)
                ) :
                nn.append ('%5s %-73s' % (c.id, c.name))
        for u, v in self.raw_messages.iteritems () :
            for idx in xrange (len (v) - 1) :
                if v [idx] and v [idx + 1] :
                    v [idx].append ('')
            parts = ['\n'.join (x) for x in v if x]
            parts.append ('')
            self.formatted_messages [u] = '\n'.join (parts)
    # end def build_mails

    def pretty_issue (self, sissue, cstname) :
        fmt   = \
            ( '%5s %-8s %10s %-14.14s %-17.17s %-20.20s'
              '\n      %-73.73s\n      %-73.73s%s\n'
            )
        pdate = sissue.creation.pretty ('%Y-%m-%d')
        user  = self.db.user.get (sissue.responsible, 'username')
        cls   = self.classification [sissue.classification]
        ser   = sissue.serial_number or ''
        ri    = ''
        if sissue.related_issues :
            ri = '\n      %s' % ', '.join (sissue.related_issues)
        i = sissue
        return fmt % \
            ( i.id, self.status [i.status], pdate, user, cls, ser
            , cstname, i.title, ri
            )
    # end def pretty_issue

    def output (self, fp) :
        for uid, m in sorted (self.formatted_messages.iteritems ()) :
            if uid :
                user = self.db.user.getnode (uid)
                print ("Support-Issues for %s:" % user.username, file = fp)
            else :
                print ("All Support-Issues:", file = fp)
            print (m, file = fp)
            print ("", file = fp)
    # end def output

    def send_mails (self) :
        srvr = self.db.config.MAIL_HOST
        if opt.send_email :
            srvr = opt.send_email
        date = "Date: %s" % formatdate (time (), True)
        smtp = SMTP (srvr)
        subj = "Subject: Status of Support issues"
        mime = '\n'.join \
            (( 'Mime-Version: 1.0'
             , 'Content-Type: text/plain; charset=UTF-8'
             , 'Content-Transfer-Encoding: 8bit'
            ))
        frm = "From: %s" % self.db.config.ADMIN_EMAIL

        for uid, m in sorted (self.formatted_messages.iteritems ()) :
            if uid :
                if not opt.mail :
                    continue
                user = self.db.user.getnode (uid)
                addr = user.address
            else :
                if not self.opt.mail_to :
                    continue
                addr = self.opt.mail_to
            to  = "To: %s" % addr
            try :
                mail = '\n'.join \
                    ((subj, to, frm, date, "X-" + date, mime, '\n', m))
                smtp.sendmail (self.db.config.ADMIN_EMAIL, addr, mail)
            except SMTPRecipientsRefused, cause :
                print (cause, file = sys.stderr)

    # end def send_mails

# end def class Support_Report

cmd = OptionParser (usage = '%prog [options]')
cmd.add_option \
    ('-d', '--tracker-directory'
    , dest    = "dir"
    , help    = "Directory of the tracker to check"
    , default = "."
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
    , dest    = 'send_email'
    , help    = "Send as email via this server, defaults to roundup mail config"
    , default = None
    )
cmd.add_option \
    ('-t', '--send-email-to'
    , dest    = 'mail_to'
    , help    = "Send summary email to this destination"
    , default = None
    )
opt, args = cmd.parse_args ()
if len (args) :
    cmd.error ('No parameters expected')
    sys.exit (23)

sys.path.insert (1, os.path.join (opt.dir, 'lib'))

from common import user_has_role

sr = Support_Report (opt)
if opt.prnt :
    sr.output (sys.stdout)
if opt.mail or opt.mail_to :
    sr.send_mails ()

