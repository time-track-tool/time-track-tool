#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from roundup      import instance
from roundup.date import Date

class User_Dyn_Flexifixer (object) :
    """ Loop over all user-dynamic records and find the ones that are
        currently valid (since start of year). Set max_flexitime for all of
        them that have all_in set. If any of the records for one user starts
        earlier than the start year below, we thaw that user, split the dyn.
        user record at 2018-01-01, set max_flexitime and re-freeze everything.
        For this to work we store dyn. user records by user.
    """
    year    = Date ('2018-01-01')
    maxflex = 5
    olo     = dict.fromkeys (('1', '3', '7', '10', '31', '36', '37'))

    def __init__ (self, dir) :
        tracker    = instance.open (dir)
        self.db    = db = tracker.open ('admin')
        self.now   = Date ('.')
        udids      = db.user_dynamic.getnodeids (retired = False)
        self.by_u  = {}
        self.freez = {}
        for udid in udids :
            dyn = db.user_dynamic.getnode (udid)
            if not dyn.all_in :
                continue
            if dyn.max_flexitime is not None :
                continue
            if dyn.valid_to and dyn.valid_to <= self.year :
                continue
            if dyn.org_location not in self.olo :
                continue
            username = db.user.get (dyn.user, 'username')
            if username not in self.by_u :
                self.by_u [username] = []
            self.by_u [username].append (dyn)
    # end def __init__

    def thaw (self, username) :
        db  = self.db
        uid = db.user.lookup (username)
        props = \
            ( 'date'
            , 'achieved_hours'
            , 'balance'
            , 'month_balance'
            , 'week_balance'
            )
        d   = dict \
            ( user   = uid
            , date   = '%s;' % self.year.pretty ('%Y-%m-%d')
            , frozen = True
            )
        frs = db.daily_record_freeze.filter (None, d, ('-', 'date'))
        assert username not in self.freez
        self.freez [username] = {}
        for frid in frs :
            fr = db.daily_record_freeze.getnode (frid)
            self.freez [username][frid] = dict ((p, fr [p]) for p in props)
            self.db.daily_record_freeze.set (frid, frozen = False)
    # end def thaw

    def freeze (self, username) :
        srt = lambda x : self.freez [username][x]['date']
        for frid in sorted (self.freez [username], key = srt) :
            self.db.daily_record_freeze.set (frid, frozen = True)
            fr = self.db.daily_record_freeze.getnode (frid)
            for k in self.freez [username][frid] :
                uf = self.freez [username][frid][k]
                if uf != fr [k] :
                    print "DIFFER: %s %s %s" % (k, uf, fr [k])
    # end def freeze

    def fix_flexitime (self) :
        db = self.db
        for username in sorted (self.by_u) :
            to_split = 0
            for dyn in self.by_u [username] :
                if dyn.valid_from < self.year :
                    to_split += 1
                    assert to_split == 1
                    self.thaw (username)
                    d = dict \
                        ((k, dyn [k]) for k in db.user_dynamic.properties
                        if dyn [k] is not None
                        )
                    d ['valid_from']    = self.year
                    d ['max_flexitime'] = self.maxflex
                    # If dyn.valid_to is None, valid_to is set for the
                    # existing record, we need to set explicitly if
                    # non-empty.
                    if dyn.valid_to :
                        db.user_dynamic.set (dyn.id, valid_to = self.year)
                    print ("Creating user_dynamic: %s %s-%s" % \
                        (username, d ['valid_from'], d.get ('valid_to')))
                    db.user_dynamic.create (**d)
                    self.freeze (username)
                else :
                    print ("Setting user_dynamic%s: %s %s-%s" % \
                        (dyn.id, username, dyn.valid_from, dyn.valid_to))
                    db.user_dynamic.set (dyn.id, max_flexitime = self.maxflex)
    # end def fix_flexitime

    def close (self) :
        self.db.commit ()
    # end def close

# end class User_Dyn_Flexifixer

dir = os.getcwd ()
ff  = User_Dyn_Flexifixer (dir)
ff.fix_flexitime ()
ff.close ()
