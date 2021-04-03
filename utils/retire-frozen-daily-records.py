#!/usr/bin/python

__author__ = "Robert Klonner"

import argparse
import logging
import os
import sys

import roundup.instance
import roundup.date
dir = os.getcwd()
sys.path.insert(1, os.path.join(dir, 'lib'))
import common
import time

parser = argparse.ArgumentParser(description='Retire frozen daily records for AD-domain and date')
parser.add_argument('--ad_domain', type=str, required=True, help='AD-domain of user group')
parser.add_argument('--date', type=str, required=True, help='Date of daily record freeze (e.g. 2020-06-30)')
args = parser.parse_args()

start_time = time.time()
tracker = roundup.instance.open(dir)
db = tracker.open('admin')

# reset roundup logger
# otherwise logging to stdout for this script will not work
root = logging.getLogger()
map(root.removeHandler, root.handlers[:])
map(root.removeFilter, root.filters[:])
# define new logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__file__)
# set log level according to command line args


ad_domain = args.ad_domain
date = args.date
user_id_list = db.user.filter(None, dict(ad_domain=ad_domain))
logger.info("Found %s users", len(user_id_list))

for user_id in user_id_list:
    user_item = db.user.getnode(user_id)
    username = user_item.username
    daily_record_freeze_id_list = db.daily_record_freeze.filter(None, dict(user=user_id,date=date))
    if daily_record_freeze_id_list:
        for drf_id in daily_record_freeze_id_list:
            logger.info("Retire item daily_record_freeze%s for user '%s' ('%s').", drf_id, username, user_id)
            db.daily_record_freeze.retire(drf_id)
    else:
        logger.info("Skip user '%s' ('%s'). No daily_record_freeze entries.", username, user_id)
db.commit()

logger.info("Finished after %s seconds" % (time.time() - start_time))
