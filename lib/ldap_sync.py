#!/usr/bin/python
from __future__ import print_function
import sys
import logging
import ldap3
import user_dynamic
import common
import io

from copy                import copy
from ldap3.utils.conv    import escape_bytes
from rsclib.autosuper    import autosuper
from rsclib.execute      import Log
from roundup.date        import Date
from roundup.cgi.actions import LoginAction
from roundup.cgi         import exceptions
from roundup.exceptions  import Reject
from datetime            import datetime
from PIL                 import Image

LDAPCursorError = ldap3.core.exceptions.LDAPCursorError
LDAPKeyError    = ldap3.core.exceptions.LDAPKeyError

class Pic :

    def __init__ (self, fileobj) :
        self.b = b = fileobj.binary_content
        self.len   = len (b)
        self.img   = Image.open (io.BytesIO (b))
    # end def __init__

    def resized_picture (self, size) :
        if self.len <= size :
            return self.b
        #print (self.img.getbbox ())
        x1, y1, x2, y2 = self.img.getbbox ()
        #self.img.show ()
        bb = self.img.getbbox ()
        u  = ((bb [2] - bb [0]), (bb [3] - bb [1]))
        l  = (0, 0)
        im = None
        for divide in range (10) :
            middle = ((u [0] + l [0]) // 2, (u [1] + l [1]) // 2)
            if middle == l :
                break
            imn    = self.img.resize (middle)
            picio  = io.BytesIO ()
            imn.save (picio, format = self.img.format)
            sz     = len (picio.getvalue ())
            #print (size, sz)
            if sz <= size :
                l  = middle
                im = imn
                sv = picio.getvalue ()
            else :
                u = middle
        #im.show ()
        #print (im.getbbox ())
        return sv
    # end def resized_picture

# end class Pic

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
            raise KeyError (name)
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
        try :
            self.dn = val.entry_dn
        except AttributeError :
            # When iterating via paged_search we get something different, make
            # it look the same
            self.dn  = val ['dn']
            self.val = val ['attributes']
        dn = ldap3.utils.dn.parse_dn (self.dn.lower ())
        self.ou  = dict.fromkeys (k [1] for k in dn if k [0] == 'ou')
    # end def __init__

    @property
    def is_obsolete (self) :
        for i in self.ou_obsolete :
            if i in self.ou :
                return True
        return False
    # end def is_obsolete

    def raw_value (self, name) :
        return self.val [name].raw_values [0]
    # end def raw_value

    def value (self, name) :
        if isinstance (self.val [name], ldap3.abstract.attribute.Attribute) :
            return self.val [name].value
        return self.val [name]
    # end def value

    def get (self, name, default = None) :
        try :
            return self.value (name)
        except (KeyError, LDAPCursorError, LDAPKeyError) :
            return default
    # end def get

    def __getitem__ (self, name) :
        try :
            return self.val [name]
        except (LDAPCursorError, LDAPKeyError, KeyError) as err :
            raise KeyError (str (err))
    # end def __getitem__

    def __getattr__ (self, name) :
        try :
            return self.val [name]
        except (LDAPCursorError, LDAPKeyError, KeyError) as err :
            raise AttributeError (str (err))
    # end def __getattr__

    def __contains__ (self, name) :
        try :
            x = self.val [name]
            return True
        except (LDAPCursorError, LDAPKeyError, KeyError) as err :
            pass
        return False
    # end def __contains__

# end class LDAP_Search_Result

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
    assert attr == 'objectGUID'
    guid = luser.raw_value ('objectGUID')
    if guid is not None :
        return tohex (guid)
    return None
# end def get_guid

class Config_Entry :

    def __str__ (self) :
        s = []
        for a in self.attrs :
            s.append ('%s: %%(%s)s' % (a, a))
        return ', '.join (s) % self.__dict__
    # end def __str__
    __repr__ = __str__

# end class Config_Entry

class User_Sync_Config_Entry (Config_Entry) :
    """ Configuration of LDAP <-> Roundup Sync (by roundup property)
        name:           is the name in ldap
        do_change:      is 0 for no change to ldap, 1 for change or a
                        method for conversion from roundup to ldap when
                        syncing
        to_roundup:     is an conversion function from ldap to roundup
                        or None if not syncing to roundup
        empty_allowed:  indicates if updates coming from ldap may be
                        empty, currently used only for nickname (aka
                        initials in ldap) and room
        from_vie_user:  tells us if the parameter in roundup comes from
                        a linked vie_user_ml (True) or from the original
                        user (False)
        creation_only:  tells us if we do the update ldap->roundup in
                        all cases (False) or only on creation (True),
                        see to_roundup above.
        write_vie_user: tells us if we write to the user if it has a
                        vie_user_ml link. This keeps it consistent with
                        the linked_from user.
    """

    attrs = ( 'name', 'do_change', 'to_roundup', 'empty_allowed'
            , 'from_vie_user', 'creation_only', 'write_vie_user'
            )

    def __init__ \
        ( self
        , name
        , do_change
        , to_roundup
        , empty_allowed
        , from_vie_user
        , creation_only
        , write_vie_user
        ) :
        self.name           = name
        self.do_change      = do_change
        self.to_roundup     = to_roundup
        self.empty_allowed  = empty_allowed
        self.from_vie_user  = from_vie_user
        self.creation_only  = creation_only
        self.write_vie_user = write_vie_user
    # end def __init__

# end class User_Sync_Config_Entry

class Usercontact_Sync_Config_Entry (Config_Entry) :
    """ Configuration of user contact sync
        sync_vie_user:  a flag that tells us if users that have a
                        vie_user set should be synced *to* LDAP.
        keep_attribute: a flag that tells us if we keep attributes that
                        are not in LDAP, this is only done if there are
                        only single-valued attributes in LDAP, it's a
                        config error if the flag is set and the
                        following list contains multi-valued attributes.
        attributes:     a list of attributes in LDAP, if there are two,
                        the first one is a single-value attribute and
                        the second is a multi-value attribute that takes
                        additional values from roundup.
    """

    attrs = ( 'sync_vie_user', 'keep_attribute', 'attributes')

    def __init__ \
        ( self
        , sync_vie_user
        , keep_attribute
        , attributes
        ) :
        self.sync_vie_user  = sync_vie_user
        self.keep_attribute = keep_attribute
        self.attributes     = attributes
    # end def __init__

# end class Usercontact_Sync_Config_Entry

class Userdynamic_Sync_Config_Entry (Config_Entry) :
    """ Items to be synced from current user_dynamic record.
        Currently this is one-way, only from roundup to ldap.
        Except for creation: If a new user is created and the
        org_location and department properties exist in ldap we perform
        the user_create_magic.
        The entries inside the sub-properties 'sap_cc', 'org_location'
        are as follows:
        One entry for each transitive property to be synced to LDAP
        name:         is the property name of the linked item (in our
                      case from sap_cc, org_location)
        ldap_prop:    is the LDAP property
        from_roundup: is the function to convert roundup->LDAP
        to_roundup:   is the function to convert LDAP->roundup this is
                      currently unused, we don't sync to roundup
    """

    attrs = ( 'name', 'ldap_prop', 'from_roundup', 'to_roundup')

    def __init__ \
        ( self
        , name
        , ldap_prop
        , from_roundup
        , to_roundup
        ) :
        self.name         = name
        self.ldap_prop    = ldap_prop
        self.from_roundup = from_roundup
        self.to_roundup   = to_roundup
    # end def __init__

# end class Userdynamic_Sync_Config_Entry

class LDAP_Roundup_Sync (Log) :
    """ Sync users from LDAP to Roundup """

    page_size     = 50

    def __init__ \
        (self, db, update_roundup = None, update_ldap = None, verbose = 0) :
        self.db             = db
        self.cfg            = db.config.ext
        self.verbose        = verbose
        self.update_ldap    = update_ldap
        self.update_roundup = update_roundup
        self.ad_domain      = self.cfg.LDAP_AD_DOMAINS.split (',')
        self.objectclass    = getattr (self.cfg, 'LDAP_OBJECTCLASS', 'person')
        self.base_dn        = self.cfg.LDAP_BASE_DN
        self.__super.__init__ ()

        # If verbose is set, add logging to stderr in addition to syslog
        if self.verbose :
            formatter = logging.Formatter \
                ('%(asctime)s - %(name)s - %(funcName)20s() - %(levelname)s - %(message)s')
            handler = logging.StreamHandler (sys.stderr)
            level   = logging.INFO
            if self.verbose > 1 :
                level = logging.DEBUG
            handler.setLevel (level)
            handler.setFormatter (formatter)
            self.log.addHandler (handler)

        self.log.info ("User sync started")
        self.log.info ("Read sync config")
        self.dn_allowed = {}
        varname = 'allowed_dn_suffix_by_domain'
        dn_allowed = getattr (self.cfg, 'LDAP_' + varname.upper (), None)
        if dn_allowed :
            for kv in dn_allowed.split (';') :
                k, v = (x.lower () for x in kv.split (':', 1))
                if k not in self.dn_allowed :
                    self.dn_allowed [k] = {}
                self.dn_allowed [k][v] = True
        if not self.dn_allowed :
            self.log.error \
                ('No allowed DN suffix configured for vie_user, '
                 'use "%s" in [ldap] section of ext config' % varname
                )

        self.debug (4, 'Read sync direction config')
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
            self.log.debug ("%s: %s" % (k, getattr (self, k)))

        self.log.info ('Connect to LDAP: %s' % self.cfg.LDAP_URI )
        self.server = ldap3.Server (self.cfg.LDAP_URI, get_info = ldap3.ALL)
        self.debug (4, 'Server')
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
        # Double negation because we want the default to be *with* starttls
        no_starttls = getattr (self.db.config.ext, 'LDAP_NO_STARTTLS', False)
        if not no_starttls :
            self.ldcon.start_tls ()
        self.log.debug ('TLS: %s' % (not no_starttls))
        self.ldcon.bind      ()
        self.debug (4, 'Bind')
        self.schema = self.server.schema

        self.valid_stati     = []
        self.status_obsolete = db.user_status.lookup ('obsolete')
        self.status_sync     = [self.status_obsolete]
        self.ldap_stati      = {}
        self.ldap_groups     = {}
        # read ldap groups from user_status in Roundup to specify which
        # LDAP groups to look for
        for id in db.user_status.filter (None, {}, sort = ('+', 'id')) :
            st = db.user_status.getnode (id)
            if st.ldap_group :
                self.log.info ("Add group '%s' for user lookup"
                    % st.ldap_group)
                self.status_sync.append (id)
                self.valid_stati.append (id)
                self.ldap_stati  [id] = st
                self.ldap_groups [id] = LDAP_Group \
                    (self.ldcon, self.base_dn, st.ldap_group, st.ldap_prio)
        self.contact_types = {}
        # uc_type = user_contact_type
        if 'uc_type' in self.db.classes :
            self.contact_types = dict \
                ((id, self.db.uc_type.get (id, 'name'))
                 for id in self.db.uc_type.list ()
                )
        self.compute_attr_map ()
    # end def __init__

    def debug (self, prio, *args, **kw) :
        if self.verbose >= prio :
            self.log.debug (*args, **kw)
    # end debug

    def bind_as_user (self, username, password) :
        luser = self.get_ldap_user_by_username (username)
        if not luser :
            return None
        if not self.ldcon.rebind (user = luser.dn, password = password) :
            self.log.error ('Error binding as %s' % luser.dn)
            return None
        self.log.debug ('Successful bind by %s' % luser.dn)
        return True
    # end def bind_as_user

    def get_cn (self, user, attr) :
        """ Get the common name of this user
            Note that this defaults to realname but will add ' (External)'
            if the 'group_external' flag in contract_type exists and is set.
        """
        assert attr == 'realname'
        # Don't asume we have a realname. Some users don't.
        rn = ''
        if user.firstname and user.lastname :
            rn = ' '.join ((user.firstname, user.lastname))
        elif user.firstname :
            rn = user.firstname
        elif user.lastname :
            rn = user.lastname
        else :
            rn = user.realname
        assert (rn)
        dyn = self.get_dynamic_user (user.id)
        # check for group external flag in contract type and mark external
        # users in CN attribute with additional suffix
        if dyn and dyn.contract_type :
            ct = self.db.contract_type.getnode (dyn.contract_type)
            if ct.group_external :
                rn = rn + ' (External)'
        return rn
    # end def get_cn

    def truncate_department (self, department):
        AD_MAX_LENGTH_DEPARTMENT = 64
        if department and len (department) > AD_MAX_LENGTH_DEPARTMENT :
            department_trunc = department [0:AD_MAX_LENGTH_DEPARTMENT]
            self.log.warning ("Cutting of department string to %s"
                " chars to fit AD: '%s' -> '%s'" %
                (AD_MAX_LENGTH_DEPARTMENT, department, department_trunc))
            department = department_trunc
        return department

    def get_department (self, user, attr) :
        if user.department_temp :
            return self.truncate_department (user.department_temp)
        dyn = self.get_dynamic_user (user.id)
        if dyn :
            dyn_d = self.db.department.get (dyn.department, 'name')
            return self.truncate_department (dyn_d)
    # end def get_department

    def get_name (self, user, attr) :
        """ Get name from roundup user class Link attr """
        if user [attr] is None :
            return None
        cl = user.cl.db.classes [attr]
        return cl.get (user [attr], 'name')
    # end def get_name

    def get_picture (self, user, attr, max_size = 102400) :
        """ Get picture from roundup user class
            and reduce to given max_size
        """
        pics = [self.db.file.getnode (i) for i in user.pictures]
        for p in sorted (pics, reverse = True, key = lambda x : x.activity) :
            pic = Pic (p)
            return pic.resized_picture (max_size)
    # end def get_picture

    def get_realname (self, x, y) :
        fn = x.get ('givenname', '')
        ln = x.get ('sn', '')
        if fn and ln :
            return ' '.join ((fn, ln))
        elif fn :
            return fn
        return ln
    # end def get_realname

    def get_username_attribute_dn (self, node, attribute) :
        """ Get dn of a user Link-attribute of a node """
        s = node [attribute]
        if not s :
            return s
        n = self.db.user.getnode (s)
        if n.vie_user :
            n = self.db.user.getnode (n.vie_user)
        s = n.username
        r = self.get_ldap_user_by_username (s)
        if r is None :
            return None
        return r.dn
    # end def get_username_attribute_dn

    def allow_sync_user (self, roundup_attribute, ldap_attribute = None) :
        if  (   roundup_attribute not in self.user_props
            and roundup_attribute not in self.dynprops
            ) :
            return False
        if roundup_attribute in self.dontsync_rup :
            return False
        if ldap_attribute is not None and ldap_attribute in self.dontsync_ldap :
            return False
        return True
    # end def allow_sync_user

    def append_sync_attribute (self, key = 'user', **kw) :
        if key not in self.attr_map :
            self.attr_map [key] = {}
        attr_u = self.attr_map [key]
        for k in kw :
            if k not in attr_u :
                attr_u [k] = []
            attr_u [k].append (kw [k])
    # end def append_sync_attribute

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
        name = 'LDAP_DO_NOT_SYNC_ROUNDUP_PROPERTIES'
        dontsync_rup = getattr (self.cfg, name, '')
        if dontsync_rup :
            dontsync_rup = dict.fromkeys (dontsync_rup.split (','))
        else :
            dontsync_rup = {}
        self.log.info \
            ( "Exclude the following Roundup attributes from sync: %s"
            % dontsync_rup.keys ()
            )
        self.dontsync_rup = dontsync_rup
        name = 'LDAP_DO_NOT_SYNC_LDAP_PROPERTIES'
        dontsync_ldap = getattr (self.cfg, name, '')
        if dontsync_ldap :
            dontsync_ldap = dict.fromkeys (dontsync_ldap.split (','))
        else :
            dontsync_ldap = {}
        self.log.info \
            ( "Exclude the following LDAP attributes from sync: %s"
            % dontsync_ldap.keys ()
            )
        self.dontsync_ldap = dontsync_ldap
        attr_map = self.attr_map = dict ()
        self.user_props = props = self.db.user.properties
        self.dynprops = {}
        if 'user_dynamic' in self.db.classes :
            self.dynprops = self.db.user_dynamic.properties
        self.append_sync_attribute \
            (id = User_Sync_Config_Entry
                ( name           = 'employeenumber'
                , do_change      = 1
                , to_roundup     = None
                , empty_allowed  = False
                , from_vie_user  = False
                , creation_only  = True
                , write_vie_user = False
                )
            )
        if 'firstname' in props :
            self.append_sync_attribute \
                ( firstname = User_Sync_Config_Entry
                    ( name = 'givenname'
                    , do_change      = 1
                    , to_roundup     = lambda x, y : x.get (y, None)
                    , empty_allowed  = False
                    , from_vie_user  = True
                    , creation_only  =
                        (  self.update_ldap
                        or not self.allow_sync_user ('firstname', 'givenname')
                        )
                    , write_vie_user = False # Done directly
                    )
                )
        if self.update_ldap and self.allow_sync_user ('realname', 'cn') :
            # Note that cn is a special case: First of all the CN (i.e. RDN)
            # is part of the DN and we need to call modify_dn instead of
            # a simple modify call. In addition we also need to
            # modify the displayname. See code that checks for update
            # of CN -> sync_user_to_ldap()
            # But it seems the displayname is not changed if we
            # explicitly write it (and there is no error message either)
            # so it may well be that the displayname is magic and
            # follows the cn setting.
            self.append_sync_attribute \
                ( realname = User_Sync_Config_Entry
                    ( name           = 'cn'
                    , do_change      = self.get_cn
                    , to_roundup     = None
                    , empty_allowed  = False
                    , from_vie_user  = True
                    , creation_only  = True
                    , write_vie_user = False
                    )
                )
        if 'lastname' in props :
            self.append_sync_attribute \
                ( lastname = User_Sync_Config_Entry
                    ( name           = 'sn'
                    , do_change      = 1
                    , to_roundup     = lambda x, y : x.get (y, None)
                    , empty_allowed  = False
                    , from_vie_user  = True
                    , creation_only  =
                        (  self.update_ldap
                        or not self.allow_sync_user ('lastname', 'sn')
                        )
                    , write_vie_user = False # Done directly
                    )
                )
        if self.allow_sync_user ('nickname', 'initials') :
            self.append_sync_attribute \
                ( nickname = User_Sync_Config_Entry
                    ( name           = 'initials'
                    , do_change      = lambda x, y : (x [y] or '').upper ()
                    , to_roundup     = lambda x, y : str (x.get (y, '')).lower()
                    , empty_allowed  = True
                    , from_vie_user  = False
                    , creation_only  = self.update_ldap
                    , write_vie_user = False
                    )
                )
        if self.allow_sync_user ('ad_domain', 'UserPrincipalName') :
            self.append_sync_attribute \
                ( ad_domain = User_Sync_Config_Entry
                    ( name           = 'UserPrincipalName'
                    , do_change      = 0
                    , to_roundup     =
                        lambda x, y : str (x [y]).split ('@', 1)[1]
                    , empty_allowed  = False
                    , from_vie_user  = False
                    , creation_only  = False
                    , write_vie_user = False
                    )
                )
        if 'username' in props :
            self.append_sync_attribute \
                ( username = User_Sync_Config_Entry
                    ( name           = 'UserPrincipalName'
                    , do_change      = 0
                    , to_roundup     = lambda x, y : str (x.get (y))
                    , empty_allowed  = False
                    , from_vie_user  = False
                    , creation_only  = not self.allow_sync_user \
                        ('username', 'UserPrincipalName')
                    , write_vie_user = False
                    )
                )
        if self.allow_sync_user ('pictures', 'thumbnailPhoto') :
            self.append_sync_attribute \
                ( pictures = User_Sync_Config_Entry
                    ( name           = 'thumbnailPhoto'
                    , do_change      = self.get_picture
                    , to_roundup     = None # was: self.ldap_picture
                    , empty_allowed  = False
                    , from_vie_user  = True
                    , creation_only  = True
                    , write_vie_user = True
                    )
                )
        if self.allow_sync_user ('position_text', 'title') :
            # We sync that field *to* ldap but not *from* ldap.
            self.append_sync_attribute \
                ( position_text = User_Sync_Config_Entry
                    ( name           = 'title'
                    , do_change      = 1
                    , to_roundup     = None
                    , empty_allowed  = False
                    , from_vie_user  = True
                    , creation_only  = True
                    , write_vie_user = True
                    )
                )
        if self.allow_sync_user ('realname', 'cn') and 'firstname' not in props:
            self.append_sync_attribute \
                ( realname = User_Sync_Config_Entry
                    ( name           = 'cn'
                    , do_change      = 0
                    , to_roundup     = self.get_realname
                    , empty_allowed  = False
                    , from_vie_user  = False
                    , creation_only  = False
                    , write_vie_user = False
                    )
                )
        if self.allow_sync_user ('room', 'physicalDeliveryOfficeName') :
            self.append_sync_attribute \
                ( room = User_Sync_Config_Entry
                    ( name           = 'physicalDeliveryOfficeName'
                    , do_change      = self.get_name
                    , to_roundup     = self.cls_lookup (self.db.room)
                    , empty_allowed  = True
                    , from_vie_user  = True
                    , creation_only  = self.update_ldap
                    , write_vie_user = True
                    )
                )
        if self.allow_sync_user ('substitute', 'secretary') :
            self.append_sync_attribute \
                ( substitute = User_Sync_Config_Entry
                    ( name           = 'secretary'
                    , do_change      = self.get_username_attribute_dn
                    , to_roundup     = (self.get_roundup_uid_from_dn_attr)
                    , empty_allowed  = False
                    , from_vie_user  = True
                    , creation_only  = self.update_ldap
                    , write_vie_user = True
                    )
                )
        if self.allow_sync_user ('supervisor', 'manager') :
            self.append_sync_attribute \
                ( supervisor = User_Sync_Config_Entry
                    ( name           = 'manager'
                    , do_change      = self.get_username_attribute_dn
                    , to_roundup     = (self.get_roundup_uid_from_dn_attr)
                    , empty_allowed  = False
                    , from_vie_user  = True
                    , creation_only  = self.update_ldap
                    , write_vie_user = True
                    )
                )
        # This should probably never be excluded as the guid is the key
        # to syncing users
        if self.allow_sync_user ('guid', 'objectGUID') :
            self.append_sync_attribute \
                ( guid = User_Sync_Config_Entry
                    ( name           = 'objectGUID'
                    , do_change      = None
                    , to_roundup     = get_guid
                    , empty_allowed  = False
                    , from_vie_user  = False
                    , creation_only  = True
                    , write_vie_user = False
                    )
                )
        if  (   self.allow_sync_user ('department_temp', 'department')
            and self.allow_sync_user ('department', 'department')
            ) :
            self.append_sync_attribute \
                ( department_temp = User_Sync_Config_Entry
                    ( name           = 'department'
                    , do_change      = self.get_department
                    , to_roundup     = None
                    , empty_allowed  = False
                    , from_vie_user  = True
                    , creation_only  = True
                    , write_vie_user = False
                    )
                )
        if self.allow_sync_user ('org_location', 'company') :
            self.append_sync_attribute \
                ( key = 'user_dynamic'
                , org_location = Userdynamic_Sync_Config_Entry
                    ( name         = 'name'
                    , ldap_prop    = 'company'
                    , from_roundup = self.set_user_dynamic_prop
                    , to_roundup   = None
                    )
                )
        if  (   self.allow_sync_user ('sap_cc', 'extensionAttribute3')
            and self.allow_sync_user ('sap_cc', 'extensionAttribute4')
            ) :
            self.append_sync_attribute \
                ( key = 'user_dynamic'
                , sap_cc = Userdynamic_Sync_Config_Entry
                    ( name         = 'name'
                    , ldap_prop    = 'extensionAttribute3'
                    , from_roundup = self.set_user_dynamic_prop
                    , to_roundup   = None
                    )
                )
            self.append_sync_attribute \
                ( key = 'user_dynamic'
                , sap_cc = Userdynamic_Sync_Config_Entry
                    ( name         = 'description'
                    , ldap_prop    = 'extensionAttribute4'
                    , from_roundup = self.set_user_dynamic_prop
                    , to_roundup   = None
                    )
                )
        if self.contact_types :
            d = dict \
                ( key   = 'user_contact'
                , Email          = Usercontact_Sync_Config_Entry
                    (False, False, ('mail',))
                )
            d ['internal Phone'] = Usercontact_Sync_Config_Entry \
                (True,  False, ('otherTelephone',))
            d ['external Phone'] = Usercontact_Sync_Config_Entry \
                (True,  False, ('telephoneNumber',))
            d ['mobile Phone']   = Usercontact_Sync_Config_Entry \
                (True,  False, ('mobile', 'otherMobile'))
            d ['Mobile short']   = Usercontact_Sync_Config_Entry \
                (True,  False, ('pager',  'otherPager'))
            self.append_sync_attribute (**d)
        else :
            self.append_sync_attribute \
                ( address = User_Sync_Config_Entry
                    ( name           = 'mail'
                    , do_change      = 0
                    , to_roundup     = self.set_roundup_email_address
                    , empty_allowed  = False
                    , from_vie_user  = False
                    , creation_only  = False
                    , write_vie_user = False
                    )
                )
    # end def compute_attr_map

    def cls_lookup (self, cls, insert_attr_name = None, params = None) :
        """ Generate a lookup method (non-failing) for the given class.
            Needed for easy check if an LDAP attribute exists as a
            roundup class. We need the roundup class in a closure.
        """
        def look (luser, txt, **dynamic_params) :
            try :
                key = luser [txt]
            except KeyError :
                return None
            try :
                return cls.lookup (key)
            except KeyError :
                pass
            if insert_attr_name :
                n = ''
                if not self.update_roundup :
                    n = ' (deactivated)'
                self.log.info \
                    ("Update Roundup%s: new %s: %s%s" % (n, cls.classname, key))
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

    def is_single_value (self, ldap_attr_name) :
        return self.schema.attribute_types [ldap_attr_name].single_value
    # end def is_single_value

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
                self.debug (3, "Sync user %s due to LDAP group %s"
                    % (dn, g.name))
                return gid
    # end def member_status_id

    def set_roundup_email_address (self, luser, txt) :
        """ Look up email of ldap user and do email processing in case
            roundup is configured for only the standard 'address' and
            'alternate_addresses' attributes. Old email settings are
            retained.
        """
        try :
            mail = luser [txt]
        except KeyError :
            return None
        uid = None
        for k in 'UserPrincipalName', 'uid' :
            try :
                uid = self.db.user.lookup (luser [k])
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
            n = ''
            if not self.update_roundup :
                n = ' (deactivated)'
            self.log.info \
                ( "Update Roundup%s: %s alternate_addresses = %s" \
                % (n, user.username, ','.join (aa.iterkeys ()))
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
            yield (r.userprincipalname)
    # end def get_all_ldap_usernames

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
                return self.db.user.lookup (lsup [k])
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

    def get_dynamic_user (self, uid) :
        """ Get user_dynamic record with the following properties
            - If a record for *now* exists return this one
            - otherwise return the latest record in the past
            - If None exists in the past, try to find one in the future
            - Return None if we didn't find any
        """
        # This already returns the latest record in the past if no
        # current record exists:
        now = Date ('.')
        dyn = user_dynamic.get_user_dynamic (self.db, uid, now)
        if dyn :
            return dyn
        # First record after 'now' or None
        return user_dynamic.first_user_dynamic (self.db, uid, now)
    # end def get_dynamic_user

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
            lpic = luser.raw_value (attr)
        except KeyError :
            return None
        uid = None
        for k in 'UserPrincipalName', 'uid' :
            try :
                uid = self.db.user.lookup (luser [k])
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
        self.debug (3, 'old contacts: %s' % oldmap.keys ())
        found = {}
        new_contacts = []
        for typ in self.attr_map ['user_contact'] :
            # Only a single entry per typ
            synccfg = self.attr_map ['user_contact'][typ][0]
            self.debug (3, 'user_contact config "%s": %s' % (typ, synccfg))
            # Uncomment if we do not update local user with remote contact data
            #if not user or (user.vie_user_ml and synccfg.sync_vie_user) :
            #    continue
            tid = self.db.uc_type.lookup (typ)
            order = 1
            for k, ld in enumerate (synccfg.attributes) :
                if ld not in luser :
                    continue
                l = len (synccfg.attributes)
                if self.is_single_value (ld) :
                    if k == l - 1  and l > 1 :
                        self.log.warn \
                            ('Single-valued attribute is last: %s' % ld)
                elif k < l - 1 :
                    self.log.warn \
                        ('Multi-valued attribute is not last: %s' % ld)
                for ldit in luser [ld] :
                    self.debug (3, "contacts LDAP %s: %s" % (ld, ldit))
                    key = (typ, ldit)
                    if key in oldmap :
                        n = oldmap [key]
                        new_contacts.append (n.id)
                        if n.order != order and self.update_roundup :
                            self.db.user_contact.set (n.id, order = order)
                            changed = True
                        del oldmap [key]
                        found [key] = 1
                        self.debug (3, 'contacts LDAP found: %s' % (key,))
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
        # This used to be a special hard-coded behaviour for emails so
        # that emails not found in LDAP were kept in roundup. This is due
        # to the fact that Active directory has only *one* single-valued
        # attribute for emails.
        order_by_ct = {}
        for k, n in sorted (oldmap.items (), key = lambda x : x [1].order) :
            # Get the contact_type name and look up the ldap attrs
            # Only if keep_attribute is set *and* all the attributes are
            # single-valued do we continue
            ctname = ctypes [n.contact_type]
            # Do not touch non-synced user_contact types
            if ctname not in self.attr_map ['user_contact'] :
                self.debug (3, 'LDAP oldmap %s: add new' % str (k))
                new_contacts.append (n.id)
                del oldmap [k]
                continue
            synccfg = self.attr_map ['user_contact'][ctname][0]
            self.debug (3, 'user_contact config "%s": %s' % (ctname, synccfg))
            if user.vie_user_ml and synccfg.sync_vie_user :
                self.debug (3, 'LDAP oldmap %s: not vie_user' % str (k))
                continue
            if not synccfg.keep_attribute :
                self.debug (3, 'LDAP oldmap %s: not keep' % str (k))
                continue
            is_single = True
            for ld in synccfg.attributes :
                if not self.is_single_value (ld) :
                    # This is a config error. Seems LDAP has changed an
                    # attribute to multi-valued or programmer error.
                    self.log.warn \
                        ("User contact sync %s with keep_attribute set "
                         "has multi-valued attribute %s"
                        % (ctname, ld)
                        )
                    # Correct config to avoid multiple warnings
                    synccfg.keep_attribute = False
                    is_single = False
                    break
            if not is_single :
                self.debug (3, 'LDAP oldmap %s: not single' % str (k))
                continue
            if n.contact_type not in order_by_ct :
                order_by_ct [n.contact_type] = 2
            if n.order != order_by_ct [n.contact_type] and self.update_roundup :
                order = order_by_ct [n.contact_type]
                self.db.user_contact.set (n.id, order = order)
                changed = True
            order_by_ct [n.contact_type] += 1
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
        self.log.info ("Sync user '%s' from LDAP" % username)
        luser = self.get_ldap_user_by_username (username)
        self.debug (3, 'User by username')
        if luser :
            guid = luser.raw_value ('objectGUID')
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
            self.debug (3, 'User by guid')
        # don't modify system users:
        reserved = ('admin', 'anonymous')
        if  (  username in reserved
            or user and user.status not in self.status_sync
            ) :
            self.debug (4, "Skip user %s as this is a reserved username "
                " in Roundup" % username)
            return
        if not user and (not luser or self.is_obsolete (luser)) :
            self.log.info \
                ("Not syncing %s: Not in LDAP or obsolete" % username)
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
            c = {}
            for k in self.attr_map ['user'] :
                for synccfg in self.attr_map ['user'][k] :
                    if synccfg.to_roundup :
                        v = synccfg.to_roundup (luser, synccfg.name)
                        # FIXME: This must change for python3
                        if isinstance (v, unicode) :
                            v = v.encode ('utf-8')
                        if v or synccfg.empty_allowed :
                            if  (   synccfg.creation_only
                                and not synccfg.write_vie_user
                                ) :
                                c [k] = v
                            else :
                                d [k] = v
            self.debug \
                ( 3
                , 'c: %s d: %s, contact_type: %s'
                % (c, d, self.contact_types)
                )
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
                n = ''
                if not self.update_roundup :
                    n = ' (deactivated)'
                if d :
                    self.log.info ("Update Roundup%s: %s %s" % (n, username, d))
                    self.debug (3, 'Before Roundup update')
                    if self.update_roundup :
                        self.db.user.set (uid, ** d)
                        changed = True
                    self.debug (3, 'After Roundup update')
                else:
                    self.log.info (\
                        "Update Roundup%s: %s: No Changes" % (n, username))
            else :
                d.update (c)
                assert (d)
                assert 'lastname'  in d
                assert 'firstname' in d
                d ['roles']  = roles
                d ['status'] = new_status_id
                if 'username' not in d :
                    d ['username'] = username
                self.log.info ("Create Roundup user: %s: %s" % (username, d))
                if self.update_roundup :
                    self.debug (3, 'Before Roundup create')
                    uid = self.db.user.create (** d)
                    self.debug (3, 'After Roundup create')
                    changed = True
                    # Perform user creation magic for new user
                    if 'org_location' in self.db.classes :
                        olo = dep = None
                        if 'company' in luser :
                            olo = luser ['company'].value
                            olo = olo.encode ('utf-8')
                            try :
                                olo = self.db.org_location.lookup (olo)
                            except KeyError :
                                olo = None
                        if 'department' in luser :
                            dep = luser ['department'].value
                            dep = dep.encode ('utf-8')
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
        for ct in contacts :
            cs = contacts [ct]
            if ct not in self.attr_map ['user_contact'] :
                continue
            synccfg = self.attr_map ['user_contact'][ct][0]
            # Only write if allowed
            if not synccfg.sync_vie_user :
                continue
            # Only write if this user has a vie_user (which means it is
            # an external user that may write attributes to ldap)
            if synccfg.sync_vie_user and not user.vie_user :
                continue
            if len (ldn) != 2 :
                assert (len (ldn) == 1)
                p = ldn [0]
                s = None
            else :
                p, s = ldn
            if p not in luser :
                ins = cs [0]
                if not s and not self.is_single_value (p) :
                    ins = cs
                self.log.info \
                    ("%s: Add insertion: %s (%s)" % (user.username, p, ins))
                modlist.append ((ldap3.MODIFY_ADD, p, ins))
            else :
                ldattr = luser [p][0]
                ins    = cs [0]
                if self.is_single_value (p) and len (luser [p]) != 1 :
                    self.log.error \
                        ("%s: invalid length: %s" % (user.username, p))
                if not s and not self.is_single_value (p) :
                    ldattr = luser [p]
                    ins    = cs
                if ldattr != ins and [ldattr] != ins :
                    if not ins :
                        self.log.info \
                            ( "%s: Add deletion: %s -> %s [%s -> %s]"
                            % (user.username, ct, p, ldattr, ins)
                            )
                        modlist.append ((ldap3.MODIFY_DELETE, p, None))
                    else :
                        self.log.info \
                            ( "%s: Add update: %s -> %s [%s -> %s]"
                            % (user.username, ct, p, ldattr, ins)
                            )
                        modlist.append ((ldap3.MODIFY_REPLACE, p, ins))
            if s :
                if s not in luser :
                    if cs [1:] :
                        self.log.info \
                            ( "%s: Add insertion: %s (%s)" \
                            % (user.username, s, cs [1:])
                            )
                        modlist.append ((ldap3.MODIFY_ADD, s, cs [1:]))
                else :
                    if luser [s] != cs [1:] :
                        self.log.info \
                            ( "%s: Add update: %s -> %s [%s -> %s]"
                            % (user.username, ct, s, ldattr, cs [1:])
                            )
                        modlist.append ((ldap3.MODIFY_REPLACE, s, cs [1:]))
        for ct in self.attr_map ['user_contact'] :
            attributes = self.attr_map ['user_contact'][ct][0].attributes
            if ct not in contacts :
                for a in attributes :
                    if a in luser :
                        self.log.info \
                            ("%s: Add deletion: %s" % (user.username, a))
                        modlist.append ((ldap3.MODIFY_REPLACE, a, []))
    # end def sync_contacts_to_ldap

    def sync_user_to_ldap (self, username, update = None) :
        self.log.info ("Sync user '%s' to LDAP" % username )
        if update is not None :
            self.update_ldap = update
        allow_empty = False
        if not self.update_ldap :
            allow_empty = True
        check = self.domain_user_check (username, allow_empty = allow_empty)
        # Do nothing if empty domain and we would require one and we
        # don't update anyway
        if not check :
            self.log.info ("Not syncing user with empty domain: %s" % username)
            return
        uid  = self.db.user.lookup (username)
        user = self.db.user.getnode (uid)
        self.debug (3, 'Before user_by_username')
        luser = self.get_ldap_user_by_username (user.username)
        self.debug (3, 'After user_by_username')
        if not luser :
            self.log.info ("LDAP user not found:", user.username)
            # Might want to create user in LDAP
            return
        r_user = user
        if user.vie_user_ml :
            if user.vie_user_bl_override :
                allowed = user.vie_user_ml
                allowed.append (user.id)
                if user.vie_user_bl_override not in allowed :
                    self.log.error \
                        ( "User %s: invalid user in backlink override: %s"
                        % (user.username, user.vie_user_bl_override)
                        )
                    return
                r_user = self.db.user.getnode (user.vie_user_bl_override)
            elif len (user.vie_user_ml) > 1 :
                self.log.error \
                    ( "More than one user links to user %s: %s"
                    % (user.username
                      , ', '.join
                        (self.db.user.get (u, 'username')
                         for u in user.vie_user_ml)
                      )
                    )
                return
            else :
                assert len (user.vie_user_ml) == 1
                r_user = self.db.user.getnode (user.vie_user_ml [0])
            dom = r_user.ad_domain
            for dn in self.dn_allowed.get (dom, {}) :
                if luser.dn.lower ().endswith (dn) :
                    break
            else :
                self.log.error \
                    ('User has no allowed dn, not syncing: %s' % luser.dn)
                return
        assert (user.status in self.status_sync)
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
        # If we have a vie_user:
        if user.id != r_user.id :
            if self.get_dynamic_user (user.id) :
                self.log.error \
                    ( "ERROR: User %s has a vie_user_ml link "
                      "and a dynamic user record"
                    % user.username
                    )
            dd = {}
            if user.firstname != r_user.firstname :
                dd ['firstname'] = r_user.firstname
            if user.lastname != r_user.lastname :
                dd ['lastname'] = r_user.lastname
            if user.pictures != r_user.pictures :
                dd ['pictures'] = r_user.pictures
            if dd :
                self.log.debug \
                    ("Set vie_user: %s: %s" % (user.username, dd))
                self.db.user.set (user.id, **dd)
                self.db.commit ()
        for rk in sorted (umap) :
            for synccfg in umap [rk] :
                curuser = r_user if synccfg.from_vie_user else user
                rupattr = curuser [rk]
                if rk and callable (synccfg.do_change) :
                    rupattr = synccfg.do_change (curuser, rk)
                prupattr = rupattr
                if rupattr is not None :
                    if rk == 'pictures' :
                        prupattr = '<suppressed: %s>' % len (rupattr)
                    # FIXME: No longer necessary in python3
                    elif isinstance (rupattr, str) :
                        rupattr = rupattr.decode ('utf-8')
                if synccfg.name not in luser :
                    if rupattr :
                        self.log.info \
                            ( "%s: Add insertion: %s (%s)" \
                            % (user.username, synccfg.name, prupattr)
                            )
                        assert (synccfg.do_change)
                        modlist.append \
                            ((ldap3.MODIFY_ADD, synccfg.name, rupattr))
                elif len (luser [synccfg.name]) != 1 :
                    self.log.error \
                        ( "%s: invalid length: %s"
                        % (curuser.username, synccfg.name)
                        )
                else :
                    ldattr = pldattr = luser [synccfg.name]
                    if rk == 'pictures' :
                        pldattr = '<suppressed>'
                    if rk == 'guid' :
                        pldattr = repr (ldattr)
                    if ldattr != rupattr :
                        if synccfg.do_change :
                            self.log.info \
                                ( "%s: Add update: %s -> %s [%s -> %s]"
                                % ( user.username, rk, synccfg.name, pldattr
                                  , prupattr
                                  )
                                )
                            op = ldap3.MODIFY_REPLACE
                            if rupattr is None or rupattr == '':
                                op = ldap3.MODIFY_DELETE
                                rupattr = None
                            # Special case for common name (CN), this needs a
                            # modify_dn call and we also need to modify the
                            # displayname
                            if synccfg.name.lower () == 'cn' :
                                if self.update_ldap :
                                    assert rupattr is not None
                                    # displayname needs to be set, too
                                    modlist.append \
                                        ((op, 'displayname', rupattr))
                                    self.log.info \
                                        ( "%s: Add update: %s -> %s [%s -> %s]"
                                        % ( user.username, rk, 'displayname'
                                          ,luser.displayname, rupattr
                                          )
                                        )
                                    self.log.info \
                                        ("Update LDAP: %s 'MODIFY_DN' "
                                         "(RDN part of DN) "
                                         "['cn=%s' -> 'cn=%s']"
                                        % (user.username, ldattr, rupattr))
                                    self.debug (4, 'Before modify_dn')
                                    self.ldcon.modify_dn \
                                        (luser.dn, 'cn=%s' % rupattr)
                                    self.debug (4, 'After modify_dn')
                                    if self.ldcon.last_error :
                                        # Note: We try to continue if mod of
                                        # DN fails, maybe a permission
                                        # problem and other updates to same
                                        # user go through.
                                        self.log.error \
                                            ( 'Error on modify_dn (set to %s) '
                                            'for %s: %s %s'
                                            % ( rupattr
                                              , luser.dn
                                              , self.ldcon.result['description']
                                              , self.ldcon.result['message']
                                              )
                                            )
                                    else :
                                        # Need to set DN so the future
                                        # updates use the correct DN
                                        rdn, rest = luser.dn.split (',', 1)
                                        nrdn = '='.join (('CN', rupattr))
                                        luser.dn = ','.join ((nrdn, rest))
                                    self.debug \
                                        (3, 'Result: %s' % self.ldcon.result)
                            else :
                                modlist.append ((op, synccfg.name, rupattr))
                        else : # no synccfg.do_change
                            # For comparison we need to convert *from* ldap
                            # Only log a warning if this is *not* correct
                            if synccfg.to_roundup :
                                pldattr = synccfg.to_roundup \
                                    (luser, synccfg.name)
                            if pldattr != prupattr :
                                self.log.debug \
                                    ( "%s: attribute differs: %s/%s >%s/%s<"
                                    % ( user.username, rk, synccfg.name
                                      , prupattr, pldattr
                                      )
                                    )
        if 'user_dynamic' in self.attr_map :
            udmap = self.attr_map ['user_dynamic']
            for udprop in udmap :
                for dynsync in udmap [udprop] :
                    if callable (dynsync.from_roundup) :
                        if dynsync.ldap_prop not in luser :
                            ldattr = None
                        else :
                            ldattr = luser [dynsync.ldap_prop]
                        chg = dynsync.from_roundup \
                            ( r_user
                            , udprop
                            , dynsync.name
                            , dynsync.ldap_prop
                            , ldattr
                            )
                        if chg :
                            self.log.info \
                                ( "%s: Updating: %s.%s -> %s [%s -> %s]"
                                % ( user.username
                                  , udprop
                                  , dynsync.name
                                  , dynsync.ldap_prop
                                  , ldattr
                                  , chg [2]
                                  )
                                )
                            modlist.append (chg)
        if self.contact_types :
            self.debug \
                ( 3
                , "Prepare changes for contacts: %s %s"
                % (user.username, self.contact_types)
                )
            self.sync_contacts_to_ldap (r_user, luser, modlist)
        self.debug (3, 'Modlist before updates: %s' % modlist)
        n = ''
        if not self.update_ldap :
            n = ' (deactivated)'
            # Can produce *huge* output if a picture is updated!
            self.log.info ('Update LDAP%s: %s There are changes but sync is'
                'deactivated' % (n, user.username))
            self.debug (4, 'Update LDAP%s: %s %s' % (n, user.username, modlist))
        if not modlist :
            self.log.info ('Update LDAP%s: %s: No changes' % (n, user.username))
        if modlist and self.update_ldap :
            # Make a dictionary from modlist as required by ldap3
            moddict = {}
            for op, lk, attr in modlist :
                if lk not in moddict :
                    moddict [lk] = []
                if attr is None :
                    attr = []
                if not isinstance (attr, list) :
                    attr = [attr]
                moddict [lk].append ((op, attr))
            logdict = dict (moddict)
            if 'thumbnailPhoto' in logdict :
                logdict ['thumbnailPhoto'] = '<suppressed>'
            self.debug (3, 'modifying Properties for DN: %s' % luser.dn)
            self.debug (3, 'Mod-Dict: %s' % str (logdict))
            self.debug (3, 'Before modify')
            # Can produce *huge* output if a picture is updated!
            self.log.info ("Update LDAP: Apply collected modifications to %s"
                % user.username)
            self.debug (4, 'Update LDAP: %s %s' % (user.username, moddict))
            self.ldcon.modify (luser.dn, moddict)
            self.debug (3, 'After modify')
            self.debug (3, 'Result: %s' % self.ldcon.result)
            if self.ldcon.last_error :
                self.log.error \
                    ( 'Error on modify of user %s: %s %s'
                    % (luser.dn, self.ldcon.result['description'],
                       self.ldcon.result['message'])
                    )
    # end def sync_user_to_ldap

    def set_user_dynamic_prop (self, user, udprop, linkprop, lk, ldattr) :
        """ Sync transitive dynamic user properties to ldap
            Gets the user to sync, the linkclass, one of (sap_cc,
            org_location), the linkprop (property of the
            given class), the LDAP attribute key lk and the ldap
            attribute value ldattr.
            Return a triple (ldap3.<action>, lk, rupattr)
            where action is one of MODIFY_ADD, MODIFY_REPLACE, MODIFY_DELETE
            or None if nothing to sync
        """
        dyn = self.get_dynamic_user (user.id)
        now = Date ('.')
        is_empty = True
        if dyn :
            is_current = \
                (   dyn.valid_from <= now
                and not dyn.valid_to or dyn.valid_to > now
                )
            dynprop = dyn [udprop]
            if dynprop :
                classname = self.db.user_dynamic.properties [udprop].classname
                is_empty  = False
                node      = self.db.getclass (classname).getnode (dynprop)
                val       = node [linkprop]
                # Special case: Add '*' in fron of organisation if dyn
                # user record is not current.
                if udprop == 'org_location' and linkprop == 'name' :
                    if not is_current :
                        val = '*' + val
                # FIXME: Not needed in python3
                if isinstance (val, str) :
                    val = val.decode ('utf-8')
                if val != ldattr :
                    if not ldattr :
                        return (ldap3.MODIFY_ADD, lk, val)
                    else :
                        return (ldap3.MODIFY_REPLACE, lk, val)
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
