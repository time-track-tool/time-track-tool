import sys
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
    setorderprop = setkey

Contact_Class = FileClass = IssueClass = Class
db = DB ()

from schemacfg import schemadef
# Don't sort these -- need specific include order:
schemas = \
    ( 'ext_issue'
    , 'company'
    , 'issue'
    , 'it_tracker'
    , 'legalclient'
    , 'nwm'
    , 'time_tracker'
    , 'complex'
    , 'address'
    , 'adr_ext'
    , 'adr_ptr'
    , 'contact'
    , 'person_adr'
    , 'person_sep'
    , 'person'
    , 'pers_ext'
    , 'support'
    , 'letter'
    , 'pers_letter'
    , 'sinvoice'
    , 'abo'
    , 'legalclient'
    , 'support'
    , 'erp'
    , 'doc'
    , 'dyndns'
    , 'lielas'
    , 'umts'
    , 'user'
    , 'email'
    , 'core'
    )
importer = schemadef.Importer (globals (), schemas)

Department_Class (db, ''"department")
