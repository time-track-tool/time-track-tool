#!/usr/bin/python3

from __future__ import print_function

import sys
import os
import json
import urllib3
import requests
from datetime import datetime
from argparse import ArgumentParser
from netrc    import netrc
from getpass  import getpass
from rsclib.autosuper import autosuper
try :
    from urllib.parse import urlparse, urlencode
except ImportError:
    from urlparse import urlparse
    from urllib   import urlencode

class Requester (autosuper) :

    def __init__ (self, args) :
        self.args    = args
        if args.disable_cert_check_warning :
            urllib3.disable_warnings (urllib3.exceptions.InsecureRequestWarning)
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
                raise ValueError \
                    ( "Netrc username doesn't match: %s vs.  %s"
                    % (un, self.user)
                    )
            return pw
        pw = getpass ('Password: ')
        return pw
    # end def get_pw

    def delete (self, s, etag = None) :
        h = dict (self.headers)
        if etag :
            h ['If-Match'] = etag
        r = self.session.delete (self.url + s, headers = h)
        if not (200 <= r.status_code <= 299) :
            raise RuntimeError \
                ( 'Invalid get result: %s: %s\n    %s'
                % (r.status_code, r.reason, r.text)
                )
        return r.json ()
    # end def delete

    def post_or_put (self, method, s, data = None, json = None, etag = None) :
        d = {}
        if data :
            d ['data'] = data
        if json :
            d ['json'] = json
        d ['headers'] = h = dict (self.headers)
        if etag :
            h ['If-Match'] = etag
        r = method (self.url + s, **d)
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

# end class Requester

def get_default_cmd (argv = None) :
    if argv is None :
        argv = sys.argv [1:]
    cmd = ArgumentParser ()
    cmd.add_argument \
        ( "-C", "--disable-cert-check-warning"
        , help    = "Disable certificate check warning for https connection"
        , default = False
        , action  = 'store_true'
        )
    cmd.add_argument \
        ( "-U", "--url"
        , help    = "URL of tracker (without rest path) default: %(default)s"
        , default = 'http://cat:8080/ttt/'
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
    return cmd
# end def get_default_cmd

def main (argv = None) :
    cmd  = get_default_cmd (argv)
    args = cmd.parse_args (argv)
    rq = Requester (args)
    return rq
# end def main
