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
#    extproperty
#
# Purpose
#    Extended properties for roundup templating
#
# Revision Dates
#     6-Jun-2005 (RSC) Moved from another project
#     8-Jun-2005 (RSC) Several convenience functions added.
#    ««revision-date»»···
#--

from roundup.cgi.templating         import MultilinkHTMLProperty     \
                                         , BooleanHTMLProperty       \
                                         , DateHTMLProperty          \
                                         , propclasses, MissingValue
from roundup.cgi.TranslationService import get_translation
from xml.sax.saxutils               import quoteattr as quote

_ = None

def propsort (p1, p2) :
    return cmp (_ (p1._name), _ (p2._name))
# end def propsort

def sorted_properties (db, context) :
    props = db [context._classname].properties ()
    props.sort (propsort)
    return props
# end def sorted_properties

def properties_dict (db, context) :
    props = {}
    for prop in db [context._classname].properties () :
        props [prop._name] = prop
    return props
# end def properties_dict

def menu_or_field (prop) :
    if hasattr (prop._prop, 'classname') :
        return prop.menu (height=5)
    return prop.field (60)
# end def menu_or_field

dwidth  = 550
dheight = 220
#dwidth  = 460
#dheight = 190
def comment_edit \
    ( klass
    , property
    , width    = dwidth
    , height   = dheight
    , value    = ""
    , form     = "itemSynopsis"
    , title    = "Comment"
    , editable = False
    ) :
    """ Create a hidden field for this item with proper contents and
        a javascript link for editing the content property.
    """
    return ( """<input type="hidden" name="%s" value=%s> """
             """<a class="classhelp" """
             """href="javascript:help_window """
             """('%s?@template=comment"""
             """&property=%s&editable=%s"""
             """&form=%s', %d, %d)">"""
             """<img src="@@file/comment.png" alt="C" title="%s" border="0">"""
             """</a>"""
             % ( property
               , quote (str (value))
               , klass
               , property
               , ('1','')[not editable]
               , form
               , width
               , height
               , title
               )
           )
