# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Ralf Schlatterbeck. All rights reserved
# Reichergasse 131, A-3411 Weidling
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

def uni (latin1) :
    return latin1.decode ('latin1').encode ('utf8')

prettymap = \
{ 'abo'          : uni('Abos')
, 'abos'         : uni('Abos')
, 'abo_price'    : uni('Preis')
, 'aboprice'     : uni('Abo Preis')
, 'abo_type'     : uni('Abo-Typ')
, 'abotype'      : uni('Abotyp')
, 'activity'     : uni('letzte Änderung')
, 'address'      : uni('Adressen')
, 'adr_type'     : uni('Typ')
, 'amount'       : uni('Betrag')
, 'begin'        : uni('Beginn')
, 'city'         : uni('Ort')
, 'confirm'      : uni('Bestätigung Passwort')
, 'country'      : uni('Land')
, 'countrycode'  : uni('Ländercode')
, 'currency'     : uni('Währung')
, 'description'  : uni('Beschreibung')
, 'email'        : uni('Email')
, 'end'          : uni('Storniert per')
, 'fax'          : uni('Fax')
, 'firstname'    : uni('Vorname')
, 'function'     : uni('Funktion')
, 'history'      : uni('Liste der Änderungen')
, 'id'           : uni('ID')
, 'invalid'      : uni('Ungültig')
, 'lastname'     : uni('Nachname')
, 'messages'     : uni('Notizen')
, 'name'         : uni('Name')
, 'password'     : uni('Passwort')
, 'payed_abos'   : uni('Zahler für')
, 'payer'        : uni('Zahler')
, 'phone_home'   : uni('Telefon privat')
, 'phone_mobile' : uni('Telefon mobil')
, 'phone_office' : uni('Telefon Geschäft')
, 'realname'     : uni('Name')
, 'postalcode'   : uni('PLZ')
, 'salutation'   : uni('Anrede')
, 'street'       : uni('Strasse')
, 'subscriber'   : uni('Abonnent')
, 'title'        : uni('Titel')
, 'username'     : uni('Login Name')
}

def pretty (name) :
    return (prettymap.get (name, name))

