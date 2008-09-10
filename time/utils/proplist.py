#!/usr/bin/python2.4
import sys
from roundup           import date
from roundup           import instance
tracker = instance.open ('/home/ralf/roundup/ttt')
db      = tracker.open ('admin')

#print db.classes

for cl in sorted (db.getclasses ()) :
    print cl
    for p in sorted (db.getclass (cl).properties.keys ()) :
        print "    ", p
