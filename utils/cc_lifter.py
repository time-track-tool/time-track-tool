#!/usr/bin/python3

import sys
import os
import csv
from roundup import instance

dir     = os.getcwd ()
tracker = instance.open (dir)
db      = tracker.open ('admin')
stderr  = sys.stderr
update  = True

cc_bu = dict.fromkeys \
    (( 'AERO'
    ,  'AUTO'
    ,  'DIGITAL'
    ,  'General'
    ,  'INDU'
    ,  'MARINE'
    ,  'OFF-HIGHWAY'
    ,  'Dependable Networks'
    ))
cc_cat = dict.fromkeys \
    (( 'Aero'
    ,  'Auto'
    ,  'Board'
    ,  'Board Assistant'
    ,  'Chip'
    ,  'Corporate Business Development'
    ,  'Devops'
    ,  'Documentation'
    ,  'Facility'
    ,  'Finance'
    ,  'General Processes'
    ,  'Global process management'
    ,  'Go-to-Market & Commercial Operations'
    ,  'Grants'
    ,  'HR'
    ,  'HW'
    ,  'Indu'
    ,  'IT'
    ,  'Legal'
    ,  'Marine'
    ,  'Marketing'
    ,  'NiG'
    ,  'Off-Hwy'
    ,  'Office'
    ,  'Product Management'
    ,  'Project Management'
    ,  'Quality'
    ,  'Sales Backoffice'
    ,  'SAP'
    ,  'SCM'
    ,  'TTTech Labs'
    ))


cc_bu_csv = """
p_id;productivity;open_closed;prodcat;bucat;;;
957;Absence;Open;Absence;General;;;
968;Aerospace-Grants;Open;Productive;AERO;;;
948;Aerospace-Overhead;Open;Overhead;AERO;;;
946;Aerospace-Productive;Open;Productive;AERO;;;
951;Aerospace-Sales;Open;Sales;AERO;;;
;Auto-AB-Productive;CLOSED;Productive;AUTO;;;
976;Auto-CPE-Productive;CLOSED;Productive;AUTO;;;
977;Auto-COS-Productive;CLOSED;Productive;AUTO;;;
978;Auto Customer Programs A-Productive;Open;Productive;AUTO;;;BU Productivy Category
979;Auto Customer Programs B-Productive;Open;Productive;AUTO;;;AERO
980;Auto Customer Programs C-Productive;Open;Productive;AUTO;;;AUTO
986;Auto General-Chargeable OH;Open;Productive;AUTO;;;DIGITAL
969;Auto General-Grants;Open;Productive;AUTO;;;General
955;Auto General-Overhead;Open;Overhead;AUTO;;;MARINE
952;Auto General-Sales;Open;Sales;AUTO;;;OFF-HIGHWAY
981;Auto Growth and Performance-Productive;Open;Productive;AUTO;;;Dependable Networks
947;Auto-Productive;CLOSED;Productive;AUTO;;;
975;Auto Safety Products-Productive;Open;Productive;AUTO;;;
987;Digital-Grants;Open;Productive;DIGITAL;;;
988;Digital-Overhead;Open;Overhead;DIGITAL;;;
989;Digital-Productive;Open;Productive;DIGITAL;;;
990;Digital-Sales;Open;Sales;DIGITAL;;;
949;General-Chargeable OH;Open;Productive;General;;;
972;General-Grants;Open;Productive;General;;;
950;General-Overhead;Open;Overhead;General;;;
956;General-Sales;Open;Sales;General;;;
970;Industrial-Grants;Open;Productive;INDU;;;
967;Industrial-Overhead;Open;Overhead;INDU;;;
964;Industrial-Productive;Open;Productive;INDU;;;
965;Industrial-Sales;Open;Sales;INDU;;;
985;Marine-Grants;Open;Productive;MARINE;;;
984;Marine-Overhead;Open;Overhead;MARINE;;;
982;Marine-Productive;Open;Productive;MARINE;;;
983;Marine-Sales;Open;Sales;MARINE;;;
959;New-markets-Productive;CLOSED;Productive;BU not exist any more;;;
958;New-markets-Sales;CLOSED;Sales;BU not exist any more;;;
971;Off-Highway-Grants;Open;Productive;OFF-HIGHWAY;;;
960;Off-Highway-Overhead;Open;Overhead;OFF-HIGHWAY;;;
953;Off-Highway-Productive;Open;Productive;OFF-HIGHWAY;;;
954;Off-Highway-Sales;Open;Sales;OFF-HIGHWAY;;;
962;Off-Hwy-Productive;CLOSED;Productive;OFF-HIGHWAY;;;
961;Off-Hwy-Sales;CLOSED;Sales;OFF-HIGHWAY;;;
963;Off-Hwy-Sales;CLOSED;Sales;OFF-HIGHWAY;;;
973;Overall-Grants;CLOSED;Grants;BU not exist any more;;;
974;Overall-Overhead;CLOSED;Overhead;BU not exist any more;;;
966;Overall-Productive;Hmpf;Productive;BU not exist any more;;;
993;Dependable Networks-Productive;Open;Productive;Dependable Networks;;;
994;Dependable Networks-Overhead;Open;Overhead;Dependable Networks;;;
995;Dependable Networks-Grants;Open;Productive;Dependable Networks;;;
996;Dependable Networks-Sales;Open;Sales;Dependable Networks;;;
997;Auto Technology and Innovation-Productive;Open;Productive;AUTO;;;
"""

