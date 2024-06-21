#!/usr/bin/python

import sys
import requests
import datetime
from bs4 import BeautifulSoup
from roundup.date import Date

sys.path.insert (1, 'utils')
import requester
urlencode = requester.urlencode

url = 'https://www.wien.gv.at/amtshelfer/feiertage/'

monthnames = \
    [ 'Jänner'
    , 'Februar'
    , 'März'
    , 'April'
    , 'Mai'
    , 'Juni'
    , 'Juli'
    , 'August'
    , 'September'
    , 'Oktober'
    , 'November'
    , 'Dezember'
    ]

english = dict \
    (( ('Allerheiligen',       "All Saint's Day")
    ,  ('Christi Himmelfahrt', 'Ascension Day')
    ,  ('Christtag',           'Christmas Day')
    ,  ('Fronleichnam',        'Corpus Christi')
    ,  ('Heiligabend',         'Christmas Eve')
    ,  ('Heilige Drei Könige', 'Epiphany')
    ,  ('Karfreitag',          'Good Friday')
    ,  ('Mariä Empfängnis',    'Immaculate Conception')
    ,  ('Mariä Himmelfahrt',   'Assumption')
    ,  ('Nationalfeiertag',    'National holiday')
    ,  ('Neujahr',             "New Year's Day")
    ,  ('Ostermontag',         'Easter Monday')
    ,  ('Ostersonntag',        'Easter Sunday')
    ,  ('Pfingstmontag',       'Whit Monday')
    ,  ('Pfingstsonntag',      'Whit Sunday')
    ,  ('Staatsfeiertag',      'Labour Day')
    ,  ('Silvester',           "New Year's Eve")
    ,  ('Stefanitag',          'Boxing Day')
    ))

olos = dict \
    ( TCAG = ['1', '7', '10', '41', '80', '84']
    , TAAG = ['36', '37']
    )

month_num = {}
for n, m in enumerate (monthnames):
    month_num [m] = n + 1

def try_create_ph (rq, dt, name):
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
    for tcname in olos:
        olo = olos [tcname]
        if loc_ph:
            print \
                ( 'Warning: Holiday on %s has locations'
                % (dt,)
                )
            continue
        if olo_ph.intersection (olo):
            print \
                ( 'Warning: Holiday on %s exists for %s'
                % (dt, tcname)
                )
            continue
        # now create it
        d = dict \
            ( name         = english.get (name, name)
            , description  = name
            , date         = dt
            , is_half      = 0
            , org_location = ','.join (olo)
            )
        rq.post ('public_holiday', json = d)
# end try_create_ph

def import_public_holidays (rq):
    ans = requests.get (url)
    if not (200 <= ans.status_code <= 299):
        raise RuntimeError \
            ( 'Invalid get result: %s: %s\n    %s'
            % (ans.status_code, ans.reason, ans.text)
            )
    soup = BeautifulSoup (ans.text, 'html.parser')
    for div in soup.find_all ('div'):
        cls = div.get ('class')
        if not cls or 'editableDocument' not in cls:
            continue
        year = None
        for item in div:
            txt = item.text
            if item.name == 'h2' and txt.startswith ('Feiertage im Jahr'):
                year = txt.split ()[-1]
                continue
            if item.name == 'ul' and year:
                for li in item.find_all ('li'):
                    if len (li) != 1:
                        print ('Unexpected content of <li>', file = sys.stderr)
                    for span in li.find_all ('span'):
                        name, date = span.text.split (':')
                        dayname, rest = (x.strip () for x in date.split (','))
                        day, rest = rest.split ('.')
                        day = int (day)
                        monthname, dyear = rest.split ()
                        month = month_num [monthname]
                        assert year == dyear
                        dt = '%s-%02d-%02d' % (year, month, day)
                        try_create_ph (rq, dt, name)
                        if name == 'Stefanitag':
                            dti = datetime.datetime.strptime (dt, '%Y-%m-%d')
                            dif = datetime.timedelta (days = 2)
                            dt  = (dti - dif).strftime ('%Y-%m-%d')
                            try_create_ph (rq, dt, 'Heiligabend')
                            dif = datetime.timedelta (days = 5)
                            dt  = (dti + dif).strftime ('%Y-%m-%d')
                            try_create_ph (rq, dt, 'Silvester')
                        if name in ('Ostermontag', 'Pfingstmontag'):
                            dti = datetime.datetime.strptime (dt, '%Y-%m-%d')
                            dti -= datetime.timedelta (days = 1)
                            dt  = dti.strftime ('%Y-%m-%d')
                            n   = name.replace ('montag', 'sonntag')
                            try_create_ph (rq, dt, n)
                            if name == 'Ostermontag':
                                # Subtract another 2 days
                                dti -= datetime.timedelta (days = 2)
                                dt  = dti.strftime ('%Y-%m-%d')
                                n   = 'Karfreitag'
                                try_create_ph (rq, dt, n)
# end import_public_holidays

def main (argv = sys.argv [1:]):
    cmd  = requester.get_default_cmd (argv)
    args = cmd.parse_args (argv)
    rq   = requester.Requester (args)
    import_public_holidays (rq)
# end def main

if __name__ == '__main__':
    main (sys.argv [1:])
