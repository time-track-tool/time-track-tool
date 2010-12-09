#!/usr/bin/python
import os
import xmlrpclib
import signal
from optparse import OptionParser

cmd = OptionParser ()
cmd.add_option \
    ( '-t', '--timeout'
    , help    = "Timeout for xmlrpc request (Default: %default)"
    , default = 10
    , type    = "int"
    )
cmd.add_option \
    ( '-u', '--url'
    , help    = "URL to roundup tracker (Default: %default)"
    , default = 'https://anonymous:@time-tracker.vie.at.tttech.ttt/ttt/'
    )
opt, arg = cmd.parse_args ()
if len (arg) :
    cmd.error ("No arguments expected")
    exit (3)

s   = xmlrpclib.ServerProxy (opt.url, allow_none=True)

def sig_alarm (* args) :
    print "Critical: Socket Timeout: %s seconds" % opt.timeout
    exit (2)
# end def sig_alarm

oldsig = signal.signal (signal.SIGALRM, sig_alarm)
signal.alarm (opt.timeout)

try :
    r = s.lookup ('user', 'anonymous')
    print "Critical: roundup seems to allow lookup for anonymous"
    exit (2)
except xmlrpclib.Fault, reason :
    if  ( reason.faultCode != 1
        or not reason.faultString.startswith
           ("<class 'roundup.exceptions.Unauthorised'>")
        ) :
        print "Critical: Unknown permission error: %s/%s" \
            % (reason.faultCode, reason.faultString)
        exit (2)
    else :
        print "OK: roundup correctly denies lookup request to anonymous"
        exit (0)
except Exception, reason :
        print "Critical: Error: %s" % reason
        exit (2)
print "Unknown: Unknown error encountered"
exit (3)
