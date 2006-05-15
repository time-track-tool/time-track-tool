from roundup           import date
from roundup           import instance
tracker = instance.open ('/roundup/tracker/ttt')
db      = tracker.open ('admin')

user    = db.user.lookup ('senn')
for j in range (1,7) :
    i = '2006-05-%s' % j
    dr = db.daily_record.filter \
        (None, dict (date = '%s;%s' % (i, i), user = user))
    print i, dr
    for d in dr :
        tr = db.time_record.find (daily_record = dict (((d, 1),)))
        dv = db.daily_record.getnode (d)
        print d, tr, dv.user, dv.date, dv.status, dv.time_record

