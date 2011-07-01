#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import ldap

from ldap.cidict         import cidict
from rsclib.autosuper    import autosuper
from roundup.date        import Date
from roundup.cgi.actions import LoginAction
from roundup.cgi         import exceptions

class LDAP_Search_Result (cidict, autosuper) :
    """ Wraps an LDAP search result.
        Noteworthy detail: We use an ldap.cidict for keeping the
        attributes, this is a case-insensitive dictionary variant.
    """
    def __init__ (self, vals) :
        assert (vals [0])
        self.dn = vals [0]
        dn = (x.split ('=') for x in self.dn.lower ().split (','))
        ou = dict.fromkeys (v.strip () for k, v in dn if k.strip () == 'ou')
        self.ou = ou
        self.__super.__init__ (vals [1])
    # end def __init__

    ou_obsolete = ('obsolete', 'z_test')

    @property
    def is_obsolete (self) :
        for i in self.ou_obsolete :
            if i in self.ou :
                return True
        return False
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

def get_picture (user, attr) :
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

    roundup_group = 'roundup-users'
    
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
        self.compute_attr_map  ()
        self.get_roundup_group ()
    # end def __init__

    def bind_as_user (self, username, password) :
        luser = self.get_ldap_user_by_username (username)
        if not luser :
            return None
        try :
            self.ldcon.bind_s (luser.dn, password)
            return True
        except ldap.LDAPError, e :
            print >> sys.stderr, e
            pass
        return None
    # end def bind_as_user

    def compute_attr_map (self) :
        """ map roundup attributes to ldap attributes """
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

    def get_all_ldap_usernames (self) :
        filter = '(objectclass=person)'
        attrs  = ['uid']
        res = self.ldcon.search_s \
            (self.cfg.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, filter, attrs)
        for r in res :
            if not r [0] :
                continue
            r = LDAP_Search_Result (r)
            if 'uid' not in r :
                continue
            yield (r.uid [0]).lower ()
    # end def get_all_ldap_usernames

    def get_roundup_group (self) :
        """ Get list of members of self.roundup_group into self.members
        """
        f = '(&(sAMAccountName=%s)(objectclass=group))' % self.roundup_group
        l = self.ldcon.search_s (self.cfg.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, f)
        results = []
        for r in l :
            if not r [0] : continue
            r = LDAP_Search_Result (r)
            results.append (r)
        assert (len (results) == 1)
        r = results [0]
        self.members = dict.fromkeys (m.lower () for m in r.member)
    # end def get_roundup_group

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

    def is_obsolete (self, luser) :
        return luser.dn.lower () not in self.members
    # end def is_obsolete

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
                        self.db.file.set (p.id, name = str (Date ('.')))
                    break
            else :
                f = self.db.file.create \
                    ( name    = str (Date ('.'))
                    , content = lpic
                    , type    = 'image/jpeg'
                    )
                upicids.append (f)
            return upicids
        else :
            f = self.db.file.create \
                ( name    = str (Date ('.'))
                , content = lpic
                , type    = 'image/jpeg'
                )
            return [f]
    # end def ldap_picture

    def sync_user_from_ldap (self, username, update = True) :
        uid = None
        try :
            uid   = self.db.user.lookup  (username)
        except KeyError :
            pass
        user  = uid and self.db.user.getnode (uid)
        # don't modify system users:
        reserved = ('admin', 'anonymous')
        if username in reserved or user and user.status == self.status_system :
            return
        luser = self.get_ldap_user_by_username (username)
        if not user and (not luser or self.is_obsolete (luser)) :
            # nothing to do
            return
        changed = False
        if not luser or self.is_obsolete (luser) :
            if user.status != self.status_obsolete :
                print >> sys.stderr, "Obsolete: %s" % username
                if update :
                    self.db.user.set (uid, status = self.status_obsolete)
                changed = True
        else :
            d = {}
            for k, (lk, x, method) in self.attr_map ['user'].iteritems () :
                if method :
                    v = method (luser, lk)
                    if v :
                        d [k] = v
            oct = []
            if user :
                oct = user.contacts
            oct = dict ((id, self.db.user_contact.getnode (id)) for id in oct)
            ctypes = dict \
                ((i, self.db.uc_type.get (i, 'name'))
                 for i in self.db.uc_type.getnodeids ()
                )
            oldmap = dict \
                (((ctypes [n.contact_type], n.contact), n)
                 for n in oct.itervalues ()
                )
            new_contacts = []
            for type, lds in self.attr_map ['user_contact'].iteritems () :
                tid = self.db.uc_type.lookup (type)
                order = 1
                for ld in lds :
                    if ld not in luser : continue
                    for ldit in luser [ld] :
                        key = (type, ldit)
                        if key in oldmap :
                            n = oldmap [key]
                            new_contacts.append (n.id)
                            if n.order != order and update :
                                self.db.user_contact.set (n.id, order = order)
                                changed = True
                            del oldmap [key]
                        elif update :
                            id = self.db.user_contact.create \
                                ( contact_type = tid
                                , contact      = ldit
                                , order        = order
                                )
                            new_contacts.append (id)
                            changed = True
                        order += 1
            # special case of emails: we don't have "other" attributes
            # so roundup potentially has more emails which should be
            # preserved
            email = self.db.uc_type.lookup ('Email')
            order = 2
            for k, n in sorted (oldmap.items (), key = lambda x : x [1].order) :
                if n.contact_type == email :
                    if n.order != order and update :
                        self.db.user_contact.set (n.id, order = order)
                        changed = True
                    order += 1
                    new_contacts.append (n.id)
                    del oldmap [k]
            if update :
                for n in oldmap.itervalues () :
                    self.db.user_contact.retire (n.id)
                    changed = True
            oct = list (sorted (oct.iterkeys ()))
            new_contacts.sort ()
            if new_contacts != oct :
                d ['contacts'] = new_contacts

            if user :
                assert (user.status != self.status_system)
                for k, v in d.items () :
                    if user [k] == v :
                        del d [k]
                if user.status == self.status_obsolete :
                    # Roles where removed when setting user obsolete
                    # set these to default settings
                    d ['status'] = self.status_valid
                    d ['roles']  = self.db.config.NEW_WEB_USER_ROLES
                if d :
                    print "Update roundup: %s" % username, d
                    if update :
                        self.db.user.set (uid, ** d)
                        changed = True
            else :
                print "Create roundup: %s" % username, d
                assert (d)
                d ['roles'] = self.db.config.NEW_WEB_USER_ROLES
                if update :
                    uid = self.db.user.create \
                        (username = username.lower (), ** d)
                    changed = True
        if changed and update:
            self.db.commit ()
    # end def sync_user_from_ldap

    def sync_user_to_ldap (self, username, update = True) :
        self.update = update
        uid  = self.db.user.lookup (username)
        user = self.db.user.getnode (uid)
        assert (user.status != self.status_system)
        luser = self.get_ldap_user_by_username (user.username)
        if not luser :
            print "LDAP user not found:", user.username
            # Might want to create user in LDAP
            return
        if user.status == self.status_obsolete :
            if not self.is_obsolete (luser) :
                print "Roundup user obsolete:", user.username
                # Might want to move user in LDAP Tree
            return
        if self.is_obsolete (luser) :
            print "Obsolete LDAP user: %s" % user.username
            return
        umap = self.attr_map ['user']
        modlist = []
        for rk, (lk, change, x) in umap.iteritems () :
            rupattr = user [rk]
            if rupattr and callable (change) :
                rupattr = change (user, rk)
            prupattr = rupattr
            if rk == 'pictures' :
                prupattr = '<suppressed>'
                if len (rupattr) > 102400 :
                    print "%s: Picture too large: %s" \
                        % (user.username, len (rupattr))
                    continue
            if lk not in luser :
                if user [rk] :
                    print "%s: Inserting: %s (%s)" \
                        % (user.username, lk, prupattr)
                    assert (change)
                    modlist.append ((ldap.MOD_ADD, lk, rupattr))
            elif len (luser [lk]) != 1 :
                print "%s: invalid length: %s" % (user.username, lk)
            else :
                ldattr = pldattr = luser [lk][0]
                if rk == 'pictures' :
                    pldattr = '<suppressed>'
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
            n = self.contact_types [contact.contact_type]
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
            if p not in luser :
                print "%s: Inserting: %s (%s)" % (user.username, p, cs [0])
                modlist.append ((ldap.MOD_ADD, p, cs [0]))
            elif len (luser [p]) != 1 :
                print "%s: invalid length: %s" % (user.username, p)
            else :
                ldattr = luser [p][0]
                if ldattr != cs [0] :
                    print "%s:  Updating: %s/%s %s/%s" % \
                        (user.username, ct, p, cs [0], ldattr)
                    modlist.append ((ldap.MOD_REPLACE, p, cs [0]))
            if s :
                if s not in luser :
                    if cs [1:] :
                        print "%s: Inserting: %s (%s)" \
                            % (user.username, s, cs [1:])
                        if s not in self.forbidden :
                            modlist.append ((ldap.MOD_ADD, s, cs [1:]))
                else :
                    if luser [s] != cs [1:] :
                        print "%s:  Updating: %s/%s %s/%s" % \
                            (user.username, ct, s, cs [1:], ldattr)
                        if s not in self.forbidden :
                            modlist.append ((ldap.MOD_REPLACE, s, cs [1:]))
        for ct, fields in self.attr_map ['user_contact'].iteritems () :
            if ct not in contacts :
                for f in fields :
                    if f in luser :
                        print "%s:  Deleting: %s" % (user.username, f)
                        modlist.append ((ldap.MOD_REPLACE, f, []))
        #print "Modlist:"
        #for k in modlist :
        #    print k
        if modlist and self.update :
            self.ldcon.modify_s (luser.dn, modlist)
    # end def sync_user_to_ldap

    def sync_all_users_from_ldap (self, update = False) :
        usrcls = self.db.user
        usernames = dict.fromkeys \
            (usrcls.get (i, 'username') for i in usrcls.getnodeids ())
        usernames.update (dict.fromkeys (self.get_all_ldap_usernames ()))
        for username in usernames.iterkeys () :
            self.sync_user_from_ldap (username, update = update)
    # end def sync_all_users_from_ldap

    def sync_all_users_to_ldap (self, update = False) :
        for uid in self.db.user.filter \
            (None, dict (status = self.status_valid), sort=[('+','username')]) :
            username = self.db.user.get (uid, 'username')
            self.sync_user_to_ldap (username, update)
    # end def sync_all_users_to_ldap
