properties = \
    [ ( 'absence'
      , [ 'absence_type'
        , 'first_day'
        , 'last_day'
        , 'user'
        ]
      )
    , ( 'absence_type'
      , [ 'code'
        , 'cssclass'
        , 'description'
        ]
      )
    , ( 'analysis_result'
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
    , ( 'attendance_record'
      , [ 'daily_record'
        , 'dist'
        , 'end'
        , 'end_generated'
        , 'start'
        , 'start_generated'
        , 'work_location'
        ]
      )
    , ( 'auto_wp'
      , [ 'all_in'
        , 'contract_type'
        , 'duration'
        , 'durations_allowed'
        , 'is_valid'
        , 'name'
        , 'org_location'
        , 'time_project'
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
    , ( 'cc_bu_category'
      , [ 'description'
        , 'name'
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
        , 'group_external'
        , 'name'
        , 'order'
        ]
      )
    , ( 'cost_center'
      , [ 'cc_bu_category'
        , 'cost_center_group'
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
    , ( 'cost_center_permission_group'
      , [ 'cost_center'
        , 'description'
        , 'name'
        , 'permission_for'
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
      , [ 'attendance_record'
        , 'date'
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
    , ( 'doc'
      , [ 'artefact'
        , 'doc_category'
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
    , ( 'doc_category'
      , [ 'doc_num'
        , 'name'
        , 'valid'
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
        , 'rq_link'
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
    , ( 'file'
      , [ 'content'
        , 'name'
        , 'type'
        ]
      )
    , ( 'functional_role'
      , [ 'name'
        , 'name_group'
        , 'rank'
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
        , 'confidential'
        , 'deadline'
        , 'files'
        , 'int_prio'
        , 'it_prio'
        , 'it_project'
        , 'it_request_type'
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
        , 'city'
        , 'country'
        , 'domain_part'
        , 'name'
        , 'room_prefix'
        , 'valid_from'
        , 'valid_to'
        , 'weekly_hours_fte'
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
    , ( 'org_group'
      , [ 'name'
        ]
      )
    , ( 'org_location'
      , [ 'do_auto_wp'
        , 'do_leave_process'
        , 'location'
        , 'name'
        , 'organisation'
        , 'phone'
        , 'sap_lifnr'
        , 'vac_aliq'
        , 'vacation_legal_year'
        , 'vacation_yearly'
        , 'valid_from'
        , 'valid_to'
        ]
      )
    , ( 'organisation'
      , [ 'company_code'
        , 'description'
        , 'mail_domain'
        , 'may_purchase'
        , 'messages'
        , 'name'
        , 'org_group'
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
        , 'valid'
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
      , [ 'description'
        , 'location'
        , 'name'
        ]
      )
    , ( 'safety_level'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'sap_cc'
      , [ 'deputy'
        , 'description'
        , 'group_lead'
        , 'name'
        , 'nosy'
        , 'organisation'
        , 'purchasing_agents'
        , 'responsible'
        , 'sap_cc_category'
        , 'team_lead'
        , 'valid'
        ]
      )
    , ( 'sap_cc_category'
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
    , ( 'summary_report'
      , [ 'all_in'
        , 'cost_center'
        , 'cost_center_group'
        , 'date'
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
        , 'time_wp_summary_no'
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
    , ( 'time_activity'
      , [ 'description'
        , 'is_valid'
        , 'name'
        , 'time_activity_perm'
        , 'travel'
        ]
      )
    , ( 'time_activity_perm'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'time_project'
      , [ 'approval_hr'
        , 'approval_required'
        , 'cost_center'
        , 'deputy'
        , 'description'
        , 'group_lead'
        , 'infosec_req'
        , 'is_extern'
        , 'is_public_holiday'
        , 'is_special_leave'
        , 'is_vacation'
        , 'max_hours'
        , 'name'
        , 'no_overtime'
        , 'no_overtime_day'
        , 'nosy'
        , 'only_hours'
        , 'op_project'
        , 'organisation'
        , 'overtime_reduction'
        , 'planned_effort'
        , 'product_family'
        , 'project_type'
        , 'purchasing_agents'
        , 'reporting_group'
        , 'responsible'
        , 'status'
        , 'team_lead'
        , 'work_location'
        , 'wps'
        ]
      )
    , ( 'time_project_status'
      , [ 'active'
        , 'description'
        , 'name'
        ]
      )
    , ( 'time_record'
      , [ 'attendance_record'
        , 'comment'
        , 'daily_record'
        , 'dist'
        , 'duration'
        , 'end'
        , 'end_generated'
        , 'metadata'
        , 'start'
        , 'start_generated'
        , 'time_activity'
        , 'tr_duration'
        , 'work_location'
        , 'wp'
        ]
      )
    , ( 'time_report'
      , [ 'file'
        , 'last_updated'
        , 'time_project'
        ]
      )
    , ( 'time_wp'
      , [ 'auto_wp'
        , 'bookers'
        , 'cost_center'
        , 'description'
        , 'durations_allowed'
        , 'epic_key'
        , 'has_expiration_date'
        , 'is_extern'
        , 'is_public'
        , 'name'
        , 'planned_effort'
        , 'project'
        , 'responsible'
        , 'time_end'
        , 'time_start'
        , 'time_wp_summary_no'
        , 'wp_no'
        ]
      )
    , ( 'time_wp_group'
      , [ 'description'
        , 'name'
        , 'wps'
        ]
      )
    , ( 'time_wp_summary_no'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'timesheet'
      , [ 'first_day'
        , 'last_day'
        , 'supervisor'
        , 'user'
        ]
      )
    , ( 'uc_type'
      , [ 'description'
        , 'is_email'
        , 'name'
        , 'order'
        , 'url_template'
        , 'visible'
        ]
      )
    , ( 'user'
      , [ 'ad_domain'
        , 'address'
        , 'alternate_addresses'
        , 'business_responsible'
        , 'clearance_by'
        , 'contacts'
        , 'csv_delimiter'
        , 'department_temp'
        , 'entry_date'
        , 'firstname'
        , 'guid'
        , 'hide_message_files'
        , 'job_description'
        , 'lastname'
        , 'lunch_duration'
        , 'lunch_start'
        , 'nickname'
        , 'password'
        , 'pictures'
        , 'planning_role'
        , 'position_text'
        , 'queries'
        , 'realname'
        , 'reduced_activity_list'
        , 'roles'
        , 'room'
        , 'scale_seniority'
        , 'sex'
        , 'status'
        , 'subst_active'
        , 'substitute'
        , 'supervisor'
        , 'sync_foreign_key'
        , 'timetracking_by'
        , 'timezone'
        , 'timing_info'
        , 'tt_lines'
        , 'username'
        , 'vie_user'
        , 'vie_user_bl_override'
        , 'vie_user_ml'
        ]
      )
    , ( 'user_contact'
      , [ 'contact'
        , 'contact_type'
        , 'description'
        , 'order'
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
        , 'do_auto_wp'
        , 'durations_allowed'
        , 'exemption'
        , 'hours_fri'
        , 'hours_mon'
        , 'hours_sat'
        , 'hours_sun'
        , 'hours_thu'
        , 'hours_tue'
        , 'hours_wed'
        , 'max_flexitime'
        , 'org_location'
        , 'overtime_period'
        , 'sap_cc'
        , 'short_time_work_hours'
        , 'supp_per_period'
        , 'supp_weekly_hours'
        , 'time_activity_perm'
        , 'travel_full'
        , 'user'
        , 'vac_aliq'
        , 'vacation_day'
        , 'vacation_month'
        , 'vacation_yearly'
        , 'valid_from'
        , 'valid_to'
        , 'weekend_allowed'
        , 'weekly_hours'
        ]
      )
    , ( 'user_functional_role'
      , [ 'functional_role'
        , 'ratio'
        , 'user'
        ]
      )
    , ( 'user_status'
      , [ 'description'
        , 'is_internal'
        , 'is_nosy'
        , 'is_system'
        , 'ldap_group'
        , 'ldap_prio'
        , 'name'
        , 'roles'
        , 'timetracking_allowed'
        ]
      )
    , ( 'vac_aliq'
      , [ 'name'
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
        , 'flexi_max'
        , 'flexi_rem'
        , 'flexi_sub'
        , 'flexi_time'
        , 'org_location'
        , 'organisation'
        , 'show_obsolete'
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
        print (cl)
        for p in props :
            print ('    ', p)
