# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    nwm
#
# Purpose
#    Schema definitions for network management.
#
#--
#

from roundup.hyperdb import Class
import schemadef

def init \
    ( db
    , Class
    , Location_Class
    , Org_Location_Class
    , Organisation_Class
    , Date
    , String
    , Link
    , Multilink
    , Boolean
    , Number
    , ** kw
    ) :
    class User_Class (kw ['User_Class']) :
        """ add some default attributes to User_Class
        """
        def __init__ (self, db, classname, ** properties) :
            ancestor = kw ['User_Class']
            self.update_properties \
                ( is_lotus_user         = Boolean   ()
                , sync_with_ldap        = Boolean   ()
                , group                 = Link      ("group")
                , secondary_groups      = Multilink ("group")
                , uid                   = Number    () #
                , home_directory        = String    () #
                , login_shell           = String    () #
                , samba_home_drive      = String    () #
                , samba_home_path       = String    () #
                , samba_kickoff_time    = Date      () #
                , samba_lm_password     = String    () #
                , samba_logon_script    = String    () #
                , samba_nt_password     = String    () #
                , samba_profile_path    = String    () #
                , samba_pwd_can_change  = Date      () #
                , samba_pwd_last_set    = Date      () #
                , samba_pwd_must_change = Date      () #
                , user_password         = String    ()
                , shadow_last_change    = Date      ()
                , shadow_min            = Number    ()
                , shadow_max            = Number    ()
                , shadow_warning        = Number    ()
                , shadow_inactive       = Number    ()
                , shadow_expire         = Date      ()
                , shadow_used           = Boolean   ()
                )
            ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Class

    alias = Class \
        ( db
        , ''"alias"
        , name                  = String    ()
        , description           = String    ()
        , alias_to_alias        = Multilink ("alias")
        , alias_to_user         = Multilink ("user")
        , use_in_ln             = Boolean   ()
        , org_location          = Link      ("org_location")
        )

    dns_record_type = Class \
        ( db
        , ''"dns_record_type"
        , name                  = String    ()
        , description           = String    ()
        )
    dns_record_type.setkey ("name")

    group = Class \
        ( db
        , ''"group"
        , name                  = String    ()
        , description           = String    ()
        , gid                   = Number    ()
        , org_location          = Link      ("org_location")
        )
    group.setkey ("name")

    ip_subnet = Class \
        ( db
        , ''"ip_subnet"
        , ip                    = String    ()
        , netmask               = Number    ()
        , org_location          = Link      ("org_location")
        , routers               = Multilink ("machine_name")
        , dns_servers           = Multilink ("machine_name")
        , dhcp_range            = String    ()
        , default_lease_time    = Number    ()
        , max_lease_time        = Number    ()
        )
    ip_subnet.setlabelprop ('ip')

    Location_Class \
        ( db
        , ''"location"
        , domain_part           = String    ()
        )

    machine = Class \
        ( db
        , ''"machine"
        , inventory_no          = String    ()
        , link_field            = String    ()
        , description           = String    ()
        , owner                 = Link      ("user")
        , operating_system      = Multilink ("operating_system")
        )
    machine.setkey ("inventory_no")

    # This should really be two separate classes. But roundup does not allow
    # subclassing for this -- we need machine_name pointers in other records
    # that can either be an A-Record or a CNAME. This is currently not
    # possible with two classes.
    # Another solution would be something that can either point to an
    # A-Record or to a CNAME. Maybe call this machine_name, too. But that
    # would get really complicated.

    machine_name = Class \
        ( db
        , ''"machine_name"
        , name                  = String    ()
        , network_address       = Multilink ("network_address")
        , machine_name          = Multilink ("machine_name")
        , do_reverse_mapping    = Boolean   ()
        , dns_record_type       = Link      ("dns_record_type")
        )
    machine_name.setkey ("name")

    network_address = Class \
        ( db
        , ''"network_address"
        , ip                    = String    ()
        , org_location          = Link      ("org_location")
        , use_dhcp              = Boolean   ()
        , network_interface     = Link      ("network_interface")
        )
    network_address.setkey ("ip")

    network_interface = Class \
        ( db
        , ''"network_interface"
        , mac                   = String    ()
        , card_type             = String    ()
        , description           = String    ()
        , machine               = Link      ("machine")
        )
    network_interface.setkey ("mac")

    operating_system = Class \
        ( db
        , ''"operating_system"
        , name_version          = String    ()
        , description           = String    ()
        )
    operating_system.setkey ("name_version")

    Org_Location_Class \
        ( db
        , ''"org_location"
        , smb_domain            = Link      ("smb_domain")
        , dhcp_server           = Link      ("machine_name")
        , domino_dn             = String    ()
        )

    Organisation_Class \
        ( db
        , ''"organisation"
        , domain_part           = String    ()
        )

    smb_domain = Class \
        ( db
        , ''"smb_domain"
        , name                  = String    ()
        , description           = String    ()
        , sid                   = String    ()
        , pdc                   = Link      ("machine")
        , uid_range             = String    ()
        , private_gid_range     = String    ()
        , machine_uid_range     = String    ()
        , gid_range             = String    ()
        , machine_group         = Number    ()
        , last_uid              = Number    ()
        , last_gid              = Number    ()
        , last_machine_uid      = Number    ()
        , org_location          = Link      ("org_location")
        , netbios_ns            = Multilink ("machine_name")
        , netbios_dd            = Multilink ("machine_name")
        , netbios_nodetype      = String    ()
        )
    smb_domain.setkey ("name")

    smb_machine = Class \
        ( db
        , ''"smb_machine"
        , name                  = String    ()
        , machine_uid           = Number    ()
        , smb_domain            = Link      ("smb_domain")
        , machine_name          = Link      ("machine_name")
        )
    smb_machine.setkey ("name")
    return dict (User_Class = User_Class)
# end def init

    #
    # SECURITY SETTINGS
    #
    # See the configuration and customisation document for information
    # about security setup.
    # Assign the access and edit Permissions for issue, file and message
    # to regular users now

def security (db, ** kw) :
    roles = \
        [ ("IT"            , "IT-Department"                 )
        , ("ITView"        , "View but not change IT data"   )
        ]

    #     classname        allowed to view   /  edit
    classes = \
        [ ("alias",             ["IT", "ITView"],     ["IT"])
        , ("dns_record_type",   ["IT", "ITView"],     [])
        , ("group",             ["IT", "ITView"],     ["IT"])
        , ("ip_subnet",         ["IT", "ITView"],     ["IT"])
        , ("machine",           ["IT", "ITView"],     ["IT"])
        , ("machine_name",      ["IT", "ITView"],     ["IT"])
        , ("network_address",   ["IT", "ITView"],     ["IT"])
        , ("network_interface", ["IT", "ITView"],     ["IT"])
        , ("operating_system",  ["IT", "ITView"],     ["IT"])
        , ("smb_domain",        ["IT", "ITView"],     ["IT"])
        , ("smb_machine",       ["IT", "ITView"],     ["IT"])
        ]

    prop_perms = \
        [ ( "location", "Edit", ["IT"]
          , ("domain_part",)
          )
        , ( "org_location", "Edit", ["IT"]
          , ("smb_domain", "dhcp_server", "domino_dn")
          )
        , ( "organisation", "Edit", ["IT"]
          , ("domain_part",)
          )
        ]

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)
# end def security
