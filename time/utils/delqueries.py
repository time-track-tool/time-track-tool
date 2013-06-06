#!/usr/bin/python
import os
from roundup           import instance
from roundup.password  import Password, encodePassword
from optparse          import OptionParser

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

"""
    Delete obsolete queries, these are the ones that refer to classes
    that do not (or no longer) exist.
    If additional --retired flag is given, destroy retired queries, too.
"""

def delq (qid, txt = ' ', retired = False) :
    q = db.query.getnode (qid)
    if q.klass not in db.classes or retired and db.query.is_retired (qid) :
        print "Deleting%squery for class %s" % (txt, q.klass)
        db.query.destroy (qid)
        return 1
    else :
        print "Keeping %squery for class %s" % (txt, q.klass)
        return 0
# end def delq

cmd = OptionParser ()
cmd.add_option \
    ( '-r', '--retired'
    , dest   = 'retired'
    , help   = 'Destroy retired queries'
    , action = 'store_true'
    )
cmd.add_option \
    ( '-a', '--action'
    , dest   = 'action'
    , help   = 'Really destroy retired queries (do a commit)'
    , action = 'store_true'
    )
opt, args = cmd.parse_args ()
if len (args) :
    cmd.error ('No arguments please')
    sys.exit  (23)

for uid in db.user.getnodeids () :
    u  = db.user.getnode (uid)
    qs = dict.fromkeys (u.queries)
    for qid in u.queries :
        if delq (qid, retired = opt.retired) :
            del qs [qid]
    db.user.set (uid, queries = list (qs.iterkeys ()))

for qid in db.query.getnodeids () :
    delq (qid, txt = ' remaining ')

if opt.action :
    db.commit()
