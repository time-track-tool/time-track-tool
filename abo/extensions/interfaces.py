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

from roundup.cgi.TranslationService import get_translation

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

def letter_link (request, id) :
    return """<a href="%s">%s</a>""" \
        % ( request.indexargs_url
            ( 'letter'
            , { '@action'  : 'download_letter'
              , 'id'       : id
              }
            )
          , _ ('Download letter')
          )
# end def letter_link

formattable = \
    [ ('end',  'canc', 'run')
    , ('open', 'open', 'closed')
    ]
def linkclass (item) :
    """
        returns css link-class: for "end" date we need a special
        color code for marking abos that no longer valid.
    """
    for i, t, f in formattable :
        try :
            return (t, f) [not item [i]]
        except KeyError :
            pass
    return ''
# end def linkclass

def menu_or_field (prop) :
    if hasattr (prop._prop, 'classname') :
        return prop.menu (height=5)
    return prop.field ()
# end def menu_or_field

def init (instance) :
    global _
    _   = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.tracker_home).gettext
    reg = instance.registerUtil
    reg ('sorted_properties', sorted_properties)
    reg ('properties_dict',   properties_dict)
    reg ('letter_link',       letter_link)
    reg ('linkclass',         linkclass)
    reg ('menu_or_field',     menu_or_field)
