#!/usr/bin/python

import sys
import os
from traceback import format_tb
from syslog    import syslog, openlog, LOG_INFO, LOG_ERR, LOG_DEBUG \
                    , LOG_AUTH, setlogmask, LOG_UPTO
from roundup   import instance

tracker = instance.open ('/home/ralf/roundup/tttech')
db      = tracker.open ('admin')
openlog    ('get_from_ldap (%s)' % os.getpid (), LOG_DEBUG, LOG_AUTH)
setlogmask (LOG_UPTO (LOG_INFO)) # set to LOG_DEBUG if needed
syslog     (LOG_DEBUG, "started")

for line in sys.stdin :
    name = line.strip ()
    syslog (LOG_DEBUG, "name=%s" % name)
    try :
        u = db.user.lookup (name)
        syslog (LOG_INFO, "%s", db.user.get (u, 'realname'))
    except StandardError, cause :
        syslog (LOG_ERR, str (cause))
        for l in format_tb (sys.exc_info()[2]) :
            syslog (LOG_DEBUG, l)
syslog (LOG_DEBUG, "end")
