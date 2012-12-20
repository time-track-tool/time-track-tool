#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

try :
    from imap_sync import ImapLoginAction check_imap_config

    def init (instance) :
	if not check_imap_config (instance) :
	    return
        instance.registerAction ('login', ImapLoginAction)
    # end def init
except ImportError :
    def init (instance) :
        pass
    # end def init
