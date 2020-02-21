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
        , help    = "Turn on the config-item that tries to write to LDAP: "
                    "By default a reactor would write local changes back "
                    "to LDAP but this is disabled in this script. "
                    "This option turns on this config-item so "
                    "that the reactor does write to LDAP."
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
    print("%s: Start to sync users '%s' from LDAP" % (
        timestamp_start.strftime("%Y-%m-%d %H:%M:%S"), users))

    # This raises InvalidOptionError whenever no ldap sync is
    # configured at all. But the next InvalidOptionError would be
    # raised when instantiating LDAP_Roundup_Sync below anyway.
    # So we do not guard for this case (that LDAP sync is called
    # without a valid LDAP configuration)
    # Disbale sync to LDAP (disable user reactor) by default
    db.config.ext.LDAP_UPDATE_LDAP = 'no'
    if args.write_to_ldap :
        db.config.ext.LDAP_UPDATE_LDAP = 'yes'

    lds = LDAP_Roundup_Sync (db, verbose = args.verbose)
    if args.users :
        for username in args.users :
            lds.sync_user_from_ldap (username, update = args.update)
    else :
        lds.sync_all_users_from_ldap (update = args.update)

    timestamp_end = datetime.datetime.now()
    duration = (timestamp_end - timestamp_start)
    print("%s: User sync finished after %s" % (
        timestamp_end.strftime("%Y-%m-%d %H:%M:%S"), duration))
# end def main

if __name__ == '__main__' :
    main ()
