#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import ldap

from copy                import copy
from traceback           import print_exc
from ldap.cidict         import cidict
from ldap.controls       import SimplePagedResultsControl
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
        dn = ldap.dn.str2dn (self.dn.lower ())
        self.ou = dict.fromkeys (k [0][1] for k in dn if k [0][0] == 'ou')
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
    db   = user.cl.db
    pics = [db.file.getnode (i) for i in user.pictures]
    for p in sorted (pics, reverse = True, key = lambda x : x.activity) :
        return p.content
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

    page_size     = 50
    
    def __init__ (self, db, update_roundup = None, update_ldap = None) :
        self.db             = db
        self.cfg            = db.config.ext
        self.update_ldap    = update_ldap
        self.update_roundup = update_roundup

        for k in 'update_ldap', 'update_roundup' :
            if getattr (self, k) is None :
                # try finding out via config, default to True
                try :
                    update = getattr (self.cfg, 'LDAP_' + k.upper ())
                except AttributeError :
                    update = 'yes'
                setattr (self, k, False)
                if update.lower () in ('yes', 'true') :
                    setattr (self, k, True)

        self.ldcon = ldap.initialize (self.cfg.LDAP_URI)
        self.ldcon.set_option (ldap.OPT_REFERRALS, 0)
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
            raise
            #print >> sys.stderr,"LDAP bind failed: %s" % cause.args [0]['desc']
        self.valid_stati     = []
        self.status_obsolete = db.user_status.lookup ('obsolete')
        self.status_sync     = [self.status_obsolete]
        self.ldap_groups     = {}
        for id in db.user_status.filter (None, {}, sort = ('+', 'id')) :
            st = db.user_status.getnode (id)
            if st.ldap_group :
                self.status_sync.append (id)
                self.valid_stati.append (id)
                self.ldap_groups [id] = st
        self.contact_types = {}
        if 'uc_type' in self.db.classes :
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
        """ Map roundup attributes to ldap attributes
            for 'user' we have a dict indexed by user attribute and
            store a 3-tuple:
            - Name of ldap attribute
            - method or function to convert from roundup to ldap
              alternatively a value that evaluates to True or False,
              False means we don't sync to ldap, True means we use the
              roundup attribute without modification.
            - method or function to convert from ldap to roundup
            for user_contact we have a dict indexed by uc_type name
            storing the primary ldap attribute and an optional secondary
            attribute of type list.
        """
        attr_map = dict (user = dict ())
        attr_u   = attr_map ['user']
        props    = self.db.user.properties
        if 'department' in props :
            attr_u ['department'] = \
                ( 'department'
                , get_name
                , self.cls_lookup (self.db.department)
                )
        if 'firstname' in props :
            attr_u ['firstname'] = \
                ( 'givenname'
                , 0
                , lambda x, y : x.get (y, [None])[0]
                )
        if 'lastname' in props :
            attr_u ['lastname'] = \
                ( 'sn'
                , 0
                , lambda x, y : x.get (y, [None])[0]
                )
        if 'nickname' in props :
            attr_u ['nickname'] = \
                ( 'initials'
                , lambda x, y : x [y].upper ()
                , lambda x, y : x.get (y, [''])[0].lower ()
                )
        if 'org_location' in props :
            attr_u ['org_location'] = \
                ( 'company'
                , get_name
                , self.cls_lookup (self.db.org_location)
                )
        if 'picture' in props :
            attr_u ['pictures'] = \
                ( 'thumbnailPhoto'
                , get_picture
                , self.ldap_picture
                )
        if 'position' in props :
            attr_u ['position'] = \
                ( 'title'
                , get_position
                , self.cls_lookup (self.db.position, 'position')
                )
        if 'realname' in props :
            g = lambda x, y : x.get (y, [None])[0]
            if 'firstname' in props :
                g = None
            attr_u ['realname'] = \
                ( 'cn'
                , 0
                , g
                )
        if 'room' in props :
            attr_u ['room'] = \
                ( 'physicalDeliveryOfficeName'
                , get_name
                , self.cls_lookup
                    ( self.db.room
                    , 'name'
                    , dict (location = self.db.location.lookup ('Wien'))
                    )
                )
        if 'substitute' in props :
            attr_u ['substitute'] = \
                ( 'secretary'
                , self.get_username_attribute_dn
                , self.get_roundup_uid_from_dn_attr
                )
        if 'supervisor' in props :
            attr_u ['supervisor'] = \
                ( 'manager'
                , self.get_username_attribute_dn
                , self.get_roundup_uid_from_dn_attr
                )
        if 'title' in props :
            attr_u ['title'] = \
                ( 'carLicense'
                , 1
                , lambda x, y : x.get (y, [None])[0]
                )
        if self.contact_types :
            attr_map ['user_contact'] = \
                { 'Email'          : ('mail',)
                , 'internal Phone' : ('telephoneNumber', 'otherTelephone')
                , 'mobile Phone'   : ('mobile',          'otherMobile')
                , 'Mobile short'   : ('pager',           'otherPager')
        #       , 'external Phone' : ('telephoneNumber', 'otherTelephone')
        #       , 'private Phone'  : ('homePhone',       'otherHomePhone')
                }
        else :
            attr_u ['address'] = \
                ( 'mail'
                , 0
                , self.set_roundup_email_address
                )
        self.attr_map = attr_map
    # end def compute_attr_map

    def cls_lookup (self, cls, insert_attr_name = None, params = None) :
        """ Generate a lookup method (non-failing) for the given class.
            Needed for easy check if an LDAP attribute exists as a
            roundup class. We need the roundup class in a closure.
        """
        def look (luser, txt) :
            try :
                key = luser [txt][0]
            except KeyError :
                return None
            try :
                return cls.lookup (key)
            except KeyError :
                pass
            if insert_attr_name :
                print "Update roundup: new %s: %s" % (cls.classname, key)
                if self.update_roundup :
                    d = params or {}
                    d [insert_attr_name] = key
                    return cls.create (** d)
            return None
        # end def look
        return look
    # end def cls_lookup

    def set_roundup_email_address (self, luser, txt) :
        """ Look up email of ldap user and do email processing in case
            roundup is configured for only the standard 'address' and
            'alternate_addresses' attributes. Old email settings are
            retained.
        """
        try :
            mail = luser [txt][0]
        except KeyError :
            return None
        uid = None
        try :
            uid = self.db.user.lookup (luser.uid  [0])
        except KeyError :
            pass
        if not uid :
            return mail
        user = self.db.user.getnode (uid)
        # unchanged ?
        if user.address == mail :
            return mail
        aa = {}
        if user.alternate_addresses :
            aa = dict.fromkeys \
                (x.strip () for x in user.alternate_addresses.split ('\n'))
        oldaa = copy (aa)
        aa [user.address] = None
        if mail in aa :
            del aa [mail]
        if aa != oldaa :
            print "Update roundup: %s alternate_addresses = %s" \
                % (user.username, ','.join (aa.iterkeys ()))
            if self.update_roundup :
                self.db.user.set \
                    (uid, alternate_addresses = '\n'.join (aa.iterkeys ()))
        return mail
    # end def set_roundup_email_address

    def get_all_ldap_usernames (self) :
        for r in self.paged_search_iter ('(objectclass=person)', ['uid']) :
            if 'uid' not in r :
                continue
            yield (r.uid [0])
    # end def get_all_ldap_usernames

    def get_roundup_group (self) :
        """ Get list of members of self.ldap_groups into self.members
            The value stored under the member is the group (the
            user_status.id).
            Implementation note: We sort by the key of self.ldap_groups,
            this is by numeric user_status id. This means later
            user_status will overwrite earlier user_status if a user is
            in several groups. This usually means he will get the lower
            credentials as the first group in self.ldap_groups is the
            normal user group.
        """
        self.members = {}
        for us_id, ustatus in sorted (self.ldap_groups.iteritems ()) :
            gname = ustatus.ldap_group
            f = '(&(sAMAccountName=%s)(objectclass=group))' % gname
            l = self.ldcon.search_s \
                (self.cfg.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, f)
            results = []
            for r in l :
                if not r [0] : continue
                r = LDAP_Search_Result (r)
                results.append (r)
            assert (len (results) == 1)
            r = results [0]
            names = dict.fromkeys ((m.lower () for m in r.member), us_id)
            self.members.update (names)
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
        """ Either the user is not in one of the ldap groups anymore or
            the group has no roles which means the user should be
            deleted.
        """
        ldn = luser.dn.lower ()
        return \
            (  ldn not in self.members
            or not self.ldap_groups [self.members [ldn]].roles
            )
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
            for n, p in enumerate \
                (sorted (pics, reverse = True, key = lambda x : x.activity)) :
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

    def paged_search_iter (self, filter, attrs = None) :
        # Test vor version 2.3 API
        try :
            lc = SimplePagedResultsControl \
                (ldap.LDAP_CONTROL_PAGE_OID, True, (self.page_size, ''))
            api_version = 3
        except AttributeError :
            # New version 2.4 API
            lc = SimplePagedResultsControl \
                (True, size = self.page_size, cookie = '')
            sc = \
                { SimplePagedResultsControl.controlType :
                    SimplePagedResultsControl
                }
            api_version = 4
        res = self.ldcon.search_ext \
            ( self.cfg.LDAP_BASE_DN
            , ldap.SCOPE_SUBTREE
            , filter
            , attrlist    = attrs
            , serverctrls = [lc]
            )
        while True :
            params = (res,)
            if api_version == 3 :
                rtype, rdata, rmsgid, serverctrls = self.ldcon.result3 (res)
                pctrls = \
                    [c for c in serverctrls
                       if c.controlType == ldap.LDAP_CONTROL_PAGE_OID
                    ]
            else :
                rtype, rdata, rmsgid, serverctrls = self.ldcon.result3 \
                    (res, resp_ctrl_classes = sc)
                pctrls = \
                    [c for c in serverctrls
                       if c.controlType == SimplePagedResultsControl.controlType
                    ]
            for r in rdata :
                if not r [0] :
                    continue
                r = LDAP_Search_Result (r)
                yield r
            if pctrls :
                if api_version == 3 :
                    x, cookie = pctrls [0].controlValue
                    lc.controlValue = (self.page_size, cookie)
                else :
                    cookie = pctrls [0].cookie
                    lc.cookie = cookie
                if not cookie :
                    break
                res =  self.ldcon.search_ext \
                    ( self.cfg.LDAP_BASE_DN
                    , ldap.SCOPE_SUBTREE
                    , filter
                    , attrs
                    , serverctrls = [lc]
                    )
            else :
                break
    # end def paged_search_iter

    def sync_contacts_from_ldap (self, luser, user, udict) :
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
                        if n.order != order and self.update_roundup :
                            self.db.user_contact.set (n.id, order = order)
                            changed = True
                        del oldmap [key]
                    elif self.update_roundup :
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
                if n.order != order and self.update_roundup :
                    self.db.user_contact.set (n.id, order = order)
                    changed = True
                order += 1
                new_contacts.append (n.id)
                del oldmap [k]
        if self.update_roundup :
            for n in oldmap.itervalues () :
                self.db.user_contact.retire (n.id)
                changed = True
        oct = list (sorted (oct.iterkeys ()))
        new_contacts.sort ()
        if new_contacts != oct :
            udict ['contacts'] = new_contacts
    # end def sync_contacts_from_ldap

    def sync_user_from_ldap (self, username, update = None) :
        if update is not None :
            self.update_roundup = update
        uid = None
        try :
            uid   = self.db.user.lookup  (username)
        except KeyError :
            pass
        user  = uid and self.db.user.getnode (uid)
        # don't modify system users:
        reserved = ('admin', 'anonymous')
        if  (  username in reserved
            or user and user.status not in self.status_sync
            ) :
            return
        luser = self.get_ldap_user_by_username (username)
        if not user and (not luser or self.is_obsolete (luser)) :
            # nothing to do
            return
        changed = False
        if not luser or self.is_obsolete (luser) :
            if user.status != self.status_obsolete :
                print >> sys.stderr, "Obsolete: %s" % username
                if self.update_roundup :
                    self.db.user.set (uid, status = self.status_obsolete)
                changed = True
        else :
            d = {}
            for k, (lk, x, method) in self.attr_map ['user'].iteritems () :
                if method :
                    v = method (luser, lk)
                    if v :
                        d [k] = v

            if self.contact_types :
                self.sync_contacts_from_ldap (luser, user, d)
            new_status_id = self.members [luser.dn.lower ()]
            assert (new_status_id)
            new_status = self.db.user_status.getnode (new_status_id)
            roles = new_status.roles
            if not roles :
                roles = self.db.config.NEW_WEB_USER_ROLES
            if user :
                assert (user.status in self.status_sync)
                for k, v in d.items () :
                    if user [k] == v :
                        del d [k]
                if user.status != new_status_id :
                    # Roles were removed when setting user obsolete
                    # Also need to adapt roles if user.status changes
                    # set these to default settings for this status
                    d ['roles']  = roles
                    d ['status'] = new_status_id
                if d :
                    print "Update roundup: %s" % username, d
                    if self.update_roundup :
                        self.db.user.set (uid, ** d)
                        changed = True
            else :
                assert (d)
                d ['roles']  = roles
                d ['status'] = new_status_id
                print "Create roundup: %s" % username, d
                if self.update_roundup :
                    uid = self.db.user.create \
                        (username = username, ** d)
                    changed = True
        if changed and self.update_roundup :
            self.db.commit ()
    # end def sync_user_from_ldap

    def sync_contacts_to_ldap (self, user, luser, modlist) :
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
                        modlist.append ((ldap.MOD_ADD, s, cs [1:]))
                else :
                    if luser [s] != cs [1:] :
                        print "%s:  Updating: %s/%s %s/%s" % \
                            (user.username, ct, s, cs [1:], ldattr)
                        modlist.append ((ldap.MOD_REPLACE, s, cs [1:]))
        for ct, fields in self.attr_map ['user_contact'].iteritems () :
            if ct not in contacts :
                for f in fields :
                    if f in luser :
                        print "%s:  Deleting: %s" % (user.username, f)
                        modlist.append ((ldap.MOD_REPLACE, f, []))
    # end def sync_contacts_to_ldap

    def sync_user_to_ldap (self, username, update = None) :
        if update is not None :
            self.update_ldap = update
        uid  = self.db.user.lookup (username)
        user = self.db.user.getnode (uid)
        assert (user.status in self.status_sync)
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
        if self.contact_types :
            self.sync_contacts_to_ldap (user, luser, modlist)
        #print "Modlist:"
        #for k in modlist :
        #    print k
        if modlist and self.update_ldap :
            self.ldcon.modify_s (luser.dn, modlist)
        elif modlist :
            print "No ldap updates performed"
    # end def sync_user_to_ldap

    def sync_all_users_from_ldap (self, update = None) :
        if update is not None :
            self.update_roundup = update
        usrcls = self.db.user
        usernames = dict.fromkeys \
            (usrcls.get (i, 'username') for i in usrcls.getnodeids ())
        usernames.update (dict.fromkeys (self.get_all_ldap_usernames ()))
        for username in usernames.iterkeys () :
            try :
                self.sync_user_from_ldap (username)
            except Exception :
                print >> sys.stderr, "Error synchronizing user %s" % username
                print_exc ()
    # end def sync_all_users_from_ldap

    def sync_all_users_to_ldap (self, update = None) :
        if update is not None :
            self.update_ldap = update
        for uid in self.db.user.filter \
            ( None
            , dict (status = ','.join (self.valid_stati))
            , sort = [('+','username')]
            ) :
            username = self.db.user.get (uid, 'username')
            self.sync_user_to_ldap (username)
    # end def sync_all_users_to_ldap
# end LDAP_Roundup_Sync

def check_ldap_config (db) :
    """ The given db can also be an instance, it just has to have a config
        object as an attribute.
    """
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
        invalid = self.db.user_status.lookup ('obsolete')
        # try to get user
        user = None
        try :
            user = self.db.user.lookup  (username)
            user = self.db.user.getnode (user)
        except KeyError :
            pass
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
            if user.status not in self.ldsync.status_sync :
                return self.__super.verifyLogin (username, password)
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
