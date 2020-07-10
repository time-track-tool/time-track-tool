#!/usr/bin/python
from __future__ import print_function
import sys
import logging
import ldap3
import user_dynamic
import common

from copy                import copy
from ldap3.utils.conv    import escape_bytes
from rsclib.autosuper    import autosuper
from rsclib.execute      import Log
from roundup.date        import Date
from roundup.cgi.actions import LoginAction
from roundup.cgi         import exceptions
from roundup.exceptions  import Reject

LDAPCursorError = ldap3.core.exceptions.LDAPCursorError
LDAPKeyError    = ldap3.core.exceptions.LDAPKeyError

class LDAP_Group (object) :
    """ Get all users and all member-groups of a given group.
        Microsoft has defined a magic OID 1.2.840.113556.1.4.1941 that
        allows recursive group membership search. We're using this to
        find all groups (objectclass=group) and all persons
        (objectclass=person) in the given group.
        https://docs.microsoft.com/en-us/windows/win32/adsi/search-filter-syntax
    """

    def __init__ (self, ldcon, base_dn, name, prio) :
        self.name    = name
        self.prio    = prio
        self.ldcon   = ldcon
        self.base_dn = base_dn
        self.users   = set ()
        self.groups  = set ()
        f = '(&(sAMAccountName=%s)(objectclass=group))' % name
        ldcon.search (base_dn, f)
        if not len (ldcon.entries) :
            raise KeyError (groupname)
        assert len (ldcon.entries) == 1
        self.add_group (ldcon.entries [0].entry_dn)
    # end def __init__

    def add_group (self, dn) :
        t = '(&(memberOf:1.2.840.113556.1.4.1941:=%s)(objectclass=%s))'
        self.groups.add (dn)
        for s, n in (self.users, 'person'), (self.groups, 'group') :
            f = t % (dn, n)
            self.ldcon.search (self.base_dn, f)
            for e in self.ldcon.entries :
                s.add (e.entry_dn)
    # end def add_group

# end class LDAP_Group

class LDAP_Search_Result (object) :
    """ Wraps an LDAP search result.
    """
    ou_obsolete = ('obsolete', 'z_test')

    def __init__ (self, val) :
        self.val = val
        self.dn  = val.entry_dn
        dn = ldap3.utils.dn.parse_dn (self.dn.lower ())
        self.ou  = dict.fromkeys (k [0][1] for k in dn if k [0][0] == 'ou')
    # end def __init__

    @property
    def is_obsolete (self) :
        for i in self.ou_obsolete :
            if i in self.ou :
                return True
        return False
    # end def is_obsolete

    def get (self, name, default = None) :
        try :
            return self.val [name]
        except (KeyError, LDAPCursorError, LDAPKeyError) :
            return default
    # end def get

    def __getitem__ (self, name) :
        try :
            return self.val [name]
        except (LDAPCursorError, LDAPKeyError) as err :
            raise KeyError (str (err))
    # end def __getitem__

    def __getattr__ (self, name) :
        try :
            return getattr (self.val, name)
        except (LDAPCursorError, LDAPKeyError) as err :
            raise AttributeError (str (err))
    # end def __getattr__

    def __contains__ (self, name) :
        try :
            x = self.val [name]
            return True
        except (LDAPCursorError, LDAPKeyError) as err :
            pass
        return False
    # end def __contains__

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

