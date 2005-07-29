from cStringIO                      import StringIO
from roundup.cgi.actions            import Action
from roundup.cgi                    import templating
from roundup                        import hyperdb
from roundup.date                   import Date, Interval
from ooopy.OOoPy                    import OOoPy
from ooopy.Transformer              import Transformer, autosuper
from ooopy.Transforms               import renumber_all, get_meta, set_meta
from roundup.cgi.exceptions         import Redirect
from roundup.cgi.TranslationService import get_translation
from os.path                        import splitext

import ooopy.Transforms as Transforms

Reject = ValueError
_      = None

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
        abotype     = db.abo_price.get (aboprice, 'abotype')
        iv_tmplates = db.abo_type.get  (abotype, 'invoice_template')
        if not iv_tmplates :
            raise Reject, \
                ( _ ('No invoice_template defined for all invoices: %s')
                % iv ['invoice_no']
                )
        ivts = [db.invoice_template.getnode (i) for i in iv_tmplates]
        ivts = [i for i in ivts if i ['invoice_level'] <= iv ['n_sent']]
        if not ivts :
            raise Reject, \
                ( _ ('No matching invoice_template for invoice %s')
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
            raise Reject, _ ('You can only mark invoices')
        # get invoice_group:
        self.invoice_group = filterspec ['invoice_group'][0]
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
            raise Reject, _ ('invoices are already marked')

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
        self.items = \
            { 'invoice' : iv
            , 'date'    : date
            }
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
        invoices  = [self.db.invoice.getnode (i) for i in self.marked (True)]
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
        for tid,tp in tp_by_tid.iteritems () :
            sio [tid] = StringIO ()
            fileid    = self.db.tmplate.get (tp ['tmplate'], 'files')[-1]
            file      = StringIO (self.db.file.get (fileid, 'content'))

            o = OOoPy (infile = file, outfile = sio [tid])
            t = Transformer \
                ( get_meta
                , Transforms.Addpagebreak_Style ()
                , Transforms.Mailmerge          (iterator = iv_by_tid [tid])
                , renumber_all
                , set_meta
                )
            t.transform (o)
            o.close ()
        outfiles = sio.values ()
        if len (outfiles) > 1 :
            out = StringIO ()
            o   = OOoPy (infile = outfiles [0], outfile = out)
            t   = Transformer \
                  ( get_meta
                  , Transforms.Concatenate (* (outfiles [1:]))
                  , renumber_all
                  , set_meta
                  )
            t.transform (o)
            o.close ()
        else :
            out = outfiles [0]
        h = self.client.additional_headers
        h ['Content-Type']        = 'application/vnd.sun.xml.writer'
        h ['Content-Disposition'] = 'inline; filename=inv.sxw'
        self.client.header  ()
        return out.getvalue ()
    # end def handle
# end class Generate_Invoice

class Mark_Invoice_Sent (Invoice) :
    def handle (self) :
        ''' Mark the marked invoices as sent and remove mark.'''
        self.__super.handle ()
        now       = Date ('.')
        ivclass   = self.db.invoice
        invoices  = [ivclass.getnode (i) for i in self.marked (True)]
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
            ivclass.set \
                ( id
                , letters   = letters
                , n_sent    = iv ['n_sent'] + 1
                , last_sent = now
                )
        self._unmark   ()
        self.db.commit ()
        self.redirect  ()
    # end def handle
# end class Mark_Invoice_Sent

class Download_Letter (Action, autosuper) :
    def create_file (self, file, invoice, date, address) :
        if  (   file.type != 'application/vnd.sun.xml.writer'
            and splitext (file.name) [1] != '.sxw'
            ) :
            raise Redirect, 'file%s/%s' % (file.id, file.name)
        out = StringIO ()
        o   = OOoPy (infile = StringIO (file.content), outfile = out)
        t   = Transformer \
              ( Transforms.Editinfo ()
              , Transforms.Field_Replace
                ( replace = OOoPy_Invoice_Wrapper
                    (self.db, invoice, date, address)
                )
              )
        t.transform (o)
        o.close ()
        h = self.client.additional_headers
        h ['Content-Type']        = 'application/vnd.sun.xml.writer'
        h ['Content-Disposition'] = 'inline; filename=inv.sxw'
        self.client.header  ()
        return out.getvalue ()
    # end def create_file

    def handle (self) :
        request    = templating.HTMLRequest (self.client)
        filterspec = request.filterspec

        if request.classname != 'letter' :
            raise Reject, _ ('You can only download letters')
        # get id:
        try :
            self.id = request.form ['id'].value
        except KeyError :
            self.id = filterspec ['id'][0]
        letter = self.db.letter.getnode (str (self.id))
        files  = letter.files
        if not files :
            raise Redirect, 'letter%s' % self.id
        return self.create_file \
            ( self.db.file.getnode (files [0])
            , self.db.invoice.getnode (letter.invoice)
            , letter.date
            , self.db.address.getnode (letter.address)
            )
    # end def handle
# end class Download_Letter

class Personalized_Template (Download_Letter) :
    def handle (self) :
        request    = templating.HTMLRequest (self.client)
        filterspec = request.filterspec

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

def init (instance) :
    global _
    _   = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.tracker_home).gettext
    instance.registerAction ('mark_invoice',          Mark_Invoice)
    instance.registerAction ('unmark_invoice',        Unmark_Invoice)
    instance.registerAction ('mark_invoice_sent',     Mark_Invoice_Sent)
    instance.registerAction ('generate_invoice',      Generate_Invoice)
    instance.registerAction ('download_letter',       Download_Letter)
    instance.registerAction ('personalized_template', Personalized_Template)
# end def init
