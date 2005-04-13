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

from roundup.rup_utils import uni

#
# INITIAL VALUES
#

# create the two default users
user = db.getclass('user')
user.create \
    ( username="admin"
    , password=adminpw
    , address=db.config.ADMIN_EMAIL
    , roles='Admin'
    )
user.create (username="anonymous", roles='Anonymous')

currency = db.getclass ('currency')
currency.create (name = 'CHF', description = 'Schweizer Franken')
currency.create (name = 'EUR', description = 'Euro')
currency.create (name = 'GBP', description = 'Britische Pfund')
currency.create (name = 'USD', description = 'US-Dollar')

abo_type = db.getclass ('abo_type')
abo_type.create \
    ( name        = 'ZFW12norm'
    , description = uni ('Jahresabo Zeit-Fragen')
    , order       = 1
    )
abo_type.create \
    ( name        = 'ZFW06norm'
    , description = uni ('Halbjahresabo Zeit-Fragen')
    , order       = 2
    )
abo_type.create \
    ( name        = 'ZFW12gift'
    , description = uni ('Geschenkabo Zeit-Fragen')
    , order       = 3
    )
abo_type.create \
    ( name        = 'CCM12norm'
    , description = uni ('Subscription Current Concerns')
    , order       = 4
    )
abo_type.create \
    ( name        = 'HDM12norm'
    , description = uni ('abonnement Horizons et débats')
    , order       = 5
    )
abo_type.create \
    ( name        = 'ZFM12norm'
    , description = uni ('Jahresabo Zeit-Fragen Monatsausgabe')
    , order       = 6
    )
abo_type.create \
    ( name        = 'ZFM12gift'
    , description = uni ('Geschenkabo Zeit-Fragen Monatsausgabe')
    , order       = 7
    )
abo_type.create \
    ( name        = 'ZFM12spon'
    , description = uni ('Förderabo Zeit-Fragen Monatsausgabe')
    , order       = 8
    )
abo_type.create \
    ( name        = 'ZFW12free'
    , description = uni ('Gratisabo Zeit-Fragen')
    , order       = 9
    )
abo_type.create \
    ( name        = 'ZFW12spec'
    , description = uni ('Spezialabo Zeit-Fragen')
    , order       = 10
    )
abo_type.create \
    ( name        = 'CCM12gift'
    , description = uni ('Gift subscription Current Concerns')
    , order       = 11
    )
abo_type.create \
    ( name        = 'CCM12free'
    , description = uni ('Free subscription Current Concerns')
    , order       = 12
    )
abo_type.create \
    ( name        = 'HDM12gift'
    , description = uni ('abonnement-cadeau Horizons et débats')
    , order       = 13
    )
abo_type.create \
    ( name        = 'ZFW12pate'
    , description = uni ('Patenschaftsabo Zeit-Fragen')
    , order       = 14
    )
abo_type.create \
    ( name        = 'ZFW06gift'
    , description = uni ('Halbjahres-Geschenkabo Zeit-Fragen')
    , order       = 15
    )
abo_type.create \
    ( name        = 'ZFW06spec'
    , description = uni ('Halbjahres-Spezialabo Zeit-Fragen')
    , order       = 16
    )

valid = db.getclass ('valid')
valid.create \
    ( name = uni ('gültig')
    , description = uni ('Gültige Adresse')
    )
valid.create \
    ( name = uni ('verstorben')
    , description = uni ('Verstorbener Adressat')
    )
#SHA: 9b88fcddef8b08c95429c81fdb29c4f65851e9ee
