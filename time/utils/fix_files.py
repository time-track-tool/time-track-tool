#!/usr/bin/python
import os
import sys
from roundup           import instance
from optparse          import OptionParser
from rsclib.autosuper  import autosuper
from roundup.hyperdb   import Multilink

class File_Checker (autosuper) :
    """ Check files:
        - Referencing, does the file on disk exist, fix .tmp files
        - Files on disk (with or without .tmp suffix) existing for which
          no file object exists in DB
        - Optionally referencing: Is file referenced from another object
          linking to it
    """

    def __init__ (self, db, opt) :
        self.db        = db
        self.opt       = opt
        self.dir       = os.path.join (db.dir, 'files', opt.klass)
        self.cls       = db.getclass (opt.klass)
        self.files     = {}
        self.classname = self.opt.klass
    # end def __init__

    def check (self) :
        self.walk        ()
        self.check_files ()
        if self.opt.reference :
            self.check_refs ()
    # end def check

    def check_files (self) :
        for id in self.nodeids () :
            if id not in self.files :
                print >> sys.stderr, "File missing for %s" % id
            elif self.files [id][1] :
                print >> sys.stderr, "File %s: ext: %s" \
                    % (id, self.files [id][1])
        for id in sorted (self.files.iterkeys ()) :
            try :
                f = self.cls.getnode (id)
            except IndexError :
                r, ext = self.files [id]
                print >> sys.stderr, "No %s object for file %s%s" \
                    % (self.classname, r, ext)
    # end def check_files

    def check_refs (self) :
        """ Check if all class objects are referenced by some other
            object.
        """
        referenced = {}
        for clsname, prop in linkclass_iter (self.db, self.classname) :
            cls = db.getclass (clsname)
            for id in cls.getnodeids () :
                items = cls.get (id, prop)
                if isinstance (cls.properties [prop], Multilink) :
                    for k in items :
                        referenced [int (k)] = True
                else :
                    referenced [int (items)] = True
        for id in self.nodeids () :
            if id not in referenced :
                print >> sys.stderr, "%s %s not referenced" \
                    % (self.classname, id)
    # end def check_refs

    def nodeids (self) :
        """ Sorted iterator over our class's node ids """
        for id in sorted (int (i) for i in self.cls.getnodeids ()) :
            yield id
    # end def nodeids

    def walk (self) :
        length    = len (self.classname)
        for d in os.listdir (self.dir) :
            for f in os.listdir (os.path.join (self.dir, d)) :
                root, ext = os.path.splitext (f)
                if not root.startswith (self.classname) :
                    print >> sys.stderr, "Invalid filename: %s/%s" % (d, f)
                    continue
                id = int (root [length:], 10)
                if id in self.files :
                    ff = self.files [id]
                    print >> sys.stderr, "Duplicate filename: %s/%s%s %s/%s%s" \
                        % (d, ff [0], ff [1], d, root, ext)
                self.files [id] = (root, ext)
    # end def walk

# end class File_Checker

cmd = OptionParser ()
cmd.add_option \
    ( '-c', '--class'
    , dest    = 'klass'
    , help    = 'File class to check, default "file"'
    , default = 'file'
    )
cmd.add_option \
    ( '-r', '--reference'
    , dest    = 'reference'
    , help    = 'Check if files are referenced by another object'
    , action  = 'store_true'
    )
cmd.add_option \
    ( '-t', '--tracker'
    , dest    = 'tracker'
    , help    = 'Tracker directory (default cwd)'
    , default = '.'
    )
cmd.add_option \
    ( '-u', '--update'
    , dest    = 'update'
    , help    = 'Really destroy files/remove disk files (do a commit)'
    , action  = 'store_true'
    )
opt, args = cmd.parse_args ()

if len (args) :
    cmd.error ('No arguments please')
    sys.exit  (23)

sys.path.insert (1, os.path.join (opt.tracker, 'lib'))
from linking import linkclass_iter
tracker = instance.open (opt.tracker)
db      = tracker.open ('admin')

fc      = File_Checker (db, opt)
fc.check ()

if opt.update :
    db.commit()
