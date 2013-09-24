#!/usr/bin/python

import xmlrpclib
import logging
from   mod_python       import apache
from   logging.handlers import SysLogHandler

host = 'issue-tracker.vie.at.tttech.ttt'
url  = 'https://%%(username)s:%%(password)s@%(host)s/ttt/xmlrpc' % globals ()

pf   = 'roundup_auth'
log  = logging.getLogger (pf)
fmt  = logging.Formatter ('%s[%%(process)d]: %%(message)s' % pf)
hdl  = SysLogHandler ('/dev/log', 'daemon')
hdl.setLevel (logging.INFO)
hdl.setFormatter (fmt)
log.addHandler (hdl)
log.setLevel (logging.INFO)

def authenhandler (req) :
    """Called by mod_python to handle Apache's authentication phase"""
    password = req.get_basic_auth_pw ()
    username = req.user
    server   = xmlrpclib.ServerProxy (url % locals (), allow_none = True)
    try :
        userid   = server.lookup ('user', username) 
        status   = server.display ('user%s' % userid, 'status') ['status']
        status   = server.display ('user_status%s' % status, 'name') ['name']
    except xmlrpclib.Fault, err :
        log.error (str (err))
        return apache.HTTP_UNAUTHORIZED
    except xmlrpclib.ProtocolError, err :
        log.error (str (err))
        return apache.HTTP_UNAUTHORIZED
    if status != 'external' :
        log.warn ("Try to login from non-external user %s" % username)
        return apache.HTTP_UNAUTHORIZED
    return apache.OK
# end def authenhandler
  
#def authzhandler (req) :
#    """Called by mod_python to handle Apache's authorization phase"""
#    print >> x, "authzhandler"
#    return apache.OK
## end def authzhandler
