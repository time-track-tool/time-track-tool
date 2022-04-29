#! /usr/bin/python
# Copyright (C) 2006-10 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    extproperty
#
# Purpose
#    Extended properties for roundup templating
#
#--

from urllib                         import quote as urlquote
from roundup.cgi.templating         import MultilinkHTMLProperty     \
                                         , BooleanHTMLProperty       \
                                         , DateHTMLProperty          \
                                         , StringHTMLProperty        \
                                         , _HTMLItem                 \
                                         , HTMLClass                 \
                                         , HTMLProperty              \
                                         , propclasses, MissingValue
from xml.sax.saxutils               import quoteattr as quote
from roundup.hyperdb                import Link, Multilink, Boolean
from roundup.date                   import Date

def sorted_properties (db, context) :
    props = db [context._classname].properties ()
    return list (sorted (props, key = lambda x: db.i18n.gettext (x._name)))
# end def sorted_properties

def properties_dict (db, context) :
    props = {}
    for prop in db [context._classname].properties (cansearch = False) :
        props [prop._name] = prop
    return props
# end def properties_dict

def filtered_properties (db, utils, context, props) :
    retprops = []
    pdict = properties_dict (db, context)
    for pname, attrs in props :
        if pname not in pdict :
            continue
        if 'searchname' in attrs :
            tprop = attrs ['searchname']
            kls = db._db.getclass (context.classname)
            if not kls.get_transitive_prop (tprop) :
                continue
        retprops.append (ExtProperty (utils, pdict [pname], ** attrs))
    return retprops
