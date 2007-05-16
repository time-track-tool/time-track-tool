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

def letter_link (request, id) :
    return """<a href="%s">%s</a>""" \
        % ( request.indexargs_url
            ( 'letter'
            , { '@action'  : 'download_letter'
              , 'id'       : id
              }
            )
          , _ ('Download&nbsp;letter')
          )
# end def letter_link

def valid_adr_types (db, adr_type_cat = None) :
    tc = None
    if adr_type_cat :
        try :
            tc = [db._db.adr_type_cat.lookup (adr_type_cat)]
        except KeyError :
            pass
    if not tc :
        tc = db._db.adr_type_cat.getnodeids ()
    return tc
# end def valid_adr_types

def adr_type_classhelp (db, property = 'adr_type', adr_type_cat = None) :
    tc = valid_adr_types (db, adr_type_cat = adr_type_cat)
    args = dict \
        ( properties = 'code,description'
        , property   = property
        , pagesize   = 500
        , sort       = 'code'
        , filter     = 'typecat=' + ','.join (tc)
        )
    return db.adr_type.classhelp (** args)
# end def adr_type_classhelp

def init (instance) :
    global _
    _   = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.tracker_home).gettext
    reg = instance.registerUtil
    reg ('letter_link',        letter_link)
    reg ('valid_adr_types',    valid_adr_types)
    reg ('adr_type_classhelp', adr_type_classhelp)
