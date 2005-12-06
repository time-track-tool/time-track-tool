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
#
#++
# Name
#    nwm
#
# Purpose
#    Detectors for classes needed for network management
#

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation

_      = lambda x : x
common = None

def reject_invalid_ip (ip) :
    octets = ip.split ('.')
    if len (octets) != 4 :
        raise Reject, _ ('Invalid IP "%(ip)s": must contain 4 octets') \
            % locals ()
    for o in octets :
        on = None
        try :
            on = int (o)
        except ValueError :
            pass
        if on is None or on < 0 or on > 255 :
            raise Reject, _ ('Invalid IP "%(ip)s": invalid octet "%(o)s"') \
                % locals ()
# end def reject_invalid_ip

def ip_as_number (ip, mask = 32) :
    """ Compute the IP address as a numeric quantity from an ip address
        string and an optional integer netmask.
        >>> ip_as_number ('10.100.10.0')
        174328320L
        >>> ip_as_number ('10.100.10.0', 24)
        174328320L
        >>> ip_as_number ('10.100.10.5', 24)
        174328320L
        >>> ip_as_number ('10.100.10.5', 16)
        174325760L
        >>> ip_as_number ('10.100.0.0', 16)
        174325760L
        >>> ip_as_number ('10.100.0.0')
        174325760L
    """
    number = 0L
    mask   = long (mask)
    mask   = ((1L << mask) - 1L) << (32L - mask)
    for octet in ip.split ('.') :
        number <<= 8L
        number  |= long (octet)
    return number & mask
# end def ip_as_number

def check_ip_olo (db, ip, olo) :
    reject_invalid_ip (ip)
    sn = db.ip_subnet.find (org_location = olo)
    for sn_id in sn :
        subnet = db.ip_subnet.getnode (sn_id)
        if  (  ip_as_number (subnet.ip, subnet.netmask)
            == ip_as_number (ip,        subnet.netmask)
            ) :
            return
    olo_name = db.org_location.get (olo, 'name')
    ip_sn    = _ ('ip_subnet')
    raise Reject, _ ("IP %(ip)s does not match any %(ip_sn)s of %(olo_name)s") \
        % locals ()
# end def check_ip_olo

def check_network_address (db, cl, nodeid, new_values) :
    for i in 'ip', 'org_location' :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
    ip  = new_values.get ('ip',           cl.get (nodeid, 'ip'))
    olo = new_values.get ('org_location', cl.get (nodeid, 'org_location'))
    check_ip_olo (db, ip, olo)
# end def check_network_address

def new_network_address (db, cl, nodeid, new_values) :
    for i in 'ip', 'org_location' :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
    check_ip_olo (db, new_values ['ip'], new_values ['org_location'])
# end def new_network_address

def reject_invalid_mac (mac) :
    octets = mac.split (':')
    if len (octets) != 6 :
        raise Reject, _ ('Invalid MAC "%(mac)s": must contain 6 octets') \
            % locals ()
    for o in octets :
        on = None
        try :
            on = int (o, 16)
        except ValueError :
            pass
        if on is None or on < 0 or on > 255 :
            raise Reject, _ ('Invalid MAC "%(mac)s": invalid octet "%(o)s"') \
                % locals ()
# end def reject_invalid_mac

def check_network_interface (db, cl, nodeid, new_values) :
    for i in 'mac', :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
    mac = new_values.get ('mac', cl.get (nodeid, 'mac'))
    reject_invalid_mac (mac)
# end def check_network_interface

def new_network_interface (db, cl, nodeid, new_values) :
    for i in 'mac', :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
    reject_invalid_mac (new_values ['mac'])
# end def new_network_interface

def check_nw_adr_location (db, adr) :
    locations = {}
    for a in adr :
        l = db.network_address.get (a, 'org_location')
        if l in locations :
            olo      = _ ('org_location')
            na       = _ ('network_address')
            olo_name = db.org_location.get (l, 'name')
            raise Reject, _ ("Duplicate %(olo)s for %(na)s: %(olo_name)s") \
                % locals ()
        locations [l] = True
# end def check_nw_adr_location

def check_machine_name (db, cl, nodeid, new_values) :
    for i in 'name', :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
    adr = new_values.get ('network_address', cl.get (nodeid, 'network_address'))
    check_nw_adr_location (db, adr)
# end def check_machine_name

