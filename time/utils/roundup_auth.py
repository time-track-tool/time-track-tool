#!/usr/bin/python

import xmlrpclib
from   mod_python import apache

url = 'https://%(username)s:%(password)s@time-tracker.vie.at.tttech.ttt/ttt/'

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
        return apache.HTTP_UNAUTHORIZED
    except xmlrpclib.ProtocolError, err :
        return apache.HTTP_UNAUTHORIZED
    if status != 'external' :
        return apache.HTTP_UNAUTHORIZED
    return apache.OK
# end def authenhandler
  
#def authzhandler (req) :
#    """Called by mod_python to handle Apache's authorization phase"""
#    print >> x, "authzhandler"
#    return apache.OK
## end def authzhandler
