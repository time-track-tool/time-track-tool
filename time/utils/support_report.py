#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from time        import time
from email.Utils import formatdate
from smtplib     import SMTP, SMTPRecipientsRefused
from optparse    import OptionParser
from roundup     import instance

cmd = OptionParser (usage = '%prog [options]')
cmd.add_option \
    ('-s', '--send-email-via'
    , dest    = 'send_email'
    , help    = "Send as email via this server, defaults to roundup mail config"
    , default = None
    )
cmd.add_option \
    ('-t', '--send-email-to'
    , dest    = 'mail_to'
    , help    = "Send as email to this destination"
    , default = None
    )
cmd.add_option \
    ('-d', '--tracker-directory'
    , dest    = "dir"
    , help    = "Directory of the tracker to check"
    , default = "."
    )
opt, args = cmd.parse_args ()
if len (args) :
    cmd.error ('No parameters expected')

sys.path.insert (1, os.path.join (opt.dir, 'lib'))

from common import user_has_role

tracker = instance.open (opt.dir)
db      = tracker.open ('admin')

stati   = [db.sup_status.lookup (x) for x in ('open', 'customer')]
sissues = db.support.filter \
    (None, dict (status=stati), sort=[('+', 'status'), ('+', 'creation')])
sowner  = db.user.lookup ('support')
valid   = db.user_status.lookup ('valid')
status  = dict ((k, db.sup_status.get (k, 'name')) for k in stati)

unassigned = []
todo       = []
for i in sissues :
    sissue = db.support.getnode (i)
    if sissue.responsible == sowner :
        unassigned.append (sissue)
    else :
        todo.append (sissue)

format = '%5s %-8s %s %-54s'
m = []
if unassigned :
    m.append ('Unassigned Support Issues:')
    m.append ('Issue Status   Date       Title')
    for i in unassigned :
        pdate = i.creation.pretty ('%Y-%m-%d')
        m.append (format % (i.id, status [i.status], pdate, i.title))
if todo :
    if m :
        m.append ('')
    m.append ('open/customer Support Issues:')
    m.append ('Issue Status   Date       Title')
    for i in todo :
        pdate = i.creation.pretty ('%Y-%m-%d')
        m.append (format % (i.id, status [i.status], pdate, i.title))
m = '\n'.join (m)


if opt.mail_to :
    srvr = db.config.MAIL_HOST
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

if opt.mail_to :
    to  = "To: %s" % opt.mail_to
    frm = "From: %s" % db.config.ADMIN_EMAIL
    try :
        smtp.sendmail \
            ( db.config.ADMIN_EMAIL
            , opt.mail_to
            , '\n'.join ((subj, to, frm, date, "X-" + date, mime, '\n', m))
            )
    except SMTPRecipientsRefused, cause :
        print >> sys.stderr, cause
else :
    print m
    print
