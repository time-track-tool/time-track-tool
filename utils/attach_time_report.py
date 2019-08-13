#!/usr/bin/python3
import sys
import os
import requests
from datetime import datetime

class Report_Updater (object) :

    def __init__ (self, url, user, password) :
        self.session = requests.session ()
        self.user    = user
        self.url     = url
        # Basic Auth: user, password
        self.session.auth = (user, password)
        if self.url.endswith ('/') :
            orig = self.url.rstrip ('/')
        else :
            orig = self.url
            self.url += '/'
        self.headers = dict \
            ( Origin  = orig
            , Referer = self.url
            )
        self.headers ['X-Requested-With'] = 'requests library'
        self.url += 'rest/data/'
    # end def __init__

    def get (self, s) :
        r = self.session.get (self.url + s, headers = self.headers)
        if not (200 <= r.status_code <= 299) :
            raise RuntimeError \
                ( 'Invalid get result: %s: %s\n    %s'
                % (r.status_code, r.reason, r.text)
                )
        return r.json ()
    # end def get

    def post_or_put (self, method, s, data = None, json = None, etag = None) :
        d = {}
        if data :
            d ['data'] = data
        if json :
            d ['json'] = json
        h = dict (self.headers)
        if etag :
            h ['If-Match'] = etag
        r = method (self.url + s, headers = h, **d)
        if not (200 <= r.status_code <= 299) :
            raise RuntimeError \
                ( 'Invalid post result: %s: %s\n    %s'
                % (r.status_code, r.reason, r.text)
                )
        return r.json ()
    # end def post_or_put

    def post (self, s, data = None, json = None, etag = None) :
        return self.post_or_put (self.session.post, s, data, json, etag)
    # end def post

    def put (self, s, data = None, json = None, etag = None) :
        return self.post_or_put (self.session.put, s, data, json, etag)
    # end def put

    def update_time_project (self, tpid, filename, content_type, content) :
        """ Get the time_project from the database (to verify it
            exists), check if we have a time_report for this project.
            If the time_report doesn't exist, create a new file with the
            given parameters (filename, content_type, content) and
            attach this to a new time_report. If the report is already
            existing, we update the file and the last_updated field of
            the report.
        """
        now = datetime.now ().strftime ('%Y-%m-%d.%H:%M:%S')
        j = self.get ('time_project/%s' % tpid)
        #print (j)
        assert j ['data']['id'] == tpid
        j = self.get ('time_report?time_project=%s' % tpid)
        #print (j)
        if j ['data']['collection'] :
            #print (j)
            rid = j ['data']['collection'][0]['id']
            j = self.get ('time_report/%s' % rid)
            #print (j)
            r_etag = j ['data']['@etag']
            j = self.get ('file/%s' % j ['data']['attributes']['file']['id'])
            #print (j)
            fid = j ['data']['id']
            etag = j ['data']['@etag']
            d = dict (name = filename, content = content, type = content_type)
            j = self.put ('file/%s' % fid, etag = etag, data = d)
            #print (j)
            d = dict (last_updated = now)
            j = self.put ('time_report/%s' % rid, etag = r_etag, data = d)
            #print (j)
        else :
            # create file, the file could be binary so we use the 'data'
            # parameter of the post request instead of 'json'
            d = dict (name = filename, content = content, type = content_type)
            j = self.post ('file', data = d)
            #print (j)
            fid = j ['data']['id']
            d = dict (file = fid, time_project = tpid, last_updated = now)
            j = self.post ('time_report', json = d)
            #print (j)
            rid = j ['data']['id']
    # end def update_time_project

# end class Report_Updater

tpid = sys.argv [1]
file = sys.argv [2]
with open (file, 'r') as f :
    content = f.read ()

# use basename as filename in timetracker
filename = os.path.basename (file)

ru = Report_Updater ('http://bee:8080/ttt', 'admin', 'xyzzy')
ru.update_time_project (tpid, filename, 'application/octet-stream', content)