def cc_bu_cat_update ():
    csvr = csv.DictReader (cc_bu_csv.strip ().split ('\n'), delimiter = ';')
    for rec in csvr:
        if rec ['open_closed'] != 'Open':
            print ('Not open: %s' % rec ['productivity'], file = stderr)
            continue
        try:
            cc    = db.cost_center.getnode (rec ['p_id'])
            ccn   = cc.name
            pname = rec ['productivity']
        except (IndexError, KeyError):
            print ("Productivity not found: %s" % rec ['p_id'], file = stderr)
            continue
        if ccn != pname:
            print \
                ( "Non-matching name: %s vs %s for %s"
                % (pname, ccn, cc.id)
                , file = stderr
                )
            continue
        if cc.cc_bu_category is None:
            if rec ['bucat'] not in cc_bu:
                print ("Not in cc_bu: %s" % rec ['bucat'], file = stderr)
                continue
            print \
                ( "Updating productivity %s: %s"
                % (cc.id, rec ['bucat'])
                )
            if update:
                db.cost_center.set \
                    (cc.id, cc_bu_category = cc_bu [rec ['bucat']])
# end def cc_bu_cat_update

cc_cat_csv = """
cc_name;cc_desc;cc_cat;Profit Center;
001-001;Aerospace Sales;Aero;B1000;Aero
001-002;Automotive Sales;Auto;B9000;Auto
001-003;Industrial Sales;Indu;B4000;Indu
001-004;del_NIG Sales;NiG;B5000;NiG
001-005;Off-Highway Sales;Off-Hwy;B3000;Off-Hwy
001-006;Aero Techn. support;Aero;B1000;Aero
001-007;Auto Prod & Proj;Auto;B9000;Auto
001-008;Indu Prod & Proj;Indu;B4000;Indu
001-011;Off-Hwy Prod. Dev.;Off-Hwy;B3000;Off-Hwy
001-012;HR General;HR;U0100;General
001-013;Accounting;Finance;U0100;General
001-014;Legal;Legal;U0100;General
001-015;Office;Office;U0100;General
001-016;Board;Board;U0100;General
001-017;IT System Operations;IT;U0100;General
001-018;General Processes;General Processes;U0100;General
001-019;Product management;Product Management;U0300;R&D Non Core
001-020;Project management;Project Management;U0300;R&D Non Core
001-021;Sales Backoffice;Sales Backoffice;U0100;General
001-022;General Marketing;Marketing;U0100;General
001-029;Chip-IP-Design&DE-Core;Chip;U0200;R&D Core
001-030;TTTech Labs;TTTech Labs;U0300;R&D Non Core
001-032;Quality;Quality;U0300;R&D Non Core
001-033;General Grants;Grants;U0300;R&D Non Core
001-039;SCM Logistik;SCM;U0100;General
001-040;SCM Einkauf;SCM;U0100;General
001-043;Brno;Chip;U0903;R&D Core
001-049;Board Assistance;Board Assistant;U0100;General
001-051;Corporate Business Development;Corporate Business Development;U0100;General
001-052;Facility;Facility;U0100;General
001-053;DevOps;Devops;U0300;R&D Non Core
001-055;Pre-Series;Auto;B9000;Auto
001-056;Auto AD Customer Eng;Auto;B9000;Auto
001-057;Auto AD Platform Dev;Auto;B9000;Auto
001-059;Aero R&D;Aero;B1000;Aero
001-060;Aero PDM & Tech Sale;Aero;B1000;Aero
001-061;Electr. Dev. Auto & Off-Hwy;HW;U0200;R&D Core
001-062;Electr. Dev. Aero & Indu;HW;U0200;R&D Core
001-063;Testing Infrastructure;HW;U0200;R&D Core
001-064;Aero Project Mngmt;Aero;B1000;Aero
001-065;Mechanical Design;HW;U0200;R&D Core
001-066;Auto CU Prod & PreS;Auto;B9000;Auto
001-067;Auto Customer Programs Munich;Auto;#N/A;
001-068;SAP;SAP;U0100;General
001-069;Documentation;Documentation;U0300;R&D Non Core
001-071;Aero Software;Aero;B1000;Aero
001-072;Ingolstadt;Auto;#N/A;
001-073;Wolfsburg;Auto;#N/A;
001-074;System Development Aerospace;HW;U0200;Aero
001-075;Technomous;Auto;#N/A;
001-076;CTO Scale Office;Auto;#N/A;
001-077;Internal Communications;Marketing;U0100;General
001-079;External Communications;Marketing;U0100;General
001-080;Finance & Admin;Finance;U0100;General
001-081;Controlling;Finance;U0100;General
001-082;HR Business Partner;HR;U0100;General
001-083;HR Learning & Dev.;HR;U0100;General
001-084;HR Operations;HR;U0100;General
001-085;HR Recruiting;HR;U0100;General
001-086;SCM Product Configuration;SCM;U0100;General
001-087;IT Network;IT;U0100;General
001-088;IT Security;IT;U0100;General
001-089;IT Service Desk;IT;U0100;General
001-090;Site Munich;Auto;#N/A;
001-091;Global Operations;Corporate Business Development;#N/A;
001-092;The Autonomous;Auto;#N/A;
001-095;CISO;IT;U0100;General
001-096;IT Admin & Projects;IT;U0100;General
001-097;SCM RMA;SCM;U0100;General
001-098;SCM Admin;SCM;U0100;General
001-099;Network Dev Aviation;Aero;B1000;Aero
001-100;Aviation System IV&V;Aero;B1000;Aero
001-101;Aviation System Dev;Aero;B1000;Aero
001-102;System Development;Aero;B1000;Aero
001-103;System Dev Space;Aero;B1000;Aero
001-104;System Dev Safety;Aero;B1000;Aero
001-105;IT & Ops. Admin;IT;U0100;General
001-106;Financial Controlling;Finance;U0100;General
001-108;FuSa & Compliance;HW;U0200;R&D Core
001-112;Go-to-Market;Go-to-Market & Commercial Operations;U0100;General
001-127;HR Administration & Employee Services;HR;U0100;General
001-128;Global process management;Global process management;U0300;R&D Non Core
001-130;Marine Sales;Marine;B7000;Marine
001-134;Marine Tech. Support;Marine;B7000;Marine
001-135;Marine TSN;Marine;B7000;Marine
001-136;Travel;Office;U0100;General
"""

