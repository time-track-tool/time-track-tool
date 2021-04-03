#!/usr/bin/python
from __future__ import print_function
import sys
import os
from roundup           import instance

try:
    from urllib.parse import parse_qs, urlencode
except ImportError :
    from urlparse import parse_qs
    from urllib   import urlencode

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')

qids = db.query.filter (None, {}, exact_match_spec = dict (klass = 'user'))
for qid in qids :
    q = db.query.getnode (qid)
    if 'title' not in q.url and 'position' not in q.url :
        continue
    obj = parse_qs (q.url)
    for k in obj :
        assert not k.startswith ('@')
    #print (q.url)
    for fn in ':sort', ':group', ':columns', ':filter' :
        if fn in obj :
            modified = False
            assert len (obj [fn]) == 1
            fields = dict.fromkeys (obj [fn][0].split (','))
            if 'title' in fields :
                modified = True
                print ("Dropping %s:title from query%s" % (fn [1:], qid))
                del fields ['title']
                if 'title' in obj :
                    del obj ['title']
            if 'position' in fields :
                modified = True
                if fn == ':filter' :
                    print ("Dropping %s:position from query%s" % (fn [1:], qid))
                    del fields ['position']
                    del obj ['position']
                else :
                    print ("Replacing %s:position of query%s" % (fn [1:], qid))
                    del fields ['position']
                    fields ['position_text'] = 1
            if modified :
                obj [fn] = [','.join (fields)]
    url = urlencode (obj, doseq = True)
    db.query.set (qid, url = url)
    #print (url)
db.commit()