def new_machine_name (db, cl, nodeid, new_values) :
    for i in 'name', :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
    adr = new_values.get ('network_address', [])
    check_nw_adr_location (db, adr)
# end def new_machine_name

def check_netmask (mask) :
    if mask < 0 or mask > 32 or mask - int (mask) :
        raise Reject, _ ("Invalid netmask: %(mask)s") % locals ()
# end def check_netmask

def check_duplicate_ip_subnet (cl, nodeid, ip, mask) :
    for sn_id in cl.getnodeids () :
        if sn_id == nodeid : continue
        n      = _ ('ip_subnet')
        ips    = cl.getnode (sn_id)
        o_ip   = ips.ip
        o_mask = ips.netmask
        if  (  ip_as_number (ip,   mask) == ip_as_number (o_ip,   mask)
            or ip_as_number (ip, o_mask) == ip_as_number (o_ip, o_mask)
            ) :
            raise Reject, \
                ( ("%(n)s %(ip)s %(mask)s overlaps with %(o_ip)s %(o_mask)s")
                % locals ()
                )
# end def check_duplicate_ip_subnet

def check_ip_subnet (db, cl, nodeid, new_values) :
    for i in 'ip', 'netmask', 'org_location' :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
    ip   = new_values.get     ('ip',      cl.get (nodeid, 'ip'))
    mask = new_values.get     ('netmask', cl.get (nodeid, 'netmask'))
    reject_invalid_ip         (ip)
    check_netmask             (mask)
    check_duplicate_ip_subnet (cl, nodeid, ip, mask)
# end def check_ip_subnet

def new_ip_subnet (db, cl, nodeid, new_values) :
    for i in 'ip', 'netmask', 'org_location' :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
    ip   = new_values ['ip']
    mask = new_values ['netmask']
    reject_invalid_ip         (ip)
    check_netmask             (mask)
    check_duplicate_ip_subnet (cl, nodeid, ip, mask)
# end def new_ip_subnet

def check_group (db, cl, nodeid, new_values) :
    for i in 'name', 'gid' :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
# end def check_group

def new_group (db, cl, nodeid, new_values) :
    for i in 'name', 'gid' :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
# end def new_group

def check_smb_domain (db, cl, nodeid, new_values) :
    for i in 'name', 'sid' :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
# end def check_smb_domain

def new_smb_domain (db, cl, nodeid, new_values) :
    for i in 'name', 'sid' :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
# end def new_smb_domain

def check_alias (db, cl, nodeid, new_values) :
    for i in 'name', :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
    alias_to_alias = new_values.get \
        ('alias_to_alias', cl.get (nodeid, 'alias_to_alias'))
    alias_to_user  = new_values.get \
        ('alias_to_user',  cl.get (nodeid, 'alias_to_user'))
    if not (alias_to_alias or alias_to_user) :
        raise Reject, _ ("Either %s or %s must be defined") \
            % ('alias_to_alias', 'alias_to_user')
# end def check_alias

def new_alias (db, cl, nodeid, new_values) :
    for i in 'name', :
        if i not in new_values :
            raise Reject, "%(attr)s must be specified" % {'attr' : _ (i)}
    if not ('alias_to_alias' in new_values or 'alias_to_user' in new_values) :
        raise Reject, _ ("Either %s or %s must be defined") \
            % ('alias_to_alias', 'alias_to_user')
# end def new_alias

def init (db) :
    import sys, os
    global common, _
    sys.path.insert (0, os.path.join (db.config.HOME, 'lib'))
    common = __import__ ('common', globals (), locals ())
    del (sys.path [0])
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    db.alias.audit             ("create", new_alias)
    db.alias.audit             ("set",    check_alias)
    db.group.audit             ("create", new_group)
    db.group.audit             ("set",    check_group)
    db.ip_subnet.audit         ("create", new_ip_subnet)
    db.ip_subnet.audit         ("set",    check_ip_subnet)
    db.machine_name.audit      ("create", new_machine_name)
    db.machine_name.audit      ("set",    check_machine_name)
    db.smb_domain.audit        ("create", new_smb_domain)
    db.smb_domain.audit        ("set",    check_smb_domain)
    db.network_address.audit   ("create", new_network_address)
    db.network_address.audit   ("set",    check_network_address)
    db.network_interface.audit ("create", new_network_interface)
    db.network_interface.audit ("set",    check_network_interface)
# end def init

### __END__ time_project
