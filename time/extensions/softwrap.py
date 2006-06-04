#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
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
from roundup.cgi.TranslationService import get_translation

_ = str

CUTOFF     = re.compile ("(.*?)(\s+\S+)$")
NL         = re.compile ("\r?\n")
LEADWSWORD = re.compile ('(\s*\S+)')

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
    global _
    _ = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.tracker_home).gettext
    instance.registerUtil ('soft_wrap',       soft_wrap)
    instance.registerUtil ('truncate_chars',  truncate_chars)
# end def init
