properties = \
    [ ( 'department'
      , [ 'deputy'
        , 'deputy_gets_mail'
        , 'description'
        , 'manager'
        , 'name'
        , 'no_approval'
        , 'nosy'
        , 'part_of'
        , 'valid_from'
        , 'valid_to'
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
    , ( 'file'
      , [ 'content'
        , 'name'
        , 'type'
        ]
      )
    , ( 'infosec_level'
      , [ 'is_consulting'
        , 'name'
        , 'order'
        ]
      )
    , ( 'internal_order'
      , [ 'name'
        , 'order_number'
        , 'valid'
        ]
      )
    , ( 'location'
      , [ 'address'
        , 'city'
        , 'country'
        , 'name'
        , 'order'
        , 'sync_id'
        , 'valid_from'
        , 'valid_to'
        ]
      )
    , ( 'msg'
      , [ 'author'
        , 'content'
        , 'date'
        , 'files'
        , 'inreplyto'
        , 'messageid'
        , 'recipients'
        , 'summary'
        , 'type'
        ]
      )
    , ( 'o_permission'
      , [ 'organisation'
        , 'user'
        ]
      )
    , ( 'org_location'
      , [ 'location'
        , 'name'
        , 'organisation'
        , 'sync_id'
        , 'valid_from'
        , 'valid_to'
        ]
      )
    , ( 'organisation'
      , [ 'company_code'
        , 'description'
        , 'may_purchase'
        , 'name'
        , 'sync_id'
        , 'valid_from'
        , 'valid_to'
        ]
      )
    , ( 'part_of_budget'
      , [ 'description'
        , 'name'
        , 'order'
        ]
      )
    , ( 'payment_type'
      , [ 'name'
        , 'need_approval'
        , 'order'
        ]
      )
    , ( 'pg_category'
      , [ 'name'
        , 'sap_ref'
        ]
      )
    , ( 'pr_approval'
      , [ 'by'
        , 'date'
        , 'deputy'
        , 'deputy_gets_mail'
        , 'description'
        , 'msg'
        , 'order'
        , 'purchase_request'
        , 'role'
        , 'role_id'
        , 'status'
        , 'user'
        ]
      )
    , ( 'pr_approval_config'
      , [ 'amount'
        , 'departments'
        , 'if_not_in_las'
        , 'infosec_amount'
        , 'oob_amount'
        , 'organisations'
        , 'payment_type_amount'
        , 'pr_ext_resource'
        , 'purchase_type'
        , 'quality_amount'
        , 'role'
        , 'valid'
        ]
      )
    , ( 'pr_approval_order'
      , [ 'is_board'
        , 'is_finance'
        , 'is_quality'
        , 'only_nosy'
        , 'order'
        , 'role'
        , 'users'
        , 'want_no_messages'
        ]
      )
    , ( 'pr_approval_status'
      , [ 'name'
        , 'order'
        , 'transitions'
        ]
      )
    , ( 'pr_currency'
      , [ 'description'
        , 'exchange_rate'
        , 'key_currency'
        , 'max_group'
        , 'max_team'
        , 'min_sum'
        , 'name'
        , 'order'
        ]
      )
    , ( 'pr_ext_resource'
      , [ 'name'
        ]
      )
    , ( 'pr_offer_item'
      , [ 'add_to_las'
        , 'description'
        , 'gl_account'
        , 'index'
        , 'infosec_level'
        , 'internal_order'
        , 'is_asset'
        , 'offer_number'
        , 'payment_type'
        , 'pr_currency'
        , 'pr_supplier'
        , 'price_per_unit'
        , 'product_group'
        , 'psp_element'
        , 'purchase_type'
        , 'sap_cc'
        , 'supplier'
        , 'time_project'
        , 'units'
        , 'vat'
        ]
      )
    , ( 'pr_rating_category'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'pr_status'
      , [ 'name'
        , 'order'
        , 'relaxed'
        , 'transitions'
        ]
      )
    , ( 'pr_supplier'
      , [ 'name'
        , 'sap_ref'
        ]
      )
    , ( 'pr_supplier_rating'
      , [ 'organisation'
        , 'rating'
        , 'scope'
        , 'supplier'
        ]
      )
    , ( 'pr_supplier_risk'
      , [ 'organisation'
        , 'security_req_group'
        , 'supplier'
        , 'supplier_risk_category'
        ]
      )
    , ( 'product_group'
      , [ 'infosec_level'
        , 'name'
        , 'pg_category'
        , 'sap_ref'
        , 'security_req_group'
        ]
      )
    , ( 'psp_element'
      , [ 'name'
        , 'number'
        , 'organisation'
        , 'project'
        , 'project_org'
        , 'valid'
        ]
      )
    , ( 'purchase_request'
      , [ 'approvals'
        , 'charge_to'
        , 'continuous_obligation'
        , 'contract_term'
        , 'date_approved'
        , 'date_ordered'
        , 'date_progress'
        , 'delivery_address'
        , 'delivery_deadline'
        , 'department'
        , 'files'
        , 'frame_purchase'
        , 'frame_purchase_end'
        , 'gl_account'
        , 'infosec_level'
        , 'infosec_project'
        , 'intended_duration'
        , 'internal_order'
        , 'issue_ids'
        , 'messages'
        , 'nosy'
        , 'offer_items'
        , 'organisation'
        , 'part_of_budget'
        , 'payment_type'
        , 'pr_currency'
        , 'pr_ext_resource'
        , 'pr_justification'
        , 'pr_risks'
        , 'psp_element'
        , 'purchase_risk_type'
        , 'purchase_type'
        , 'purchasing_agents'
        , 'renegotiations'
        , 'renew_until'
        , 'requester'
        , 'responsible'
        , 'safety_critical'
        , 'sap_cc'
        , 'sap_reference'
        , 'special_approval'
        , 'status'
        , 'termination_date'
        , 'terms_conditions'
        , 'time_project'
        , 'title'
        , 'total_cost'
        ]
      )
    , ( 'purchase_risk_type'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'purchase_security_risk'
      , [ 'infosec_level'
        , 'purchase_risk_type'
        , 'supplier_risk_category'
        ]
      )
    , ( 'purchase_type'
      , [ 'allow_gl_account'
        , 'confidential'
        , 'description'
        , 'name'
        , 'nosy'
        , 'order'
        , 'organisations'
        , 'pr_edit_roles'
        , 'pr_forced_roles'
        , 'pr_roles'
        , 'pr_view_roles'
        , 'purchasing_agents'
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
    , ( 'sap_cc'
      , [ 'deputy'
        , 'deputy_gets_mail'
        , 'description'
        , 'group_lead'
        , 'name'
        , 'nosy'
        , 'organisation'
        , 'purchasing_agents'
        , 'responsible'
        , 'sync_id'
        , 'team_lead'
        , 'valid'
        ]
      )
    , ( 'security_req_group'
      , [ 'is_consulting'
        , 'name'
        ]
      )
    , ( 'supplier_risk_category'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'terms_conditions'
      , [ 'description'
        , 'name'
        , 'order'
        ]
      )
    , ( 'time_project'
      , [ 'deputy'
        , 'deputy_gets_mail'
        , 'description'
        , 'group_lead'
        , 'infosec_req'
        , 'name'
        , 'nosy'
        , 'organisation'
        , 'purchasing_agents'
        , 'responsible'
        , 'status'
        , 'sync_id'
        , 'team_lead'
        ]
      )
    , ( 'time_project_status'
      , [ 'active'
        , 'description'
        , 'name'
        , 'sync_id'
        ]
      )
    , ( 'user'
      , [ 'ad_domain'
        , 'address'
        , 'alternate_addresses'
        , 'business_responsible'
        , 'clearance_by'
        , 'csv_delimiter'
        , 'guid'
        , 'hide_message_files'
        , 'organisation'
        , 'password'
        , 'queries'
        , 'realname'
        , 'roles'
        , 'status'
        , 'subst_until'
        , 'substitute'
        , 'supervisor'
        , 'timezone'
        , 'username'
        , 'want_no_messages'
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
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print (cl)
        for p in props :
            print ('    ', p)
