# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Ralf Schlatterbeck. All rights reserved
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
# Dual License:
# If you need a proprietary license that permits you to add your own
# software without the need to publish your source-code under the GNU
# General Public License above, contact
# Reder, Christian Reder, A-2560 Berndorf, Austria, christian@reder.eu

import os
from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation
from common                         import reject_attributes, changed_values
from signal                         import SIGUSR1

_ = lambda x : x


def deny_adr (db, cl, nodeid, new_values) :
    reject_attributes (_, new_values, 'adr')
# end def deny_adr

def update_device_surrogate (db, cl, nodeid, new_values) :
    if 'name' in new_values :
        n  = cl.getnode (nodeid)
        na = n.adr
        if na.isdigit () :
            na = "%03d" % int (na)
        new_values ['surrogate'] = '-'.join ((new_values ['name'], na))
        for sid in db.sensor.filter (None, dict (device = nodeid)) :
            s = db.sensor.getnode (sid)
            nv = dict (name = s.name)
            update_sensor_surrogate (db, db.sensor, sid, nv)
            db.sensor.set (sid, **nv)
# end def update_device_surrogate

def round_sint_mint (db, cl, nodeid, new_values) :
    if 'sint' in new_values :
        new_values ['sint'] = 60 * int (new_values ['sint'] / 60. + 0.5)
        if new_values ['sint'] < 60 :
            new_values ['sint'] = 60
        if 'sint_pending' not in new_values :
            new_values['sint_pending'] = True
    if 'mint' in new_values :
        new_values ['mint'] = int (new_values ['mint'] + 0.5)
        if new_values ['mint'] < 10 :
            new_values ['mint'] = 10
        if 'mint_pending' not in new_values :
            new_values['mint_pending'] = True
# end def round_sint_mint

def update_order (db, cl, nodeid, new_values) :
    order = new_values.get ('order')
    if order is None and nodeid :
        order = cl.get (nodeid, 'order')
    if order is None and 'adr' in new_values :
        adr = new_values ['adr']
        new_values ['order'] = 0
        if str (adr).isdigit () :
            new_values ['order'] = int (adr)
# end def update_order

def update_is_app (db, cl, nodeid, new_values) :
    app = new_values.get ('is_app_sensor')
    if app is None and nodeid :
        app = cl.get (nodeid, 'is_app_sensor')
    if app is None and 'adr' in new_values :
        adr = new_values ['adr']
        new_values ['is_app_sensor'] = False
        if str (adr).isdigit () :
            new_values ['is_app_sensor'] = True
# end def update_is_app

def update_sensor_surrogate (db, cl, nodeid, new_values) :
    if 'name' in new_values :
        n  = cl.getnode (nodeid)
        d  = db.device.get (n.device, 'adr')
        if d.isdigit () :
            d = "%03d" % int (d)
        na = n.adr
        if na.isdigit () :
            na = "%03d" % int (na)
        new_values ['surrogate'] = '-'.join ((new_values ['name'], d, na))
# end def update_sensor_surrogate

def notify_lielas_daemon (db = None, cl = None, nodeid = None, ov = None) :
    """ We search for the lielas daemon and try to send it a SIGUSR1
        signal so it will update it's state from the database.
    """
    names = ("lielas-daemon", "roundup_handler.py")
    for process in os.listdir ('/proc') :
        if not process.isdigit () :
            continue
        try :
            cmd = open (os.path.join ('/proc',  process, 'cmdline')).read ()
        except IOError :
            continue
        cmd = cmd.rstrip ('\0').split ('\0')
        if  (   cmd [0].endswith ('/python')
            and (names [0] in cmd [1] or names [1] in cmd [1])
            ) :
            try :
                os.kill (int (process), SIGUSR1)
            except OSError :
                pass
# end def notify_lielas_daemon

def check_daemon_props (db, cl, nodeid, old_values) :
    changed = changed_values (old_values, cl, nodeid)
    for a in 'almin', 'almax', 'do_logging', 'mint', 'sint', 'gapint', 'rec' :
        if a in changed :
            notify_lielas_daemon ()
            break
# end def check_daemon_props


def init (db) :
    if 'measurement' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.device.audit      ("set",    deny_adr)
    db.device.audit      ("set",    update_device_surrogate)
    db.device.audit      ("set",    round_sint_mint)
    db.device.audit      ("create", update_order)
    db.device.audit      ("create", round_sint_mint)
    db.device.react      ("set",    check_daemon_props)
    db.device.react      ("retire", notify_lielas_daemon)
    db.sensor.audit      ("set",    deny_adr)
    db.sensor.audit      ("set",    update_sensor_surrogate)
    db.sensor.audit      ("create", update_order)
    db.sensor.audit      ("create", update_is_app)
    db.sensor.react      ("set",    check_daemon_props)
    db.transceiver.react ("set",    check_daemon_props)
    db.transceiver.react ("retire", notify_lielas_daemon)
    db.transceiver.audit ("set",    round_sint_mint)
    db.transceiver.audit ("create", round_sint_mint)
# end def init
