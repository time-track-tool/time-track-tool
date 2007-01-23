#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
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
#--

from roundup.cgi.templating         import MultilinkHTMLProperty     \
                                         , BooleanHTMLProperty       \
                                         , DateHTMLProperty          \
                                         , _HTMLItem                 \
                                         , propclasses, MissingValue
from roundup.cgi.TranslationService import get_translation
from xml.sax.saxutils               import quoteattr as quote
from roundup.hyperdb                import Link, Multilink

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

def prop_as_array (prop) :
    if isinstance (prop, MultilinkHTMLProperty) :
        return prop
    return [prop]
# end def prop_as_array

formattable = \
    [ ('end',  'canc', 'run')
    , ('open', 'open', 'closed')
    ]
def get_cssclass (item) :
    """
        returns css link-class: for "end" date we need a special
        color code for marking abos that are no longer valid.
    """
    for i, t, f in formattable :
        try :
            return (t, f) [not item [i]]
        except KeyError :
            pass
    return ''
# end def get_cssclass

class ExtProperty :
    """
        An extended HTML property.

        ExtProperty items can come from the index page for
        a class (an entry in "props" for the search_display macro).
        They are then filled with the HTMLItems resulting from the
        search results.

        utils: utils from templating, used to navigate to other functions
        prop: The HTMLProperty
        item: Optional parent HTMLItem, can also be added later.
            This is the item of which the given prop is a property.
        get_cssclass: optional function for getting css class for
            formatting, takes the HTMLItem as single parameter
        pretty: optional pretty-printing function (defaults to _)
        multiselect: Show property as a multiselect in search-box
            used by html rendering in template
        is_labelprop: Render this property as a link to item -- usually
            done for labelprop of item and for id
        editable: Render property as an editable property (e.g. field)
        add_hidden: Add a hidden attribute in addition to the link
        searchable: Usually a safe bet if this can be searched for, can
            be overridden when you know what you're doing.
        displayprop: Name of the property to display. Only used
            internally, should not be used in the external interface
            (e.g., in a search mask) because the value will not show up
            in the generated URL and therefore will not work in CSV
            export.
            Testcases:
            abo.setlabelprop ('id')
            and
            abo.setlabelprop ('abotype')
            must both work.
        filter: A dictionary of properties / values to filter on when
            displaying a menu (in a search mask) or help.
        help_filter: deprecated, a string of property/value pairs
            usually computed from filter and used in classhelp

        Internal attributes:
        name: name of the property
        key: key attribute
        label: label of the field in html.
        i18nlabel: i18n translated label

    """
    def __init__ \
        ( self
        , utils
        , prop
        , item          = None
        , searchname    = None
        , label         = None
        , displayprop   = None
        , multiselect   = None
        , is_labelprop  = None
        , editable      = None
        , add_hidden    = False
        , searchable    = None # usually computed, override with False
        , sortable      = None
        , pretty        = _
        , get_cssclass  = get_cssclass
        , do_classhelp  = None
        , fieldwidth    = 30
        , format        = None
        , filter        = None
        , help_props    = None
        , help_filter   = None
        , help_sort     = None
        , bool_tristate = True
        ) :
        self.utils         = utils
        self.prop          = prop
        self.item          = item
        self.classname     = prop._classname
        self.klass         = prop._db.getclass (self.classname)
        self.name          = prop._name
        self.add_hidden    = add_hidden
        self.searchname    = searchname
        self.label         = label
        self.displayprop   = displayprop
        self.multiselect   = multiselect
        self.is_labelprop  = is_labelprop
        self.pretty        = pretty or _
        self.get_cssclass  = get_cssclass
        self.editable      = editable
        self.key           = None
        self.searchable    = searchable
        self.sortable      = sortable
        self.do_classhelp  = do_classhelp
        self.fieldwidth    = fieldwidth
        self.format        = format
        self.filter        = filter
        self.help_props    = help_props or []
        self.help_filter   = help_filter
        self.help_sort     = help_sort
        self.bool_tristate = bool_tristate
        self.propname      = displayprop
        if self.sortable is None :
            self.sortable = not isinstance (self.prop, MultilinkHTMLProperty)
        if isinstance (self.prop, MissingValue) :
            self.name = ''
        if not self.searchname or isinstance (searchname, MissingValue) :
            self.searchname = self.name
        if not self.label :
            self.label = self.searchname
        if not self.get_cssclass :
            if hasattr (self.utils, 'get_cssclass') :
                self.get_cssclass = self.utils.get_cssclass
            else :
                self.get_cssclass = lambda a : ""
        if not self.filter :
            self.filter = {}
        if not self.help_filter and self.filter :
            f = []
            for k, v in self.filter.iteritems () :
                if isinstance (v, list) :
                    v = ','.join (str (v))
                f.append ((k, v))
            self.help_filter = ' '.join ('%s=%s' % (k, v) for k, v in f)
        self.lnkcls = None

        self.helpcls  = self.classname
        self.helpname = self.name
        if self.is_link_or_multilink :
            if self.searchname :
                proptree = self.klass._proptree ({self.searchname : 1})
                props = [p for p in proptree]
                p = props [-1]
                if not p.classname :
                    if not self.propname :
                        self.propname = p.name
                    p = p.parent
                self.lnkcls = p.cls
                if len (props) > 1:
                    self.helpcls  = props [-2].classname
                    self.helpname = props [-1].name
            else :
                self.lnkcls = prop._db.getclass (prop._prop.classname)
            self.key     = self.lnkcls.getkey ()
        self.i18nlabel = self.pretty \
            (self.utils.combined_name
                (self.helpcls, self.helpname, self.searchname)
            )
        if self.do_classhelp is None :
            self.do_classhelp = \
                (   self.lnkcls
                and (  not self.propname
                    or self.propname in ('id', self.lnkcls.labelprop ())
                    )
                )
        if self.lnkcls and not self.propname :
            self.propname = self.lnkcls.labelprop ()
        if self.searchable is None :
            self.searchable = not self.need_lookup ()
        if (   self.is_labelprop is None
           and (  self.name == 'id'
               or self.name == self.klass.labelprop ()
               )
           ) :
            self.is_labelprop = 1
        if self.item :
            self.prop = item [self.name]
    # end def __init__

    def _is_link_or_multilink (self) :
        return hasattr (self.prop._prop, 'classname')
    is_link_or_multilink = property (_is_link_or_multilink)

    def _set_item (self, item = None) :
        if item :
            self.item = item
            self.prop = item [self.name]
    # end def _set_item

    def formatted (self, item = None) :
        self._set_item (item)
        if self.prop is None or isinstance (self.prop, MissingValue) :
            return ""
        if self.displayprop :
            format = self.format or '%s'
            return format % str (self.item [self.displayprop])
        if isinstance (self.prop, DateHTMLProperty) :
            format = self.format or '%Y-%m-%d'
            return self.prop.pretty (format)
        if self.format :
            return self.format % self.item [self.name]
        return str (self.prop)
    # end def formatted

    def need_lookup (self) :
        """ Needs a list-lookup, because the user can't specify the key """
        return self.propname and not self.key
    # end def need_lookup

    def as_listentry (self, item = None, as_link = True) :
        self._set_item (item)
        if self.editable and self.item [self.name].is_edit_ok () :
            return self.editfield ()
        if self.is_labelprop :
            return self.formatlink (as_link = as_link)
        elif self.lnkcls :
            if isinstance (self.prop, MultilinkHTMLProperty) :
                props = [i for i in self.prop]
                return ", ".join \
                    ([self.deref (p).formatlink (as_link = as_link)
                      for p in props
                    ])
            else :
                return self.deref ().formatlink (as_link = as_link)
        else :
            return self.formatted ()
    # end def as_listentry

    as_html = as_listentry

    def deref (self, prop = None) :
        """
            from an item get the property prop. This does some recursive
            magic: If prop consists of a path across several other Link
            properties, we dereference the whole prop list.
            Returns the new ExtProperty.
            There is a special case for 'id': The 'id' will not return a
            HTMLProperty but a python string. Therefore we return the
            labelprop and set the displayprop to 'id'.
        """
        p = prop or self.prop

        if self.propname == 'id' :
            lp = self.lnkcls.labelprop ()
            if lp == 'id' :
                lp = 'creation'
            return self.__class__ \
                ( self.utils, p [lp]
                , item         = p
                , pretty       = self.pretty
                , get_cssclass = self.get_cssclass
                , displayprop  = 'id'
                )
        for i in self.searchname.split ('.')[1:] :
            last_p = p
            p      = p [i]
        if  (   self.propname
            and (isinstance (p, _HTMLItem) or hasattr (p._prop, 'classname'))
            ) :
            last_p = p
            p      = p [self.propname]
        return self.__class__ \
            ( self.utils, p
            , item         = last_p
            , pretty       = self.pretty
            , get_cssclass = self.get_cssclass
            )
    # end def deref

    def formatlink (self, item = None, as_link = True) :
        """
            Render my property of an item as a link to this item (unless
            as_link is False). We get the item. The name of the item and
            its id are computed.
        """
        i = item or self.item
        hidden = ""
        if self.add_hidden :
            hidden = """<input name="%s" value="%s" type="hidden"/>""" \
                % (self.searchname, str (self.prop))
        if not i.is_view_ok () or not as_link :
            return hidden + self.formatted ()
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
        """ Render as menu if condition, otherwise formatlink to prop """
        if self.editable :
            return self.prop.menu ()
        return self.deref ().formatlink ()
    # end def menu

    def editfield (self) :
        return "<span style='white-space:nowrap'>%s</span>" \
            % self.item [self.name].field (size = self.fieldwidth)
    # end def editfield

    def menu_or_field (self, db) :
        prop = self.prop
        if self.is_link_or_multilink :
            if prop._prop.classname == 'user' :
                return ' '.join \
                    (( prop.field (size = 60)
                    ,  db.user.classhelp \
                        ( 'username,lastname,firstname,nickname'
                        , property=self.searchname
                        , inputtype='%s' % ('radio', 'checkbox')
                          [isinstance (self.prop, MultilinkHTMLProperty)]
                        , width='600'
                        , pagesize=500
                        , filter='status=%s' % ','.join
                           (db._db.user_status.lookup (i)
                            for i in ('valid', 'system')
                           )
                        )
                    ))
            return prop.menu (height=5)
        try :
            return prop.field (size=self.fieldwidth)
        except TypeError :
            pass
        return prop.field ()
    # end def menu_or_field

    def colonlabel (self, delimiter = ':') :
        return self.utils.fieldname \
            (self.helpcls, self.helpname, self.label, delimiter, 'header')
    # end def colonlabel

    def colonfield (self, item = None) :
        return """%s&nbsp;%s""" % (self.colonlabel (), self.as_listentry (item))
    # end def colonfield

    def classhelp_properties (self, *propnames) :
        """create list of properties for classhelp. Order matters."""
        assert (self.lnkcls)
        if self.propname == self.key or self.propname == 'id' :
            p = [self.propname]
        else :
            p = ['id', self.propname]
        props = dict ([(x, 1) for x in p])
        for pn in self.help_props :
            if (   pn in self.lnkcls.properties
               and pn != self.propname
               and pn not in props
               ) :
                p.append (pn)
                props [pn] = 1
        for pn in propnames :
            if (   pn in self.lnkcls.properties
               and pn != self.propname
               and pn not in props
               ) :
                p.append (pn)
                props [pn] = 1
        return ','.join (p)
    # end def classhelp_properties

    def pretty_ids (self, idstring) :
        if not idstring or idstring == '-1' or not self.key :
            return idstring
        ids = idstring.split (',')
        try :
            ids = [self.lnkcls.lookup (i) for i in ids]
        except KeyError :
            pass
        return ",".join ([self.lnkcls.get (i, self.key) for i in ids])
    # end def pretty_ids

    def _propstring (self) :
        return "%s%s@%s" % (self.classname, self.item.id, self.name)
    # end def _propstring

    def search_input (self, request) :
        value = request.form.getvalue (self.searchname) or ''
        if isinstance (self.prop, BooleanHTMLProperty) :
            yvalue = value == 'yes'
            nvalue = value == 'no'
            s = [ """<input type="radio" name="%s" value="yes"%s>%s"""
                  """<input type="radio" name="%s" value="no"%s>%s"""
                % ( self.searchname
                  , ['', ' checked="checked"'] [yvalue]
                  , self.pretty ('Yes')
                  , self.searchname
                  , ['', ' checked="checked"'] [nvalue]
                  , self.pretty ('No')
                  )
                ,
                ]
            if self.bool_tristate :
                s.append \
                    ( """<input type="radio" name="%s" value=""%s>%s"""
                    % ( self.searchname
                      , ['', ' checked="checked"'] [not (yvalue or nvalue)]
                      , self.pretty (''"Don't care")
                      )
                    )
            return ''.join (s)
        return \
            ( """<input type="text" size="40" value="%s" name="%s">"""
            % (self.pretty_ids (value), self.searchname)
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
            , title    = self.i18nlabel
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
    from urllib import quote as urlquote
    global _
    _ = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.tracker_home).gettext
    instance.registerUtil ('ExtProperty',       ExtProperty)
    instance.registerUtil ('sorted_properties', sorted_properties)
    instance.registerUtil ('properties_dict',   properties_dict)
    instance.registerUtil ('new_property',      new_property)
    instance.registerUtil ('comment_edit',      comment_edit)
    instance.registerUtil ('urlquote',          urlquote)
    instance.registerUtil ('prop_as_array',     prop_as_array)
    instance.registerUtil ('get_cssclass',      get_cssclass)
# end def init
