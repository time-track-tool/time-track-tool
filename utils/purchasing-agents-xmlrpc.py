#!/usr/bin/python2

from __future__ import print_function

try :
    from xmlrpc.client import ServerProxy
except ImportError :
    from xmlrpclib import ServerProxy
import csv
from netrc    import netrc
from getpass  import getpass
from argparse import ArgumentParser

try :
    from urllib.parse import urlunparse, quote
except ImportError :
    from urlparse import urlunparse
    from urllib   import quote

class Timecat_Updater (object) :

    def __init__ (self, args) :
        self.args  = args
        self._url  = None
        self.srv   = ServerProxy (self.url, allow_none=True)
        self.udict = {}
    # end def __init__

    def process_csv (self, csv_file) :
        print ("Syncing: %s" % csv_file)
        with open (csv_file, 'rb') as f :
            dr = csv.DictReader (f, delimiter = self.args.delimiter)
            for line in dr :
                id = line ['Id'].decode (self.args.encoding)
                tc = self.srv.display ('time_project%s' % id)
                name = line ['Name'].decode (self.args.encoding)
                if name != tc ['name'] :
                    raise ValueError \
                        ('Inconsistent Name %s for time_project%s' % (name, id))
                pa = line ['Purchasing agents'].decode (self.args.encoding)
                pa = [x.strip () for x in pa.split (',')]
                pa = [x for x in pa if x]
                users = []
                for u in pa :
                    if u not in self.udict :
                        self.udict [u] = self.srv.lookup ('user', u)
                    users.append (self.udict [u])
                if set (users) != set (tc ['purchasing_agents']) :
                    arg = 'purchasing_agents=%s' % ','.join (users)
                    self.srv.set ('time_project%s' % id, arg)
                    print ("Updated time_project%s: %s" % (id, arg))
    # end def process_csv

    @property
    def url (self) :
        if self._url :
            return self._url
        username = self.args.username
        password = None
        try :
            n = netrc ()
        except IOError :
            pass
        if n :
            a = n.authenticators (self.args.hostname)
        if a :
            un, d, pw = a
            username = un
            password = pw
        if not password :
            password = getpass ('Password: ')
        un = [username]
        un.append (':')
        un.append (quote (password))
        un.append ('@')
        un.append (self.args.hostname)
        un = ''.join (un)
        netloc = []
        netloc.append (un)
        if self.args.port :
            netloc.append (':')
            netloc.append (self.args.port)
        netloc = ''.join (netloc)
        self._url = urlunparse \
            ((self.args.scheme, netloc, self.args.path, '', '', ''))
        return self._url
    # end def url

# end class Timecat_Updater

def main () :
    cmd = ArgumentParser ()
    cmd.add_argument \
        ( "file"
        , help    = 'CSV file to import'
        , nargs   = '+'
        )
    cmd.add_argument \
        ( '-D', '--delimiter'
        , help    = 'CSV delimiter character, default: "%(default)s"'
        , default = ';'
        )
    cmd.add_argument \
        ( '-E', '--encoding'
        , help    = 'CSV encoding, default: "%(default)s"'
        , default = 'utf-8'
        )
    cmd.add_argument \
        ( '-H', '--hostname'
        , help    = 'Tracker hostname, default: "%(default)s"'
        , default = 'example.com'
        )
    cmd.add_argument \
        ( '-P', '--port'
        , help    = 'Tracker port, default: empty'
        , default = ''
        )
    cmd.add_argument \
        ( '-p', '--path'
        , help    = 'URL path for retrieving file, default=%(default)s"'
        , default = 'xmlrpc'
        )
    cmd.add_argument \
        ( '-s', '--scheme'
        , help    = 'URL scheme for retrieving file, default=%(default)s"'
        , default = 'https'
        )
    cmd.add_argument \
        ( '-u', '--username'
        , help    = 'User name to access tracker, default: "%(default)s"'
        , default = 'admin'
        )
    args = cmd.parse_args ()
    tu = Timecat_Updater (args)
    for csv in args.file :
        tu.process_csv (csv)
# end def main

if __name__ == '__main__' :
    main ()
