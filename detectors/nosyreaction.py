#
# Copyright (c) 2001 Bizar Software Pty Ltd (http://www.bizarsoftware.com.au/)
# Copyright (c) 2004-22 Dr. Ralf Schlatterbeck Open Source Consulting.
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
    from email          import encoders
    from email.utils    import getaddresses
    from email.parser   import Parser
    from email.mime.nonmultipart import MIMENonMultipart
except ImportError :
    pass

from roundup import roundupdb, hyperdb
from roundup.mailer import Mailer, MessageSendError

fromprops_by_type = \
    { 'Support Issue'      : 'fromaddress'
    , 'Other'              : 'fromaddress'
    , 'RMA Issue'          : 'rmafrom'
    , 'Supplier Claim'     : 'suppclaimfrom'
    , 'Supplier Claim RMA' : 'suppclaimfrom'
    , 'Supplier Claim IGC' : 'suppclaimfrom'
    }

def send_non_roundup_mail (db, cls, issueid, msgid, sendto, cc = [], bcc = []) :
    """ Send mail to customer, don't use roundup change-email
        (nosymessage) mechanism -- so we can set different values and
        don't confuse the customer with roundup information.
    """
    cn        = cls.classname
    msg       = db.msg.getnode (msgid)

    issue     = cls.getnode (issueid)
    title     = issue.title or '%s message copy' % cn
    subject   = '[%s%s] %s' % (cn, issueid, title)
    charset   = getattr (db.config, 'EMAIL_CHARSET', 'utf-8')
    fromaddr  = None
    if 'customer' in cls.properties :
        customer = db.customer.getnode (issue.customer)
        if 'type' in cls.properties and 'rmafrom' in db.customer.properties :
            type = db.sup_type.get (issue.type, 'name')
            fromaddr = getattr (customer, fromprops_by_type.get (type))
        if not fromaddr :
            fromaddr = customer.fromaddress
    if not fromaddr :
        fromaddr = db.config.TRACKER_EMAIL
    user      = db.user.getnode (msg.author)
    authname  = user.realname or user.username or ''
    author    = (authname, fromaddr)

    m = ['']
    m.append (msg.content or '')
    body = '\n'.join (m).encode (charset)

    mailer  = Mailer (db.config)
    message = mailer.get_standard_message (multipart = bool (msg.files))
    mailer.set_message_attributes (message, sendto, subject, author)
    message ['Message-Id']  = msg.messageid
    if cc :
        message ['Cc'] = ', '.join (cc)
    if msg.inreplyto :
        message ['In-Reply-To'] = msg.inreplyto
    if msg.files :
        part = mailer.get_text_message ()
        part.set_payload (body, charset)
        message.attach (part)
    else :
        message.set_payload (body, charset)
    for f in msg.files :
        file = db.file.getnode (f)
        if file.type == 'text/plain' :
            part = mailer.get_text_message ()
            part.set_payload (file.content)
        else :
            type = file.type
            if not type :
                type = mimetypes.guess_type (file.name) [0]
            if type is None :
                type = 'application/octet-stream'
            main, sub = type.split ('/')
            part = MIMENonMultipart (main, sub)
            part.set_payload (file.binary_content)
            encoders.encode_base64 (part)
        cd = 'Content-Disposition'
        part [cd] = 'attachment;\n filename="%s"' % file.name
        message.attach (part)
    mailer.smtp_send (sendto + cc + bcc, message.as_string (), fromaddr)
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
            to_emails = []
            cc_emails = []
            bcc_mails = []
            if 'header' in db.msg.properties and db.msg.get (msgid, 'header') :
                h = Parser ().parsestr \
                    (db.msg.get (msgid, 'header'), headersonly = True)
                mto = h.get_all ('X-ROUNDUP-TO')
                rcc = h.get_all ('X-ROUNDUP-CC')
                bcc = h.get_all ('X-ROUNDUP-BCC')
                if mto :
                    for rn, mail in getaddresses (mto) :
                        to_emails.append (mail)
                if rcc :
                    for rn, mail in getaddresses (rcc) :
                        cc_emails.append (mail)
                if bcc :
                    for rn, mail in getaddresses (bcc) :
                        bcc_mails.append (mail)
            cl.nosymessage(nodeid, msgid, oldvalues)
            if to_emails or cc_emails :
                send_non_roundup_mail \
                    (db, cl, nodeid, msgid, to_emails, cc_emails, bcc_mails)
        except roundupdb.MessageSendError as message :
            raise roundupdb.DetectorError (message)

def determineNewMessages(cl, nodeid, oldvalues):
    ''' Figure a list of the messages that are being added to the given
        node in this transaction.
    '''
    messages = []
    if oldvalues is None:
        # the action was a create, so use all the messages in the create
        messages = cl.get(nodeid, 'messages')
    elif 'messages' in oldvalues :
        # the action was a set (so adding new messages to an existing issue)
        m = {}
        for msgid in oldvalues['messages']:
            m[msgid] = 1
        messages = []
        # figure which of the messages now on the issue weren't there before
        for msgid in cl.get(nodeid, 'messages'):
            if msgid not in m :
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
        if 'nosy' not in newvalues :
            nosy    = cl.get(nodeid, 'nosy')
            current = dict.fromkeys (nosy)
    oldnosy.sort ()

    # if the nosy list changed in this transaction, init from the new value
    if 'nosy' in newvalues :
        nosy = newvalues.get('nosy', [])
        for value in nosy:
            if not db.hasnode('user', value):
                continue
            if value not in current :
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
        item = None
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
                if assignedto_id not in current :
                    current [assignedto_id] = 1

    # see if there's any new messages - if so, possibly add the author and
    # recipient to the nosy
    if 'messages' in newvalues :
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
        [ x for x in current
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
                   , "purchase_request"
                   ]
    for klass in nosy_classes :
        if klass not in db.classes :
            continue
        cl = db.getclass (klass)
        cl.react('create', nosyreaction, priority = 200)
        cl.react('set'   , nosyreaction, priority = 200)
        cl.audit('create', updatenosy,   priority = 500)
        cl.audit('set'   , updatenosy,   priority = 500)

