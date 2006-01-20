# -*- coding: iso-8859-1 -*-
#
# Copyright (c) 2001 Bizar Software Pty Ltd (http://www.bizarsoftware.com.au/)
# This module is free software, and you may redistribute it and/or modify
# under the same terms as Python, so long as this copyright message and
# disclaimer are retained in their original form.
#
# IN NO EVENT SHALL BIZAR SOFTWARE PTY LTD BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING
# OUT OF THE USE OF THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# BIZAR SOFTWARE PTY LTD SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS"
# BASIS, AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#
#$Id$
#
#++
# Name
#    nosyreaction
#
# Purpose
#    Send out notification emails to all the users on the nosy list.
#
# Revision Dates
#    24-Jun-2004 (MPH) Creation
#     6-Jul-2004 (MPH) Changed `*_document` to `document`.
#    ««revision-date»»···
#--
#


from roundup import roundupdb, hyperdb

def nosyreaction(db, cl, nodeid, oldvalues):
    ''' A standard detector is provided that watches for additions to the
        "messages" property.

        When a new message is added, the detector sends it to all the users on
        the "nosy" list for the issue that are not already on the "recipients"
        list of the message.

        Those users are then appended to the "recipients" property on the
        message, so multiple copies of a message are never sent to the same
        user.

        The journal recorded by the hyperdatabase on the "recipients" property
        then provides a log of when the message was sent to whom.
    '''
    # send a copy of all new messages to the nosy list
    for msgid in determineNewMessages(cl, nodeid, oldvalues):
        try:
            cl.nosymessage(nodeid, msgid, oldvalues)
        except roundupdb.MessageSendError, message:
            raise roundupdb.DetectorError, message

def determineNewMessages(cl, nodeid, oldvalues):
    ''' Figure a list of the messages that are being added to the given
        node in this transaction.
    '''
    messages = []
    if oldvalues is None:
        # the action was a create, so use all the messages in the create
        messages = cl.get(nodeid, 'messages')
    elif oldvalues.has_key('messages'):
        # the action was a set (so adding new messages to an existing issue)
        m = {}
        for msgid in oldvalues['messages']:
            m[msgid] = 1
        messages = []
        # figure which of the messages now on the issue weren't there before
        for msgid in cl.get(nodeid, 'messages'):
            if not m.has_key(msgid):
                messages.append(msgid)
    return messages

def updatenosy(db, cl, nodeid, newvalues):
    '''Update the nosy list for changes to the responsible
    '''
    # nodeid will be None if this is a new node
    current = {}
    if nodeid is None:
        ok = ('new', 'yes')
    else:
        ok = ('yes',)
        # old node, get the current values from the node if they haven't
        # changed
        if not newvalues.has_key('nosy'):
            nosy = cl.get(nodeid, 'nosy')
            for value in nosy:
                if not current.has_key(value):
                    current[value] = 1

    # if the nosy list changed in this transaction, init from the new value
    if newvalues.has_key('nosy'):
        nosy = newvalues.get('nosy', [])
        for value in nosy:
            if not db.hasnode('user', value):
                continue
            if not current.has_key(value):
                current[value] = 1

    # add responsible(s) etc. to the nosy list
    for k in 'responsible', 'stakeholder' :
        if newvalues.has_key(k) and newvalues[k] is not None:
            propdef = cl.getprops()
            if isinstance(propdef[k], hyperdb.Link):
                assignedto_ids = [newvalues[k]]
            elif isinstance(propdef[k], hyperdb.Multilink):
                assignedto_ids = newvalues[k]
            for assignedto_id in assignedto_ids:
                if not current.has_key(assignedto_id):
                    current[assignedto_id] = 1

    # see if there's any new messages - if so, possibly add the author and
    # recipient to the nosy
    if newvalues.has_key('messages'):
        if nodeid is None:
            ok = ('new', 'yes')
            messages = newvalues['messages']
        else:
            ok = ('yes',)
            # figure which of the messages now on the issue weren't
            # there before
            oldmessages = cl.get(nodeid, 'messages')
            messages = []
            for msgid in newvalues['messages']:
                if msgid not in oldmessages:
                    messages.append(msgid)

        # configs for nosy modifications
        add_author = getattr(db.config, 'ADD_AUTHOR_TO_NOSY', 'new')
        add_recips = getattr(db.config, 'ADD_RECIPIENTS_TO_NOSY', 'new')

        # now for each new message:
        msg = db.msg
        for msgid in messages:
            if add_author in ok:
                authid = msg.get(msgid, 'author')
                current[authid] = 1

            # add on the recipients of the message
            if add_recips in ok:
                for recipient in msg.get(msgid, 'recipients'):
                    current[recipient] = 1

    # that's it, save off the new nosy list
    newvalues['nosy'] = current.keys()

def init(db):
    nosy_classes = [ "document"
                   , "release"
                   , "feature"
                   , "task"
                   , "defect"
                   , "meeting"
                   , "action_item"
                   , "it_issue"
                   , "it_project"
                   ]
    for klass in nosy_classes :
        #eval ("db.%s.react('create', nosyreaction)" % klass)
        #eval ("db.%s.react('set'   , nosyreaction)" % klass)
        eval ("db.%s.audit('create', updatenosy  )" % klass)
        eval ("db.%s.audit('set'   , updatenosy  )" % klass)

# vim: set filetype=python ts=4 sw=4 et si
#SHA: 4edb2ed32a6d616c10f440cf443082a148e06751
