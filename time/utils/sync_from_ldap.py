#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from optparse import OptionParser
from roundup  import instance

def main () :
    # most ldap info is now fetched from extensions/config.ini
    parser  = OptionParser ()
    parser.add_option \
        ( "-d", "--database-directory"
        , dest    = "database_directory"
        , help    = "Directory of the roundup installation"
        , default = '.'
        )
    parser.add_option \
        ( "-u", "--update"
        , help    = "Update the roundup with info from LDAP directory"
        , default = False
        , action  = 'store_true'
        )
    opt, args = parser.parse_args ()

    sys.path.insert (1, os.path.join (opt.database_directory, 'lib'))
    from ldap_sync import LDAP_Roundup_Sync
    tracker = instance.open (opt.database_directory)
    db      = tracker.open ('admin')

    lds = LDAP_Roundup_Sync (db)
    if args :
        for username in args :
            lds.sync_user_from_ldap (username, update = opt.update)
    else :
        lds.sync_all_users_from_ldap (update = opt.update)
# end def main

if __name__ == '__main__' :
    main ()
