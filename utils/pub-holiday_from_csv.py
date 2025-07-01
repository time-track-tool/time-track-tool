#!/usr/bin/python

import sys
import requests
import datetime
from roundup.date import Date
from argparse import ArgumentParser
from csv import DictReader
from datetime import datetime

sys.path.insert (1, 'utils')
import requester
sys.path.insert (1, 'lib')
import common
urlencode = requester.urlencode

olo_map   = {'TTTech Deutschland GmbH; DEU, München' :
             'TTTech Deutschland GmbH; DEU, Taufkirchen'
            }
olo_names = {}

def try_create_ph (rq, dt, name, desc, olo, is_half):
    # Get ph on that date
    d  = dict (date = dt)
    d ['@fields'] = 'locations,org_location'
    phs = rq.get ('public_holiday?' + urlencode (d))
    phs = phs ['data']['collection']
    olo_ph = set ()
    loc_ph = set ()
    for ph in phs:
        olo_ph.update \
            (x ['id'] for x in ph ['org_location'])
        loc_ph.update \
            (x ['id'] for x in ph ['locations'])
    if loc_ph:
        print \
            ( 'Warning: Holiday on %s has locations'
            % (dt,)
            )
        return
    if olo in olo_ph:
        print \
            ( 'Warning: Holiday %s on %s exists for %s'
            % (name, dt, olo_names.get (olo, ''))
            )
        #return
    # now create it
    print ('Creating: %s on %s for %s' % (name, dt, olo_names [olo]))
    d = dict \
        ( name         = name
        , description  = desc
        , date         = dt
        , is_half      = is_half
        , org_location = olo
        )
    try:
        rq.post ('public_holiday', json = d)
    except RuntimeError as err:
        print (err)
# end try_create_ph

def main (argv = sys.argv [1:]):
    cmd = requester.get_default_cmd (argv)
    cmd.add_argument \
        ( 'filename'
        , nargs = 1
        )
    args = cmd.parse_args ()
    rq   = requester.Requester (args)

    assert len (args.filename) == 1
    with open (args.filename [0], 'r') as f:
        dr = DictReader (f, delimiter = ';')
        for rec in dr:
            if not rec ['Date']:
                break
            dt = datetime.strptime (rec ['Date'], '%d.%m.%Y')
            dt = dt.strftime (common.ymd)
            on = rec ['Organisation/Location']
            on = olo_map.get (on, on)
            olo = rq.get ('org_location?' + urlencode (dict (name = on)))
            olo = olo ['data']['collection']
            if len (olo) == 0:
                print ('Warning: non-existing olo: %s' % on)
                continue
            assert len (olo) == 1
            olo  = olo [0]
            olo  = olo ['id']
            olo_names [olo] = on
            name = rec ['Public Holiday (English Name)']
            desc = rec ['Public Holiday (German Name/Description)']
            assert rec ['Full or Half Day'] in ('Full Day', 'Half Day')
            is_half = rec ['Full or Half Day'] == 'Half Day'
            try_create_ph (rq, dt, name, desc, olo, is_half)
# end def main

if __name__ == '__main__':
    main (sys.argv [1:])
