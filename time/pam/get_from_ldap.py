#!/usr/bin/python

# Config:
URL    = 'ldap://localhost:3890/'
BASEDN = 'dc=tttech,dc=com'
BIND_DN = 'uid=tracker,ou=Users,ou=vie,ou=at,' \
          'ou=tttech,o=ttt,dc=tttech,dc=com'
BIND_DN = ''
BIND_PW = ''
MODE    = {'once' : True, 'always' : True}

import sys
import ldap
from traceback        import format_tb
from time             import gmtime
from syslog           import syslog, openlog, LOG_INFO, LOG_ERR, LOG_DEBUG \
                           , LOG_AUTH, setlogmask, LOG_UPTO
from roundup          import instance
from roundup.date     import Date
from roundup.password import Password

ld = ldap.initialize (URL)
ld.simple_bind_s (BIND_DN, BIND_PW)

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

KEYS = \
    { 'uid'                : ('never',   None,    None)
    , 'gidNumber'          : ('once',    gid,     'group')
    , 'homeDirectory'      : ('once',    str,     'home_directory')
    , 'loginShell'         : ('once',    str,     'login_shell')
    , 'sambaHomeDrive'     : ('once',    str,     'samba_home_drive')
    , 'sambaHomePath'      : ('once',    str,     'samba_home_path')
    , 'sambaKickoffTime'   : ('always',  datecvt, 'samba_kickoff_time')
    , 'sambaLMPassword'    : ('always',  str,     'samba_lm_password')
    , 'sambaLogonScript'   : ('always',  str,     'samba_logon_script')
    , 'sambaNTPassword'    : ('always',  str,     'samba_nt_password')
    , 'sambaProfilePath'   : ('once',    str,     'samba_profile_path')
    , 'sambaPwdCanChange'  : ('always',  datecvt, 'samba_pwd_can_change')
    , 'sambaPwdLastSet'    : ('always',  datecvt, 'samba_pwd_last_set')
    , 'sambaPwdMustChange' : ('always',  datecvt, 'samba_pwd_must_change')
    , 'shadowExpire'       : ('always',  datecvt, 'shadow_expire')
    , 'shadowFlag'         : ('always',  bool,    'shadow_used')
    , 'shadowInactive'     : ('always',  int,     'shadow_inactive')
    , 'shadowLastChange'   : ('always',  datecvt, 'shadow_last_change')
    , 'shadowMax'          : ('always',  int,     'shadow_max')
    , 'shadowMin'          : ('always',  int,     'shadow_min')
    , 'shadowWarning'      : ('always',  int,     'shadow_warning')
    , 'uidNumber'          : ('once',    int,     'uid')
    , 'userPassword'       : ('always',  str,     'user_password')
    }

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
        syslog (LOG_INFO, "updating: %s" % u.realname)
        if u.sync_with_ldap :
            k = KEYS.keys ()
            lu = ld.search_s (BASEDN, ldap.SCOPE_SUBTREE, 'uid=%s' % name, k)
            if len (lu) > 1 :
                dn = ' '.join ([l [0] for l in lu])
                syslog (LOG_ERR, 'more than one user: %s' % dn)
                continue
            # lu was a list of 2-tuples, (dn, attributes) where
            # attributes is a dict. The values in the dict are *always*
            # arrays. We currently use only the first item in the array.
            lu = lu [0][1]
            for k, v in KEYS.iteritems () :
                mode, func, param = v
                if k in lu :
                    syslog (LOG_INFO, "%s: %s" % (k, lu [k]))
                    if callable (func) and mode in MODE :
                        db.user.set (u.id, ** {param : func (lu [k][0])})
                    if k == 'userPassword' :
                        pw = lu [k][0].replace ('{CRYPT}', '{crypt}')
                        pw = Password (encrypted = pw)
                        db.user.set (u.id, password = pw)
            db.commit ()
    except StandardError, cause :
        syslog (LOG_ERR, str (cause))
        for l in format_tb (sys.exc_info()[2]) :
            syslog (LOG_DEBUG, l)
syslog (LOG_DEBUG, "end")
