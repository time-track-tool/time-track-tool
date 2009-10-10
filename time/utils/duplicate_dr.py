#!/usr/bin/python
from roundup           import date
from roundup           import instance
tracker  = instance.open ('/roundup/tracker/ttt')
db       = tracker.open ('admin')
monthd   = [21,28,31,30,31,30,31,31,30,31,30,31]

user     = db.user.lookup ('schlatterbeck')
daystart = 10
month    = 05

for j in range (7) :
    max = monthd [month -1] + 1
    i = '2009-%s-%s' % ((j + daystart) / max + month, j + daystart)
    dr = db.daily_record.filter \
        (None, dict (date = '%s;%s' % (i, i), user = user))
    for d in dr :
        print i, d
        tr = db.time_record.find (daily_record = dict (((d, 1),)))
        dv = db.daily_record.getnode (d)
        print d, tr, dv.user, dv.date, dv.status, dv.time_record
