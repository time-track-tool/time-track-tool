#! /usr/bin/python
# Copyright (C) 2005 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************

from cStringIO                      import StringIO
from os.path                        import splitext

from roundup.cgi.actions            import Action, EditItemAction
from roundup.cgi                    import templating
from roundup                        import hyperdb
from roundup.date                   import Date, Interval
from roundup.cgi.exceptions         import Redirect

try :
    import ooopy.Transforms as Transforms
    from ooopy.OOoPy                    import OOoPy
    from ooopy.Transformer              import Transformer, autosuper
    from ooopy.Transforms               import renumber_all, get_meta, set_meta
except ImportError :
    from rsclib.autosuper               import autosuper

Reject = ValueError

class Invoice (Action, autosuper) :
    name = 'invoice actions'
    permissionType = 'Edit'

    def marked (self, send_it = False) :
        marked_spec = {'invoice_group' : self.invoice_group}
        if send_it :
            marked_spec ['send_it'] = True
        return self.db.invoice.filter (None, marked_spec)
    # end def marked

    def get_iv_template (self, iv) :
        """ Get the correct invoice_template for the invoice_level <=
            n_sent for the current invoice.
        """
        db          = self.db
        aboprice    = db.abo.get       (iv ['abo'], 'aboprice')
        iv_tmplates = db.abo_price.get (aboprice, 'invoice_template')
        if not iv_tmplates :
            raise Reject, \
                ( db._ ('No invoice_template defined for all invoices: %s')
                % iv ['invoice_no']
                )
        ivts = [db.invoice_template.getnode (i) for i in iv_tmplates]
        ivts = [i for i in ivts if i ['invoice_level'] <= iv ['n_sent']]
        if not ivts :
            raise Reject, \
                ( db._ ('No matching invoice_template for invoice %s')
                % iv ['invoice_no']
                )
        max = ivts [0]
        for ivt in ivts :
            if ivt ['invoice_level'] > max ['invoice_level'] :
                max = ivt
        return max
    # end def get_iv_template

    def handle (self) :
        # figure the request
        request    = templating.HTMLRequest (self.client)
        filterspec = request.filterspec

        if request.classname != 'invoice' :
            raise Reject, self.db._ ('You can only mark invoices')
        # get invoice_group -- if existing:
        self.invoice_group = None
        try :
            self.invoice_group = filterspec ['invoice_group'][0]
        except KeyError :
            pass
    # end def handle

    def _unmark (self) :
        for i in self.marked () :
            self.db.invoice.set (i, invoice_group = None)
        self.db.commit ()
    # end def _unmark

    def redirect (self) :
        url = templating.HTMLRequest (self.client).indexargs_url \
            ('' , { '@template'  : 'send' })
        raise Redirect, url
    # end def redirect

# end class Invoice

class Unmark_Invoice (Invoice) :
    name = 'unmark'

    def handle (self) :
        ''' Remove mark created by Mark_Invoice. '''
        self.__super.handle ()
        self._unmark        ()
        self.redirect       ()
    # end def handle
# end class Unmark_Invoice

class Mark_Invoice (Invoice) :
    name = 'mark'

    def iv_filter (self, ids) :
        """ Filter invoices for 

            - invoice belongs to a running subscription
            - invoice is in the correct self.invoice_group
            - correct interval: We do not want to send invoices before
              the interval of the invoice_template has expired after
              sending the last invoice (last_sent < now - interval)
              where interval is in months
        """
        db = self.db
        retval = []
        for id in ids :
            iv       = self.db.invoice.getnode (id)
            abo      = self.db.abo.getnode (iv ['abo'])
            if abo ['end'] :
                continue
            grp      = self.db.abo_price.get (abo ['aboprice'], 'invoice_group')
            if grp != self.invoice_group :
                continue
            ivt      = self.get_iv_template (iv)
            interval = ivt ['interval']
            if iv ['last_sent'] > self.now - Interval ('%dm' % interval) :
                continue
            retval.append (iv)
        return retval
    # end def iv_filter

    def handle (self) :
        ''' Mark invoices with the given invoice_group. '''
        self.__super.handle ()
        self.now   = Date ('.')

        if self.marked () :
            raise Reject, self.db._ ('invoices are already marked')

        invoice = self.db.invoice
        spec = \
            { 'open'         : True
            , 'period_start' : ';1m'
            }
        ids = invoice.filter (None, spec)
        invoices = self.iv_filter (ids)

        for i in invoices :
            invoice.set \
                (i ['id'], send_it = True, invoice_group = self.invoice_group)
        self.db.commit ()
        self.redirect ()
    # end def handle
