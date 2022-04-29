# Copyright (C) 2011 Ralf Schlatterbeck. All rights reserved
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
from socket                         import socket, SOCK_SEQPACKET, AF_UNIX
from roundup.exceptions             import Reject

def umts_update (db, cl, nodeid, old_values) :
    pin = cl.get (nodeid, 'pin')
    # Notify a daemon
    s = socket (AF_UNIX, SOCK_SEQPACKET)
    s.connect (db.config.detectors.UPDATE_SOCKET)
    s.send ('umtspin %s' % pin)
    s.close ()
# end def umts_update

def init (db) :
    if 'umts' in db.classes :
        db.umts.react         ("set",    umts_update)
# end def init
