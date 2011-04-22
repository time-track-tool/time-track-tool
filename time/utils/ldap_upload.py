#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
import ldap
from optparse import OptionParser
from getpass  import getpass
from roundup  import instance

def main () :
    parser  = OptionParser ()
    parser.add_option \
        ( "-b", "--base-dn"
        , help    = "Search base (DN to search from)"
        , default = "DC=ds1,DC=internal"
        )
    parser.add_option \
        ( "-D", "--bind-dn"
        , help    = "DN to bind to LDAP database"
        , default = "cn=Manager,dc=example,dc=com"
        )
    parser.add_option \
        ( "-d", "--database-directory"
        , dest    = "database_directory"
        , help    = "Directory of the roundup installation"
        , default = '.'
        )
    parser.add_option \
        ( "-H", "--ldap-uri"
        , help    = "URI of ldap server"
        , default = 'ldap://localhost:3890'
        )
    parser.add_option \
        ( "-w", "--bind-password"
        , help    = "LDAP bind password, will be asked for if not given"
        )
    opt, args = parser.parse_args ()
    if len (args) :
        parser.error ('No arguments please')
        exit (23)

    dir     = opt.database_directory
    tracker = instance.open (dir)
    db      = tracker.open ('admin')

    ldcon   = ldap.initialize(opt.ldap_uri)
    pw      = opt.bind_password
    if not pw :
        pw = getpass (prompt = 'LDAP Password: ')
    try :
        ldcon.simple_bind_s (opt.bind_dn, pw or '')
    except ldap.LDAPError, cause :
        print >> sys.stderr, "LDAP bind failed: %s" % cause.args['desc']
        exit (42)

    for uid in db.user.filter_iter(None, {}, sort=[('+','username')]) :
        user = db.user.getnode (uid)
        if user.username in ('admin', 'anonymous') :
            continue
        dn, attr = ldcon.search_s \
            ( opt.base_dn
            , ldap.SCOPE_SUBTREE
            , '(uid=%s)' % user.username
            , None
            )[0]
        if not dn :
            print "not found: %s" % user.username
        print "User: %s: %s" % (user.username, dn)

if __name__ == '__main__' :
    main ()
