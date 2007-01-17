#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    query
#
# Purpose
#    Detectors for queries
#
#--
#

def new_query (db, cl, nodeid, new_values) :
    if 'template' not in new_values :
        new_values ['tmplate'] = 'index'
# end def new_query

def check_query (db, cl, nodeid, new_values) :
    if 'template' in new_values and not new_values ['template'] :
        new_values ['tmplate'] = 'index'
# end def check_query

def init (db) :
    db.query.audit ("create", new_query)
    db.query.audit ("set",    check_query)
# end def init
