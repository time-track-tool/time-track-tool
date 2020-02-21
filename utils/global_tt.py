#!/usr/bin/python

"""
Upgrade and configuration script for:
 - Change to usernames including domain
 - Providing roles for subsidiaries to sync users
"""

__author__ = "Ralf Schaltterbeck, Robert Klonner"

import logging
import os
import sys
import argparse

import roundup.instance
import roundup.date
dir     = os.getcwd ()
sys.path.insert (1, os.path.join (dir, 'lib'))
import common


parser = argparse.ArgumentParser(description='Upgrade script for domain user names')
parser.add_argument('--staging-instance', action='store_true',
    help='Acticate settings and configs that are for staging instances only')
parser.add_argument('--debug', action='store_true',
    help='Set logging level to DEBUG')
args = parser.parse_args()

tracker = roundup.instance.open (dir)
db      = tracker.open ('admin')

# reset roundup logger
# otherwise logging to stdout for this script will not work
root = logging.getLogger()
map(root.removeHandler, root.handlers[:])
map(root.removeFilter, root.filters[:])
# define new logger
logging.basicConfig(stream=sys.stdout,level=logging.INFO)
logger = logging.getLogger(__file__)
# set log level according to command line args
logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

if args.staging_instance:
    logger.info("Script is running in non-prodution mode (staging)")
else:
    logger.info("Script is running in production mode")

# add new users status 'valid-ad'
# this users status will be used for users that are synced from AD
# currently this status is reflected by 'valid' so replace it
# 'old' users status 'valid' will be used for users that are synced
# to Time Tracker from subsidiaries and are not linked to AD
try :
    v = db.user_status.lookup ('valid-ad')
    logger.info("Users status 'valid-ad' already created. Skip task.")
except KeyError :
    # Rename old 'valid' user-status
    v = db.user_status.lookup ('valid')
    logger.info("Rename user status 'valid' to 'valid-ad'")
    db.user_status.set (v, name = 'valid-ad', timetracking_allowed = True)
    logger.info("Create new user status 'valid'")
    v = db.user_status.create \
        ( name                 = 'valid'
        , is_nosy              = True
        , timetracking_allowed = True
        , description          = 'Valid user not synced to AD'
        , roles                = 'User,Nosy'
        )
    db.commit ()

# Setup domain permissions for TTTech internal users
# Create domain, all users that need this role will be set in next task
# that is about specific permissions and roles
domain = 'ds1.internal'
try :
    domain_permission = db.domain_permission.lookup (domain)
    logger.info("Domain permisson for '%s' already created. Skip task.", domain)
except KeyError :
    logger.info("Create domain permission for '%s'", domain)
    domain_permission = db.domain_permission.create \
        ( ad_domain     = domain
        , default_roles = 'user,nosy'
        , status        =  db.user_status.lookup ('valid-ad')
        )
    db.commit()

# Check if appropriate permission exist
# Loop over *all* valid* users and check roles:
# - Add 'Dom-User-Edit-GTT' to gtime-sync-users for currently supported
#   subsidiaries, gtime-sync-rtrk, gtime-sync-sg
# - Add 'Dom-User-Edit-HR' to users with 'HR' role (if not yet added)
# - Add 'Dom-User-Edit-Office' to users with 'Office' role
# case-insensitive substring match:
valid = [db.user_status.lookup (i)
         for i in ("valid", "valid-ad", "system", "system-ad")
        ]
all_users = db.user.filter (None, dict (status = valid))
logger.info("Check permissions of '%d' users", len(all_users))
for u in all_users:
    user = db.user.getnode (u)
    username = user.username
    roles = set (common.role_list (user.roles))
    domain_permission_node = db.domain_permission.filter (None, dict (ad_domain = domain)) [0]
    domain_permission = db.domain_permission.getnode (domain_permission_node)
    domain_permission_users = domain_permission.users
    logger.debug('Current user: %s', username)
    logger.debug('Current roles: %s', ','.join([str(r) for r in roles]))
    if username in ['gtime-sync-rtrk@ds1.internal', 'gtime-sync-sg@ds1.internal'] and 'dom-user-edit-gtt' not in roles :
        if args.staging_instance :
            logger.info("Add role 'dom-user-edit-gtt' to user '%s'", username)
            roles.add ('dom-user-edit-gtt')
        else :
            logger.info("Skip user '%s' due to non-production mode of script", username)
            continue
    # the dom-user roles restrict what you may edit, don't do this to it
    if 'it' not in roles :
        if 'hr' in roles :
            if 'dom-user-edit-hr' not in roles :
                logger.info("Add role 'dom-user-edit-hr' to user '%s'", username)
                roles.add ('dom-user-edit-hr')
            if u not in domain_permission.users :
                logger.info("Add user '%s' to domain_permisson '%s'", username, domain)
                domain_permission_users.append (u)
        if 'office' in roles :
            if 'dom-user-edit-office' not in roles:
                logger.info("Add role 'dom-user-edit-office' to user '%s'", username)
                roles.add ('dom-user-edit-office')
            if u not in domain_permission.users :
                logger.info("Add user '%s' to domain_permisson '%s'", username, domain)
                domain_permission_users.append (u)
        if 'facility' in roles :
            if 'dom-user-edit-facility' not in roles:
                logger.info("Add role 'dom-user-edit-facility' to user '%s'", username)
                roles.add ('dom-user-edit-facility')
            if u not in domain_permission.users :
                logger.info("Add user '%s' to domain_permisson '%s'", username, domain)
                domain_permission_users.append (u)
    if roles != set (common.role_list (user.roles)) :
        logger.info("Save changed roles '%s' for user '%s'", ','.join (sorted (roles)), username)
        db.user.set (u, roles = ','.join (sorted (roles)))
    if domain_permission.users != domain_permission_users :
        logger.info("Save changed domain permission '%s' users '%s:'", domain, ','.join (sorted (domain_permission_users)))
        db.domain_permission.set (domain_permission_node, users = domain_permission_users)
db.commit ()

logger.info("Loop over all active time_projects and set is_extern to False")
active_stati = db.time_project_status.filter (None, dict (active = True))
for tpid in db.time_project.filter (None, dict (status = active_stati)) :
    tp = db.time_project.getnode (tpid)
    if tp.cost_center is None :
        logger.info("'time_project%s': Skip because tp has no productivity (cost center)." % tpid)
        continue
    if tp.is_extern is None :
        logger.info("'time_project%s': Set is_extern to False" % tpid)
        db.time_project.set (tpid, is_extern = False)
db.commit ()

logger.info("Loop over all work packages and set is_extern to False")
for wpid in db.time_wp.getnodeids (retired = False) :
    wp = db.time_wp.getnode (wpid)
    tp = db.time_project.getnode (wp.project)
    # This must be set, should be for all active wps
    if not wp.time_wp_summary_no and tp.op_project :
        logger.info("'time_wp%s': Skip because wp has no summary work package" % wpid)
        continue
    if wp.is_extern is None :
        logger.info("'time_wp%s': Set is_extern to False" % wpid)
        db.time_wp.set (wpid, is_extern = False)
db.commit ()

if args.staging_instance :
    # Set user.reduced_activity_list for caban to 2019-12-19
    try :
        username = 'caban@ds1.internal'
        caban = db.user.lookup (username)
        logger.info("Set date for reduced_activity_list for user '%s'" % username)
        db.user.set (caban, reduced_activity_list = roundup.date.Date ('2019-12-19'))
        db.commit ()
    except KeyError : # No user caban
        logger.error("No user '%s'" % username)
        pass
