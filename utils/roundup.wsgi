#!/usr/bin/python3

from os.path import dirname, abspath
from roundup.cgi.wsgi_handler import RequestDispatcher

tracker_home = dirname (dirname (abspath (__file__)))
ff = dict (cache_tracker = True)
application = RequestDispatcher(tracker_home, feature_flags = ff)
