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
# $Id$

from roundup                import mailgw
from roundup.cgi            import client
from roundup.cgi.templating import MultilinkHTMLProperty
from roundup.rup_utils      import pretty
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

def propsort (p1, p2) :
    return cmp (pretty (p1._name), pretty (p2._name))

class Client(client.Client):
    ''' derives basic CGI implementation from the standard module,
        with any specific extensions
    '''
    pass

class TemplatingUtils:
    ''' Methods implemented on this class will be available to HTML templates
        through the 'utils' variable.
    '''

    def sorted_properties (self, db, context) :
        props = db [context._classname].properties ()
        props.sort (propsort)
        return props

    def pretty (self, name) :
        return pretty (name)

    def fieldname (self, name) :
        return "%s&nbsp;" % pretty (name)

    def colonfield (self, klass, name) :
        return "%s:&nbsp;%s" % (pretty (name), str (klass [name]))

    def linkclass (self, item) :
        try :
            return ('canc','run') [not item.end.plain()]
        except AttributeError :
            pass
        return ''

    def formatlink (self, hprop, item, name, id) :
        """
            render a property of an item as a link to this item. We get
            the property, the item, the name of the item and its id
            already pre-computed (although we could get everything from
            the item).
        """
        return """<a class="%s" href="%s%s">%s</a>""" \
            % (self.linkclass (item), name, id, hprop)

    def deref (self, item, prop) :
        """
            from an item get the property prop. This does some recursive
            magic: If prop consists of a path across several other Link
            properties, we dereference the whole prop list.
        """
        for i in prop.split ('.') :
            item = item [i]
        return item

    def listingprop (self, item, prop, labelprop, classname, edit = False) :
        """
            The "prop" attribute is a tuple consisting of at least 2 and
            at most 4 fields. The 0th item of the tuple is the label of
            the field in html. The 1st item is the name of the attribute
            of the item. The 3rd and 4th field apply to Link and
            Multilink properties only and give the name of the class to
            which the link points and the attribute to display for this
            class. The prop attribute will come from the index page for
            a class (an entry in "props" for the search_display macro).
        """
        f     = prop [1]
        hprop = item [f]
        l     = len (prop)
        if edit :
            return \
                "<span style='white-space:nowrap'>" + hprop.field () + "</span>"
        if f == labelprop or f == 'id' :
            return self.formatlink (hprop, hprop, classname, item.id)
        elif l > 2 :
            cln  = prop [2]
            attr = prop [3]
            if isinstance (hprop, MultilinkHTMLProperty) : 
                return ", ".join \
                    ([ self.formatlink
                           ( self.deref (hprop [i], attr)
                           , hprop [i]
                           , cln
                           , hprop._value [i]
                           )
                       for i in range (len (hprop))
                    ])
            else :
                return self.formatlink \
                    (self.deref (hprop, attr), hprop, cln, hprop._value)
        return hprop.plain ()

    def menu_or_field (self, prop) :
        if hasattr (prop._prop, 'classname') :
            return prop.menu ()
        return prop.field ()

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
