# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Philipp Gortan <gortan@tttech.com>
# Copyright (C) 2009 Dr. Ralf Schlatterbeck Open Source Consulting.
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
    , Number
    , String
    , Link
    , Multilink
    , Full_Issue_Class
    , ** kw
    ) :

    class Ext_Department_Class (Department_Class) :
        """Add the attribute `doc_num` to the existing Department class."""

        def __init__ (self, db, classname, ** properties) :
            self.update_properties (doc_num = String ())
            self.__super.__init__ (db, classname, ** properties)
        # end def __init__
    # end class Ext_Department_Class

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
        )
    doc_status.setkey ("name")

    doc = Full_Issue_Class \
        ( db, "doc"
        , product_type        = Link      ("product_type", do_journal = 'no')
        , reference           = Link      ("reference",    do_journal = 'no')
        , artefact            = Link      ("artefact",     do_journal = 'no')
        , department          = Link      ("department",   do_journal = 'no')
        , status              = Link      ("doc_status",   do_journal = 'no')
        , link                = String    ()
        , document_nr         = String    ()
        , state_changed_by    = Link      ("user")
        )
    doc.setkey       ("document_nr")
    doc.setlabelprop ("title")

    return dict (Department_Class = Ext_Department_Class)
# end def init


def security (db, ** kw) :
    roles      = ( ("Doc_Admin", "Admin for documents (e.g. QM)")
                 , ("Nosy",      "Allowed on nosy list")
                 )
    prop_perms = (("department", "Edit", ("Doc_Admin", ), ("doc_num", )), )
    classes    = \
        ( ("doc"         , ("User",), ("Doc_Admin", "User"))
        , ("artefact"    , ("User",), ("Doc_Admin",))
        , ("product_type", ("User",), ("Doc_Admin",))
        , ("reference"   , ("User",), ("Doc_Admin",))
        , ("doc_status"  , ("User",), ("Doc_Admin",))
        )

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)
    schemadef.register_nosy_classes      (db, ['doc'])
# end def security

### __END__ doc
