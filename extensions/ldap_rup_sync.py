#!/usr/bin/python

try :
    from ldap_sync import LdapLoginAction, LDAP_Roundup_Sync
    from ldap_sync import check_ldap_config, sync_from_ldap

    def sync_from_ldap_util (context, db, username) :
        """ Called from templating mechanism
            We re-open the db as the admin user to ensure that logs do
            not contain the currently logged-in user as the actor.
        """
        rdb = db._db
        uid = rdb.getuid ()
        dbusername = rdb.user.get (uid, 'username')
        if uid != '1' :
            client = db._client
            client.opendb ('admin')
            rdb = client.db
        sync_from_ldap (rdb, username)
        db._db.commit ()
        if uid != '1' :
            client.opendb (dbusername)
    # end def sync_from_ldap_util

    def init (instance) :
        instance.registerUtil   ('check_ldap_config', check_ldap_config)
	if not check_ldap_config (instance) :
	    instance.registerUtil ('sync_from_ldap', None)
	    return
        instance.registerAction ('login',             LdapLoginAction)
        instance.registerUtil   ('LDAP_Roundup_Sync', LDAP_Roundup_Sync)
        instance.registerUtil   ('sync_from_ldap',    sync_from_ldap_util)
    # end def init
except ImportError :
    def check_ldap_config (*args, **kw) :
        return False
    def init (instance) :
        instance.registerUtil ('sync_from_ldap',    None)
        instance.registerUtil ('check_ldap_config', check_ldap_config)
