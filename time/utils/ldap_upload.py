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

def get_picture (user) :
    """ Get picture from roundup user class """
    p  = user.pictures[-1]
    return user.cl.db.file.get (p, 'content')
# end def get_picture

def get_department (user) :
    """ Get department name from roundup user class """
    return user.cl.db.department.get (user.department, 'name')
# end def get_department

def get_org_location (user) :
    """ Get org_location name from roundup user class """
    return user.cl.db.org_location.get (user.org_location, 'name')
# end def get_org_location

def get_position (user) :
    """ Get position name from roundup user class """
    return user.cl.db.position.get (user.position, 'position')
# end def get_room

def get_room (user) :
    """ Get room name from roundup user class """
    return user.cl.db.room.get (user.room, 'name')
# end def get_room

class LDAP_Converter (object) :
    
    forbidden = dict.fromkeys (('otherTelephone',))

    def __init__ (self, opt) :
        self.opt   = opt
        path       = opt.database_directory
        tracker    = instance.open (path)
        self.db    = tracker.open ('admin')

        self.ldcon = ldap.initialize(opt.ldap_uri)
        pw         = opt.bind_password
        if not pw and opt.ask_bind_password :
            pw = getpass (prompt = 'LDAP Password: ')
        # try getting a secure connection, may want to force this later
        try :
            self.ldcon.start_tls_s ()
        except ldap.LDAPError, cause :
            pass
        try :
            self.ldcon.simple_bind_s (opt.bind_dn, pw or '')
        except ldap.LDAPError, cause :
            print >> sys.stderr, "LDAP bind failed: %s" % cause.args [0]['desc']
            exit (42)
        self.compute_attr_map ()
    # end def __init__

    # map roundup attributes to ldap attributes
    def compute_attr_map (self) :
        attr_map = \
            { 'user' :
                { 'department'   : ( 'Department'
                                   , get_department
                                   , None
                                   )
                , 'firstname'    : ( 'givenname'
                                   , 0
                                   , None
                                   )
                , 'lastname'     : ( 'sn'
                                   , 0
                                   , None
                                   )
                , 'nickname'     : ( 'initials'
                                   , lambda x : x.nickname.upper ()
                                   , None
                                   )
                , 'org_location' : ( 'company'
                                   , get_org_location
                                   , None
                                   )
                , 'pictures'     : ( 'thumbnailPhoto'
                                   , get_picture
                                   , None
                                   )
                , 'position'     : ( 'title'
                                   , get_position
                                   , None
                                   )
                , 'realname'     : ( 'cn'
                                   , 0
                                   , None
                                   )
                , 'room'         : ( 'physicalDeliveryOfficeName'
                                   , get_room
                                   , None
                                   )
                , 'substitute'   : ( 'secretary'
                                   , self.get_substitute
                                   , None
                                   )
                , 'supervisor'   : ( 'manager'
                                   , self.get_supervisor
                                   , None
                                   )
                , 'title'        : ( 'carLicense'
                                   , 1
                                   , None
                                   )
                }
            , 'user_contact' :
                { 'Email'          : ('mail',)
                , 'internal Phone' : ('telephoneNumber', 'otherTelephone')
                , 'mobile Phone'   : ('mobile',          'otherMobile')
                , 'Mobile short'   : ('pager',           'otherPager')
        #       , 'external Phone' : ('telephoneNumber', 'otherTelephone')
        #       , 'private Phone'  : ('homePhone',       'otherHomePhone')
                }
            }
        self.attr_map = attr_map
    # end def compute_attr_map

    def get_username_attribute_dn (self, node, attribute) :
        """ Get dn of a user Link-attribute of a node """
        s = node [attribute]
        if not s :
            return s
        s = self.db.user.get (s, 'username')
        r = self.get_ldap_user (s)
        return r.dn
    # end def get_supervisor

    def get_supervisor (self, user) :
        return self.get_username_attribute_dn (user, 'supervisor')
    # end def get_supervisor

    def get_substitute (self, user) :
        return self.get_username_attribute_dn (user, 'substitute')
    # end def get_substitute

    def get_ldap_user (self, username) :
        result = self.ldcon.search_s \
            ( self.opt.base_dn
            , ldap.SCOPE_SUBTREE
            , '(uid=%s)' % username
            , None
            )
        res = []
        for r in result :
            if r [0] :
                res.append (LDAP_Search_Result (r))
        assert (len (res) <= 1)
        if res :
            return res [0]
        return None
    # end def get_ldap_user

    def convert (self) :
        valid = self.db.user_status.lookup ('valid')
        contact_types = dict \
            ((id, self.db.uc_type.get (id, 'name'))
             for id in self.db.uc_type.list ()
            )
        for uid in self.db.user.filter (None, {}, sort=[('+','username')]) :
            user = self.db.user.getnode (uid)
            if user.status != valid :
                continue
            res = self.get_ldap_user (user.username)
            print
            if not res :
                print "User not found:", user.username
                continue
            if res.dn.split (',')[-4] == 'OU=obsolete' :
                print "Obsolete LDAP user: %s" % user.username
                continue
            umap = self.attr_map ['user']
            modlist = []
            for rk, (lk, change, method) in umap.iteritems () :
                rupattr = user [rk]
                if callable (rupattr and change) :
                    rupattr = change (user)
                prupattr = rupattr
                if rk == 'pictures' :
                    prupattr = '<suppressed>'
                if lk not in res :
                    if user [rk] :
                        print "%s: Inserting: %s (%s)" \
                            % (user.username, lk, prupattr)
                        assert (change)
                        modlist.append ((ldap.MOD_ADD, lk, rupattr))
                elif len (res [lk]) != 1 :
                    print "%s: invalid length: %s" % (user.username, lk)
                else :
                    ldattr = pldattr = res [lk][0]
		    if rk == 'pictures' :
			pldattr = '<suppressed>'
                    if method :
                        ldattr = method (ldattr)
                    if ldattr != rupattr :
                        if not change :
                            print "%s:  attribute differs: %s/%s >%s/%s<" % \
                                (user.username, rk, lk, prupattr, pldattr)
                        else :
                            print "%s:  Updating: %s/%s >%s/%s<" % \
                                (user.username, rk, lk, prupattr, pldattr)
                            op = ldap.MOD_REPLACE
                            if rupattr is None :
                                op = ldap.MOD_DELETE
                            modlist.append ((op, lk, rupattr))
            contacts = {}
            for cid in self.db.user_contact.filter \
                ( None
                , dict (user = user.id)
                , sort = [('+', 'contact_type'), ('+', 'order')]
                ) :
                contact = self.db.user_contact.getnode (cid)
                n = contact_types [contact.contact_type]
                if n not in contacts :
                    contacts [n] = []
                contacts [n].append (contact.contact)
            for ct, cs in contacts.iteritems () :
                if ct not in self.attr_map ['user_contact'] :
                    continue
                ldn = self.attr_map ['user_contact'][ct]
                if len (ldn) != 2 :
                    assert (len (ldn) == 1)
                    assert (ct == 'Email')
                    p = ldn [0]
                    s = None
                else :
                    p, s = ldn
                if p not in res :
                    print "%s: Inserting: %s (%s)" % (user.username, p, cs [0])
                    modlist.append ((ldap.MOD_ADD, p, cs [0]))
                elif len (res [p]) != 1 :
                    print "%s: invalid length: %s" % (user.username, p)
                else :
                    ldattr = res [p][0]
                    if ldattr != cs [0] :
                        print "%s:  Updating: %s/%s %s/%s" % \
                            (user.username, ct, p, cs [0], ldattr)
                        modlist.append ((ldap.MOD_REPLACE, p, cs [0]))
                if s :
                    if s not in res :
                        if cs [1:] :
                            print "%s: Inserting: %s (%s)" \
                                % (user.username, s, cs [1:])
                            if s not in self.forbidden :
                                modlist.append ((ldap.MOD_ADD, s, cs [1:]))
                    else :
                        if res [1] != cs [1:] :
                            print "%s:  Updating: %s/%s %s/%s" % \
                                (user.username, ct, s, cs [1:], ldattr)
                            if s not in self.forbidden :
                                modlist.append ((ldap.MOD_REPLACE, s, cs [1:]))
            #print "Modlist:"
            #for k in modlist :
            #    print k
            if modlist and self.opt.update :
                self.ldcon.modify_s (res.dn, modlist)

            if 0 and (1 or user.username == 'senn') :
                print "User: %s: %s" % (user.username, res.dn)
                print "content:", res
    # end def convert

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
        ( "-u", "--update"
        , help    = "Update the LDAP directory with info from roundup"
        , default = False
        , action  = 'store_true'
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

    ldc = LDAP_Converter (opt)
    ldc.convert ()
# end def main


if __name__ == '__main__' :
    main ()