# end class Mark_Invoice

class OOoPy_Invoice_Wrapper (autosuper) :
    def __init__ (self, db, iv, date = None, address = None) :
        self.db = db
        if not date :
            date = Date ('.')
        self.items = {'date' : date}
        if iv :
            self.items ['invoice'] = iv
        if not address :
            address = self._deref ('invoice.payer')
        self.items ['address'] = address
    # end def __init__

    def _pretty (self, item) :
        if isinstance (item, Date) :
            return item.pretty ('%d. %m. %Y')
        return str (item).decode ('utf-8')
    # end def _pretty

    def _deref (self, name) :
        """ dereference a dotted name -- we may want to cache this."""
        names = name.split ('.')
        x  = self.items [names [0]]
        if not x :
            raise KeyError, names [0]
        for i in names [1:] :
            p = x.cl.properties [i]
            if isinstance (p, hyperdb.Link) :
                x = self.db.getclass (p.classname).getnode (x [i])
            else :
                x = x [i]
        if x : return x
        return ""
    # end def _split

    def __getitem__ (self, name) :
        return self._pretty (self._deref (name))
    # end def __getitem__

    def has_key (self, name) :
        try :
            self._deref (name)
        except KeyError :
            return False
        return True
    # end def has_key

    __contains__ = has_key

# end class OOoPy_Invoice_Wrapper

class Generate_Invoice (Invoice) :
    def handle (self) :
        ''' Prepare invoices for printout and send to browser.'''
        self.__super.handle ()
        mimetype  = None
        extension = None
        invoices = [self.db.invoice.getnode (i) for i in self.marked (True)]
        ivts      = [(self.get_iv_template (i), i) for i in invoices]
        iv_by_tid = {}
        tp_by_tid = {}
        for i in ivts :
            tid = i [0]['id']
            if tid not in iv_by_tid :
                iv_by_tid [tid] = []
                tp_by_tid [tid] = i [0]
            iv_by_tid [tid].append (OOoPy_Invoice_Wrapper (self.db, i [1]))
        sio = {}
        for tid, tp in tp_by_tid.iteritems () :
            sio [tid] = StringIO ()
            fileid    = self.db.tmplate.get (tp ['tmplate'], 'files')[-1]
            file      = StringIO (self.db.file.get (fileid, 'content'))
            extension = splitext (self.db.file.get (fileid, 'name'))[1]

            o = OOoPy (infile = file, outfile = sio [tid])
            t = Transformer \
                ( o.mimetype
                , get_meta (o.mimetype)
                , Transforms.Addpagebreak_Style ()
                , Transforms.Mailmerge (iterator = iv_by_tid [tid])
                , renumber_all (o.mimetype)
                , set_meta     (o.mimetype)
                , Transforms.Fix_OOo_Tag ()
                )
            t.transform (o)
            mimetype = o.mimetype
            o.close ()
        outfiles = sio.values ()
        if len (outfiles) > 1 :
            out = StringIO ()
            o   = OOoPy (infile = outfiles [0], outfile = out)
            t   = Transformer \
                  ( o.mimetype
                  , get_meta (o.mimetype)
                  , Transforms.Concatenate (* (outfiles [1:]))
                  , renumber_all (o.mimetype)
                  , set_meta     (o.mimetype)
                  , Transforms.Fix_OOo_Tag ()
                  )
            t.transform (o)
            o.close ()
        else :
            out = outfiles [0]
        h = self.client.additional_headers
        h ['Content-Type']        = mimetype
        h ['Content-Disposition'] = 'inline; filename=inv%s' % extension
        self.client.header  ()
        return out.getvalue ()
    # end def handle
# end class Generate_Invoice

class _Mark_Invoice (Invoice) :
    def _mark_ivs (self, invoices) :
        ''' Mark the marked invoices as sent.'''
        now       = Date ('.')
        for iv in invoices :
            id   = iv ['id']
            ivt  = self.get_iv_template (iv)
            file = self.db.tmplate.get (ivt ['tmplate'], 'files') [-1]
            letter = self.db.letter.create \
                ( subject  = ivt ['name']
                , address  = iv.payer
                , date     = now
                , files    = [file]
                , messages = []
                , invoice  = id
                )
            letters = iv ['letters']
            letters.append (letter)
            self.db.invoice.set \
                ( id
                , letters   = letters
                , n_sent    = iv ['n_sent'] + 1
                , last_sent = now
                )
    # end def _mark_ivs
# end class _Mark_Invoice