class LDAP_Roundup_Sync (Log) :
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
        self.base_dn        = self.cfg.LDAP_BASE_DN
        self.__super.__init__ ()

        if self.verbose :
            formatter = logging.Formatter ('%(message)s')
            handler = logging.StreamHandler (sys.stderr)
            handler.setLevel (logging.DEBUG)
            handler.setFormatter (formatter)
            self.log.addHandler (handler)

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

        self.server = ldap3.Server (self.cfg.LDAP_URI, get_info = ldap3.ALL)
        # auto_range:
        # https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ldap/searching-using-range-retrieval
        self.ldcon  = ldap3.Connection \
            ( self.server
            , self.cfg.LDAP_BIND_DN
            , self.cfg.LDAP_PASSWORD
            , auto_range = True # auto range tag handling RFC 3866
            )
        # start_tls won't work without a previous open, may be a
        # microsoft specific feature -- the ldap3 docs say otherwise
        self.ldcon.open      ()
        self.ldcon.start_tls ()
        self.ldcon.bind      ()

        self.valid_stati     = []
        self.status_obsolete = db.user_status.lookup ('obsolete')
        self.status_sync     = [self.status_obsolete]
        self.ldap_stati      = {}
        self.ldap_groups     = {}
        for id in db.user_status.filter (None, {}, sort = ('+', 'id')) :
            st = db.user_status.getnode (id)
            if st.ldap_group :
                self.status_sync.append (id)
                self.valid_stati.append (id)
                self.ldap_stati  [id] = st
                self.ldap_groups [id] = LDAP_Group \
                    (self.ldcon, self.base_dn, st.ldap_group, st.ldap_prio)
        self.contact_types = {}
        if 'uc_type' in self.db.classes :
            self.contact_types = dict \
                ((id, self.db.uc_type.get (id, 'name'))
                 for id in self.db.uc_type.list ()
                )
        self.compute_attr_map  ()
    # end def __init__

    def bind_as_user (self, username, password) :
        FIXME
        luser = self.get_ldap_user_by_username (username)
        if not luser :
            return None
        try :
            self.ldcon.bind_s (luser.dn, password)
            return True
        except ldap.LDAPError, e :
            print (e, file = sys.stderr)
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
                , lambda x, y : str (x.get (y, '')).lower ()
                , True
                )
        if 'ad_domain' in props and 'ad_domain' not in dontsync :
            attr_u ['ad_domain'] = \
                ( 'UserPrincipalName'
                , 0
                , lambda x, y : str (x [y]).split ('@', 1)[1]
                , False
                )
        if 'username' in props and 'username' not in dontsync :
            attr_u ['username'] = \
                ( 'UserPrincipalName'
                , 0
                , lambda x, y : str (x.get (y))
                , False
                )
        if 'pictures' in props and 'pictures' not in dontsync :
            attr_u ['pictures'] = \
                ( 'thumbnailPhoto'
                , get_picture
                , self.ldap_picture
                , False
                )
        if 'position_text' in props and 'position_text' not in dontsync :
            # We sync that field *to* ldap but not *from* ldap.
            attr_u ['position_text'] = \
                ( 'title'
                , 1
                , None
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
                , self.cls_lookup (self.db.room)
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
        def look (luser, txt, **dynamic_params) :
            try :
                key = luser [txt][0]
            except KeyError :
                return None
            try :
                return cls.lookup (key)
            except KeyError :
                pass
            if insert_attr_name :
                self.log.info \
                    ("Update roundup: new %s: %s" % (cls.classname, key))
                if self.update_roundup :
                    d = {}
                    if params :
                        d.update (params)
                    if dynamic_params :
                        d.update (dynamic_params)
                    d [insert_attr_name] = key
                    return cls.create (** d)
            return None
        # end def look
        return look
    # end def cls_lookup

    def member_status_id (self, dn) :
        """ Check if the given dn (which must be a person dn) is a
            member of one of our ldap_groups, return the id of the
            user_status that defines this group. We return the matching
            group with the lowest ldap_prio in the user status.
        """
        srt = lambda gid: self.ldap_groups [gid].prio
        for gid in sorted (self.ldap_groups, key = srt) :
            g = self.ldap_groups [gid]
            if dn in g.users :
                return gid
    # end def member_status_id

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
            self.log.info \
                ( "Update roundup: %s alternate_addresses = %s" \
                % (user.username, ','.join (aa.iterkeys ()))
                )
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
            # Do not return any users with wrong group
            if not self.member_status_id (r.dn) :
                continue
            yield (r.userprincipalname [0])
    # end def get_all_ldap_usernames

    def get_username_attribute_dn (self, node, attribute) :
        """ Get dn of a user Link-attribute of a node """
        s = node [attribute]
        if not s :
            return s
        s = self.db.user.get (s, 'username')
        r = self.get_ldap_user_by_username (s)
        if r is None :
            return None
        return r.dn
    # end def get_username_attribute_dn

    def _get_ldap_user (self, result) :
        if len (result) == 0 :
            return None
        assert len (result) == 1
        return LDAP_Search_Result (result [0])
    # end def _get_ldap_user

    def get_ldap_user_by_username (self, username) :
        """ This now uses the UserPrincipalName in preference over the uid.
            This used only the uid previously. We distinguish the old
            version by checking if username contains '@'.
        """
        if '@' in username :
            self.ldcon.search \
                ( self.base_dn
                , ( '(&(UserPrincipalName=%s)(objectclass=%s))'
                  % (username, self.objectclass)
                  )
                , attributes = ldap3.ALL_ATTRIBUTES
                )
        else :
            self.ldcon.search \
                ( self.base_dn
                , ( '(&(uid=%s)(objectclass=%s))'
                  % (username, self.objectclass)
                  )
                , attributes = ldap3.ALL_ATTRIBUTES
                )
        return self._get_ldap_user (self.ldcon.entries)
    # end def get_ldap_user_by_username

    def get_ldap_user_by_guid (self, guid) :
        g = escape_bytes (guid)
        self.ldcon.search \
            ( self.base_dn
            , '(&(objectGUID=%s)(objectclass=%s))' % (g, self.objectclass)
            , attributes = ldap3.ALL_ATTRIBUTES
            )
        return self._get_ldap_user (self.ldcon.entries)
    # end def get_ldap_user_by_guid

    def get_roundup_uid_from_dn_attr (self, luser, attr) :
        try :
            v = str (luser [attr])
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
        f = '(objectclass=*)'
        d = dict (search_scope = ldap3.BASE, attributes = ldap3.ALL_ATTRIBUTES)
        self.ldcon.search (dn, f, **d)
        return self._get_ldap_user (self.ldcon.entries)
    # end def get_ldap_user_by_dn

    def is_obsolete (self, luser) :
        """ Either the user is not in one of the ldap groups anymore or
            the group has no roles which means the user should be
            deleted.
        """
        stid = self.member_status_id (luser.dn)
        return (not stid or not self.ldap_stati [stid].roles)
    # end def is_obsolete

    def ldap_picture (self, luser, attr) :
        try :
            lpic = luser [attr].raw_values [0]
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
                    if n and self.update_roundup :
                        # refresh name to put it in front
                        self.db.file.set (p.id, name = str (Date ('.')))
                    break
            else :
                if self.update_roundup :
                    f = self.db.file.create \
                        ( name    = str (Date ('.'))
                        , content = lpic
                        , type    = 'image/jpeg'
                        )
                else :
                    f = '999999999'
                upicids.append (f)
            return upicids
        else :
            if self.update_roundup :
                f = self.db.file.create \
                    ( name    = str (Date ('.'))
                    , content = lpic
                    , type    = 'image/jpeg'
                    )
            else :
                f = '999999999'
            return [f]
    # end def ldap_picture

    def paged_search_iter (self, filter, attrs = None) :
        ps  = self.ldcon.extend.standard.paged_search
        d   = dict (paged_size = self.page_size, generator = True)
        if attrs :
            d ['attributes'] = attrs
        res = ps (self.base_dn, filter, **d)
        for r in res :
            yield (LDAP_Search_Result (r))
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
        found = {}
        new_contacts = []
        for type in self.attr_map ['user_contact'] :
            lds = self.attr_map ['user_contact'][type]
            tid = self.db.uc_type.lookup (type)
            order = 1
            for ld in lds :
                if ld not in luser :
                    continue
                for ldit in luser [ld] :
                    key = (type, ldit)
                    if key in oldmap :
                        n = oldmap [key]
                        new_contacts.append (n.id)
                        if n.order != order and self.update_roundup :
                            self.db.user_contact.set (n.id, order = order)
                            changed = True
                        del oldmap [key]
                        found [key] = 1
                    elif key in found :
                        self.log.error ("Duplicate: %s" % ':'.join (key))
                        continue
                    elif self.update_roundup :
                        d = dict \
                            ( contact_type = tid
                            , contact      = ldit
                            , order        = order
                            )
                        # If we have the user id at this point add it
                        if user :
                            d ['user'] = user.id
                        id = self.db.user_contact.create (** d)
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
                    return False
                raise ValueError ("User without domain: %s" % username)
            dom = username.split ('@', 1) [1]
            if dom not in self.ad_domain :
                raise ValueError ("User with invalid domain: %s" % username)
        return True
    # end def domain_user_check

    def sync_user_from_ldap (self, username, update = None) :
        assert '\\' not in username

        luser = self.get_ldap_user_by_username (username)
        if luser :
            guid = luser.objectGUID.raw_values [0]
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
            # Try with full username and with username without domain
            for u in (username, username.split ('@') [0]) :
                try :
                    uid   = self.db.user.lookup  (u)
                    break
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
                self.log.info ("Obsolete: %s" % username)
                if self.update_roundup :
                    self.db.user.set (uid, status = self.status_obsolete)
                changed = True
        else :
            d = {}
            for k in self.attr_map ['user'] :
                lk, x, method, em = self.attr_map ['user'][k]
                if method :
                    v = method (luser, lk)
                    if v or em :
                        d [k] = v
            if self.contact_types :
                self.sync_contacts_from_ldap (luser, user, d)
            new_status_id = self.member_status_id (luser.dn)
            assert (new_status_id)
            new_status = self.db.user_status.getnode (new_status_id)
            roles = new_status.roles
            if not roles :
                roles = self.db.config.NEW_WEB_USER_ROLES
            if user :
                assert (user.status in self.status_sync)
                # dict changes during iteration, use items here
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
                    self.log.info ("Update roundup: %s" % username, d)
                    if self.update_roundup :
                        self.db.user.set (uid, ** d)
                        changed = True
            else :
                assert (d)
                d ['roles']  = roles
                d ['status'] = new_status_id
                if 'username' not in d :
                    d ['username'] = username
                self.log.info ("Create roundup user: %s" % username, d)
                if self.update_roundup :
                    uid = self.db.user.create (** d)
                    changed = True
                    # Perform user creation magic for new user
                    if 'org_location' in self.db.classes :
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
                        self.log.info \
                            ( "Dynamic user create magic: %s, "
                              "org_location: %s, department: %s"
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
                self.log.info \
                    ("%s: Inserting: %s (%s)" % (user.username, p, ins))
                modlist.append ((ldap3.MODIFY_ADD, p, ins))
            elif len (luser [p]) != 1 :
                self.log.error ("%s: invalid length: %s" % (user.username, p))
            else :
                ldattr = luser [p][0]
                ins = cs [0]
                if not s and ct.lower () not in self.single_ldap_attributes :
                    ins = cs
                if ldattr != ins and [ldattr] != ins :
                    self.log.info \
                        ( "%s:  Updating: %s/%s %s/%s"
                        % (user.username, ct, p, ins, ldattr)
                        )
                    modlist.append ((ldap3.MODIFY_REPLACE, p, ins))
            if s :
                if s not in luser :
                    if cs [1:] :
                        self.log.info \
                            ( "%s: Inserting: %s (%s)" \
                            % (user.username, s, cs [1:])
                            )
                        modlist.append ((ldap3.MODIFY_ADD, s, cs [1:]))
                else :
                    if luser [s] != cs [1:] :
                        self.log.info \
                            ( "%s:  Updating: %s/%s %s/%s"
                            % (user.username, ct, s, cs [1:], ldattr)
                            )
                        modlist.append ((ldap3.MODIFY_REPLACE, s, cs [1:]))
        for ct, fields in self.attr_map ['user_contact'].iteritems () :
            if ct not in contacts :
                for f in fields :
                    if f in luser :
                        self.log.info \
                            ("%s:  Deleting: %s" % (user.username, f))
                        modlist.append ((ldap3.MODIFY_REPLACE, f, []))
    # end def sync_contacts_to_ldap

    def sync_user_to_ldap (self, username, update = None) :
        if update is not None :
            self.update_ldap = update
        allow_empty = False
        if not self.update_ldap :
            allow_empty = True
        check = self.domain_user_check (username, allow_empty = allow_empty)
        # Do nothing if empty domain and we would require one and we
        # don't update anyway
        if not check :
            self.log.info \
                ("Not syncing user with empty domain: %s" % user.username)
            return
        uid  = self.db.user.lookup (username)
        user = self.db.user.getnode (uid)
        assert (user.status in self.status_sync)
        luser = self.get_ldap_user_by_username (user.username)
        if not luser :
            self.log.info ("LDAP user not found:", user.username)
            # Might want to create user in LDAP
            return
        if user.status == self.status_obsolete :
            if not self.is_obsolete (luser) :
                self.log.info ("Roundup user obsolete:", user.username)
                # Might want to move user in LDAP Tree
            return
        if self.is_obsolete (luser) :
            self.log.info ("Obsolete LDAP user: %s" % user.username)
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
                    self.log.error \
                        ( "%s: Picture too large: %s" \
                        % (user.username, len (rupattr))
                        )
                    continue
            if rk == 'guid' :
                prupattr = repr (rupattr)
            if lk not in luser :
                if user [rk] :
                    self.log.info \
                        ( "%s: Inserting: %s (%s)" \
                        % (user.username, lk, prupattr)
                        )
                    assert (change)
                    modlist.append ((ldap3.MODIFY_ADD, lk, rupattr))
            elif len (luser [lk]) != 1 :
                self.log.error ("%s: invalid length: %s" % (user.username, lk))
            else :
                ldattr = pldattr = luser [lk][0]
                if rk == 'pictures' :
                    pldattr = '<suppressed>'
                if rk == 'guid' :
                    pldattr = repr (ldattr)
                if ldattr != rupattr :
                    if not change :
                        self.log.info \
                            ( "%s:  attribute differs: %s/%s >%s/%s<"
                            % (user.username, rk, lk, prupattr, pldattr)
                            )
                    else :
                        self.log.info \
                            ( "%s:  Updating: %s/%s >%s/%s<"
                            % (user.username, rk, lk, prupattr, pldattr)
                            )
                        op = ldap3.MODIFY_REPLACE
                        if rupattr is None :
                            op = ldap3.MODIFY_DELETE
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
                            self.log.info \
                                ( "%s:  Updating: %s.%s/%s >%s/%s<"
                                % ( user.username
                                  , udprop
                                  , prop
                                  , lk
                                  , chg [2]
                                  , ldattr
                                  )
                                )
                            modlist.append (chg)
        if self.contact_types :
            self.sync_contacts_to_ldap (user, luser, modlist)
        if modlist and self.update_ldap :
            # Make a dictionary from modlist as required by ldap3
            moddict = {}
            for op, lk, attr in modlist :
                if attr not in modlist :
                    modlist [attr] = []
                moddict [attr].append ((op, lk))
            self.ldcon.modify (luser.dn, moddict)
        elif modlist :
            self.log.info \
                ( 'No LDAP updates performed for user: "%s" with attributes: %s'
                % (user.username, modlist)
                )
    # end def sync_user_to_ldap

    def set_user_dynamic_prop (self, user, udprop, linkprop, lk, ldattr) :
        """ Sync transitive dynamic user properties to ldap
            Gets the user to sync, the linkclass, one of (sap_cc,
            department, org_location), the linkprop (property of the
            given class), the LDAP attribute key lk and the ldap
            attribute value ldattr.
            Return a triple (ldap3.<action>, lk, rupattr)
            where action is one of MODIFY_ADD, MODIFY_REPLACE, MODIFY_DELETE
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
                        return (ldap3.MODIFY_ADD, lk, node [linkprop])
                    else :
                        return (ldap3.MODIFY_REPLACE, lk, node [linkprop])
        if is_empty and ldattr != '' :
            if ldattr is None :
                return None
            else :
                return (ldap3.MODIFY_DELETE, lk, None)
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
            except (Exception, Reject) :
                self.log.error ("Error synchronizing user %s" % username)
                self.log_exception ()
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
            except (Exception, Reject) :
                self.log.error ("Error synchronizing user %s" % username)
                self.log_exception ()
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
        if  ( common.user_has_role
                (self.db, self.client.userid, 'admin', 'sub-login')
            ) :
            if not user :
                raise exceptions.LoginError (self._ ('Invalid login'))
            if user.status == invalid :
                raise exceptions.LoginError (self._ ('Invalid login'))
            self.client.userid = user.id
        elif self.try_ldap () :
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
