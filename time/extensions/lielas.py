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

from rsclib.iter_recipes            import grouper
from rsclib.autosuper               import autosuper
from roundup.cgi.actions            import Action
from roundup.cgi.exceptions         import Redirect
from roundup.exceptions             import Reject
from roundup.date                   import Date
import common

# Action codes and strings used in the web-interface and as action names
# in this module. We make sure these are properly localized here
lielas_actions = dict \
    ( data   = ( ""'Clear Measurement Data', 0, ""'Clear Measurements now'
               , ''"'Really clear measurements now?'"
               )
    , device = ( ""'Remove last Device',     1, ""'Remove last Device now'
               , ''"'Really remove last device now?'"
               )
    , db     = ( ""'Delete Database',        2, ""'Delete Database now'
               , ''"'Really delete database now?'"
               )
    )

# Default sensor and measurement queries -- used in the web-interface
# and here (for redirects) -- define them only once
sensor_query = \
    ('@columns=id,device.adr,device.name,device.name,adr,type,name,unit&'
     '@sort=device.order,order&@pagesize=50&@startwith=0'
    )
measurement_query = \
    ('@columns=sensor.device.device_group,sensor.device.adr,sensor.device.name'
     ',sensor.adr,sensor.type,sensor.name,val,sensor.unit,date&'
     '@sort=-date&@group=sensor.device.order,sensor.order&'
     '@pagesize=20&@startwith=0'
    )

class Delete_Something (Action, autosuper) :
    def delete_measurements (self, ids = None) :
        """ Delete given ids (or all if ids is None) from the
            measurements -- used for cleanup of measurements or when
            deleting a device for removing measurements for that device
        """
        sql  = 'delete from _measurement'
        sqlj = 'delete from measurement__journal'
        if ids is not None :
            b  = 500
            l  = len (ids) % b
            a  = self.db.arg
            w  = ' where _measurement.id in (%s)'
            wj = ' where nodeid in (%s)'
            for g in grouper (b, ids) :
                p = ','.join (a for k in g)
                self.db.sql (sql  + w  % p, g)
                self.db.sql (sqlj + wj % p, g)
            p = ','.join (a for k in xrange (l))
            g = ids [-l:]
            if g :
                self.db.sql (sql  + w  % p, g)
                self.db.sql (sqlj + wj % p, g)
        else :
            self.db.sql (sql)
            self.db.sql (sqlj)
    # end def delete_measurements

    def handle (self) :
        """ Common permission check -- we may want to add more roles here """
        if not common.user_has_role (self.db, self.db.getuid (), 'Admin') :
            raise Reject ("You are not allowed to execute this action")
    # end def handle
# end class Delete_Something

class Delete_Device (Delete_Something) :
    def handle (self) :
        self.__super.handle ()
        # device adrs are strings, query all, keep largest
        largest = 0
        dev     = None
        for id in self.db.device.getnodeids () :
            adr = int (self.db.device.get (id, 'adr'))
            if adr > largest :
                largest = adr
                dev     = id
        if dev is None :
            raise Redirect ('dyndns?@template=lindex')
        ids = self.db.measurement.filter (None, {'sensor.device' : dev})
        if ids :
            self.delete_measurements (ids)
        ids = self.db.sensor.filter (None, {'device' : dev})
        for id in ids :
            self.db.sensor.destroy (id)
        self.db.device.retire (dev)
        self.db.commit ()
        self.db.clearCache ()
        raise Redirect ('sensor?'+sensor_query+'&@template=index&:nosearch=1')
    # end def handle
# end class Delete_Device

class Delete_Data (Delete_Something) :
    def handle (self) :
        self.__super.handle ()
        self.delete_measurements ()
        self.db.commit ()
        self.db.clearCache ()
        raise Redirect ('measurement?'+measurement_query+'&@template=index')
    # end def handle
# end class Delete_Data

class Delete_DB (Delete_Something) :
    def handle (self) :
        self.__super.handle ()
        self.delete_measurements ()
        for k in self.db.device.getnodeids () :
            self.db.device.destroy (k)
        for k in self.db.sensor.getnodeids () :
            self.db.sensor.destroy (k)
        tr = self.db.transceiver.getnodeids ()
        assert (len (tr) == 1)
        self.db.transceiver.retire (tr [0])
        self.db.commit ()
        self.db.clearCache ()
        raise Redirect ('sensor?'+sensor_query+'&@template=index&:nosearch=1')
    # end def handle
# end class Delete_DB

