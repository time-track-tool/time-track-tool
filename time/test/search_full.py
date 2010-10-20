properties = \
    [ ( 'adr_type'
      , [ ( 'code'
          , ["admin", "adr_readonly", "support", "user"]
          )
        , ( 'description'
          , ["admin", "adr_readonly", "support", "user"]
          )
        , ( 'typecat'
          , ["admin", "adr_readonly", "support", "user"]
          )
        ]
      )
    , ( 'adr_type_cat'
      , [ ( 'code'
          , ["admin", "adr_readonly", "support", "user"]
          )
        , ( 'description'
          , ["admin", "adr_readonly", "support", "user"]
          )
        , ( 'type_valid'
          , ["admin", "adr_readonly", "support", "user"]
          )
        ]
      )
    , ( 'area'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'artefact'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'filename_format'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'category'
      , [ ( 'cert_sw'
          , ["admin", "user"]
          )
        , ( 'default_part_of'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'nosy'
          , ["admin", "user"]
          )
        , ( 'responsible'
          , ["admin", "user"]
          )
        , ( 'valid'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'contact'
      , [ ( 'contact'
          , ["admin", "adr_readonly", "support", "user"]
          )
        , ( 'contact_type'
          , ["admin", "adr_readonly", "support", "user"]
          )
        , ( 'customer'
          , ["admin", "adr_readonly", "support", "user"]
          )
        , ( 'description'
          , ["admin", "adr_readonly", "support", "user"]
          )
        ]
      )
    , ( 'contact_type'
      , [ ( 'description'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'name'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'order'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'url_template'
          , ["admin", "adr_readonly", "user"]
          )
        ]
      )
    , ( 'cost_center'
      , [ ( 'cost_center_group'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'organisation'
          , ["admin", "user"]
          )
        , ( 'status'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'cost_center_group'
      , [ ( 'active'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'responsible'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'cost_center_status'
      , [ ( 'active'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'customer'
      , [ ( 'adr_type'
          , ["admin", "support", "user"]
          )
        , ( 'affix'
          , ["admin", "support", "user"]
          )
        , ( 'city'
          , ["admin", "support", "user"]
          )
        , ( 'contacts'
          , ["admin", "support", "user"]
          )
        , ( 'country'
          , ["admin", "support", "user"]
          )
        , ( 'files'
          , ["admin", "support", "user"]
          )
        , ( 'firstname'
          , ["admin", "support", "user"]
          )
        , ( 'function'
          , ["admin", "support", "user"]
          )
        , ( 'initial'
          , ["admin", "support", "user"]
          )
        , ( 'lastname'
          , ["admin", "support", "user"]
          )
        , ( 'lettertitle'
          , ["admin", "support", "user"]
          )
        , ( 'lookalike_city'
          , ["admin", "support", "user"]
          )
        , ( 'lookalike_firstname'
          , ["admin", "support", "user"]
          )
        , ( 'lookalike_function'
          , ["admin", "support", "user"]
          )
        , ( 'lookalike_lastname'
          , ["admin", "support", "user"]
          )
        , ( 'lookalike_street'
          , ["admin", "support", "user"]
          )
        , ( 'messages'
          , ["admin", "support", "user"]
          )
        , ( 'name'
          , ["admin", "support", "user"]
          )
        , ( 'postalcode'
          , ["admin", "support", "user"]
          )
        , ( 'salutation'
          , ["admin", "support", "user"]
          )
        , ( 'street'
          , ["admin", "support", "user"]
          )
        , ( 'title'
          , ["admin", "support", "user"]
          )
        , ( 'valid'
          , ["admin", "support", "user"]
          )
        ]
      )
    , ( 'daily_record'
      , [ ( 'date'
          , ["admin", "user"]
          )
        , ( 'required_overtime'
          , ["admin", "user"]
          )
        , ( 'status'
          , ["admin", "user"]
          )
        , ( 'time_record'
          , ["admin", "user"]
          )
        , ( 'tr_duration_ok'
          , ["admin", "user"]
          )
        , ( 'user'
          , ["admin", "user"]
          )
        , ( 'weekend_allowed'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'daily_record_freeze'
      , [ ( 'achieved_hours'
          , ["admin", "controlling", "hr"]
          )
        , ( 'balance'
          , ["admin", "controlling", "hr"]
          )
        , ( 'date'
          , ["admin", "controlling", "hr"]
          )
        , ( 'frozen'
          , ["admin", "controlling", "hr"]
          )
        , ( 'month_balance'
          , ["admin", "controlling", "hr"]
          )
        , ( 'month_validity_date'
          , ["admin", "controlling", "hr"]
          )
        , ( 'user'
          , ["admin", "controlling", "hr"]
          )
        , ( 'validity_date'
          , ["admin", "controlling", "hr"]
          )
        , ( 'week_balance'
          , ["admin", "controlling", "hr"]
          )
        ]
      )
    , ( 'daily_record_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'department'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'doc_num'
          , ["admin", "user"]
          )
        , ( 'manager'
          , ["admin", "user"]
          )
        , ( 'messages'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'part_of'
          , ["admin", "user"]
          )
        , ( 'valid_from'
          , ["admin", "user"]
          )
        , ( 'valid_to'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'doc'
      , [ ( 'artefact'
          , ["admin", "user"]
          )
        , ( 'department'
          , ["admin", "user"]
          )
        , ( 'document_nr'
          , ["admin", "user"]
          )
        , ( 'files'
          , ["admin", "user"]
          )
        , ( 'link'
          , ["admin", "user"]
          )
        , ( 'messages'
          , ["admin", "user"]
          )
        , ( 'nosy'
          , ["admin", "user"]
          )
        , ( 'product_type'
          , ["admin", "user"]
          )
        , ( 'reference'
          , ["admin", "user"]
          )
        , ( 'responsible'
          , ["admin", "user"]
          )
        , ( 'state_changed_by'
          , ["admin", "user"]
          )
        , ( 'status'
          , ["admin", "user"]
          )
        , ( 'title'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'doc_status'
      , [ ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        , ( 'transitions'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'file'
      , [ ( 'content'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'type'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'issue'
      , [ ( 'area'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'category'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'closed'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'composed_of'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'confidential'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'cur_est_begin'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'cur_est_end'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'deadline'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'depends'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'earliest_start'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'effective_prio'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'files'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'files_affected'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'fixed_in'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'keywords'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'kind'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'maturity_index'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'messages'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'needs'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'needs_doc'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'nosy'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'numeric_effort'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'part_of'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'planned_begin'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'planned_end'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'priority'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'release'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'responsible'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'severity'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'status'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'superseder'
          , ["admin", "issue_admin", "user"]
          )
        , ( 'title'
          , ["admin", "issue_admin", "user"]
          )
        ]
      )
    , ( 'it_category'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'it_issue'
      , [ ( 'category'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'confidential'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'deadline'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'files'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'it_prio'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'it_project'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'messages'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'nosy'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'responsible'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'stakeholder'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'status'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'superseder'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'title'
          , ["admin", "it", "itview", "user"]
          )
        ]
      )
    , ( 'it_issue_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        , ( 'relaxed'
          , ["admin", "user"]
          )
        , ( 'transitions'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'it_prio'
      , [ ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'it_project'
      , [ ( 'category'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'confidential'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'deadline'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'files'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'it_prio'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'messages'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'nosy'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'responsible'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'stakeholder'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'status'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'title'
          , ["admin", "it", "itview", "user"]
          )
        ]
      )
    , ( 'it_project_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        , ( 'transitions'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'keyword'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'kind'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'location'
      , [ ( 'address'
          , ["admin", "user"]
          )
        , ( 'country'
          , ["admin", "user"]
          )
        , ( 'domain_part'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'meeting_room'
      , [ ( 'name'
          , ["admin", "user"]
          )
        , ( 'phone'
          , ["admin", "user"]
          )
        , ( 'room'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'msg'
      , [ ( 'author'
          , ["admin", "user"]
          )
        , ( 'content'
          , ["admin", "user"]
          )
        , ( 'date'
          , ["admin", "user"]
          )
        , ( 'files'
          , ["admin", "user"]
          )
        , ( 'header'
          , ["admin", "user"]
          )
        , ( 'inreplyto'
          , ["admin", "user"]
          )
        , ( 'keywords'
          , ["admin", "user"]
          )
        , ( 'messageid'
          , ["admin", "user"]
          )
        , ( 'recipients'
          , ["admin", "user"]
          )
        , ( 'subject'
          , ["admin", "user"]
          )
        , ( 'summary'
          , ["admin", "user"]
          )
        , ( 'type'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'msg_keyword'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'org_location'
      , [ ( 'location'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'organisation'
          , ["admin", "user"]
          )
        , ( 'phone'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'organisation'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'mail_domain'
          , ["admin", "user"]
          )
        , ( 'messages'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'valid_from'
          , ["admin", "user"]
          )
        , ( 'valid_to'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'overtime_correction'
      , [ ( 'comment'
          , ["admin", "controlling", "hr"]
          )
        , ( 'date'
          , ["admin", "controlling", "hr"]
          )
        , ( 'user'
          , ["admin", "controlling", "hr"]
          )
        , ( 'value'
          , ["admin", "controlling", "hr"]
          )
        ]
      )
    , ( 'overtime_period'
      , [ ( 'months'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        , ( 'weekly'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'position'
      , [ ( 'position'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'product_type'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'public_holiday'
      , [ ( 'date'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        , ( 'is_half'
          , ["admin", "user"]
          )
        , ( 'locations'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'query'
      , [ ( 'klass'
          , ["admin", "controlling", "user"]
          )
        , ( 'name'
          , ["admin", "controlling", "user"]
          )
        , ( 'private_for'
          , ["admin", "controlling", "user"]
          )
        , ( 'tmplate'
          , ["admin", "controlling", "user"]
          )
        , ( 'url'
          , ["admin", "controlling", "user"]
          )
        ]
      )
    , ( 'reference'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'room'
      , [ ( 'location'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'severity'
      , [ ( 'abbreviation'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'sex'
      , [ ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        , ( 'transitions'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'status_transition'
      , [ ( 'name'
          , ["admin", "user"]
          )
        , ( 'require_msg'
          , ["admin", "user"]
          )
        , ( 'require_resp_change'
          , ["admin", "user"]
          )
        , ( 'target'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'summary_report'
      , [ ( 'all_in'
          , ["admin", "user"]
          )
        , ( 'cost_center'
          , ["admin", "user"]
          )
        , ( 'cost_center_group'
          , ["admin", "user"]
          )
        , ( 'date'
          , ["admin", "user"]
          )
        , ( 'department'
          , ["admin", "user"]
          )
        , ( 'op_project'
          , ["admin", "user"]
          )
        , ( 'org_location'
          , ["admin", "user"]
          )
        , ( 'planned_effort'
          , ["admin", "user"]
          )
        , ( 'show_all_users'
          , ["admin", "user"]
          )
        , ( 'show_empty'
          , ["admin", "user"]
          )
        , ( 'show_missing'
          , ["admin", "user"]
          )
        , ( 'status'
          , ["admin", "user"]
          )
        , ( 'summary'
          , ["admin", "user"]
          )
        , ( 'summary_type'
          , ["admin", "user"]
          )
        , ( 'supervisor'
          , ["admin", "user"]
          )
        , ( 'time_project'
          , ["admin", "user"]
          )
        , ( 'time_wp'
          , ["admin", "user"]
          )
        , ( 'time_wp_group'
          , ["admin", "user"]
          )
        , ( 'user'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'summary_type'
      , [ ( 'is_staff'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'sup_prio'
      , [ ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'sup_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        , ( 'relaxed'
          , ["admin", "user"]
          )
        , ( 'transitions'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'support'
      , [ ( 'category'
          , ["admin", "support", "user"]
          )
        , ( 'closed'
          , ["admin", "support", "user"]
          )
        , ( 'confidential'
          , ["admin", "support", "user"]
          )
        , ( 'customer'
          , ["admin", "support", "user"]
          )
        , ( 'files'
          , ["admin", "support", "user"]
          )
        , ( 'messages'
          , ["admin", "support", "user"]
          )
        , ( 'nosy'
          , ["admin", "support", "user"]
          )
        , ( 'numeric_effort'
          , ["admin", "support", "user"]
          )
        , ( 'prio'
          , ["admin", "support", "user"]
          )
        , ( 'related_issues'
          , ["admin", "support", "user"]
          )
        , ( 'release'
          , ["admin", "support", "user"]
          )
        , ( 'responsible'
          , ["admin", "support", "user"]
          )
        , ( 'serial_number'
          , ["admin", "support", "user"]
          )
        , ( 'status'
          , ["admin", "support", "user"]
          )
        , ( 'superseder'
          , ["admin", "support", "user"]
          )
        , ( 'title'
          , ["admin", "support", "user"]
          )
        ]
      )
    , ( 'time_activity'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'travel'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'time_project'
      , [ ( 'department'
          , ["admin", "controlling", "project", "project_view"]
          )
        , ( 'deputy'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'description'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'is_public_holiday'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'max_hours'
          , ["admin", "controlling", "project", "project_view"]
          )
        , ( 'name'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'no_overtime'
          , ["admin", "controlling", "project", "project_view"]
          )
        , ( 'nosy'
          , ["admin", "controlling", "project", "project_view"]
          )
        , ( 'op_project'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'organisation'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'planned_effort'
          , ["admin", "controlling", "project", "project_view"]
          )
        , ( 'responsible'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'status'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'work_location'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        ]
      )
    , ( 'time_project_status'
      , [ ( 'active'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'time_record'
      , [ ( 'comment'
          , ["admin", "controlling", "hr", "user"]
          )
        , ( 'daily_record'
          , ["admin", "controlling", "hr", "user"]
          )
        , ( 'dist'
          , ["admin", "controlling", "hr", "user"]
          )
        , ( 'duration'
          , ["admin", "controlling", "hr", "user"]
          )
        , ( 'end'
          , ["admin", "controlling", "hr", "user"]
          )
        , ( 'end_generated'
          , ["admin", "controlling", "hr", "user"]
          )
        , ( 'start'
          , ["admin", "controlling", "hr", "user"]
          )
        , ( 'start_generated'
          , ["admin", "controlling", "hr", "user"]
          )
        , ( 'time_activity'
          , ["admin", "controlling", "hr", "user"]
          )
        , ( 'tr_duration'
          , ["admin", "controlling", "hr", "user"]
          )
        , ( 'work_location'
          , ["admin", "controlling", "hr", "user"]
          )
        , ( 'wp'
          , ["admin", "controlling", "hr", "user"]
          )
        ]
      )
    , ( 'time_wp'
      , [ ( 'bookers'
          , ["admin", "controlling", "project", "project_view"]
          )
        , ( 'cost_center'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'description'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'durations_allowed'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'name'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'planned_effort'
          , ["admin", "controlling", "project", "project_view"]
          )
        , ( 'project'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'responsible'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'time_end'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'time_start'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'travel'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        , ( 'wp_no'
          , ["admin", "controlling", "project", "project_view", "user"]
          )
        ]
      )
    , ( 'time_wp_group'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'wps'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'user'
      , [ ( 'address'
          , ["admin", "user"]
          )
        , ( 'alternate_addresses'
          , ["admin", "user"]
          )
        , ( 'clearance_by'
          , ["admin", "user"]
          )
        , ( 'department'
          , ["admin", "user"]
          )
        , ( 'external_phone'
          , ["admin", "user"]
          )
        , ( 'firstname'
          , ["admin", "user"]
          )
        , ( 'internal_phone'
          , ["admin", "user"]
          )
        , ( 'job_description'
          , ["admin", "user"]
          )
        , ( 'lastname'
          , ["admin", "user"]
          )
        , ( 'lunch_duration'
          , ["admin", "user"]
          )
        , ( 'lunch_start'
          , ["admin", "user"]
          )
        , ( 'nickname'
          , ["admin", "user"]
          )
        , ( 'org_location'
          , ["admin"]
          )
        , ( 'password'
          , ["admin", "user"]
          )
        , ( 'phone'
          , ["admin", "user"]
          )
        , ( 'pictures'
          , ["admin", "user"]
          )
        , ( 'position'
          , ["admin", "user"]
          )
        , ( 'private_mobile'
          , ["admin"]
          )
        , ( 'private_mobile_visible'
          , ["admin", "user"]
          )
        , ( 'private_phone'
          , ["admin"]
          )
        , ( 'private_phone_visible'
          , ["admin", "user"]
          )
        , ( 'queries'
          , ["admin", "user"]
          )
        , ( 'quick_dialling'
          , ["admin", "user"]
          )
        , ( 'realname'
          , ["admin", "user"]
          )
        , ( 'roles'
          , ["admin", "controlling"]
          )
        , ( 'room'
          , ["admin", "user"]
          )
        , ( 'sex'
          , ["admin", "user"]
          )
        , ( 'status'
          , ["admin", "user"]
          )
        , ( 'subst_active'
          , ["admin", "user"]
          )
        , ( 'substitute'
          , ["admin", "user"]
          )
        , ( 'supervisor'
          , ["admin", "user"]
          )
        , ( 'timezone'
          , ["admin", "user"]
          )
        , ( 'timing_info'
          , ["admin"]
          )
        , ( 'title'
          , ["admin", "user"]
          )
        , ( 'tt_lines'
          , ["admin", "user"]
          )
        , ( 'username'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'user_dynamic'
      , [ ( 'additional_hours'
          , ["admin", "hr"]
          )
        , ( 'all_in'
          , ["admin", "hr"]
          )
        , ( 'booking_allowed'
          , ["admin", "hr"]
          )
        , ( 'daily_worktime'
          , ["admin", "hr"]
          )
        , ( 'department'
          , ["admin", "hr"]
          )
        , ( 'durations_allowed'
          , ["admin", "hr"]
          )
        , ( 'hours_fri'
          , ["admin", "hr"]
          )
        , ( 'hours_mon'
          , ["admin", "hr"]
          )
        , ( 'hours_sat'
          , ["admin", "hr"]
          )
        , ( 'hours_sun'
          , ["admin", "hr"]
          )
        , ( 'hours_thu'
          , ["admin", "hr"]
          )
        , ( 'hours_tue'
          , ["admin", "hr"]
          )
        , ( 'hours_wed'
          , ["admin", "hr"]
          )
        , ( 'org_location'
          , ["admin", "hr"]
          )
        , ( 'overtime_period'
          , ["admin", "hr"]
          )
        , ( 'supp_per_period'
          , ["admin", "hr"]
          )
        , ( 'supp_weekly_hours'
          , ["admin", "hr"]
          )
        , ( 'travel_full'
          , ["admin", "hr"]
          )
        , ( 'user'
          , ["admin", "hr"]
          )
        , ( 'vacation_remaining'
          , ["admin", "hr"]
          )
        , ( 'vacation_yearly'
          , ["admin", "hr"]
          )
        , ( 'valid_from'
          , ["admin", "hr"]
          )
        , ( 'valid_to'
          , ["admin", "hr"]
          )
        , ( 'weekend_allowed'
          , ["admin", "hr"]
          )
        , ( 'weekly_hours'
          , ["admin", "hr"]
          )
        ]
      )
    , ( 'user_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'valid'
      , [ ( 'description'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'name'
          , ["admin", "adr_readonly", "user"]
          )
        ]
      )
    , ( 'work_location'
      , [ ( 'code'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
