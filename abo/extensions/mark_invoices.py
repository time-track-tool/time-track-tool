from cStringIO           import StringIO
from roundup.cgi.actions import Action
from roundup.cgi         import templating
from roundup             import hyperdb
from roundup.date        import Date, Interval
from ooopy.OOoPy         import OOoPy
from ooopy.Transformer   import Transformer, autosuper
from ooopy.Transforms    import renumber_frames, renumber_sections \
                              , renumber_tables, get_meta, set_meta
import ooopy.Transforms as Transforms

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
        aboprice    = db.abo.get (iv ['abo'], 'aboprice')
        iv_tmplates = db.abo_price.get (aboprice, 'invoice_template')
        if not iv_tmplates :
            raise Reject, \
                ( self._ ('No invoice_template defined for all invoices: %s')
                % iv ['invoice_no']
                )
        ivs = [db.invoice_template.getnode (i) for i in iv_tmplates]
        ivs = [i for i in ivs if i ['invoice_level'] <= iv ['n_sent']]
        if not ivs :
            raise Reject, \
                ( self._ ('No matching invoice_template for invoice%s')
                % iv ['invoice_no']
                )
        max = ivs [0]
        for iv in ivs :
            if iv ['invoice_level'] > max ['invoice_level'] :
                max = iv
        return max
    # end def get_iv_template

    def handle (self) :
        # figure the request
        request    = templating.HTMLRequest (self.client)
        filterspec = request.filterspec

        if request.classname != 'invoice' :
            raise Reject, self._ ('You can only mark invoices')
        # get invoice_group:
        self.invoice_group = filterspec ['invoice_group'][0]
    # end def handle

    def _unmark (self) :
        for i in self.marked () :
            self.db.invoice.set (i, invoice_group = None)
        self.db.commit ()
    # end def _unmark

# end class Invoice

class UnMarkInvoice (Invoice) :
    name = 'unmark'

    def handle (self) :
        ''' Remove mark created by MarkInvoice. '''
        self.__super.handle ()
        self._unmark ()
    # end def handle
# end class UnMarkInvoice

class MarkInvoice (Invoice) :
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
            raise Reject, self._ ('invoices are already marked')

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
    # end def handle
# end class MarkInvoice

class OOoPyInvoiceWrapper (autosuper) :
    def __init__ (self, db, iv) :
        self.db = db
        self.items = \
            { 'invoice' : iv
            , 'date'    : Date ('.')
            }
        self.items ['address'] = self._deref ('invoice.payer')
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

# end class OOoPyInvoiceWrapper

class GenerateInvoice (Invoice) :
    def handle (self) :
        ''' Prepare invoices for printout and send to browser.'''
        self.__super.handle ()
        invoices  = [self.db.invoice.getnode (i) for i in self.marked (True)]
        ivts      = [(self.get_iv_template (i), i) for i in invoices]
        iv_by_tid = {}
        tp_by_tid = {}
        for i in ivts :
            tid = i [0]['id']
            if tid not in iv_by_tid :
                iv_by_tid [tid] = []
                tp_by_tid [tid] = i [0]
            iv_by_tid [tid].append (OOoPyInvoiceWrapper (self.db, i [1]))
        sio = {}
        for tid,tp in tp_by_tid.iteritems () :
            sio [tid] = StringIO ()
            fileid    = self.db.tmplate.get (tp ['tmplate'], 'files')[-1]
            file      = StringIO (self.db.file.get (fileid, 'content'))

            o = OOoPy (infile = file, outfile = sio [tid])
            t = Transformer \
                ( get_meta
                , Transforms.Addpagebreak_Style ()
                , Transforms.Mailmerge          (iterator = iv_by_tid [tid])
                , Transforms.Attribute_Access
                  ( ( renumber_frames
                    , renumber_sections
                    , renumber_tables
                  ) )
                , set_meta
                )
            t.transform (o)
            o.close ()
        h = self.client.additional_headers
        h ['Content-Type']        = 'application/vnd.sun.xml.writer'
        h ['Content-Disposition'] = 'inline; filename=inv.sxw'
        self.client.header ()
        return sio.itervalues ().next ().getvalue ()
    # end def handle
# end class GenerateInvoice

class MarkInvoiceSent (Invoice) :
    def handle (self) :
        ''' Mark the marked invoices as sent and remove mark.'''
        self.__super.handle ()
        now       = Date ('.')
        ivclass   = self.db.invoice
        invoices  = [ivclass.getnode (i) for i in self.marked (True)]
        for iv in invoices :
            id   = iv ['id']
            print id
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
            print "letter:", letter
            letters = iv ['letters']
            letters.append (letter)
            ivclass.set \
                ( id
                , letters   = letters
                , n_sent    = iv ['n_sent'] + 1
                , last_sent = now
                )
        self._unmark ()
        self.db.commit ()
    # end def handle
# end class MarkSent

def init (instance) :
    instance.registerAction ('mark_invoice',      MarkInvoice)
    instance.registerAction ('unmark_invoice',    UnMarkInvoice)
    instance.registerAction ('mark_invoice_sent', MarkInvoiceSent)
    instance.registerAction ('generate_invoice',  GenerateInvoice)
# end def init
#SHA: 163bbf34c9a4006b58963d9fc9b1619fdf5c8df5
