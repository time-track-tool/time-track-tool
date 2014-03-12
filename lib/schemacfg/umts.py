#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Dr. Ralf Schlatterbeck Open Source Consulting.
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
# Dual License:
# If you need a proprietary license that permits you to add your own
# software without the need to publish your source-code under the GNU
# General Public License above, contact
# Reder, Christian Reder, A-2560 Berndorf, Austria, christian@reder.eu
#++
# Name
#    umts
#
# Purpose
#    Definition for configuring an UMTS modem

from roundup.hyperdb import Class
from schemacfg       import schemadef

def init \
    ( db
    , Class
    , String
    , Date
    , Link
    , Boolean
    , Number
    , ** kw
    ) :

    umts = Class \
        ( db, ''"umts"
        , tty                 = String    ()
        , pin                 = String    ()
        )
    umts.setkey (''"tty")

# end def init

# Currently no security settings -- allowed only for admin.

# end def security
