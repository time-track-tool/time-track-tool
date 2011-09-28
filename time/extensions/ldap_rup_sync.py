#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

try :
    from ldap_sync import LdapLoginAction, LDAP_Roundup_Sync
    from ldap_sync import check_ldap_config, sync_from_ldap

    def init (instance) :
        instance.registerAction ('login',             LdapLoginAction)
        instance.registerUtil   ('LDAP_Roundup_Sync', LDAP_Roundup_Sync)
        instance.registerUtil   ('check_ldap_config', check_ldap_config)
        instance.registerUtil   ('sync_from_ldap',    sync_from_ldap)
    # end def init
except ImportError :
    def init (instance) :
        instance.registerUtil ('sync_from_ldap', None)
