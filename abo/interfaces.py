#
# Copyright (c) 2001 Bizar Software Pty Ltd (http://www.bizarsoftware.com.au/)
# This module is free software, and you may redistribute it and/or modify
# under the same terms as Python, so long as this copyright message and
# disclaimer are retained in their original form.
#
# IN NO EVENT SHALL BIZAR SOFTWARE PTY LTD BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING
# OUT OF THE USE OF THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# BIZAR SOFTWARE PTY LTD SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS"
# BASIS, AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#
# $Id$

from roundup import mailgw
from roundup.cgi import client
import re
import cgi
import copy
import time

CUTOFF = re.compile ("(.*?)(\s+\S+)$")

def _splitline (line, width) :
    line = line.rstrip ()
    if len (line) <= width:
        return line + "\n"
    else:
        rem = ""
        while 1:
            # try to cut something off
            m = CUTOFF.match (line)
            if m:
                lin = m.groups()[0]
                rem = m.groups()[1] + rem
                if len (lin) <= width:
                    return lin + "\n" + \
                           _splitline (rem.strip (), width)
                else:
                    # try to cut off the next piece
                    line = lin
            else:
                return line + "\n" + _splitline (rem.strip (), width)

class Client(client.Client):
    ''' derives basic CGI implementation from the standard module,
        with any specific extensions
    '''
    pass

class TemplatingUtils:
    ''' Methods implemented on this class will be available to HTML templates
        through the 'utils' variable.
    '''

    def soft_wrap (self, str, width=80) :
        """just insert \n's after max 'length' characters

        and split on word boundaries ;-)
        """

        result   = ""
        lines    = re.split ("\r?\n", str)

        for line in lines :
            result += _splitline (line, width)
        return result

    def truncate_chars(self, str, max_chars=40, append=''):
        """truncates a String on a word boundary.

        max_chars specifies number of max chars. note that the string will
        be smaller than max_chars. If no whitespace can be found, the string
        will be cut off at max_chars.

        if append is specified, the length of append will be subtracted from max_chars
        if string is longer than max_chars, and append gets appended to the
        result. usually append could be ' ...'
        """

        result = ""
        real_append = ""
        if str:
            if len(str) > max_chars:
                if len(append) < max_chars:
                    max_chars = max_chars - len(append)
                    real_append = append

            parts = re.findall('(\s*)(\S*)',str)
            for (ws, c) in parts:
                if len(result) + len(ws) + len(c) > max_chars:
                    break
                else:
                    result = result + ws + c

            if not result:
                result = str[:max_chars]

        return result + real_append

    def url_2_dict (self, url) :
        url_dict = cgi.parse_qs (url)
        result = { "sort"      : None
                 , "group"     : None
                 , "filter"    : []
                 , "columns"   : []
                 , "filterspec": {}
                 , "pagesize"  : 20
                 , "queryname" : ""
                 }
        for k, v in url_dict.items () :
            v = v[0]
            if k in (":sort", ":group") :
                if v[0] == "-" :
                    result [k[1:]] = ("-", v[1:])
                else:
                    result [k[1:]] = ("", v)
            elif k == "queryname" :
                result ["queryname"] = v
            elif k in (":pagesize", ":startwith") :
                result [k[1:]] = int (v)
            elif k[0] != ":" :
                result ["filterspec"] [k] = v.split(",")
            else :
                result [k[1:]] = v.split(",")
        return result

    def user_list_to_named_list (self, userlist) :
        result = []
        if type (userlist) == type ("") :
            for user in userlist.split (",") :
                if user.isdigit () :
                    # convert to name
                    result.append (self.client.db.user.get (user, "username"))
                else:
                    result.append (user)
        return ",".join (result)

class MailGW(mailgw.MailGW):
    ''' derives basic mail gateway implementation from the standard module,
        with any specific extensions
    '''
    pass

# vim: set filetype=python ts=4 sw=4 et si
#SHA: 231e956e0e973fbc52fc70761328664493fb68a9
