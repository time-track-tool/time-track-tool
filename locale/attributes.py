import sys
from rsclib.autosuper import autosuper
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
    classes  = {}

class Class (autosuper) :
    def __init__ (self, db, classname, ** props) :
        print '_("%s")' % classname
        for p in props.keys () :
            print '_("%s")' % p
        db.classes [classname] = True
    def setkey (self, key) : pass
    def update_properties (self, ** properties) :
        for p in properties.keys () :
            print '_("%s")' % p
    default_properties = {}
    setlabelprop = setkey
    setorderprop = setkey

Contact_Class = FileClass = IssueClass = Superseder_Issue_Class = Class
File_Class = Location_Class = Org_Location_Class = Time_Project_Class = Class
db = DB ()

from schemacfg import schemadef
# Don't sort these -- need specific include order:
schemas = \
    ( 'ext_issue'
    , 'company'
    , 'org_loc'
    , 'org_min'
    , 'nickname'
    , 'external_users'
    , 'docissue'
    , 'keyword'
    , 'kpm'
    , 'ext_tracker'
    , 'issue'
    , 'doc'
    , 'it_tracker'
    , 'it_part_of'
    , 'ituser'
    , 'legalclient'
    , 'address'
    , 'adr_ext'
    , 'adr_perm'
    , 'adr_ptr'
    , 'contact'
    , 'contact_sec'
    #, 'person_cust'
    , 'callerid'
    , 'person_adr'
    , 'min_adr'
    , 'person_sep'
    , 'person'
    , 'pers_ext'
    , 'pers_prov'
    , 'sip'
    , 'letter'
    , 'pers_letter'
    , 'sinvoice'
    , 'abo'
    , 'legalclient'
    , 'support'
    , 'erp'
    , 'time_project'
    , 'time_tracker'
    , 'pr'
    , 'dyndns'
    , 'lielas'
    , 'umts'
    , 'extcompany'
    , 'user'
    , 'user_contact'
    , 'email'
    #, 'hamlog'
    , 'ldap'
    , 'core'
    , 'extuser'
    , 'light'
    , 'msg_header'
    , 'nickname'
    , 'rouser'
    , 'sync_id'
    )

importer = schemadef.Importer (globals (), schemas)
