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
        , 'severity'
        , 'status'
        , 'superseder'
        , 'title'
        ]
      )
    , ( 'it_category'
      , [ 'description'
        , 'name'
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
        ]
      )
    , ( 'kpm'
      , [ 'analysis'
        , 'description'
        , 'fault_frequency'
        , 'hardware_version'
        , 'issue'
        , 'kpm_function'
        , 'ready_for_sync'
        , 'reproduceable'
        , 'supplier_answer'
        ]
      )
    , ( 'kpm_function'
      , [ 'kpm_group'
        , 'kpm_key'
        , 'name'
        , 'order'
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
      , [ 'name'
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
    , ( 'support'
      , [ 'analysis_end'
        , 'analysis_result'
        , 'analysis_start'
        , 'bcc'
        , 'category'
        , 'cc'
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
        , 'status'
        , 'superseder'
        , 'title'
        , 'type'
        , 'warranty'
        ]
      )
    , ( 'user'
      , [ 'address'
        , 'alternate_addresses'
        , 'csv_delimiter'
        , 'guid'
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
