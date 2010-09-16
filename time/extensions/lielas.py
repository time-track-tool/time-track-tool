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
from roundup.cgi.TranslationService import get_translation
from roundup.cgi.actions            import Action
from roundup.cgi.exceptions         import Redirect
from roundup.exceptions             import Reject

_      = None

lielas_actions = dict \
    ( device = (""'Remove last Device',     0, ""'Remove last Device now')
    , data   = (""'Clear Measurement Data', 1, ""'Clear Measurements now')
    , db     = (""'Delete Database',        2, ""'Delete Database now')
    )

sensor_query = \
    ('@columns=id,device.adr,device.name,device.name,adr,type,name,unit&'
     '@sort=device.order,type&@pagesize=50&@startwith=0'
    )
measurement_query = \
    ('@columns=sensor.device.device_group,sensor.device.adr,sensor.device.name'
     ',sensor.adr,sensor.type,sensor.name,val,sensor.unit,date&'
     '@sort=-date&@group=sensor.device.order,sensor.order&'
     '@pagesize=20&@startwith=0'
    )

class Delete_Something (Action) :
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
# end class Delete_Something

class Delete_Device (Delete_Something) :
    def handle (self) :
        # device adrs are strings, query all, keep largest
        largest = 0
        dev     = None
        for id in self.db.device.getnodeids () :
            adr = int (self.db.device.get (id, 'adr'))
            if adr > largest :
                largest = adr
                dev     = id
        if dev is None :
            return
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
        self.delete_measurements ()
        self.db.commit ()
        self.db.clearCache ()
        raise Redirect ('measurement?'+measurement_query+'&@template=index')
    # end def handle
# end class Delete_Device

def init (instance) :
    global _
    _   = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.tracker_home).gettext
    act = instance.registerAction
    reg = instance.registerUtil

    act ('delete_device',     Delete_Device)
    act ('delete_data',       Delete_Data)
    #act ('delete_db',         Delete_DB)

    reg ('lielas_actions',    lielas_actions)
    reg ('sensor_query',      sensor_query)
    reg ('measurement_query', measurement_query)
# end def init
