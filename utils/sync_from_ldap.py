#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
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
    args = parser.parse_args ()

    sys.path.insert (1, os.path.join (args.database_directory, 'lib'))
    from ldap_sync import LDAP_Roundup_Sync
    tracker = instance.open (args.database_directory)
    db      = tracker.open ('admin')

    lds = LDAP_Roundup_Sync (db, verbose = args.verbose)
    if args.users :
        for username in args.users :
            lds.sync_user_from_ldap (username, update = args.update)
    else :
        lds.sync_all_users_from_ldap (update = args.update)
# end def main

if __name__ == '__main__' :
    main ()
