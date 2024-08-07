security = """
New Web users get the Roles "User,Nosy"
New Email users get the Role "User"
Role "admin":
 User may access the rest interface (Rest Access)
 User may access the web interface (Web Access)
 User may access the xmlrpc interface (Xmlrpc Access)
 User may create everything (Create)
 User may edit everything (Edit)
 User may manipulate user Roles through the web (Web Roles)
 User may restore everything (Restore)
 User may retire everything (Retire)
 User may use the email interface (Email Access)
 User may view everything (View)
Role "anonymous":
 User may access the web interface (Web Access)
Role "dom-user-edit-facility":
 Users may view/edit user records for ad_domain for which they are in the domain_permission for the user (Edit for "user": ['room'] only)
 Users may view/edit user records for ad_domain for which they are in the domain_permission for the user (View for "user": ['room'] only)
Role "dom-user-edit-gtt":
 User is allowed to create user (Create for "user" only)
 Users may view/edit user records for ad_domain for which they are in the domain_permission for the user (Edit for "user": ['contacts', 'csv_delimiter', 'entry_date', 'department_temp', 'firstname', 'hide_message_files', 'job_description', 'lastname', 'lunch_duration', 'lunch_start', 'nickname', 'pictures', 'position_text', 'room', 'status', 'subst_active', 'substitute', 'supervisor', 'sync_foreign_key', 'timezone', 'tt_lines', 'username', 'vie_user'] only)
 Users may view/edit user records for ad_domain for which they are in the domain_permission for the user (View for "user": ['contacts', 'csv_delimiter', 'department_temp', 'entry_date', 'firstname', 'hide_message_files', 'job_description', 'lastname', 'lunch_duration', 'lunch_start', 'nickname', 'pictures', 'position_text', 'room', 'status', 'subst_active', 'substitute', 'supervisor', 'sync_foreign_key', 'timezone', 'tt_lines', 'username', 'vie_user'] only)
Role "dom-user-edit-hr":
 Users may view/edit user records for ad_domain for which they are in the domain_permission for the user (Edit for "user": ['clearance_by', 'csv_delimiter', 'hide_message_files', 'lunch_duration', 'lunch_start', 'reduced_activity_list', 'room', 'subst_active', 'substitute', 'timezone', 'tt_lines'] only)
 Users may view/edit user records for ad_domain for which they are in the domain_permission for the user (View for "user": ['clearance_by', 'csv_delimiter', 'hide_message_files', 'lunch_duration', 'lunch_start', 'reduced_activity_list', 'room', 'subst_active', 'substitute', 'timezone', 'tt_lines'] only)
Role "dom-user-edit-office":
 Users may view/edit user records for ad_domain for which they are in the domain_permission for the user (Edit for "user": ['contacts', 'position_text', 'room'] only)
 Users may view/edit user records for ad_domain for which they are in the domain_permission for the user (View for "user": ['contacts', 'position_text', 'room'] only)
Role "external":
  (Search for "ext_tracker_state": ('id', 'issue') only)
  (Search for "user": ('id', 'nickname', 'username') only)
 External users are allowed to access issue if they are on the list of allowed external users or there is a transitive permission via containers (Edit for "issue": ['activity', 'actor', 'area', 'category', 'closed', 'composed_of', 'creation', 'creator', 'cur_est_begin', 'cur_est_end', 'deadline', 'depends', 'doc_issue_status', 'earliest_start', 'effective_prio', 'effort_hours', 'external_users', 'files', 'files_affected', 'fixed_in', 'id', 'keywords', 'kind', 'maturity_index', 'messages', 'needs', 'nosy', 'numeric_effort', 'part_of', 'planned_begin', 'planned_end', 'priority', 'release', 'responsible', 'safety_level', 'severity', 'status', 'superseder', 'test_level', 'title'] only)
 External users are allowed to access issue if they are on the list of allowed external users or there is a transitive permission via containers (View for "issue": ['activity', 'actor', 'area', 'category', 'closed', 'composed_of', 'creation', 'creator', 'cur_est_begin', 'cur_est_end', 'deadline', 'depends', 'doc_issue_status', 'earliest_start', 'effective_prio', 'effort_hours', 'external_users', 'files', 'files_affected', 'fixed_in', 'id', 'keywords', 'kind', 'maturity_index', 'messages', 'needs', 'nosy', 'numeric_effort', 'part_of', 'planned_begin', 'planned_end', 'priority', 'release', 'responsible', 'safety_level', 'severity', 'status', 'superseder', 'test_level', 'title'] only)
 User is allowed View on (View for "category": ('id', 'name') only)
 User is allowed View on (View for "user": ('nickname', 'status', 'username') only)
 User is allowed View on (View for "user_status": ('name',) only)
 User is allowed View on file if file is linked from an item with View permission (View for "file" only)
 User is allowed View on msg if msg is linked from an item with View permission (View for "msg" only)
 User is allowed to access area (View for "area" only)
 User is allowed to access doc_issue_status (View for "doc_issue_status" only)
 User is allowed to access ext_tracker (View for "ext_tracker" only)
 User is allowed to access ext_tracker_state (View for "ext_tracker_state" only)
 User is allowed to access ext_tracker_type (View for "ext_tracker_type" only)
 User is allowed to access fault_frequency (View for "fault_frequency" only)
 User is allowed to access keyword (View for "keyword" only)
 User is allowed to access kind (View for "kind" only)
 User is allowed to access kpm (View for "kpm" only)
 User is allowed to access kpm_function (View for "kpm_function" only)
 User is allowed to access kpm_hw_variant (View for "kpm_hw_variant" only)
 User is allowed to access kpm_occurrence (View for "kpm_occurrence" only)
 User is allowed to access kpm_release (View for "kpm_release" only)
 User is allowed to access kpm_tag (View for "kpm_tag" only)
 User is allowed to access msg_keyword (View for "msg_keyword" only)
 User is allowed to access safety_level (View for "safety_level" only)
 User is allowed to access severity (View for "severity" only)
 User is allowed to access status (View for "status" only)
 User is allowed to access status_transition (View for "status_transition" only)
 User is allowed to access test_level (View for "test_level" only)
 User is allowed to create file (Create for "file" only)
 User is allowed to create issue (Create for "issue" only)
 User is allowed to create kpm (Create for "kpm" only)
 User is allowed to create msg (Create for "msg" only)
 User is allowed to create query (Create for "query" only)
 User is allowed to edit kpm (Edit for "kpm" only)
 User is allowed to edit their queries (Edit for "query" only)
 User is allowed to retire their queries (Retire for "query" only)
 User is allowed to search for their own files (Search for "file" only)
 User is allowed to search for their own messages (Search for "msg" only)
 User is allowed to search for their queries (Search for "query" only)
 User is allowed to search issue (Search for "issue" only)
 User is allowed to view their own files (View for "file" only)
 User may access the web interface (Web Access)
 User may use the email interface (Email Access)
 Users are allowed to edit some of their details (Edit for "user": ('csv_delimiter', 'hide_message_files', 'password', 'timezone') only)
 Users are allowed to view some of their details (View for "user": ('activity', 'actor', 'creation', 'creator', 'firstname', 'lastname', 'realname', 'username') only)
 Users are allowed to view their own and public queries for classes where they have search permission (View for "query" only)
Role "issue_admin":
 User is allowed Edit on msg if msg is linked from an item with Edit permission (Edit for "msg" only)
 User is allowed to access issue (View for "issue" only)
 User is allowed to access query (View for "query" only)
 User is allowed to create area (Create for "area" only)
 User is allowed to create category (Create for "category" only)
 User is allowed to create doc_issue_status (Create for "doc_issue_status" only)
 User is allowed to create ext_tracker (Create for "ext_tracker" only)
 User is allowed to create issue (Create for "issue" only)
 User is allowed to create keyword (Create for "keyword" only)
 User is allowed to create kind (Create for "kind" only)
 User is allowed to create msg_keyword (Create for "msg_keyword" only)
 User is allowed to create query (Create for "query" only)
 User is allowed to create safety_level (Create for "safety_level" only)
 User is allowed to create severity (Create for "severity" only)
 User is allowed to create status (Create for "status" only)
 User is allowed to create status_transition (Create for "status_transition" only)
 User is allowed to create test_level (Create for "test_level" only)
 User is allowed to edit area (Edit for "area" only)
 User is allowed to edit category (Edit for "category" only)
 User is allowed to edit doc_issue_status (Edit for "doc_issue_status" only)
 User is allowed to edit ext_tracker (Edit for "ext_tracker" only)
 User is allowed to edit issue (Edit for "issue" only)
 User is allowed to edit keyword (Edit for "keyword" only)
 User is allowed to edit kind (Edit for "kind" only)
 User is allowed to edit msg_keyword (Edit for "msg_keyword" only)
 User is allowed to edit query (Edit for "query" only)
 User is allowed to edit safety_level (Edit for "safety_level" only)
 User is allowed to edit severity (Edit for "severity" only)
 User is allowed to edit status (Edit for "status" only)
 User is allowed to edit status_transition (Edit for "status_transition" only)
 User is allowed to edit test_level (Edit for "test_level" only)
Role "it":
 User is allowed Edit on (Edit for "file": ('name', 'type') only)
 User is allowed Edit on (Edit for "location": ('domain_part',) only)
 User is allowed Edit on (Edit for "organisation": ('domain_part',) only)
 User is allowed Edit on (Edit for "user": ('address', 'alternate_addresses', 'nickname', 'password', 'timezone', 'username') only)
 User is allowed Edit on (Edit for "user": ('firstname', 'lastname', 'realname', 'roles', 'status') only)
 User is allowed Edit on file if file is linked from an item with Edit permission (Edit for "file" only)
 User is allowed Edit on msg if msg is linked from an item with Edit permission (Edit for "msg" only)
 User is allowed View on (View for "user": ('roles',) only)
 User is allowed View on file if file is linked from an item with View permission (View for "file" only)
 User is allowed to access domain_permission (View for "domain_permission" only)
 User is allowed to access it_int_prio (View for "it_int_prio" only)
 User is allowed to access it_issue (View for "it_issue" only)
 User is allowed to access it_project (View for "it_project" only)
 User is allowed to create domain_permission (Create for "domain_permission" only)
 User is allowed to create it_category (Create for "it_category" only)
 User is allowed to create it_int_prio (Create for "it_int_prio" only)
 User is allowed to create it_issue (Create for "it_issue" only)
 User is allowed to create it_project (Create for "it_project" only)
 User is allowed to create it_request_type (Create for "it_request_type" only)
 User is allowed to create mailgroup (Create for "mailgroup" only)
 User is allowed to edit domain_permission (Edit for "domain_permission" only)
 User is allowed to edit it_category (Edit for "it_category" only)
 User is allowed to edit it_int_prio (Edit for "it_int_prio" only)
 User is allowed to edit it_issue (Edit for "it_issue" only)
 User is allowed to edit it_project (Edit for "it_project" only)
 User is allowed to edit it_request_type (Edit for "it_request_type" only)
 User is allowed to edit mailgroup (Edit for "mailgroup" only)
 User may manipulate user Roles through the web (Web Roles)
Role "ituser":
 User is allowed View on file if file is linked from an item with View permission (View for "file" only)
 User is allowed View on msg if msg is linked from an item with View permission (View for "msg" only)
 User is allowed to access it_issue if on nosy list (Edit for "it_issue": ('confidential', 'deadline', 'files', 'messages', 'title') only)
 User is allowed to access it_issue if on nosy list (View for "it_issue": ('activity', 'actor', 'creation', 'creator', 'files', 'messages', 'responsible', 'stakeholder', 'status') only)
 User is allowed to access it_issue_status (View for "it_issue_status" only)
 User is allowed to create file (Create for "file" only)
 User is allowed to create it_issue (Create for "it_issue" only)
 User is allowed to create msg (Create for "msg" only)
 User is allowed to create query (Create for "query" only)
 User is allowed to edit their queries (Edit for "query" only)
 User is allowed to retire their queries (Retire for "query" only)
 User is allowed to search for their own files (Search for "file" only)
 User is allowed to search for their own messages (Search for "msg" only)
 User is allowed to search for their queries (Search for "query" only)
 User is allowed to search it_issue (Search for "it_issue" only)
 User is allowed to see other IT users (View for "user": ('realname', 'username') only)
 User is allowed to view their own files (View for "file" only)
 User may access the web interface (Web Access)
 User may use the email interface (Email Access)
 Users are allowed to edit some of their properties (Edit for "user": ('alternate_addresses', 'csv_delimiter', 'hide_message_files', 'password', 'realname') only)
 Users are allowed to see some of their attributes (View for "user": ('address', 'username') only)
 Users are allowed to view their own and public queries for classes where they have search permission (View for "query" only)
Role "itview":
 User is allowed to access it_int_prio (View for "it_int_prio" only)
 User is allowed to access it_issue (View for "it_issue" only)
 User is allowed to access it_project (View for "it_project" only)
Role "kpm-admin":
 User is allowed to create kpm_function (Create for "kpm_function" only)
 User is allowed to create kpm_hw_variant (Create for "kpm_hw_variant" only)
 User is allowed to create kpm_occurrence (Create for "kpm_occurrence" only)
 User is allowed to create kpm_release (Create for "kpm_release" only)
 User is allowed to create kpm_tag (Create for "kpm_tag" only)
 User is allowed to edit kpm_function (Edit for "kpm_function" only)
 User is allowed to edit kpm_hw_variant (Edit for "kpm_hw_variant" only)
 User is allowed to edit kpm_occurrence (Edit for "kpm_occurrence" only)
 User is allowed to edit kpm_release (Edit for "kpm_release" only)
 User is allowed to edit kpm_tag (Edit for "kpm_tag" only)
Role "msgedit":
  (Search for "msg": ('date', 'id') only)
 User is allowed Edit on (Edit for "msg": ('author', 'date', 'id', 'keywords', 'subject', 'summary') only)
 User is allowed to access ext_msg (View for "ext_msg" only)
 User is allowed to access ext_tracker_state (View for "ext_tracker_state" only)
 User is allowed to access ext_tracker_type (View for "ext_tracker_type" only)
Role "msgsync":
  (Search for "msg": ('date', 'id') only)
 User is allowed Edit on (Edit for "msg": ('author', 'date', 'id', 'keywords', 'subject', 'summary') only)
 User is allowed to access ext_msg (View for "ext_msg" only)
 User is allowed to access ext_tracker_state (View for "ext_tracker_state" only)
 User is allowed to access ext_tracker_type (View for "ext_tracker_type" only)
 User is allowed to create ext_msg (Create for "ext_msg" only)
 User is allowed to create ext_tracker_state (Create for "ext_tracker_state" only)
 User is allowed to edit ext_msg (Edit for "ext_msg" only)
 User is allowed to edit ext_tracker_state (Edit for "ext_tracker_state" only)
Role "nosy":
 User may get nosy messages for issue (Nosy for "issue" only)
 User may get nosy messages for it_issue (Nosy for "it_issue" only)
 User may get nosy messages for it_project (Nosy for "it_project" only)
 User may get nosy messages for support (Nosy for "support" only)
Role "pgp":
Role "readonly-user":
  (Search for "ext_tracker_state": ('id', 'issue') only)
  (Search for "user": ('id', 'nickname', 'username') only)
 Read-only users are allowed to view issue if they are on the list of allowed external users or there is a transitive permission via containers (View for "issue": ['activity', 'actor', 'area', 'category', 'closed', 'composed_of', 'creation', 'creator', 'cur_est_begin', 'cur_est_end', 'deadline', 'depends', 'doc_issue_status', 'earliest_start', 'effective_prio', 'effort_hours', 'external_users', 'files', 'files_affected', 'fixed_in', 'id', 'inherit_ext', 'keywords', 'kind', 'maturity_index', 'messages', 'needs', 'nosy', 'numeric_effort', 'part_of', 'planned_begin', 'planned_end', 'priority', 'release', 'responsible', 'safety_level', 'severity', 'status', 'superseder', 'test_level', 'title'] only)
 User is allowed View on (View for "category": ('id', 'name') only)
 User is allowed View on (View for "user": ('nickname', 'status', 'username') only)
 User is allowed View on (View for "user_status": ('name',) only)
 User is allowed View on file if file is linked from an item with View permission (View for "file" only)
 User is allowed View on msg if msg is linked from an item with View permission (View for "msg" only)
 User is allowed to access area (View for "area" only)
 User is allowed to access doc_issue_status (View for "doc_issue_status" only)
 User is allowed to access ext_tracker (View for "ext_tracker" only)
 User is allowed to access ext_tracker_state (View for "ext_tracker_state" only)
 User is allowed to access ext_tracker_type (View for "ext_tracker_type" only)
 User is allowed to access fault_frequency (View for "fault_frequency" only)
 User is allowed to access keyword (View for "keyword" only)
 User is allowed to access kind (View for "kind" only)
 User is allowed to access kpm (View for "kpm" only)
 User is allowed to access kpm_function (View for "kpm_function" only)
 User is allowed to access kpm_hw_variant (View for "kpm_hw_variant" only)
 User is allowed to access kpm_occurrence (View for "kpm_occurrence" only)
 User is allowed to access kpm_release (View for "kpm_release" only)
 User is allowed to access kpm_tag (View for "kpm_tag" only)
 User is allowed to access msg_keyword (View for "msg_keyword" only)
 User is allowed to access safety_level (View for "safety_level" only)
 User is allowed to access severity (View for "severity" only)
 User is allowed to access status (View for "status" only)
 User is allowed to access status_transition (View for "status_transition" only)
 User is allowed to access test_level (View for "test_level" only)
 User is allowed to search for their own files (Search for "file" only)
 User is allowed to search for their own messages (Search for "msg" only)
 User is allowed to search issue (Search for "issue" only)
 User is allowed to view their own files (View for "file" only)
 User may access the rest interface (Rest Access)
 User may access the web interface (Web Access)
 User may access the xmlrpc interface (Xmlrpc Access)
 User may use the email interface (Email Access)
 Users are allowed to edit some of their details (Edit for "user": ('csv_delimiter', 'hide_message_files', 'timezone') only)
 Users are allowed to view some of their details (View for "user": ('activity', 'actor', 'creation', 'creator', 'firstname', 'lastname', 'realname', 'username') only)
Role "sec-incident-nosy":
 User is allowed to access it_int_prio (View for "it_int_prio" only)
 User is allowed to access it_issue (View for "it_issue" only)
 User is allowed to access it_project (View for "it_project" only)
Role "sec-incident-responsible":
 User is allowed to access it_int_prio (View for "it_int_prio" only)
 User is allowed to access it_issue (View for "it_issue" only)
 User is allowed to access it_project (View for "it_project" only)
Role "sub-login":
Role "supportadmin":
 User is allowed to access analysis_result (View for "analysis_result" only)
 User is allowed to access contact (View for "contact" only)
 User is allowed to access customer (View for "customer" only)
 User is allowed to access customer_agreement (View for "customer_agreement" only)
 User is allowed to access mailgroup (View for "mailgroup" only)
 User is allowed to access return_type (View for "return_type" only)
 User is allowed to access sup_classification (View for "sup_classification" only)
 User is allowed to access support (View for "support" only)
 User is allowed to create analysis_result (Create for "analysis_result" only)
 User is allowed to create contact (Create for "contact" only)
 User is allowed to create contact_type (Create for "contact_type" only)
 User is allowed to create customer (Create for "customer" only)
 User is allowed to create customer_agreement (Create for "customer_agreement" only)
 User is allowed to create mailgroup (Create for "mailgroup" only)
 User is allowed to create return_type (Create for "return_type" only)
 User is allowed to create sup_classification (Create for "sup_classification" only)
 User is allowed to create support (Create for "support" only)
 User is allowed to edit analysis_result (Edit for "analysis_result" only)
 User is allowed to edit contact (Edit for "contact" only)
 User is allowed to edit contact_type (Edit for "contact_type" only)
 User is allowed to edit customer (Edit for "customer" only)
 User is allowed to edit customer_agreement (Edit for "customer_agreement" only)
 User is allowed to edit mailgroup (Edit for "mailgroup" only)
 User is allowed to edit return_type (Edit for "return_type" only)
 User is allowed to edit sup_classification (Edit for "sup_classification" only)
 User is allowed to edit support (Edit for "support" only)
Role "user":
  (Search for "user": ('realname',) only)
 User is allowed Edit on (Edit for "msg": ('keywords',) only)
 User is allowed Edit on file if file is linked from an item with Edit permission (Edit for "file" only)
 User is allowed Edit on issue if issue is non-confidential or user is on nosy list (Edit for "issue" only)
 User is allowed Edit on it_issue if it_issue is non-confidential or user is on nosy list (Edit for "it_issue": ('messages', 'files', 'nosy') only)
 User is allowed Edit on it_project if it_project is non-confidential or user is on nosy list (Edit for "it_project": ('messages', 'files', 'nosy') only)
 User is allowed Edit on support if support is non-confidential or user is on nosy list (Edit for "support": ('analysis_end', 'analysis_result', 'analysis_start', 'bcc', 'business_unit', 'category', 'cc', 'cc_emails', 'classification', 'closed', 'confidential', 'customer', 'emails', 'execution', 'external_ref', 'files', 'goods_received', 'goods_sent', 'lot', 'messages', 'nosy', 'number_effected', 'numeric_effort', 'prio', 'prodcat', 'product', 'related_issues', 'related_support', 'release', 'responsible', 'return_type', 'sap_ref', 'send_to_customer', 'serial_number', 'set_first_reply', 'status', 'superseder', 'title', 'type', 'warranty') only)
 User is allowed View on (View for "user": ('activity', 'actor', 'ad_domain', 'address', 'alternate_addresses', 'creation', 'creator', 'firstname', 'id', 'lastname', 'nickname', 'realname', 'status', 'timezone', 'title', 'username') only)
 User is allowed View on (View for "user": ('activity', 'actor', 'address', 'alternate_addresses', 'creation', 'creator', 'id', 'queries', 'realname', 'status', 'timezone', 'username') only)
 User is allowed View on file if file is linked from an item with View permission (View for "file" only)
 User is allowed View on issue if issue is non-confidential or user is on nosy list (View for "issue" only)
 User is allowed View on it_issue if it_issue is non-confidential or user is on nosy list (View for "it_issue" only)
 User is allowed View on it_project if it_project is non-confidential or user is on nosy list (View for "it_project" only)
 User is allowed View on msg if msg is linked from an item with View permission (View for "msg" only)
 User is allowed View on support if support is non-confidential or user is on nosy list (View for "support" only)
 User is allowed to access analysis_result (View for "analysis_result" only)
 User is allowed to access area (View for "area" only)
 User is allowed to access business_unit (View for "business_unit" only)
 User is allowed to access category (View for "category" only)
 User is allowed to access contact (View for "contact" only)
 User is allowed to access contact_type (View for "contact_type" only)
 User is allowed to access customer (View for "customer" only)
 User is allowed to access customer_agreement (View for "customer_agreement" only)
 User is allowed to access doc_issue_status (View for "doc_issue_status" only)
 User is allowed to access ext_tracker (View for "ext_tracker" only)
 User is allowed to access ext_tracker_state (View for "ext_tracker_state" only)
 User is allowed to access ext_tracker_type (View for "ext_tracker_type" only)
 User is allowed to access fault_frequency (View for "fault_frequency" only)
 User is allowed to access it_category (View for "it_category" only)
 User is allowed to access it_issue_status (View for "it_issue_status" only)
 User is allowed to access it_prio (View for "it_prio" only)
 User is allowed to access it_project_status (View for "it_project_status" only)
 User is allowed to access it_request_type (View for "it_request_type" only)
 User is allowed to access keyword (View for "keyword" only)
 User is allowed to access kind (View for "kind" only)
 User is allowed to access kpm (View for "kpm" only)
 User is allowed to access kpm_function (View for "kpm_function" only)
 User is allowed to access kpm_hw_variant (View for "kpm_hw_variant" only)
 User is allowed to access kpm_occurrence (View for "kpm_occurrence" only)
 User is allowed to access kpm_release (View for "kpm_release" only)
 User is allowed to access kpm_tag (View for "kpm_tag" only)
 User is allowed to access mailgroup (View for "mailgroup" only)
 User is allowed to access msg_keyword (View for "msg_keyword" only)
 User is allowed to access prodcat (View for "prodcat" only)
 User is allowed to access product (View for "product" only)
 User is allowed to access return_type (View for "return_type" only)
 User is allowed to access safety_level (View for "safety_level" only)
 User is allowed to access severity (View for "severity" only)
 User is allowed to access status (View for "status" only)
 User is allowed to access status_transition (View for "status_transition" only)
 User is allowed to access sup_classification (View for "sup_classification" only)
 User is allowed to access sup_execution (View for "sup_execution" only)
 User is allowed to access sup_prio (View for "sup_prio" only)
 User is allowed to access sup_status (View for "sup_status" only)
 User is allowed to access sup_type (View for "sup_type" only)
 User is allowed to access sup_warranty (View for "sup_warranty" only)
 User is allowed to access test_level (View for "test_level" only)
 User is allowed to access user_status (View for "user_status" only)
 User is allowed to create ext_tracker_state (Create for "ext_tracker_state" only)
 User is allowed to create file (Create for "file" only)
 User is allowed to create issue (Create for "issue" only)
 User is allowed to create it_issue (Create for "it_issue" only)
 User is allowed to create kpm (Create for "kpm" only)
 User is allowed to create msg (Create for "msg" only)
 User is allowed to create queries (Create for "query" only)
 User is allowed to create support (Create for "support" only)
 User is allowed to edit (some of) their own user details (Edit for "user": ('csv_delimiter', 'hide_message_files', 'password', 'queries', 'realname', 'timezone') only)
 User is allowed to edit category if he is responsible for it (Edit for "category": ('nosy', 'default_part_of') only)
 User is allowed to edit ext_tracker_state (Edit for "ext_tracker_state" only)
 User is allowed to edit kpm (Edit for "kpm" only)
 User is allowed to edit several fields if he is Responsible for an it_issue (Edit for "it_issue": ('responsible',) only)
 User is allowed to edit several fields if he is Stakeholder/Responsible for an it_issue (Edit for "it_issue": ('deadline', 'status', 'title') only)
 User is allowed to edit their queries (Edit for "query" only)
 User is allowed to retire their queries (Retire for "query" only)
 User is allowed to search for their own files (Search for "file" only)
 User is allowed to search for their own messages (Search for "msg" only)
 User is allowed to search for their queries (Search for "query" only)
 User is allowed to search issue (Search for "issue" only)
 User is allowed to search it_issue (Search for "it_issue" only)
 User is allowed to search it_project (Search for "it_project" only)
 User is allowed to search support (Search for "support" only)
 User is allowed to search user_status (Search for "user": ('status',) only)
 User is allowed to view their own files (View for "file" only)
 User is allowed to view their own messages (View for "msg" only)
 User may access the rest interface (Rest Access)
 User may access the web interface (Web Access)
 User may access the xmlrpc interface (Xmlrpc Access)
 User may use the email interface (Email Access)
 Users are allowed to view their own and public queries for classes where they have search permission (View for "query" only)
Role "user_view":
 User is allowed to access user (View for "user" only)
""".strip ()
