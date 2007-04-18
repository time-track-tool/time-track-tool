#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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

import re

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation
from operator                       import or_
from rsclib.IP4_Address             import IP4_Address

import common

name_re_start = re.compile (r"[^a-z]")
name_re       = re.compile (r"[^\-a-z0-9]")

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

def check_ip_olo (db, ip, olo) :
    reject_invalid_ip (ip)
    sn = db.ip_subnet.find (org_location = olo)
    for sn_id in sn :
        subnet = db.ip_subnet.getnode (sn_id)
        if IP4_Address (ip) in IP4_Address (subnet.ip, subnet.netmask) :
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
    common.require_attributes (_, cl, nodeid, new_values, 'ip', 'org_location')
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
    common.require_attributes (_, cl, nodeid, new_values, 'mac')
    reject_invalid_mac (new_values ['mac'])
# end def new_network_interface

def check_machine_alias (db, mn) :
    olos = {}
    if not mn :
        return
    for id in mn :
        m = db.machine_name.getnode (id)
        if  (  m.dns_record_type == db.dns_record_type.lookup ('CNAME')
            or m.machine_name
            ) :
            raise Reject, _ ("Machine names may not point to other CNAMEs")
        for na_id in m.network_address :
            na = db.network_address.getnode (na_id)
            if na.org_location in olos :
                olon = _ ('org_location')
                polo = db.org_location.get (na.org_location, 'name')
                ip   = na.ip
                raise Reject, _ ("Duplicate %(olon)s %(polo)s in %(ip)s") \
                    % locals ()
            olos [na.org_location] = na.ip
# end def check_machine_alias

def check_nw_adr_location (db, id, adr, mn, drt, new_values) :
    na       = _ ('network_address')
    olo      = _ ('org_location')
    mnn      = _ ('machine_name')
    drtn     = _ ('dns_record_type')
    invalid  = db.dns_record_type.lookup ('invalid')
    a_rec    = db.dns_record_type.lookup ('A')
    cname    = db.dns_record_type.lookup ('CNAME')
    if adr and mn :
        raise Reject, _ ("Only one of %(na)s and %(mnn)s may be given") \
            % locals ()
    locations = {}
    for a in adr :
        l = db.network_address.get (a, 'org_location')
        if l in locations :
            olo_name = db.org_location.get (l, 'name')
            raise Reject, _ ("Duplicate %(olo)s for %(na)s: %(olo_name)s") \
                % locals ()
        locations [l] = True
    check_machine_alias (db, mn)
    if id :
        for alias in db.machine_name.find (machine_name = id) :
            check_machine_alias (db, alias)
    if  (   ('network_address' in new_values or 'machine_name' in new_values)
        and not 'dns_record_type' in new_values
        and drt != invalid
        ) :
        drt =  [a_rec, cname]['machine_name' in new_values]
        new_values ['dns_record_type'] = drt
    if drt != invalid :
        if mn and drt != cname :
            raise Reject, _ ("For %(mnn)s, %(drtn)s must be CNAME") % locals ()
        if adr and drt != a_rec :
            raise Reject, _ ("For %(na)s, %(drtn)s must be CNAME")  % locals ()
# end def check_nw_adr_location

def namecheck (name) :
    if not name or name_re_start.match (name) or name_re.search (name) :
        raise Reject, 'Illegal name: "%(name)s"' % locals ()
# end def namecheck

def check_machine_name (db, cl, nodeid, new_values) :
    for i in 'name', :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
    namecheck (new_values.get ('name', cl.get (nodeid, 'name')))
    adr = new_values.get ('network_address', cl.get (nodeid, 'network_address'))
    mn  = new_values.get ('machine_name',    cl.get (nodeid, 'machine_name'))
    drt = new_values.get ('dns_record_type', cl.get (nodeid, 'dns_record_type'))
    check_nw_adr_location (db, nodeid, adr, mn, drt, new_values)
# end def check_machine_name

