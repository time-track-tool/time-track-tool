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

from roundup.cgi.templating import MultilinkHTMLProperty, DateHTMLProperty

class ExtProperty :
    """
        An extended HTML property.
        name:  name of the attribute of the item to be displayed in the
               search.
        label: label of the field in html.
        lnkcls, lnkattr: applies to Link and Multilink properties
        only and give the class to which the link points and the
        attribute to display for this class.

        ExtProperty items can come from the index page for
        a class (an entry in "props" for the search_display macro).
    """
    def __init__ \
        ( self
        , utils
        , prop
        , item        = None
        , selname     = None
        , label       = None
        , lnkcls      = None
        , lnkattr     = None
        , multiselect = None
        , is_label    = None
        , editable    = None
        , searchable  = None # usually computed, override with False
        , pretty      = None # optional pretty-printing function
        , linkclass   = None # optional function for getting css class
        ) :
        self.utils       = utils
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
        self.pretty      = pretty or utils.pretty
        self.get_linkcls = linkclass
        self.editable    = editable
        self.key         = None
        self.searchable  = searchable
        if not self.get_linkcls :
            if hasattr (self.utils, 'linkclass') :
                self.get_linkcls = self.utils.linkclass
            else :
                self.get_linkcls = lambda a : ""
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
            self.label = self.pretty (self.selname)

        if self.lnkname and not self.lnkattr :
            self.lnkattr = self.lnkcls.labelprop ()
        if self.searchable is None or self.searchable :
            self.searchable = self.key or not self.lnkattr
        if (   self.is_label is None
           and (  self.name == 'id'
               or self.name == self.klass.labelprop ()
               )
           ) :
            self.is_label = 1
        if self.item :
            self.hprop = item [self.name]
        else :
            self.hprop = self.prop
    # end def __init__

    def _set_item (self, item = None) :
        if item :
            self.item  = item
            self.hprop = item [self.name]
    # end def _set_item

    def as_listentry (self, item = None) :
        self._set_item (item)
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
        elif isinstance (self.hprop, DateHTMLProperty) :
            return self.hprop.pretty ('%Y-%m-%d')
        return str (self.hprop)
    # end def as_listentry

    def deref (self, index = None) :
        """
            from an item get the property prop. This does some recursive
            magic: If prop consists of a path across several other Link
            properties, we dereference the whole prop list.
            Returns the new ExtProperty.
        """
        p = self.hprop
        if index is not None :
            # Looks like newer version do no longer support index.
            try :
                p = self.hprop [index]
            except AttributeError :
                p = [i for i in self.hprop][index]

        for i in self.lnkattr.split ('.') :
            last_p = p
            p      = p [i]
        return self.__class__ \
            ( self.utils
            , p
            , item = last_p
            , pretty = self.pretty
            , linkclass = self.get_linkcls
            )
    # end def deref

    def sortable (self) :
        """
            Check if it's a Link and has a key property and the key
            property is the current property -- or it's some other
            Non-Link property. It also doesn't make much sense to sort
            by Multilink.
        """
        if isinstance (self.hprop, MultilinkHTMLProperty) :
            return False
        return self.key == self.lnkattr
    # def sortable

    def formatlink (self, item = None) :
        """
            Render my property of an item as a link to this item. We get
            the item. The name of the item and its id are computed.
        """
        i = item or self.item
        return """<a class="%s" href="%s%s">%s</a>""" \
            % (self.get_linkcls (i), self.classname, i.id, self.hprop)
    # end def formatlink

    def menu (self) :
        """ Render as menu if condition, otherwise formatlink to hprop """
        if self.editable :
            return self.hprop.menu ()
        print "non-editable:"
        return self.formatlink (self.hprop)
    # end def menu

    def editfield (self) :
        return "<span style='white-space:nowrap'>%s</span>" \
            % self.item [self.name].field ()
    # end def editfield

    def colonfield (self, item = None) :
        return "%s:&nbsp;%s" % (self.label, self.as_listentry (item))
    # end def colonfield
# end class ExtProperty

def init (instance) :
    instance.registerUtil ('ExtProperty', ExtProperty)
