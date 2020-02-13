#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import ldap
import user_dynamic

from copy                import copy
from traceback           import print_exc
from ldap.cidict         import cidict
from ldap.controls       import SimplePagedResultsControl
from ldap.filter         import escape_filter_chars
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
# end def get_name

def get_position (user, attr) :
    """ Get position name from roundup user class """
    assert (attr == 'position')
    return user.cl.db.position.get (user.position, 'position')
# end def get_position

def tohex (s) :
    return ''.join ('%02X' % ord (k) for k in s)
# end def tohex

def fromhex (s) :
    """ Invert tohex above
        >>> fromhex ('1001020304050607ff4142')
        '\\x10\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\xffAB'
        >>> fromhex ('47110815')
        'G\\x11\\x08\\x15'
    """
    return ''.join (chr (int (a+b, 16)) for (a, b) in zip (s [0::2], s [1::2]))
# end def fromhex

def get_guid (luser, attr) :
    r = luser.get (attr, [None]) [0]
    if r is not None :
        return tohex (r)
    return r
# end def get_guid

def set_guid (node, attribute) :
    s = node [attribute]
    if not s :
        return s
    return fromhex (s)
# end def set_guid

class BackslashInUsername(Exception):
    def __init__(self, expression, message=None):
        if message is None:
            # set default message
            message = "Backslash in username '%s' not allowed." % expression
        super(BackslashInUsername, self).__init__(expression, message)
        self.expression = expression
        self.message = message

