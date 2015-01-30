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
    , ( 'artefact'
      , [ 'description'
        , 'filename_format'
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
    , ( 'contract_type'
      , [ 'description'
        , 'name'
        , 'order'
        ]
      )
    , ( 'cost_center'
      , [ 'cost_center_group'
        , 'description'
        , 'name'
        , 'status'
        ]
      )
    , ( 'cost_center_group'
      , [ 'active'
        , 'description'
        , 'name'
        , 'responsible'
        ]
      )
    , ( 'cost_center_status'
      , [ 'active'
        , 'description'
        , 'name'
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
    , ( 'daily_record'
      , [ 'date'
        , 'required_overtime'
        , 'status'
        , 'time_record'
        , 'tr_duration_ok'
        , 'user'
        , 'weekend_allowed'
        ]
      )
    , ( 'daily_record_freeze'
      , [ 'achieved_hours'
        , 'balance'
        , 'date'
        , 'frozen'
        , 'month_balance'
        , 'month_validity_date'
        , 'user'
        , 'validity_date'
        , 'week_balance'
        ]
      )
    , ( 'daily_record_status'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'department'
      , [ 'description'
        , 'doc_num'
        , 'manager'
        , 'messages'
        , 'name'
        , 'part_of'
        , 'valid_from'
        , 'valid_to'
        ]
      )
    , ( 'doc'
      , [ 'artefact'
        , 'department'
        , 'document_nr'
        , 'files'
        , 'link'
        , 'messages'
        , 'nosy'
        , 'product_type'
        , 'reference'
        , 'responsible'
        , 'state_changed_by'
        , 'status'
        , 'title'
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
    , ( 'doc_status'
      , [ 'name'
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
    , ( 'leave_status'
      , [ 'name'
        , 'order'
        , 'transitions'
        ]
      )
    , ( 'leave_submission'
      , [ 'approval_hr'
        , 'comment'
        , 'comment_cancel'
        , 'first_day'
        , 'last_day'
        , 'status'
        , 'time_wp'
        , 'user'
        ]
      )
    , ( 'location'
      , [ 'address'
        , 'country'
        , 'domain_part'
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
    , ( 'org_location'
      , [ 'location'
        , 'name'
        , 'organisation'
        , 'phone'
        , 'vacation_legal_year'
        , 'vacation_yearly'
        ]
      )
    , ( 'organisation'
      , [ 'description'
        , 'mail_domain'
        , 'messages'
        , 'name'
        , 'valid_from'
        , 'valid_to'
        ]
      )
    , ( 'overtime_correction'
      , [ 'comment'
        , 'date'
        , 'user'
        , 'value'
        ]
      )
    , ( 'overtime_period'
      , [ 'months'
        , 'name'
        , 'order'
        , 'required_overtime'
        , 'weekly'
        ]
      )
    , ( 'position'
      , [ 'position'
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
    , ( 'product_family'
      , [ 'description'
        , 'name'
        , 'responsible'
        ]
      )
    , ( 'product_type'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'project_type'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'public_holiday'
      , [ 'date'
        , 'description'
        , 'is_half'
        , 'locations'
        , 'name'
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
    , ( 'reference'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'reporting_group'
      , [ 'description'
        , 'name'
        , 'responsible'
        ]
      )
    , ( 'return_type'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'room'
      , [ 'contacts'
        , 'location'
        , 'name'
        ]
      )
    , ( 'sap_cc'
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
    , ( 'sex'
      , [ 'name'
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
    , ( 'summary_report'
      , [ 'all_in'
        , 'cost_center'
        , 'cost_center_group'
        , 'date'
        , 'department'
        , 'op_project'
        , 'org_location'
        , 'organisation'
        , 'planned_effort'
        , 'product_family'
        , 'project_type'
        , 'reporting_group'
        , 'sap_cc'
        , 'show_all_users'
        , 'show_empty'
        , 'show_missing'
        , 'status'
        , 'summary'
        , 'summary_type'
        , 'supervisor'
        , 'time_project'
        , 'time_wp'
        , 'time_wp_group'
        , 'user'
        ]
      )
    , ( 'summary_type'
      , [ 'is_staff'
        , 'name'
        , 'order'
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
    , ( 'time_activity'
      , [ 'description'
        , 'name'
        , 'travel'
        ]
      )
    , ( 'time_project'
      , [ 'approval_hr'
        , 'approval_required'
        , 'cost_center'
        , 'department'
        , 'deputy'
        , 'description'
        , 'is_public_holiday'
        , 'is_special_leave'
        , 'is_vacation'
        , 'max_hours'
        , 'name'
        , 'no_overtime'
        , 'nosy'
        , 'op_project'
        , 'organisation'
        , 'overtime_reduction'
        , 'planned_effort'
        , 'product_family'
        , 'project_type'
        , 'reporting_group'
        , 'responsible'
        , 'status'
        , 'work_location'
        ]
      )
    , ( 'time_project_status'
      , [ 'active'
        , 'description'
        , 'name'
        ]
      )
    , ( 'time_record'
      , [ 'comment'
        , 'daily_record'
        , 'dist'
        , 'duration'
        , 'end'
        , 'end_generated'
        , 'start'
        , 'start_generated'
        , 'time_activity'
        , 'tr_duration'
        , 'work_location'
        , 'wp'
        ]
      )
    , ( 'time_wp'
      , [ 'bookers'
        , 'cost_center'
        , 'description'
        , 'durations_allowed'
        , 'is_public'
        , 'name'
        , 'planned_effort'
        , 'project'
        , 'responsible'
        , 'time_end'
        , 'time_start'
        , 'travel'
        , 'wp_no'
        ]
      )
    , ( 'time_wp_group'
      , [ 'description'
        , 'name'
        , 'wps'
        ]
      )
    , ( 'uc_type'
      , [ 'description'
        , 'name'
        , 'order'
        , 'url_template'
        , 'visible'
        ]
      )
    , ( 'user'
      , [ 'address'
        , 'alternate_addresses'
        , 'clearance_by'
        , 'contacts'
        , 'csv_delimiter'
        , 'department'
        , 'firstname'
        , 'job_description'
        , 'lastname'
        , 'lunch_duration'
        , 'lunch_start'
        , 'nickname'
        , 'org_location'
        , 'password'
        , 'pictures'
        , 'position'
        , 'queries'
        , 'realname'
        , 'roles'
        , 'room'
        , 'sex'
        , 'status'
        , 'subst_active'
        , 'substitute'
        , 'supervisor'
        , 'timezone'
        , 'timing_info'
        , 'title'
        , 'tt_lines'
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
    , ( 'user_dynamic'
      , [ 'additional_hours'
        , 'all_in'
        , 'booking_allowed'
        , 'contract_type'
        , 'daily_worktime'
        , 'department'
        , 'durations_allowed'
        , 'hours_fri'
        , 'hours_mon'
        , 'hours_sat'
        , 'hours_sun'
        , 'hours_thu'
        , 'hours_tue'
        , 'hours_wed'
        , 'org_location'
        , 'overtime_period'
        , 'sap_cc'
        , 'supp_per_period'
        , 'supp_weekly_hours'
        , 'travel_full'
        , 'user'
        , 'vacation_day'
        , 'vacation_month'
        , 'vacation_yearly'
        , 'valid_from'
        , 'valid_to'
        , 'weekend_allowed'
        , 'weekly_hours'
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
    , ( 'vacation_correction'
      , [ 'absolute'
        , 'comment'
        , 'contract_type'
        , 'date'
        , 'days'
        , 'user'
        ]
      )
    , ( 'vacation_report'
      , [ 'additional_submitted'
        , 'approved_submissions'
        , 'date'
        , 'department'
        , 'flexi_sub'
        , 'flexi_time'
        , 'org_location'
        , 'organisation'
        , 'special_leave'
        , 'special_sub'
        , 'supervisor'
        , 'time_project'
        , 'user'
        ]
      )
    , ( 'work_location'
      , [ 'code'
        , 'description'
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
