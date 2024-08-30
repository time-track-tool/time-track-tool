#!/usr/bin/python3
import sys
import os
from roundup           import date
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

sys.path.insert (1, os.path.join (dir, 'lib'))
import common

obsolete = \
    { 'procurement', 'pr-view', 'procure-approval', 'measurement-approval'
    , 'board', 'finance', 'hr', 'hr-approval', 'it-approval', 'subcontract'
    , 'subcontract-org', 'training-approval', 'quality'
    }

changed = False
for uid in db.user.getnodeids (retired = False):
    u  = db.user.getnode (uid)
    rl = common.role_list (u.roles)
    if obsolete.intersection (rl):
        roles = ','.join (r for r in rl if r not in obsolete)
        db.user.set (uid, roles = roles)
        print ('Fixed roles for "%s"' % u.username)
        changed = True
if changed:
    db.commit ()

changed = False

view_users = \
    [ 3851, 451, 1724, 3693, 1431, 534, 264, 804, 725, 1737, 165, 704
    , 3666, 800, 4176, 3623, 4204, 452, 712, 156, 66, 192, 4075, 1397
    , 1850, 19, 908, 1860, 970, 638, 1411, 2043, 483, 4133, 3497, 2091
    , 3368, 990, 232, 1880, 3653, 2263, 2069, 632, 4178, 447, 2105, 487
    , 444, 127, 1789, 1634, 440, 108, 33, 200, 39, 4112, 760, 395, 569
    , 3974, 1960, 724, 1429, 3971, 4121, 3972, 4177, 751, 3772, 3897
    , 1959, 2540, 3489, 851, 2086
    ]
view_users = [str (x) for x in view_users]
vu = []
for uid in view_users:
    try:
        u = db.user.getnode (uid)
        n = u.username
        vu.append (uid)
    except IndexError:
        pass
view_users = vu

try:
    pr_view = db.pr_approval_order.lookup ('PR-View')
except KeyError:
    pr_view = db.pr_approval_order.create \
        ( role       = 'PR-View'
        , order      = 3.5
        , only_nosy  = False
        , is_board   = False
        , is_finance = False
        , is_quality = False
        , users      = view_users
        , want_no_messages = False
        )
    changed = True
if changed:
    db.commit ()

changed = False

# Move roles from pr_view_roles to pr_edit_roles if the latter is empty
# Set pr_view_roles to the new approval order
for id in db.purchase_type.getnodeids (retired = False):
    pt = db.purchase_type.getnode (id)
    if not pt.pr_edit_roles:
        view = [pr_view]
        if pt.pr_view_roles == ['5']:
            view = []
        db.purchase_type.set \
            (id, pr_edit_roles = pt.pr_view_roles, pr_view_roles = view)
        changed = True

if changed:
    db.commit ()

changed = False
orgs = \
    [ '19', '20', '21', '22', '27', '31', '32', '33', '34', '40'
    , '41', '42', '43', '44', '45', '48', '50', '51', '52', '53'
    , '55', '58', '59', '61', '62', '63', '64', '65', '66'
    ]
orgn = []
for oid in orgs:
    try:
        org = db.organisation.getnode (oid)
        n   = org.name
        orgn.append (oid)
    except IndexError:
        pass
orgs = orgn
users = \
    [ '55', '854', '110', '322', '2629', '4226', '330', '958', '720', '1822'
    , '878', '1109', '4219', '4108', '1960', '108', '1429', '990', '3974'
    , '632', '2091', '200', '3666', '908', '156', '165', '959', '4075'
    , '4176', '33', '19', '569', '1880', '1850', '3489', '2086', '440'
    , '451', '276', '1752', '487', '3972', '1789', '444'
    ]
nusers = []
for uid in users:
    try:
        u = db.user.getnode (uid)
        n = u.username
        nusers.append (uid)
    except IndexError:
        pass
users = nusers

for uid in users:
    puids = db.o_permission.filter (None, dict (user = uid))
    if puids:
        assert len (puids) == 1
    else:
        db.o_permission.create (user = uid, organisation = orgs)
        changed = True
if changed:
    db.commit ()
