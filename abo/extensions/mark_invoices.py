from roundup.cgi.actions import Action
from roundup.cgi         import templating
from roundup             import hyperdb
from roundup.date        import Date, Interval

Reject = ValueError


class Invoice (Action, object) :
    name = 'invoice actions'
    permissionType = 'Edit'

    def marked (self) :
        marked_spec = {'invoice_group' : self.invoice_group}
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
# end class Invoice

class UnMarkInvoice (Invoice) :
    name = 'unmark'

    def handle (self) :
        super (self.__class__, self).handle ()
        for i in self.marked () :
            self.db.invoice.set (i, invoice_group = None)
        self.db.commit ()
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
        super (self.__class__, self).handle ()
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

def

def init (instance) :
          instance.registerAction ('mark_invoice',   MarkInvoice)
          instance.registerAction ('unmark_invoice', UnMarkInvoice)
