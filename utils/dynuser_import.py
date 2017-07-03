#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os

from argparse import ArgumentParser
from roundup  import instance, date
from csv      import DictReader

class Reader (object) :

    def __init__ (self, filename) :
        self.file   = open (filename, 'r')
        self.lineno = None
    # end def __init__

    def __iter__ (self) :
        for n, line in enumerate (self.file) :
            if n == 0 :
                continue
            self.lineno = n
            yield (line)
    # end def __iter__

# end def Reader

def main () :
    # most ldap info is now fetched from extensions/config.ini
    parser  = ArgumentParser ()
    parser.add_argument \
        ( "file"
        , help    = "CSV import file"
        )
    parser.add_argument \
        ( "-d", "--database-directory"
        , dest    = "database_directory"
        , help    = "Directory of the roundup installation"
        , default = '.'
        )
    parser.add_argument \
        ( '-D', '--delimiter'
        , dest    = 'delimiter'
        , help    = 'CSV delimiter character (tab)'
        , default = '\t'
        )
    parser.add_argument \
        ( "-N", "--new"
        , help    = "Date of new dynamic user"
        , default = '2017-07-01'
        )
    parser.add_argument \
        ( "-u", "--update"
        , help    = "Update roundup"
        , default = False
        , action  = 'store_true'
        )
    args = parser.parse_args ()

    tracker = instance.open (args.database_directory)
    db      = tracker.open ('admin')

    sys.path.insert (1, os.path.join (args.database_directory, 'lib'))
    import user_dynamic

    r       = Reader (args.file)
    d       = DictReader (r, delimiter = args.delimiter)

    for line in d :
        sn = line ['Surname'].decode ('utf-8')
        fn = line ['First name'].decode ('utf-8')
        if not sn or not fn :
            print "Name empty: %(sn)s %(fn)s" % locals ()
            continue
        dt    = date.Date (args.new)
        users = db.user.filter (None, dict (firstname = fn, lastname = sn))
        if not users and ' ' in fn :
            fn = fn.split (' ', 1)[0]
            users = db.user.filter (None, dict (firstname = fn, lastname = sn))
        if not users :
            print "User not found: %(sn)s %(fn)s" % locals ()
            continue
        assert len (users) == 1
        # Get user dynamic record
        dyn = user_dynamic.get_user_dynamic (db, users [0], dt)
        if not dyn :
            print "No dyn. user record: %(sn)s %(fn)s" % locals ()
            continue
        if dyn.valid_to :
            print "Dyn. user record limited: %(sn)s %(fn)s" % locals ()
            continue
        if dyn.valid_from >= dt :
            print "Dyn. record starts after date: %(sn)s %(fn)s" % locals ()
            continue
        cc = line ['Cost Center'].decode ('utf-8').strip ()
        try :
            sap_cc = db.sap_cc.lookup (cc)
        except KeyError :
            print "Cost-Center not found: %(cc)s: %(sn)s %(fn)s" % locals ()
            continue
        fields = user_dynamic.dynuser_copyfields
        param  = dict ((i, dyn [i]) for i in fields)
        param ['valid_from'] = dt
        param ['sap_cc'] = sap_cc
        if args.update :
            id = db.user_dynamic.create (** param)
            #print "CREATED: %s" % id
        else :
            print "user_dynamic-create: %s" % param
    if args.update :
        db.commit ()
# end def main


if __name__ == '__main__' :
    main ()