# end def filtered_properties

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
    , nodeid   = ''
    ) :
    """ Create a hidden field for this item with proper contents and
        a javascript link for editing the content property.
    """
    return ( """<input type="hidden" name="%s" value=%s> """
             """<a class="classhelp" """
             """href="javascript:help_window """
             """('%s%s?@template=comment"""
             """&property=%s&editable=%s"""
             """&form=%s', %d, %d)">"""
             """<img src="@@file/comment%s.png" alt="C" title="%s" border="0">"""
             """</a>"""
             % ( property
               , quote (str (value))
               , klass
               , nodeid
               , property
               , ('1','')[not editable]
               , form
               , width
               , height
               , ("-empty", "") [bool (value)]
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
        pretty: optional pretty-printing function (defaults to i18n.gettext)
        multiselect: Show property as a multiselect in search-box
            used by html rendering in template
        multi_add: Additional properties to show in menu and search
            multiselect.
        multi_selonly: When showing multi search-box, don't show
            'not selected' option
        is_labelprop: Render this property as a link to item -- usually
            done for labelprop of item and for id
        editable: Render property as an editable property (e.g. field)
        editparams: Parameters passed to field() in editfield
        add_hidden: Add a hidden attribute in addition to the link
        searchable: Usually a safe bet if this can be searched for, can
            be overridden when you know what you're doing.
        sortable: True if the item can be sorted by.
        terse: True if the item should be displayed in terse mode
        displayable: Usually True, set to False if no display in
            search-mask
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
        do_classhelp: usually determined automatically, may be used to
            turn off classhelp for searchable properties
        help_groupby: Optional property by which classhelp is grouped
        filter: A dictionary of properties / values to filter on when
            displaying a menu (in a search mask) or help.
        force_link: make this property a link (e.g. in index view)
        help_filter: deprecated, a string of property/value pairs
            usually computed from filter and used in classhelp
        help_props: Properties used for classhelp
        helpname: Name used for looking up helptext, can be overridden
            in case the class uses shadowed attributes for searching
            (e.g. lookalike_city)
        translate: Do translation of values for searching (in menu) and
            retrieved values from the database
        url_template: A (transitive) property of our item that tells us
            how to format this property as a link
        text_only: By default (text_only = False) everything is rendered as
            HTML. If True, do not create html entities etc.

        Internal attributes:
        name: name of the property
        key: key attribute
        label: label of the field in html.
        i18nlabel: i18n translated label
        additional: additional properties in a menu, see menu
        popcal: Display popup calendar on date properties on edit
    """
    def __init__ \
        ( self
        , utils
        , prop
        , item          = None
        , searchname    = None
        , helpname      = None
        , label         = None
        , displayprop   = None
        , multiselect   = None
        , is_labelprop  = None
        , editable      = None
        , add_hidden    = False
        , searchable    = None # usually computed, override with False
        , displayable   = True
        , sortable      = None
        , terse         = True
        , pretty        = None
        , get_cssclass  = get_cssclass
        , do_classhelp  = None
        , fieldwidth    = None
        , format        = None
        , filter        = None
        , help_props    = None
        , help_filter   = None
        , help_sort     = None
        , help_groupby  = ''
        , bool_tristate = True
        , force_link    = False
        , translate     = False
        , url_template  = None
        , additional    = []
        , menuheight    = 5
        , popcal        = True
        , multi_add     = ()
        , multi_selonly = False
        , editparams    = {}
        , text_only     = False
        ) :
        self.db            = prop._db
        self.utils         = utils
        self.prop          = prop
        self.item          = item
        self.classname     = prop._classname
        self.klass         = prop._db.getclass (self.classname)
        self.name          = prop._name
        self.helpname      = helpname
        self.add_hidden    = add_hidden
        self.searchname    = searchname
        self.label         = label
        self.displayprop   = displayprop
        self.multiselect   = multiselect
        self.is_labelprop  = is_labelprop
        self.pretty        = pretty or prop._db.i18n.gettext
        self.get_cssclass  = get_cssclass
        self.editable      = editable
        self.key           = None
        self.searchable    = searchable
        self.displayable   = displayable
        self.sortable      = sortable
        self.terse         = terse
        self.do_classhelp  = do_classhelp
        self.format        = format
        self.filter        = filter
        self.help_props    = help_props or []
        self.help_filter   = help_filter
        self.help_sort     = help_sort
        self.help_groupby  = help_groupby
        self.bool_tristate = bool_tristate
        self.propname      = displayprop
        self.leafprop      = prop._prop
        self.force_link    = force_link
        self.url_template  = url_template
        self.additional    = additional
        self.fieldwidth    = fieldwidth or self.default_fieldwidth ()
        self.menuheight    = menuheight
        self.popcal        = popcal
        self.multi_add     = multi_add
        self.multi_selonly = multi_selonly
        self.translate     = translate
        self.editparams    = editparams
        self.text_only     = text_only
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
                    v = ','.join (str (k) for k in v)
                f.append ((k, v))
            self.help_filter = ' '.join ('%s=%s' % (k, v) for k, v in f)
        self.lnkcls = None

        self.helpcls   = self.classname
        self._helpname = self.helpname or self.name
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
                    if not self.helpname :
                        self._helpname = props [-1].name
                    self.leafprop = props [-1].propclass
            else :
                self.lnkcls = prop._db.getclass (prop._prop.classname)
            self.key     = self.lnkcls.getkey ()
        self.i18nlabel = self.pretty \
            (self.utils.combined_name
                (self.helpcls, self._helpname, self.searchname)
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

    def _set_item (self, item = None, prop = None) :
        if not prop :
            prop = self.name
        if item :
            self.item = item
            self.prop = item [prop]
    # end def _set_item

    def default_fieldwidth (self) :
        if self.is_link_or_multilink and self.prop._prop.classname == 'user' :
            if isinstance (self.prop, MultilinkHTMLProperty) :
                return 60
        return 30
    # end def default_fieldwidth

    def formatted (self, item = None) :
        self._set_item (item)
        if  (  self.prop is None
            or isinstance (self.prop, MissingValue)
            or self.name != 'id' and not self.prop.is_view_ok ()
            ) :
            return ""
        if self.displayprop :
            format = self.format or '%s'
            p = self.item [self.displayprop]
            if getattr (p, 'plain', None) :
                p = p.plain (escape = not self.text_only)
            return format % str (p)
        if isinstance (self.prop, DateHTMLProperty) :
            format = self.format or '%Y-%m-%d'
            if  (  not getattr (self.prop, 'pretty', None)
                or not isinstance (self.prop._value, Date)
                ) :
                return str (self.prop)
            return self.prop.pretty (format)
        if self.format :
            return self.format % self.item [self.name]
        if isinstance (self.prop, type ('')) :
            return self.prop
        return str (self.prop.plain (escape = not self.text_only))
    # end def formatted

    def need_lookup (self) :
        """ Needs a list-lookup, because the user can't specify the key """
        return self.propname and not self.key
    # end def need_lookup

    def as_listentry (self, item = None, as_link = True) :
        usehtml = not self.text_only
        self._set_item (item)
        if usehtml and self.editable and self.prop.is_edit_ok () :
            return self.editfield ()
        if self.name != 'id' and not self.prop.is_view_ok () :
            return self.pretty ('[hidden]')
        if self.url_template :
            tpl = self.item
            for t in self.url_template.split ('.') :
                tpl = tpl [t]
            tpl = str (tpl)
            if usehtml and tpl :
                return '<a href="%s">%s</a>' \
                    % (tpl % self.item, self.formatted ())
            else :
                return self.formatted ()
        if self.is_labelprop or self.force_link :
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

    def deref (self, prop = None, searchname = None) :
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
        searchname = searchname or self.searchname

        for i in searchname.split ('.')[1:] :
            if i == 'id' :
                break
            last_p = p
            p      = p [i]
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
                , text_only    = self.text_only
                )
        # TODO: Handle multilinks in the transitive search
        # this will also be needed in callers of deref, e.g.,
        # formatlink etc... they need to be aware that the result
        # can be a list. The resulting deref is probably a recursive
        # function.
        if  (   self.propname
            and (isinstance (p, _HTMLItem) or hasattr (p._prop, 'classname'))
            and not isinstance (p, MultilinkHTMLProperty)
            ) :
            last_p = p
            p      = p [self.propname]
        return self.__class__ \
            ( self.utils, p
            , item         = last_p
            , pretty       = self.pretty
            , get_cssclass = self.get_cssclass
            , format       = self.format
            , text_only    = self.text_only
            )
    # end def deref

    def formatlink (self, item = None, as_link = True, with_title = False) :
        """
            Render my property of an item as a link to this item (unless
            as_link is False). We get the item. The name of the item and
            its id are computed.
        """
        i = item or self.item
        if  (   not i.is_view_ok ()
            or self.name != 'id' and not self.prop.is_view_ok ()
            ) :
            return ""
        if self.text_only :
            return self.formatted ()
        hidden = ""
        if self.add_hidden :
            hidden = """<input name="%s" value="%s" type="hidden"/>""" \
                % (self.searchname, str (self.prop.plain (escape = 1)))
        if not as_link :
            return hidden + self.formatted ()
        if not self.classname :
            return ""
        title = ''
        if with_title :
            title = ' title="%s"' % i.description
        return """<a tabindex="-1" class="%s"%s href="%s%s">%s</a>%s""" \
            % ( self.get_cssclass (i)
              , title
              , self.classname
              , i.id
              , self.formatted ()
              , hidden
              )
    # end def formatlink

    def menu (self, item = None, ** p) :
        """ Render as menu if condition, otherwise formatlink to prop """
        self._set_item (item)
        if self.editable :
            p.setdefault ('height', self.menuheight)
            p.update (self.filter)
            return self.prop.menu \
                ( translate  = self.translate
                , additional = self.additional
                , ** p
                )
        return self.deref ().formatlink ()
    # end def menu

    def editfield (self, item = None) :
        self._set_item (item)
        parameters = self.editparams or {}
        if not isinstance (self.prop, BooleanHTMLProperty) :
            parameters ['size'] = self.fieldwidth
        return "<span style='white-space:nowrap'>%s</span>" \
            % self.item [self.name].field (** parameters)
    # end def editfield

    def menu_or_field (self, item = None, editable = True) :
        self._set_item (item)
        prop = self.prop
        if editable is not None :
            self.editable = editable
        # msg and file are never editable (as a menu)
        if self.is_link_or_multilink :
            classname = prop._prop.classname
            if classname == 'msg' or classname == 'file' :
                self.editable = False
        if self.editable :
            if self.is_link_or_multilink :
                if prop._prop.classname == 'user' :
                    return ' '.join \
                        (( prop.field (size = self.fieldwidth)
                        ,  self.utils.user_classhelp \
                            ( self.db
                            , property = self.searchname
                            , inputtype='%s' % ('radio', 'checkbox')
                              [isinstance (self.prop, MultilinkHTMLProperty)]
                            , client = self.item._client
                            )
                        ))
                return self.menu ()
            fprops = {}
            if not isinstance (self.prop, BooleanHTMLProperty) :
                fprops ['size'] = self.fieldwidth
            if isinstance (self.prop, DateHTMLProperty) :
                fprops ['popcal'] = self.popcal
                if self.format :
                    fprops ['format'] = self.format
            try :
                return prop.field (** fprops)
            except TypeError :
                pass
            return prop.field ()
        else :
            if self.additional :
                x = self.as_listentry ()
                p = self.deref ()
                z = []
                for k in self.additional :
                    p._set_item (p.item, k)
                    z.append (p.as_listentry ())
                x += ' (' + ','.join (z) + ')'
                return x
            return self.as_listentry ()
    # end def menu_or_field

    def colonlabel (self, delimiter = ':') :
        return self.utils.fieldname \
            (self.helpcls, self._helpname, self.label, delimiter, 'header')
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
        if isinstance (idstring, list) :
            return ' '.join (idstring)
        if  (  not idstring
            or idstring == '-1'
            or not self.key
            or '.' in self.searchname
            ) :
            return idstring
        ids = idstring.split (',')
        if self.prop._prop.try_id_parsing :
            try :
                ids = [self.lnkcls.lookup (i) for i in ids]
            except KeyError :
                pass
        numeric = self.prop._prop.try_id_parsing
        if numeric :
            for i in ids :
                try :
                    x = int (i)
                    z = self.lnkcls.get (i, self.key)
                except (ValueError, IndexError) :
                    numeric = False
                    break
        if numeric :
            return ",".join ([self.lnkcls.get (i, self.key) for i in ids])
        return ','.join (ids)
    # end def pretty_ids

    def _propstring (self) :
        return "%s%s@%s" % (self.classname, self.item.id, self.name)
    # end def _propstring

    def search_input (self, request) :
        value = request.form.getvalue (self.searchname) or ''
        if isinstance (self.leafprop, Boolean) :
            yvalue = value in ('yes', '1')
            nvalue = value in ('no',  '0')
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
            , nodeid   = self.item.id
            )
    # end def comment_edit

