#!/usr/bin/python3
import sys
import os
import datetime
from argparse import ArgumentParser

from roundup  import instance

def main ():
    # most ldap info is now fetched from extensions/config.ini
    parser = ArgumentParser ()
    parser.add_argument \
        ( "users"
        , nargs   = "*"
        , help    = "Users to update, default: all"
        )
    parser.add_argument \
        ( "-2", "--two-way-sync"
        , help    = "Turn on two-way sync: By default we will only write "
                    "to LDAP if some user attribute change (and the -w "
                    "option is specified). With this option we will "
                    "alway write the current user setting to LDAP "
                    "*after* syncing from LDAP"
        , action  = 'store_true'
        )
    parser.add_argument \
        ( "-C", "--no-roundup-user-creation"
        , dest    = 'roundup_user_creation'
        , help    = "Do not create users in roundup"
        , action  = 'store_false'
        , default = True
        )
    parser.add_argument \
        ( "-d", "--database-directory"
        , dest    = "database_directory"
        , help    = "Directory of the roundup installation"
        , default = '.'
        )
    parser.add_argument \
        ( "-m", "--max-changes"
        , help    = "Maximum number of changed users in any direction"
        , default = 30
        , type    = int
        )
    parser.add_argument \
        ( "-R", "--roundup-wins"
        , help    = "If both directions of sync are specified, roundup wins"
        , action  = 'store_true'
        )
    parser.add_argument \
        ( "-u", "--update"
        , help    = "Update roundup with info from LDAP directory"
        , default = False
        , action  = 'store_true'
        )
    parser.add_argument \
        ( "-v", "--verbose"
        , help    = "Verbosity"
        , default = 0
        , action  = 'count'
        )
    parser.add_argument \
        ( "-w", "--write-to-ldap"
        , help    = "By default ldap dry-run is configured, this turns it off"
        , default = False
        , action  = 'store_true'
        )
    args = parser.parse_args ()
    if args.roundup_wins and not args.two_way_sync:
        print ("Option roundup-wins (-R) only valid with two way sync")
        sys.exit (23)

    sys.path.insert (1, os.path.join (args.database_directory, 'lib'))
    from ldap_sync import LDAP_Roundup_Sync
    tracker = instance.open (args.database_directory)
    db      = tracker.open ('admin')

    timestamp_start = datetime.datetime.now()
    users = 'all' if not args.users else ','.join(args.users)
    # If max_changes is 0 we do not set a limit
    max_changes = args.max_changes or None

    params = dict \
        ( verbose                   = args.verbose
        , dry_run_roundup           = not args.update
        , dry_run_ldap              = not args.write_to_ldap
        , rup_user_creation_allowed = args.roundup_user_creation
        , roundup_wins              = args.roundup_wins
        )
    lds = LDAP_Roundup_Sync (db, **params)
    if not args.two_way_sync:
        lds.log.info ("Update LDAP (two-way-sync) is deactivated")
    try:
        if args.users:
            lds.log.info ("Start to sync users '%s' from LDAP" % users)
            for username in args.users:
                lds.sync_user_from_ldap (username)
                if args.two_way_sync:
                    lds.sync_user_to_ldap (username)
        else:
            lds.log.info ("Start to sync all users from LDAP")
            lds.sync_all_users_from_ldap (max_changes = max_changes)
            if args.two_way_sync:
                lds.sync_all_users_to_ldap (max_changes = max_changes)
    except Exception:
        lds.log_exception ()

    timestamp_end = datetime.datetime.now()
    duration = (timestamp_end - timestamp_start)
    lds.log.info ("Summary_overall;Duration;%s" % duration)
# end def main

if __name__ == '__main__':
    main ()
