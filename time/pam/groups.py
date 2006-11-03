#!/usr/bin/python

import sys
import ldap
from traceback          import format_tb
from time               import gmtime
from syslog             import syslog, openlog, LOG_INFO, LOG_ERR, LOG_DEBUG \
                             , LOG_AUTH, setlogmask, LOG_UPTO
from rsclib.Config_File import Config_File
from rsclib.autosuper   import autosuper
from roundup            import instance
from roundup.date       import Date
from roundup.password   import Password

class Config (Config_File, autosuper) :
    def __init__ (self, config = 'from_ldap', path = '/etc/roundup') :
        self.__super.__init__ \
            ( path, config
            , URL          = 'ldap://localhost:389/'
            , BASEDN       = 'dc=example,dc=com'
            , BIND_DN      = ''
            , BIND_PW      = ''
            , LOGLEVEL     = LOG_INFO # set to LOG_DEBUG if needed
            , LOG_FACILITY = LOG_AUTH
            , LOG_PREFIX   = 'get_from_ldap'
            , MODE         = {'always' : True}
            , TRACKER      = '/roundup/example'
            , ROUNDUP_USER = 'admin'
            )
    # end def __init__
# end class Config

def datecvt (s) :
    return Date (gmtime (int (s)))
# end def datecvt

def gid (s) :
    groups = db.group.filter (None, dict (gid = int (s)))
    g = None
    l = len (groups)
    if l >= 1 :
        g = groups [0]
    if l != 1 :
        syslog (LOG_ERR, "Invalid number of groups found: %s" % groups)
    return g
# end def gid

def log_traceback (cause) :
    syslog (LOG_ERR, str (cause))
    for l in format_tb (sys.exc_info()[2]) :
        syslog (LOG_DEBUG, l)
# end def log_traceback

config     = Config ()
openlog    (config.LOG_PREFIX, 0, config.LOG_FACILITY)
setlogmask (LOG_UPTO (config.LOGLEVEL))
syslog     (LOG_DEBUG, "started")
try :
    tracker = instance.open (config.TRACKER)
    db      = tracker.open  (config.ROUNDUP_USER)
    ld      = ldap.initialize (config.URL)
    ld.simple_bind_s (config.BIND_DN, config.BIND_PW)
except StandardError, cause :
    log_traceback (cause)
    sys.exit (23)

    try :
        scope = ldap.SCOPE_SUBTREE
        lu    = ld.search_s (config.BASEDN, scope)
        print lu
    except StandardError, cause :
        log_traceback (cause)
syslog (LOG_DEBUG, "end")
