from roundup import instance
tracker = instance.open ('..')
db      = tracker.open ('admin')
for c in db.getclasses () :
    cls = db.getclass (c)
    for p in cls.getprops ().keys () :
        print '_("%s")' % p

