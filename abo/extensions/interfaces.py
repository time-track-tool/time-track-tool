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

class SearchAttribute :
    """
        util:  instance of TemplatingUtils
        name:  name of the attribute of the item to be displayed in the
               search.
        label: label of the field in html.
        lnkcls, lnkattr: applies to Link and Multilink properties
        only and give the class to which the link points and the
        attribute to display for this class.

        SearchAttribute items will come from the index page for
        a class (an entry in "props" for the search_display macro).
    """
    def __init__ \
        ( self
        , util
        , prop
        , item        = None
        , selname     = None
        , label       = None
        , lnkcls      = None
        , lnkattr     = None
        , multiselect = None
        , is_label    = None
        , editable    = None
        ) :
        self.util        = util
        self.prop        = prop
        self.item        = item
        self.classname   = prop._classname
        self.klass       = prop._db.getclass (self.classname)
        self.name        = prop._name
        self.selname     = selname
        self.label       = label
        self.lnkname     = None
        self.lnkattr     = lnkattr
        self.multiselect = multiselect
        self.is_label    = is_label
        self.editable    = editable
        self.key         = None
        if hasattr (prop._prop, 'classname') :
            self.lnkname = prop._prop.classname
            self.lnkcls  = prop._db.getclass (self.lnkname)
            self.key     = self.lnkcls.getkey ()
        if not self.selname :
            self.selname = self.name
            if self.lnkattr :
                l = self.lnkattr.split ('.')
                if len (l) > 1 :
                    self.selname = l [-2]
        if not self.label :
            self.label = self.util.pretty (self.selname)

        if self.lnkname and not self.lnkattr :
            self.lnkattr = self.lnkcls.labelprop ()
        if (   self.is_label is None
           and (  self.name == 'id'
               or self.klass.labelprop () == self.classname
               )
           ) :
            self.is_label = 1
        if self.item :
            self.hprop = item [self.name]
    # end def __init__

    def as_listentry (self, item) :
        self.item  = item
        self.hprop = item [self.name]
        if self.editable :
            return self.editfield ()
        if self.is_label :
            return self.formatlink ()
        elif self.lnkname :
            if isinstance (self.hprop, MultilinkHTMLProperty) : 
                return ", ".join \
                    ([ self.deref (i).formatlink ()
                       for i in range (len (self.hprop))
                    ])
            else :
                return self.deref ().formatlink ()
        return str (self.hprop)
    # end def as_listentry

    def deref (self, index = None) :
        """
            from an item get the property prop. This does some recursive
            magic: If prop consists of a path across several other Link
            properties, we dereference the whole prop list.
            Returns the new SearchAttribute.
        """
        p = self.hprop
        if index is not None : p = self.hprop [index]
        for i in self.lnkattr.split ('.') :
            last_p = p
            p      = p [i]
        return self.util.SearchAttribute (self.util, p, item = last_p)
    # end def deref

    def sortable (self) :
        return self.key == self.lnkattr
    # def sortable

    def formatlink (self) :
        """
            Render my property of an item as a link to this item. We get
            the item. The name of the item and its id are computed.
        """
        i = self.item
        return """<a class="%s" href="%s%s">%s</a>""" \
            % (self.util.linkclass (i), self.classname, i.id, self.hprop)
    # end def formatlink

    def editfield (self) :
        return "<span style='white-space:nowrap'>%s</span>" \
            % self.item [self.name].field ()
    # end def editfield

# end class SearchAttribute

def sorted_properties (self, db, context) :
    props = db [context._classname].properties ()
    props.sort (propsort)
    return props

def properties_dict (self, db, context) :
    props = {}
    for prop in db [context._classname].properties () :
        props [prop._name] = prop
    return props

def fieldname (self, name) :
    return "%s&nbsp;" % pretty (name)

def colonfield (self, klass, name) :
    return "%s:&nbsp;%s" % (pretty (name), str (klass [name]))

def linkclass (self, item) :
    """
        returns css link-class: for "end" date we need a special
        color code for marking abos that no longer valid.
    """
    try :
        return ('canc','run') [not item.end.plain()]
    except AttributeError :
        pass
    return ''

def menu_or_field (self, prop) :
    if hasattr (prop._prop, 'classname') :
        return prop.menu (height=5)
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

def init (instance)
    reg = instance.registerUtil
    reg ('sorted_properties', sorted_properties)
    reg ('properties_dict',   properties_dict)
    reg ('SearchAttribute',   SearchAttribute)
    reg ('fieldname',         fieldname)
    reg ('colonfield',        colonfield)
    reg ('linkclass',         linkclass)
    reg ('menu_or_field',     menu_or_field)
