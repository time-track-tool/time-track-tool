#!/usr/bin/python

import sys
import ldap
from traceback          import format_tb
from time               import gmtime
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
            , LOGLEVEL     = 0 # set to LOG_DEBUG if needed
            , LOG_FACILITY = 0
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


prefix     = 'GROUP'

KEYS = \
    [ ('gidNumber',   'gid',         int)
    , ('description', 'description', str)
    ]

config     = Config ()
tracker = instance.open (config.TRACKER)
db      = tracker.open  (config.ROUNDUP_USER)
ld      = ldap.initialize (config.URL)
ld.simple_bind_s (config.BIND_DN, config.BIND_PW)

scope = ldap.SCOPE_SUBTREE
lu    = ld.search_s (config.BASEDN, scope, 'ou=Groups')
tttech_wien = db.org_location.lookup ('TTTech Wien')
tttech_paf  = db.org_location.lookup ('TTTech Germany Hettenshausen')
group_olo = \
    { 11260 : tttech_paf
    }
for item in lu :
    print "--> ", item [0]
    lusub = ld.search_s (item [0], ldap.SCOPE_ONELEVEL)
    for x in lusub :
        #print x [0]
        d     = x [1]
        gid   = int (d ['gidNumber'][0])
        if 1 :
            print "%s: %s" % (d ['cn'][0], gid)
            try :
                g_id = db.group.lookup (d ['cn'][0])
                g    = db.group.getnode (g_id)
                db.group.set \
                    ( g_id
                    , ** dict 
                        ( (rk, fun (d [lk][0])) for lk, rk, fun in KEYS
                          if fun (d.get (lk, [None])[0]) != fun (g [rk])
                        )
                    )
            except KeyError :
                olo = group_olo.get (gid, tttech_wien)
                db.group.create \
                    ( name         = d ['cn'][0]
                    , org_location = olo
                    , ** dict
                        ( (rk, fun (d.get (lk, [None])[0]))
                          for lk, rk, fun in KEYS
                        )
                    )
db.commit ()
