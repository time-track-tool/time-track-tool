from roundup.cgi.actions import Action
from roundup.cgi import templating
from roundup import hyperdb

import csv

def repr_date (x) :
    if x == None :
        return ""
    else :
        return x.pretty ('%Y-%m-%d')
# end def repr_date

class ExportCSVNamesAction (Action) :
    name = 'export'
    permissionType = 'View'

    def handle (self) :
        ''' Export the specified search query as CSV. '''
        # figure the request
        request    = templating.HTMLRequest (self.client)
        filterspec = request.filterspec
        sort       = request.sort
        group      = request.group
        columns    = request.columns
        klass      = self.db.getclass (request.classname)
        props      = klass.getprops ()
        if not columns :
            columns = props.keys ()
            columns.sort ()

        # full-text search
        if request.search_text :
            matches = self.db.indexer.search (
                re.findall (r'\b\w{2,25}\b', request.search_text), klass)
        else :
            matches = None

        h                        = self.client.additional_headers
        h ['Content-Type']       = 'text/csv'
        # some browsers will honor the filename here...
        h ['Content-Disposition'] = 'inline; filename=query.csv'

        self.client.header ()

        if self.client.env ['REQUEST_METHOD'] == 'HEAD' :
            # all done, return a dummy string
            return 'dummy'

        writer = csv.writer (self.client.request.wfile)
        writer.writerow (columns)

        # Figure out Link columns
        represent = {}

        def repr_link (cls, cols) :
            def f (x) :
                if x == None :
                    return ""
                else :
                    return " ".join ([str (cls.get (x, col)) for col in cols])
            return f


        for col in columns :
            represent [col] = str
            if isinstance (props [col], hyperdb.Link) :
                cn = props [col].classname
                cl = self.db.getclass (cn)
                pr = cl.getprops ()
                if 'lastname' in pr :
                    represent [col] = repr_link (cl, ('firstname', 'lastname'))
                else :
                    represent [col] = repr_link (cl, (cl.labelprop (),))
            elif isinstance (props [col], hyperdb.Date) :
                represent [col] = repr_date

        # and search
        for itemid in klass.filter (matches, filterspec, sort, group) :
            writer.writerow ([represent [col] (klass.get (itemid, col)) for 
                col in columns])

        return '\n'
    # end def handle

def init (instance) :
          instance.registerAction ('export_csv_names', ExportCSVNamesAction)
