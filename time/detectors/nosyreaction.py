# -*- coding: iso-8859-1 -*-
#
# Copyright (c) 2001 Bizar Software Pty Ltd (http://www.bizarsoftware.com.au/)
# Copyright (c) 2004-10 Dr. Ralf Schlatterbeck Open Source Consulting.
#                       Web: http://www.runtux.com Email: office@runtux.com
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
#++
# Name
#    nosyreaction
#
# Purpose
#    Send out notification emails to all the users on the nosy list.


try :
    # fail at runtime if these are used
    from email.utils  import getaddresses
    from email.parser import Parser
except ImportError :
    pass

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
            cc_emails = []
            if 'header' in db.msg.properties and db.msg.get (msgid, 'header') :
                h = Parser ().parsestr (db.msg.get (msgid, 'header'), headersonly = True)
                for rn, mail in getaddresses (h.get_all ('X-ROUNDUP-CC')) :
                    cc_emails.append (mail)
            cl.nosymessage(nodeid, msgid, oldvalues, cc_emails = cc_emails)
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
    oldnosy = []
    if nodeid is None:
        ok = ('new', 'yes')
    else:
        ok = ('yes',)
        # old node, get the current values from the node if they haven't
        # changed
        oldnosy = cl.get(nodeid, 'nosy')
        if not newvalues.has_key('nosy'):
            nosy    = cl.get(nodeid, 'nosy')
            current = dict.fromkeys (nosy)
    oldnosy.sort ()

    # if the nosy list changed in this transaction, init from the new value
    if newvalues.has_key('nosy'):
        nosy = newvalues.get('nosy', [])
        for value in nosy:
            if not db.hasnode('user', value):
                continue
            if not current.has_key(value):
                current[value] = 1

    # check if doc_issue_status changed and has a nosy list
    if 'doc_issue_status' in newvalues :
        di = db.doc_issue_status.getnode (newvalues ['doc_issue_status'])
        for n in di.nosy :
            current [n] = 1

    # *always* add responsible(s) etc. to the nosy list -- make sure
    # responsible/stakeholder cannot be removed from nosy.
    props = cl.getprops ()
    for k in 'responsible', 'stakeholder' :
        if k not in props :
            continue
        if k in newvalues :
            item = newvalues [k]
        elif nodeid :
            item = cl.get (nodeid, k)
        if item:
            if isinstance(props [k], hyperdb.Link):
                assignedto_ids = [item]
            elif isinstance(props [k], hyperdb.Multilink):
                assignedto_ids = item
            for assignedto_id in assignedto_ids:
                if not current.has_key (assignedto_id) :
                    current [assignedto_id] = 1

    # see if there's any new messages - if so, possibly add the author and
    # recipient to the nosy
    if newvalues.has_key ('messages'):
        if nodeid is None:
            ok = ('new', 'yes')
            messages = newvalues ['messages']
        else:
            ok = ('yes',)
            # figure which of the messages now on the issue weren't
            # there before
            oldmessages = dict.fromkeys (cl.get (nodeid, 'messages'))
            messages = []
            for msgid in newvalues ['messages'] :
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

    # that's it, save off the new nosy list -- filter out those users
    # that do not have the 'Nosy' permission.
    newnosy = \
        [ x for x in current.keys ()
            if db.security.hasPermission ('Nosy', x, cl.classname)
        ]
    newnosy.sort ()
    newvalues ['nosy'] = newnosy
    # only set if really changed
    if oldnosy == newnosy :
        del newvalues ['nosy']
# end def updatenosy

def init(db):
    nosy_classes = [ "action_item"
                   , "defect"
                   , "doc"
                   , "feature"
                   , "issue"
                   , "it_issue"
                   , "it_project"
                   , "meeting"
                   , "release"
                   , "task"
                   , "support"
                   ]
    for klass in nosy_classes :
        if klass not in db.classes :
            continue
        cl = db.getclass (klass)
        cl.react('create', nosyreaction, priority = 200)
        cl.react('set'   , nosyreaction, priority = 200)
        cl.audit('create', updatenosy,   priority = 500)
        cl.audit('set'   , updatenosy,   priority = 500)

