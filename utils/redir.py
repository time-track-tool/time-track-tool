#!/usr/local/bin/python

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import os

content = \
"""
<html>
<head>
  <meta HTTP-EQUIV="expires" content="0">
  <meta HTTP-EQUIV="refresh" content="5; URL=%(url)s ">
    <title>Weiterleitung Roundup</title>
</head>
<body>
  <p>
    <a href="%(url)s">
     Neuer Roundup LINK
     --
     NEW Roundup LINK
    </a>
  </p>
  <p>
        Roundup ist umgezogen. Bitte neuen Link verwenden!
        Wir versuchen sie in einigen Sekunden weiterzuleiten.
  </p>
  <p>
        Roundup has moved. Please use the new link!
        We try to redirect you in a few seconds.
  </p>
  <p>
        %(debug)s
  </p>
</body>
</html>
"""

#old =  'http://tttroundup.vie.at.tttech.ttt:8080/tttech/'
old =  '/tttech'
new =  'https://time-tracker.vie.at.tttech.ttt/ttt'

class Handler (BaseHTTPRequestHandler) :
    def do_GET (self) :
        url = new + '/'
        if self.path.startswith (old) :
            url = new + self.path.replace (old, '', 1)
        debug = '' # self.path + ' ' + url
        self.send_response (400)
        self.send_header   ('Content-Type', 'text/html')
        self.end_headers   ()
        self.wfile.write   (content % locals ())
    # end def do_GET
# end class Handler

httpd = HTTPServer (('', 8080), Handler)
httpd.serve_forever()

#print 'Content-Type: text/plain\n\n'
#for k, v in os.environ.iteritems () :
#    print "%20s: %s" % (k, v)
