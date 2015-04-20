# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Philipp Gortan <gortan@tttech.com>
# Copyright (C) 2010 Dr. Ralf Schlatterbeck Open Source Consulting
# Web: http://www.runtux.com Email: office@runtux.com
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
#    issue
#
# Purpose
#    Provide utitity functions for the issue class and friends
#
#--

import json
from   roundup.cgi.templating import MultilinkHTMLProperty
import common
from   rsclib.pycompat import string_types

def filter_status_transitions (context) :
    may_close = True
    # there was a check for closing -- we leave the logic in
    if context.status :
        if 'status_transition' in context._db.classes :
            values = [t.target.id for t in context.status.transitions
                      if t.target.name != 'closed' or may_close
                     ]
        else :
            values = [t.id for t in context.status.transitions
                      if t.name != 'closed' or may_close
                     ]
        return {'id' : values}
    return {}
# end def filter_status_transitions

def ext_attr (value) :
    if isinstance (value, string_types) :
        return value.encode ('utf-8')
    elif isinstance (value, dict) :
        if 'displayName' in value :
            if 'name' in value :
                v = '%s (%s)' % (value ['displayName'], value ['name'])
                return v.encode ('utf-8')
            return value ['displayName'].encode ('utf-8')
        elif 'name' in value :
            return value ['name'].encode ('utf-8')
        elif 'key' in value :
            return value ['key'].encode ('utf-8')
        else :
            return ','.join \
                ('%s: %s' % (k, ext_attr (v))
                 for k, v in sorted (value.iteritems ())
                )
    elif isinstance (value, list) :
        return ','.join (ext_attr (x) for x in value)
    else :
        return repr (value)
# end def ext_attr

def ext_attributes (context) :
    json_attr = str (context.ext_attributes.content)
    d = json.loads (json_attr)
    return dict \
        ((k.encode ('utf-8'), ext_attr (v)) for k, v in d.iteritems ())
# end def ext_attributes

def init (instance) :
    reg = instance.registerUtil
    reg ('filter_status_transitions', filter_status_transitions)
    reg ('copy_url',                  common.copy_url)
    reg ('copy_js',                   common.copy_js)
    reg ('ext_attributes',            ext_attributes)
# end def init

### __END__ issue