class LDAP_Roundup_Sync (object) :
    """ Sync users from LDAP to Roundup """

    page_size     = 50

    single_ldap_attributes = dict.fromkeys \
        (('email', 'telephonenumber'))
    
    def __init__ \
        (self, db, update_roundup = None, update_ldap = None, verbose = 1) :
        self.db             = db
        self.cfg            = db.config.ext
        self.verbose        = verbose
        self.update_ldap    = update_ldap
        self.update_roundup = update_roundup
        self.ad_domain      = self.cfg.LDAP_AD_DOMAINS.split (',')
        self.objectclass    = getattr (self.cfg, 'LDAP_OBJECTCLASS', 'person')

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

    def get_realname (self, x, y) :
        fn = x.get ('givenname', [''])[0]
        ln = x.get ('sn', ['']) [0]
        if fn and ln :
            return ' '.join ((fn, ln))
        elif fn :
            return fn
        return ln
    # end def get_realname

    def compute_attr_map (self) :
        """ Map roundup attributes to ldap attributes
            for 'user' we have a dict indexed by user attribute and
            store a 4-tuple:
            - Name of ldap attribute
            - method or function to convert from roundup to ldap
              alternatively a value that evaluates to True or False,
              False means we don't sync to ldap, True means we use the
              roundup attribute without modification.
            - method or function to convert from ldap to roundup
            - 4th arg indicates if updates coming from ldap may be
              empty, currently used only for nickname (aka initials in ldap)
            for user_contact we have a dict indexed by uc_type name
            storing the primary ldap attribute and an optional secondary
            attribute of type list.
        """
        dontsync = getattr (self.cfg, 'LDAP_DO_NOT_SYNC', '')
        if dontsync :
            dontsync = dict.fromkeys (dontsync.split (','))
        else :
            dontsync = {}
        attr_map = dict (user = dict ())
        attr_u   = attr_map ['user']
        props    = self.db.user.properties
        dynprops = {}
        if 'user_dynamic' in self.db.classes :
            dynprops = self.db.user_dynamic.properties
        # 1st arg is the name in ldap
        # 2nd arg is 0 for no change, 1 for change or a method for
        #         conversion from roundup to ldap when syncing 
        # 3rd arg is an conversion function from ldap to roundup or None
        #         if not syncing to roundup
        # 4th arg indicates if updates coming from ldap may be
        # empty, currently used only for nickname (aka initials in ldap)
        attr_u ['id'] = \
            ( 'employeenumber'
            , 1
            , None
            , False
            )
        if 'firstname' in props and 'firstname' not in dontsync :
            attr_u ['firstname'] = \
                ( 'givenname'
                , 0
                , lambda x, y : x.get (y, [None])[0]
                , False
                )
        if 'lastname' in props and 'lastname' not in dontsync :
            attr_u ['lastname'] = \
                ( 'sn'
                , 0
                , lambda x, y : x.get (y, [None])[0]
                , False
                )
        if 'nickname' in props and 'nickname' not in dontsync :
            attr_u ['nickname'] = \
                ( 'initials'
                , lambda x, y : x [y].upper ()
                , lambda x, y : x.get (y, [''])[0].lower ()
                , True
                )
        if 'ad_domain' in props and 'ad_domain' not in dontsync :
            attr_u ['ad_domain'] = \
                ( 'UserPrincipalName'
                , 0
                , lambda x, y : x [y][0].split ('@', 1)[1]
                , False
                )
        if 'username' in props and 'username' not in dontsync :
            attr_u ['username'] = \
                ( 'UserPrincipalName'
                , 0
                , lambda x, y : x.get (y, [None])[0]
                , False
                )
        if 'pictures' in props and 'pictures' not in dontsync :
            attr_u ['pictures'] = \
                ( 'thumbnailPhoto'
                , get_picture
                , self.ldap_picture
                , False
                )
        if 'position' in props and 'position' not in dontsync :
            attr_u ['position'] = \
                ( 'title'
                , get_position
                , self.cls_lookup (self.db.position, 'position')
                , False
                )
        if 'realname' in props and 'realname' not in dontsync :
            g = self.get_realname
            if 'firstname' in props :
                g = None
            attr_u ['realname'] = \
                ( 'cn'
                , 0
                , g
                , False
                )
        if 'room' in props and 'room' not in dontsync :
            attr_u ['room'] = \
                ( 'physicalDeliveryOfficeName'
                , get_name
                , self.cls_lookup
                    ( self.db.room
                    , 'name'
                    )
                , False
                )
        if 'substitute' in props and 'substitute' not in dontsync :
            attr_u ['substitute'] = \
                ( 'secretary'
                , self.get_username_attribute_dn
                , self.get_roundup_uid_from_dn_attr
                , False
                )
        if 'supervisor' in props and 'supervisor' not in dontsync :
            attr_u ['supervisor'] = \
                ( 'manager'
                , self.get_username_attribute_dn
                , self.get_roundup_uid_from_dn_attr
                , False
                )
        if 'title' in props and 'title' not in dontsync :
            attr_u ['title'] = \
                ( 'carLicense'
                , 1
                , lambda x, y : x.get (y, [None])[0]
                , False
                )
        if 'guid' in props and 'guid' not in dontsync :
            attr_u ['guid'] = \
                ( 'objectGUID'
                , set_guid
                , get_guid
                , False
                )
        # Items to be synced from current user_dynamic record.
        # Currently this is one-way, only from roundup to ldap.
        # Except for creation: If a new user is created and the
        # org_location and department properties exist in ldap we
        # perform the user_create_magic.
        # The entries inside the sub-properties 'sap_cc', 'department',
        # 'org_location' are as follows:
        # One entry for each transitive property to be synced to LDAP
        # 1st item is the property name of the linked item (in our
        #     case from sap_cc, department, org_location)
        # 2nd item is the LDAP property
        # 3rd item is the function to convert roundup->LDAP
        # 4th item is the function to convert LDAP->roundup
        #     this is currently unused, we don't sync to roundup
        attr_map ['user_dynamic'] = {}
        attr_dyn = attr_map ['user_dynamic']
        if 'org_location' in dynprops and 'org_location' not in dontsync :
            attr_dyn ['org_location'] = \
                ( ( 'name'
                  ,  'company'
                  ,  self.set_user_dynamic_prop
                  ,  None
                  )
                ,
                )
        if 'department' in dynprops and 'department' not in dontsync :
            attr_dyn ['department'] = \
                ( ( 'name'
                  ,  'department'
                  ,  self.set_user_dynamic_prop
                  ,  None
                  )
                ,
                )
        if 'sap_cc' in dynprops :
            attr_dyn ['sap_cc'] = \
                ( ( 'name'
                  , 'extensionAttribute3'
                  , self.set_user_dynamic_prop
                  , None
                  )
                , ( 'description'
                  , 'extensionAttribute4'
                  , self.set_user_dynamic_prop
                  , None
                  )
                )
        if self.contact_types :
            attr_map ['user_contact'] = \
                { 'Email'          : ('mail',)
                , 'internal Phone' : ('otherTelephone',)
                , 'external Phone' : ('telephoneNumber',)
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
                , False
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
                if self.verbose :
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
        for k in 'UserPrincipalName', 'uid' :
            try :
                uid = self.db.user.lookup (luser[k][0])
                break
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
        if user.address :
            aa [user.address] = None
        if mail in aa :
            del aa [mail]
        if aa != oldaa :
            if self.verbose :
                print "Update roundup: %s alternate_addresses = %s" \
                    % (user.username, ','.join (aa.iterkeys ()))
            if self.update_roundup :
                self.db.user.set \
                    (uid, alternate_addresses = '\n'.join (aa.iterkeys ()))
        return mail
    # end def set_roundup_email_address

    def get_all_ldap_usernames (self) :
        """ This used to return the 'uid' attribute in ldap
            We're now using the long username variant with the domain,
            so we now return the User Principal Name.
        """
        q = '(objectclass=%s)' % self.objectclass
        for r in self.paged_search_iter (q, ['UserPrincipalName']) :
            if 'UserPrincipalName' not in r :
                continue
            yield (r.userprincipalname [0])
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
            Retrieval uses a range retrieval with 1000 items for each
            request. Microsoft AD has a limit around 1500-5000 entries
            in a multivalues attribute (member in this case):
            https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ldap/searching-using-range-retrieval
        """
        self.members = {}
        for us_id, ustatus in sorted (self.ldap_groups.iteritems ()) :
            gname = ustatus.ldap_group
            f  = '(&(sAMAccountName=%s)(objectclass=group))' % gname
            n  = 0
            sz = 1000
            r  = 1000
            while r >= 1000 :
                a = ['member;range=%s-%s' % (n, n + sz - 1)]
                l = self.ldcon.search_s \
                    (self.cfg.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, f, a)
                results = []
                for r in l :
                    if not r [0] : continue
                    r = LDAP_Search_Result (r)
                    results.append (r)
                assert (len (results) == 1)
                r = results [0]
                assert len (r) == 1 # only the member range attribute
                k = r.keys () [0]
                assert k.startswith ('member')
                member = r [k]
                rng    = k.split (';', 1) [1]
                assert rng.startswith ('range=')
                rng    = rng [6:].split ('-')
                assert int (rng [0]) == n
                # The last range retrieved may contain '*' as right bound
                if rng [1] == '*' :
                    r = len (member)
                else :
                    r = int (rng [1]) - n + 1
                assert r > 0
                assert r <= sz
                assert r == len (member)
                n += r
                names = dict.fromkeys ((m.lower () for m in member), us_id)
                self.members.update (names)
                if rng [1] == '*' :
                    break
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
        """ This now uses the UserPrincipalName in preference over the uid.
            This used only the uid previously. We distinguish the old
            version by checking if username contains '@'.
        """
        if '@' in username :
            result = self.ldcon.search_s \
                ( self.cfg.LDAP_BASE_DN
                , ldap.SCOPE_SUBTREE
                , ( '(&(UserPrincipalName=%s)(objectclass=%s))'
                  % (username, self.objectclass)
                  )
                , None
                )
        else :
            result = self.ldcon.search_s \
                ( self.cfg.LDAP_BASE_DN
                , ldap.SCOPE_SUBTREE
                , ( '(&(uid=%s)(objectclass=%s))'
                  % (username, self.objectclass)
                  )
                , None
                )
        return self._get_ldap_user (result)
    # end def get_ldap_user_by_username

    def get_ldap_user_by_guid (self, guid) :
        g = escape_filter_chars (guid, escape_mode = 1)
        result = self.ldcon.search_s \
            ( self.cfg.LDAP_BASE_DN
            , ldap.SCOPE_SUBTREE
            , '(&(objectGUID=%s)(objectclass=%s))' % (g, self.objectclass)
            , None
            )
        return self._get_ldap_user (result)
    # end def get_ldap_user_by_guid

    def get_roundup_uid_from_dn_attr (self, luser, attr) :
        try :
            v = luser [attr][0]
        except KeyError :
            return None
        lsup = self.get_ldap_user_by_dn (v)
        if not lsup :
            return None
        # Legacy: The supervisor/substitute may still be stored without
        # domain, so we have to try both, the UserPrincipalName and the
        # uid to find the user in roundup.
        for k in 'UserPrincipalName', 'uid' :
            try :
                return self.db.user.lookup (lsup [k][0])
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
        for k in 'UserPrincipalName', 'uid' :
            try :
                uid = self.db.user.lookup (luser[k][0])
                break
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
        # Test for version 2.3 API
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

    def domain_user_check (self, username, allow_empty = False) :
        if self.ad_domain :
            if '@' not in username :
                if allow_empty :
                    return
                raise ValueError ("User without domain: %s" % username)
            dom = username.split ('@', 1) [1]
            if dom not in self.ad_domain :
                raise ValueError ("User with invalid domain: %s" % username)
    # end def domain_user_check

    def sync_user_from_ldap (self, username, update = None) :
        # Backslash in username will create all sorts of confusion in
        # generated LDAP queries, so raise an error here we can't deal
        # with it anyway:
        if '\\' in username :
            raise ValueError ("Invalid username: %s" % username)
        luser = self.get_ldap_user_by_username (username)
        if luser :
            guid = luser.objectGUID [0]
        if update is not None :
            self.update_roundup = update
        uid = None
        # First try to find user via guid:
        uids = None
        if luser :
            uids = self.db.user.filter (None, dict (guid = tohex (guid)))
        if uids :
            assert len (uids) == 1
            uid = uids [0]
        else :
            try :
                uid   = self.db.user.lookup  (username)
            except KeyError :
                pass
        user  = uid and self.db.user.getnode (uid)
        if user and not luser and user.guid :
            luser = self.get_ldap_user_by_guid (fromhex (user.guid))
        # don't modify system users:
        reserved = ('admin', 'anonymous')
        if  (  username in reserved
            or user and user.status not in self.status_sync
            ) :
            return
        if not user and (not luser or self.is_obsolete (luser)) :
            # nothing to do
            return
        self.domain_user_check (username, allow_empty = True)
        changed = False
        if not luser or self.is_obsolete (luser) :
            if user.status != self.status_obsolete :
                if self.verbose :
                    print >> sys.stderr, "Obsolete: %s" % username
                if self.update_roundup :
                    self.db.user.set (uid, status = self.status_obsolete)
                changed = True
        else :
            d = {}
            for k, (lk, x, method, em) in self.attr_map ['user'].iteritems () :
                if method :
                    v = method (luser, lk)
                    if v or em :
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
                    if self.verbose :
                        print "Update roundup: %s" % username, d
                    if self.update_roundup :
                        self.db.user.set (uid, ** d)
                        changed = True
            else :
                assert (d)
                d ['roles']  = roles
                d ['status'] = new_status_id
                if 'username' not in d :
                    d ['username'] = username
                if self.verbose :
                    print "Create roundup: %s" % username, d
                if self.update_roundup :
                    uid = self.db.user.create (** d)
                    changed = True
                    # Perform user creation magic for new user
                    olo = dep = None
                    if 'company' in luser :
                        olo = luser ['company'][0]
                        try :
                            olo = self.db.org_location.lookup (olo)
                        except KeyError :
                            olo = None
                    if 'department' in luser :
                        dep = luser ['department'][0]
                        try :
                            dep = self.db.department.lookup (dep)
                        except KeyError :
                            dep = None
                    if self.verbose :
                        print \
                            ( "User magic: %s, olo:%s dep:%s"
                            % (username, olo, dep)
                            )
                    user_dynamic.user_create_magic (self.db, uid, olo, dep)
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
                p = ldn [0]
                s = None
            else :
                p, s = ldn
            if p not in luser :
                ins = cs [0]
                if not s and ct.lower () not in self.single_ldap_attributes :
                    ins = cs
                if self.verbose :
                    print "%s: Inserting: %s (%s)" % (user.username, p, ins)
                modlist.append ((ldap.MOD_ADD, p, ins))
            elif len (luser [p]) != 1 :
                print "%s: invalid length: %s" % (user.username, p)
            else :
                ldattr = luser [p][0]
                ins = cs [0]
                if not s and ct.lower () not in self.single_ldap_attributes :
                    ins = cs
                if ldattr != ins and [ldattr] != ins :
                    if self.verbose :
                        print "%s:  Updating: %s/%s %s/%s" % \
                            (user.username, ct, p, ins, ldattr)
                    modlist.append ((ldap.MOD_REPLACE, p, ins))
            if s :
                if s not in luser :
                    if cs [1:] :
                        if self.verbose :
                            print "%s: Inserting: %s (%s)" \
                                % (user.username, s, cs [1:])
                        modlist.append ((ldap.MOD_ADD, s, cs [1:]))
                else :
                    if luser [s] != cs [1:] :
                        if self.verbose :
                            print "%s:  Updating: %s/%s %s/%s" % \
                                (user.username, ct, s, cs [1:], ldattr)
                        modlist.append ((ldap.MOD_REPLACE, s, cs [1:]))
        for ct, fields in self.attr_map ['user_contact'].iteritems () :
            if ct not in contacts :
                for f in fields :
                    if f in luser :
                        if self.verbose :
                            print "%s:  Deleting: %s" % (user.username, f)
                        modlist.append ((ldap.MOD_REPLACE, f, []))
    # end def sync_contacts_to_ldap

    def sync_user_to_ldap (self, username, update = None) :
        self.domain_user_check (username)
        if update is not None :
            self.update_ldap = update
        uid  = self.db.user.lookup (username)
        user = self.db.user.getnode (uid)
        assert (user.status in self.status_sync)
        luser = self.get_ldap_user_by_username (user.username)
        if not luser :
            if self.verbose :
                print "LDAP user not found:", user.username
            # Might want to create user in LDAP
            return
        if user.status == self.status_obsolete :
            if not self.is_obsolete (luser) :
                if self.verbose :
                    print "Roundup user obsolete:", user.username
                # Might want to move user in LDAP Tree
            return
        if self.is_obsolete (luser) :
            if self.verbose :
                print "Obsolete LDAP user: %s" % user.username
            return
        umap = self.attr_map ['user']
        modlist = []
        for rk, (lk, change, x, empty) in umap.iteritems () :
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
            if rk == 'guid' :
                prupattr = repr (rupattr)
            if lk not in luser :
                if user [rk] :
                    if self.verbose :
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
                if rk == 'guid' :
                    pldattr = repr (ldattr)
                if ldattr != rupattr :
                    if not change :
                        if self.verbose > 1 :
                            print "%s:  attribute differs: %s/%s >%s/%s<" % \
                                (user.username, rk, lk, prupattr, pldattr)
                    else :
                        if self.verbose :
                            print "%s:  Updating: %s/%s >%s/%s<" % \
                                (user.username, rk, lk, prupattr, pldattr)
                        op = ldap.MOD_REPLACE
                        if rupattr is None :
                            op = ldap.MOD_DELETE
                        modlist.append ((op, lk, rupattr))
        if 'user_dynamic' in self.attr_map :
            udmap = self.attr_map ['user_dynamic']
            for udprop, plist in udmap.iteritems () :
                for prop, lk, method, x in plist :
                    if callable (method) :
                        if lk not in luser :
                            ldattr = None
                        else :
                            ldattr = luser [lk][0]
                        chg = method (user, udprop, prop, lk, ldattr)
                        if chg :
                            if self.verbose :
                                print "%s:  Updating: %s.%s/%s >%s/%s<" % \
                                    ( user.username
                                    , udprop
                                    , prop
                                    , lk
                                    , chg [2]
                                    , ldattr
                                    )
                            modlist.append (chg)
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

    def set_user_dynamic_prop (self, user, udprop, linkprop, lk, ldattr) :
        """ Sync transitive dynamic user properties to ldap
            Gets the user to sync, the linkclass, one of (sap_cc,
            department, org_location), the linkprop (property of the
            given class), the LDAP attribute key lk and the ldap
            attribute value ldattr.
            Return a triple (ldap.<action>, lk, rupattr)
            where action is one of MOD_ADD, MOD_REPLACE, MOD_DELETE
            or None if nothing to sync
        """
        dyn = user_dynamic.get_user_dynamic (self.db, user.id, Date ('.'))
        is_empty = True
        if dyn :
            dynprop = dyn [udprop]
            if dynprop :
                classname = self.db.user_dynamic.properties [udprop].classname
                is_empty  = False
                node      = self.db.getclass (classname).getnode (dynprop)
                if node [linkprop] != ldattr :
                    if not ldattr :
                        return (ldap.MOD_ADD, lk, node [linkprop])
                    else :
                        return (ldap.MOD_REPLACE, lk, node [linkprop])
        if is_empty and ldattr != '' :
            if ldattr is None :
                return None
            else :
                return (ldap.MOD_DELETE, lk, None)
        return None
    # end def set_user_dynamic_prop

    def sync_all_users_from_ldap (self, update = None) :
        if update is not None :
            self.update_roundup = update
        usrcls = self.db.user
        # A note on this code: Users might be renamed in ldap.
        # Therefore we *first* sync with ldap to get renames (users are
        # matched via guid). Then we sync again with all usernames in
        # roundup that are *not* in ldap.
        usernames = dict.fromkeys (self.get_all_ldap_usernames ())
        for username in usernames :
            if self.ad_domain :
                if '@' not in username :
                    continue
                dom = username.split ('@', 1) [1]
                if dom not in self.ad_domain :
                    continue
            try :
                self.sync_user_from_ldap (username)
            except Exception :
                print >> sys.stderr, "Error synchronizing user %s" % username
                print_exc ()
        u_rup = [usrcls.get (i, 'username') for i in usrcls.getnodeids ()]
        users = []
        for u in u_rup :
            if u in usernames :
                continue
            if self.ad_domain :
                # A user without a domain is probably obsolete and
                # *must* be synced, so don't filter those
                if '@' in u :
                    dom = u.split ('@', 1) [1]
                    if dom not in self.ad_domain :
                        continue
            users.append (u)
        u_rup = users
        for username in u_rup :
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
            , dict (status = self.valid_stati)
            , sort = [('+','username')]
            ) :
            username = self.db.user.get (uid, 'username')
            if self.ad_domain :
                if '@' not in username :
                    continue
                dom = username.split ('@', 1) [1]
                if dom not in self.ad_domain :
                    continue
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
