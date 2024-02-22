#! /usr/bin/python
# Copyright (C) 2023-24 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
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
#
#++
# Name
#    o_permission
#
# Purpose
#    Routines for handling permissions bound to org/location
#

from roundup.date       import Date
from roundup.exceptions import Reject
import user_dynamic
import common

def get_allowed_olo (db, uid):
    """ Return a set of allowed org location ids for that user """
    assert 'org_location' in db.o_permission.properties
    ids = db.o_permission.filter (None, dict (user = uid))
    assert len (ids) <= 1
    if ids:
        operm = db.o_permission.getnode (ids [0])
        return set (operm.org_location)
    elif 'user_dynamic' in db.classes:
        now = Date ('.')
        dyn = user_dynamic.get_user_dynamic (db, uid, now)
        if dyn and dyn.org_location:
            return {dyn.org_location}
    return set ()
# end def get_allowed_olo

def get_allowed_org (db, uid):
    ids = db.o_permission.filter (None, dict (user = uid))
    assert len (ids) <= 1
    if 'org_location' in db.o_permission.properties:
        olo = get_allowed_olo (db, uid)
        org = set (db.org_location.get (ol, 'organisation') for ol in olo)
        return org
    operm = db.o_permission.getnode (ids [0])
    return set (operm.organisation)
# end def get_allowed_org

def organisation_allowed (db, userid, itemid, classname):
    """ User may view item because organisation is allowed
    """
    cls  = db.classes [classname]
    item = cls.getnode (itemid)
    orgs = get_allowed_org (db, userid)
    # Allow items where organisation is not set
    if not item.organisation:
        return True
    return item.organisation in orgs
# end def organisation_allowed

def sap_cc_allowed_by_org (db, userid, itemid):
    """ User may access sap cost center because organisation is allowed
    """
    return organisation_allowed (db, userid, itemid, 'sap_cc')
# end def sap_cc_allowed_by_org

def time_project_allowed_by_org (db, userid, itemid):
    """ User may access time category because organisation is allowed
    """
    return organisation_allowed (db, userid, itemid, 'time_project')
# end def time_project_allowed_by_org

def time_wp_allowed_by_org (db, userid, itemid):
    """ User may access work package because organisation is allowed
    """
    wp = db.time_wp.getnode (itemid)
    return time_project_allowed_by_org (db, userid, wp.project)
# end def time_wp_allowed_by_org

def time_wp_group_allowed_by_org (db, userid, itemid):
    """ User may access time_wp_group because organisation of time
        category is allowed
    """
    wpg = db.time_wp_group.getnode (itemid)
    for wp in wpg.wps:
        if time_wp_allowed_by_org (db, userid, wp):
            return True
    return False
# end def time_wp_group_allowed_by_org

def auto_wp_allowed_by_olo (db, userid, itemid):
    """ User may access automatic work package if Organisation/Location
        is allowed
    """
    olo = get_allowed_olo (db, userid)
    awp = db.auto_wp.getnode (itemid)
    if awp.org_location in olo:
        return True
    return False
# end def auto_wp_allowed_by_olo

def dynamic_user_allowed_by_olo (db, userid, itemid):
    """ User may access dynamic user record because the org_location is
        allowed
    """
    olo = get_allowed_olo (db, userid)
    dyn = db.user_dynamic.getnode (itemid)
    return dyn.org_location in olo or olo.intersection (dyn.aux_org_locations)
# end def dynamic_user_allowed_by_olo

def user_allowed_by_olo (db, userid, itemuid, date = None):
    """ User may access item because item->user_dynamic->org_location is
        allowed
    """
    if date is None:
        date = Date ('.')
    dyn  = user_dynamic.get_user_dynamic (db, itemuid, date)
    if not dyn:
        return False
    return dynamic_user_allowed_by_olo (db, userid, dyn.id)
# end def user_allowed_by_olo

def daily_record_allowed_by_olo (db, userid, itemid):
    """ User may access item because org_location in dynamic user is
        allowed
    """
    dr = db.daily_record.getnode (itemid)
    return user_allowed_by_olo (db, userid, dr.user, dr.date)
# end def daily_record_allowed_by_olo

def dr_freeze_allowed_by_olo (db, userid, itemid):
    """ User may access item because org_location in dynamic user is
        allowed
    """
    dr = db.daily_record_freeze.getnode (itemid)
    return user_allowed_by_olo (db, userid, dr.user, dr.date)
# end def dr_freeze_allowed_by_olo

def dr_item_allowed_by_olo (db, userid, itemid, classname):
    """ Allow access to something that has a daily_record
    """
    cls  = db.classes [classname]
    item = cls.getnode (itemid)
    return daily_record_allowed_by_olo (db, userid, item.daily_record)
# end def dr_item_allowed_by_olo

def tr_allowed_by_olo (db, userid, itemid):
    """ User may access time_record because org_location in dynamic user
        is allowed
    """
    return dr_item_allowed_by_olo (db, userid, itemid, 'time_record')
# end def tr_allowed_by_olo

def ar_allowed_by_olo (db, userid, itemid):
    """ User may access attendance_record because org_location in
        dynamic user is allowed
    """
    return dr_item_allowed_by_olo (db, userid, itemid, 'attendance_record')
