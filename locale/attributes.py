import sys
from rsclib.autosuper import autosuper
sys.path.insert (0, '../lib')

class String :
    def __init__ (self, *v, **kw) :
        rmul = kw.get ('rev_multilink')
        if rmul :
            print '_("%s")' % rmul

Link = Multilink = Password = Date = Boolean = Number = Interval = String
Integer = String

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
        for p in props :
            print '_("%s")' % p
        db.classes [classname] = True
    def setkey (self, key) : pass
    def update_properties (self, ** properties) :
        for p in properties :
            print '_("%s")' % p
    default_properties = {}
    setlabelprop = setkey
    setorderprop = setkey

Contact_Class = FileClass = IssueClass = Superseder_Issue_Class = Class
File_Class = Location_Class = Org_Location_Class = Time_Project_Class = Class
Currency_Class = Class
#Person_Class = Invoice_Class = Letter_Class = Min_Issue_Class = Class
#Address_Class = Contact_Type_Class = Ext_Class = Msg_Class = Class
#Department_Class = Full_Issue_Class = Nosy_Issue_Class = Class
#Ext_Tracker_Class = Category_Class = Optional_Doc_Issue_Class = Class
#Ext_Mixin = IT_Issue_Baseclass = Organisation_Class = Class
#Time_Project_Status_Class = Currency_Class = SAP_CC_Class = Class
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
    , 'msg_header'
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
    #, 'min_adr' # Do not use, overrides real Address_Class
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
    , 'hamlog'
    , 'ldap'
    , 'core'
    , 'extuser'
    , 'light'
    , 'nickname'
    , 'rouser'
    , 'sync_id'
    , 'job_log'
    , 'recipe'
    )

importer = schemadef.Importer (globals (), schemas)
