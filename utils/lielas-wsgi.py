#!/usr/bin/python
import sys
sys.stdout = sys.stderr
# obtain the WSGI request dispatcher
from roundup.cgi.wsgi_handler import RequestDispatcher
tracker_home = '/usr/local/src/lielas'
application = RequestDispatcher(tracker_home)