# end def comment_edit

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
        , item          = None
        , selname       = None
        , label         = None
        , lnkcls        = None
        , lnkattr       = None
        , multiselect   = None
        , is_label      = None
        , editable      = None
        , searchable    = None # usually computed, override with False
        , pretty        = _    # optional pretty-printing function
        , linkclass     = None # optional function for getting css class
        , do_classhelp  = None
        , fieldwidth    = None
        , format        = None
        , help_props    = None
        , help_filter   = None
        , bool_tristate = True
        ) :
        self.utils         = utils
        self.prop          = prop
        self.item          = item
        self.classname     = prop._classname
        self.klass         = prop._db.getclass (self.classname)
        self.name          = prop._name
        self.selname       = selname
        self.label         = label
        self.lnkcls        = lnkcls
        self.lnkname       = None
        self.lnkattr       = lnkattr
        self.multiselect   = multiselect
        self.is_label      = is_label
        self.pretty        = pretty or _
        self.get_cssclass  = linkclass
        self.editable      = editable
        self.key           = None
        self.searchable    = searchable
        self.do_classhelp  = do_classhelp
        self.fieldwidth    = fieldwidth
        self.format        = format
        self.help_props    = help_props or []
        self.help_filter   = help_filter
        self.bool_tristate = bool_tristate
        if not self.get_cssclass :
            if hasattr (self.utils, 'linkclass') :
                self.get_cssclass = self.utils.linkclass
            else :
                self.get_cssclass = lambda a : ""
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
            if self.selname :
                self.label = self.pretty (self.selname)
            else :
                self.label = ''
        if self.lnkname and not self.lnkattr :
            self.lnkattr = self.lnkcls.labelprop ()
        if self.do_classhelp is None :
            self.do_classhelp = self.lnkname
        if self.searchable is None :
            self.searchable = not self.need_lookup ()
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

    def formatted (self) :
        if self.hprop is None or isinstance (self.hprop, MissingValue) :
            return ""
        elif isinstance (self.hprop, DateHTMLProperty) :
            if self.format :
                format = self.format
            else :
                format = '%Y-%m-%d'
            return self.hprop.pretty (format)
        elif self.format :
            return self.format % self.item [self.name]
        if self.lnkattr :
            return str (self.item [self.lnkattr])
        return str (self.hprop)
    # end def formatted

    def need_lookup (self) :
        """ Needs a list-lookup, because the user can't specify the key """
        return self.lnkattr and not self.key
    # end def need_lookup

    def as_listentry (self, item = None, add_hidden = False) :
        self._set_item (item)
        if self.editable and self.item [self.name].is_edit_ok () :
            return self.editfield ()
        if self.is_label :
            return self.formatlink (add_hidden = add_hidden)
        elif self.lnkname :
            if isinstance (self.hprop, MultilinkHTMLProperty) :
                hprops = [i for i in self.hprop]
                return ", ".join \
                    ([self.deref (p).formatlink (add_hidden = add_hidden)
                      for p in hprops
                    ])
            else :
                return self.deref ().formatlink (add_hidden = add_hidden)
        else :
            return self.formatted ()
    # end def as_listentry

    def deref (self, hprop = None) :
        """
            from an item get the property prop. This does some recursive
            magic: If prop consists of a path across several other Link
            properties, we dereference the whole prop list.
            Returns the new ExtProperty.
            There is a special case for 'id': The 'id' will not return a
            HTMLProperty but a python string. Therefore we return the
            labelprop and set the lnkattr to 'id'.
        """
        p = hprop or self.hprop

        if self.lnkattr == 'id' :
            return self.__class__ \
                ( self.utils, p [self.lnkcls.labelprop ()]
                , item = p
                , pretty = self.pretty
                , linkclass = self.get_cssclass
                , lnkattr = 'id'
                )
        for i in self.lnkattr.split ('.') :
            last_p = p
            p      = p [i]
        return self.__class__ \
            ( self.utils, p
            , item = last_p
            , pretty = self.pretty
            , linkclass = self.get_cssclass
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

    def formatlink (self, item = None, add_hidden = False) :
        """
            Render my property of an item as a link to this item. We get
            the item. The name of the item and its id are computed.
        """
        hidden = ""
        if add_hidden :
            hidden = """<input name="%s" value="%s" type="hidden"/>""" \
                % (self.classname, str (self.hprop))
        i = item or self.item
        if not i.is_view_ok () :
            return self.formatted ()
        if not self.classname :
            return ""
        return """<a class="%s" href="%s%s">%s</a>%s""" \
            % ( self.get_cssclass (i)
              , self.classname
              , i.id
              , self.formatted ()
              , hidden
              )
    # end def formatlink

    def menu (self) :
        """ Render as menu if condition, otherwise formatlink to hprop """
        if self.editable :
            return self.hprop.menu ()
        return self.deref ().formatlink ()
    # end def menu

    def editfield (self) :
        return "<span style='white-space:nowrap'>%s</span>" \
            % self.item [self.name].field (size = self.fieldwidth)
    # end def editfield

    def colonlabel (self) :
        return ("""<a class="header" title="Help for %s" """
                """href="javascript:help_window"""
                """('%s?:template=property_help#%s', '500', '400')">"""
                """%s:</a>"""
               % (self.label, self.classname, self.name, self.label)
               )
    # end def colonlabel

    def colonfield (self, item = None) :
        return """%s&nbsp;%s""" % (self.colonlabel (), self.as_listentry (item))
    # end def colonfield

    def classhelp_properties (self, *propnames) :
        assert (self.lnkcls)
        if self.lnkattr == self.lnkcls.getkey () :
            p = [self.lnkattr]
        else :
            p = ['id', self.lnkattr]
        props = dict ([(x, 1) for x in p])
        for pn in self.help_props :
            if (   pn in self.lnkcls.properties.keys ()
               and pn != self.lnkattr
               and pn not in props
               ) :
                p.append (pn)
                props [pn] = 1
        for pn in propnames :
            if (   pn in self.lnkcls.properties.keys ()
               and pn != self.lnkattr
               and pn not in props
               ) :
                p.append (pn)
                props [pn] = 1
        return ','.join (p)
    # end def classhelp_properties

    def pretty_ids (self, idstring) :
        if not idstring or idstring == '-1' or not self.lnkcls :
            return idstring
        key = self.lnkcls.getkey ()
        if not key :
            return idstring
        ids = idstring.split (',')
        try :
            ids = [self.lnkcls.lookup (i) for i in ids]
        except KeyError :
            pass
        return ",".join ([self.lnkcls.get (i, key) for i in ids])
    # end def pretty_ids

    def _propstring (self) :
        return "%s%s@%s" % (self.classname, self.item.id, self.name)
    # end def _propstring

    def search_input (self, request) :
        value = request.form.getvalue (self.selname) or ''
        if isinstance (self.hprop, BooleanHTMLProperty) :
            yvalue = value == 'yes'
            nvalue = value == 'no'
            s = [ """<input type="radio" name="%s" value="yes"%s>%s"""
                  """<input type="radio" name="%s" value="no"%s>%s"""
                % ( self.selname
                  , ['', ' checked="checked"'] [yvalue]
                  , self.pretty ('Yes')
                  , self.selname
                  , ['', ' checked="checked"'] [nvalue]
                  , self.pretty ('No')
                  )
                ,
                ]
            if self.bool_tristate :
                s.append \
                    ( """<input type="radio" name="%s" value=""%s>%s"""
                    % ( self.selname
                      , ['', ' checked="checked"'] [not (yvalue or nvalue)]
                      , self.pretty ("Don't care")
                      )
                    )
            return ''.join (s)
        return \
            ( """<input type="text" size="40" value="%s" name="%s">"""
            % (self.pretty_ids (value), self.selname)
            )
    # end def search_input

    def del_link (self, form) :
        """Generate a javascript delete link for the current item, to be
           used in a href
        """
        prop = self._propstring ()
        return \
            ("""javascript:"""
             """document.forms.%(form)s ['%(prop)s'].value = ' '; """
            % locals ()
            )
    # end def del_link

    def comment_edit \
        (self, width = dwidth, height = dheight, form = "itemSynopsis") :
        return comment_edit \
            ( self.classname
            , self._propstring ()
            , width
            , height
            , form     = form
            , value    = self.item [self.name]
            , title    = self.label
            , editable = self.editable
            )
    # end def comment_edit

# end class ExtProperty

def new_property (context, db, classname, id, propname) :
    kl     = db [classname]
    prop   = db [classname]._props [propname]
    for kl, hkl in propclasses :
        if isinstance (prop, kl) :
            return hkl (context._client, classname, id, prop, propname, None)
    return None
# end def new_property

def init (instance) :
    global _
    _ = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.tracker_home).gettext
    instance.registerUtil ('ExtProperty',       ExtProperty)
    instance.registerUtil ('sorted_properties', sorted_properties)
    instance.registerUtil ('properties_dict',   properties_dict)
    instance.registerUtil ('menu_or_field',     menu_or_field)
    instance.registerUtil ('new_property',      new_property)
    instance.registerUtil ('comment_edit',      comment_edit)
# end def init
