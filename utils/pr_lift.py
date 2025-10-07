#!/usr/bin/python3

import sys
from argparse import ArgumentParser
from roundup  import instance

def main ():
    dir = '.'
    tracker = instance.open (dir)
    db      = tracker.open ('admin')
    for id in db.pr_rating_category.getnodeids (retired = False):
        rc = db.pr_rating_category.getnode (id)
        v  = True
        if rc.name == 'good impression':
            v = False
        if rc.quality_relevant is None:
            db.pr_rating_category.set (id, quality_relevant = v)
    db.commit ()
# end def main

if __name__ == '__main__' :
    main ()