def cc_cat_update ():
    csvr = csv.DictReader (cc_cat_csv.strip ().split ('\n'), delimiter = ';')
    for rec in csvr:
        try:
            sccid  = db.sap_cc.lookup  (rec ['cc_name'])
            scc    = db.sap_cc.getnode (sccid)
        except (IndexError, KeyError):
            print ("SAP-CC not found: %s" % rec ['cc_name'], file = stderr)
            continue
        if scc.sap_cc_category is None:
            if rec ['cc_cat'] not in cc_cat:
                print ("Not in cc_cat: %s" % rec ['cc_cat'], file = stderr)
                continue
            print ("Updating sap_cc%s: %s" % (scc.id, rec ['cc_cat']))
            if update:
                db.sap_cc.set \
                    (scc.id, sap_cc_category = cc_cat [rec ['cc_cat']])
# end def cc_cat_update

def main ():
    if update:
        for n in cc_bu:
            try:
                bcid = db.cc_bu_category.lookup (n)
            except KeyError:
                bcid = db.cc_bu_category.create (name = n)
            cc_bu [n] = bcid

    if update:
        for n in cc_cat:
            try:
                bcid = db.sap_cc_category.lookup (n)
            except KeyError:
                bcid = db.sap_cc_category.create (name = n)
            cc_cat [n] = bcid

    cc_bu_cat_update ()
    cc_cat_update    ()
    if update:
        db.commit ()
# end def main

if __name__ == '__main__':
    main ()

