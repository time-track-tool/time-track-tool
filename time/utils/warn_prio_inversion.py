#!/usr/bin/python2.4
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup           import date
from roundup           import instance
from roundup.password  import Password, encodePassword
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

containers = dict ((x, db.issue.getnode (x)) for x in sys.argv [1:])

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
        for e in adrs.iterkeys () :
            if e not in emails :
                emails [e] = []
            emails [e].append (s)
for e, m in emails.iteritems () :
    print e
    for k in m :
        print k
    print
