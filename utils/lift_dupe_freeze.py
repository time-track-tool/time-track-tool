#!/usr/bin/python3

import sys
import os
from roundup import instance

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

db.sql \
    ( 'alter table _daily_record_freeze add constraint '
      'drf_date_user_unique unique '
      '(_date, _user, __retired__);'
    )

