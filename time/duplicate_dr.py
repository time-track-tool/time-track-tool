from roundup           import date
from roundup           import instance
tracker = instance.open ('/roundup/tracker/ttt')
db      = tracker.open ('admin')

user    = db.user.lookup ('prammer')
for j in range (7) :
    i = '2006-04-%s' % (j + 10)
    dr = db.daily_record.filter \
        (None, dict (date = '%s;%s' % (i, i), user = user))
    for d in dr :
        print i, d
        tr = db.time_record.find (daily_record = dict (((d, 1),)))
        dv = db.daily_record.getnode (d)
        print d, tr, dv.user, dv.date, dv.status, dv.time_record

