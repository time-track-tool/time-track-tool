#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from time        import time
from email.Utils import formatdate
from smtplib     import SMTP, SMTPRecipientsRefused
from optparse    import OptionParser
from roundup     import instance

cmd = OptionParser (usage = '%prog [options] container-issue, ...')
cmd.add_option \
    ('-s', '--send-email-via'
    , dest    = 'send_email'
    , help    = "Send as email via this server, don't report to standard output"
    , default = None
    )
cmd.add_option \
    ('-d', '--tracker-directory'
    , dest    = "dir"
    , help    = "Directory of the tracker to check"
    , default = "."
    )
opt, args = cmd.parse_args ()
if not len (args) :
    cmd.error ('Need at least one container issue number')

tracker = instance.open (opt.dir)
db      = tracker.open ('admin')

containers = dict ((x, db.issue.getnode (x)) for x in args)

emails = {} # (adr, what) to send to
stati  = [db.status.lookup (x) for x in 'open', 'testing']
closed = db.status.lookup ('closed')
issues = db.issue.filter (None, dict (status = stati))
for i in issues :
    issue = db.issue.getnode (i)
    # dependency check:
    if not issue.depends :
        continue
    # container check:
    parent = issue
    while parent :
        if parent.id in containers :
            co = containers [parent.id]
            uc = db.user.getnode (co.responsible)
            break
        if parent.part_of :
            parent = db.issue.getnode (parent.part_of)
        else :
            parent = None
    else : # not found -- don't report
        continue
    # now look at dependencies
    for d in issue.depends :
        dep = db.issue.getnode (d)
        if dep.status == closed :
            continue
        if dep.effective_prio >= issue.effective_prio :
            continue
        u1 = db.user.getnode (issue.responsible)
        u2 = db.user.getnode (dep.responsible)
        s = ( 'issue%s (prio=%s, owner=%s)\n'
              '    in container issue%s (owner=%s)\n'
              '    depends on issue%s (prio=%s, owner=%s)'
            % ( issue.id, issue.effective_prio, u1.username
              , co.id, uc.username
              , dep.id, dep.effective_prio, u2.username
              )
            )
        adrs = dict.fromkeys (x.address for x in (u1, u2, uc))
        for e in adrs :
            if e not in emails :
                emails [e] = []
            emails [e].append (s)

if opt.send_email :
    date = "Date: %s" % formatdate (time (), True)
    smtp = SMTP (opt.send_email)
    subj = "Subject: Priority inversion for issues"
    mime = '\n'.join \
        (( 'Mime-Version: 1.0'
         , 'Content-Type: text/plain; charset=UTF-8'
         , 'Content-Transfer-Encoding: 8bit'
        ))

for e in emails :
    m = emails [e]
    if opt.send_email :
        to  = "To: %s" % e
        frm = "From: %s" % db.config.ADMIN_EMAIL
        m   = '\n'.join (m)
        try :
            smtp.sendmail \
                ( db.config.ADMIN_EMAIL
                , e
                , '\n'.join ((subj, to, frm, date, "X-" + date, mime, '\n', m))
                )
        except SMTPRecipientsRefused, cause :
            print >> sys.stderr, cause
    else :
        print e
        for k in m :
            print k
        print