def new_machine_name (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'name')
    namecheck (new_values ['name'])
    adr = new_values.get ('network_address', [])
    mn  = new_values.get ('machine_name',    None)
    drt = new_values.get ('dns_record_type', None)
    check_nw_adr_location (db, nodeid, adr, mn, drt, new_values)
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
        if IP4_Address (ip, mask).overlaps (IP4_Address (o_ip, o_mask)) :
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
    common.require_attributes \
        (_, cl, nodeid, new_values, 'ip', 'netmask', 'org_location')
    ip   = new_values ['ip']
    mask = new_values ['netmask']
    reject_invalid_ip         (ip)
    check_netmask             (mask)
    check_duplicate_ip_subnet (cl, nodeid, ip, mask)
# end def new_ip_subnet

def check_and_update_gid (_, db, cl, nodeid, sd, gid) :
    is_other  = common.uid_or_gid_in_range (gid, sd.gid_range)
    is_person = common.uid_or_gid_in_range (gid, sd.private_gid_range)
    if not is_other and not is_person and gid != sd.machine_group :
        gname  = _ ('gid')
        sdname = _ ('smb_domain')
        raise Reject, _("Invalid %(gname)s: %(gid)s for %(sdname)s") % locals ()
    common.check_unique (_, cl, nodeid, gid = gid)
    if is_other :
        db.smb_domain.set (sd.id, last_gid = max (gid, sd.last_gid))
# end def check_and_update_gid

def check_group (db, cl, nodeid, new_values) :
    for i in 'name', 'gid', 'org_location' :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
    ol = new_values.get ('org_location', cl.get (nodeid, 'org_location'))
    if 'gid' in new_values :
        gid = new_values ['gid']
        sd  = db.smb_domain.getnode (db.org_location.get (ol, 'smb_domain'))
        check_and_update_gid (_, db, cl, nodeid, sd, gid)
# end def check_group

def new_group (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'name', 'org_location')
    si = db.org_location.get   (new_values ['org_location'], 'smb_domain')
    sd = db.smb_domain.getnode (si)
    if 'gid' not in new_values :
        new_values ['gid'] = common.next_uid_or_gid (sd.last_gid, sd.gid_range)
    check_and_update_gid (_, db, cl, nodeid, sd, new_values ['gid'])
# end def new_group

def check_smb_domain (db, cl, nodeid, new_values) :
    for i in 'name', 'sid' :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
    if 'sid' in new_values :
        common.check_unique (_, cl, nodeid, sid = new_values ['sid'])
# end def check_smb_domain

def new_smb_domain (db, cl, nodeid, new_values) :
    common.require_attributes (_, cl, nodeid, new_values, 'name', 'sid')
    common.check_unique (_, cl, nodeid, sid = new_values ['sid'])
# end def new_smb_domain

def check_alias_consistency (cl, name, olo, a2a) :
    for a in a2a :
        if cl.get (a, 'org_location') != olo :
            on  = _ ('org_location')
            a2  = cl.get (a, 'name')
            raise Reject, _ ("%(on)s must match for alias: %(name)s->%(a2)s") \
                % locals ()
# end def check_alias_consistency

def reject_if_alias_has_depends (cl, id, msg) :
    if cl.find (alias_to_alias = id) :
        raise Reject, msg
# end def reject_if_alias_has_depends

