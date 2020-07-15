properties = \
    [ ( 'analysis_result'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'area'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'business_unit'
      , [ 'name'
        , 'valid'
        ]
      )
    , ( 'category'
      , [ 'cert_sw'
        , 'default_part_of'
        , 'description'
        , 'ext_trackers'
        , 'name'
        , 'nosy'
        , 'prodcat'
        , 'responsible'
        , 'valid'
        ]
      )
    , ( 'contact'
      , [ 'contact'
        , 'contact_type'
        , 'customer'
        , 'description'
        ]
      )
    , ( 'contact_type'
      , [ 'description'
        , 'name'
        , 'order'
        , 'url_template'
        ]
      )
    , ( 'customer'
      , [ 'business_unit'
        , 'confidential'
        , 'contacts'
        , 'customer_code'
        , 'fromaddress'
        , 'is_customer'
        , 'is_supplier'
        , 'is_valid'
        , 'maildomain'
        , 'name'
        , 'nosy'
        , 'nosygroups'
        , 'responsible'
        , 'rmafrom'
        , 'suppclaimfrom'
        ]
      )
    , ( 'customer_agreement'
      , [ 'customer'
        , 'description'
        , 'product'
        ]
      )
    , ( 'doc_issue_status'
      , [ 'description'
        , 'may_change_state_to'
        , 'name'
        , 'need_msg'
        , 'nosy'
        , 'order'
        , 'transitions'
        ]
      )
    , ( 'domain_permission'
      , [ 'ad_domain'
        , 'clearance_by'
        , 'default_roles'
        , 'roles_enabled'
        , 'status'
        , 'timetracking_by'
        , 'users'
        ]
      )
    , ( 'ext_msg'
      , [ 'ext_id'
        , 'ext_tracker'
        , 'key'
        , 'msg'
        ]
      )
    , ( 'ext_tracker'
      , [ 'description'
        , 'name'
        , 'type'
        , 'url_template'
        ]
      )
    , ( 'ext_tracker_state'
      , [ 'ext_attributes'
        , 'ext_id'
        , 'ext_status'
        , 'ext_tracker'
        , 'issue'
        ]
      )
    , ( 'ext_tracker_type'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'fault_frequency'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'file'
      , [ 'content'
        , 'name'
        , 'type'
        ]
      )
    , ( 'issue'
      , [ 'area'
        , 'category'
        , 'closed'
        , 'composed_of'
        , 'confidential'
        , 'cur_est_begin'
        , 'cur_est_end'
        , 'deadline'
        , 'depends'
        , 'doc_issue_status'
        , 'earliest_start'
        , 'effective_prio'
        , 'effort_hours'
        , 'external_users'
        , 'files'
        , 'files_affected'
        , 'fixed_in'
        , 'inherit_ext'
        , 'keywords'
        , 'kind'
        , 'maturity_index'
        , 'messages'
        , 'needs'
        , 'nosy'
        , 'numeric_effort'
        , 'part_of'
        , 'planned_begin'
        , 'planned_end'
        , 'priority'
        , 'release'
        , 'responsible'
        , 'safety_level'
        , 'severity'
        , 'status'
        , 'superseder'
        , 'test_level'
        , 'title'
        ]
      )
    , ( 'it_category'
      , [ 'description'
        , 'name'
        , 'nosy'
        , 'responsible'
        , 'valid'
        ]
      )
    , ( 'it_int_prio'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'it_issue'
      , [ 'category'
        , 'composed_of'
        , 'confidential'
        , 'deadline'
        , 'files'
        , 'int_prio'
        , 'it_prio'
        , 'it_project'
        , 'it_request_type'
        , 'messages'
        , 'nosy'
        , 'part_of'
        , 'responsible'
        , 'stakeholder'
        , 'status'
        , 'superseder'
        , 'title'
        ]
      )
    , ( 'it_issue_status'
      , [ 'description'
        , 'name'
        , 'order'
        , 'relaxed'
        , 'transitions'
        ]
      )
    , ( 'it_prio'
      , [ 'default'
        , 'must_change'
        , 'name'
        , 'order'
        ]
      )
    , ( 'it_project'
      , [ 'category'
        , 'confidential'
        , 'deadline'
        , 'files'
        , 'it_prio'
        , 'messages'
        , 'nosy'
        , 'responsible'
        , 'stakeholder'
        , 'status'
        , 'title'
        ]
      )
    , ( 'it_project_status'
      , [ 'description'
        , 'name'
        , 'order'
        , 'transitions'
        ]
      )
    , ( 'it_request_type'
      , [ 'close_immediately'
        , 'log_template'
        , 'name'
        , 'order'
        , 'title_regex'
        ]
      )
    , ( 'keyword'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'kind'
      , [ 'description'
        , 'name'
        , 'simple'
        ]
      )
    , ( 'kpm'
      , [ 'analysis'
        , 'customer_effect'
        , 'description'
        , 'fault_frequency'
        , 'hardware_version'
        , 'is_known_limitation'
        , 'issue'
        , 'kpm_function'
        , 'kpm_hw_variant'
        , 'kpm_occurrence'
        , 'kpm_tag'
        , 'planned_correction'
        , 'problem_description'
        , 'problem_solution'
        , 'ready_for_sync'
        , 'reproduceable'
        , 'safety_relevant'
        , 'supplier_answer'
        , 'tested_with'
        , 'workaround'
        ]
      )
    , ( 'kpm_function'
      , [ 'kpm_group'
        , 'kpm_key'
        , 'name'
        , 'order'
        ]
      )
    , ( 'kpm_hw_variant'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'kpm_occurrence'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'kpm_release'
      , [ 'name'
        , 'order'
        , 'valid'
        ]
      )
    , ( 'kpm_tag'
      , [ 'name'
        , 'order'
        , 'valid'
        ]
      )
    , ( 'mailgroup'
      , [ 'default_nosy'
        , 'name'
        , 'nosy'
        ]
      )
    , ( 'msg'
      , [ 'author'
        , 'content'
        , 'date'
        , 'files'
        , 'header'
        , 'inreplyto'
        , 'keywords'
        , 'messageid'
        , 'recipients'
        , 'subject'
        , 'summary'
        , 'type'
        ]
      )
    , ( 'msg_keyword'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'prodcat'
      , [ 'level'
        , 'name'
        , 'valid'
        ]
      )
    , ( 'product'
      , [ 'business_unit'
        , 'description'
        , 'is_series'
        , 'name'
        , 'product_family'
        , 'product_line'
        , 'product_use_case'
        , 'sap_material'
        , 'valid'
        ]
      )
    , ( 'query'
      , [ 'klass'
        , 'name'
        , 'private_for'
        , 'tmplate'
        , 'url'
        ]
      )
    , ( 'return_type'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'safety_level'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'severity'
      , [ 'abbreviation'
        , 'name'
        , 'order'
        ]
      )
    , ( 'status'
      , [ 'description'
        , 'name'
        , 'order'
        , 'simple_transitions'
        , 'transitions'
        ]
      )
    , ( 'status_transition'
      , [ 'name'
        , 'require_msg'
        , 'require_resp_change'
        , 'target'
        ]
      )
    , ( 'sup_classification'
      , [ 'description'
        , 'examples'
        , 'name'
        , 'sup_warranty'
        , 'valid'
        ]
      )
    , ( 'sup_execution'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'sup_prio'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'sup_status'
      , [ 'description'
        , 'name'
        , 'order'
        , 'relaxed'
        , 'transitions'
        ]
      )
    , ( 'sup_type'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'sup_warranty'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'support'
      , [ 'analysis_end'
        , 'analysis_result'
        , 'analysis_start'
        , 'bcc'
        , 'business_unit'
        , 'category'
        , 'cc'
        , 'cc_emails'
        , 'classification'
        , 'closed'
        , 'confidential'
        , 'customer'
        , 'emails'
        , 'execution'
        , 'external_ref'
        , 'files'
        , 'first_reply'
        , 'goods_received'
        , 'goods_sent'
        , 'lot'
        , 'messages'
        , 'nosy'
        , 'number_effected'
        , 'numeric_effort'
        , 'prio'
        , 'prodcat'
        , 'product'
        , 'related_issues'
        , 'related_support'
        , 'release'
        , 'responsible'
        , 'return_type'
        , 'sap_ref'
        , 'satisfied'
        , 'send_to_customer'
        , 'serial_number'
        , 'set_first_reply'
        , 'status'
        , 'superseder'
        , 'title'
        , 'type'
        , 'warranty'
        ]
      )
    , ( 'test_level'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'user'
      , [ 'ad_domain'
        , 'address'
        , 'alternate_addresses'
        , 'csv_delimiter'
        , 'guid'
        , 'hide_message_files'
        , 'nickname'
        , 'password'
        , 'queries'
        , 'realname'
        , 'roles'
        , 'status'
        , 'timezone'
        , 'username'
        ]
      )
    , ( 'user_status'
      , [ 'description'
        , 'is_nosy'
        , 'ldap_group'
        , 'ldap_prio'
        , 'name'
        , 'roles'
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
