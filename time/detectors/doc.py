# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Philipp Gortan <gortan@tttech.com>
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
# ****************************************************************************
#
#++
# Name
#    doc
#
# Purpose
#    Detectors for document class
#
# Revision Dates
#    22-May-2007 (PGO) Creation
#    29-May-2007 (PGO) Creation continued
#     8-Jun-2007 (PGO) Creation continued.
#    ««revision-date»»···
#--

from   roundup.exceptions             import Reject
from   roundup.cgi.TranslationService import get_translation
import common
import re

doc_nr_re = re.compile ("^[0-9a-zA-Z_\-]+? (?P<suffix> [0-9]+ )$", re.X)

def check_document_required (db, cl, nodeid, newvalues) :
    req = ['product_type', 'reference', 'artefact', 'department', 'title']
    if nodeid :
        req.append ('document_nr')
    common.require_attributes (_, cl, nodeid, newvalues, * req)
# end def check_document_required

def check_document_frozen (db, cl, nodeid, newvalues) :
    if common.user_has_role (db, db.getuid (), 'Doc_Admin') :
        return

    if nodeid :
        attr_lst = ('product_type', 'reference', 'artefact', 'department')
        action   = _ ('modify')
    else :
        attr_lst = ('document_nr', 'owner')
        action   = _ ('specify')

    attrs = ", ".join (_ (a) for a in attr_lst if a in newvalues)
    if attrs :
        raise Reject, _ \
            ('Your are not allowed to %(action)s: %(attrs)s'
            % locals ()
            )
# end def check_document_frozen

def check_document_nr (db, cl, nodeid, newvalues) :
    """Check or calculate document number."""
    doc_nr = newvalues.get ('document_nr')
    if doc_nr :
        if not doc_nr_re.match (doc_nr) :
            raise Reject (_ ('Document number is not valid: "%s"') % doc_nr)
    elif not nodeid :
        ### Creation where no `document_nr` is given
        dept_doc_num = db.department.get (newvalues ['department'], 'doc_num')
        prefix  = "-".join \
            ( ( db.product_type.get (newvalues ['product_type'], 'name')
              , db.reference.get    (newvalues ['reference']   , 'name')
              , db.artefact.get     (newvalues ['artefact']    , 'name')
              , _dept_doc_nr (db, cl, nodeid, newvalues)
              , "" # for the trailing dash
              )
            )
        next_nr                   = _next_document_nr (db, cl, prefix)
        newvalues ['document_nr'] = "%s%03d" % (prefix, next_nr)
# end def check_document_nr

def _check_for_description (db, cl, nodeid, newvalues) :
    """Checks that `description` is given and unique."""
    common.require_attributes (_, cl, nodeid, newvalues, 'description')
    if 'description' in newvalues :
        desc = newvalues ['description']
        common.check_unique (_, cl, nodeid, description = desc)
# end def _check_for_description

check_product_type = _check_for_description
check_reference    = _check_for_description

def default_owner (db, cl, nodeid, newvalues) :
    if not newvalues.get ('owner', None) :
        newvalues ['owner'] = db.getuid ()
# end def default_owner

# end def _check_document_nr

def _dept_doc_nr (db, cl, nodeid, newvalues) :
    """Return the selected department's `doc_num`, or reject, if it is not set.
    """
    res = db.department.get (newvalues ['department'], 'doc_num')
    if not res :
        raise Reject, _ ('Selected department has no document number')
    return res
# end def _dept_doc_nr

def _next_document_nr (db, cl, prefix) :
    filterspec = dict (document_nr = prefix)
    res = db.doc.filter (None, filterspec, sort = ('-', 'document_nr'))
    if res :
        doc_nr = cl.get (res [0], "document_nr")
        nr     = int (doc_nr_re.match (doc_nr).group ("suffix"), 10)
        return nr + 1
    else :
        return 1
# end def _next_document_nr

def init (db) :
    if 'doc' not in db.classes :
        return
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext

    for action in ('create', 'set') :
        db.doc.audit          (action, check_document_required, priority = 110)
        db.doc.audit          (action, check_document_frozen,   priority = 120)
        db.doc.audit          (action, check_document_nr,       priority = 130)
        db.product_type.audit (action, check_product_type)
        db.reference.audit    (action, check_reference)

    db.doc.audit ('create', default_owner, 140)

### __END__ doc
