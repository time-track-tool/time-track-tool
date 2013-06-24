#!/usr/bin/python
import os
from roundup           import instance
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
    try :
        if q.klass not in db.classes or retired and db.query.is_retired (qid) :
            print "Deleting%squery for class %s" % (txt, q.klass)
            db.query.destroy (qid)
            return 1
        else :
            print "Keeping %squery for class %s" % (txt, q.klass)
            return 0
    except IndexError :
        pass
    except AttributeError :
        pass
# end def delq

cmd = OptionParser ()
cmd.add_option \
    ( '-r', '--retired'
    , dest   = 'retired'
    , help   = 'Destroy retired queries'
    , action = 'store_true'
    )
cmd.add_option \
    ( '-u', '--update'
    , dest   = 'update'
    , help   = 'Really destroy retired queries (do a commit)'
    , action = 'store_true'
    )
opt, args = cmd.parse_args ()
if len (args) :
    cmd.error ('No arguments please')
    sys.exit  (23)

for uid in db.user.getnodeids () :
    u  = db.user.getnode (uid)
    qs = dict.fromkeys (getattr (u, 'queries', []))
    for qid in u.queries :
        if delq (qid, retired = opt.retired) :
            try :
                del qs [qid]
            except KeyError :
                pass
    db.user.set (uid, queries = list (qs.iterkeys ()))

for qid in db.query.getnodeids () :
    delq (qid, txt = ' remaining ')

if opt.update :
    db.commit()
