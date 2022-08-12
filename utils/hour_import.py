#!/usr/bin/python3

from __future__ import print_function

import sys
import os
import json
import requests
from datetime import datetime
from argparse import ArgumentParser
from netrc    import netrc
from getpass  import getpass
try :
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

class Hour_Updater (object) :

    def __init__ (self, args) :
        self.args    = args
        self.session = requests.session ()
        self.session.verify = False
        self.user    = args.username
        self.url     = args.url
        self.baseurl = args.url
        # Basic Auth: user, password
        self.session.auth = (self.user, self.get_pw ())
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

    def get_pw (self) :
        """ Password given as option takes precedence.
            Next we try password via .netrc. If that doesn't work we ask.
        """
        if self.args.password :
            return self.args.password
        a = n = None
        try :
            n = netrc ()
        except IOError :
            pass
        if n and self.args.url :
            t = urlparse (self.args.url)
            a = n.authenticators (t.netloc)
        if a :
            un, d, pw = a
            if un != self.user :
                raise ValueError ("Netrc username doesn't match")
            return pw
        pw = getpass ('Password: ')
        return pw
    # end def get_pw

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
                ( 'Invalid put/post result: %s: %s\n    %s'
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

    def get_wp_for_user (self, username) :
        """ Search for all work packages the user may book on.
            Note that individual work packages have a time_start and
            time_end property (the latter may be empty) that have to be
            checked *at which times* a user may book.
            We ignore public WPs, these you would get with
            time_wp?is_public=1&fields=...
        """
        q = 'time_wp?bookers=%s&@fields=name,project,time_start,time_end'
        return self.get (q % username)
    # end def get_wp_for_user

    def get_project (self, p_id) :
        q = 'time_project/%s' % p_id
        return self.get (q) ['data']['attributes']
    # end def get_project

    @staticmethod
    def round_hours (h) :
        """ Round given hours h to quarters of an hour
        >>> Hour_Updater.round_hours (4.27)
        4.25
        >>> Hour_Updater.round_hours (4.47)
        4.5
        """
        return round (h * 4.) / 4.
    # end def round_hours

    def book_on_day (self, username, date, hours, wp, activity) :
        """ Search for the daily_record on the given date and create it
            if not found.
            Then book the given hours on the given work package wp
            Note that this doesn't take into account *changes* to
            already-booked hours.
            Note that hours are rounded to quarter of hours, see above
            for the algorithm used.
        """
        # Find daily record
        dt = date.strftime ('%Y-%m-%d')
        dr = self.get ('daily_record?user=%s&date=%s' % (username, dt))
        if not dr ['data']['collection'] :
            d = dict (user = username, date = dt)
            self.post ('daily_record', json = d)
            dr = self.get ('daily_record?user=%s&date=%s' % (username, dt))
        assert len (dr ['data']['collection']) == 1
        # Fill in the metadata field.
        # The metadata field should be in json.
        # This field should have the following format:
        # { 'system_name' : 'name-of-your-timetracking-system'
        # , 'levels'      : [ { 'level' : 1
        #                     , 'level_name' : 'Project'
        #                     , 'name' : 'Project-Name'
        #                     , 'id' : '4711'
        #                   , ...
        #                   ]
        # }
        # Note that both, the top-level system_name and levels are
        # required. In the levels array at least one member is required.
        # The level is an integer value and levels must start with 1 and
        # be tightly numbered (without jumps of the counter). The
        # level_name and name of the respective item on that level depends
        # on the remote system. The id is a string because some systems
        # may use non-numeric ids here. The fields shown are all required,
        # additional fields may be present.

        js = dict (system_name = 'WTIS', levels = [])
        lvl1 = dict \
            ( level = 1
            , level_name = 'Project or whatever your first level is called'
            , name = 'Name of this particular project'
            , id = 'ID-of-this-particular-project'
            )
        js ['levels'].append (lvl1)
        # ... add further levels here

        d  = dict \
            ( daily_record  = dr ['data']['collection'][0]['id']
            , wp            = wp
            , duration      = self.round_hours (hours)
            , work_location = 'office'
            , time_activity = activity
            , metadata      = json.dumps (js)
            )
        tr = self.post ('time_record', json = d)
        print (tr)
    # end def book_on_day

    def submit_day (self, username, date) :
        """ Search for the daily_record on the given date and submit it.
            The given daily record must exist, it's an error if not.
        """
        dt = date.strftime ('%Y-%m-%d')
        dr = self.get ('daily_record?user=%s&date=%s' % (username, dt))
        assert len (dr ['data']['collection']) == 1
        id = dr ['data']['collection'][0]['id']
        dr = self.get ('daily_record/%s' % id)
        e  = dr ['data']['@etag']
        d  = dict (status = 'submitted')
        self.put ('daily_record/%s' % id, json = d, etag = e)
    # end def submit_day

# end class Hour_Updater

def main () :
    cmd = ArgumentParser ()
    cmd.add_argument \
        ( "-c", "--client-user"
        , help    = "Username for whom to book, default: %(default)s"
        , default = 'schlatterbeck'
        )
    cmd.add_argument \
        ( "-U", "--url"
        , help    = "URL of tracker (without rest path) default: %(default)s"
        , default = 'https://timetracking113.ds1.internal/'
        )
    cmd.add_argument \
        ( "-u", "--username"
        , help    = "Username, default: %(default)s"
        , default = 'admin'
        )
    cmd.add_argument \
        ( "-p", "--password"
        , help    = "Password, better use .netrc"
        )
    args = cmd.parse_args ()
    hup = Hour_Updater (args)
    j = hup.get_wp_for_user (args.client_user)
    for wp in j ['data']['collection'] :
        tp = hup.get_project (wp ['project']['id'])
        print ("%5s " % wp ['id'], end = ' ')
        print ("%50s" % (tp ['name'] + '/' + wp ['name']), end = ' ')
        if wp ['time_start'] :
            print (wp ['time_start'][:10], end = '-')
        else :
            print (' ' * 10, end = '-')
        if wp ['time_end'] :
            print (wp ['time_end'][:10])
        else :
            print ('')
    date = datetime (2019, 8, 1)
    # This is a wp my test-user may book on in our test tracker.
    wp   = 24429

    # For the last parameter (activity) perform a get on 'time_activity'
    # You can use the name or the number

    # Commented-out for now
    hup.book_on_day (args.client_user, date, 6.24, wp, 'Implementation')

    # Daily record must be submitted:
    # Commented-out for now
    # hup.submit_day (args.client_user, date)
# end def main

if __name__ == '__main__' :
    main ()
