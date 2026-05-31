#!/usr/bin/python3
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

# Loop over dynamic user recs of german users and
# - check there are no gaps
# - check that if there are absolute vacation corrections the're on the
#   start day-of-month of the first dyn

sort  = [('+', 'user'), ('+', 'valid_from')]
drecs = db.user_dynamic.filter (None, dict (vac_aliq = '2'), sort = sort)

last_dyn = start = None
vc_seen = False
for drec in drecs:
    dyn = db.user_dynamic.getnode (drec)
    if not last_dyn or dyn.user != last_dyn.user:
        last_dyn = dyn
        start = dyn.valid_from
        vsrt  = ('+', 'date')
        vcs   = db.vacation_correction.filter \
            (None, dict (user = dyn.user, absolute = True), sort = vsrt)
        vcs   = [db.vacation_correction.getnode (i) for i in vcs]
        vc_seen = False
        for n, vc in enumerate (vcs):
            if vc.date <= start:
                vc_seen = True
            else:
                break
        else:
            n = len (vcs)
        vcs = vcs [n:]
        continue
    assert last_dyn.valid_to
    assert last_dyn.valid_to <= dyn.valid_from
    if dyn.valid_from > last_dyn.valid_to:
        last_vc_seen = vc_seen
        vc_seen = False
        for n, vc in enumerate (vcs):
            if last_dyn.valid_to <= vc.date <= dyn.valid_from:
                vc_seen = True
            else:
                break
        else:
            n = len (vcs)
        if not vc_seen: # and last_vc_seen:
            u = db.user.get (dyn.user, 'username')
            print \
                ( 'Gap w/o vac corr: user_dynamic%s user: %s vfrom: %s'
                % (dyn.id, u, dyn.valid_from)
                )
        vcs = vcs [n:]
    for n, vc in enumerate (vcs):
        if not dyn.valid_to or vc.date < dyn.valid_to:
            vc_seen = True
            if dyn.vac_aliq == '2':
                u = db.user.get (dyn.user, 'username')
                print \
                    ( 'Abs vacation_correction%s Germany: user: %s date: %s' 
                    % (vc.id, u, vc.date)
                    )
        else:
            break
    else:
        n = len (vcs)
    vcs = vcs [n:]
    last_dyn = dyn

