#!/usr/bin/python

from __future__ import print_function

import sys
from csv      import DictReader
from argparse import ArgumentParser
from requester import Requester, get_default_cmd, urlencode

def export_iter (f) :
    found = False
    for line in f :
        if found :
            yield (line.decode ('utf-8'))
        else :
            if b'Id;' in line :
                yield (line.decode ('utf-8'))
                found = True
# end def export_iter

class Verify (Requester) :

    props = dict \
        ( user         = ('username', 'status')
        , time_project = ('name',)
        , sap_cc       = ('name',)
        )

    usernames = {}

    def lookup (self, cls, key, keyprop = 'name') :
        if not key :
            return None
        try :
            d = {}
            d ['@fields'] = ','.join (self.props [cls])
            d [keyprop + ':'] = key
            result = self.get (cls + '?' + urlencode (d))
            data = result ['data']['collection']
            if not data :
                print ('%s not found: "%s"' % (cls, key), file = sys.stderr)
                return None
        except RuntimeError as err :
            print (err)
            print ('%s not found: "%s"' % (cls, key), file = sys.stderr)
            return
        assert len (data) == 1
        return data [0]
    # end def lookup

    def lookup_user (self, key) :
        if key in self.usernames :
            return self.usernames [key]
        u = self.lookup ('user', key, keyprop = 'username')
        self.usernames [key] = u
        if not u :
            return
        print ("OK username=%s" % u ['username'])
        if u ['status']['id'] != '1' :
            d = dict (u)
            d ['status'] = u ['status']['id']
            print ("Username %(username)s: Wrong status: %(status)s" % d)
    # end def lookup_user

# end class Verify

def main () :
    cmd = get_default_cmd ()
    cmd.add_argument \
        ( 'cc'
        , help = 'SAP Cost Center file'
        )
    cmd.add_argument \
        ( 'tc'
        , help = 'Time Category file'
        )
    args    = cmd.parse_args ()
    vv      = Verify (args)

    with open (args.tc, 'rb') as f :
        dr = DictReader (export_iter (f), delimiter = ';')
        for rec in dr :
            name = rec ['Name']
            tc = vv.lookup ('time_project', name)
            if tc :
                print ("OK TC=%s" % tc ['name'])
                rid  = rec ['Id']
                if tc ['id'] != rid :
                    print \
                        ( "Non-matching ID for %s: got %s expected %s"
                        % (tc ['name'], tc ['id'], rid)
                        )
            vv.lookup_user ((rec ['Grouplead'] or b'').strip ())
            vv.lookup_user ((rec ['Teamlead'] or b'').strip ())
    with open (args.cc, 'rb') as f :
        dr = DictReader (export_iter (f), delimiter = ';')
        for rec in dr :
            name = rec ['Name']
            cc = vv.lookup ('sap_cc', name)
            if cc :
                print ("OK CC=%s" % cc ['name'])
                rid  = rec ['Id']
                if cc ['id'] != rid :
                    print \
                        ( "Non-matching ID for %s: got %s expected %s"
                        % (cc ['name'], cc ['id'], rid)
                        )
            vv.lookup_user ((rec ['Grouplead'] or b'').strip ())
            vv.lookup_user ((rec ['Teamlead'] or b'').strip ())
# end def main

if __name__ == '__main__' :
    main ()
