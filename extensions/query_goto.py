#! /usr/bin/python
# Copyright (C) 2004-21 Dr. Ralf Schlatterbeck Open Source Consulting.
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

#++
# Name
#    query_goto
#
# Purpose
#    Action for redirecting to the view of a query
#--

from roundup.cgi.actions    import Action
from roundup.cgi            import templating
from roundup                import hyperdb
from roundup.cgi.exceptions import Redirect


class Query_Goto (Action) :

    def handle (self) :
        ''' Export the specified search query as CSV. '''
        # figure the request
        request    = self.request = templating.HTMLRequest     (self.client)
        filterspec = request.filterspec
        sort       = request.sort
        group      = request.group
        klass      = self.klass = self.db.getclass (request.classname)
        assert (request.classname == 'query')
        id         = self.client.nodeid
        query = klass.getnode (id)
        raise Redirect \
            ("%s?%s&@old-queryname=%s&@queryname=%s"
            % (query.klass, query.url, query.name, query.name)
            )
    # end def handle

# end class Query_Goto

def init (instance) :
    instance.registerAction ('query_goto',     Query_Goto)
# end def init
