#! /usr/bin/python
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    softwrap
#
# Purpose
#    utilities for displaying long lines (e.g. mail header)
#
# Revision Dates
#     4-Jun-2006 (RSC) Moved from old roundup tracker
#--

import re
from html import escape
from roundup.cgi.templating import StringHTMLProperty

CUTOFF     = re.compile (r"(.*?)(\s+\S+)$")
NL         = re.compile ("\r?\n")
LEADWSWORD = re.compile (r'(\s*\S+)')

def _splitline (line, width) :
    line = line.rstrip ()
    if len (line) <= width:
        return line
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
# end def _splitline

def soft_wrap (in_str, width=80) :
    """just insert \n's after max 'length' characters
       and split on word boundaries ;-)
    """
    result   = []
    if in_str :
        lines    = NL.split (in_str)
        for line in lines :
            result.append (_splitline (line, width))
    return '\n'.join (result)
# end def soft_wrap

def hyperlinked_soft_wrap (content, width = 120) :
    """ Wrap like in soft_wrap then hyperlink as in
        msg.content.hyperlinked.
    """
    s = soft_wrap  (content.plain (), width)
    s = escape (s)
    s = content.hyper_re.sub (content._hyper_repl, s)
    return s
# end def hyperlinked_soft_wrap

def truncate_chars(in_str, max_len=40, append=''):
    """truncates a String on a word boundary.

       note that the string will be smaller than max_len. If no
       whitespace can be found, the string will be cut off at max_len.

       if append is specified, the length of append will be subtracted
       from max _chars if string is longer than max_len, and append
       gets appended to the result. usually append could be ' ...'
    """
    result      = []
    real_append = ""
    in_str      = in_str or ""
    if len (in_str) > max_len :
        length  = 0
        if len (append) < max_len :
            max_len     -= len (append)
            real_append  = append
        words = LEADWSWORD.findall (in_str)
        for w in words :
            if length + len (w) > max_len :
                break
            else:
                result.append (w)
                length += len (w)
    result = ''.join (result)
    if not result:
        result = in_str [:max_len]
    return result + real_append
# end def truncate_chars


def init (instance) :
    instance.registerUtil ('soft_wrap',             soft_wrap)
    instance.registerUtil ('truncate_chars',        truncate_chars)
    instance.registerUtil ('hyperlinked_soft_wrap', hyperlinked_soft_wrap)
# end def init
