#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
import ldap

from optparse         import OptionParser
from getpass          import getpass
from ldap.cidict      import cidict
from roundup          import instance
from rsclib.autosuper import autosuper

class LDAP_Search_Result (cidict, autosuper) :
    """ Wraps an LDAP search result.
        Noteworthy detail: We use an ldap.cidict for keeping the
        attributes, this is a case-insensitive dictionary variant.
    """
    def __init__ (self, vals) :
        assert (vals [0])
        self.dn    = vals [0]
        self.__super.__init__ (vals [1])
    # end def __init__

# end class LDAP_Search_Result

# map roundup attributes to ldap attributes
attribute_map = \
    { 'user' :
        { 'realname'  : ('cn',        None)
        , 'lastname'  : ('sn',        None)
        , 'firstname' : ('givenname', None)
        , 'nickname'  : ('initials',  lambda x : x.lower() )
        }
    , 'user_contact' :
        { 'Email'          : ('mail',)
        , 'internal Phone' : ('pager',           'otherPager')
        , 'mobile Phone'   : ('mobile',          'otherMobile')
        , 'external Phone' : ('telephoneNumber', 'otherTelephone')
        , 'private Phone'  : ('homePhone',       'otherHomePhone')
        }
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
    contact_types = dict \
        ((id, db.uc_type.get (id, 'name'))
         for id in db.uc_type.list ()
        )
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
            print "User not found:", user.username
            continue
        res = res [0]
        if res.dn.split (',')[-4] == 'OU=obsolete' :
            print "Obsolete LDAP user: %s" % user.username
        for rk, (lk, method) in attribute_map ['user'].iteritems () :
            if len (res [lk]) != 1 :
                print "%s: invalid length: %s" % (user.username, lk)
            ldattr = res [lk][0]
            if method :
                ldattr = method (ldattr)
            if ldattr != user [rk] :
                print "%s: non-matching attribute: %s/%s %s/%s" % \
                    (user.username, rk, lk, user [rk], ldattr)

        contacts = {}
        for cid in db.user_contact.filter \
            ( None
            , dict (user = user.id)
            , sort = [('+', 'contact_type'), ('+', 'order')]
            ) :
            contact = db.user_contact.getnode (cid)
            n = contact_types [contact.contact_type]
            if n not in contacts :
                contacts [n] = []
            contacts [n].append (contact.contact)
        for ct, cs in contacts.iteritems () :
            ldn = attribute_map ['user_contact'][ct]
            if len (ldn) != 2 :
                assert (len (ldn) == 1)
                assert (ct == 'Email')
                p = ldn [0]
                s = None
            else :
                p, s = ldn
            if p not in res :
                print "%s: not found: %s (%s)" % (user.username, p, cs [0])
            elif len (res [p]) != 1 :
                print "%s: invalid length: %s" % (user.username, p)
            else :
                ldattr = res [p][0]
                if ldattr != cs [0] :
                    print "%s: non-matching attribute: %s/%s %s/%s" % \
                        (user.username, ct, p, cs [0], ldattr)
            if s :
                if s not in res :
                    print "%s: not found: %s" % (user.username, s)
                else :
                    if res [1] != cs [1:] :
                        print "%s: non-matching attribute: %s/%s %s/%s" % \
                            (user.username, ct, s, cs [1:], ldattr)


        # FIXME thumbnailPhoto
        if 0 and (1 or user.username == 'senn') :
            print "User: %s: %s" % (user.username, res.dn)
            print "content:", res

if __name__ == '__main__' :
    main ()
