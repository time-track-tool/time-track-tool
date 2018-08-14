# -*- coding: iso-8859-1 -*-
# Copyright (C) 2018 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
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
#    sync-id
#
# Purpose
#    Store the ID of the original tracker in classes of a secondary
#    tracker synced from the primary. Use-case: Sync of PR-Tracker from
#    Time-Tracker
#
#--
#

from roundup.hyperdb import Class
from schemacfg       import schemadef
import common

def init (db, Class, String, ** kw) :
    export = {}

    oc_base = kw ['Organisation_Class']
    class Organisation_Class (oc_base) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( sync_id               = String    ()
                )
            oc_base.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Organisation_Class
    export.update (dict (Organisation_Class = Organisation_Class))

    lc_base = kw ['Location_Class']
    class Location_Class (lc_base) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( sync_id               = String    ()
                )
            lc_base.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Location_Class
    export.update (dict (Location_Class = Location_Class))

    olo_base = kw ['Org_Location_Class']
    class Org_Location_Class (olo_base) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( sync_id               = String    ()
                )
            olo_base.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Org_Location_Class
    export.update (dict (Org_Location_Class = Org_Location_Class))

    tc_base = kw ['Time_Project_Class']
    class Time_Project_Class (tc_base) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( sync_id               = String    ()
                )
            tc_base.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Time_Project_Class
    export.update (dict (Time_Project_Class = Time_Project_Class))

    tps_base = kw ['Time_Project_Status_Class']
    class Time_Project_Status_Class (tps_base) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( sync_id               = String    ()
                )
            tps_base.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class Time_Project_Status_Class
    export.update (dict (Time_Project_Status_Class = Time_Project_Status_Class))

    scc_base = kw ['SAP_CC_Class']
    class SAP_CC_Class (scc_base) :
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( sync_id               = String    ()
                )
            scc_base.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class SAP_CC_Class
    export.update (dict (SAP_CC_Class = SAP_CC_Class))

    return export
# end def init

def security (db, ** kw) :
    pass
# end def security
