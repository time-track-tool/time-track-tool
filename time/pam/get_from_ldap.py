#!/usr/bin/python

# Config:
URL    = 'ldap://localhost:3890/'
BASEDN = 'dc=tttech,dc=com'

import sys
import ldap
from traceback import format_tb
from syslog    import syslog, openlog, LOG_INFO, LOG_ERR, LOG_DEBUG \
                    , LOG_AUTH, setlogmask, LOG_UPTO
from roundup   import instance

ld = ldap.initialize (URL)
ld.simple_bind_s ("","")

KEYS = \
    [ 'uid'
    , 'gidNumber'
    , 'homeDirectory'
    , 'loginShell'
    , 'sambaHomeDrive'
    , 'sambaHomePath'
    , 'sambaKickoffTime'
    , 'sambaLMPassword'
    , 'sambaLogonScript'
    , 'sambaNTPassword'
    , 'sambaProfilePath'
    , 'sambaPwdCanChange'
    , 'sambaPwdLastSet'
    , 'sambaPwdMustChange'
    , 'shadowExpire'
    , 'shadowFlag'
    , 'shadowInactive'
    , 'shadowLastChange'
    , 'shadowMax'
    , 'shadowMin'
    , 'shadowWarning'
    , 'uidNumber'
    , 'userPassword'
    ]

tracker = instance.open ('/home/ralf/roundup/tttech')
db      = tracker.open ('admin')
openlog    ('get_from_ldap', LOG_DEBUG, LOG_AUTH)
setlogmask (LOG_UPTO (LOG_INFO)) # set to LOG_DEBUG if needed
syslog     (LOG_DEBUG, "started")

for line in sys.stdin :
    name = line.strip ()
    syslog (LOG_DEBUG, "name=%s" % name)
    try :
        u = db.user.getnode (db.user.lookup (name))
        syslog (LOG_INFO, "%s", u.realname)
        if u.sync_with_ldap :
            lu = l.search_s (BASEDN, ldap.SCOPE_SUBTREE, 'uid=%s' % name, KEYS)
            if len (lu) > 1 :
                dn = ' '.join ([l [0] for l in lu])
                syslog (LOG_ERR, 'more than one user: %s' % dn)
                continue
    except StandardError, cause :
        syslog (LOG_ERR, str (cause))
        for l in format_tb (sys.exc_info()[2]) :
            syslog (LOG_DEBUG, l)
syslog (LOG_DEBUG, "end")