# end class ExtProperty

def new_property (context, db, classname, id, propname, value=None) :
    prop = db [classname]._props [propname]
    for kl, hkl in propclasses :
        if isinstance (prop, kl) :
            return hkl (context._client, classname, id, prop, propname, value)
    return None
# end def new_property

def get_cssclass_from_status (context) :
    """ Sample get_cssclass function that returns the status name of the
        current issue.
    """
    return context.status.name
# end def get_cssclass_from_status

def search_allowed (db, request, classname, propname) :
    try :
        db = db._db
    except AttributeError :
        pass
    try :
        cls = db.getclass (classname)
    except KeyError :
        return False
    if propname in cls.getprops () or propname == 'id' :
        allowed = False
        for perm in ('Search', 'View') :
            if request.user.hasPermission (perm, classname, propname) :
                allowed = True
                break
        if not allowed :
            return False
        lnk = getattr (cls.getprops () [propname], 'classname', None)
        if not lnk :
            return True
        lnkcls = db.getclass (lnk)
        lbl = lnkcls.labelprop ()
        for pr in lbl, 'id' :
            allowed = False
            for perm in ('Search', 'View') :
                if request.user.hasPermission (perm, lnk, pr) :
                    allowed = True
                    break
            if not allowed :
                return False
        return True
    return False
# end def search_allowed

def init (instance) :
    instance.registerUtil ('ExtProperty',              ExtProperty)
    instance.registerUtil ('sorted_properties',        sorted_properties)
    instance.registerUtil ('properties_dict',          properties_dict)
    instance.registerUtil ('new_property',             new_property)
    instance.registerUtil ('comment_edit',             comment_edit)
    instance.registerUtil ('urlquote',                 urlquote)
    instance.registerUtil ('prop_as_array',            prop_as_array)
    instance.registerUtil ('get_cssclass',             get_cssclass)
    instance.registerUtil ('get_cssclass_from_status', get_cssclass_from_status)
    instance.registerUtil ('filtered_properties',      filtered_properties)
    instance.registerUtil ('search_allowed',           search_allowed)
# end def init
