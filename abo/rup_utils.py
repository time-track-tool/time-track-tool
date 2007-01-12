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

def abo_max_invoice (db, abo) :
    if not len (abo ['invoices']) :
        return None
    maxinv  = db.invoice.getnode (abo ['invoices'][0])
    maxdate = maxinv ['period_end']
    for i in abo ['invoices'] :
        inv = db.invoice.getnode (i)
        d   = inv ['period_end']
        if maxdate < d :
            maxdate = d
            maxinv  = inv
    return maxinv
# end def abo_max_invoice

def uni (x) :
    return x.decode ("latin1").encode ("utf-8")

translation_table = {}
translation_table.update (dict ([(k, ord ('A')) for k in range (192, 198)]))
translation_table [198] = 'AE'.decode ('latin-1')
translation_table [199] = ord ('C')
translation_table.update (dict ([(k, ord ('E')) for k in range (200, 204)]))
translation_table.update (dict ([(k, ord ('I')) for k in range (204, 208)]))
translation_table [208] = ord ('D')
translation_table [209] = ord ('N')
translation_table.update (dict ([(k, ord ('O')) for k in range (210, 215)]))
translation_table.update (dict ([(k, ord ('U')) for k in range (217, 221)]))
translation_table [221] = ord ('Y')
translation_table [223] = 'ss'.decode ('latin-1')
translation_table.update (dict ([(k, ord ('a')) for k in range (224, 230)]))
translation_table [230] = 'ae'.decode ('latin-1')
translation_table [231] = ord ('c')
translation_table.update (dict ([(k, ord ('e')) for k in range (232, 236)]))
translation_table.update (dict ([(k, ord ('i')) for k in range (236, 240)]))
translation_table [240] = ord ('d')
translation_table [241] = ord ('n')
translation_table.update (dict ([(k, ord ('o')) for k in range (242, 247)]))
translation_table.update (dict ([(k, ord ('u')) for k in range (249, 253)]))
translation_table [253] = ord ('y')
translation_table [255] = ord ('y')

def translate (x) :
    """ Translate utf-8 string to lookalike utf-8 string without accents

        >>> translate (uni ('äöüÄÖÜß'))
        'aouAOUss'
    """
    return x.decode ('utf-8').translate (translation_table).encode ('utf-8')
