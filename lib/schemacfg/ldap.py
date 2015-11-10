# -*- coding: iso-8859-1 -*-
# Copyright (C) 2012-15 Dr. Ralf Schlatterbeck Open Source Consulting.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
#++
# Name
#    ldap
#
# Purpose
#    LDAP specific attributes used for syncing with LDAP.
#
#--
#

def init \
    ( db
    , String
    , Ext_Class
    , ** kw
    ) :
    export = {}

    User_Status_Ancestor = kw.get ('User_Status_Class', Ext_Class)
    class User_Status_Class (User_Status_Ancestor) :
        """ Add some attrs for tracking ldap behaviour
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( ldap_group             = String    ()
                , roles                  = String    ()
                )
            User_Status_Ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Status_Class
    export.update (dict (User_Status_Class = User_Status_Class))

    User_Ancestor = kw.get ('User_Class', Ext_Class)
    class User_Class (User_Ancestor) :
        """ Add some attrs to user class: We need the active directory
            guid for matching users when syncing users with ldap.
        """
        def __init__ (self, db, classname, ** properties) :
            self.update_properties \
                ( guid                   = String    ()
                )
            User_Ancestor.__init__ (self, db, classname, ** properties)
        # end def __init__
    # end class User_Class
    export.update (dict (User_Class = User_Class))

    return export
# end def init
