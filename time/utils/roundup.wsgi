#!/usr/bin/python
from roundup.cgi.wsgi_handler import RequestDispatcher
tracker_home = '/var/lib/tracker/helpdesk'
application = RequestDispatcher(tracker_home)
