properties = \
    [ ( 'adr_type'
      , [ ( 'code'
          , ["adr_readonly", "support", "user"]
          )
        , ( 'description'
          , ["adr_readonly", "support", "user"]
          )
        , ( 'typecat'
          , ["adr_readonly", "support", "user"]
          )
        ]
      )
    , ( 'adr_type_cat'
      , [ ( 'code'
          , ["adr_readonly", "support", "user"]
          )
        , ( 'description'
          , ["adr_readonly", "support", "user"]
          )
        , ( 'type_valid'
          , ["adr_readonly", "support", "user"]
          )
        ]
      )
    , ( 'area'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'artefact'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'filename_format'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'category'
      , [ ( 'cert_sw'
          , ["user"]
          )
        , ( 'default_part_of'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'nosy'
          , ["user"]
          )
        , ( 'responsible'
          , ["user"]
          )
        , ( 'valid'
          , ["user"]
          )
        ]
      )
    , ( 'contact'
      , [ ( 'contact'
          , ["adr_readonly", "support", "user"]
          )
        , ( 'contact_type'
          , ["adr_readonly", "support", "user"]
          )
        , ( 'customer'
          , ["adr_readonly", "support", "user"]
          )
        , ( 'description'
          , ["adr_readonly", "support", "user"]
          )
        ]
      )
    , ( 'contact_type'
      , [ ( 'description'
          , ["adr_readonly", "user"]
          )
        , ( 'name'
          , ["adr_readonly", "user"]
          )
        , ( 'order'
          , ["adr_readonly", "user"]
          )
        , ( 'url_template'
          , ["adr_readonly", "user"]
          )
        ]
      )
    , ( 'cost_center'
      , [ ( 'cost_center_group'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'organisation'
          , ["user"]
          )
        , ( 'status'
          , ["user"]
          )
        ]
      )
    , ( 'cost_center_group'
      , [ ( 'active'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'responsible'
          , ["user"]
          )
        ]
      )
    , ( 'cost_center_status'
      , [ ( 'active'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'customer'
      , [ ( 'adr_type'
          , ["support", "user"]
          )
        , ( 'affix'
          , ["support", "user"]
          )
        , ( 'city'
          , ["support", "user"]
          )
        , ( 'contacts'
          , ["support", "user"]
          )
        , ( 'country'
          , ["support", "user"]
          )
        , ( 'files'
          , ["support", "user"]
          )
        , ( 'firstname'
          , ["support", "user"]
          )
        , ( 'function'
          , ["support", "user"]
          )
        , ( 'initial'
          , ["support", "user"]
          )
        , ( 'lastname'
          , ["support", "user"]
          )
        , ( 'lettertitle'
          , ["support", "user"]
          )
        , ( 'lookalike_city'
          , ["support", "user"]
          )
        , ( 'lookalike_firstname'
          , ["support", "user"]
          )
        , ( 'lookalike_function'
          , ["support", "user"]
          )
        , ( 'lookalike_lastname'
          , ["support", "user"]
          )
        , ( 'lookalike_street'
          , ["support", "user"]
          )
        , ( 'messages'
          , ["support", "user"]
          )
        , ( 'name'
          , ["support", "user"]
          )
        , ( 'postalcode'
          , ["support", "user"]
          )
        , ( 'salutation'
          , ["support", "user"]
          )
        , ( 'street'
          , ["support", "user"]
          )
        , ( 'title'
          , ["support", "user"]
          )
        , ( 'valid'
          , ["support", "user"]
          )
        ]
      )
    , ( 'daily_record'
      , [ ( 'date'
          , ["user"]
          )
        , ( 'required_overtime'
          , ["user"]
          )
        , ( 'status'
          , ["user"]
          )
        , ( 'time_record'
          , ["user"]
          )
        , ( 'tr_duration_ok'
          , ["user"]
          )
        , ( 'user'
          , ["user"]
          )
        , ( 'weekend_allowed'
          , ["user"]
          )
        ]
      )
    , ( 'daily_record_freeze'
      , [ ( 'achieved_hours'
          , ["controlling", "hr"]
          )
        , ( 'balance'
          , ["controlling", "hr"]
          )
        , ( 'date'
          , ["controlling", "hr"]
          )
        , ( 'frozen'
          , ["controlling", "hr"]
          )
        , ( 'month_balance'
          , ["controlling", "hr"]
          )
        , ( 'month_validity_date'
          , ["controlling", "hr"]
          )
        , ( 'user'
          , ["controlling", "hr"]
          )
        , ( 'validity_date'
          , ["controlling", "hr"]
          )
        , ( 'week_balance'
          , ["controlling", "hr"]
          )
        ]
      )
    , ( 'daily_record_status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'department'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'doc_num'
          , ["user"]
          )
        , ( 'manager'
          , ["user"]
          )
        , ( 'messages'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'part_of'
          , ["user"]
          )
        , ( 'valid_from'
          , ["user"]
          )
        , ( 'valid_to'
          , ["user"]
          )
        ]
      )
    , ( 'doc'
      , [ ( 'artefact'
          , ["user"]
          )
        , ( 'department'
          , ["user"]
          )
        , ( 'document_nr'
          , ["user"]
          )
        , ( 'files'
          , ["user"]
          )
        , ( 'link'
          , ["user"]
          )
        , ( 'messages'
          , ["user"]
          )
        , ( 'nosy'
          , ["user"]
          )
        , ( 'product_type'
          , ["user"]
          )
        , ( 'reference'
          , ["user"]
          )
        , ( 'responsible'
          , ["user"]
          )
        , ( 'state_changed_by'
          , ["user"]
          )
        , ( 'status'
          , ["user"]
          )
        , ( 'title'
          , ["user"]
          )
        ]
      )
    , ( 'doc_status'
      , [ ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        , ( 'transitions'
          , ["user"]
          )
        ]
      )
    , ( 'file'
      , [ ( 'content'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'type'
          , ["user"]
          )
        ]
      )
    , ( 'issue'
      , [ ( 'area'
          , ["issue_admin", "user"]
          )
        , ( 'category'
          , ["issue_admin", "user"]
          )
        , ( 'closed'
          , ["issue_admin", "user"]
          )
        , ( 'composed_of'
          , ["issue_admin", "user"]
          )
        , ( 'confidential'
          , ["issue_admin", "user"]
          )
        , ( 'cur_est_begin'
          , ["issue_admin", "user"]
          )
        , ( 'cur_est_end'
          , ["issue_admin", "user"]
          )
        , ( 'deadline'
          , ["issue_admin", "user"]
          )
        , ( 'depends'
          , ["issue_admin", "user"]
          )
        , ( 'earliest_start'
          , ["issue_admin", "user"]
          )
        , ( 'effective_prio'
          , ["issue_admin", "user"]
          )
        , ( 'files'
          , ["issue_admin", "user"]
          )
        , ( 'files_affected'
          , ["issue_admin", "user"]
          )
        , ( 'fixed_in'
          , ["issue_admin", "user"]
          )
        , ( 'keywords'
          , ["issue_admin", "user"]
          )
        , ( 'kind'
          , ["issue_admin", "user"]
          )
        , ( 'maturity_index'
          , ["issue_admin", "user"]
          )
        , ( 'messages'
          , ["issue_admin", "user"]
          )
        , ( 'needs'
          , ["issue_admin", "user"]
          )
        , ( 'needs_doc'
          , ["issue_admin", "user"]
          )
        , ( 'nosy'
          , ["issue_admin", "user"]
          )
        , ( 'numeric_effort'
          , ["issue_admin", "user"]
          )
        , ( 'part_of'
          , ["issue_admin", "user"]
          )
        , ( 'planned_begin'
          , ["issue_admin", "user"]
          )
        , ( 'planned_end'
          , ["issue_admin", "user"]
          )
        , ( 'priority'
          , ["issue_admin", "user"]
          )
        , ( 'release'
          , ["issue_admin", "user"]
          )
        , ( 'responsible'
          , ["issue_admin", "user"]
          )
        , ( 'severity'
          , ["issue_admin", "user"]
          )
        , ( 'status'
          , ["issue_admin", "user"]
          )
        , ( 'superseder'
          , ["issue_admin", "user"]
          )
        , ( 'title'
          , ["issue_admin", "user"]
          )
        ]
      )
    , ( 'it_category'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'it_issue'
      , [ ( 'category'
          , ["it", "itview", "user"]
          )
        , ( 'confidential'
          , ["it", "itview", "user"]
          )
        , ( 'deadline'
          , ["it", "itview", "user"]
          )
        , ( 'files'
          , ["it", "itview", "user"]
          )
        , ( 'it_prio'
          , ["it", "itview", "user"]
          )
        , ( 'it_project'
          , ["it", "itview", "user"]
          )
        , ( 'messages'
          , ["it", "itview", "user"]
          )
        , ( 'nosy'
          , ["it", "itview", "user"]
          )
        , ( 'responsible'
          , ["it", "itview", "user"]
          )
        , ( 'stakeholder'
          , ["it", "itview", "user"]
          )
        , ( 'status'
          , ["it", "itview", "user"]
          )
        , ( 'superseder'
          , ["it", "itview", "user"]
          )
        , ( 'title'
          , ["it", "itview", "user"]
          )
        ]
      )
    , ( 'it_issue_status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        , ( 'relaxed'
          , ["user"]
          )
        , ( 'transitions'
          , ["user"]
          )
        ]
      )
    , ( 'it_prio'
      , [ ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        ]
      )
    , ( 'it_project'
      , [ ( 'category'
          , ["it", "itview", "user"]
          )
        , ( 'confidential'
          , ["it", "itview", "user"]
          )
        , ( 'deadline'
          , ["it", "itview", "user"]
          )
        , ( 'files'
          , ["it", "itview", "user"]
          )
        , ( 'it_prio'
          , ["it", "itview", "user"]
          )
        , ( 'messages'
          , ["it", "itview", "user"]
          )
        , ( 'nosy'
          , ["it", "itview", "user"]
          )
        , ( 'responsible'
          , ["it", "itview", "user"]
          )
        , ( 'stakeholder'
          , ["it", "itview", "user"]
          )
        , ( 'status'
          , ["it", "itview", "user"]
          )
        , ( 'title'
          , ["it", "itview", "user"]
          )
        ]
      )
    , ( 'it_project_status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        , ( 'transitions'
          , ["user"]
          )
        ]
      )
    , ( 'keyword'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'kind'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'location'
      , [ ( 'address'
          , ["user"]
          )
        , ( 'country'
          , ["user"]
          )
        , ( 'domain_part'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'meeting_room'
      , [ ( 'name'
          , ["user"]
          )
        , ( 'phone'
          , ["user"]
          )
        , ( 'room'
          , ["user"]
          )
        ]
      )
    , ( 'msg'
      , [ ( 'author'
          , ["user"]
          )
        , ( 'content'
          , ["user"]
          )
        , ( 'date'
          , ["user"]
          )
        , ( 'files'
          , ["user"]
          )
        , ( 'header'
          , ["user"]
          )
        , ( 'inreplyto'
          , ["user"]
          )
        , ( 'keywords'
          , ["user"]
          )
        , ( 'messageid'
          , ["user"]
          )
        , ( 'recipients'
          , ["user"]
          )
        , ( 'subject'
          , ["user"]
          )
        , ( 'summary'
          , ["user"]
          )
        , ( 'type'
          , ["user"]
          )
        ]
      )
    , ( 'msg_keyword'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'org_location'
      , [ ( 'location'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'organisation'
          , ["user"]
          )
        , ( 'phone'
          , ["user"]
          )
        ]
      )
    , ( 'organisation'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'mail_domain'
          , ["user"]
          )
        , ( 'messages'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'valid_from'
          , ["user"]
          )
        , ( 'valid_to'
          , ["user"]
          )
        ]
      )
    , ( 'overtime_correction'
      , [ ( 'comment'
          , ["controlling", "hr"]
          )
        , ( 'date'
          , ["controlling", "hr"]
          )
        , ( 'user'
          , ["controlling", "hr"]
          )
        , ( 'value'
          , ["controlling", "hr"]
          )
        ]
      )
    , ( 'overtime_period'
      , [ ( 'months'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        , ( 'weekly'
          , ["user"]
          )
        ]
      )
    , ( 'position'
      , [ ( 'position'
          , ["user"]
          )
        ]
      )
    , ( 'product_type'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'public_holiday'
      , [ ( 'date'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        , ( 'is_half'
          , ["user"]
          )
        , ( 'locations'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'query'
      , [ ( 'klass'
          , ["controlling", "user"]
          )
        , ( 'name'
          , ["controlling", "user"]
          )
        , ( 'private_for'
          , ["controlling", "user"]
          )
        , ( 'tmplate'
          , ["controlling", "user"]
          )
        , ( 'url'
          , ["controlling", "user"]
          )
        ]
      )
    , ( 'reference'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'room'
      , [ ( 'location'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'severity'
      , [ ( 'abbreviation'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        ]
      )
    , ( 'sex'
      , [ ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        , ( 'transitions'
          , ["user"]
          )
        ]
      )
    , ( 'status_transition'
      , [ ( 'name'
          , ["user"]
          )
        , ( 'require_msg'
          , ["user"]
          )
        , ( 'require_resp_change'
          , ["user"]
          )
        , ( 'target'
          , ["user"]
          )
        ]
      )
    , ( 'summary_report'
      , [ ( 'all_in'
          , ["user"]
          )
        , ( 'cost_center'
          , ["user"]
          )
        , ( 'cost_center_group'
          , ["user"]
          )
        , ( 'date'
          , ["user"]
          )
        , ( 'department'
          , ["user"]
          )
        , ( 'op_project'
          , ["user"]
          )
        , ( 'org_location'
          , ["user"]
          )
        , ( 'planned_effort'
          , ["user"]
          )
        , ( 'show_all_users'
          , ["user"]
          )
        , ( 'show_empty'
          , ["user"]
          )
        , ( 'show_missing'
          , ["user"]
          )
        , ( 'status'
          , ["user"]
          )
        , ( 'summary'
          , ["user"]
          )
        , ( 'summary_type'
          , ["user"]
          )
        , ( 'supervisor'
          , ["user"]
          )
        , ( 'time_project'
          , ["user"]
          )
        , ( 'time_wp'
          , ["user"]
          )
        , ( 'time_wp_group'
          , ["user"]
          )
        , ( 'user'
          , ["user"]
          )
        ]
      )
    , ( 'summary_type'
      , [ ( 'is_staff'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        ]
      )
    , ( 'sup_prio'
      , [ ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        ]
      )
    , ( 'sup_status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        , ( 'relaxed'
          , ["user"]
          )
        , ( 'transitions'
          , ["user"]
          )
        ]
      )
    , ( 'support'
      , [ ( 'category'
          , ["support", "user"]
          )
        , ( 'closed'
          , ["support", "user"]
          )
        , ( 'confidential'
          , ["support", "user"]
          )
        , ( 'customer'
          , ["support", "user"]
          )
        , ( 'files'
          , ["support", "user"]
          )
        , ( 'messages'
          , ["support", "user"]
          )
        , ( 'nosy'
          , ["support", "user"]
          )
        , ( 'numeric_effort'
          , ["support", "user"]
          )
        , ( 'prio'
          , ["support", "user"]
          )
        , ( 'related_issues'
          , ["support", "user"]
          )
        , ( 'release'
          , ["support", "user"]
          )
        , ( 'responsible'
          , ["support", "user"]
          )
        , ( 'serial_number'
          , ["support", "user"]
          )
        , ( 'status'
          , ["support", "user"]
          )
        , ( 'superseder'
          , ["support", "user"]
          )
        , ( 'title'
          , ["support", "user"]
          )
        ]
      )
    , ( 'time_activity'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'travel'
          , ["user"]
          )
        ]
      )
    , ( 'time_project'
      , [ ( 'department'
          , ["controlling", "project", "project_view"]
          )
        , ( 'deputy'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'description'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'is_public_holiday'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'max_hours'
          , ["controlling", "project", "project_view"]
          )
        , ( 'name'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'no_overtime'
          , ["controlling", "project", "project_view"]
          )
        , ( 'nosy'
          , ["controlling", "project", "project_view"]
          )
        , ( 'op_project'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'organisation'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'planned_effort'
          , ["controlling", "project", "project_view"]
          )
        , ( 'responsible'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'status'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'work_location'
          , ["controlling", "project", "project_view", "user"]
          )
        ]
      )
    , ( 'time_project_status'
      , [ ( 'active'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'time_record'
      , [ ( 'comment'
          , ["controlling", "hr", "user"]
          )
        , ( 'daily_record'
          , ["controlling", "hr", "user"]
          )
        , ( 'dist'
          , ["controlling", "hr", "user"]
          )
        , ( 'duration'
          , ["controlling", "hr", "user"]
          )
        , ( 'end'
          , ["controlling", "hr", "user"]
          )
        , ( 'end_generated'
          , ["controlling", "hr", "user"]
          )
        , ( 'start'
          , ["controlling", "hr", "user"]
          )
        , ( 'start_generated'
          , ["controlling", "hr", "user"]
          )
        , ( 'time_activity'
          , ["controlling", "hr", "user"]
          )
        , ( 'tr_duration'
          , ["controlling", "hr", "user"]
          )
        , ( 'work_location'
          , ["controlling", "hr", "user"]
          )
        , ( 'wp'
          , ["controlling", "hr", "user"]
          )
        ]
      )
    , ( 'time_wp'
      , [ ( 'bookers'
          , ["controlling", "project", "project_view"]
          )
        , ( 'cost_center'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'description'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'durations_allowed'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'name'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'planned_effort'
          , ["controlling", "project", "project_view"]
          )
        , ( 'project'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'responsible'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'time_end'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'time_start'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'travel'
          , ["controlling", "project", "project_view", "user"]
          )
        , ( 'wp_no'
          , ["controlling", "project", "project_view", "user"]
          )
        ]
      )
    , ( 'time_wp_group'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'wps'
          , ["user"]
          )
        ]
      )
    , ( 'user'
      , [ ( 'address'
          , ["user"]
          )
        , ( 'alternate_addresses'
          , ["user"]
          )
        , ( 'clearance_by'
          , ["user"]
          )
        , ( 'department'
          , ["user"]
          )
        , ( 'external_phone'
          , ["user"]
          )
        , ( 'firstname'
          , ["user"]
          )
        , ( 'internal_phone'
          , ["user"]
          )
        , ( 'job_description'
          , ["user"]
          )
        , ( 'lastname'
          , ["user"]
          )
        , ( 'lunch_duration'
          , ["user"]
          )
        , ( 'lunch_start'
          , ["user"]
          )
        , ( 'nickname'
          , ["user"]
          )
        , ( 'org_location'
          , []
          )
        , ( 'password'
          , ["user"]
          )
        , ( 'phone'
          , ["user"]
          )
        , ( 'pictures'
          , ["user"]
          )
        , ( 'position'
          , ["user"]
          )
        , ( 'private_mobile'
          , []
          )
        , ( 'private_mobile_visible'
          , ["user"]
          )
        , ( 'private_phone'
          , []
          )
        , ( 'private_phone_visible'
          , ["user"]
          )
        , ( 'queries'
          , ["user"]
          )
        , ( 'quick_dialling'
          , ["user"]
          )
        , ( 'realname'
          , ["user"]
          )
        , ( 'roles'
          , ["controlling"]
          )
        , ( 'room'
          , ["user"]
          )
        , ( 'sex'
          , ["user"]
          )
        , ( 'status'
          , ["user"]
          )
        , ( 'subst_active'
          , ["user"]
          )
        , ( 'substitute'
          , ["user"]
          )
        , ( 'supervisor'
          , ["user"]
          )
        , ( 'timezone'
          , ["user"]
          )
        , ( 'timing_info'
          , []
          )
        , ( 'title'
          , ["user"]
          )
        , ( 'tt_lines'
          , ["user"]
          )
        , ( 'username'
          , ["user"]
          )
        ]
      )
    , ( 'user_dynamic'
      , [ ( 'additional_hours'
          , ["hr"]
          )
        , ( 'all_in'
          , ["hr"]
          )
        , ( 'booking_allowed'
          , ["hr"]
          )
        , ( 'daily_worktime'
          , ["hr"]
          )
        , ( 'department'
          , ["hr"]
          )
        , ( 'durations_allowed'
          , ["hr"]
          )
        , ( 'hours_fri'
          , ["hr"]
          )
        , ( 'hours_mon'
          , ["hr"]
          )
        , ( 'hours_sat'
          , ["hr"]
          )
        , ( 'hours_sun'
          , ["hr"]
          )
        , ( 'hours_thu'
          , ["hr"]
          )
        , ( 'hours_tue'
          , ["hr"]
          )
        , ( 'hours_wed'
          , ["hr"]
          )
        , ( 'org_location'
          , ["hr"]
          )
        , ( 'overtime_period'
          , ["hr"]
          )
        , ( 'supp_per_period'
          , ["hr"]
          )
        , ( 'supp_weekly_hours'
          , ["hr"]
          )
        , ( 'travel_full'
          , ["hr"]
          )
        , ( 'user'
          , ["hr"]
          )
        , ( 'vacation_remaining'
          , ["hr"]
          )
        , ( 'vacation_yearly'
          , ["hr"]
          )
        , ( 'valid_from'
          , ["hr"]
          )
        , ( 'valid_to'
          , ["hr"]
          )
        , ( 'weekend_allowed'
          , ["hr"]
          )
        , ( 'weekly_hours'
          , ["hr"]
          )
        ]
      )
    , ( 'user_status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'valid'
      , [ ( 'description'
          , ["adr_readonly", "user"]
          )
        , ( 'name'
          , ["adr_readonly", "user"]
          )
        ]
      )
    , ( 'work_location'
      , [ ( 'code'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
