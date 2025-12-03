# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Philipp Gortan <gortan@tttech.com>
# Copyright (C) 2009-25 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
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
#    Document number tracker
#--

from schemacfg import schemadef

def init \
    ( db
    , Class
    , Department_Class
    , Boolean
    , Number
    , String
    , Link
    , Multilink
    , Full_Issue_Class
    , ** kw
    ) :

    product_type = Class \
        ( db, "product_type"
        , name                = String    ()
        , description         = String    (required = True)
        )
    product_type.setkey       ("name")
    product_type.setlabelprop ("description")

    reference = Class \
        ( db, "reference"
        , name                = String    (required = True)
        , description         = String    ()
        )
    reference.setkey       ("name")
    reference.setlabelprop ("description")

    artefact = Class \
        ( db, "artefact"
        , name                = String    (required = True)
        , description         = String    ()
        , filename_format     = String    ()
        )
    artefact.setkey ("description") ### names are not unique

    doc_status = Class \
        ( db, "doc_status"
        , name                = String    (required = True)
        , order               = Number    ()
        , transitions         = Multilink ("doc_status")
        , rq_link             = Boolean   ()
        )
    doc_status.setkey ("name")

    doc_category = Class \
        ( db, "doc_category"
        , name                = String    (required = True)
        , doc_num             = String    (required = True)
        , valid               = Boolean   ()
        )
    doc_category.setkey ("name")

    doc = Full_Issue_Class \
        ( db, "doc"
        , product_type        = Link      ("product_type", do_journal = 'no')
        , reference           = Link      ("reference",    do_journal = 'no')
        , artefact            = Link      ("artefact",     do_journal = 'no')
        , doc_category        = Link      ("doc_category", do_journal = 'no')
        , status              = Link      ("doc_status",   do_journal = 'no')
        , link                = String    ()
        , document_nr         = String    ()
        , state_changed_by    = Link      ("user")
        )
    doc.setkey       ("document_nr")
    doc.setlabelprop ("title")

    return {}
# end def init

def security (db, ** kw) :
    roles      = ( ("Doc_Admin", "Admin for documents (e.g. QM)")
                 , ("Nosy",      "Allowed on nosy list")
                 , ("Artefact",  "Allowed to see artefact tracker")
                 )
    is_readonly = int (getattr (db.config.ext, 'TTT_ARTEFACT_READONLY', '0'))

    if is_readonly:
        doc_admin = ()
        doc_admin_and_user = ()
    else:
        doc_admin = ("Doc_Admin",)
        doc_admin_and_user = ("Doc_Admin", "Artefact")

    classes    = \
        ( ("doc"          , ("Artefact",), doc_admin_and_user)
        , ("artefact"     , ("Artefact",), doc_admin)
        , ("product_type" , ("Artefact",), doc_admin)
        , ("reference"    , ("Artefact",), doc_admin)
        , ("doc_status"   , ("Artefact",), doc_admin)
        , ("doc_category" , ("Artefact",), doc_admin)
        )

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, ())
    schemadef.register_nosy_classes      (db, ['doc'])
# end def security

### __END__ doc
