#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import ldap

from ldap.cidict      import cidict
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

    @property
    def is_obsolete (self) :
        return self.dn.split (',')[-4] == 'OU=obsolete'
    # end def is_obsolete

    def __getattr__ (self, name) :
        if not name.startswith ('__') :
            try :
                result = self [name]
                setattr (self, name, result)
                return result
            except KeyError, cause :
                raise AttributeError, cause
        raise AttributeError, name
    # end def __getattr__

# end class LDAP_Search_Result

def get_picture (user) :
    """ Get picture from roundup user class """
    p  = user.pictures[-1]
    return user.cl.db.file.get (p, 'content')
# end def get_picture

def get_name (user, attr) :
    """ Get name from roundup user class Link attr """
    cl = user.cl.db.classes [attr]
    return cl.get (user [attr], 'name')
# end def get_department

def get_position (user, attr) :
    """ Get position name from roundup user class """
    assert (attr == 'position')
    return user.cl.db.position.get (user.position, 'position')
# end def get_position

class LDAP_Roundup_Sync (object) :
    """ Sync users from LDAP to Roundup """
    
    def __init__ (self, db) :
        self.db    = db
        self.cfg   = db.config.ext

        self.ldcon = ldap.initialize(self.cfg.LDAP_URI)
        # try getting a secure connection, may want to force this later
        try :
            pass
            #self.ldcon.start_tls_s ()
        except ldap.LDAPError, cause :
            pass
        try :
            self.ldcon.simple_bind_s \
                (self.cfg.LDAP_BIND_DN, self.cfg.LDAP_PASSWORD)
        except ldap.LDAPError, cause :
            print >> sys.stderr, "LDAP bind failed: %s" % cause.args [0]['desc']
            exit (42)
        self.status_valid    = self.db.user_status.lookup ('valid')
        self.status_obsolete = self.db.user_status.lookup ('obsolete')
        self.status_system   = self.db.user_status.lookup ('system')
        self.contact_types = dict \
            ((id, self.db.uc_type.get (id, 'name'))
             for id in self.db.uc_type.list ()
            )
        self.compute_attr_map ()
    # end def __init__

    # map roundup attributes to ldap attributes
    def compute_attr_map (self) :
        attr_map = \
            { 'user' :
                { 'department'   : ( 'department'
                                   , get_name
                                   , self.cls_lookup (self.db.department)
                                   )
                , 'firstname'    : ( 'givenname'
                                   , 0
                                   , lambda x, y : x.get (y, [None])[0]
                                   )
                , 'lastname'     : ( 'sn'
                                   , 0
                                   , lambda x, y : x.get (y, [None])[0]
                                   )
                , 'nickname'     : ( 'initials'
                                   , lambda x, y : x [y].upper ()
                                   , lambda x, y : x.get (y, [''])[0].lower ()
                                   )
                , 'org_location' : ( 'company'
                                   , get_name
                                   , self.cls_lookup (self.db.org_location)
                                   )
                , 'pictures'     : ( 'thumbnailPhoto'
                                   , get_picture
                                   , self.ldap_picture
                                   )
                , 'position'     : ( 'title'
                                   , get_position
                                   , self.cls_lookup (self.db.position)
                                   )
                , 'realname'     : ( 'cn'
                                   , 0
                                   , None
                                   )
                , 'room'         : ( 'physicalDeliveryOfficeName'
                                   , get_name
                                   , self.cls_lookup (self.db.room)
                                   )
                , 'substitute'   : ( 'secretary'
                                   , self.get_username_attribute_dn
                                   , self.get_roundup_uid_from_dn_attr
                                   )
                , 'supervisor'   : ( 'manager'
                                   , self.get_username_attribute_dn
                                   , self.get_roundup_uid_from_dn_attr
                                   )
                , 'title'        : ( 'carLicense'
                                   , 1
                                   , lambda x, y : x.get (y, [None])[0]
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

    def cls_lookup (self, cls) :
        """ Generate a lookup method (non-failing) for the given class.
            Needed for easy check if an LDAP attribute exists as a
            roundup class. We need the roundup class in a closure.
        """
        def look (luser, txt) :
            try :
                return cls.lookup (luser [txt][0])
            except KeyError :
                pass
            return None
        # end def look
        return look
    # end def cls_lookup

    def get_username_attribute_dn (self, node, attribute) :
        """ Get dn of a user Link-attribute of a node """
        s = node [attribute]
        if not s :
            return s
        s = self.db.user.get (s, 'username')
        r = self.get_ldap_user_by_username (s)
        return r.dn
    # end def get_username_attribute_dn

    def _get_ldap_user (self, result) :
        res = []
        for r in result :
            if r [0] :
                res.append (LDAP_Search_Result (r))
        assert (len (res) <= 1)
        if res :
            return res [0]
        return None
    # end def _get_ldap_user

    def get_ldap_user_by_username (self, username) :
        result = self.ldcon.search_s \
            ( self.cfg.LDAP_BASE_DN
            , ldap.SCOPE_SUBTREE
            , '(uid=%s)' % username
            , None
            )
        return self._get_ldap_user (result)
    # end def get_ldap_user_by_username

    def get_roundup_uid_from_dn_attr (self, luser, attr) :
        try :
            v = luser [attr][0]
        except KeyError :
            return None
        lsup = self.get_ldap_user_by_dn (v)
        if not lsup :
            return None
        try :
            return self.db.user.lookup (lsup ['uid'][0])
        except KeyError :
            pass
        return None
    # end def get_roundup_uid_from_dn_attr

    def get_ldap_user_by_dn (self, dn) :
        result = self.ldcon.search_s (dn, ldap.SCOPE_BASE)
        return self._get_ldap_user (result)
    # end def get_ldap_user_by_dn

    def ldap_picture (self, luser, attr) :
        try :
            lpic = luser [attr][0]
        except KeyError :
            return None
        uid = None
        try :
            uid = self.db.user.lookup (luser.uid  [0])
        except KeyError :
            pass
        if uid :
            upicids = self.db.user.get (uid, 'pictures')
            pics = [self.db.file.getnode (i) for i in upicids]
            for n, p in enumerate (sorted (pics, key = lambda x : x.activity)) :
                if p.content == lpic :
                    if n :
                        # refresh name to put it in front
                        self.db.file.set (p.id, name = str (date.Date ('.')))
                    break
            else :
                f = self.db.file.create \
                    ( name    = str (date.Date ('.'))
                    , content = lpic
                    , type    = 'image/jpeg'
                    )
                upicids.append (f)
            return upicids
        else :
            f = self.db.file.create \
                ( name    = str (date.Date ('.'))
                , content = lpic
                , type    = 'image/jpeg'
                )
            return [f]
    # end def ldap_picture

    def sync_user_from_ldap (self, username) :
        uid = None
        try :
            uid   = self.db.user.lookup  (username)
        except KeyError :
            pass
        user  = uid and self.db.user.getnode (uid)
        luser = self.get_ldap_user_by_username (username)
        if not user and not luser :
            # nothing to do
            return
        changed = False
        if not luser or luser.is_obsolete :
            self.db.user.set (uid, status = self.status_obsolete)
            print >> sys.stderr, "Obsolete: %s" % username
            changed = True
        else :
            d = {}
            for k, (lk, x, method) in self.attr_map ['user'].iteritems () :
                if method :
                    v = method (luser, lk)
                    print "Got:", lk, v
                    if v :
                        d [k] = v
            if user :
                assert (user.status != self.status_system)
                for k, v in d.items () :
                    if user [k] == v :
                        del d [k]
                if user.status == self.status_obsolete :
                    d ['status'] = self.status_valid
                if d :
                    print >> sys.stderr, "Update roundup: %s" % username, d
                    self.db.user.set (uid, ** d)
                    changed = True
            else :
                print >> sys.stderr, "Create roundup: %s" % username, d
                assert (d)
                d ['roles'] = 'User,Nosy'
                uid = self.db.user.create (username = username, ** d)
                changed = True
        if changed :
            pass
            self.db.commit ()
    # end def sync_user_from_ldap

    def sync_user_to_ldap (self, username) :
        uid = self.db.user.lookup (username)
        user = self.db.user.getnode (uid)
        assert (user.status != self.status_system)
        luser = self.get_ldap_user_by_username (user.username)
        if not luser :
            print "LDAP user not found:", user.username
            # Might want to create user in LDAP
            return
        if user.status == self.status_obsolete :
            if not luser.is_obsolete :
                print "Roundup user obsolete:", user.username
                # Might want to move user in LDAP Tree
            return
        if luser.is_obsolete :
            print "Obsolete LDAP user: %s" % user.username
            return
        umap = self.attr_map ['user']
        modlist = []
        for rk, (lk, change, x) in umap.iteritems () :
            rupattr = user [rk]
            if callable (rupattr and change) :
                rupattr = change (user, rk)
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
                ldattr = res [lk][0]
                if ldattr != rupattr :
                    if not change :
                        print "%s:  attribute differs: %s/%s >%s/%s<" % \
                            (user.username, rk, lk, prupattr, ldattr)
                    else :
                        print "%s:  Updating: %s/%s >%s/%s<" % \
                            (user.username, rk, lk, prupattr, ldattr)
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
# end LDAP_Roundup_Sync

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

#        for uid in self.db.user.filter (None, {}, sort=[('+','username')]) :

def init (instance) :
    pass
# end def init
