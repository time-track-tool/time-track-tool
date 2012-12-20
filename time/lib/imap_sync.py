#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys

from imaplib             import IMAP4
from rsclib.autosuper    import autosuper
from roundup.cgi.actions import LoginAction
from roundup.cgi         import exceptions

class IMAP_Roundup_Sync (object) :
    """ Sync users from IMAP to Roundup """

    roundup_group = 'roundup-users'
    page_size     = 50
    
    def __init__ (self, db, imapadr, update_roundup = None) :
        self.db             = db
        self.cfg            = db.config.ext
        self.update_roundup = update_roundup

        if self.update_roundup is None :
            # try finding out via config, default to True
            try :
                update = getattr (self.cfg, 'IMAP_UPDATE_ROUNDUP')
            except AttributeError :
                update = 'yes'
            self.update_roundup = False
            if update.lower () in ('yes', 'true') :
                self.update_roundup = True

        self.imap = IMAP4 (* check_imap_config (self.db))

        self.valid_stati     = []
        self.status_obsolete = db.user_status.lookup ('obsolete')
        self.status_valid    = db.user_status.lookup ('valid')
        self.status_sync     = [self.status_obsolete, self.status_valid]
    # end def __init__

    def bind_as_user (self, username, password) :
        if not username :
            return None
        try :
            self.imap.login (username, password)
            return True
        except IMAP4.error, e :
            print >> sys.stderr, e
            pass
        return None
    # end def bind_as_user

    def sync_user_from_imap (self, username, status, pw = None, update = None) :
        reserved = ('admin', 'anonymous')
        if update is not None :
            self.update_roundup = update
        uid = None
        try :
            uid   = self.db.user.lookup  (username)
        except KeyError :
            pass
        # nothing to do if user not existing and imap says it's obsolete
        if not user :
            assert username not in reserved
            if status == self.status_obsolete :
                return
            else :
                assert status == self.status_valid
                uid = self.db.user.create \
                    ( username = username
                    , password = pw
                    , address  = username
                    )
        db.commit ()
    # end def sync_user_from_imap

# end IMAP_Roundup_Sync

def check_imap_config (db) :
    """ The given db can also be an instance, it just has to have a config
        object as an attribute.
    """
    cfg = db.config.ext
    host = None
    port = 143
    try :
        host = cfg.IMAP_HOST
        port = cfg.IMAP_PORT
    except KeyError :
        pass
    if not host :
        return
    return (host, port)
# end def check_imap_config

class ImapLoginAction (LoginAction, autosuper) :
    def try_imap (self) :
        adr = check_imap_config (self.db)
        if adr :
            self.imsync = IMAP_Roundup_Sync (self.db)
        return bool (adr)
    # end def try_imap

    def verifyLogin (self, username, password) :
        self.client.error_message = []
        if username in ('admin', 'anonymous') :
            return self.__super.verifyLogin (username, password)
        obsolete = self.db.user_status.lookup ('obsolete')
        try :
            user = self.db.user.lookup  (username)
            user = self.db.user.getnode (user)
        except KeyError :
            pass
        if self.try_imap () :
            if not password :
                raise exceptions.LoginError (self._ ('Invalid login'))
            if user and user.status not in self.imsync.status_sync :
                return self.__super.verifyLogin (username, password)
            if not self.imsync.bind_as_user (username, password) :
                self.imsync.sync_user_from_imap (username, obsolete)
                raise exceptions.LoginError (self._ ('Invalid login'))
            self.imsync.sync_user_from_imap \
                (username, self.imsync.status_valid, pw = password)
            try :
                user = self.db.user.lookup  (username)
                user = self.db.user.getnode (user)
            except KeyError :
                raise exceptions.LoginError (self._ ('Invalid login'))
            if user.status == obsolete :
                raise exceptions.LoginError (self._ ('Invalid login'))
            self.client.userid = user.id
        else :
            if not user or user.status == obsolete :
                raise exceptions.LoginError (self._ ('Invalid login'))
            return self.__super.verifyLogin (username, password)
    # end def verifyLogin
# end class ImapLoginAction