# end LDAP_Roundup_Sync

def check_ldap_config (db) :
    cfg = db.config.ext
    uri = None
    try :
        uri = cfg.LDAP_URI
    except KeyError :
        pass
    return uri
# end def check_ldap_config

class LdapLoginAction (LoginAction, autosuper) :
    def try_ldap (self) :
        uri = check_ldap_config (self.db)
        if uri :
            self.ldsync = LDAP_Roundup_Sync (self.db)
        return bool (uri)
    # end def try_ldap

    def verifyLogin (self, username, password) :
        if username in ('admin', 'anonymous') :
            return self.__super.verifyLogin (username, password)
        sysuser = self.db.user_status.lookup ('system')
        invalid = self.db.user_status.lookup ('obsolete')
        # try to get user
        user = None
        try :
            user = self.db.user.lookup  (username)
            user = self.db.user.getnode (user)
        except KeyError :
            pass
        if user and user.status == sysuser :
            return self.__super.verifyLogin (username, password)
        # sync the user
        self.client.error_message = []
        if self.try_ldap () :
            self.ldsync.sync_user_from_ldap (username)
            try :
                user = self.db.user.lookup  (username)
                user = self.db.user.getnode (user)
            except KeyError :
                raise exceptions.LoginError (self._ ('Invalid login'))
            if user.status == invalid :
                raise exceptions.LoginError (self._ ('Invalid login'))
            if not password :
                raise exceptions.LoginError (self._ ('Invalid login'))
            if not self.ldsync.bind_as_user (username, password) :
                raise exceptions.LoginError (self._ ('Invalid login'))
            self.client.userid = user.id
        else :
            if not user or user.status == invalid :
                raise exceptions.LoginError (self._ ('Invalid login'))
            return self.__super.verifyLogin (username, password)
    # end def verifyLogin
# end class LdapLoginAction

def sync_from_ldap (db, username) :
    """ Convenience method """
    if not check_ldap_config (db) :
        return
    lds = LDAP_Roundup_Sync (db)
    lds.sync_user_from_ldap (username)
# end def sync_from_ldap
