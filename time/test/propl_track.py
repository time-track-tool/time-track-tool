properties = \
    [ ( 'area'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'category'
      , [ 'cert_sw'
        , 'default_part_of'
        , 'description'
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
      , [ 'confidential'
        , 'contacts'
        , 'fromaddress'
        , 'is_valid'
        , 'maildomain'
        , 'name'
        , 'nosy'
        , 'nosygroups'
        , 'responsible'
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
        ]
      )
    , ( 'it_issue'
      , [ 'category'
        , 'confidential'
        , 'deadline'
        , 'files'
        , 'it_prio'
        , 'it_project'
        , 'messages'
        , 'nosy'
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
      , [ 'name'
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
      , [ 'name'
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
    , ( 'support'
      , [ 'bcc'
        , 'category'
        , 'cc'
        , 'classification'
        , 'closed'
        , 'confidential'
        , 'customer'
        , 'emails'
        , 'files'
        , 'messages'
        , 'nosy'
        , 'numeric_effort'
        , 'prio'
        , 'related_issues'
        , 'release'
        , 'responsible'
        , 'send_to_customer'
        , 'serial_number'
        , 'status'
        , 'superseder'
        , 'title'
        ]
      )
    , ( 'user'
      , [ 'address'
        , 'alternate_addresses'
        , 'csv_delimiter'
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
    , ( 'user_contact'
      , [ 'contact'
        , 'contact_type'
        , 'description'
        , 'order'
        , 'room'
        , 'user'
        , 'visible'
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
