import sys
sys.path.insert (0, '../schema')
sys.path.insert (0, '../lib')

class String :
    def __init__ (self, *v, **kw) : pass

Link = Multilink = Password = Date = Boolean = Number = String

class Security :
    def addRole (*v, **kw) : pass
    addPermission = addPermissionToRole = addRole
    role = ''

class DB :
    security = Security ()

class Class :
    def __init__ (self, db, classname, ** props) :
        print '_("%s")' % classname
        for p in props.keys () :
            print '_("%s")' % p
    def setkey (self, key) : pass
    setlabelprop = setkey

FileClass = IssueClass = Class
db = DB ()

import schemadef
schemas = \
    ( 'ext_issue'
    , 'company'
    , 'issue'
    , 'it_tracker'
    , 'nwm'
    , 'time_tracker'
    , 'complex'
    , 'address'
    , 'adr_ext'
    , 'sinvoice'
    , 'abo'
    , 'legalclient'
    , 'erp'
    , 'doc'
    , 'core'
    )
importer = schemadef.Importer (globals (), schemas)

Department_Class (db, ''"department")
