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
    from email          import Encoders
    from email.utils    import getaddresses
    from email.parser   import Parser
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
except ImportError :
    pass

from roundup import roundupdb, hyperdb
from roundup.mailer import Mailer, MessageSendError, encode_quopri

def send_non_roundup_mail (db, cls, issueid, msgid, sendto, bcc = []) :
    """ Send mail to customer, don't use roundup change-email
        (nosymessage) mechanism -- so we can set different values and
        don't confuse the customer with roundup information.
    """
    cn        = cls.classname
    msg       = db.msg.getnode (msgid)

    title     = cls.get (issueid, 'title') or '%s message copy' % cn
    subject   = '[%s%s] %s' % (cn, issueid, title)
    charset   = getattr (db.config, 'EMAIL_CHARSET', 'utf-8')
    fromaddr  = None
    if 'customer' in cls.properties :
        customer = db.customer.getnode (cls.get (issueid, 'customer'))
        fromaddr = customer.fromaddress
    if not fromaddr :
        fromaddr = db.config.TRACKER_EMAIL
    user      = db.user.getnode (msg.author)
    authname  = user.realname or user.username or ''
    author    = (authname, fromaddr)

    m = ['']
    m.append (msg.content or '')
    body = unicode ('\n'.join (m), 'utf-8').encode (charset)

    mailer  = Mailer (db.config)
    message = mailer.get_standard_message (multipart = bool (msg.files))
    mailer.set_message_attributes (message, sendto, subject, author)
    message ['Message-Id']  = msg.messageid
    if msg.inreplyto :
        message ['In-Reply-To'] = msg.inreplyto
    if msg.files :
        part = MIMEText (body)
        part.set_charset (charset)
        encode_quopri (part)
        message.attach (part)
        for f in msg.files :
            file = db.file.getnode (f)
            if file.type == 'text/plain' :
                part = MIMEText (file.content)
                try :
                    file.content.decode ('ascii')
                except UnicodeError :
                    encode_quopri (part)
                else :
                    part ['Content-Transfer-Encoding'] = '7bit'
            elif file.type == 'message/rfc822' :
                main, sub = file.type.split ('/')
                p = FeedParser ()
                p.feed (file.content)
                part = MIMEBase (main, sub)
                part.set_payload ([p.close ()])
            else :
                type = file.type
                if not type :
                    type = mimetypes.guess_type (file.name) [0]
                if type is None :
                    type = 'application/octet-stream'
                main, sub = type.split ('/')
                part = MIMEBase (main, sub)
                part.set_payload (file.content)
                Encoders.encode_base64 (part)
            cd = 'Content-Disposition'
            part [cd] = 'attachment;\n filename="%s"' % file.name
            message.attach (part)
    else :
        message.set_payload (body)
        encode_quopri (message)
    mailer.smtp_send (sendto + bcc, message.as_string ())
# end def send_non_roundup_mail

def nosyreaction(db, cl, nodeid, oldvalues) :
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
            bcc_mails = []
            if 'header' in db.msg.properties and db.msg.get (msgid, 'header') :
                h = Parser ().parsestr \
                    (db.msg.get (msgid, 'header'), headersonly = True)
                rcc = h.get_all ('X-ROUNDUP-CC')
                bcc = h.get_all ('X-ROUNDUP-BCC')
                if rcc :
                    for rn, mail in getaddresses (rcc) :
                        cc_emails.append (mail)
                if bcc :
                    for rn, mail in getaddresses (bcc) :
                        bcc_mails.append (mail)
            cl.nosymessage(nodeid, msgid, oldvalues)
            if cc_emails :
                send_non_roundup_mail \
                    (db, cl, nodeid, msgid, cc_emails, bcc_mails)
        except roundupdb.MessageSendError, message :
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
                # don't add system users (!)
                authid = msg.get(msgid, 'author')
                is_system = False
                if 'status' in db.user.properties :
                    system = db.user_status.lookup ('system')
                    is_system = system == db.user.get (authid, 'status')
                if not is_system :
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