def is_lielas (request) :
    return (  request.env.get ('TRACKER_NAME') == 'lielas'
           or request.env.get ('REQUEST_URI', '').startswith ('/lielas')
           or request.env.get ('SCRIPT_NAME', '').startswith ('/lielas')
           )
# end def is_lielas

template_by_class = \
    { ''             : ''
    , 'device_group' : 'index'
    , 'device'       : 'index'
    , 'measurement'  : 'index'
    }

bodyclass = \
    { ''            : 'filter'
    , 'device'      : 'filter'
    , 'sensor'      : 'filter'
    , 'measurement' : 'filter'
    }

def menu_by_class (db) :
    uok = db.user.is_edit_ok ()
    return \
        ( (x [0], x [1], x [2]) for x in
            ( ( ''
              , db._ ('Device manager')
              , 'home'
              , True
              )
            , ( 'device_group'
              , db._ ('device_group')
              , 'device_group?@template=index'
              , True
              )
            , ( 'user'
              , db._ ('User')
              , 'user1?@template=lindex'
              , uok
              )
            , ( 'dyndns'
              , db._ ('Configuration')
              , 'dyndns?@template=lindex'
              , True
              )
            ) if x [3]
        )
# end def menu_by_class

def latest_measurements (db, sensor, maxlen = 7) :
    """ return the latest maxlen measurements for given sensor
        if the sensor is an app sensor, only one measurement for status
        sensors (battery etc)
    """
    result = []
    if not sensor.is_app_sensor :
        maxlen = 1
    proptree, sql, args = db._db.measurement._filter_sql \
        (None, dict (sensor = sensor.id), ('-', 'date'))
    sql = sql + ' limit %s' % maxlen
    cursor = db._db.conn.cursor ()
    db._db.sql (sql, args, cursor)
    while True :
        m = cursor.fetchone ()
        if not m : break
        m = m [0]
        n = db._db.measurement.getnode (m)
        result.append ((Date (n.date), n.val))
        if len (result) >= maxlen :
            return result
    return result
# end def latest_measurements

def sensors_by_device (db, is_app = True) :
    by_dev = {}
    searchdict = dict (is_app_sensor = is_app)
    for s in db.sensor.filter (None, searchdict, sort = ('+', 'name')) :
        if s.device.id not in by_dev :
            by_dev [s.device.id] = []
        by_dev [s.device.id].append (s)
    return by_dev
# end def sensors_by_device

def sensor_measurements (db) :
    """ measurements indexed by sensor """
    return dict ((s.id, latest_measurements (db, s)) for s in db.sensor.list ())
# end def sensor_measurements

# some common strings for the web-interface for translation:
(""' (sec):', ""' (min):')

def anon_class (db, classname) :
    """ Return HTMLClass generated from classname but with _anonymous
        property set so that the class is suitable for generation of
        edit forms in a page.
    """
    cl = db [classname]
    cl._anonymous = True
    return cl
# end def anon_class

def dyndns_default_host (db, dyndns) :
    ds = db.dyndns_service.list ()
    dh = db.dyndns_host.list ()
    if not ds :
        protocol = db._db.dyndns_protocol.filter(None, {})
        db._db.dyndns_service.create \
            ( dyndns   = dyndns.id
            , protocol = protocol [0]
	    , login    = 'login'
	    , password = 'password'
            )
        ds = db.dyndns_service.list ()
    ds = ds [0]
    if not dh :
        db._db.dyndns_host.create \
            ( dyndns_service = ds.id
            , hostname       = 'hostname.dyndns.org'
            )
        dh = db.dyndns_host.list ()
    db._db.commit ()
    dh = dh [0]
    return dh
# end def dyndns_default_host

def init (instance) :
    act = instance.registerAction
    reg = instance.registerUtil

    act ('delete_device',       Delete_Device)
    act ('delete_data',         Delete_Data)
    act ('delete_db',           Delete_DB)

    reg ('lielas_actions',      lielas_actions)
    reg ('sensor_query',        sensor_query)
    reg ('measurement_query',   measurement_query)
    reg ('is_lielas',           is_lielas)
    reg ('menu_by_class',       menu_by_class)
    reg ('latest_measurements', latest_measurements)
    reg ('sensors_by_device',   sensors_by_device)
    reg ('sensor_measurements', sensor_measurements)
    reg ('getlocale',           common.get_num_locale)
    reg ('tracker_languages',   common.tracker_languages)
    reg ('anon_class',          anon_class)
    reg ('dyndns_default_host', dyndns_default_host)
    reg ('template_by_class',   template_by_class)
    reg ('bodyclass',           bodyclass)
# end def init
