#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
import ldap

from optparse    import OptionParser
from getpass     import getpass
from ldap.cidict import cidict
from roundup     import instance

class LDAP_Search_Result (object) :
    """ Wraps an LDAP search result.
        Noteworthy detail: We use an ldap.cidict for keeping the
        attributes, this is a case-insensitive dictionary variant.
    """
    def __init__ (self, vals) :
        assert (vals [0])
        self.dn    = vals [0]
        self.attrs = cidict (vals [1])
    # end def __init__

    def __getattr__ (self, name) :
        """ Delegate to our attrs dict """
        if not name.startswith ('__') :
            result = getattr (self.attrs, name)
            setattr (self, name, result)
            return result
        raise AttributeError, name
    # end def __getattr__

    def __getitem__ (self, name) :
        return self.attrs [name]
    # end def __getitem__
# end class LDAP_Search_Result

# map roundup attributes to ldap attributes
attribute_map = \
    { 'user' : \
        { 'realname'  : ('cn',        None)
        , 'lastname'  : ('sn',        None)
        , 'firstname' : ('givenname', None)
        , 'nickname'  : ('initials',  lambda x : x.lower() )
        }
    , 'user_contact' : {}
    }

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
        , default = 'ldap://localhost:389'
        )
    parser.add_option \
        ( "-w", "--bind-password"
        , help    = "LDAP bind password, will be asked for if not given"
        , default = ''
        )
    parser.add_option \
        ( "-W", "--ask-bind-password"
        , help    = "Ask for bind password"
        , action  = 'store_true'
        , default = False
        )
    opt, args = parser.parse_args ()
    if len (args) :
        parser.error ('No arguments please')
        exit (23)

    path    = opt.database_directory
    tracker = instance.open (path)
    db      = tracker.open ('admin')

    ldcon   = ldap.initialize(opt.ldap_uri)
    pw      = opt.bind_password
    if not pw and opt.ask_bind_password :
        pw = getpass (prompt = 'LDAP Password: ')
    # try getting a secure connection, may want to force this later
    try :
        ldcon.start_tls_s ()
    except ldap.LDAPError, cause :
        pass
    try :
        ldcon.simple_bind_s (opt.bind_dn, pw or '')
    except ldap.LDAPError, cause :
        print >> sys.stderr, "LDAP bind failed: %s" % cause.args [0]['desc']
        exit (42)

    valid = db.user_status.lookup ('valid')
    for uid in db.user.filter_iter(None, {}, sort=[('+','username')]) :
        user = db.user.getnode (uid)
        if user.status != valid :
            continue
        result = ldcon.search_s \
            ( opt.base_dn
            , ldap.SCOPE_SUBTREE
            , '(uid=%s)' % user.username
            , None
            )
        res = []
        for r in result :
            if r [0] :
                res.append (LDAP_Search_Result (r))
        assert (len (res) <= 1)

        if not res :
            print "Not found:", user.username
            continue
        res = res [0]
        for rk, (lk, method) in attribute_map ['user'].iteritems () :
            if len (res [lk]) != 1 :
                print "%s: invalid length: %s" % (user.username, lk)
            ldattr = res [lk][0]
            if method :
                ldattr = method (ldattr)
            if ldattr != user [rk] :
                print "%s: non-matching attribute: %s/%s %s/%s" % \
                    (user.username, rk, lk, user [rk], ldattr)

        #print "User: %s: %s" % (user.username, res.dn)
        #print "content:", res.attrs

if __name__ == '__main__' :
    main ()