def check_alias (db, cl, nodeid, new_values) :
    for i in 'name', 'org_location' :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
    name = new_values.get ('name',           cl.get (nodeid, 'name'))
    a2a  = new_values.get ('alias_to_alias', cl.get (nodeid, 'alias_to_alias'))
    a2u  = new_values.get ('alias_to_user',  cl.get (nodeid, 'alias_to_user'))
    olo  = new_values.get ('org_location',   cl.get (nodeid, 'org_location'))
    olon = _ ('org_location')
    if not (a2a or a2u) :
        raise Reject, _ ("Either %s or %s must be defined") \
            % (_ ('alias_to_alias'), _ ('alias_to_user'))
    if 'alias_to_alias' in new_values :
        new_values ['alias_to_alias'] = common.sort_uniq (a2a)
    if 'alias_to_user'  in new_values :
        new_values ['alias_to_user']  = common.sort_uniq (a2u)
    if 'org_location' in new_values and a2a :
        check_alias_consistency (cl, name, olo, a2a)
        reject_if_alias_has_depends \
            ( cl, nodeid
            , _ ("May not change %(olon)s if dependencies exist") % locals ()
            )
    if 'name' in new_values or 'org_location' in new_values :
        common.check_unique (_, cl, nodeid, name = name, org_location = olo)
    if 'name' in new_values or 'alias_to_alias' in new_values :
        common.check_loop (_, cl, nodeid, 'alias_to_alias', a2a)
# end def check_alias

def check_alias_retire (db, cl, nodeid, dummy) :
    reject_if_alias_has_depends \
        (cl, nodeid, _ ("May not retire if dependencies exist"))
# end def check_alias_retire

def new_alias (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'name', 'org_location')
    if not ('alias_to_alias' in new_values or 'alias_to_user' in new_values) :
        raise Reject, _ ("Either %s or %s must be defined") \
            % ('alias_to_alias', 'alias_to_user')
    name = new_values ['name']
    olo  = new_values ['org_location']
    common.check_unique (_, cl, nodeid, name = name, org_location = olo)
    if 'alias_to_alias' in new_values :
        a2a = new_values ['alias_to_alias']
        new_values ['alias_to_alias'] = common.sort_uniq (a2a)
        check_alias_consistency (cl, name, olo, a2a)
        common.check_loop (_, cl, nodeid, 'alias_to_alias', a2a)
    if 'alias_to_user'  in new_values :
        a2u = new_values ['alias_to_user']
        new_values ['alias_to_user']  = common.sort_uniq (a2u)
# end def new_alias

def new_smb_machine (db, cl, nodeid, new_values) :
    common.require_attributes \
        (_, cl, nodeid, new_values, 'smb_domain', 'machine_name')
    sd = db.smb_domain.getnode (new_values ['smb_domain'])
    if 'smb_domain' in new_values and 'machine_uid' not in new_values :
        new_values ['machine_uid'] = common.next_uid_or_gid \
            (sd.last_machine_uid, sd.machine_uid_range)
    mu = new_values ['machine_uid']
    common.check_unique (_, cl, nodeid, machine_uid = mu)
    db.smb_domain.set (sd.id, last_machine_uid = max (sd.last_machine_uid, mu))
# end def new_smb_machine

def check_smb_machine (db, cl, nodeid, new_values) :
    for i in 'smb_domain', 'machine_name', 'machine_uid' :
        if i in new_values and not new_values [i] :
            raise Reject, "%(attr)s may not be undefined" % {'attr' : _ (i)}
    sd_id = new_values.get ('smb_domain', cl.get (nodeid, 'smb_domain'))
    sd    = db.smb_domain.getnode (sd_id)
    if 'machine_uid' in new_values :
        db.smb_domain.set \
            ( sd.id
            , last_machine_uid = max
                (sd.last_machine_uid, new_values ['machine_uid'])
            )
# end def check_smb_machine

def init (db) :
    if 'alias' not in db.classes :
        return
    assert (common.TFL is not None)
    global _
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
    db.network_address.audit   ("create", new_network_address)
    db.network_address.audit   ("set",    check_network_address)
    db.network_interface.audit ("create", new_network_interface)
    db.network_interface.audit ("set",    check_network_interface)
    db.smb_domain.audit        ("create", new_smb_domain)
    db.smb_domain.audit        ("set",    check_smb_domain)
    db.smb_machine.audit       ("create", new_smb_machine)
    db.smb_machine.audit       ("set",    check_smb_machine)
# end def init

### __END__ time_project