class Mark_Invoice_Sent (_Mark_Invoice) :
    def handle (self) :
        ''' Mark the marked invoices as sent and remove mark.'''
        self.__super.handle ()
        invoices  = [self.db.invoice.getnode (i) for i in self.marked (True)]
        self._mark_ivs (invoices)
        self._unmark   ()
        self.db.commit ()
        self.redirect  ()
    # end def handle
# end class Mark_Invoice_Sent

class Mark_Single_Invoice_Sent (_Mark_Invoice) :
    def handle (self) :
        '''get current invoice and handle it'''
        self.__super.handle ()
        invoice  = self.db.invoice.getnode (self.context ['context'].id)
        invoices = [invoice]
        self._mark_ivs (invoices)
        self.db.commit ()
        raise Redirect ('invoice%s' % invoice.id)
    # end def handle
# end class Mark_Single_Invoice_Sent

class Download_Letter (Action, autosuper) :
    def create_file (self, file, invoice, date, address) :
        if  (   file.type not in 
                ( 'application/vnd.sun.xml.writer'
                , 'application/vnd.oasis.opendocument.text'
                )
            and splitext (file.name) [1] not in ('.sxw', '.odt')
            ) :
            raise Redirect, 'file%s/%s' % (file.id, file.name)
        out = StringIO ()
        o   = OOoPy (infile = StringIO (file.content), outfile = out)
        t   = Transformer \
              ( o.mimetype
              , Transforms.Editinfo ()
              , Transforms.Field_Replace
                ( replace = OOoPy_Invoice_Wrapper
                    (self.db, invoice, date, address)
                )
              , Transforms.Fix_OOo_Tag ()
              )
        t.transform (o)
        o.close ()
        h = self.client.additional_headers
        h ['Content-Type']        = file.type
        h ['Content-Disposition'] = 'inline; filename=inv.sxw'
        self.client.header  ()
        return out.getvalue ()
    # end def create_file

    def handle (self) :
        request    = templating.HTMLRequest (self.client)
        filterspec = request.filterspec

        if request.classname != 'letter' :
            raise Reject, self.db._ ('You can only download letters')
        # get id:
        try :
            self.id = request.form ['id'].value
        except KeyError :
            self.id = filterspec ['id'][0]
        letter = self.db.letter.getnode (str (self.id))
        files  = letter.files
        if not files :
            raise Redirect, 'letter%s' % self.id
        invoice = letter.invoice
        if invoice :
            invoice = self.db.invoice.getnode (invoice)
        return self.create_file \
            ( self.db.file.getnode (files [0])
            , invoice
            , letter.date
            , self.db.address.getnode (letter.address)
            )
    # end def handle
# end class Download_Letter

class Personalized_Template (Download_Letter) :
    def handle (self) :
        request    = templating.HTMLRequest (self.client)
        filterspec = request.filterspec

        _ = self.db._
        if request.classname != 'address' :
            raise Reject, _ ('You can only download templates for an address')
        try :
            template = request.form ['tmplate'].value
        except KeyError :
            template = filterspec ['tmplate'][0]
        template = self.db.tmplate.getnode (template)
        address  = self.db.address.getnode (self.context ['context'].id)
        files    = template.files
        if not files :
            raise Reject, _ ('No files for %(tmplate)s' % template.name)
        return self.create_file \
            ( self.db.file.getnode (files [0])
            , None
            , Date ('.')
            , address
            )
    # end def handle
# end class Personalized_Template

class Edit_Payment_Action (EditItemAction, autosuper) :
    """ Remove items that did not change (for which we defined a hidden
        attribute in the mask) from the new items. Then proceed as usual
        like for EditItemAction.
    """
    def _editnodes (self, props, links) :
        # use props.items here, with iteritems we get a RuntimeError
        # "dictionary changed size during iteration"
        for (cl, id), val in props.items () :
            if (   cl == 'payment'
               and int (id) < 0
               and sorted (val.keys ()) == ['invoice', 'receipt_no']
               and val ['receipt_no'] == 'auto'
               ) :
               del props [(cl, id)]
        return EditItemAction._editnodes (self, props, links)
    # end def _editnodes
# end class Edit_Payment_Action

def init (instance) :
    reg = instance.registerAction
    reg ('mark_invoice',             Mark_Invoice)
    reg ('unmark_invoice',           Unmark_Invoice)
    reg ('mark_invoice_sent',        Mark_Invoice_Sent)
    reg ('generate_invoice',         Generate_Invoice)
    reg ('mark_single_invoice_sent', Mark_Single_Invoice_Sent)
    reg ('download_letter',          Download_Letter)
    reg ('personalized_template',    Personalized_Template)
    reg ('edit_payment',             Edit_Payment_Action)
# end def init
