#! /usr/bin/python
# Copyright (C) 2006-21 Dr. Ralf Schlatterbeck Open Source Consulting.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from roundup.mailgw import parseContent
from roundup.date   import Date

def summarygenerator (db, cl, nodeid, newvalues) :
    ''' If the message doesn't have a summary, make one for it.
    '''
    if 'summary' in newvalues or 'content' not in newvalues :
        return

    summary, content = parseContent (newvalues ['content'], 1, 1)
    newvalues ['summary'] = summary
# end def summarygenerator

def check_params (db, cl, nodeid, newvalues) :
    """ Check if message has an author, use creator if not """
    if 'author' not in newvalues :
        newvalues ['author'] = db.getuid ()
    if 'date' not in newvalues :
        newvalues ['date'] = Date ('.')
# end def check_params

def init(db):
    # fire before changes are made
    db.msg.audit('create', summarygenerator)
    db.msg.audit('create', check_params)
