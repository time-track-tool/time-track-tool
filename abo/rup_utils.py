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

def uni (latin1) :
    return latin1.decode ('latin1').encode ('utf8')

prettymap = \
{ 'abo'          : uni('Abo')
, 'abos'         : uni('Abos')
, 'abo_price'    : uni('Preis')
, 'aboprice'     : uni('Abo Preis')
, 'abo_type'     : uni('Abo-Typ')
, 'abotype'      : uni('Abotyp')
, 'activity'     : uni('letzte Änderung')
, 'address'      : uni('Adressen')
, 'adr_type'     : uni('Typ')
, 'amount'       : uni('Betrag')
, 'author'       : uni('Autor')
, 'balance_open' : uni('Offen')
, 'begin'        : uni('Beginn')
, 'bookentry'    : uni('Buchung am')
, 'changed'      : uni('geändert')
, 'city'         : uni('Ort')
, 'code'         : uni('Code')
, 'confirm'      : uni('Bestätigung Passwort')
, 'content'      : uni('Inhalt')
, 'country'      : uni('Land')
, 'countrycode'  : uni('Ländercode')
, 'currency'     : uni('Währung')
, 'date'         : uni('Datum')
, 'date_payed'   : uni('Bezahlt am')
, 'description'  : uni('Beschreibung')
, 'email'        : uni('Email')
, 'end'          : uni('Storniert per')
, 'fax'          : uni('Fax')
, 'firstname'    : uni('Vorname')
, 'function'     : uni('Funktion')
, 'history'      : uni('Liste der Änderungen')
, 'id'           : uni('ID')
, 'invoice_no'   : uni('RgNr')
, 'lastname'     : uni('Nachname')
, 'last_sent'    : uni('verschickt am')
, 'messages'     : uni('Notizen')
, 'msg'          : uni('Notiz')
, 'n_sent'       : uni('verschickt')
, 'name'         : uni('Name')
, 'password'     : uni('Passwort')
, 'payed_abos'   : uni('Zahler für')
, 'payer'        : uni('Zahler')
, 'period_start' : uni('Datum von')
, 'period_end'   : uni('Datum bis')
, 'phone'        : uni('Telefon')
, 'phone_home'   : uni('Telefon privat')
, 'phone_mobile' : uni('Telefon mobil')
, 'phone_office' : uni('Telefon Geschäft')
, 'realname'     : uni('Name')
, 'receipt_no'   : uni('BelegNr')
, 'recipients'   : uni('Empfänger')
, 'postalcode'   : uni('PLZ')
, 'remove'       : uni('löschen')
, 'salutation'   : uni('Anrede')
, 'street'       : uni('Strasse')
, 'subscriber'   : uni('Abonnent')
, 'title'        : uni('Titel')
, 'username'     : uni('Login Name')
, 'valid'        : uni('gültig')
}

def pretty (name) :
    return (prettymap.get (name, name))

#SHA: 016d10a7e587e6ae6f26d398e0fab4bf738db628
