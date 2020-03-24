import argparse
import datetime
import getpass
import logging
import requests
import sys


cmd = argparse.ArgumentParser()
cmd.add_argument('--url', help="URL to the Time Tracker (e.g. https://service.domain.com/)", required=True)

logging.basicConfig(level=logging.INFO, filename='errors.csv', format='%(message)s')
logger = logging.getLogger(__name__)


def check_dynamic_user_records_for_user(user_id, durs_list):
    """Loop through users and perfom checks on dynamic user records"""
    is_first_item = True
    is_last_item = False
    num_items = len(durs_list)

    num_valid_to_none = 0

    for i, dur_item in enumerate(durs_list):
        if i > 0:
            is_first_item = False
        if i+1 == num_items:
            is_last_item = True

        user_id = dur_item['user.id']
        dur_id = dur_item['id']
        valid_from = dur_item['valid_from']
        valid_to = dur_item['valid_to']

        if not valid_from:
            logger.error("Empty valid_from,%suser_dynamic%s", log_url, dur_id)
        if not valid_to and not is_last_item:
            logger.error("Empty valid_to for non-last dur,%suser_dynamic%s", log_url, dur_id)
        if not valid_to:
            num_valid_to_none += 1
        if not is_first_item:
            if valid_from and durs_list[i-1]['valid_to']:
                if valid_from < durs_list[i-1]['valid_to']:
                    logger.error("Overlapping durs,%suser_dynamic%s", log_url, dur_id)
    if num_valid_to_none > 1:
        logger.error("Multiple valid_to durs,%suser%s", log_url, user_id)


if __name__ == "__main__":
    args = cmd.parse_args()

    username = input("Username: ")
    password = getpass.getpass(f"Password [{username}]:")
    base_url = args.url
    rest_url = base_url + "rest/data/"
    log_url = base_url

    session = requests.session()
    session.auth = (username, password)

    # All dynamic user records ordered by user id and valid_from
    query = f"{base_url}/rest/data/user_dynamic?@fields=user.id,valid_from,valid_to&@sort=user.id,valid_from"
    user_data = session.get(query)
    user_list = user_data.json()['data']['collection']

    # Group dynamic user records by user
    user_id_tmp = None
    user_dict = {}
    dyn_list = []
    for dyn_user_item in user_list:
        user_id = dyn_user_item['user.id']
        if user_id == user_id_tmp or not user_id_tmp:
            dyn_list.append(dyn_user_item)
            user_id_tmp = user_id
        else:
            user_dict[user_id_tmp] = dyn_list
            dyn_list = []
            dyn_list.append(dyn_user_item)
            user_id_tmp = user_id

    # Execute tests for dynamic user records on every user
    num_user = len(user_dict)
    i = 1
    for user_id, durs_list in user_dict.items():
        print(f"{i}/{num_user}")
        check_dynamic_user_records_for_user(user_id, durs_list)
        i += 1
