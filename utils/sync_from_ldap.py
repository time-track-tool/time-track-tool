#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
import datetime
from argparse import ArgumentParser

from roundup  import instance

def main () :
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
        ( "-d", "--database-directory"
        , dest    = "database_directory"
        , help    = "Directory of the roundup installation"
        , default = '.'
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
        , help    = "Do not turn off the config-item that tries to write "
                    "to LDAP: "
                    "If configured a reactor would write local changes back "
                    "to LDAP but this is disabled in this script. "
                    "This option leaves the default so "
                    "that the reactor does write to LDAP if configured "
                    "in the config-file."
        , default = False
        , action  = 'store_true'
        )
    args = parser.parse_args ()

    sys.path.insert (1, os.path.join (args.database_directory, 'lib'))
    from ldap_sync import LDAP_Roundup_Sync
    tracker = instance.open (args.database_directory)
    db      = tracker.open ('admin')

    timestamp_start = datetime.datetime.now()
    users = 'all' if not args.users else ','.join(args.users)

    # This raises InvalidOptionError whenever no ldap sync is
    # configured at all. But the next InvalidOptionError would be
    # raised when instantiating LDAP_Roundup_Sync below anyway.
    # So we do not guard for this case (that LDAP sync is called
    # without a valid LDAP configuration)
    # Disable sync to LDAP (disable user reactor) by default
    # Note that we leave the default in the config file if write_to_ldap
    # is False -- we never turn on the sync if it is not configured!
    if not args.write_to_ldap :
        db.config.ext.LDAP_UPDATE_LDAP = 'no'

    lds = LDAP_Roundup_Sync (db, verbose = args.verbose)
    lds.log.info ("Start to sync users '%s' from LDAP" % users)
    try :
        if args.users :
            for username in args.users :
                lds.sync_user_from_ldap (username, update = args.update)
                if args.two_way_sync :
                    lds.sync_user_to_ldap (username)
        else :
            lds.sync_all_users_from_ldap (update = args.update)
            if args.two_way_sync :
                lds.sync_all_users_to_ldap ()
    except Exception :
        lds.log_exception ()

    timestamp_end = datetime.datetime.now()
    duration = (timestamp_end - timestamp_start)
    lds.log.info ("User sync finished after %s" % duration)
# end def main

if __name__ == '__main__' :
    main ()
