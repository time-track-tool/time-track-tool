#!/usr/bin/python

try :
    from imap_sync import ImapLoginAction, check_imap_config

    def init (instance) :
	if not check_imap_config (instance) :
            instance.registerUtil ('imaplogin', False)
	    return
        instance.registerAction ('login', ImapLoginAction)
        instance.registerUtil ('imaplogin', True)
    # end def init
except ImportError :
    def init (instance) :
        instance.registerUtil ('imaplogin', False)
    # end def init
