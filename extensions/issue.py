# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Philipp Gortan <gortan@tttech.com>
# Copyright (C) 2010-15 Dr. Ralf Schlatterbeck Open Source Consulting
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
from   roundup.cgi.templating import HTMLClass, _HTMLItem
from   roundup.cgi.actions    import EditItemAction, NewItemAction, EditCommon
import common
from   rsclib.pycompat import string_types


def filter_status_transitions (context, *invalid_states) :
    # there was a check for closing -- we leave the logic in
    may_close = True
    classname = context.status._prop.classname
    cls       = context.status._db.getclass (classname)
    invalid   = [cls.lookup (x) for x in invalid_states]
    if context.status :
        if 'status_transition' in context._db.classes :
            values = [t.target.id for t in context.status.transitions
                      if t.target.name != 'closed' or may_close
                     ]
        else :
            values = [t.id for t in context.status.transitions
                      if t.name != 'closed' or may_close
                     ]
        values = [v for v in values if v not in invalid]
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
    json_attr = str (context.ext_attributes.content.plain (escape=1))
    d = json.loads (json_attr)
    return dict \
        ((k.encode ('utf-8'), ext_attr (v)) for k, v in d.iteritems ())
# end def ext_attributes

class KPM_Filter_Action (EditCommon) :
    """ Remove new message msg-2, msg-3, or msg-4 from props if the
        content did not change from the current message of the kpm
        issue. These encode the values of 'analysis', 'description' and
        'supplier_answer' of a kpm, respectively.
        Note: Technically this is only needed if we support external
        tracker sync with KPM which introduces additional attributes to
        be synced to this tracker.
        Note: The message indeces -2, -3, -4 and the association with
        message Links in kpm depend on the issue.item form. So if the
        form changes, msgidx needs to be changed, too.
    """

    msgidx = \
        { '-2': 'analysis'
        , '-3': 'description'
        , '-4': 'supplier_answer'
        , '-5': 'customer_effect'
        , '-6': 'workaround'
        , '-7': 'problem_solution'
        , '-8': 'problem_description'
        }

    def _editnodes (self, props, links) :
        kpmid = None
        for p in props :
            if p [0] == 'kpm' :
                kpmid = p [1]
                break
        if kpmid :
            for id in self.msgidx :
                key = ('msg', id)
                if key in props :
                    assert props [key].keys () == ['content']
                    content = props [key]['content']
                    msgid   = self.db.kpm.get (kpmid, self.msgidx [id])
                    if msgid :
                        oldcon  = self.db.msg.get (msgid, 'content')
                        if (oldcon == content) :
                            del props [key]
        return EditCommon._editnodes (self, props, links)
    # end def _editnodes
# end class KPM_Filter_Action

class KPM_Edit_Action (EditItemAction, KPM_Filter_Action) :
    def _editnodes (self, props, links) :
        return KPM_Filter_Action._editnodes (self, props, links)
    # end def _editnodes
# end class KPM_Edit_Action

class KPM_New_Action (NewItemAction, KPM_Filter_Action) :
    def _editnodes (self, props, links) :
        return KPM_Filter_Action._editnodes (self, props, links)
    # end def _editnodes
# end class KPM_New_Action

def edit_button (context, utils) :
    if isinstance (context, _HTMLItem) :
        return 'kpm_edit_action'
    elif isinstance (context, HTMLClass) :
        return 'kpm_new_action'
    assert None
# end def edit_button

def init (instance) :
    reg = instance.registerUtil
    reg ('filter_status_transitions', filter_status_transitions)
    reg ('copy_url',                  common.copy_url)
    reg ('copy_js',                   common.copy_js)
    reg ('ext_attributes',            ext_attributes)
    reg ('kpm_edit_button',           edit_button)
    act = instance.registerAction
    act ('kpm_edit_action',           KPM_Edit_Action)
    act ('kpm_new_action',            KPM_New_Action)
# end def init

### __END__ issue
