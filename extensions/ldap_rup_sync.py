#!/usr/bin/python

try :
    from ldap_sync import LdapLoginAction, LDAP_Roundup_Sync
    from ldap_sync import check_ldap_config, config_read_boolean, sync_from_ldap

    def sync_from_ldap_util (context, db, username) :
        """ Called from templating mechanism
            We re-open the db as the admin user to ensure that logs do
            not contain the currently logged-in user as the actor.
        """
        user_html_template_update_roundup = config_read_boolean \
            (db.config.ext, "LDAP_USER_HTML_TEMPLATE_UPDATE_ROUNDUP")
        # return if user update for html template is deactivated in the config
        if not user_html_template_update_roundup :
            return
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
