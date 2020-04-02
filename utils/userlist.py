#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import sys
import os
from roundup           import instance
tracker = instance.open (os.getcwd ())
db      = tracker.open  ('admin')

from rup_utils import update_userlist_html, update_userlist_json

update_userlist_html (db)
update_userlist_json (db)
