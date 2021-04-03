#! /usr/bin/python
# Copyright (C) 2020 Dr. Ralf Schlatterbeck Open Source Consulting.
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

import common

def check_domain_permission (db, uid, ad_domain) :
    """ Get all domain permission records for this user with all roles.
        Then check if the user has permission to edit ad_domain
        Return the domain_permission if found.
        Note that we return the *first* one found, there shouldn't be
        several.
    """
    user    = db.user.getnode (uid)
    roles   = set (common.role_list (user.roles))
    dpids   = db.domain_permission.filter (None, dict (users = uid))
    for dpid in db.domain_permission.getnodeids (retired = False) :
        dp = db.domain_permission.getnode (dpid)
        if dp.ad_domain != ad_domain :
            continue
        if uid in dp.users :
            return dp
        rl = set (common.role_list (dp.roles_enabled))
        if roles & rl :
            return dp
    return None
# end def check_domain_permission

### __END__
