#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
from __future__ import print_function
from argparse import ArgumentParser
from roundup  import instance, date
from csv      import DictReader
import sys
import os

class Reader (object) :

    def __init__ (self, filename) :
        self.file   = open (filename, 'r')
        self.lineno = None
    # end def __init__

    def __iter__ (self) :
        for n, line in enumerate (self.file) :
            self.lineno = n
            yield (line)
    # end def __iter__

# end def Reader

rename = \
    { 'costcenter' : 'sap_cc'
    }

fieldmap = \
    { 'Cost Center'                             : 'sap_cc'
    , 'Department Feld in TimeTracker (for IT)' : 'department' 
    , 'costcenter'                              : 'sap_cc'
    }

item_map = dict \
    ( department =
        { 'BU Off-Highway, Product Development' :
              'Business Unit Off-Highway, Product Development'
        }
    )


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
        ( "-f", "--field"
        , dest    = "fields"
        , help    = "Fields to update in dyn. user, e.g. sap_cc or department"
                    " can be specified multiple times"
        , action  = 'append'
        , default = []
        )
    parser.add_argument \
        ( "-N", "--new"
        , help    = "Date of new dynamic user"
        , default = '2017-10-01'
        )
    parser.add_argument \
        ( "-u", "--update"
        , help    = "Update roundup"
        , default = False
        , action  = 'store_true'
        )
    parser.add_argument \
        ( "-v", "--verbose"
        , help    = "Verbose messages"
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
        if 'username' in line :
            try :
                user = db.user.getnode (db.user.lookup (line ['username']))
            except KeyError :
                print ("User not found: %s" % line ['username'])
                continue
            sn = user.lastname
            fn = user.firstname
            username = user.username
        else :
            sn = line ['Surname'].decode ('utf-8')
            fn = line ['First name'].decode ('utf-8')
            if not sn or not fn :
                print ("Name empty: %(sn)s %(fn)s" % locals ())
                continue
            users = db.user.filter \
                (None, dict (firstname = fn, lastname = sn, status = st))
            if not users and ' ' in fn :
                fn = fn.split (' ', 1)[0]
                users = db.user.filter \
                    (None, dict (firstname = fn, lastname = sn, status = st))
            if not users :
                print ("User not found: %(sn)s %(fn)s" % locals ())
                continue
            if len (users) != 1 :
                uu = []
                for u in users :
                    user = db.user.getnode (u)
                    if  (  user.firstname.decode ('utf-8') != fn
                        or user.lastname.decode ('utf-8')  != sn
                        ) :
                        continue
                    uu.append (u)
                users = uu
            if len (users) != 1 :
                print (users, fn, sn)
            assert len (users) == 1
            user = db.user.getnode (users [0])
            if  (  user.firstname.decode ('utf-8') != fn
                or user.lastname.decode ('utf-8')  != sn
                ) :
                print (user.firstname, user.lastname, fn, sn)
            username = user.username
        dt    = date.Date (args.new)
        st    = db.user_status.lookup ('valid')
        # Get user dynamic record
        dyn = user_dynamic.get_user_dynamic (db, user.id, dt)
        if not dyn :
            print ("No dyn. user record: %(username)s" % locals ())
            continue
        if dyn.valid_to :
            print ("Dyn. user record limited: %(username)s" % locals ())
            continue
        if dyn.valid_from > dt :
            print ("Dyn. record starts after date: %(username)s" % locals ())
            continue
        if not dyn.vacation_yearly :
            print ("No yearly vacation: %(username)s" % locals ())
            continue
        do_create = True
        if dyn.valid_from == dt :
            do_create = False
        update = {}
        try :
            key = ''
            for k in fieldmap :
                f = fieldmap [k]
                if f in args.fields and k in line :
                    key  = line [k].strip ()
                    if f in item_map :
                        key = item_map [f].get (key, key)
                    cn   = dyn.cl.properties [f].classname
                    cls  = db.getclass (cn)
                    item = cls.lookup (key)
                    if dyn [f] != item :
                        update [f] = item
        except KeyError :
            print ("%(f)s not found: %(key)s: %(username)s" % locals ())
            continue
        if update :
            if do_create :
                fields = user_dynamic.dynuser_copyfields
                param  = dict ((i, dyn [i]) for i in fields)
                param ['valid_from'] = dt
                param.update (update)
                if args.update :
                    id = db.user_dynamic.create (** param)
                    if args.verbose :
                        print ("CREATED: %s" % id)
                else :
                    if args.verbose :
                        print ("user_dynamic-create: %s" % param)
            else :
                if args.update :
                    db.user_dynamic.set (dyn.id, ** update)
                else :
                    if args.verbose :
                        print \
                            ( "user_dynamic-update: %s %s %s"
                            % (update, fn, sn)
                            )
    if args.update :
        db.commit ()
# end def main


if __name__ == '__main__' :
    main ()
