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
u_ctrl = ['108', '3974', '2091', '990', '1911', '805']
u_fin  = ['156', '908']
u_it   = ['440', '447', '1850', '2086', '3240', '3489']
u_lab  = ['780', '1077']
u_qua  = ['929', '2501']
u_trn  = ['760', '1860', '4093']
u_hr   = \
    [ '13', '19', '51', '344', '671', '908', '971', '1737', '1860', '2401'
    , '3368'
    ]
u_proc = \
    [ '11', '55', '104', '110', '142', '322', '330', '395', '444', '671'
    , '696', '720', '842', '854', '878', '958', '971', '1109', '1341', '1384'
    , '1822', '1860', '2014', '2126', '2404', '2622', '2629', '2787', '2847'
    , '2915', '3273', '3599', '4108', '4219', '4226'
    ]
users = u_ctrl + u_fin + u_it + u_lab + u_qua + u_trn + u_hr + u_proc
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

changed = False
operm_users = ('444', '110')
for uid in operm_users:
    if not common.user_has_role (db, uid, 'o-permission'):
        u = db.user.getnode (uid)
        r = common.role_list (u.roles)
        r.append ('o-permission')
        db.user.set (uid, roles = ','.join (r))
        changed = True
if changed:
    db.commit ()

changed = False
qid = db.pr_approval_order.lookup ('quality')
quality = db.pr_approval_order.getnode (qid)
if not quality.is_quality:
    db.pr_approval_order.set (qid, is_quality = True)
    changed = True
cid = db.pr_approval_config.filter (None, dict (role = qid))
assert len (cid) <= 1
if not cid:
    cfg = db.pr_approval_config.create \
        ( role           = qid
        , quality_amount = 1000
        , valid          = True
        , if_not_in_las  = False
        )
    changed = True
else:
    cid = cid [0]
    cfg = db.pr_approval_config.getnode (cid)
    assert cfg.quality_amount is not None
if changed:
    db.commit ()
