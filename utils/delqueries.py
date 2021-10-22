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

def delq (qid, txt = ' ', retired = False, verbose = False) :
    q = db.query.getnode (qid)
    try :
        if q.klass not in db.classes or retired and db.query.is_retired (qid) :
            print "Deleting%squery for class %s" % (txt, q.klass)
            db.query.destroy (qid)
            return 1
        else :
            if verbose :
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
cmd.add_option \
    ( '-v', '--verbose'
    , dest   = 'verbose'
    , help   = 'Verbose output'
    , action = 'store_true'
    )
opt, args = cmd.parse_args ()
if len (args) :
    cmd.error ('No arguments please')
    sys.exit  (23)

for uid in db.user.getnodeids () :
    u  = db.user.getnode (uid)
    qs = dict.fromkeys (u.queries)
    ch = False
    allq = db.query.filter (None, dict (private_for = uid))
    diff = set (allq).difference (qs)
    if diff :
        print "Restoring some queries for user %s: %s" \
            % (uid, ', '.join (sorted (list (diff))))
        qs.update (dict.fromkeys (allq))
        ch = True
    # dict modified during iteration
    for qid in list (qs) :
        q = db.query.getnode (qid)
        try :
            n = q.name
        except IndexError :
            print "deleting missing query %s from user %s" % (qid, uid)
            del qs [qid]
            ch = True
            continue

        if delq (qid, retired = opt.retired, verbose = opt.verbose) :
            try :
                del qs [qid]
                ch = True
            except KeyError :
                pass
    if ch :
        db.user.set (uid, queries = list (qs))

for qid in db.query.getnodeids () :
    delq (qid, txt = ' remaining ', verbose = opt.verbose)

if opt.update :
    db.commit()