# end def ar_allowed_by_olo

def overtime_corr_allowed_by_olo (db, userid, itemid):
    """ User may access item because org_location in dynamic user is
        allowed
    """
    oc = db.overtime_correction.getnode (itemid)
    return user_allowed_by_olo (db, userid, oc.user, oc.date)
# end def overtime_corr_allowed_by_olo

def vacation_corr_allowed_by_olo (db, userid, itemid):
    """ User may access item because org_location in dynamic user is
        allowed
    """
    vc = db.vacation_correction.getnode (itemid)
    return user_allowed_by_olo (db, userid, vc.user, vc.date)
# end def vacation_corr_allowed_by_olo

def leave_allowed_by_olo (db, userid, itemid):
    """ User may access item because org_location in dynamic user is
        allowed
    """
    ls = db.leave_submission.getnode (itemid)
    return user_allowed_by_olo (db, userid, ls.user)
# end def leave_allowed_by_olo

def check_valid_user (db, cl, nodeid, new_values, date = None):
    uid = db.getuid ()
    if uid == '1' or common.user_has_role (db, uid, 'Admin'):
        return
    assert not nodeid
    userid = new_values.get ('user')
    assert userid
    if date is None:
        date = Date ('.')
    dyn  = user_dynamic.get_user_dynamic (db, userid, date)
    # Allow creation of *first* dynamic user record or same as existing
    if cl == db.user_dynamic and dyn is None:
        dyn = user_dynamic.last_user_dynamic (db, userid)
        if dyn is None:
            return
    # Allow creation of vac correction *before* first dyn user
    if cl == db.vacation_correction and dyn is None:
        dyn = user_dynamic.last_user_dynamic (db, userid)
    # Allow creation of freeze record *after* last dyn user
    # Or in a gap between dyn users
    if cl == db.daily_record_freeze and dyn is None and date:
        dyn = user_dynamic.find_user_dynamic (db, userid, date, direction = '-')
    _    = db.i18n.gettext
    if not dyn or not dynamic_user_allowed_by_olo (db, userid, dyn.id):
        uname = dict (uname = db.user.get (userid, 'username'))
        raise Reject (_ ('User "%(uname)s" not allowed') % uname)
# end def check_valid_user

def check_valid_org (db, cl, nodeid, new_values):
    uid = db.getuid ()
    if uid == '1' or common.user_has_role (db, uid, 'Admin'):
        return
    org = new_values.get ('organisation')
    if org is None:
        return
    orgs = get_allowed_org (db, uid)
    _    = db.i18n.gettext
    if org not in orgs:
        orgname = dict (orgname = db.organisation.get (org, 'name'))
        raise Reject (_ ('Organisation "%(orgname)s not allowed') % orgname)
# end def check_valid_org

def check_valid_wp_member (db, cl, nodeid, new_values):
    """ Check that the changed wps of a time_wp_group are allowed
    """
    uid = db.getuid ()
    if uid == '1' or common.user_has_role (db, uid, 'Admin'):
        return
    if 'wps' not in new_values:
        return
    old = []
    if nodeid:
        old = set (cl.get (nodeid, 'wps'))
    new = set (new_values ['wps'])
    changed = (old - new).union (new - old)
    orgs = get_allowed_org (db, uid)
    _    = db.i18n.gettext
    for wpid in changed:
        wp = db.time_wp.getnode (wpid)
        tp = db.time_project.getnode (wp.project)
        if not tp.organisation or tp.organisation in orgs:
            continue
        raise Reject (_ ('Changing member time_wp%s not allowed') % wpid)
# end def check_valid_wp_member

def check_new_tr_or_ar_allowed (db, cl, nodeid, new_values):
    """ Creation is allowed if the dyn user record for the daily record
        has the correct org_location
    """
    uid = db.getuid ()
    if uid == '1' or common.user_has_role (db, uid, 'Admin'):
        return
    dr = db.daily_record.getnode (new_values ['daily_record'])
    if dr.user == uid:
        return
    _  = db.i18n.gettext
    if not daily_record_allowed_by_olo (db, uid, dr.id):
        classname = dict (classname = _ (cl.classname))
        raise Reject \
            (_ ('Creating %(classname)s not allowed for this user') % classname)
# end def check_new_tr_or_ar_allowed

def check_new_leave_submission_perm (db, cl, nodeid, new_values):
    uid = db.getuid ()
    if uid == '1' or common.user_has_role (db, uid, 'Admin'):
        return
    if new_values ['user'] == uid:
        return
    fd = new_values ['first_day']
    check_valid_user (db, cl, nodeid, new_values, date = fd)
# end def check_new_leave_submission_perm

def check_new_auto_wp_olo (db, cl, nodeid, new_values):
    uid = db.getuid ()
    if uid == '1' or common.user_has_role (db, uid, 'Admin'):
        return
    if new_values ['org_location'] in get_allowed_olo (db, uid):
        return
    d = dict (auto_wp = _ ('auto_wp'), olo = _ ('org_location'))
    raise Reject \
        ( _ ("You are not allowed to create %(auto_wp)s for this %(olo)s") % d)
# end def check_new_auto_wp_olo
