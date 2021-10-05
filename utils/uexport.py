#!/usr/bin/python3

from argparse import ArgumentParser
from rsclib   import sqlparser

# Read a database dump and export only the data relevant for the given
# users. Optionally strip everything before a cut-off date.

class Exporter (sqlparser.SQL_Parser) :

    empty_tables = \
        ['absence', 'artefact', 'doc', 'doc_category', 'doc_status'
        , 'file', 'job_log', 'query', 'reference', 'time_report'
        , 'time_wp_group', 'timesheet', 'product_family', 'reporting_group'
        ]
    empty_multilinks = \
        [ 'doc_files', 'doc_messages', 'doc_nosy', 'msg_files'
        , 'doc_status_transitions', 'time_project_product_family'
        , 'time_project_reporting_group', 'msg_recipients'
        , 'time_wp_group_wps', 'user_pictures', 'user_queries'
        , 'time_project_purchasing_agents', 'time_project_nosy'
        ]
    empty_single_tables = \
        [ 'time_record__journal', 'daily_record__journal'
        , 'user__journal', 'user_contact__journal'
        , 'user_dynamic__journal'
        , '__words', '__textids'
        ]
    obsolete_multilinks = \
        [ 'doc_issue_status_may_change_state_to'
        , 'doc_issue_status_nosy', 'doc_issue_status_transitions'
        , 'issue_composed_of', 'issue_depends', 'issue_external_company'
        , 'issue_files', 'issue_keywords', 'issue_messages'
        , 'issue_needs', 'issue_nosy', 'issue_superseder'
        , 'it_issue_files', 'it_issue_messages', 'it_issue_nosy'
        , 'it_issue_status_transitions', 'it_issue_superseder'
        , 'it_project_files', 'it_project_messages', 'it_project_nosy'
        , 'it_project_status_transitions', 'mailgroup_nosy'
        , 'sup_status_transitions', 'support_emails'
        , 'support_files', 'support_messages', 'support_nosy'
        , 'support_related_issues', 'support_superseder'
        , 'category_nosy', 'customer_contacts', 'customer_nosy'
        , 'customer_nosygroups', 'status_transitions'
        ]

    def __init__ (self, args, **kw) :
        self.args = args
        self.__super.__init__ (**kw)
        # Remove contents of several tables:
        for t in self.empty_tables :
            tn = '_' + t
            self.register_empty_table (tn)
            # Remove journals too
            tn = '__'.join ((t, 'journal'))
            self.register_empty_table (tn)
        self.uids = dict.fromkeys (int (i) for i in self.args.user_id)
        # admin and anonymous
        self.uids [1] = True
        self.uids [2] = True
        self.drid = {}
        self.wpid = {}
        for t in self.empty_multilinks :
            self.register_empty_table (t)
        for t in self.empty_single_tables :
            self.register_empty_table (t)
        for t in self.obsolete_multilinks :
            self.register_drop_table (t)
        self.register_table_callback ('_user',         self.user_callback)
        self.register_table_callback ('_daily_record', self.dr_callback)
        self.register_table_callback ('_time_record',  self.tr_callback)
        self.register_table_callback \
            ('daily_record_time_record', self.drtr_callback)
    # end def __init__

    def user_callback (self, rec) :
        if rec.id in self.uids :
            rec._supervisor = rec._substitute = 1
            return True
        return False
    # end def user_callback

    def dr_callback (self, rec) :
        if rec._user in self.uids :
            self.drid [rec.id] = True
            return True
        return False
    # end def dr_callback

    def tr_callback (self, rec) :
        if rec._daily_record in self.drid :
            self.wpid [rec._wp] = True
            return True
        return False
    # end def tr_callback

    def drtr_callback (self, rec) :
        if rec.nodeid in self.drid :
            return True
        return False
    # end def drtr_callback

    def export (self) :
        tpid = {}
        drfnew = []
        for i in self.tables._daily_record_freeze.contents :
            if i._user in self.uids :
                drfnew.append (i)
        self.tables._daily_record_freeze.contents = drfnew
        ls = []
        for i in self.tables._leave_submission.contents :
            if i._user in self.uids :
                ls.append (i)
        self.tables._leave_submission.contents = ls
        otc = []
        for i in self.tables._overtime_correction.contents :
            if i._user in self.uids :
                otc.append (i)
        self.tables._overtime_correction.contents = otc
        bookers = []
        bookwp = {}
        for i in self.tables.time_wp_bookers.contents :
            if i.linkid in self.uids :
                bookers.append (i)
                bookwp [i.nodeid] = True
        self.tables.time_wp_bookers.contents = bookers
        wps = []
        for i in self.tables._time_wp.contents :
            if i.id in self.wpid or i.id in bookwp :
                i._responsible = 1
                wps.append (i)
                tpid [i._project] = True
        self.tables._time_wp.contents = wps
        tps = []
        for i in self.tables._time_project.contents :
            if i.id in tpid :
                tps.append (i)
        self.tables._time_project.contents = tps
        # contacts, first go over multilink and retain only the ones for
        # the users we want to retain
        cml = []
        ucid = {}
        for i in self.tables.user_contacts.contents :
            if i.nodeid in self.uids :
                cml.append (i)
                ucid [i.linkid] = True
        self.tables.user_contacts.contents = cml
        uc = []
        for i in self.tables._user_contact.contents :
            if i.id in ucid :
                uc.append (i)
        self.tables._user_contact.contents = uc
        ud = []
        for i in self.tables._user_dynamic.contents :
            if i._user in self.uids :
                ud.append (i)
        self.tables._user_dynamic.contents = ud
        vc = []
        for i in self.tables._vacation_correction.contents :
            if i._user in self.uids :
                vc.append (i)
        self.tables._vacation_correction.contents = vc
        ufr = []
        fr  = {}
        for i in self.tables._user_functional_role.contents :
            if i._user in self.uids :
                ufr.append (i)
                fr [i._functional_role] = True
        self.tables._user_functional_role.contents = ufr
        frn = []
        for i in self.tables._functional_role.contents :
            if i.id in fr :
                frn.append (i)
        self.tables._functional_role.contents = frn
        for i in self.tables._cost_center_group.contents :
            i._responsible = 1
        for i in self.tables._department.contents :
            i._deputy = i._manager = 1
        for i in self.tables._domain_permission.contents :
            i._clearance_by = i._timetracking_by = 1
        for i in self.tables._msg.contents :
            i._author = 1
        for tblname in '_sap_cc', '_time_project' :
            tbl = getattr (self.tables, tblname)
            for i in tbl.contents :
                i._deputy = i._group_lead = i._responsible = i._team_lead = 1
    # end def export

# end class Exporter


def main () :
    cmd = ArgumentParser ()
    cmd.add_argument \
        ( 'filename'
        , help    = 'File to anonymize'
        )
    cmd.add_argument \
        ( '-u', '--user-id'
        , help    = 'Specify users to retain, may be given multiple times'
        , action  = 'append'
        , default = []
        )

    args = cmd.parse_args ()
    e = Exporter (args)
    with open (args.filename, 'rb') as f :
        e.parse (f)
    e.export ()
    print (e.as_pgsql ().decode ('utf-8'))
# end def main

if __name__ == '__main__' :
    main ()
