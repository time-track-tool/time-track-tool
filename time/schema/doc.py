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
#    Document number tracker
#--

import schemadef

def init (db, Class, Department_Class, Number, String, Link, Multilink, ** kw) :
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

    doc = Class \
        ( db, "doc"
        , title               = String    ()
        , product_type        = Link      ("product_type")
        , reference           = Link      ("reference")
        , artefact            = Link      ("artefact")
        , department          = Link      ("department")
        , owner               = Link      ("user")
        , link                = String    ()
        , document_nr         = String    ()
        , messages            = Multilink ("msg")
        )
    doc.setkey ("document_nr")

    return dict (Department_Class = Ext_Department_Class)
# end def init


def security (db, ** kw) :
    roles      = (("Doc_Admin", "Admin for documents (e.g. QM)"),)
    prop_perms = (("department", "Edit", ("Doc_Admin", ), ("doc_num", )), )
    classes    = \
        ( ("doc"         , ("User",), ("User",))
        , ("artefact"    , ("User",), ("Doc_Admin",))
        , ("product_type", ("User",), ("Doc_Admin",))
        , ("reference"   , ("User",), ("Doc_Admin",))
        )

    schemadef.register_roles             (db, roles)
    schemadef.register_class_permissions (db, classes, prop_perms)
# end def security

### __END__ doc
