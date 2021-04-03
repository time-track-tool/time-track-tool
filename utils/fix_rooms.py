#!/usr/bin/python
from __future__ import print_function
import sys
import os
from roundup           import instance
dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

if len (sys.argv) != 3 :
    print ("Usage: %s <location-id> <room-prefix>" % sys.argv [0])
    sys.exit (23)

location = db.location.getnode (sys.argv [1])
prefix   = sys.argv [2]

if location.room_prefix is None :
    db.location.set (location.id, room_prefix = prefix)
    location = db.location.getnode (location.id)

if prefix != location.room_prefix :
    print \
        ( "Non-matching room-prefix: %s in location vs. given %s"
        % (location.room_prefix, prefix)
        )

# Now set the prefix for all rooms:
for rid in db.room.filter (None, dict (location = location.id)) :
    room = db.room.getnode (rid)
    if not room.name.startswith (prefix) :
        db.room.set (rid, name = prefix + room.name)

db.commit()
